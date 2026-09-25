"""Draft, check and (on Tom's word) apply corrections for the English Language student-walk findings.

25 Sep 2026. Every click-and-choose question the examiner model ruled key_wrong, ambiguous or
unanswerable gets a corrected question object drafted by Opus (subscription), then:
  1. a mechanical check that the object still fits the renderer (same input type, same fields,
     answer indices in range, a traffic-light has at least two categories), and
  2. a second, independent Opus pass that sees the passage and the corrected question WITH its key
     and rules whether the key is now the one defensible answer.
Nothing touches Supabase until `apply` is run, which backs every lesson row up first.

  python scripts/_studentwalk_draft_fixes.py draft     -> scripts/_studentwalk_fixdrafts.json
  python scripts/_studentwalk_draft_fixes.py check     -> adds "check" to each draft
  python scripts/_studentwalk_draft_fixes.py report    -> scripts/_studentwalk_fixes_review.md
  python scripts/_studentwalk_draft_fixes.py apply     (only with Tom's go-ahead)
"""
import io, json, os, sys, time, urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("SV_WALK_DIR", os.path.join(HERE, "_studentwalk_fixwork"))
os.environ.setdefault("SV_WALK_BUDGET", "400")   # Tom 25 Sep: allowance is not the constraint
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util
_spec = importlib.util.spec_from_file_location("walk", os.path.join(HERE, "_qa_student_walk.py"))
walk = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(walk)

BOARDS = ("english-language-edexcel", "english-language-aqa", "english-language-ocr", "english-language-eduqas",
          "english-language")
AI = walk.AI_TYPES
DRAFTS = os.path.join(HERE, "_studentwalk_fixdrafts.json")
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}


def rest(path, method="GET", body=None):
    req = urllib.request.Request(U + "/rest/v1/" + path, method=method, headers=dict(H, **{
        "Content-Type": "application/json", "Prefer": "return=minimal"}), data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=120) as r:
        t = r.read()
        return json.loads(t) if t else None


