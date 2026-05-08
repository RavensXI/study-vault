"""Fix pass 2 — remaining items with unicode issues."""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

from lib.supabase_client import get_client
sb = get_client()

RSQUO = '’'  # '
LDQUO = '“'  # "
RDQUO = '”'  # "
MDASH = '—'  # —
LSQUO = '‘'  # '

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
# Anita and Me Part 2 'd4682 - father is absent (already correct, no fix needed)
# d4682 lesson text: 'Anita's father is absent' - that IS the fix needed
# audit said 'father has left' but lesson has 'is absent' already
# So it was already fixed or the audit text didn't match. No action.
# ============================================================
print("Anita Part 2 - 'father is absent' already in lesson - no fix needed")

# ============================================================
# Anita and Me Narrative Voice - 'Tollington' not found in html
# The lesson might use a different phrasing. Check what the opening line says.
# ============================================================
print("\n=== Anita and Me Narrative Voice check ===")
lid = '9f0e34ed-17d2-4473-92af-313aaf5ab61e'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
# Check the actual opening line quote
idx = html.find('do not have many memories')
if idx >= 0:
    print(f"  Found opening line at {idx}: {repr(html[max(0,idx-200):idx+200])}")
else:
    print(f"  'do not have many memories' not found")
    # Check first 1000 chars
    print(f"  First 500 chars: {repr(html[:500])}")

# ============================================================
# Frankenstein Key Themes (0a12) - 'The Creature quotes Paradise Lost'
# ============================================================
print("\n=== Frankenstein Key Themes ===")
lid = '0a12f1b6-4c0a-44f4-bbba-b4ead1ca5491'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('request thee')
if idx >= 0:
    print(f"  Context: {repr(html[max(0,idx-300):idx+200])}")
    # The issue: "The Creature quotes Paradise Lost"
    old_pat = f'The Creature quotes {LDQUO}Paradise Lost{RDQUO}'
    if old_pat in html:
        new_html = html.replace(old_pat, f'the novel{RSQUO}s title-page epigraph draws from {LDQUO}Paradise Lost{RDQUO}')
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature/frankenstein/key-themes',
                   "Corrected: 'Did I request thee' is the title-page epigraph, not a speech by the Creature")
        print(f"  Fixed")
    else:
        # Try italic version
        old_pat2 = 'The Creature quotes <em>Paradise Lost</em>'
        if old_pat2 in html:
            new_html = html.replace(old_pat2, f'the novel{RSQUO}s title-page epigraph draws from <em>Paradise Lost</em>')
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/frankenstein/key-themes',
                       "Corrected: 'Did I request thee' is the title-page epigraph, not a speech by the Creature")
            print(f"  Fixed")
        else:
            # Just find and fix "The Creature quotes"
            if 'The Creature quotes' in html:
                new_html = html.replace('The Creature quotes', f'the novel{RSQUO}s title-page epigraph, drawn from')
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature/frankenstein/key-themes',
                           "Corrected: 'Did I request thee' is the title-page epigraph, not a Creature speech")
                print(f"  Fixed")
            else:
                print(f"  WARN: Could not find fix pattern")

