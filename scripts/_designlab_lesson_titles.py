"""Pull real lesson titles for the classic-dashboard demo subjects into
design-lab/_lesson_titles.json = { subjectSlug: { unitSlug: [title, ...] } }
so the lesson picker can show the actual title of each lesson.
"""
import json, os, sys, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from lib.supabase_client import get_client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "_lesson_titles.json")

# demo subject slug -> [unit slugs]  (mirrors dash-classic SUBJECTS)
DEMO = {
  "maths-aqa": ["number", "algebra", "geometry"],
  "english-language-aqa": ["paper-1-reading", "paper-1-writing", "paper-2-reading", "paper-2-writing"],
  "english-literature-aqa": ["macbeth", "a-christmas-carol", "power-and-conflict"],
  "science-aqa": ["biology-paper-1", "chemistry-paper-1", "physics-paper-1"],
  "history-aqa": ["germany-democracy-dictatorship", "conflict-tension-first-world-war", "britain-health-people", "elizabethan-england"],
  "geography-aqa": ["paper-1", "paper-2"],
  "spanish-aqa": ["people-and-lifestyle", "popular-culture", "communication-and-world"],
  "computer-science": ["computer-systems", "computational-thinking"],
  "religious-studies-ocr": ["christianity-beliefs-and-teachings", "islam-beliefs-and-teachings", "theme-relationships-and-families"],
}

def main():
    sb = get_client()
    out = {}
    for subj_slug, units in DEMO.items():
        srow = sb.table("subjects").select("id").eq("slug", subj_slug).is_("school_id", "null").execute().data
        if not srow:
            print("MISSING subject", subj_slug); continue
        sid = srow[0]["id"]
        out[subj_slug] = {}
        for uslug in units:
            urow = sb.table("units").select("id").eq("subject_id", sid).eq("slug", uslug).execute().data
            if not urow:
                print("  MISSING unit", subj_slug, uslug); out[subj_slug][uslug] = []; continue
            lessons = sb.table("lessons").select("title,lesson_number").eq("unit_id", urow[0]["id"]).order("lesson_number").execute().data or []
            out[subj_slug][uslug] = [l["title"] for l in lessons]
            print(f"  {subj_slug}/{uslug}: {len(lessons)} lessons")
    json.dump(out, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("->", OUT)

if __name__ == "__main__":
    main()
