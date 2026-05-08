"""Fix remaining items that couldn't be found due to quote character differences."""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

from lib.supabase_client import get_client
sb = get_client()

RSQUO = '’'
LDQUO = '“'
RDQUO = '”'
MDASH = '—'
LSQUO = '‘'

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_surgical_fix_log.json')

def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, encoding='utf-8') as f:
            return json.load(f)
    return []

def save_log(entries):
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

fixes_added = []

def record_fix(log_data, lid, slug, summary):
    for batch in log_data:
        if batch.get('batch') == 'A':
            batch['fixes'].append({'lesson_id': lid, 'lesson_slug': slug, 'fix_summary': summary})
            if lid not in batch['lessons_modified']:
                batch['lessons_modified'].append(lid)
            fixes_added.append(lid)
            print(f"  FIX: {lid[:8]}... - {summary[:80]}")
            return
    # Shouldn't get here
    print(f"  WARNING: Batch A not found in log")

log_data = load_log()

# ============================================================
# A Taste of Honey - Act 2 'pansified little freak' verification
# ============================================================
print("\n=== Verify pansified little freak fixes ===")
for lid in ['a7a18a44-94ab-4454-9dce-89decf924e66', 'ce6affd5-7027-40c2-b46a-eed6537b7d60']:
    res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
    html = res.data['content_html']
    if 'pansified' in html:
        print(f"  GOOD: {lid[:8]} has pansified")
        record_fix(log_data, lid, 'english-literature/a-taste-of-honey/act-2',
                   "Restored 'pansified' to Helen's insult — accurate quote is 'pansified little freak'")
    else:
        print(f"  MISSING: {lid[:8]} - checking...")

# ============================================================
# An Inspector Calls OCR Act 1 - verify + check Key Fact
# ============================================================
print("\n=== Verify AIC OCR Act 1 ===")
lid = '07014cb8-5bfd-45f3-9e94-3fd18515edd2'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
if 'When Sheila says' in html:
    print(f"  GOOD: body text fixed")
if "Sheila's line" in html or f"Sheila{RSQUO}s line" in html:
    print(f"  GOOD: Key Fact fixed")
    record_fix(log_data, lid, 'english-literature-ocr/an-inspector-calls/act-1',
               "Fixed misattribution: 'these girls aren't cheap labour' is Sheila's line in both body text and Key Fact box")
else:
    # Check key fact
    idx = html.find('Key Fact')
    if idx >= 0:
        print(f"  KeyFact context: {repr(html[idx:idx+300])}")

# ============================================================
# AIC AQA Act1-2 'turning her out'
# ============================================================
print("\n=== AIC AQA Act1-2 turning her out ===")
lid = '7830cb9d-e4f3-4c2c-85b1-a2daaed07fb4'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('turning her out')
if idx >= 0:
    seg = html[max(0,idx-200):idx+100]
    print(f"  Context bytes: {repr(seg.encode('utf-8')[:200])}")
    # Find the exact pattern to replace
    # 'gave her money and "left her — turning her out."'
    old1 = f'gave her money and {LDQUO}left her {MDASH} turning her out.{RDQUO}'
    new1 = f'gave her money and ended the affair so he could focus on his business commitments'
    if old1 in html:
        new_html = html.replace(old1, new1)
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature-aqa/an-inspector-calls/act-1-2',
                   "Removed fabricated quote 'left her — turning her out' (not in play text)")
        print(f"  Fixed")
    else:
        # Try simpler approach - find the whole problematic sentence
        m = re.search(r'gave her money and .{1,5}left her .{1,5} turning her out.{1,5}', html)
        if m:
            old_str = m.group(0)
            print(f"  Regex match: {repr(old_str.encode('utf-8'))}")
            new_html = html.replace(old_str, 'gave her money and ended the affair when he had to go away on business')
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature-aqa/an-inspector-calls/act-1-2',
                       "Removed fabricated quote 'left her — turning her out'")
            print(f"  Fixed via regex")
        else:
            print(f"  WARN: Could not match")
else:
    print(f"  Already fixed or not present")

# ============================================================
# AIC Edexcel Act2 'adoring'
# ============================================================
print("\n=== AIC Edexcel Act2 adoring ===")
lid = 'd9f1b3a4-c2df-4196-b799-6a636594df49'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('adoring')
if idx >= 0:
    seg = html[max(0,idx-200):idx+100]
    # Find the fabricated quote pattern
    m = re.search(r'.{0,5}gave me a look that was nothing less than adoring.{0,5}', html)
    if m:
        old_str = m.group(0)
        print(f"  Match: {repr(old_str.encode('utf-8'))}")
        # Replace 'Eva "was very grateful" and "gave me a look that was nothing less than adoring."'
        # with 'Eva "was very grateful" and Gerald admits "I became at once the most important person in her life."'
        old_full = f'Eva {LDQUO}was very grateful{RDQUO} and {LDQUO}gave me a look that was nothing less than adoring.{RDQUO}'
        new_full = f'Eva {LDQUO}was very grateful{RDQUO} and {LDQUO}intensely grateful{RDQUO}: Gerald admits {LDQUO}I became at once the most important person in her life.{RDQUO}'
        if old_full in html:
            new_html = html.replace(old_full, new_full)
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature-edexcel/an-inspector-calls/act-2',
                       "Replaced fabricated 'adoring look' quote with Gerald's actual Act 2 lines")
            print(f"  Fixed")
        else:
            # Try broader replacement
            new_html = html.replace(
                f'{LDQUO}gave me a look that was nothing less than adoring.{RDQUO}',
                f'{LDQUO}I became at once the most important person in her life.{RDQUO}'
            )
            if new_html != html:
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature-edexcel/an-inspector-calls/act-2',
                           "Replaced fabricated 'adoring look' quote with Gerald's actual Act 2 line")
                print(f"  Fixed")
            else:
                print(f"  WARN: Could not replace")
                print(repr(html[max(0,idx-300):idx+100].encode('utf-8')[:300]))