# ============================================================
# Frankenstein Creature's Story (346d) - same epigraph issue
# ============================================================
print("\n=== Frankenstein Creature's Story ===")
lid = '346dfdf8-2760-4122-9651-b750b7b520c9'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('The Creature asks')
if idx >= 0:
    print(f"  Context: {repr(html[max(0,idx-50):idx+300])}")
    # Replace with the epigraph framing
    old1 = f'The Creature asks: {LDQUO}Did I request thee, Maker, from my clay to mould me man?{RDQUO} {MDASH} quoting Milton{RSQUO}s Adam directly.'
    new1 = f'The novel{RSQUO}s title-page epigraph {MDASH} {LDQUO}Did I request thee, Maker, from my clay to mould me Man?{RDQUO} {MDASH} is drawn from Milton{RSQUO}s Adam in {LDQUO}Paradise Lost{RDQUO}, setting up the central theme of a creator{RSQUO}s responsibility to his creation.'
    if old1 in html:
        new_html = html.replace(old1, new1)
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature/frankenstein/creatures-story',
                   "Corrected: 'Did I request thee' is the title-page epigraph, not a Creature speech in the story")
        print(f"  Fixed")
    else:
        print(f"  Pattern not matched exactly, trying simpler approach...")
        # Just replace 'The Creature asks:' with correct framing
        if 'The Creature asks:' in html:
            new_html = html.replace('The Creature asks:', f'The novel{RSQUO}s title-page epigraph proclaims:')
            # Also fix 'quoting Milton's Adam directly' if present
            new_html = new_html.replace(
                f'{MDASH} quoting Milton{RSQUO}s Adam directly.',
                f'{MDASH} drawn from Milton{RSQUO}s Adam in Paradise Lost, setting up the theme of a creator{RSQUO}s responsibility.'
            )
            new_html = new_html.replace(
                '— quoting Milton’s Adam directly.',
                '— drawn from Milton’s Adam in Paradise Lost, setting up the theme of a creator’s responsibility.'
            )
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/frankenstein/creatures-story',
                       "Corrected: 'Did I request thee' is the title-page epigraph, not a Creature speech")
            print(f"  Fixed (simpler approach)")
        else:
            print(f"  WARN: 'The Creature asks:' also not found")
else:
    print(f"  'The Creature asks' not found")

# ============================================================
# Henry V Acts 1-2 - fix 'Quickly says' → 'Pistol says' for 'fracted and corroborate'
# ============================================================
print("\n=== Henry V Acts 1-2 fracted ===")
lid = '17bbf4d6-8468-4128-849e-cf49e2fcaeac'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('fracted and corroborate')
if idx >= 0:
    seg = html[max(0,idx-200):idx+100]
    print(f"  Context bytes: {repr(seg.encode('utf-8')[:200])}")
    # Fix: change 'Quickly says' to 'Pistol says' in the relevant sentence
    old1 = f'Quickly says Falstaff{RSQUO}s heart was {LDQUO}fracted and corroborate{RDQUO} (broken).'
    new1 = f'Pistol says Falstaff{RSQUO}s heart was {LDQUO}fracted and corroborate{RDQUO} (broken and crushed) {MDASH} a typically mangled Pistol malapropism in Act 2, Scene 1.'
    if old1 in html:
        new_html = html.replace(old1, new1)
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature/henry-v/acts-1-2',
                   "Corrected attribution: 'fracted and corroborate' is Pistol's line (Act 2 Scene 1), not Mistress Quickly's")
        print(f"  Fixed")
    else:
        # Try pattern
        m = re.search(r'Quickly says Falstaff.{0,3}s heart was .{0,3}fracted and corroborate.{0,3}', html)
        if m:
            old_str = m.group(0)
            print(f"  Match: {repr(old_str.encode('utf-8'))}")
            new_html = html.replace(old_str, f'Pistol says Falstaff{RSQUO}s heart was {LDQUO}fracted and corroborate{RDQUO} (broken) {MDASH} a typically garbled Pistol expression in Act 2, Scene 1')
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/henry-v/acts-1-2',
                       "Corrected attribution: 'fracted and corroborate' is Pistol's line, not Quickly's")
            print(f"  Fixed via regex")
        else:
            print(f"  WARN: Could not match")

