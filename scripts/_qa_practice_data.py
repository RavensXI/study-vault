"""Structural validation for every practice lesson's practice_data.

This is the gate docs/PRACTICE_PIPELINE.md has named since May and which never
existed — not deleted, never committed. It ships now, first, before any
practice generation is built, because it is the acceptance test for that
generation AND it pays back immediately across the ~19k problems already live.

Design rules, learned the hard way this week:
- Every threshold below was DERIVED from the live corpus, not guessed. The
  scan that produced them: solutions are numeric lists for quantitative types
  and absent for prose/MFL types (100%/0%, no middle ground); fraction answers
  are a number or {numerator, denominator}; every family's modal lesson size
  is 20 except Music (12-17, artisanal, deliberately exempt from count rules).
- ERRORs are things that lie to a student (an unanswerable problem, a broken
  answer key, a dangling AI prompt). WARNs are things a human should look at.
  A validator that cries wolf on Music's hand-built lessons drowns its own
  signal on the first run.
- Read-only. This script never writes to Supabase.

Usage:
  python scripts/_qa_practice_data.py            # full run, writes the report
  python scripts/_qa_practice_data.py --family maths   # one family
Report: scripts/_qa_practice_report.md (+ .json alongside).
Exit code 1 if any ERROR was found, else 0 — so a build can gate on it.
"""
import io
import json
import os
import re
import sys
import urllib.request
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(REPO, "scripts", "_qa_practice_report.md")
REPORT_JSON = os.path.join(REPO, "scripts", "_qa_practice_report.json")

TIERS = ("bronze", "silver", "gold")

# Quantitative types carry machine-checkable answers; everything else is prose
# or interaction and legitimately has none. Derived from the corpus: 100% of
# these types carry numeric solution lists; 100% of the rest carry no
# solutions field at all.
NUMERIC_TYPES = {"single_value", "two_solutions", "xy_pair", "standard_form"}
PAIR_TYPES = {"two_solutions", "xy_pair"}          # exactly two values
NO_SOLUTIONS_TYPES = {
    "ai_mark", "ai_write", "gap_fill", "translate", "dictation",
    "highlight_evidence", "vocab_match", "sentence_builder", "traffic_light",
    "connotation_picker", "spot_correct", "reorder", "misleading_summary",
    "evidence_match", "role_play", "improve_sentence", "spot_error",
}

# Music is curated by hand at ~12-17 problems by design; every other family's
# mode is 20. Count rules skip Music rather than mass-flagging Tom's own work.
COUNT_EXEMPT_FAMILIES = {"music"}
COUNT_BAND = (16, 24)

BOARD_WORDS = re.compile(r"\b(AQA|Edexcel|OCR|Eduqas|WJEC)\b")
MARKSCHEME_WORDS = re.compile(r"\bAO[1-4]\b|\bLevel [1-9]\b")
JUNK = re.compile(r"\[object Object\]|\bundefined\b|\bNaN\b")
MOJIBAKE = re.compile(r"â€|Ã©|Ã¨|â€™|â€œ")
OPTION_PREFIX = re.compile(r"^[A-D][.)]\s")
TAGS = re.compile(r"<[^>]+>")

# Interaction types carry their ask outside question/display: translate's is
# source_text, dictation's is the audio itself, vocab_match's is the pairs.
# The first run of this validator flagged 959 of these as "no-ask" — every one
# a rule misfire, almost all MFL. An ask is ANY of these fields.
ASK_FIELDS = ("question", "display", "source_text", "text", "audio_text",
              "audio_url", "pairs", "words", "scenario", "items", "segments",
              "sentence", "prompt", "instruction")

# imperative asks ("Use the trapezium rule ... to estimate the area.") are as
# valid as interrogative ones; the chart check must accept both
ASK_CUES = re.compile(
    r"\?|\b(" +
    "work out|calculate|find|estimate|state|write|draw|complete|give|how|what|which|express|plot|read off|describe|show|shade|use|convert|round|solve|simplify|expand|factorise|label|identify" +
    r")\b", re.I)

