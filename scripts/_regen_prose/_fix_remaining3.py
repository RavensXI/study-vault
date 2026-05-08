"""Fix pass 3 — final items."""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

from lib.supabase_client import get_client
sb = get_client()

RSQUO = '’'  # right single quotation mark '
LDQUO = '“'  # left double "
RDQUO = '”'  # right double "
MDASH = '—'  # em dash —
LSQUO = '‘'  # left single '
ELLIPSIS = '…'  # …

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
# Jekyll and Hyde Ch9-10 - 'in the glass' with unicode ellipsis
# ============================================================
print("\n=== Jekyll and Hyde Ch9-10 in the glass ===")
lid = '241ec110-09b6-448e-acab-91713c5f57c2'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']

# The text has: "...see his own face… in the glass."
# where … is unicode ellipsis U+2026
# We want: "...see his own face."
OLD = f'see his own face{ELLIPSIS} in the glass.{RDQUO}'
NEW = f'see his own face.{RDQUO}'

if OLD in html:
    new_html = html.replace(OLD, NEW)
    sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
    record_fix(log_data, lid, 'english-literature/jekyll-and-hyde/chapters-9-10',
               "Removed 'in the glass' with unicode ellipsis — not in Stevenson's original text")
    print(f"  Fixed")
else:
    # Try with ... instead
    OLD2 = f'see his own face... in the glass.{RDQUO}'
    if OLD2 in html:
        new_html = html.replace(OLD2, f'see his own face.{RDQUO}')
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature/jekyll-and-hyde/chapters-9-10',
                   "Removed 'in the glass' — not in Stevenson's original text")
        print(f"  Fixed (... variant)")
    else:
        print(f"  WARN: could not match. Checking bytes...")
        idx = html.find('in the glass')
        if idx >= 0:
            seg = html[max(0,idx-30):idx+20]
            print(f"  Bytes: {repr(seg.encode('utf-8'))}")
            # Direct removal approach
            new_html = html[:idx-2].rstrip() + html[idx+len('in the glass'):]
            # Also need to remove the leading ellipsis+space
            # Try: replace 'face… in the glass.' with 'face.'
            new_html2 = re.sub(r'see his own face[…\.]{0,3} in the glass\.', f'see his own face.', html)
            if new_html2 != html:
                sb.table('lessons').update({'content_html': new_html2}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature/jekyll-and-hyde/chapters-9-10',
                           "Removed 'in the glass' via regex — not in Stevenson's original text")
                print(f"  Fixed (regex)")
            else:
                print(f"  WARN: regex also failed")

# ============================================================
# Anita and Me Context c2e9 - 'If you want a nigger for a neighbour, vote Labour'
# Need to add Smethwick attribution since it's presented as Sam's speech
# ============================================================
print("\n=== Anita and Me Context c2e9 Smethwick ===")
lid = 'c2e90934-0470-49cb-8915-945c43c37131'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']

# The quote is Sam's fete speech but 'If you want a nigger...' is actually the
# 1964 Smethwick slogan. The audit says it's not confirmed as Sam's exact words.
# The lesson says "When Sam Lowbridge stands up at the village fete and declares, [quote]"
# This presents it as a direct quote from Sam. We need to clarify it as the Smethwick slogan.

OLD = f'{LDQUO}If you want a nigger for a neighbour, vote Labour,{RDQUO} he is echoing the language and attitudes that Powell legitimised.'
NEW = f'{LDQUO}If you want a nigger for a neighbour, vote Labour{RDQUO} {MDASH} echoing the notorious 1964 Smethwick election campaign slogan that circulated in the West Midlands {MDASH} he is repeating the language and attitudes that Powell legitimised.'
if OLD in html:
    new_html = html.replace(OLD, NEW)
    sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
    record_fix(log_data, lid, 'english-literature-aqa/anita-and-me/context',
               "Added Smethwick election context: Sam's fete speech echoes the 1964 Smethwick campaign slogan")
    print(f"  Fixed")