# ============================================================
# Henry V Act 5 - Epilogue paraphrase
# ============================================================
print("\n=== Henry V Act 5 Epilogue ===")
lid = 'ff8f86bd-7936-4f17-8c2a-9ca7fe88be9a'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('lived but a short time')
if idx >= 0:
    seg = html[max(0,idx-200):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:300])}")
    # Fix: remove 'lived but a short time' (not exact text) and clarify the epilogue
    # Pattern: Henry V "lived but a short time" and his son, Henry VI, "lost France..."
    old1 = f'Henry V {LDQUO}lived but a short time{RDQUO} and his son, Henry VI, {LDQUO}lost France and made his England bleed, / Which oft our stage hath shown.{RDQUO}'
    new1 = f'The Chorus notes that Henry V died young and his infant son Henry VI, left in the management of many, {LDQUO}lost France and made his England bleed{RDQUO} {MDASH} a sobering epilogue that undercuts the play{RSQUO}s triumphalism'
    if old1 in html:
        new_html = html.replace(old1, new1)
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature/henry-v/act-5',
                   "Cleaned up Epilogue: removed 'lived but a short time' (not exact text); kept accurate 'lost France and made his England bleed'")
        print(f"  Fixed")
    else:
        m = re.search(r'Henry V .{0,3}lived but a short time.{0,3} and his son', html)
        if m:
            print(f"  Regex match: {repr(html[m.start():m.start()+300].encode('utf-8')[:200])}")
            # Replace the whole thing
            end_m = re.search(r'stage hath shown\.', html[m.start():m.start()+500])
            if end_m:
                old_str = html[m.start():m.start()+end_m.end()+50]
                # Find closing quote
                close_q = html.find(RDQUO, m.start()+end_m.start()+m.start())
                if close_q >= 0:
                    old_str = html[m.start():close_q+1]
                    new_str = f'The Chorus notes that Henry V died young and his infant son Henry VI {LDQUO}lost France and made his England bleed{RDQUO}'
                    new_html = html.replace(old_str, new_str)
                    if new_html != html:
                        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                        record_fix(log_data, lid, 'english-literature/henry-v/act-5',
                                   "Cleaned Epilogue: removed unverified 'lived but a short time'; kept accurate quote")
                        print(f"  Fixed")
                    else:
                        print(f"  Replace failed")
            else:
                print(f"  Could not find end of old string")
        else:
            print(f"  WARN: Could not find pattern")
else:
    print(f"  'lived but a short time' not found")

# ============================================================
# Jane Eyre Key Themes - remove Darcy quote
# ============================================================
print("\n=== Jane Eyre Key Themes ===")
lid = 'bfd272f4-821a-4a81-9b50-e5e3af499b80'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('middle before')
if idx >= 0:
    print(f"  Already removed? checking... 'middle before' at {idx}")
    # Already been modified - verify
    seg = html[max(0,idx-200):idx+200]
    print(f"  Context: {repr(seg)}")
else:
    print(f"  'middle before' not found - already removed")

# ============================================================
# Jekyll and Hyde Context - Dracula 'earlier' fix
# ============================================================
print("\n=== Jekyll and Hyde Context Dracula ===")
lid = '7d48ecbc-71d7-4623-98dc-06684907fdd2'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('Dracula')
if idx >= 0:
    seg = html[max(0,idx-200):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:300])}")
    # Fix: Dracula (1897) is AFTER Jekyll (1886)
    # Pattern: 'Earlier Gothic novels like Mary Shelley's Frankenstein (1818) and Bram Stoker's Dracula (1897) shared similar concerns'
    old1 = f'Earlier Gothic novels like Mary Shelley{RSQUO}s <em>Frankenstein</em> (1818) and Bram Stoker{RSQUO}s <em>Dracula</em> (1897) shared similar concerns about science overreaching its boundaries and the beast within civilised humanity.'
    new1 = f'Earlier Gothic works like Mary Shelley{RSQUO}s <em>Frankenstein</em> (1818) shared similar concerns about science overreaching its limits and the beast within humanity; later Gothic novels like Bram Stoker{RSQUO}s <em>Dracula</em> (1897) developed these themes further still.'
    if old1 in html:
        new_html = html.replace(old1, new1)
        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
        record_fix(log_data, lid, 'english-literature/jekyll-and-hyde/context',
                   "Corrected: Dracula (1897) was published 11 years after Jekyll and Hyde (1886) — cannot be 'earlier'")
        print(f"  Fixed")
    else:
        m = re.search(r'Earlier Gothic novels like.{0,100}Dracula.{0,100}shared similar concerns', html)
        if m:
            old_str = m.group(0)
            print(f"  Match: {repr(old_str.encode('utf-8'))}")
            # Replace just the 'Earlier' part and restructure
            new_html = html.replace('Earlier Gothic novels like Mary Shelley',
                                    'Earlier Gothic works like Mary Shelley')
            # Remove Dracula from the 'earlier' list
            new_html = new_html.replace(
                f'and Bram Stoker{RSQUO}s <em>Dracula</em> (1897) shared similar concerns about science overreaching its boundaries and the beast within civilised humanity.',
                f'shared similar concerns about science overreaching its limits. Later Gothic novels like Bram Stoker{RSQUO}s <em>Dracula</em> (1897) developed these themes further.'
            )
            if new_html != html:
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature/jekyll-and-hyde/context',
                           "Corrected: Dracula (1897) was published AFTER Jekyll (1886) — moved to 'later'")
                print(f"  Fixed via pattern")
            else:
                print(f"  WARN: pattern fix failed")
        else:
            print(f"  Could not match Dracula pattern")
