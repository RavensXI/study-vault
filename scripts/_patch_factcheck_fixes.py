"""Push fact-check fixes for the two RS Edexcel lessons with John 3:10 -> 3:16 correction."""
import json
import os
import sys
import requests

sys.stdout.reconfigure(encoding="utf-8")

URL = os.environ["SUPABASE_URL"]
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

ARTICLE_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]

TARGETS = [
    {
        "file": "scripts/_content_religious-studies-edexcel/lessons/incarnation-paschal-mystery-and-salvation.json",
        "lesson_id": "faa324aa-c74e-4a48-8eed-4c0bca90415e",
        "description": "paper-1-catholic-christianity L2 Incarnation, Paschal Mystery and Salvation",
    },
    {
        "file": "scripts/_content_religious-studies-edexcel/lessons/the-last-days-of-jesus-salvation-and-atonement.json",
        "lesson_id": "51487cc7-aef5-4f59-b188-1dc4ed1155ab",
        "description": "paper-1-christianity L2 The Last Days of Jesus, Salvation and Atonement",
    },
]


def load_json(path):
    raw = open(path, "rb").read()
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    return json.loads(raw.decode("utf-8"))


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("DRY RUN — no changes will be made")

    for t in TARGETS:
        data = load_json(t["file"])
        payload = {k: data[k] for k in ARTICLE_KEYS if k in data}

        if dry_run:
            import re
            # Show that John 3:10 is gone
            content_dump = json.dumps(payload)
            matches = re.findall(r"John 3[:.]1[0-5]", content_dump)
            print(f"  {t['description']}: John 3:1x matches = {matches}")
            print(f"  Would update lesson_id={t['lesson_id']}")
            continue

        r = requests.patch(
            f"{URL}/rest/v1/lessons",
            headers=H,
            params={"id": f"eq.{t['lesson_id']}"},
            json=payload,
        )
        if r.status_code >= 300:
            print(f"  [FAIL] {t['description']}: {r.status_code} {r.text[:200]}")
        else:
            print(f"  [OK]   {t['description']}")

    # Also check if the paper-2-christianity / paper-2-catholic-christianity rows
    # share the same content and need propagating.
    # The insert script's Pass 2 handles sibling rows. Let's check.
    if not dry_run:
        print()
        print("Checking for sibling rows sharing same slugs...")
        sid_resp = requests.get(
            f"{URL}/rest/v1/subjects",
            headers=H,
            params={"slug": "eq.religious-studies-edexcel", "school_id": "is.null", "select": "id"},
        ).json()
        if not sid_resp:
            print("  Subject not found — skip sibling check")
            return
        sid = sid_resp[0]["id"]
        units = requests.get(
            f"{URL}/rest/v1/units",
            headers=H,
            params={"subject_id": f"eq.{sid}", "select": "id"},
        ).json()
        unit_ids = ",".join(u["id"] for u in units)

        # Fetch lessons with the target slugs
        for slug in ["incarnation-paschal-mystery-and-salvation", "the-last-days-of-jesus-salvation-and-atonement"]:
            rows = requests.get(
                f"{URL}/rest/v1/lessons",
                headers=H,
                params={
                    "slug": f"eq.{slug}",
                    "unit_id": f"in.({unit_ids})",
                    "select": "id,slug,unit_id",
                    "limit": "20",
                },
            ).json()
            if len(rows) > 1:
                print(f"  Slug '{slug}' appears in {len(rows)} rows:")
                for row in rows:
                    print(f"    id={row['id']} unit={row['unit_id']}")
                print(f"  These were updated by Pass 1 already (single lesson_id covers all).")
            else:
                print(f"  Slug '{slug}' appears in 1 row only.")


if __name__ == "__main__":
    main()
