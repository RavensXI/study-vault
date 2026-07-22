# -*- coding: utf-8 -*-
"""Apply the reader-found contextual labels for one board (AQA first).

    python scratchpad/_maths_legibility/_apply_reader_labels.py <board> _aqa_findings/all.json --check
    python scratchpad/_maths_legibility/_apply_reader_labels.py maths-aqa scratchpad/_maths_legibility/_aqa_findings/all.json --apply

These are the unit-magnitude findings the deterministic classifier could not
reach -- an angle box the step never calls "angle", a solved "x =" box whose
answer is 0.5 that a student writes as 1/2. Only unit-magnitude findings are
applied here; the wording/fragment/assumed-knowledge rewrites are a separate,
more careful pass.

Every label is validated, not trusted:
  - a decimal label requires the answer to be a real 0<x<1 non-integer
  - a unit label is applied only if it agrees with the problem's own main-box
    unit, or the problem has no main unit; a conflict goes to REVIEW, not the DB
  - the box must currently be unlabelled
  - the write asserts only `post` was added, so no answer can move
Anything unmatched or conflicting is printed for a human, never guessed into place.
"""
import copy, io, json, os, re, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
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


UNIT_LABELS = {"cm", "cm²", "cm³", "m", "m²", "m³", "mm", "km", "degrees", "m/s",
               "km/h", "g", "kg", "g/cm³", "n", "n/m²", "hours", "seconds", "minutes",
               "miles", "people/year"}


def parse(f):
    step = f.get("step", "") or ""
    prob = f.get("problem", "") or ""
    fix = f.get("fix", "") or ""
    lesson = f.get("lesson", "") or ""
    # box answer in any of the reader's formats: "box=44", "(=44)", "= 44]"
    m_ans = re.search(r"box\s*=\s*([\-−]?\d+(?:\.\d+)?)"
                      r"|\(\s*=\s*([\-−]?\d+(?:\.\d+)?)\s*\)"
                      r"|=\s*([\-−]?\d+(?:\.\d+)?)\s*[\]\)]", step)
    if not m_ans:
        m_ans = re.search(r"box\s*=\s*([\-−]?\d+(?:\.\d+)?)"
                          r"|=\s*([\-−]?\d+(?:\.\d+)?)\b", fix)
    m_prob = re.search(r"(bronze|silver|gold)\s*\[?(\d+)\]?", prob)
    m_les = re.search(r"([a-z\-]+)__L(\d+)", lesson)
    # "add label 'X'", "label 'X'", "to 'X'", or "change the label from 'A' to 'B'"
    m_change = re.search(r"from ['\"]([^'\"]+)['\"] to ['\"]([^'\"]+)['\"]", fix)
    m_lab = re.search(r"label:?\s*['\"]([^'\"]+)['\"]|add ['\"]([^'\"]+)['\"]|to ['\"]([^'\"]+)['\"]", fix)
    if not (m_ans and m_prob and m_les):
        return None
    relabel = False
    if m_change:
        lab = m_change.group(2).strip()
        relabel = True
    elif m_lab:
        lab = (m_lab.group(1) or m_lab.group(2) or m_lab.group(3)).strip()
    else:
        return None
    low = lab.lower()
    if low.startswith("(a decimal") or low.startswith("a decimal"):
        lab = "(a decimal)"
    elif low.startswith("(to ") or low.startswith("(nearest") or low.startswith("(to the nearest"):
        pass  # keep formatting hints verbatim
    elif low not in UNIT_LABELS:
        return {"skip": "label %r not in known set" % lab, "raw": f}
    ans = float((m_ans.group(1) or m_ans.group(2) or m_ans.group(3)).replace("−", "-"))
    return {"unit": m_les.group(1), "lesson": int(m_les.group(2)),
            "tier": m_prob.group(1), "index": int(m_prob.group(2)),
            "answer": ans, "label": lab, "relabel": relabel}


def only_posts_added(before, after):
    def strip(pd):
        pd = copy.deepcopy(pd)
        for items in (pd.get("problem_bank") or {}).values():
            if isinstance(items, list):
                for p in items:
                    if isinstance(p, dict):
                        for st in p.get("guided_steps") or []:
                            if isinstance(st, dict) and "post" in st:
                                del st["post"]
        return pd
    return strip(before) == strip(after)


def main(board, findings_path, apply_it):
    findings = json.load(io.open(findings_path, encoding="utf-8"))
    um = [f for f in findings if f.get("category") == "unit-magnitude"]
    recs, review = [], []
    for f in um:
        r = parse(f)
        if r is None:
            review.append(("unparseable", f.get("problem"), f.get("fix", "")[:50]))
        elif "skip" in r:
            review.append((r["skip"], f.get("problem"), ""))
        else:
            recs.append(r)

    sid = req(B + "subjects?slug=eq.%s&select=id" % board)[0]["id"]
    units = {u["slug"]: u["id"] for u in req(B + "units?subject_id=eq.%s&select=id,slug" % sid)}
    by_lesson = {}
    for r in recs:
        by_lesson.setdefault((r["unit"], r["lesson"]), []).append(r)

    applied, conflicts = 0, []
    for (uslug, ln), rs in by_lesson.items():
        uid = units.get(uslug)
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
            # validate
            if lab == "(a decimal)":
                pass  # answer-level check below
            elif lab in UNIT_LABELS and main_unit and lab.lower() != main_unit and main_unit not in ("", "none"):
                conflicts.append("%s L%d %s[%d]: reader '%s' vs main-box '%s'" %
                                 (uslug, ln, r["tier"], r["index"], lab, main_unit))
                continue
            # locate the step with this answer. A relabel (reader correcting the
            # classifier) may override an existing label; a plain add may not.
            done = False
            for st in p.get("guided_steps") or []:
                if not isinstance(st, dict):
                    continue
                if st.get("post") and not r.get("relabel"):
                    continue
                a = st.get("answer")
                if not isinstance(a, (int, float)):
                    continue
                if abs(float(a) - r["answer"]) > 1e-9:
                    continue
                if lab == "(a decimal)" and not (isinstance(a, float) and not float(a).is_integer() and 0 < a < 1):
                    review.append(("decimal-label on non-decimal %s" % a, "%s[%d]" % (r["tier"], r["index"]), ""))
                    done = True
                    break
                st["post"] = lab
                hit += 1
                done = True
                break
            if not done:
                review.append(("no unlabelled step with answer %s" % r["answer"], "%s L%d %s[%d]" % (uslug, ln, r["tier"], r["index"]), ""))
        if hit and not only_posts_added(before, pd):
            conflicts.append("%s L%d: non-post diff, skipped" % (uslug, ln))
            continue
        if hit:
            applied += hit
            if apply_it:
                req(B + "lessons?id=eq.%s" % rows[0]["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % rows[0]["id"])[0]["practice_data"]
                if not only_posts_added(before, back):
                    conflicts.append("%s L%d: readback non-post change" % (uslug, ln))

    print("reader unit-magnitude findings: %d" % len(um))
    print("labels %s: %d" % ("applied" if apply_it else "to apply", applied))
    print("REVIEW (not applied): %d" % len(review))
    for r in review[:30]:
        print("   -", r[0], "|", r[1], r[2])
    if conflicts:
        print("CONFLICTS:")
        for c in conflicts[:20]:
            print("   -", c)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0], args[1], "--apply" in sys.argv)