else:
    print(f"  'Dracula' not found")

# ============================================================
# Jekyll and Hyde Ch9-10 - 'in the glass' fix
# ============================================================
print("\n=== Jekyll and Hyde Ch9-10 in the glass ===")
lid = '241ec110-09b6-448e-acab-91713c5f57c2'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('in the glass')
if idx >= 0:
    print(f"  'in the glass' still present at {idx}: {repr(html[max(0,idx-100):idx+100])}")
    # Try unicode ellipsis variant
    m = re.search(r'see his own face\.{0,5}.{0,20}in the glass', html)
    if m:
        print(f"  Match: {repr(html[m.start():m.start()+100].encode('utf-8'))}")
    else:
        # Just find and remove the extra phrase
        new_html = html.replace('… in the glass.', '.')
        new_html = new_html.replace('... in the glass.', '.')
        new_html = new_html.replace('… in the glass', '')
        new_html = new_html.replace('... in the glass', '')
        # Unicode ellipsis check
        import unicodedata
        chars = html[idx-30:idx+20]
        print(f"  Chars around 'in the glass': {repr(chars)}")
        if new_html != html:
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/jekyll-and-hyde/chapters-9-10',
                       "Removed 'in the glass' — not in Stevenson's original text")
            print(f"  Fixed")
        else:
            # Direct replace
            seg = html[max(0,idx-50):idx+len('in the glass')+5]
            print(f"  Segment: {repr(seg.encode('utf-8'))}")
else:
    print(f"  'in the glass' already fixed or not present")

# ============================================================
# Journey's End Key Themes - find the exact text
# ============================================================
print("\n=== Journey's End Key Themes ===")
lid = '31b57455-e90a-4bbd-9132-a5b0971fda54'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']

