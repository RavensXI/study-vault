"""
One-off: prepare input JSONs + backup for the 5 sample lessons
used to gate the flashcard retrofit.
"""
import sys, os, json, datetime, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
from lib.supabase_client import get_client
from _regen_flashcards import CATEGORY_MAP, INPUT_DIR, BACKUP_ROOT, extract_key_facts

SAMPLES = [
    ('eaf4fe6e-4176-4f09-be3c-d86eca46405b', 'history'),
    ('dfd00dfa-146e-45a2-80bb-878e8b5d71fb', 'business-aqa'),
    ('9532fc0f-c8e7-48bf-a63c-67baabef0466', 'english-literature'),
    ('91783d20-0104-44d2-bf13-57bbbd99fd0d', 'religious-education'),
    ('0e45f87f-fb4f-45dc-80c0-7d0f0e3bed5f', 'science'),
]

sb = get_client()
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(os.path.join('scripts', '_regen_flashcards_output'), exist_ok=True)
today = datetime.date.today().isoformat()
backup_dir = os.path.join(BACKUP_ROOT, today)
os.makedirs(backup_dir, exist_ok=True)

for lid, subject_slug in SAMPLES:
    lesson = (
        sb.table('lessons')
        .select('id,title,description,content_html,glossary_terms,flashcard_questions,unit_id')
        .eq('id', lid)
        .single()
        .execute()
        .data
    )
    unit = sb.table('units').select('subject_id').eq('id', lesson['unit_id']).single().execute().data
    subj = sb.table('subjects').select('slug,name,exam_board').eq('id', unit['subject_id']).single().execute().data

    category = CATEGORY_MAP.get(subject_slug, 'other')

    # Backup
    with open(os.path.join(backup_dir, f"{lid}.json"), 'w', encoding='utf-8') as f:
        json.dump({
            'lesson_id': lid,
            'subject_slug': subject_slug,
            'title': lesson['title'],
            'flashcard_questions': lesson.get('flashcard_questions') or [],
            'archived_at': today,
        }, f, indent=2, ensure_ascii=False)

    # Input for agent
    input_data = {
        'lesson_id': lid,
        'title': lesson['title'],
        'description': lesson.get('description') or '',
        'subject_slug': subj['slug'],
        'subject_name': subj['name'],
        'exam_board': subj.get('exam_board') or '',
        'subject_category': category,
        'content_html': lesson['content_html'],
        'glossary_terms': lesson.get('glossary_terms') or [],
        'key_facts': extract_key_facts(lesson.get('content_html')),
        'existing_flashcards': lesson.get('flashcard_questions') or [],
    }
    with open(os.path.join(INPUT_DIR, f"{lid}.json"), 'w', encoding='utf-8') as f:
        json.dump(input_data, f, indent=2, ensure_ascii=False)

    print(f"[PREP] {category:20s} {lesson['title'][:50]}")

print(f"\n[DONE] 5 sample lessons prepared. Run the regen agent, then:")
print(f"  python scripts/_regen_flashcards.py insert --dry-run")
