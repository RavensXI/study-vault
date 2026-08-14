"""Phase 1: independent verification of practice answer keys.

The structural validator (scripts/_qa_practice_data.py) proves a problem is
well-formed. This one asks the question that matters more: is the stored
answer RIGHT? A wrong key tells a correct student they are wrong — the single
most trust-destroying failure a practice site can have.

No model calls. Three checks, in order of coverage:

  A. SCAFFOLD vs KEY (the workhorse, ~84% of quantitative problems).
     guided_steps walk the student to the answer, and the final step states
     it. If the scaffold ends somewhere the key does not accept, one of them
     is wrong and a student following the walkthrough gets failed. Pure
     numeric comparison — no natural language involved.

  B. STEP ARITHMETIC. Steps whose prompt text ends in an evaluable expression
     ("top: 18 + 6 = " -> answer 24) are recomputed with sympy. Only a strict
     arithmetic grammar is attempted; anything wordier is skipped rather than
     guessed at.

  C. BARE EXPRESSIONS. Displays that are a single \\( ... \\) with at most an
     "Evaluate/Work out" prefix are parsed with sympy's LaTeX parser and
     evaluated against the key.

Everything else — word problems, diagram problems — is counted as
NOT MACHINE-CHECKABLE and reported as coverage, never guessed. Honest coverage
beats fake completeness.

Tolerances: stored keys are frequently rounded ("to 1 d.p."), so values match
when equal, when within half a unit of the stored key's last decimal place, or
within 0.5% relative — the scaffold often computes exactly what the key rounds.

Read-only against Supabase. Report: scripts/_qa_answers_report.md (+ .json).
"""
import io
import json
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict

import sympy
from sympy.parsing.latex import parse_latex

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(REPO, "scripts", "_qa_answers_report.md")
REPORT_JSON = os.path.join(REPO, "scripts", "_qa_answers_report.json")

QUANT = {"single_value", "fraction", "two_solutions", "xy_pair", "standard_form"}
TAGS = re.compile(r"<[^>]+>")
LATEX_BLOB = re.compile(r"\\\((.+?)\\\)", re.S)

# strict grammar for step arithmetic — digits, operators, brackets, the unicode
# maths students actually see. Anything outside it is skipped, not guessed.
ARITH_OK = re.compile(r"^[\d\s\.\+\-\*/xX×÷\(\)\^%²³,]+$")
PCT_OF = re.compile(r"([\d\.]+)\s*%\s*of\s*([\d\.]+)", re.I)


def get(path):
    r = urllib.request.Request(URL + "/rest/v1/" + path, headers=H)
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def numval(x):
    """A comparable float from a solution entry (number or fraction dict)."""
    if is_num(x):
        return float(x)
    if isinstance(x, dict) and is_num(x.get("numerator")) and is_num(x.get("denominator")):
        d = float(x["denominator"])
        return float(x["numerator"]) / d if d else None
    if isinstance(x, str):
        try:
            return float(x.replace(",", ""))
        except ValueError:
            return None
    return None


def close(stored, computed):
    """Match under the rounding the corpus actually uses."""
    if stored is None or computed is None:
        return False
    if stored == computed:
        return True
    # half a unit in the stored key's last decimal place. repr(76.0) is
    # '76.0', which read as ONE decimal place and shrank the tolerance
    # tenfold — an integral key rounded "to the nearest degree" then failed
    # against its own exact value. Integral keys tolerate +/-0.5.
    if float(stored) == int(stored):
        dp = 0
    else:
        s = repr(float(stored))
        dp = len(s.split(".")[1]) if "." in s and "e" not in s else 0
    if abs(stored - computed) <= 0.5 * (10 ** -dp) + 1e-12:
        return True
    # relative slack for keys rounded to significant figures
    if computed != 0 and abs(stored - computed) / abs(computed) < 0.005:
        return True
    return False


def eval_arith(text):
    """Evaluate a strict-arithmetic string, or None."""
    t = text.strip().rstrip("=").strip()
    t = PCT_OF.sub(lambda m: "(%s/100)*(%s)" % (m.group(1), m.group(2)), t)
    t = (t.replace("×", "*").replace("÷", "/").replace("^", "**")
          .replace("²", "**2").replace("³", "**3").replace(",", ""))
    t = re.sub(r"(?<=\d)\s*[xX]\s*(?=\d)", "*", t)      # 3 x 4 -> 3*4
    if not t or not ARITH_OK.match(t.replace("**", "^").replace("*", "x")):
        return None
    # a bare number is not an equation to check
    if re.fullmatch(r"[\d\.\s]+", t):
        return None
    try:
        v = sympy.sympify(t, rational=False)
        if v.free_symbols:
            return None
        return float(v.evalf())
    except Exception:
        return None


