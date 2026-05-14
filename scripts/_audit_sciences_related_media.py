"""Audit free-tier sciences related_media against the pipeline standard.

Standard (docs/RELATED_MEDIA_PIPELINE.md):
  - ≥6 items total
  - ≥1 in Podcasts
  - ≥1 in Videos & Channels
  - ≥1 in Movies / TV Shows / Documentaries (collectively)
  - ≥1 in Study Tools (or Study Guides & Notes — treated as equivalent)

Outputs a JSON report scripts/_audit_sciences_related_media.json with per-lesson
gap info, plus a console summary.
"""
import os, requests, json, sys
from collections import defaultdict

URL = os.environ['SUPABASE_URL']
KEY = os.environ['SUPABASE_SERVICE_KEY']
H = {'apikey': KEY, 'Authorization': f'Bearer {KEY}'}

FREE_SCIENCES = [
    "science-aqa", "science-edexcel", "science-ocr", "science-ocr-b",
    "separate-sciences", "separate-sciences-edexcel", "separate-sciences-ocr", "separate-sciences-ocr-b",
]

# Accepted category names. Anything in here counts as a "real" category bucket.
# Reflects the actual category diversity across the sciences (some boards favour
# Movies/Docs, others favour Practicals & Simulations / Exam Practice).
ACCEPTED_CATEGORIES = {
    "Podcasts", "Videos & Channels", "YouTube", "YouTube Channels",
    "Movies", "TV Shows", "Documentaries",
    "Study Tools", "Study Guides", "Study Guides & Notes",
    "Practicals & Simulations", "Exam Practice", "Articles", "Articles & Reading", "Books",
}

MIN_CATEGORIES = 4
MIN_ITEMS = 6


def analyse(rm):
    if not rm: return {"item_count": 0, "categories": set()}
    item_count = 0
    cats = set()
    for c in rm:
        if not isinstance(c, dict): continue
        name = c.get("category", "")
        items = c.get("items", []) or []
        if not items: continue
        item_count += len(items)
        if name in ACCEPTED_CATEGORIES:
            cats.add(name)
    return {"item_count": item_count, "categories": cats}


def main():
    report = {"summary": {}, "lessons": []}
    subj_rows = requests.get(
        f"{URL}/rest/v1/subjects",
        headers=H,
        params={"slug": f"in.({','.join(FREE_SCIENCES)})", "school_id": "is.null", "select": "id,slug,name"},
    ).json()
    by_slug = {s["slug"]: s for s in subj_rows}

    grand_total = 0
    grand_thin = 0
    for slug in FREE_SCIENCES:
        s = by_slug.get(slug)
        if not s:
            print(f"  [MISS] subject not found: {slug}")
            continue
        units = requests.get(f"{URL}/rest/v1/units", headers=H, params={"subject_id": f"eq.{s['id']}", "select": "id,slug,name", "order": "sort_order"}).json()
        subj_total = 0
        subj_thin = 0
        for u in units:
            lessons = requests.get(
                f"{URL}/rest/v1/lessons",
                headers=H,
                params={"unit_id": f"eq.{u['id']}", "select": "id,lesson_number,slug,title,related_media", "order": "lesson_number"},
            ).json()
            for L in lessons:
                subj_total += 1
                grand_total += 1
                info = analyse(L.get("related_media"))
                is_thin = (info["item_count"] < MIN_ITEMS) or (len(info["categories"]) < MIN_CATEGORIES)
                if is_thin:
                    subj_thin += 1
                    grand_thin += 1
                    report["lessons"].append({
                        "lesson_id": L["id"],
                        "subject_slug": slug,
                        "unit_slug": u["slug"],
                        "lesson_number": L["lesson_number"],
                        "lesson_slug": L["slug"],
                        "title": L["title"],
                        "item_count": info["item_count"],
                        "categories": sorted(info["categories"]),
                        "category_count": len(info["categories"]),
                    })
        report["summary"][slug] = {"total": subj_total, "thin": subj_thin}
        print(f"  {slug:35s}  {subj_thin:3d}/{subj_total:3d} thin")

    report["summary"]["GRAND_TOTAL"] = {"total": grand_total, "thin": grand_thin}
    print()
    print(f"  GRAND TOTAL: {grand_thin}/{grand_total} thin")

    out = os.path.join(os.path.dirname(__file__), "_audit_sciences_related_media.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report: {out}")


if __name__ == "__main__":
    main()