# tier descriptions are a QUANTITATIVE-family convention (maths-shape banks);
# EngLang, MFL and Music banks never carried them and are not wrong for it
TIER_DESC_FAMILIES = {"maths", "statistics", "science", "separate-sciences", "geography",
                      "geography-edexcel"}


def get(path):
    r = urllib.request.Request(URL + "/rest/v1/" + path, headers=H)
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


def family_of(slug):
    return re.sub(r"-(aqa|edexcel(-[ab])?|eduqas|wjec|ncfe|ocr(-[ab])?)$", "", slug or "")


def text_of(p):
    """Student-facing text of a problem, tags stripped."""
    parts = [p.get("question") or "", p.get("display") or "", p.get("explanation") or ""]
    parts += [o for o in (p.get("options") or []) if isinstance(o, str)]
    return TAGS.sub(" ", " ".join(parts))


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_fraction_dict(x):
    return (isinstance(x, dict)
            and is_num(x.get("numerator")) and is_num(x.get("denominator")))


class Findings:
    def __init__(self):
        self.rows = []                      # every finding
        self.by_check = defaultdict(int)
        self.by_family = defaultdict(lambda: defaultdict(int))

    def add(self, sev, check, lesson, where, msg):
        self.rows.append({
            "severity": sev, "check": check, "family": lesson["family"],
            "subject": lesson["subject"], "unit": lesson["unit"],
            "lesson": lesson["number"], "title": lesson["title"],
            "url": "https://www.studyvault.co.uk/practice/%s/%s/%s"
                   % (lesson["subject"], lesson["unit"], lesson["number"]),
            "where": where, "message": msg,
        })
        self.by_check[(sev, check)] += 1
        self.by_family[lesson["family"]][sev] += 1