else:
    # The quote is in the novel — let's check the actual rendering
    idx = html.find('nigger for a neighbour')
    if idx >= 0:
        seg = html[max(0,idx-200):idx+200]
        print(f"  Bytes: {repr(seg.encode('utf-8')[:300])}")
        # Try simpler: add Smethwick note after the quote
        m = re.search(r'nigger for a neighbour, vote Labour.{0,5},? he is echoing', html)
        if m:
            old_str = m.group(0)
            new_str = old_str.replace(', he is echoing', ' — echoing the notorious 1964 Smethwick election slogan — he is repeating')
            new_html = html.replace(old_str, new_str)
            if new_html != html:
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature-aqa/anita-and-me/context',
                           "Clarified Sam's fete speech as echoing the 1964 Smethwick election slogan")
                print(f"  Fixed via regex")
            else:
                print(f"  WARN: replace failed")
        else:
            print(f"  WARN: pattern not matched")

# ============================================================
# Anita and Me Racism c3e0 - same Smethwick fix
# ============================================================
print("\n=== Anita and Me Racism c3e0 Smethwick ===")
lid = 'c3e0ba3c-9e6a-456d-8835-be00b08fc4c2'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']

idx = html.find('nigger for a neighbour')
if idx >= 0:
    seg = html[max(0,idx-200):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:300])}")
    # This lesson says Sam "declares" the slogan — add Smethwick note
    # Pattern: '"If you want a nigger for a neighbour, vote Labour," he declares.'
    m = re.search(r'nigger for a neighbour, vote Labour.{0,5},? he declares\.', html)
    if m:
        old_str = m.group(0)
        new_str = 'nigger for a neighbour, vote Labour' + RDQUO + ' — echoing the notorious 1964 Smethwick election slogan — Sam declares himself aligned with the far right.'
        # Be more careful about what to replace
        seg_start = html.rfind(LDQUO, 0, idx)
        if seg_start >= 0:
            old_full = html[seg_start:m.end()]
            new_full = LDQUO + 'If you want a nigger for a neighbour, vote Labour' + RDQUO + ' — echoing the notorious 1964 Smethwick election slogan — Sam declares himself aligned with the far right.'
            new_html = html.replace(old_full, new_full)
            if new_html != html:
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature-aqa/anita-and-me/racism-growing-apart',
                           "Added 1964 Smethwick election context to Sam's fete speech attribution")
                print(f"  Fixed")
            else:
                print(f"  WARN: replace failed")
        else:
            print(f"  WARN: opening quote not found")
    else:
        print(f"  WARN: pattern not matched")
else:
    print(f"  'nigger for a neighbour' not found")

# ============================================================
# Lord of the Flies Edexcel L3 - 'Which is better' — check all occurrences
# ============================================================
print("\n=== LOTF Edexcel L3 - full content check ===")
lid = 'f1e60ae7-c6ac-467a-8019-cdea9ac55afe'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']

# Look for 'better' in various forms
for phrase in ['better', 'rules and agree', 'Ralph', 'Piggy']:
    idx = html.find(phrase)
    count = 0
    while idx >= 0 and count < 3:
        print(f"  '{phrase}' at {idx}: {repr(html[max(0,idx-50):idx+100])}")
        idx = html.find(phrase, idx+1)
        count += 1
    if count == 0:
        print(f"  '{phrase}' not found")

# ============================================================
# Anita and Me d65d Part 3 - 'Rivers of Blood' check
# ============================================================
print("\n=== Anita and Me Part 3 d65d ===")
lid = 'd65db752-979e-4192-9f80-d01ba8fa7dd8'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
# Check for Sam and Powell references
for phrase in ['Rivers of Blood', 'Powell', 'Sam', 'fete', 'Spring Fete']:
    idx = html.find(phrase)
    if idx >= 0:
        print(f"  '{phrase}' at {idx}: {repr(html[max(0,idx-100):idx+200])}")
    else:
        print(f"  '{phrase}' not found")

save_log(log_data)
print("\n=== DONE ===")
total_fixes = sum(len(b.get('fixes', [])) for b in log_data if b.get('batch') == 'A')
total_lessons = len(set(f['lesson_id'] for b in log_data if b.get('batch') == 'A' for f in b.get('fixes', [])))
print(f"Total fixes in log: {total_fixes}")
print(f"Total lessons: {total_lessons}")
