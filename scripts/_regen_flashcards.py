"""
Flashcard retrofit orchestrator.

Reads lessons from Supabase, archives their current flashcards for rollback,
writes per-lesson input files for agents, and (after agents produce output)
validates + inserts the new cards back into Supabase.

Phases:
  python scripts/_regen_flashcards.py prep --subject business-aqa
    → archives existing cards + writes input JSONs for the agent(s)

  (agents run, produce output JSONs in scripts/_regen_flashcards_output/)

  python scripts/_regen_flashcards.py insert --subject business-aqa [--dry-run]
    → validates agent output and updates Supabase

Flags:
  --subject {slug}     limit to one subject
  --school-id {uuid|null}  default: null (free-tier)
  --limit N            limit number of lessons processed
  --dry-run            print what would happen, don't write
"""
import sys, os, argparse, json, re, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
from lib.supabase_client import get_client


# Map subject slug to category key (used by the agent to pick the recipe in FLASHCARD_RULES.md).
# Practice subjects return "practice" → agent skips.
CATEGORY_MAP = {
    # Practice format (skipped)
    'maths-aqa': 'practice', 'maths-ocr': 'practice', 'maths-edexcel': 'practice', 'maths-eduqas': 'practice',
    'english-language': 'practice',  # actually mixed — fallback
    'english-language-edexcel': 'practice', 'english-language-ocr': 'practice', 'english-language-eduqas': 'practice',
    'spanish': 'practice', 'french': 'practice', 'german': 'practice',
    'french-aqa': 'practice', 'spanish-aqa': 'practice', 'german-aqa': 'practice',
    # Article subjects → recipe keys
    'history': 'history',
    'history-aqa': 'history',  # future
    'religious-education': 're',
    'science': 'science', 'science-edexcel': 'science', 'science-ocr': 'science',
    'separate-sciences': 'science',
    'english-literature': 'english-literature',
    'english-literature-edexcel': 'english-literature',
    'english-literature-ocr': 'english-literature',
    'english-literature-eduqas': 'english-literature',
    'geography': 'geography',
    'business': 'business',  # Unity Edexcel
    'business-aqa': 'business', 'business-edexcel': 'business', 'business-ocr': 'business',
    'health-social-care': 'other',
    'hospitality-catering': 'other',
    'music-technology': 'other',
    'computer-science': 'other',
    'design-technology': 'other',
    'food-technology': 'other',
    'sport-science': 'other',
    'drama': 'english-literature',  # drama uses quote/character patterns
    'creative-imedia': 'other',
    'gcse-music': 'other',
}

INPUT_DIR = os.path.join('scripts', '_regen_flashcards_input')
OUTPUT_DIR = os.path.join('scripts', '_regen_flashcards_output')
BACKUP_ROOT = os.path.join('scripts', '_flashcard_backup')


def extract_key_facts(content_html):
    """Pull the <p> inside each <div class='key-fact'>."""
    facts = re.findall(
        r'<div class="key-fact"[^>]*>.*?<p>(.*?)</p>',
        content_html or '',
        flags=re.DOTALL,
    )
    out = []
    for f in facts:
        stripped = re.sub(r'<[^>]+>', '', f).strip()
        if stripped:
            out.append(stripped)
    return out