def eval_bare_latex(text):
    """A display that is one LaTeX expression, optionally prefixed by an
    imperative — parse and evaluate, or None."""
    plain = TAGS.sub(" ", text)
    blobs = LATEX_BLOB.findall(plain)
    if len(blobs) != 1:
        return None
    # mixed numbers parse as multiplication (2\frac{1}{3} -> 2 * 1/3);
    # skip rather than mis-evaluate
    if re.search(r"\d\s*\\[dt]?frac", plain):
        return None
    residue = LATEX_BLOB.sub(" ", plain)
    # ONLY evaluation verbs and pure format instructions may be stripped.
    # 'Simplify ... as a power of 2' wants the INDEX — stripping 'simplify'
    # and everything after 'give your answer' turned index-law questions into
    # evaluations and flagged six correct keys.
    residue = re.sub(r"(?i)\b(evaluate|work out|calculate|find the value of"
                     r"|give your answer to \d+ (?:d\.p\.?|s\.f\.?|decimal places?|significant figures?)"
                     r"|to \d+ d\.p\.?|to \d+ s\.f\.?)\b", " ", residue)
    if re.sub(r"[\s\.,:;\?\!]+", "", residue):
        return None                       # words remain — not a bare expression
    try:
        expr = parse_latex(blobs[0])
        if expr.free_symbols:
            return None
        return float(expr.evalf())
    except Exception:
        return None


