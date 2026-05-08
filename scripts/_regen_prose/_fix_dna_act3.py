"""Fix DNA Act 3 cigarette torture misplacement."""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

from lib.supabase_client import get_client
sb = get_client()

RSQUO = chr(0x2019)  # right single quotation mark '
LDQUO = chr(0x201C)  # left double quotation mark "
RDQUO = chr(0x201D)  # right double quotation mark "
MDASH = chr(0x2014)  # em dash —

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_surgical_fix_log.json')

def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, encoding='utf-8') as f:
            return json.load(f)
    return []

def save_log(entries):
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def record_fix(log_data, lid, slug, summary):
    for batch in log_data:
        if batch.get('batch') == 'A':
            batch['fixes'].append({'lesson_id': lid, 'lesson_slug': slug, 'fix_summary': summary})
            if lid not in batch['lessons_modified']:
                batch['lessons_modified'].append(lid)
            print(f"  FIX: {lid[:8]}... - {summary[:80]}")
            return

log_data = load_log()

# ============================================================
# DNA Act 3 154b - cigarette torture
# The lesson has: "she is the one who takes charge of controlling him. She <dfn...>tortures</dfn> Adam with a lit cigarette"
# Need to remove the cigarette torture from Act 3 since it was Act 1 backstory
# ============================================================
lid = '154bf6a7-55b0-4e0c-b019-0cd62cc40712'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']

idx = html.find('cigarette')
if idx >= 0:
    print(f"Cigarette at {idx}:")
    seg = html[max(0,idx-400):idx+400]
    print(repr(seg.encode('utf-8')[:600]))

    # The sentence structure: "She <dfn...>tortures</dfn> Adam with a lit cigarette, burning him to establish dominance and ensure his silence."
    # Replace this with describing Cathy's violence without the incorrect cigarette detail

    OLD_DFN_START = '<dfn class="term" data-def="To deliberately cause pain or suffering to someone, often as a display of power.">tortures</dfn> Adam with a lit cigarette, burning him to establish dominance and ensure his silence. This is the play\'s most physically violent moment — and significantly, it is one of the few acts of violence that occurs onstage ('

    # Build the replacement by finding the exact span
    # Find the dfn tag
    dfn_start = html.find('<dfn class="term" data-def="To deliberately cause', idx - 100)
    if dfn_start >= 0:
        # Find 'onstage (' to anchor the end of the old text
        onstage_idx = html.find('onstage (', dfn_start)
        if onstage_idx >= 0:
            old_str = html[dfn_start:onstage_idx]
            print(f"\nOld string: {repr(old_str.encode('utf-8')[:300])}")
            # New: just say Cathy exercises extreme control/violence without specifying cigarette
            new_str = 'acts with extreme violence and control, establishing dominance over Adam. This is one of the few acts of violence that occurs onstage ('
            new_html = html[:dfn_start] + new_str + html[onstage_idx + len('onstage ('):]
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/dna/act-3',
                       "Removed cigarette torture from Act 3 (was Act 1 backstory); replaced with accurate description of Cathy's violence")
            print("  Fixed")
        else:
            print("  WARN: 'onstage (' not found after dfn")
    else:
        print(f"  dfn_start not found near {idx}")

# ============================================================
# Check Journey's End Character Analysis 2042 - verify fixes
# ============================================================
print("\n=== Verify Journey's End Character Analysis ===")
lid = '2042d1a4-7334-454c-88bb-4d70f02c5f2a'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
if 'Osborne calls him' in html or "Osborne calls him" in html:
    print("  GOOD: Osborne attribution present")
else:
    print("  Checking for colonel/best company commander:")
    idx = html.find('best company commander')
    if idx >= 0:
        print(f"  At {idx}: {repr(html[max(0,idx-200):idx+200])}")
        # Still needs fixing
        m = re.search(r'the Colonel calls him .{0,5}the best company commander in the battalion.{0,5}', html)
        if m:
            old_str = m.group(0)
            print(f"  Match: {repr(old_str.encode('utf-8'))}")
            new_str = f'Osborne calls him {LDQUO}a long way the best company commander we{RSQUO}ve got{RDQUO}'
            new_html = html.replace(old_str, new_str)
            if new_html != html:
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature/journeys-end/character-analysis',
                           "Fixed attribution: 'best company commander' is Osborne's line not the Colonel's")
                print("  Fixed")

# Also check 'one man I could talk to as a friend' attribution in char analysis
idx = html.find('one man I could talk to as a friend')
if idx >= 0:
    print(f"  'one man...' still at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    # Check if Raleigh still misattributed
    nearby = html[max(0,idx-300):idx+50]
    if 'Raleigh' in nearby:
        print("  Raleigh attribution still present - needs fix")
        m = re.search(r'Raleigh.{0,30}s description of Stanhope as .{0,5}the one man I could talk to as a friend', html)
        if m:
            old_str = m.group(0)
            new_html = html.replace(old_str, f'Raleigh admires Stanhope deeply, though it is Stanhope who later describes Osborne as {LDQUO}the one man I could trust {MDASH} my best friend{RDQUO}')
            if new_html != html:
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature/journeys-end/character-analysis',
                           "Corrected 'one man I could talk to as a friend' from Raleigh→Stanhope about Osborne")
                print("  Fixed attribution")
else:
    print("  'one man...' not found - already fixed or different phrasing")

save_log(log_data)
print("\n=== DONE ===")
total_fixes = sum(len(b.get('fixes', [])) for b in log_data if b.get('batch') == 'A')
total_lessons = len(set(f['lesson_id'] for b in log_data if b.get('batch') == 'A' for f in b.get('fixes', [])))
print(f"Total fixes in log: {total_fixes}")
print(f"Total unique lessons: {total_lessons}")
