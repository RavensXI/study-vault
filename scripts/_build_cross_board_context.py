"""
Build the existing-board context that gets injected into the planning agent
when starting a new board for a subject we already have.

Usage:
  python scripts/_build_cross_board_context.py --source-slug business-aqa --out scripts/_cross_board_business_aqa.json

Output:
  {
    "source_plan": { ... full plan JSON ... },
    "source_lessons": [
      {
        "unit_slug": "...",
        "unit_name": "...",
        "lesson_number": 1,
        "title": "...",
        "description": "...",
        "spec_references": [...],
        "word_count": N,
        "key_topics": ["..."],   // extracted from h2s + glossary terms
        "glossary_terms": ["..."]
      }, ...
    ]
  }
"""
import sys, os, json, re, argparse, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client


def extract_key_topics(content_html, glossary_terms):
    """Pull top-level topic markers from the content: h2 headings + glossary terms."""
    if not content_html:
        return []
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content_html, flags=re.DOTALL)
    h2s = [re.sub(r'<[^>]+>', '', h).strip() for h in h2s]
    topics = [h for h in h2s if h]
    # Also include glossary term strings
    for g in (glossary_terms or []):
        t = (g.get('term') if isinstance(g, dict) else None) or ''
        if t and t not in topics:
            topics.append(t)
    return topics[:15]  # cap


def word_count_strip_html(html):
    if not html:
        return 0
    return len(re.sub(r'<[^>]+>', ' ', html).split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-slug", required=True, help="e.g. business-aqa")
    parser.add_argument("--out", required=True, help="output JSON path")
    args = parser.parse_args()

    sb = get_client()
    subj = (
        sb.table("subjects")
        .select("id,slug,name,exam_board,settings")
        .eq("slug", args.source_slug)
        .is_("school_id", "null")
        .single()
        .execute()
        .data
    )
    if not subj:
        print(f"ERROR: source subject {args.source_slug} not found")
        sys.exit(1)

    # Find the plan JSON on disk (produced by earlier planning run)
    plan_candidates = glob.glob(f"scripts/_plan_{args.source_slug.replace('-', '_')}*.json")
    plan_candidates += glob.glob(f"scripts/_plan_{args.source_slug}*.json")
    plan_candidates = [p for p in plan_candidates if "_sanitised" not in p]
    plan_candidates_s = glob.glob(f"scripts/_plan_{args.source_slug}*_sanitised.json")
    source_plan = None
    chosen = plan_candidates_s[0] if plan_candidates_s else (plan_candidates[0] if plan_candidates else None)
    if chosen:
        with open(chosen, "r", encoding="utf-8") as f:
            source_plan = json.load(f)
        print(f"Loaded source plan: {chosen}")
    else:
        print(f"WARN: no on-disk plan JSON for {args.source_slug}. Proceeding with summaries only.")

    # Build per-lesson summaries
    units = (
        sb.table("units")
        .select("id,slug,name,sort_order")
        .eq("subject_id", subj["id"])
        .order("sort_order")
        .execute()
        .data
    )

    summaries = []
    for u in units:
        lessons = (
            sb.table("lessons")
            .select("lesson_number,title,description,content_html,glossary_terms")
            .eq("unit_id", u["id"])
            .order("lesson_number")
            .execute()
            .data
        )
        for l in lessons:
            summaries.append({
                "unit_slug": u["slug"],
                "unit_name": u["name"],
                "lesson_number": l["lesson_number"],
                "title": l["title"],
                "description": l.get("description", ""),
                "word_count": word_count_strip_html(l.get("content_html", "")),
                "key_topics": extract_key_topics(l.get("content_html"), l.get("glossary_terms")),
                "glossary_terms": [
                    (g.get("term") if isinstance(g, dict) else str(g))
                    for g in (l.get("glossary_terms") or [])
                ][:10],
            })

    out = {
        "source_subject": {
            "slug": subj["slug"],
            "name": subj["name"],
            "exam_board": subj["exam_board"],
        },
        "source_plan": source_plan,
        "source_lessons": summaries,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] {len(summaries)} lesson summaries written to {args.out}")
    print(f"Source plan included: {source_plan is not None}")


if __name__ == "__main__":
    main()