def main():
    units = {u["id"]: u for u in get("units?select=id,slug,subject_id")}
    subs = {s["id"]: s for s in get("subjects?select=id,slug,status")}

    stats = Counter()
    findings = []
    fam_cov = defaultdict(Counter)

    def flag(check, lesson, where, msg):
        findings.append({
            "check": check, "family": lesson["family"], "subject": lesson["subject"],
            "unit": lesson["unit"], "lesson": lesson["number"], "title": lesson["title"],
            "url": "https://www.studyvault.co.uk/practice/%s/%s/%s"
                   % (lesson["subject"], lesson["unit"], lesson["number"]),
            "where": where, "message": msg,
        })

    page = 0
    while True:
        rows = get("lessons?select=id,unit_id,lesson_number,title,practice_data"
                   "&offset=%d&limit=500" % (page * 500))
        if not rows:
            break
        for r in rows:
            pd = r.get("practice_data") or {}
            pb = pd.get("problem_bank") or {}
            if not isinstance(pb, dict) or not pb:
                continue
            u = units.get(r["unit_id"]) or {}
            s = subs.get(u.get("subject_id")) or {}
            if s.get("status") == "archived":
                continue
            fam = re.sub(r"-(aqa|edexcel(-[ab])?|eduqas|wjec|ncfe|ocr(-[ab])?)$",
                         "", s.get("slug") or "")
            lesson = {"family": fam, "subject": s.get("slug") or "?",
                      "unit": u.get("slug") or "?", "number": r.get("lesson_number"),
                      "title": r.get("title") or ""}
            for tier in ("bronze", "silver", "gold"):
                for i, p in enumerate(pb.get(tier) or []):
                    if not isinstance(p, dict):
                        continue
                    t = p.get("input_type") or "single_value"
                    if t not in QUANT:
                        continue
                    where = "%s[%d]" % (tier, i)
                    stats["quant-problems"] += 1
                    sols = [numval(x) for x in (p.get("solutions") or [])]
                    sols = [x for x in sols if x is not None]

                    checked_here = False

                    # ---- A. scaffold vs key ----
                    # Scaffolds often END on a verification step whose number
                    # is deliberately not the answer ("check: ... 3 + 8 = 11").
                    # The first version compared only the LAST step and called
                    # 68% of the corpus wrong — the checker misreading the
                    # format, not 4,812 bad keys. The real contradiction is the
                    # accepted answer appearing NOWHERE in the scaffold: the
                    # walkthrough never reaches the number the key accepts.
                    gs = [g for g in (p.get("guided_steps") or []) if isinstance(g, dict)]
                    stated = [numval(g["answer"]) for g in gs if "answer" in g]
                    stated = [v for v in stated if v is not None]

                    # fraction keys have a third encoding: [num, den] as a
                    # two-int list ([1, 2] means one half). The quotient is
                    # the value the scaffold walks to.
                    if t == "fraction" and len(sols) == 2 and sols[1]:
                        sols = sols + [sols[0] / sols[1]]

                    # scaffolds state the final answer in PROSE at least as
                    # often as in a step answer: "the largest is 15",
                    # "= 39.1 kW lost in the cables". Numbers in say/done
                    # count as stated.
                    prose = " ".join(str(g.get(k) or "") for g in gs for k in ("say", "done"))
                    prose = re.sub(r"(?<=\d),(?=\d)", "", prose)
                    for mnum in re.findall(r"-?\d+(?:\.\d+)?", prose):
                        try:
                            stated.append(float(mnum))
                        except ValueError:
                            pass

                    if stated and sols:
                        stats["A-scaffold-checked"] += 1
                        fam_cov[fam]["A"] += 1
                        checked_here = True
                        def reachable(sv):
                            if any(close(sv, v) for v in stated):
                                return True
                            # scaffolds often state the PARTS and leave the final
                            # quotient or product to the answer box: steps [7, 12]
                            # with key 7/12. One elementary multiplicative step
                            # of two stated answers counts as reaching the key.
                            # Sums do NOT — widen that far and every wrong key
                            # eventually passes through some combination.
                            for a in stated:
                                for b in stated:
                                    if b and close(sv, a / b):
                                        return True
                                    if close(sv, a * b):
                                        return True
                            return False

                        missing = [sv for sv in sols if not reachable(sv)]
                        if missing:
                            flag("scaffold-vs-key", lesson, where,
                                 "solution(s) %s never appear in the scaffold's step answers %s"
                                 % (json.dumps(missing)[:40],
                                    json.dumps([g.get("answer") for g in gs if "answer" in g])[:60]))
                            stats["A-mismatch"] += 1

                    # ---- B. step arithmetic ----
                    for g in gs:
                        pre = str(g.get("pre") or "")
                        if "=" not in pre or "answer" not in g:
                            continue
                        rhs = numval(g["answer"])
                        if rhs is None:
                            continue
                        v = eval_arith(pre.split(":")[-1])
                        if v is None:
                            continue
                        stats["B-steps-checked"] += 1
                        if not close(rhs, v):
                            flag("step-arithmetic", lesson, where,
                                 "step '%s' computes to %.6g but states %s"
                                 % (pre.strip()[:60], v, g["answer"]))
                            stats["B-mismatch"] += 1

                    # ---- C. bare expression vs key ----
                    if sols and t == "single_value":
                        v = eval_bare_latex((p.get("question") or "") + " " + (p.get("display") or ""))
                        if v is not None:
                            stats["C-expressions-checked"] += 1
                            fam_cov[fam]["C"] += 1
                            checked_here = True
                            if not any(close(sv, v) for sv in sols):
                                flag("expression-vs-key", lesson, where,
                                     "expression evaluates to %.6g but solutions are %s"
                                     % (v, json.dumps(p.get("solutions"))[:40]))
                                stats["C-mismatch"] += 1

                    if not checked_here:
                        stats["not-machine-checkable"] += 1
                        fam_cov[fam]["skip"] += 1
        if len(rows) < 500:
            break
        page += 1

    # ---- report ----
    L = []
    L.append("# Practice answer verification (Phase 1)")
    L.append("")
    L.append("Independent recomputation of deterministic answer keys — scaffold")
    L.append("consistency, step arithmetic, and bare-expression evaluation. Word and")
    L.append("diagram problems are reported as unverifiable, not guessed at.")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    for k in ("quant-problems", "A-scaffold-checked", "A-mismatch", "B-steps-checked",
              "B-mismatch", "C-expressions-checked", "C-mismatch", "not-machine-checkable"):
        L.append("| %s | %d |" % (k, stats.get(k, 0)))
    L.append("")
    L.append("## Coverage by family (A=scaffold, C=expression, skip=unverifiable)")
    L.append("")
    L.append("| Family | A | C | skipped |")
    L.append("|---|---|---|---|")
    for fam in sorted(fam_cov):
        c = fam_cov[fam]
        L.append("| %s | %d | %d | %d |" % (fam, c.get("A", 0), c.get("C", 0), c.get("skip", 0)))
    L.append("")
    L.append("## Mismatches (%d)" % len(findings))
    L.append("")
    for f in findings:
        L.append("- **%s** `%s` %s — %s  " % (f["check"], f["where"], f["message"], f["title"]))
        L.append("  %s" % f["url"])

    io.open(REPORT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    io.open(REPORT_JSON, "w", encoding="utf-8").write(json.dumps(findings, indent=1))

    print("quant problems         :", stats.get("quant-problems", 0))
    print("A scaffold checked     : %d  (mismatch %d)" % (stats.get("A-scaffold-checked", 0), stats.get("A-mismatch", 0)))
    print("B step arith checked   : %d  (mismatch %d)" % (stats.get("B-steps-checked", 0), stats.get("B-mismatch", 0)))
    print("C expressions checked  : %d  (mismatch %d)" % (stats.get("C-expressions-checked", 0), stats.get("C-mismatch", 0)))
    print("not machine-checkable  :", stats.get("not-machine-checkable", 0))
    print("report:", REPORT_MD)


if __name__ == "__main__":
    main()