def check_problem(F, lesson, tier, i, p, prompts):
    where = "%s[%d]" % (tier, i)
    if not isinstance(p, dict):
        F.add("ERROR", "not-an-object", lesson, where, "problem is %s" % type(p).__name__)
        return
    t = p.get("input_type") or "single_value"
    q = (p.get("question") or "").strip()
    d = (p.get("display") or "").strip()

    # E1 — nothing to answer, in ANY ask-bearing field
    if not any(p.get(k) for k in ASK_FIELDS):
        F.add("ERROR", "no-ask", lesson, where,
              "no ask in any of question/display/source_text/pairs/audio/…")

    # W1 — the defect class the human QA actually found: a chart described but
    # nothing asked. Pure-LaTeX display without a chart is normal maths.
    if p.get("chart") is not None and not ASK_CUES.search(TAGS.sub(" ", q + " " + d)):
        F.add("WARN", "chart-no-question", lesson, where,
              "chart present but nothing asked (no question mark, no imperative)")

    # E2/E3 — multiple choice structure
    if t == "multiple_choice":
        opts = p.get("options")
        sol = p.get("solutions")
        if not isinstance(opts, list) or len(opts) < 2:
            F.add("ERROR", "mc-options", lesson, where, "options missing or fewer than 2")
        else:
            for o in opts:
                if not isinstance(o, str) or not o.strip():
                    F.add("ERROR", "mc-options", lesson, where, "empty or non-string option")
                    break
            if len(set(opts)) != len(opts):
                F.add("ERROR", "mc-duplicate-options", lesson, where,
                      "duplicate option text — two right answers or two identical wrong ones")
            for o in opts:
                if isinstance(o, str) and OPTION_PREFIX.match(o):
                    F.add("ERROR", "mc-prefixed-option", lesson, where,
                          "option starts '%s' — the renderer adds letter badges, this double-renders"
                          % o[:3])
                    break
        if (not isinstance(sol, list) or len(sol) != 1
                or not isinstance(sol[0], int) or isinstance(sol[0], bool)):
            F.add("ERROR", "mc-solutions", lesson, where,
                  "solutions must be [correctIndex], got %s" % json.dumps(sol)[:60])
        elif isinstance(opts, list) and not (0 <= sol[0] < len(opts)):
            F.add("ERROR", "mc-index-range", lesson, where,
                  "correct index %d outside options[%d]" % (sol[0], len(opts)))

    # E4 — numeric answer keys
    elif t in NUMERIC_TYPES:
        sol = p.get("solutions")
        if not isinstance(sol, list) or not sol:
            F.add("ERROR", "numeric-solutions", lesson, where,
                  "%s has no solutions list" % t)
        elif not all(is_num(x) for x in sol):
            F.add("ERROR", "numeric-solutions", lesson, where,
                  "%s solutions not all numeric: %s" % (t, json.dumps(sol)[:60]))
        elif t in PAIR_TYPES and len(sol) != 2:
            F.add("ERROR", "pair-solutions", lesson, where,
                  "%s needs exactly 2 values, got %d" % (t, len(sol)))

    # E5 — fraction: number or {numerator, denominator}
    elif t == "fraction":
        sol = p.get("solutions")
        ok = (isinstance(sol, list) and sol
              and all(is_num(x) or is_fraction_dict(x) for x in sol))
        if not ok:
            F.add("ERROR", "fraction-solutions", lesson, where,
                  "fraction solutions must be numbers or {numerator,denominator}: %s"
                  % json.dumps(sol)[:60])

    # E9 — a dangling AI prompt key means marking silently has no rubric
    if p.get("ai_prompt_key") is not None:
        if not isinstance(prompts, dict) or p["ai_prompt_key"] not in prompts:
            F.add("ERROR", "dangling-ai-prompt", lesson, where,
                  "ai_prompt_key '%s' not in this lesson's ai_marking_prompts"
                  % p["ai_prompt_key"])
    elif t in ("ai_mark", "ai_write") and not p.get("ai_system_prompt"):
        F.add("WARN", "ai-no-prompt", lesson, where,
              "%s carries neither ai_prompt_key nor ai_system_prompt" % t)

    # E6/W8 — junk and mojibake in student-facing text
    txt = text_of(p)
    m = JUNK.search(txt)
    if m:
        F.add("ERROR", "junk-literal", lesson, where,
              "literal '%s' in student-facing text" % m.group(0))
    if MOJIBAKE.search(txt):
        F.add("WARN", "mojibake", lesson, where, "encoding damage in text")

    # W3/W4 — board names and mark-scheme language in front of a student
    m = BOARD_WORDS.search(txt)
    if m:
        F.add("WARN", "board-name", lesson, where,
              "board name '%s' in student-facing text" % m.group(0))
    m = MARKSCHEME_WORDS.search(txt)
    if m:
        F.add("WARN", "markscheme-language", lesson, where,
              "'%s' is mark-scheme language" % m.group(0))


def check_lesson(F, lesson, pd):
    pb = pd.get("problem_bank") or {}
    prompts = pd.get("ai_marking_prompts")
    fam = lesson["family"]

    total = 0
    seen_asks = {}
    for tier in TIERS:
        arr = pb.get(tier)
        if not isinstance(arr, list) or not arr:
            F.add("WARN", "empty-tier", lesson, tier, "tier missing or empty")
            continue
        total += len(arr)
        for i, p in enumerate(arr):
            check_problem(F, lesson, tier, i, p, prompts)
            if isinstance(p, dict):
                # Identity is the WHOLE problem. Two earlier versions guessed
                # at "the content fields" and were wrong twice (vocab pairs,
                # then gap_fill's gaps). Only a byte-identical problem is a
                # duplicate; a single differing hint is a different problem.
                key = json.dumps(p, sort_keys=True, ensure_ascii=False)
                if key and key in seen_asks:
                    F.add("WARN", "duplicate-problem", lesson, "%s[%d]" % (tier, i),
                          "same ask as %s" % seen_asks[key])
                elif key:
                    seen_asks[key] = "%s[%d]" % (tier, i)

    if fam not in COUNT_EXEMPT_FAMILIES and not (COUNT_BAND[0] <= total <= COUNT_BAND[1]):
        F.add("WARN", "lesson-size", lesson, "bank",
              "%d problems (family norm is ~20; band %d-%d)" % (total, *COUNT_BAND))

    if fam in TIER_DESC_FAMILIES and not any(pb.get(t + "_description") for t in TIERS):
        F.add("WARN", "no-tier-descriptions", lesson, "bank",
              "no bronze/silver/gold descriptions (family convention has them)")


