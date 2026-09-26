"""Draft, check and (on Tom's word) apply corrections for student-walk findings.

25 Sep 2026. Every question the examiner model ruled key_wrong, ambiguous or unanswerable gets a
corrected question object drafted by Opus (subscription), then:
  1. a mechanical check that the object still fits the renderer (same input type, same fields,
     answer indices in range, a traffic-light has at least two categories, number keys keep their
     shape, a gap's answer is in the word bank ...), and
  2. a second, independent Opus pass that sees what is on screen and the corrected question WITH its
     key and rules whether the key is now the one defensible answer.
Nothing touches Supabase until `apply` is run, which backs every lesson row up first.

Three sets (SV_FIX_SET):
  (unset)            English Language click questions, five boards   -> _studentwalk_fixdrafts.json
  practice           the practice-format subjects (maths, science, geography, statistics, music,
                     Latin, MFL) walked 25-26 Sep 2026               -> _studentwalk_fixdrafts_practice.json
  englang_written    Edexcel 1EN0 written questions ruled unanswerable -> _studentwalk_fixdrafts_englang_written.json

  python scripts/_studentwalk_draft_fixes.py draft | check | redraft | report | apply (apply only with Tom's go-ahead)
"""
import io, json, os, sys, time, urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("SV_WALK_DIR", os.path.join(HERE, "_studentwalk_fixwork"))
os.environ.setdefault("SV_WALK_BUDGET", "100000")   # Tom 25 Sep: allowance is not the constraint
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util
_spec = importlib.util.spec_from_file_location("walk", os.path.join(HERE, "_qa_student_walk.py"))
walk = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(walk)

SET = os.environ.get("SV_FIX_SET", "")
AI = walk.AI_TYPES
ENGLISH_AI = ("ai_mark", "ai_write", "improve_sentence")
if SET == "practice":
    BOARDS = tuple(json.load(io.open(os.path.join(HERE, "_studentwalk_practice_dirs.json"), encoding="utf-8")))
    DRAFTS = os.path.join(HERE, "_studentwalk_fixdrafts_practice.json")
    REVIEW = os.path.join(HERE, "_studentwalk_fixes_review_practice.md")
    TITLE = "Practice-format walk (maths, science, geography, statistics, music, Latin, languages)"
elif SET == "englang_written":
    BOARDS = ("english-language-edexcel",)
    DRAFTS = os.path.join(HERE, "_studentwalk_fixdrafts_englang_written.json")
    REVIEW = os.path.join(HERE, "_studentwalk_fixes_review_englang_written.md")
    TITLE = "Edexcel 1EN0 written questions that could not be answered from the screen"
else:
    BOARDS = ("english-language-edexcel", "english-language-aqa", "english-language-ocr", "english-language-eduqas",
              "english-language")
    DRAFTS = os.path.join(HERE, "_studentwalk_fixdrafts.json")
    REVIEW = os.path.join(HERE, "_studentwalk_fixes_review.md")
    TITLE = "English Language walk"
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}


def rest(path, method="GET", body=None):
    req = urllib.request.Request(U + "/rest/v1/" + path, method=method, headers=dict(H, **{
        "Content-Type": "application/json", "Prefer": "return=minimal"}), data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=120) as r:
        t = r.read()
        return json.loads(t) if t else None


