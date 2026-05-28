"""Phase 6 fact-check pass — web-verifies every direct quote, scripture
citation, named scholar attribution, named production, and specific statistic
against authoritative sources.

Mandatory for fact-heavy subjects:
- English Literature (any board)
- Religious Studies / RE (any board)
- History (any board)
- Geography (where case studies / statistics appear)
- Business (case studies + theorist attributions)
- Drama / Film Studies (set texts + practitioner attributions)
- Science (where named scientists, experiments, theories are attributed)

Skip for practice-format subjects (Maths, English Language practice, Spanish/
French/German practice) — they have no factual claims to fabricate.

Usage:
    python scripts/_fact_check_subject.py {subject-slug}
    python scripts/_fact_check_subject.py {subject-slug} --apply  # apply confident fixes (NOT YET IMPLEMENTED)

Output:
    scripts/_fact_check/{subject-slug}.json — per-lesson findings
    scripts/_fact_check/{subject-slug}.md   — Markdown summary

Exit codes:
    0 — no HIGH findings, ship clear
    1 — HIGH findings present, do not ship until reviewed
    2 — script error
"""
import argparse
import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client


# Subjects where fact-check is mandatory.
FACT_CHECK_REQUIRED = {
    # English Lit any board
    "english-literature-aqa", "english-literature-edexcel",
    "english-literature-ocr", "english-literature-eduqas",
    # Religious Studies / RE
    "religious-studies-aqa", "religious-studies", "religious-studies-eduqas",
    # History any board
    "history-aqa", "history-edexcel", "history-ocr", "history-ocr-b", "history-eduqas",
    # Geography (case studies)
    "geography-aqa", "geography-ocr", "geography-eduqas",
    "geography-edexcel-a", "geography-edexcel-b",
    # Business
    "business-aqa", "business-edexcel", "business-ocr",
    # Drama / Film
    "drama-aqa", "drama-ocr", "drama-eduqas", "film-studies-eduqas",
    # Science
    "science-aqa", "science-edexcel", "science-ocr", "separate-sciences",
    "separate-sciences-edexcel", "separate-sciences-ocr",
    "science-ocr-b", "separate-sciences-ocr-b",
    # Sociology
    "sociology-aqa", "sociology-eduqas",
    # Engineering (vocational — has named technologies/standards/dates that fabricate easily)
    "engineering-eduqas",
    # Computer Science (named scientists, dates, UK legislation, programming language history)
    "computer-science-aqa", "computer-science-eduqas",
    # Information Technology (vocational — named legislation, AR/IoT examples,
    # cyber-security cases that fabricate easily)
    "it-ocr",
    # Media Studies (theorist attributions, regulator scopes, dated productions —
    # very high fabrication risk; verify Hall, Mulvey, Propp, Todorov, Curran &
    # Seaton, Gerbner, Blumler & Katz, BBFC/OFCOM/IPSO/ASA/PEGI scope)
    "media-studies-aqa",
    # PE
    "physical-education-aqa", "physical-education-ocr", "physical-education-edexcel",
    # Geology (named formations, scientists, dates, crater sizes that fabricate easily)
    "geology-eduqas",
    # Design & Technology (named designers, products, regulations, material properties)
    "design-technology-eduqas", "design-technology",
    # Electronics (named inventors, IC functions, regulations)
    "electronics-eduqas",
    # Cambridge Nationals Enterprise & Marketing (real-business case studies, regs)
    "cambridge-nationals-enterprise-and-marketing",
    # Citizenship
    "citizenship-aqa",
    # Music
    "gcse-music", "music",
    # Psychology (named core studies, scholars, statistics — very high fabrication risk:
    # Asch %, Milgram %, Murdock list lengths, Piaget age ranges, Whorf claims,
    # Von Frisch dance distance, Bruner & Minturn, Gilchrist & Nesberg method)
    "psychology-aqa",
}