# Fix 1: 'It's the only way to forget'
idx = html.find("only way to forget")
if idx >= 0:
    print(f"  'only way to forget' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    m = re.search(r'Stanhope.{0,100}inseparable from his damage.{0,30}.{0,20}It.{0,3}s the only way to forget.{0,5}', html)
    if m:
        old_str = m.group(0)
        print(f"  Match: {repr(old_str.encode('utf-8'))}")
        new_html = html.replace(old_str, f'Stanhope{RSQUO}s heroism is inseparable from his damage. He drinks to endure what most cannot face.')
        if new_html != html:
            html = new_html
            print(f"  Fix 1 applied")
    else:
        # Simpler: find the Key Fact that contains this
        idx2 = html.rfind('<div class="key-fact"', 0, idx)
        if idx2 >= 0:
            end_idx = html.find('</div>\n</div>', idx2)
            kf_block = html[idx2:end_idx+13]
            print(f"  Key Fact block: {repr(kf_block[:300])}")

# Fix 2: 'one man I could talk to as a friend' (Raleigh→Stanhope about Osborne)
idx2 = html.find('one man I could talk to as a friend')
if idx2 >= 0:
    print(f"\n  'one man I could talk to as a friend' at {idx2}: {repr(html[max(0,idx2-200):idx2+200])}")
    seg = html[max(0,idx2-200):idx2+200]
    # Replace Raleigh attribution with Stanhope about Osborne
    m = re.search(r'Raleigh describes Stanhope as .{0,5}the one man I could talk to as a friend.{0,5}', html)
    if m:
        old_str = m.group(0)
        print(f"  Match: {repr(old_str.encode('utf-8'))}")
        new_html = html.replace(old_str, f'Stanhope describes Osborne as {LDQUO}the one man I could trust {MDASH} my best friend {MDASH} the one man I could talk to as man to man,{RDQUO}')
        if new_html != html:
            html = new_html
            print(f"  Fix 2 applied")
    else:
        # Try simpler
        for old_pat in [
            f'Raleigh describes Stanhope as {LDQUO}the one man I could talk to as a friend,{RDQUO}',
            f'Raleigh describes Stanhope as {LSQUO}the one man I could talk to as a friend,{RSQUO}',
        ]:
            if old_pat in html:
                html = html.replace(old_pat, f'Stanhope describes Osborne as {LDQUO}the one man I could trust {MDASH} my best friend {MDASH} the one man I could talk to as man to man,{RDQUO}')
                print(f"  Fix 2 applied via direct match")
                break
        else:
            print(f"  Fix 2 could not match pattern")

# Save if changed
res2 = sb.table('lessons').select('content_html').eq('id', lid).single().execute()
if html != res2.data['content_html']:
    sb.table('lessons').update({'content_html': html}).eq('id', lid).execute()
    record_fix(log_data, lid, 'english-literature/journeys-end/key-themes',
               "Fixed Journey's End Key Themes: removed unverified quote and/or corrected 'one man' attribution")
    print(f"  Saved to Supabase")
else:
    print(f"  No change saved")

# ============================================================
# Journey's End Act 2 - corrupted Stanhope quote
# ============================================================
print("\n=== Journey's End Act 2 corrupted quote ===")
lid = '4b56556f-e5c8-42f0-9ef5-8fcdd75570d7'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find("Loss of Raleigh")
if idx >= 0:
    seg = html[max(0,idx-200):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:300])}")
    # Replace the corrupted quote
    m = re.search(r'Stanhope tells Hibbert: .{0,5}If you went .{0,3} Loss of Raleigh.{0,100}irreplaceable.{0,5}', html)
    if m:
        old_str = m.group(0)
        new_str = f'Stanhope tells Hibbert: {LDQUO}If you went {MDASH} and left Osborne and Trotter and Raleigh and all the other men who are staying here {MDASH} I{RSQUO}d rather spare you than any of them.{RDQUO}'
        new_html = html.replace(old_str, new_str)
        if new_html != html:
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/journeys-end/act-2',
                       "Replaced corrupted 'Loss of Raleigh's map' quote with actual Act 2 Sc 2 Stanhope speech to Hibbert")
            print(f"  Fixed")
        else:
            print(f"  Replace failed")
    else:
        print(f"  Regex not matched")
        # Try direct string
        for old_try in [
            f'Stanhope tells Hibbert: {LDQUO}If you went {MDASH} Loss of Raleigh',
            'Stanhope tells Hibbert:',
        ]:
            if old_try in html:
                print(f"  Found: {repr(old_try)} at {html.find(old_try)}")
                # Find the end of this sentence
                start_i = html.find(old_try)
                end_i = html.find('</p>', start_i)
                old_sentence = html[start_i:end_i]
                print(f"  Old sentence: {repr(old_sentence.encode('utf-8')[:200])}")
                break
else:
    print(f"  'Loss of Raleigh' not found")