def lesson(v):
    if v.get("lesson_id"):
        return rest("lessons?select=id,practice_data&id=eq.%s" % v["lesson_id"])[0]
    return rest("lessons?select=id,practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                "&units.slug=eq.%s&lesson_number=eq.%s" % (v["subject"], v["unit"], v["n"]))[0]


def dkey(d, k):
    """Draft id: the walk key, prefixed with its walk directory when two subject rows share a slug."""
    return ("%s::%s" % (d, k)) if SET == "practice" else k


def wanted(t):
    if SET == "englang_written": return t in ENGLISH_AI
    return t not in AI


def findings():
    out = []
    for sub in BOARDS:
        d = os.path.join(HERE, "_studentwalk_" + sub)
        if not os.path.exists(os.path.join(d, "adjudications.json")): continue
        v = json.load(io.open(os.path.join(d, "views.json"), encoding="utf-8"))
        a = json.load(io.open(os.path.join(d, "adjudications.json"), encoding="utf-8"))
        at = json.load(io.open(os.path.join(d, "attempts.json"), encoding="utf-8"))
        rulings = ("unanswerable",) if SET == "englang_written" else ("key_wrong", "ambiguous", "unanswerable")
        for k, x in a.items():
            if k in v and wanted(v[k]["type"]) and (x or {}).get("finding") in rulings:
                out.append({"key": k, "dir": sub, "id": dkey(sub, k), "view": v[k], "ruling": x, "attempt": at.get(k, {})})
    return out


DRAFT_SYS_EN = """You are a senior GCSE English Language examiner repairing one practice question on a revision
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

DRAFT_SYS_PRACTICE = """You are a senior GCSE examiner in the subject named in each item, repairing one practice question on a
revision website. A careful Year 11 student answered it blind and an examiner ruled the question faulty.
You see what the student saw (and, for anything visual, a SCREENSHOT path: open it with the Read tool),
the stored question object (JSON) with its answer key, the student's attempt and the examiner's ruling.

Repair the question so that a careful student reading only what is on screen can reach exactly one
defensible answer, and the key is that answer. Prefer the smallest change: correct a wrong key; say how
to round or what form to give; reword a question or option that leads a sound reader astray; restore
missing information in the question text itself. Never refer to a picture, chart, map or text that is
not on the student's screen; you cannot change images or charts, only the text and the key.

How the site marks, so the key really works:
- single_value: the typed number is compared with solutions[0] within 0.01, or within the question's own
  "tolerance" if it has one (add or widen "tolerance" when the answer is read off a graph or rounded).
- two_solutions: the two typed numbers, in any order, against solutions; xy_pair: [x, y] in order.
- fraction: solutions [numerator, denominator], any equivalent fraction accepted.
- standard_form: solutions [a, n] for a x 10^n.
- multiple_choice: solutions[0] is the INDEX of the right entry in options.
- gap_fill: each gap's "answer" and "accept" list; with a word_bank the answer must be one of its words.
- vocab_match: each pairs[i] left <-> right; every left and every right must be unique.
- sentence_builder: correct_order is the exact tile sequence; distractors are extra tiles.
- spot_correct: error_word must appear in sentence; correction and accept_corrections are accepted.
- reorder: correct_order is the list of item indices in the right order.
Keep the JSON shape exactly: same input_type, same field names, same kinds of values (you may add
"tolerance" to a number question). Keep British spelling and the GCSE register. If the examiner is wrong
and the question is sound, say so.

Reply with ONE JSON object and nothing else:
{"action": "patch" | "no_change",
 "question": <the full corrected question object, or null for no_change>,
 "change": "one or two plain sentences saying what changed and why, for the teacher"}"""

DRAFT_SYS_WRITTEN = DRAFT_SYS_EN.replace(
    "Keep the JSON shape exactly: same input_type, same field names, same kinds of values; you may add\n"
    "\"categories\" (a list of every category name) to a traffic_light question.",
    "Keep the JSON shape exactly: same input_type, same field names, same kinds of values. This is a written\n"
    "question marked by an AI marker. When it asks about several sources but only one is on screen, the page\n"
    "can show several: set \"passage_ids\" to the list of passage ids it needs (from PASSAGES IN THIS LESSON,\n"
    "e.g. [\"bronze\", \"silver\", \"gold\"]); you may add \"passage_as\" (the same length, e.g. [\"Source A\",\n"
    "\"Source B\", \"Source C\"]) so the panel labels match the question. Keep \"passage_id\" as it is.")
assert DRAFT_SYS_WRITTEN != DRAFT_SYS_EN
DRAFT_SYS = DRAFT_SYS_PRACTICE if SET == "practice" else DRAFT_SYS_WRITTEN if SET == "englang_written" else DRAFT_SYS_EN

CHECK_SYS_EN = """You are a second, independent GCSE English Language examiner. You see a passage (if any) and one
practice question with its answer key, after a colleague repaired it. Decide whether a careful Year 11
student reading only the passage and the question could reach exactly one defensible answer, and
whether the stored key is that answer. Check every option, statement, token or pair, not only the
changed ones. Be strict: a key that is arguably wrong, or a second defensible answer, is a fail.

Reply with ONE JSON object and nothing else:
{"verdict": "pass" | "fail", "why": "one or two plain sentences", "confidence": 0.0-1.0}"""

CHECK_SYS_PRACTICE = """You are a second, independent GCSE examiner in the subject named in the item. You see what is on the
student's screen (and, for anything visual, a SCREENSHOT path: open it with the Read tool; it shows the
question BEFORE the repair, so trust the repaired text where they differ) and one practice question with
its answer key, after a colleague repaired it. Work the question out yourself first. Then decide whether a
careful Year 11 student could reach exactly one defensible answer, and whether the stored key (for
multiple_choice, solutions[0] is the index of the right option) is that answer, accepted by the site's
marking (numbers within 0.01 unless the question sets "tolerance"). Check every option, pair, gap or tile,
not only the changed ones. Be strict: a key that is arguably wrong, or a second defensible answer, is a fail.

