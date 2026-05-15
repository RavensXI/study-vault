"""Insert Religious Studies Edexcel content into Supabase.

Some slugs are intentionally shared across units (e.g. paper-1-christianity
and paper-2-christianity share lesson content). Each JSON file carries one
_lesson_id but the same content needs to go into ALL rows with that slug.
Insert-by-slug handles this — query lesson rows by slug+subject and update
every match.
"""
import argparse, glob, json, os, sys, requests
from collections import defaultdict

ARTICLE_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]

URL = os.environ['SUPABASE_URL']
KEY = os.environ['SUPABASE_SERVICE_KEY']
H = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'}


def load_json(path):
    raw = open(path, "rb").read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    return json.loads(raw.decode('utf-8'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # Build slug → [lesson_ids] map
    sid = requests.get(f"{URL}/rest/v1/subjects", headers=H,
                       params={"slug": "eq.religious-studies-edexcel",
                               "school_id": "is.null", "select": "id"}).json()[0]['id']
    units = requests.get(f"{URL}/rest/v1/units", headers=H,
                         params={"subject_id": f"eq.{sid}", "select": "id"}).json()
    unit_ids = ','.join(u['id'] for u in units)
    lessons = requests.get(f"{URL}/rest/v1/lessons", headers=H,
                           params={"unit_id": f"in.({unit_ids})",
                                   "select": "id,slug,content_html", "limit": "200"}).json()
    ids_by_slug = defaultdict(list)
    for L in lessons:
        ids_by_slug[L['slug']].append(L['id'])
    print(f"Shells: {len(lessons)} lessons / {len(ids_by_slug)} slugs "
          f"({sum(1 for v in ids_by_slug.values() if len(v) > 1)} slugs across multiple rows)")

    paths = sorted(glob.glob("scripts/_content_religious-studies-edexcel/lessons/*.json"))
    print(f"Found {len(paths)} content JSONs\n")

    # ====== PASS 1: insert by _lesson_id ======
    print("=== PASS 1: insert by _lesson_id ===")
    pass1_ok = 0
    pass1_miss = 0
    targeted_ids = set()
    for p in paths:
        try:
            data = load_json(p)
        except Exception as e:
            print(f"  [PARSE-FAIL] {p}: {e}")
            pass1_miss += 1
            continue
        slug = os.path.splitext(os.path.basename(p))[0]
        lid = data.get("_lesson_id")
        if not lid:
            print(f"  [SKIP] {slug} -- no _lesson_id")
            pass1_miss += 1
            continue
        payload = {k: data[k] for k in ARTICLE_KEYS if k in data}
        if args.dry_run:
            print(f"  [DRY] {slug[:55]:55s} -> {lid[:8]}")
            targeted_ids.add(lid); pass1_ok += 1
        else:
            r = requests.patch(f"{URL}/rest/v1/lessons", headers=H,
                               params={"id": f"eq.{lid}"}, json=payload)
            if r.status_code >= 300:
                print(f"  [FAIL] {slug}: {r.status_code} {r.text[:120]}")
            else:
                targeted_ids.add(lid); pass1_ok += 1

    # ====== PASS 2: fill empty sibling rows from same-slug rows ======
    print(f"\n=== PASS 2: copy to empty sibling rows (same slug, different unit) ===")
    pass2_ok = 0
    if not args.dry_run:
        # Refetch to see which rows now have content
        lessons2 = requests.get(f"{URL}/rest/v1/lessons", headers=H,
                                params={"unit_id": f"in.({unit_ids})",
                                        "select": ",".join(["id", "slug", "content_html"] + ARTICLE_KEYS),
                                        "limit": "200"}).json()
    else:
        lessons2 = lessons  # we don't actually have payload, just simulate
    by_slug_full = defaultdict(list)
    for L in lessons2:
        by_slug_full[L['slug']].append(L)
    for slug, rows in by_slug_full.items():
        if len(rows) < 2:
            continue
        # Find a row WITH content
        donor = next((r for r in rows if r.get('content_html')), None)
        if not donor:
            continue
        for r in rows:
            if r['id'] == donor['id']:
                continue
            if r.get('content_html'):
                continue  # already has its own content (disambiguated)
            payload = {k: donor.get(k) for k in ARTICLE_KEYS if donor.get(k) is not None}
            if args.dry_run:
                print(f"  [DRY] {slug[:55]:55s} {r['id'][:8]} <- copy from {donor['id'][:8]}")
                pass2_ok += 1
            else:
                resp = requests.patch(f"{URL}/rest/v1/lessons", headers=H,
                                      params={"id": f"eq.{r['id']}"}, json=payload)
                if resp.status_code >= 300:
                    print(f"  [FAIL] {slug} {r['id'][:8]}: {resp.status_code}")
                else:
                    print(f"  [OK]   {slug[:55]:55s} {r['id'][:8]} <- {donor['id'][:8]}")
                    pass2_ok += 1

    print()
    print(f"Pass 1: {pass1_ok} rows targeted by _lesson_id ({pass1_miss} files skipped/missing).")
    print(f"Pass 2: {pass2_ok} empty-sibling rows filled from same-slug donor.")
    print(f"Total rows updated: {pass1_ok + pass2_ok} / {len(lessons)}.")


if __name__ == "__main__":
    main()