# Subjects where fact-check is unnecessary (practice format / no factual claims).
FACT_CHECK_SKIP = {
    "maths-aqa", "maths-edexcel", "maths-ocr", "maths-eduqas",
    "english-language-aqa", "english-language-edexcel",
    "english-language-ocr", "english-language-eduqas",
    "spanish-aqa", "spanish-edexcel",
    "french-aqa", "french-edexcel",
    "german-aqa", "german-edexcel",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject_slug", help="Subject slug, e.g. religious-studies-aqa")
    ap.add_argument("--apply", action="store_true",
                    help="(NOT YET IMPLEMENTED) Apply confident fixes automatically")
    args = ap.parse_args()

    if args.subject_slug in FACT_CHECK_SKIP:
        print(f"  SKIP: {args.subject_slug} is practice-format / has no factual claims to fabricate")
        return 0

    if args.subject_slug not in FACT_CHECK_REQUIRED:
        print(f"  WARN: {args.subject_slug} is not in the required list — running anyway, but consider adding it")

    sb = get_client()
    sub_rows = sb.table("subjects").select("id, name, exam_board").eq("slug", args.subject_slug).is_("school_id", "null").execute().data
    if not sub_rows:
        print(f"  ERR: free-tier subject not found for slug '{args.subject_slug}'")
        return 2
    subject = sub_rows[0]

    units = sb.table("units").select("id, slug, name").eq("subject_id", subject["id"]).order("sort_order").execute().data
    lessons = []
    for u in units:
        rows = sb.table("lessons").select("id, slug, lesson_number, title, content_html").eq("unit_id", u["id"]).order("lesson_number").execute().data
        for r in rows:
            if r.get("content_html"):
                lessons.append({
                    "lesson_id": r["id"],
                    "subject_slug": args.subject_slug,
                    "unit_slug": u["slug"],
                    "unit_name": u["name"],
                    "lesson_number": r["lesson_number"],
                    "lesson_title": r["title"],
                    "content_html": r["content_html"],
                })

    print(f"Subject: {subject['name']} ({args.subject_slug})")
    print(f"Lessons to fact-check: {len(lessons)}")
    print()

    out_dir = Path("scripts/_fact_check")
    out_dir.mkdir(exist_ok=True)
    plan_path = out_dir / f"{args.subject_slug}_plan.json"
    plan_path.write_text(json.dumps(lessons, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Lesson plan written: {plan_path}")
    print()
    print("=" * 70)
    print("NEXT: dispatch a Sonnet fact-check agent. The agent should:")
    print("  1. Read the plan file above")
    print("  2. For each lesson, identify fact-checkable claims:")
    print("     - Direct quotations (in quote marks)")
    print("     - Scripture citations (book + chapter/verse)")
    print("     - Named scholar/practitioner/theorist attributions")
    print("     - Named productions, dates, biographical facts")
    print("     - Specific statistics (production rates, census figures, etc.)")
    print("  3. Web-search authoritative sources to verify each claim:")
    print("     - Bible: BibleGateway, Bible.com")
    print("     - Qur'an: Quran.com (Sahih International)")
    print("     - Tanakh / Talmud: Sefaria.org (Bavli vs Yerushalmi distinction matters)")
    print("     - Bhagavad Gita: GitaSupersite")
    print("     - GGS: SikhiToTheMax")
    print("     - Tipitaka: SuttaCentral")
    print("     - Eng Lit set texts: Project Gutenberg + LitCharts + Folger")
    print("     - Historical events: Britannica, IWM, USHMM, gov.uk archives")
    print("     - Business/Geography stats: official corporate / ONS / gov sources")
    print("  4. Flag misalignments to scripts/_fact_check/{subject-slug}.json:")
    print("     - HIGH: fabricated quote, wrong scripture verse, wrong attribution")
    print("     - MEDIUM: real quote / wrong speaker, oversimplified")
    print("     - LOW: minor wording, edition variation")
    print("  5. Write Markdown report to scripts/_fact_check/{subject-slug}.md")
    print()
    print("If HIGH findings present after agent finishes: DO NOT SHIP.")
    print("Either fix in-place (surgical edit) or regenerate the affected lesson.")
    print("=" * 70)

    findings_path = out_dir / f"{args.subject_slug}.json"
    if findings_path.exists():
        findings = json.loads(findings_path.read_text(encoding="utf-8"))
        all_findings = findings.get("findings", []) if isinstance(findings, dict) else findings
        high = sum(1 for f in all_findings if isinstance(f, dict) and f.get("severity") == "high")
        med = sum(1 for f in all_findings if isinstance(f, dict) and f.get("severity") == "medium")
        low = sum(1 for f in all_findings if isinstance(f, dict) and f.get("severity") == "low")
        print()
        print(f"Findings: HIGH={high} MED={med} LOW={low}")
        if high > 0:
            print(f"  STATUS: BLOCKED — {high} HIGH findings must be fixed before shipping")
            return 1
        print("  STATUS: ship-ready (no HIGH findings)")
        return 0

    print(f"\n  No findings file yet — agent has not run for {args.subject_slug}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