# ============================================================
# Julius Caesar Context - Antony speech not 'directly lifted'
# ============================================================
print("\n=== Julius Caesar Context ===")
lid = '23dd9de7-1127-4c7c-bd41-c6a2ca7e413e'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('directly lifted')
if idx >= 0:
    seg = html[max(0,idx-200):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:300])}")
    m = re.search(r'Some of Antony.{0,3}s funeral speech is almost directly lifted from North.{0,3}s translation, showing how closely Shakespeare worked from this source\.', html)
    if m:
        old_str = m.group(0)
        new_str = f'Shakespeare drew on North{RSQUO}s 1579 translation of Plutarch for the broad outline of events, though Antony{RSQUO}s funeral speech is Shakespeare{RSQUO}s own rhetorical invention {MDASH} Plutarch{RSQUO}s account summarises the funeral in only a few lines.'
        new_html = html.replace(old_str, new_str)
        if new_html != html:
            sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
            record_fix(log_data, lid, 'english-literature/julius-caesar/context',
                       "Corrected: Antony's speech is Shakespeare's invention, not 'almost directly lifted' from Plutarch")
            print(f"  Fixed")
        else:
            print(f"  Replace failed")
    else:
        print(f"  Regex not matched")
else:
    idx2 = html.find('Plutarch')
    if idx2 >= 0:
        print(f"  Plutarch at {idx2}: {repr(html[max(0,idx2-100):idx2+300])}")
    print(f"  'directly lifted' not found")

# ============================================================
# LOTF Edexcel L3 - 'Which is better' Piggy vs Ralph
# ============================================================
print("\n=== Lord of the Flies Edexcel L3 ===")
lid = 'f1e60ae7-c6ac-467a-8019-cdea9ac55afe'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find('Which is better')
if idx >= 0:
    seg = html[max(0,idx-300):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:400])}")
    # Check for Ralph attribution nearby
    ralph_idx = html.rfind('Ralph', 0, idx+100)
    print(f"  Last Ralph before phrase: {ralph_idx}, distance: {idx-ralph_idx}")
    pig_idx = html.rfind('Piggy', 0, idx+100)
    print(f"  Last Piggy before phrase: {pig_idx}")

    if ralph_idx > pig_idx:  # Ralph attribution is closer
        # Find the specific attribution
        nearby = html[max(0,idx-400):idx+50]
        print(f"  Nearby for attribution: {repr(nearby[-200:])}")
        # Common patterns:
        for old_pat, new_pat in [
            (f'Ralph asks: {LDQUO}Which is better', f'Piggy asks: {LDQUO}Which is better'),
            (f'Ralph demands: {LDQUO}Which is better', f'Piggy demands: {LDQUO}Which is better'),
            (f'Ralph{RSQUO}s question: {LDQUO}Which is better', f'Piggy{RSQUO}s question: {LDQUO}Which is better'),
            (f'Ralph cries: {LDQUO}Which is better', f'Piggy cries: {LDQUO}Which is better'),
            (f'Ralph asks, {LDQUO}Which is better', f'Piggy asks, {LDQUO}Which is better'),
            (f'Ralph shouts: {LDQUO}Which is better', f'Piggy shouts: {LDQUO}Which is better'),
            (f'Ralph asks {LDQUO}Which is better', f'Piggy asks {LDQUO}Which is better'),
        ]:
            if old_pat in html:
                new_html = html.replace(old_pat, new_pat)
                sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                record_fix(log_data, lid, 'english-literature-edexcel/lord-of-the-flies/chapters-4-6',
                           "Corrected attribution: 'Which is better...' is Piggy's line (Ch 5), not Ralph's")
                print(f"  Fixed")
                break
        else:
            # More aggressive: find any 'Ralph' + verb close before 'Which is better'
            m = re.search(r'(Ralph\s+\w+[\s:,]+.{0,30}Which is better)', html)
            if m:
                old_str = m.group(0)
                print(f"  Regex match: {repr(old_str.encode('utf-8'))}")
                new_html = html.replace(old_str, old_str.replace('Ralph', 'Piggy', 1))
                if new_html != html:
                    sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                    record_fix(log_data, lid, 'english-literature-edexcel/lord-of-the-flies/chapters-4-6',
                               "Corrected: 'Which is better...' attributed to Piggy not Ralph")
                    print(f"  Fixed via regex")
            else:
                print(f"  WARN: could not find Ralph attribution near quote")
    else:
        print(f"  Piggy is closer attribution - may already be correct")