Reply with ONE JSON object and nothing else:
{"verdict": "pass" | "fail", "why": "one or two plain sentences", "confidence": 0.0-1.0}"""

CHECK_SYS_WRITTEN = """You are a second, independent GCSE English Language examiner. You see the passages a student will have on
screen and one written practice question (marked by an AI marker from the mark scheme stored with it), after a
colleague repaired it. Decide whether a careful Year 11 student could answer the question fully from what is on
screen (every source the question names is shown and labelled as the question names it), and whether the question
and its mark scheme agree. Be strict: a source the question needs that is missing or mislabelled is a fail.

Reply with ONE JSON object and nothing else:
{"verdict": "pass" | "fail", "why": "one or two plain sentences", "confidence": 0.0-1.0}"""

CHECK_SYS = CHECK_SYS_PRACTICE if SET == "practice" else CHECK_SYS_WRITTEN if SET == "englang_written" else CHECK_SYS_EN


def item_body(f, q):
    parts = []
    if SET == "practice": parts.append("SUBJECT: " + walk.subject_name(f["view"]["subject"]))
    parts += ["WHAT THE STUDENT SAW:\n" + walk.view_prompt(f["view"]),
              "STORED QUESTION OBJECT:\n" + json.dumps(q, ensure_ascii=False, indent=1),
              "THE STUDENT'S ATTEMPT:\n" + json.dumps(f["attempt"], ensure_ascii=False)[:3000],
              "THE EXAMINER'S RULING:\n" + json.dumps(f["ruling"], ensure_ascii=False)]
    if SET == "englang_written" and f.get("passages"):
        parts.append("PASSAGES IN THIS LESSON (id | label | opening):\n" + "\n".join(
            "%s | %s | %s" % (x.get("id"), x.get("label", ""), re_strip(x.get("text", ""))[:160]) for x in f["passages"]))
    return "\n\n".join(parts)


def re_strip(h):
    import re
    return re.sub(r"<[^>]+>", " ", str(h)).replace("&nbsp;", " ").strip()


def cmd_draft():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8")) if os.path.exists(DRAFTS) else {}
    items, cache = [], {}
    for f in findings():
        k, v = f["id"], f["view"]
        if k in drafts and drafts[k].get("draft"): continue
        lk = (f["dir"], v["unit"], v["n"])
        if lk not in cache: cache[lk] = lesson(v)
        q = cache[lk]["practice_data"]["problem_bank"][v["tier"]][v["i"]]
        f["passages"] = cache[lk]["practice_data"].get("passages") or []
        drafts[k] = {"lesson_id": cache[lk]["id"], "tier": v["tier"], "i": v["i"], "type": v["type"],
                     "dir": f["dir"], "key": f["key"], "ruling": f["ruling"], "original": q}
        items.append((k, item_body(f, q)))
    items = items[:int(os.environ.get("SV_FIX_LIMIT", "100000"))]
    print("drafting %d corrections" % len(items), flush=True)
    try:
        for res in walk.via_subscription("fixdraft", DRAFT_SYS, items, "opus", 3):
            for k, d in res.items():
                if isinstance(d, dict): drafts[k]["draft"] = d
            io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    finally:
        io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
        print("drafts on file: %d" % sum(1 for d in drafts.values() if d.get("draft")))


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def mech(orig, new):
    """Does the corrected object still fit the renderer? Returns a list of problems."""
    p = []
    if not isinstance(new, dict): return ["not an object"]
    if new.get("input_type") != orig.get("input_type"): p.append("input_type changed")
    extra = set(new) - set(orig) - {"categories", "tolerance"} - ({"passage_ids", "passage_as"} if SET == "englang_written" else set())
    if extra: p.append("new fields: %s" % sorted(extra))
    missing = set(orig) - set(new)
    if missing: p.append("dropped fields: %s" % sorted(missing))
    t = new.get("input_type") or "single_value"
    sol = new.get("solutions")
    if t == "multiple_choice":
        opts = new.get("options") or []
        c = new.get("correct")
        if isinstance(c, int) and not (0 <= c < len(opts)): p.append("correct index out of range")
        if isinstance(c, str) and opts and c not in opts: p.append("correct not among options")
        if "solutions" in orig and not (isinstance(sol, list) and sol and isinstance(sol[0], int) and 0 <= sol[0] < len(opts)):
            p.append("solutions[0] is not a valid option index")
        if len(set(map(str, opts))) != len(opts): p.append("two options are the same")
    if t in ("single_value", "two_solutions", "xy_pair", "standard_form", "fraction") and "solutions" in orig:
        want = {"single_value": 1, "two_solutions": 2, "xy_pair": 2, "standard_form": 2, "fraction": None}[t]
        if not isinstance(sol, list) or not sol: p.append("solutions missing")
        elif t == "fraction":
            ok = (len(sol) == 2 and all(_num(x) for x in sol)) or (len(sol) == 1 and isinstance(sol[0], dict))
            if not ok: p.append("fraction solutions not [num, den]")
        else:
            if want and len(sol) < want: p.append("solutions too short for %s" % t)
            if not all(_num(x) for x in sol[:want or len(sol)]): p.append("solutions are not numbers")
        if "tolerance" in new and not (_num(new["tolerance"]) and new["tolerance"] >= 0): p.append("tolerance is not a number")
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
    if t == "vocab_match":
        pr = new.get("pairs") or []
        if not pr or any(not (isinstance(x, dict) and x.get("left") and x.get("right")) for x in pr): p.append("pairs malformed")
        elif len({x["left"] for x in pr}) != len(pr) or len({x["right"] for x in pr}) != len(pr): p.append("a pair side is repeated")
    if t == "gap_fill":
        gaps, parts = new.get("gaps") or [], new.get("sentence_parts") or []
        if not gaps or len(parts) < len(gaps): p.append("fewer sentence parts than gaps")
        bank = new.get("word_bank") or []
        if bank and any(g.get("answer") not in bank for g in gaps): p.append("a gap answer is not in the word bank")
    if t == "sentence_builder":
        co = new.get("correct_order") or []
        if not co or not all(isinstance(x, str) for x in co): p.append("correct_order malformed")
    if t == "spot_correct":
        if not new.get("error_word") or new.get("error_word", "").split()[0].strip(".,!?;:'\"") not in new.get("sentence", ""):
            p.append("error_word not in sentence")
    if t == "reorder" and "correct_order" in new:
        co, items = new.get("correct_order") or [], new.get("items") or []
        if sorted(co) != list(range(len(items))): p.append("correct_order is not a full ordering of the items")
    return p


def check_body(d, v):
    q = json.dumps(d["draft"]["question"], ensure_ascii=False, indent=1)
    if SET == "practice":
        return "SUBJECT: %s\n\nWHAT IS ON THE STUDENT'S SCREEN (before the repair):\n%s\n\nREPAIRED QUESTION WITH ITS KEY:\n%s" % (
            walk.subject_name(v["subject"]), walk.view_prompt(v), q)
    if SET == "englang_written":
        pd = rest("lessons?select=practice_data&id=eq.%s" % d["lesson_id"])[0]["practice_data"]
        ids = d["draft"]["question"].get("passage_ids") or [d["draft"]["question"].get("passage_id")]
        shown = [x for x in pd.get("passages") or [] if x.get("id") in ids]
        return ("PASSAGES ON SCREEN AFTER THE REPAIR:\n%s\n\nWRITTEN QUESTION (AI-marked) WITH ITS MARK SCHEME:\n%s\n\n"
                "Judge whether a student can now answer it fully from what is on screen, and whether the question and its "
                "mark scheme agree." %
                ("\n\n".join("[%s] %s" % (x.get("label", x.get("id")), re_strip(x.get("text", ""))[:6000]) for x in shown) or "(none)", q))
    return ("PASSAGE ON SCREEN:\n%s\n\nQUESTION WITH ITS KEY:\n%s" %
            ("\n\n".join(x for x in (v.get("panel"), v.get("highlight_text")) if x) or "(none)", q))


def view_of(k, d):
    sub = d.get("dir") or k.split("/")[0]
    key = d.get("key") or k
    return json.load(io.open(os.path.join(HERE, "_studentwalk_" + sub, "views.json"), encoding="utf-8"))[key]


def cmd_check():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    items = []
    for k, d in drafts.items():
        dr = d.get("draft") or {}
        if dr.get("action") != "patch" or d.get("check"): continue
        d["mech"] = mech(d["original"], dr.get("question"))
        if d["mech"]: continue
        items.append((k, check_body(d, view_of(k, d))))
    io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    print("checking %d drafts" % len(items), flush=True)
    try:
        for res in walk.via_subscription("fixcheck", CHECK_SYS, items, "opus", 3):
            for k, c in res.items():
                if isinstance(c, dict): drafts[k]["check"] = c
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
    L = ["# %s: corrections for review (%s)" % (TITLE, time.strftime("%d %b %Y")), "",
         "Status: " + ", ".join("%s %d" % kv for kv in st.most_common()), "",
         "Only rows marked **ready** would be applied. Nothing has been written to the live lessons.", ""]
    if SET == "practice":
        by = Counter((d.get("dir"), status(d)) for d in drafts.values())
        L += ["| Subject | ready | failing | no change |", "|---|---|---|---|"]
        for sub in sorted({d.get("dir") for d in drafts.values()}):
            L += ["| %s | %d | %d | %d |" % (sub, by[(sub, "ready")], by[(sub, "failed second check")] + by[(sub, "failed shape check")],
                                             by[(sub, "no change (examiner overruled)")])]
        L += [""]
    for k in sorted(drafts, key=lambda k: (status(drafts[k]) != "ready", k)):
        d = drafts[k]; dr = d.get("draft") or {}
        L += ["- **%s** (%s, %s) — **%s**" % (k, d["type"], d["ruling"].get("finding"), status(d)),
              "  - Problem: " + d["ruling"].get("why", ""), "  - Change: " + (dr.get("change") or "")]
        if d.get("mech"): L += ["  - Shape check: " + "; ".join(d["mech"])]
        if d.get("check"): L += ["  - Second check: " + d["check"].get("why", "")]
    io.open(REVIEW, "w", encoding="utf-8").write("\n".join(L))
    print(REVIEW); print(dict(st))


def cmd_apply():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    ready = {k: d for k, d in drafts.items() if status(d) == "ready" and not d.get("applied")}
    by_lesson = {}
    for k, d in ready.items(): by_lesson.setdefault(d["lesson_id"], []).append(d)
    backup = {}
    for lid in by_lesson:
        backup[lid] = rest("lessons?select=id,practice_data&id=eq.%s" % lid)[0]["practice_data"]
    bpath = os.path.join(HERE, "_backup_studentwalk_fixes_%s%s.json" % (SET + "_" if SET else "", time.strftime("%Y-%m-%d_%H%M")))
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
              "'categories', which must list every category any statement uses; a number question may gain 'tolerance'.)")


def cmd_redraft():
    """Later rounds for drafts that failed the shape check or the second examiner: the failure
    reason goes back to the drafter with its previous attempt."""
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    by_key = {f["id"]: f for f in findings()}
    items = []
    for k, d in drafts.items():
        if status(d) not in ("failed shape check", "failed second check") or (d.get("round2") and not os.environ.get("SV_FIX_ROUND3")) or d.get("round3"): continue
        f = by_key[k]
        why = "; ".join(d.get("mech") or []) or (d.get("check") or {}).get("why", "")
        parts = ["SUBJECT: " + walk.subject_name(f["view"]["subject"])] if SET == "practice" else []
        body = "\n\n".join(parts + [
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
                if not isinstance(dr, dict): continue
                drafts[k]["round1"] = {"draft": drafts[k]["draft"], "mech": drafts[k].get("mech"), "check": drafts[k].get("check")}
                drafts[k]["draft"] = dr; drafts[k]["round3" if drafts[k].get("round2") else "round2"] = True
                drafts[k].pop("check", None); drafts[k].pop("mech", None)
            io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))
    finally:
        io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"draft": cmd_draft, "redraft": cmd_redraft, "check": cmd_check, "report": cmd_report, "apply": cmd_apply}[sys.argv[1]]()