else:
    print(f"  'adoring' not found")

# ============================================================
# AIC Eduqas Act2 'confess in public his responsibility'
# ============================================================
print("\n=== AIC Eduqas Act2 confess in public ===")
lid = 'ee389a4b-1087-4385-a313-2adbffb0df3d'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('confess in public')
if idx >= 0:
    seg = html[max(0,idx-200):idx+100]
    print(f"  Context: {repr(seg.encode('utf-8')[:200])}")
    # Replace the fabricated quote
    old_str = f'{LDQUO}confess in public his responsibility.{RDQUO}'
    new_str = f'{LDQUO}dealt with very severely.{RDQUO}'
    if old_str in html:
        new_html = html.replace(f'forced to {old_str}', f'{LDQUO}dealt with very severely.{RDQUO}')
        if new_html == html:
            new_html = html.replace(old_str, new_str)
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature-eduqas/an-inspector-calls/act-2',
                   "Replaced fabricated 'confess in public his responsibility' with Mrs Birling's actual phrase")
        print(f"  Fixed")
    else:
        # Regex approach
        m = re.search(r'.{0,5}confess in public his responsibility.{0,5}', html)
        if m:
            new_html = html.replace(m.group(0), f'{LDQUO}dealt with very severely.{RDQUO}')
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature-eduqas/an-inspector-calls/act-2',
                       "Replaced fabricated 'confess in public his responsibility' with actual Mrs Birling quote")
            print(f"  Fixed via regex")
else:
    print(f"  'confess in public' not found")

# ============================================================
# Animal Farm Chs7-8 - verify anthem fix
# ============================================================
print("\n=== Verify Animal Farm anthem ===")
lid = '6e95a98a-bee9-44c4-8e4d-309adc1296e7'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
if 'praising Animal Farm' in html:
    print(f"  GOOD: anthem fix present")
elif 'anthem' in html:
    idx = html.find('anthem')
    print(f"  Context: {repr(html[max(0,idx-100):idx+200])}")

# ============================================================
# Animal Farm Napoleon - verify poem/commandments fix
# ============================================================
print("\n=== Verify Animal Farm Napoleon ===")
lid = 'b3e6ed27-9f98-46e3-9f09-3d431f3572ea'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
if 'opposite end of the barn' in html:
    print(f"  GOOD: commandments fix present")
elif 'Seven Commandments' in html:
    idx = html.find('Seven Commandments')
    print(f"  Context: {repr(html[max(0,idx-100):idx+200])}")
else:
    # Need to fix - check what's there
    print(f"  No Seven Commandments found - checking replacing text...")
    idx = html.find('replacing')
    if idx >= 0:
        print(f"  'replacing' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    # The lesson may have used 'replacing' without the commandments text
    # Check barn wall content
    idx2 = html.find('barn wall')
    if idx2 >= 0:
        print(f"  'barn wall' at {idx2}: {repr(html[max(0,idx2-100):idx2+300])}")

# ============================================================
# Anita and Me - Character Analysis 'father has left' - find actual text
# ============================================================
print("\n=== Anita and Me Char Analysis - find father ===")
lid = '66acc567-1445-4dad-83bf-703bad1ee8e9'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('father')
while idx >= 0:
    print(f"  'father' at {idx}: {repr(html[max(0,idx-50):idx+100])}")
    idx = html.find('father', idx+1)

# ============================================================
# Anita and Me Part 2 'father has left' - find actual text
# ============================================================
print("\n=== Anita and Me Part 2 - find father ===")
lid = 'd4682e10-5eac-4a36-addc-ae1712a5d0cd'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('father')
count = 0
while idx >= 0 and count < 5:
    print(f"  'father' at {idx}: {repr(html[max(0,idx-50):idx+100])}")
    idx = html.find('father', idx+1)
    count += 1

# ============================================================
# Anita and Me Narrative Voice - opening line fix
# ============================================================
print("\n=== Anita and Me Narrative Voice - opening line ===")
lid = '9f0e34ed-17d2-4473-92af-313aaf5ab61e'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('Tollington')
count = 0
while idx >= 0 and count < 5:
    print(f"  at {idx}: {repr(html[max(0,idx-100):idx+150])}")
    idx = html.find('Tollington', idx+1)
    count += 1

save_log(log_data)
print(f"\nAdded {len(fixes_added)} more fixes to log")