def lesson(sub, unit, n):
    return rest("lessons?select=id,practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                "&units.slug=eq.%s&lesson_number=eq.%s" % (sub, unit, n))[0]


def findings():
    out = []
    for sub in BOARDS:
        d = os.path.join(HERE, "_studentwalk_" + sub)
        v = json.load(io.open(os.path.join(d, "views.json"), encoding="utf-8"))
        a = json.load(io.open(os.path.join(d, "adjudications.json"), encoding="utf-8"))
        at = json.load(io.open(os.path.join(d, "attempts.json"), encoding="utf-8"))
        for k, x in a.items():
            if k in v and v[k]["type"] not in AI and (x or {}).get("finding") in ("key_wrong", "ambiguous", "unanswerable"):
                out.append({"key": k, "view": v[k], "ruling": x, "attempt": at.get(k, {})})
    return out


DRAFT_SYS = """You are a senior GCSE English Language examiner repairing one practice question on a revision
website. A careful Year 11 student answered it blind and an examiner ruled the question faulty. You
see what the student saw, the stored question object (JSON) with its answer key, the student's
attempt and the examiner's ruling and suggested fix.

Repair the question so that a careful student reading only what is on screen can reach exactly one
defensible answer, and the key is that answer. Prefer the smallest change: correct a wrong key;
reword a question or option that leads a sound reader astray; add a missing category list or
restore missing text in the question itself. Never refer to text that is not on the student's screen.
Keep the JSON shape exactly: same input_type, same field names, same kinds of values; you may add
"categories" (a list of every category name) to a traffic_light question. Keep British spelling and
the site's GCSE register. If the examiner is wrong and the question is sound, say so.

Reply with ONE JSON object and nothing else:
{"action": "patch" | "no_change",
 "question": <the full corrected question object, or null for no_change>,
 "change": "one or two plain sentences saying what changed and why, for the teacher"}"""

CHECK_SYS = """You are a second, independent GCSE English Language examiner. You see a passage (if any) and one
practice question with its answer key, after a colleague repaired it. Decide whether a careful Year 11
student reading only the passage and the question could reach exactly one defensible answer, and
whether the stored key is that answer. Check every option, statement, token or pair, not only the
changed ones. Be strict: a key that is arguably wrong, or a second defensible answer, is a fail.

Reply with ONE JSON object and nothing else:
{"verdict": "pass" | "fail", "why": "one or two plain sentences", "confidence": 0.0-1.0}"""


def cmd_draft():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8")) if os.path.exists(DRAFTS) else {}
    items, cache = [], {}
    for f in findings():
        k, v = f["key"], f["view"]
        if k in drafts and drafts[k].get("draft"): continue
        lk = (v["subject"], v["unit"], v["n"])
        if lk not in cache: cache[lk] = lesson(*lk)
        q = cache[lk]["practice_data"]["problem_bank"][v["tier"]][v["i"]]
        drafts[k] = {"lesson_id": cache[lk]["id"], "tier": v["tier"], "i": v["i"], "type": v["type"],
                     "ruling": f["ruling"], "original": q}
        body = "\n\n".join([
            "WHAT THE STUDENT SAW:\n" + walk.view_prompt(v),
            "STORED QUESTION OBJECT:\n" + json.dumps(q, ensure_ascii=False, indent=1),
            "THE STUDENT'S ATTEMPT:\n" + json.dumps(f["attempt"], ensure_ascii=False)[:3000],
            "THE EXAMINER'S RULING:\n" + json.dumps(f["ruling"], ensure_ascii=False)])
        items.append((k, body))
    items = items[:int(os.environ.get("SV_FIX_LIMIT", "100000"))]
    print("drafting %d corrections" % len(items), flush=True)
    try:
        for res in walk.via_subscription("fixdraft", DRAFT_SYS, items, "opus", 3):
            for k, d in res.items(): drafts[k]["draft"] = d
            io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    finally:
        io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
        print("drafts on file: %d" % sum(1 for d in drafts.values() if d.get("draft")))


def mech(orig, new):
    """Does the corrected object still fit the renderer? Returns a list of problems."""
    p = []
    if not isinstance(new, dict): return ["not an object"]
    if new.get("input_type") != orig.get("input_type"): p.append("input_type changed")
    extra = set(new) - set(orig) - {"categories"}
    if extra: p.append("new fields: %s" % sorted(extra))
    missing = set(orig) - set(new)
    if missing: p.append("dropped fields: %s" % sorted(missing))
    t = new.get("input_type")
    if t == "multiple_choice":
        opts = new.get("options") or []
        c = new.get("correct")
        if isinstance(c, int) and not (0 <= c < len(opts)): p.append("correct index out of range")
        if isinstance(c, str) and opts and c not in opts: p.append("correct not among options")
    if t == "traffic_light":
        st = new.get("statements") or []
        cats = set(new.get("categories") or []) | {s.get("correct") for s in st}
        if len(cats) < 2: p.append("fewer than two categories on offer")
        if new.get("categories") and any(s.get("correct") not in new["categories"] for s in st):
            p.append("an answer uses a category not in the list")
    if t == "evidence_match":
        n = len(new.get("claims") or [])
        for qu in new.get("quotes") or []:
            if not (-1 <= qu.get("correctClaim", -9) < n): p.append("correctClaim out of range")
    return p


def cmd_check():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    items = []
    for k, d in drafts.items():
        dr = d.get("draft") or {}
        if dr.get("action") != "patch" or d.get("check"): continue
        d["mech"] = mech(d["original"], dr.get("question"))
        if d["mech"]: continue
        sub, unit, n = k.split("/")[:3]
        v = json.load(io.open(os.path.join(HERE, "_studentwalk_" + sub, "views.json"), encoding="utf-8"))[k]
        body = ("PASSAGE ON SCREEN:\n%s\n\nQUESTION WITH ITS KEY:\n%s" %
                ("\n\n".join(x for x in (v.get("panel"), v.get("highlight_text")) if x) or "(none)",
                 json.dumps(dr["question"], ensure_ascii=False, indent=1)))
        items.append((k, body))
    io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    print("checking %d drafts" % len(items), flush=True)
    try:
        for res in walk.via_subscription("fixcheck", CHECK_SYS, items, "opus", 3):
            for k, c in res.items(): drafts[k]["check"] = c
            io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    finally:
        io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))


def status(d):
    dr = d.get("draft") or {}
    if not dr: return "not drafted"
    if dr.get("action") == "no_change": return "no change (examiner overruled)"
    if d.get("mech"): return "failed shape check"
    c = d.get("check") or {}
    return {"pass": "ready", "fail": "failed second check"}.get(c.get("verdict"), "not checked")


