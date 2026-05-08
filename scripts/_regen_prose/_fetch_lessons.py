"""Fetch content for the 5 lessons targeted for section rewrite."""
import sys, os, json
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lib.supabase_client import get_client

LESSON_IDS = [
    "26985264-3dc8-48c5-9799-288d4fb42679",  # Coram Boy Part 3
    "2fe05d71-6399-483a-a753-1bdbda1322ed",  # Jane Eyre Gateshead AQA
    "c25f6db3-84f3-436c-bfbc-cf5a1fdc57e5",  # Journey's End Act 1
    "aad20898-d4c7-4b15-9ed3-a431d3d2499c",  # Pigeon English The Ending
    "9abb3b24-d5be-4a40-8fd8-7a44b8f14dd1",  # Pigeon English Harri's World (hutious)
    "af603814-9d9b-4c5d-abb4-3f00a87a0c1d",  # Pigeon English Character Analysis (hutious)
    "263021cb-1ef8-4ff0-a975-2049493a0bba",  # Princess & The Hustler Act 1
]

sb = get_client()
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(out_dir, exist_ok=True)

for lid in LESSON_IDS:
    res = sb.table('lessons').select(
        'id,title,lesson_number,content_html,exam_tip_html,conclusion_html,glossary_terms,flashcard_questions,knowledge_checks'
    ).eq('id', lid).single().execute()
    if res.data:
        fname = os.path.join(out_dir, f"{lid}.json")
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(res.data, f, ensure_ascii=False, indent=2)
        print(f"Fetched: {res.data['title']} (lesson {res.data['lesson_number']})")
    else:
        print(f"NOT FOUND: {lid}")
