"""Add _meta block to every Psychology lesson JSON. Filename pattern: {unit_slug}_L{NN}.json"""
import json, glob, os, re

DIR = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(DIR, "*.json")))
files = [f for f in files if "_reference_lesson" not in os.path.basename(f)]

pat = re.compile(r"^(?P<unit>[a-z0-9-]+)_L(?P<n>\d{2})\.json$")

added = 0
for p in files:
    name = os.path.basename(p)
    m = pat.match(name)
    if not m:
        print(f"  [SKIP] {name}: filename pattern mismatch")
        continue
    unit_slug = m.group("unit")
    lesson_number = int(m.group("n"))

    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "_meta" in data:
        # Update in place to be safe
        data["_meta"] = {
            "subject_slug": "psychology-aqa",
            "exam_board": "AQA",
            "school_id": None,
            "unit_slug": unit_slug,
            "lesson_number": lesson_number,
        }
    else:
        # Prepend _meta as first key
        new = {"_meta": {
            "subject_slug": "psychology-aqa",
            "exam_board": "AQA",
            "school_id": None,
            "unit_slug": unit_slug,
            "lesson_number": lesson_number,
        }}
        new.update(data)
        data = new

    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    added += 1
    print(f"  [OK] {name} -> unit={unit_slug} L{lesson_number:02d}")

print(f"\n[DONE] {added} files updated")