def cmd_report():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    st = Counter(status(d) for d in drafts.values())
    L = ["# English Language walk: corrections for review (25 Sep 2026)", "",
         "Status: " + ", ".join("%s %d" % kv for kv in st.most_common()), "",
         "Only rows marked **ready** would be applied. Nothing has been written to the live lessons.", ""]
    for k in sorted(drafts, key=lambda k: (status(drafts[k]) != "ready", k)):
        d = drafts[k]; dr = d.get("draft") or {}
        L += ["- **%s** (%s, %s) — **%s**" % (k, d["type"], d["ruling"].get("finding"), status(d)),
              "  - Problem: " + d["ruling"].get("why", ""), "  - Change: " + (dr.get("change") or "")]
        if d.get("mech"): L += ["  - Shape check: " + "; ".join(d["mech"])]
        if d.get("check"): L += ["  - Second check: " + d["check"].get("why", "")]
    path = os.path.join(HERE, "_studentwalk_fixes_review.md")
    io.open(path, "w", encoding="utf-8").write("\n".join(L))
    print(path); print(dict(st))


def cmd_apply():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    ready = {k: d for k, d in drafts.items() if status(d) == "ready" and not d.get("applied")}
    by_lesson = {}
    for k, d in ready.items(): by_lesson.setdefault(d["lesson_id"], []).append(d)
    backup = {}
    for lid in by_lesson:
        backup[lid] = rest("lessons?select=id,practice_data&id=eq.%s" % lid)[0]["practice_data"]
    bpath = os.path.join(HERE, "_backup_studentwalk_fixes_%s.json" % time.strftime("%Y-%m-%d_%H%M"))
    io.open(bpath, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
    print("backup:", bpath)
    for lid, ds in by_lesson.items():
        pd = json.loads(json.dumps(backup[lid]))
        for d in ds:
            cur = pd["problem_bank"][d["tier"]][d["i"]]
            if cur != d["original"]:
                print("  skipped (question changed since the walk):", lid, d["tier"], d["i"]); continue
            pd["problem_bank"][d["tier"]][d["i"]] = d["draft"]["question"]
            d["applied"] = time.strftime("%Y-%m-%d %H:%M")
        rest("lessons?id=eq.%s" % lid, "PATCH", {"practice_data": pd})
    io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    print("applied %d corrections in %d lessons" % (sum(1 for d in ready.values() if d.get("applied")), len(by_lesson)))


FIELD_RULE = ("\n(Field rule: keep exactly the original field names; a traffic_light may gain "
              "'categories', which must list every category any statement uses.)")


def cmd_redraft():
    """Second round for drafts that failed the shape check or the second examiner: the failure
    reason goes back to the drafter with its first attempt."""
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    by_key = {f["key"]: f for f in findings()}
    items = []
    for k, d in drafts.items():
        if status(d) not in ("failed shape check", "failed second check") or d.get("round2"): continue
        f = by_key[k]
        why = "; ".join(d.get("mech") or []) or (d.get("check") or {}).get("why", "")
        body = "\n\n".join([
            "WHAT THE STUDENT SAW:\n" + walk.view_prompt(f["view"]),
            "STORED QUESTION OBJECT (live):\n" + json.dumps(d["original"], ensure_ascii=False, indent=1),
            "THE EXAMINER'S RULING:\n" + json.dumps(d["ruling"], ensure_ascii=False),
            "YOUR FIRST REPAIR:\n" + json.dumps(d["draft"].get("question"), ensure_ascii=False, indent=1),
            "WHY IT WAS REJECTED:\n" + why + (FIELD_RULE if d.get("mech") else ""),
            "Repair it again, fixing that problem. If the question cannot be made sound with a small change, "
            "rewrite the question and its options/statements so it is sound, keeping the same input_type."])
        items.append((k, body))
    print("redrafting %d" % len(items), flush=True)
    try:
        for res in walk.via_subscription("fixredraft", DRAFT_SYS, items, "opus", 3):
            for k, dr in res.items():
                drafts[k]["round1"] = {"draft": drafts[k]["draft"], "mech": drafts[k].get("mech"), "check": drafts[k].get("check")}
                drafts[k]["draft"] = dr; drafts[k]["round2"] = True
                drafts[k].pop("check", None); drafts[k].pop("mech", None)
            io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    finally:
        io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"draft": cmd_draft, "redraft": cmd_redraft, "check": cmd_check, "report": cmd_report, "apply": cmd_apply}[sys.argv[1]]()