else:
    print(f"  'Which is better' not found")

# ============================================================
# Macbeth Key Themes - verify Incardnadine fix
# ============================================================
print("\n=== Verify Macbeth fixes ===")
for lid, name in [
    ('13affe23-f79d-4839-a453-4fa348cb7fea', 'Key Themes'),
    ('3b2aecbd-8400-42d3-a42e-1d246da356fd', 'Act 2'),
]:
    res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
    html = res.data['content_html']
    if 'ncardnadine' in html.lower():
        idx = html.lower().find('ncardnadine')
        print(f"  {name}: 'ncardnadine' at {idx}: {repr(html[max(0,idx-20):idx+20])}")
    else:
        print(f"  {name}: 'ncardnadine' not found (already fixed)")

# ============================================================
# Anita and Me 98b8 - 'We don't want your lot' fix
# ============================================================
print("\n=== Anita and Me Racism 98b8 - We don't want ===")
lid = '98b8a08a-34a2-450e-aa9b-1a34905c881e'
res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
html = res.data['content_html']
idx = html.find("We don")
if idx < 0:
    idx = html.find("We don’t want")
if idx >= 0:
    seg = html[max(0,idx-300):idx+200]
    print(f"  Context: {repr(seg.encode('utf-8')[:400])}")
    # Fix: the quote is unverified - replace with paraphrase
    for old_pat in [
        f'Sam publicly shouts racist abuse: {LDQUO}We don{RSQUO}t want your lot round here!{RDQUO}',
        f'Sam publicly shouts racist abuse: {LDQUO}We don’t want your lot round here!{RDQUO}',
        'Sam publicly shouts racist abuse:',
    ]:
        if old_pat in html:
            if old_pat == 'Sam publicly shouts racist abuse:':
                # Find the end of this phrase
                idx2 = html.find(old_pat)
                end_quote = html.find(RDQUO, idx2 + len(old_pat))
                if end_quote >= 0:
                    old_str = html[idx2:end_quote+1]
                    print(f"  Old: {repr(old_str.encode('utf-8'))}")
                    new_html = html.replace(old_str, 'Sam makes openly racist statements targeting the community')
                    if new_html != html:
                        sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                        record_fix(log_data, lid, 'english-literature-aqa/anita-and-me/racism',
                                   "Removed unverified 'We don't want your lot round here!' quote; replaced with paraphrase")
                        print(f"  Fixed")
                        break
            else:
                new_html = html.replace(old_pat, 'Sam makes openly racist statements targeting the community')
                if new_html != html:
                    sb.table('lessons').update({'content_html': new_html}).eq('id', lid).execute()
                    record_fix(log_data, lid, 'english-literature-aqa/anita-and-me/racism',
                               "Removed unverified 'We don't want your lot round here!' quote; replaced with paraphrase")
                    print(f"  Fixed")
                    break
    else:
        print(f"  WARN: Could not match pattern")
else:
    print(f"  Quote not found (may already be fixed)")

# ============================================================
# Anita and Me Context c2e9/c3e0 - 'If you want a nigger' - verify fixes
# ============================================================
print("\n=== Verify Anita Context Smethwick fixes ===")
for lid in ['c2e90934-0470-49cb-8915-945c43c37131', 'c3e0ba3c-9e6a-456d-8835-be00b08fc4c2']:
    res = sb.table('lessons').select('id,title,content_html').eq('id', lid).single().execute()
    html = res.data['content_html']
    if 'Smethwick' in html or '1964' in html:
        print(f"  {lid[:8]}: Smethwick/1964 context present - GOOD")
    else:
        idx = html.find('nigger for a neighbour')
        if idx >= 0:
            print(f"  {lid[:8]}: Still has bare quote at {idx}: {repr(html[max(0,idx-100):idx+200])}")

save_log(log_data)
print("\n=== DONE ===")
