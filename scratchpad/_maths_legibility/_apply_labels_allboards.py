# -*- coding: utf-8 -*-
"""Apply reader unit-magnitude labels across ALL four maths boards.

    python scratchpad/_maths_legibility/_apply_labels_allboards.py --check
    python scratchpad/_maths_legibility/_apply_labels_allboards.py --apply

The 3-board reader pass returned findings tagged only by lesson basename, not
board -- but a label is board-independent (a cm2 box is cm2 in every board), so
each label finding is applied to whichever boards actually have that problem with
a matching unlabelled box. AQA findings carry their board and are applied there.

Every label validated, never trusted:
  - a decimal label requires a real 0<x<1 non-integer answer
  - a unit label is applied only if it agrees with the problem's own main-box
    unit, or the problem has no main unit; a conflict is logged, not written
  - the box must be unlabelled (a relabel/correction may override)
  - every lesson write asserts only `post` changed, so no answer can move
"""
import copy, io, json, os, re, sys, urllib.request, collections

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
BOARDS = ["maths-aqa", "maths-edexcel", "maths-ocr", "maths-eduqas"]
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


UNIT_LABELS = {"cm", "cm²", "cm³", "m", "m²", "m³", "mm", "km", "degrees", "m/s", "km/h",
               "g", "kg", "g/cm³", "n", "n/m²", "hours", "seconds", "minutes", "miles",
               "people/year", "£", "%"}


def parse(f):
    step = f.get("step", "") or ""
    prob = f.get("problem", "") or ""
    fix = f.get("fix", "") or ""
    base = f.get("_lesbase", "") or ""
    m_ans = re.search(r"box\s*=\s*([\-−]?\d+(?:\.\d+)?)"
                      r"|\(\s*=\s*([\-−]?\d+(?:\.\d+)?)\s*\)"
                      r"|=\s*([\-−]?\d+(?:\.\d+)?)\s*[\]\)]", step)
    if not m_ans:
        m_ans = re.search(r"=\s*([\-−]?\d+(?:\.\d+)?)\b", fix)
        if m_ans:
            m_ans = re.match(r"()()(" + re.escape(m_ans.group(1)) + r")", m_ans.group(1)) or m_ans
    m_prob = re.search(r"(bronze|silver|gold)\s*\[?(\d+)\]?", prob)
    m_les = re.match(r"([a-z\-]+)__L(\d+)", base)
    m_change = re.search(r"from ['\"]([^'\"]+)['\"] to ['\"]([^'\"]+)['\"]", fix)
    m_lab = re.search(r"label:?\s*['\"]([^'\"]+)['\"]|add ['\"]([^'\"]+)['\"]|to ['\"]([^'\"]+)['\"]", fix)
    if not (m_ans and m_prob and m_les):
        return None
    relabel = False
    if m_change:
        lab = m_change.group(2).strip(); relabel = True
    elif m_lab:
        lab = (m_lab.group(1) or m_lab.group(2) or m_lab.group(3)).strip()
    else:
        return None
    low = lab.lower()
    if low.startswith("(a decimal") or low.startswith("a decimal"):
        lab = "(a decimal)"
    elif low.startswith("(to ") or low.startswith("(nearest") or low.startswith("(to the"):
        pass
    elif low not in UNIT_LABELS:
        return None
    grp = m_ans.group(1) or m_ans.group(2) or m_ans.group(3)
    ans = float(grp.replace("−", "-"))
    return {"unit": m_les.group(1), "lesson": int(m_les.group(2)), "tier": m_prob.group(1),
            "index": int(m_prob.group(2)), "answer": ans, "label": lab, "relabel": relabel,
            "board": f.get("_board")}


def only_posts(before, after):
    def s(pd):
        pd = copy.deepcopy(pd)
        for it in (pd.get("problem_bank") or {}).values():
            if isinstance(it, list):
                for p in it:
                    if isinstance(p, dict):
                        for st in p.get("guided_steps") or []:
                            if isinstance(st, dict) and "post" in st:
                                del st["post"]
        return pd
    return s(before) == s(after)


def main(apply_it):
    findings = json.load(io.open(os.path.join(HERE, "_all_findings", "combined.json"), encoding="utf-8"))
    recs = [r for f in findings if f.get("category") == "unit-magnitude" for r in [parse(f)] if r]
    # group by target lesson: (board or None, unit, lesson)
    want = collections.defaultdict(list)
    for r in recs:
        boards = [r["board"]] if r["board"] else BOARDS
        for b in boards:
            want[(b, r["unit"], r["lesson"])].append(r)

    subj_cache, applied, review, conflicts = {}, 0, collections.Counter(), []
    lessons_touched = 0
    for (board, uslug, ln), rs in want.items():
        if board not in subj_cache:
            sid = req(B + "subjects?slug=eq.%s&select=id" % board)[0]["id"]
            subj_cache[board] = {u["slug"]: u["id"] for u in req(B + "units?subject_id=eq.%s&select=id,slug" % sid)}
        uid = subj_cache[board].get(uslug)
        if not uid:
            continue
        rows = req(B + "lessons?unit_id=eq.%s&lesson_number=eq.%d&select=id,practice_data" % (uid, ln))
        if not rows:
            continue
        before = rows[0]["practice_data"]
        pd = copy.deepcopy(before)
        pb = pd.get("problem_bank") or {}
        hit = 0
        for r in rs:
            items = pb.get(r["tier"])
            if not isinstance(items, list) or r["index"] >= len(items):
                continue
            p = items[r["index"]]
            main_unit = (p.get("unit") or "").strip().lower()
            lab = r["label"]
            if lab in UNIT_LABELS and main_unit and lab.lower() != main_unit and main_unit not in ("", "none"):
                conflicts.append("%s %s L%d %s[%d]: '%s' vs main '%s'" % (board, uslug, ln, r["tier"], r["index"], lab, main_unit))
                continue
            for st in p.get("guided_steps") or []:
                if not isinstance(st, dict):
                    continue
                if st.get("post") and not r["relabel"]:
                    continue
                a = st.get("answer")
                if not isinstance(a, (int, float)) or abs(float(a) - r["answer"]) > 1e-9:
                    continue
                if lab == "(a decimal)" and not (isinstance(a, float) and not float(a).is_integer() and 0 < a < 1):
                    review["decimal-on-nondecimal"] += 1
                    break
                if st.get("post") == lab:
                    break
                st["post"] = lab
                hit += 1
                review["applied:" + lab] += 1
                break
        if hit and not only_posts(before, pd):
            conflicts.append("%s %s L%d: non-post diff" % (board, uslug, ln))
            continue
        if hit:
            lessons_touched += 1
            applied += hit
            if apply_it:
                req(B + "lessons?id=eq.%s" % rows[0]["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % rows[0]["id"])[0]["practice_data"]
                if not only_posts(before, back):
                    conflicts.append("%s %s L%d readback" % (board, uslug, ln))

    print("label findings parsed: %d" % len(recs))
    print("labels %s: %d across %d lessons" % ("applied" if apply_it else "to apply", applied, lessons_touched))
    print("by label:", dict(collections.Counter({k[8:]: v for k, v in review.items() if k.startswith("applied:")})))
    if conflicts:
        print("CONFLICTS (%d):" % len(conflicts))
        for c in conflicts[:15]:
            print("   -", c)


if __name__ == "__main__":
    main("--apply" in sys.argv)