def main():
    only_family = None
    if "--family" in sys.argv:
        only_family = sys.argv[sys.argv.index("--family") + 1]

    units = {u["id"]: u for u in get("units?select=id,slug,subject_id")}
    subs = {s["id"]: s for s in get("subjects?select=id,slug,school_id,status")}

    F = Findings()
    lessons_checked = 0
    problems_checked = 0
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
                continue          # retired quals — invisible to students
            fam = family_of(s.get("slug"))
            if only_family and fam != only_family:
                continue
            lesson = {"family": fam, "subject": s.get("slug") or "?",
                      "unit": u.get("slug") or "?", "number": r.get("lesson_number"),
                      "title": r.get("title") or ""}
            check_lesson(F, lesson, pd)
            lessons_checked += 1
            problems_checked += sum(len(pb.get(t) or []) for t in TIERS)
        if len(rows) < 500:
            break
        page += 1

    errors = [r for r in F.rows if r["severity"] == "ERROR"]
    warns = [r for r in F.rows if r["severity"] == "WARN"]

    # ---- report ----
    L = []
    L.append("# Practice data validation report")
    L.append("")
    L.append("Generated by `scripts/_qa_practice_data.py` — structural checks only;")
    L.append("answer *correctness* (Phase 1, sympy) is not attempted here.")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    L.append("| Lessons checked | %d |" % lessons_checked)
    L.append("| Problems checked | %d |" % problems_checked)
    L.append("| **Errors** (lie to a student) | **%d** |" % len(errors))
    L.append("| Warnings (a human should look) | %d |" % len(warns))
    L.append("")
    L.append("## By check")
    L.append("")
    L.append("| Severity | Check | Count |")
    L.append("|---|---|---|")
    for (sev, check), n in sorted(F.by_check.items(), key=lambda kv: (kv[0][0], -kv[1])):
        L.append("| %s | %s | %d |" % (sev, check, n))
    L.append("")
    L.append("## By family")
    L.append("")
    L.append("| Family | Errors | Warnings |")
    L.append("|---|---|---|")
    for fam in sorted(F.by_family):
        c = F.by_family[fam]
        L.append("| %s | %d | %d |" % (fam, c.get("ERROR", 0), c.get("WARN", 0)))
    L.append("")
    if errors:
        L.append("## Every error")
        L.append("")
        for r in errors:
            L.append("- **%s** `%s` %s — %s  " % (r["check"], r["where"], r["message"], r["title"]))
            L.append("  %s" % r["url"])
        L.append("")
    L.append("## Worst lessons by findings")
    L.append("")
    per_lesson = defaultdict(list)
    for r in F.rows:
        per_lesson[r["url"]].append(r)
    worst = sorted(per_lesson.items(), key=lambda kv: -len(kv[1]))[:25]
    for url, rows in worst:
        r0 = rows[0]
        L.append("- %d finding(s) — %s (%s)  " % (len(rows), r0["title"], r0["family"]))
        L.append("  %s" % url)

    io.open(REPORT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    io.open(REPORT_JSON, "w", encoding="utf-8").write(json.dumps(F.rows, indent=1))

    print("checked %d lessons / %d problems" % (lessons_checked, problems_checked))
    print("ERRORS: %d   WARNINGS: %d" % (len(errors), len(warns)))
    print("report: %s" % REPORT_MD)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