def prep_mode(sb, args):
    """Archive + write input JSONs for agents."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    today = datetime.date.today().isoformat()
    backup_dir = os.path.join(BACKUP_ROOT, today)
    os.makedirs(backup_dir, exist_ok=True)

    # Fetch subjects in scope
    q = sb.table('subjects').select('id,slug,name,exam_board,school_id')
    if args.subject:
        q = q.eq('slug', args.subject)
    if args.school_id == 'null':
        q = q.is_('school_id', 'null')
    elif args.school_id:
        q = q.eq('school_id', args.school_id)
    subjects = q.execute().data or []

    total_lessons = 0
    total_skipped_practice = 0
    total_lean = 0

    for subj in subjects:
        slug = subj['slug']
        category = CATEGORY_MAP.get(slug, 'other')
        if category == 'practice':
            print(f"[SKIP] {slug} (practice format — no flashcards)")
            continue

        units = sb.table('units').select('id,slug,name,subject_id').eq('subject_id', subj['id']).execute().data
        uids = [u['id'] for u in units]
        if not uids:
            continue

        lessons = (
            sb.table('lessons')
            .select('id,lesson_number,title,description,content_html,glossary_terms,flashcard_questions,status')
            .in_('unit_id', uids)
            .execute()
            .data
        )

        prepared = 0
        for l in lessons:
            # Skip lessons with no content_html (practice or empty shells)
            if not l.get('content_html'):
                continue
            if args.limit and prepared >= args.limit:
                break

            existing_fc = l.get('flashcard_questions') or []

            # Backup existing
            with open(os.path.join(backup_dir, f"{l['id']}.json"), 'w', encoding='utf-8') as f:
                json.dump({
                    'lesson_id': l['id'],
                    'subject_slug': slug,
                    'title': l['title'],
                    'flashcard_questions': existing_fc,
                    'archived_at': today,
                }, f, indent=2, ensure_ascii=False)

            # Build input JSON for agent
            key_facts = extract_key_facts(l.get('content_html'))
            input_data = {
                'lesson_id': l['id'],
                'title': l['title'],
                'description': l.get('description') or '',
                'subject_slug': slug,
                'subject_name': subj['name'],
                'exam_board': subj.get('exam_board') or '',
                'subject_category': category,
                'content_html': l['content_html'],
                'glossary_terms': l.get('glossary_terms') or [],
                'key_facts': key_facts,
                'existing_flashcards': existing_fc,
            }
            with open(os.path.join(INPUT_DIR, f"{l['id']}.json"), 'w', encoding='utf-8') as f:
                json.dump(input_data, f, indent=2, ensure_ascii=False)

            prepared += 1
            total_lessons += 1

        print(f"[PREP] {slug} ({category}): {prepared} lessons prepared for regeneration")

    print(f"\n[DONE] Total lessons prepared: {total_lessons}")
    print(f"Backup directory: {backup_dir}")
    print(f"Input directory: {INPUT_DIR}")
    print(f"Next: run the regen agents pointing at {INPUT_DIR}/, output to {OUTPUT_DIR}/")


def insert_mode(sb, args):
    """Validate agent output + write back to Supabase."""
    # Import validator
    from _validate_content_json import validate_flashcards

    output_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json') and not f.startswith('_')]
    if args.limit:
        output_files = output_files[:args.limit]
    print(f"Found {len(output_files)} agent output files")

    updated = 0
    skipped = 0
    failed = []

    for fname in output_files:
        path = os.path.join(OUTPUT_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        lesson_id = data.get('lesson_id') or fname.replace('.json', '')

        if data.get('skip'):
            print(f"  [SKIP] {lesson_id}: {data.get('reason', 'agent skipped')}")
            skipped += 1
            continue

        fc = data.get('flashcard_questions') or []
        violations = validate_flashcards(fc)

        if violations:
            print(f"  [FAIL] {lesson_id}:")
            for v in violations[:5]:
                print(f"     - {v}")
            failed.append((lesson_id, violations))
            continue

        if len(fc) < 6:
            print(f"  [FAIL] {lesson_id}: only {len(fc)} cards, need ≥6")
            failed.append((lesson_id, [f"too few cards ({len(fc)})"]))
            continue

        if args.dry_run:
            print(f"  [DRY] {lesson_id}: would update {len(fc)} cards")
        else:
            sb.table('lessons').update({'flashcard_questions': fc}).eq('id', lesson_id).execute()
            print(f"  [OK]  {lesson_id}: {len(fc)} cards")
            updated += 1

    print(f"\n[DONE] Updated {updated}, skipped {skipped}, failed {len(failed)}")
    if failed:
        failed_path = os.path.join(OUTPUT_DIR, f'_failed_{datetime.date.today().isoformat()}.json')
        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump([{'lesson_id': lid, 'violations': vs} for lid, vs in failed], f, indent=2)
        print(f"Failed list written to {failed_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prep', 'insert'])
    parser.add_argument('--subject')
    parser.add_argument('--school-id', default='null', help="'null' for free-tier, or a UUID")
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    sb = get_client()
    if args.mode == 'prep':
        prep_mode(sb, args)
    else:
        insert_mode(sb, args)


if __name__ == '__main__':
    main()
