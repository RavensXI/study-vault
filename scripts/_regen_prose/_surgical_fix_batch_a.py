"""
Surgical Fix Script — Batch A (texts A through M)
Applies single-quote / single-line fixes to lessons flagged in _prose_audit_fixlist.json.
"""
import sys, os, json, re, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

from lib.supabase_client import get_client

sb = get_client()
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_surgical_fix_log.json')


def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, encoding='utf-8') as f:
            return json.load(f)
    return []


def save_log(log_entries):
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, ensure_ascii=False, indent=2)


def fetch_lesson(lesson_id):
    res = sb.table('lessons').select(
        'id,title,content_html,flashcard_questions,knowledge_checks,glossary_terms'
    ).eq('id', lesson_id).single().execute()
    return res.data


def update_lesson(lesson_id, updates):
    sb.table('lessons').update(updates).eq('id', lesson_id).execute()


# Track modifications
fixes = []
lessons_modified = set()


def record_fix(lesson_id, lesson_slug, fix_summary):
    fixes.append({
        "lesson_id": lesson_id,
        "lesson_slug": lesson_slug,
        "fix_summary": fix_summary,
    })
    lessons_modified.add(lesson_id)
    print(f"  FIX: {lesson_id[:8]}... — {fix_summary[:80]}")


def save_partial(batch_label="A"):
    existing = load_log()
    batch_entry = {
        "batch": batch_label,
        "lessons_modified": list(lessons_modified),
        "fixes": fixes,
    }
    # Replace any prior batch A entry or append
    replaced = False
    for i, e in enumerate(existing):
        if e.get("batch") == batch_label:
            existing[i] = batch_entry
            replaced = True
            break
    if not replaced:
        existing.append(batch_entry)
    save_log(existing)
    print(f"  [Saved partial: {len(fixes)} fixes so far]")


# ============================================================
# A Christmas Carol — AQA L3 (Stave 2: Memory & Regret)
# ============================================================
print("\n=== A Christmas Carol AQA L3 ===")
lid = 'c6470abc-7bd7-4ec8-948d-c2115a7bae80'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = ('Fan died young giving birth to Fred, Scrooge’s nephew. '
       'This explains why Scrooge resents Fred — he blames him for Fan’s death, '
       'the loss of the only person who truly loved him.')
NEW = ('Fan died young, leaving Fred motherless. '
       'Dickens does not reveal the cause of her death, but her loss shapes Scrooge’s '
       'complicated feelings towards Fred — he pushes away the last living connection to the sister he loved.')

if OLD in html:
    new_html = html.replace(OLD, NEW, 1)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/a-christmas-carol/stave-2',
               "Removed unverified 'giving birth to Fred' cause-of-death claim; removed 'blames Fred' speculation")
else:
    print(f"  WARN: could not find Fan died text in {lid}")

# ============================================================
# A Christmas Carol — Eduqas L5 (Staves 4-5: Redemption)
# Section ordering: move Tiny Tim's Death + Gravestone before Stave 5
# ============================================================
print("\n=== A Christmas Carol Eduqas L5 ===")
lid = 'ff33a284-7c17-4543-a5dc-df0d5fee4006'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Locate the three blocks:
# Block A: "Stave 5: The Transformation" through end of Stave 5 text (ends before <!-- DIAGRAM -->)
# Block B: <!-- DIAGRAM --> + \n\n<h2...Tiny Tim's Death...> ... </div>
# Block C: <h2...The Gravestone...> ... </div></div>\n</div>

# Strategy: find exact string boundaries
STAVE5_HEADER = '<h2 data-narration-id="n8">Stave 5: The Transformation</h2>'
DIAGRAM_MARKER = '\n\n<!-- DIAGRAM -->\n\n'
TINY_TIM_HEADER = '<h2 data-narration-id="n12">Tiny Tim’s Death</h2>'
GRAVESTONE_HEADER = '<h2 data-narration-id="n15">The Gravestone</h2>'

stave5_pos = html.find(STAVE5_HEADER)
diagram_pos = html.find(DIAGRAM_MARKER)
tiny_pos = html.find(TINY_TIM_HEADER)
grave_pos = html.find(GRAVESTONE_HEADER)

if all(x >= 0 for x in [stave5_pos, diagram_pos, tiny_pos, grave_pos]):
    # The order is: [pre-stave5][stave5 block][diagram][tiny_tim block][gravestone block]
    # We want:      [pre-stave5][tiny_tim block][gravestone block][stave5 block][diagram]

    pre_stave5 = html[:stave5_pos]
    stave5_block = html[stave5_pos:diagram_pos]  # Stave 5 para up to diagram
    diagram_and_tiny = html[diagram_pos:grave_pos]  # DIAGRAM + Tiny Tim section
    grave_to_end = html[grave_pos:]  # Gravestone to end

    # Tiny Tim section (without the DIAGRAM part)
    tiny_block = html[tiny_pos:grave_pos]
    stave5_with_diagram = html[stave5_pos:tiny_pos]  # stave5 + diagram

    # Reorder: pre-stave5 + tiny_tim + gravestone + stave5_with_diagram
    new_html = pre_stave5 + tiny_block + grave_to_end
    # Wait — we also need to keep Stave 5 somewhere. Let me re-think.
    # Actually we want: pre_stave5 + tiny_block + grave_to_end replaces html
    # But grave_to_end includes the collapsible after The Gravestone, and stave5 block is missing
    # Let me re-do this properly

    # Correct segments:
    # seg1: html[:stave5_pos]  — everything before Stave 5
    # seg2: stave5_block = html[stave5_pos:tiny_pos]  — Stave 5 block + DIAGRAM
    # seg3: tiny_block = html[tiny_pos:grave_pos]  — Tiny Tim section
    # seg4: grave_to_end = html[grave_pos:]  — Gravestone to end

    seg1 = html[:stave5_pos]
    seg2 = html[stave5_pos:tiny_pos]
    seg3 = html[tiny_pos:grave_pos]
    seg4 = html[grave_pos:]

    # New order: seg1 + seg3 + seg4 + seg2
    new_html = seg1 + seg3 + seg4 + seg2

    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/a-christmas-carol/staves-4-5',
               "Moved 'Tiny Tim's Death' and 'The Gravestone' sections before 'Stave 5' block (both are Stave 4 events)")
else:
    print(f"  WARN: Could not find all section markers in {lid}")
    print(f"  stave5={stave5_pos} diagram={diagram_pos} tiny={tiny_pos} grave={grave_pos}")

save_partial()

# ============================================================
# A Taste of Honey — Eduqas Staging (18→19)
# ============================================================
print("\n=== A Taste of Honey Eduqas Staging ===")
lid = '15bbe5cf-9daa-4ddf-97e5-4e2972e797ba'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = 'the work of an 18-year-old'
NEW = 'the work of a 19-year-old'

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/a-taste-of-honey/staging',
               "Corrected Delaney's age at premiere from 18 to 19")
else:
    print(f"  WARN: '{OLD}' not found in {lid}")

# ============================================================
# A Taste of Honey — Eduqas Act 1 Scene 2 (Boy from Cardiff)
# ============================================================
print("\n=== A Taste of Honey Eduqas Act1S2 ===")
lid = '1d53449e-4a1b-4ab8-8f9a-f038989fb5b6'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD1 = 'a young Black sailor from Cardiff'
NEW1 = 'a young Black sailor'

if OLD1 in html:
    new_html = html.replace(OLD1, NEW1)
    # Also check if there's a note about Cardiff we can add context to
    # Find the surrounding sentence
    idx = new_html.find(NEW1)
    context = new_html[max(0,idx-200):idx+300]
    print(f"  Context around fix: {repr(context[:200])}")
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/a-taste-of-honey/act-1-scene-2',
               "Removed 'from Cardiff' — Cardiff is his joke about ancestors' origins, not his own home")
else:
    print(f"  WARN: '{OLD1}' not found in {lid}")
    # Try variant
    idx = html.find('Cardiff')
    if idx >= 0:
        print(f"  Cardiff found at {idx}: {repr(html[max(0,idx-100):idx+100])}")

# ============================================================
# A Taste of Honey — AQA Context (18→19 + 'a year'→'months')
# ============================================================
print("\n=== A Taste of Honey AQA Context ===")
lid = '41d91d53-8723-4786-8d50-915349de5fde'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False
# Fix 1: 18 → 19
OLD_AGE = 'she was just 18 years old'
NEW_AGE = 'she was just 19 years old'
if OLD_AGE in html:
    html = html.replace(OLD_AGE, NEW_AGE)
    changed = True
    print(f"  Applied age fix (18→19)")

# Fix 2: 'just a year before' → 'just months before'
OLD_YEAR = 'just a year before the play transferred to the West End'
NEW_YEAR = 'just months before the play transferred to the West End'
if OLD_YEAR in html:
    html = html.replace(OLD_YEAR, NEW_YEAR)
    changed = True
    print(f"  Applied Notting Hill timing fix (year→months)")

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature-aqa/a-taste-of-honey/context',
               "Fixed Delaney age (18→19) and Notting Hill riots timing ('a year'→'months')")
else:
    print(f"  WARN: could not find fixes in {lid}")
    # Check what's there
    idx = html.find('18 years')
    if idx >= 0:
        print(f"  '18 years' at {idx}: {repr(html[max(0,idx-50):idx+100])}")
    idx2 = html.find('Notting Hill')
    if idx2 >= 0:
        print(f"  Notting Hill at {idx2}: {repr(html[max(0,idx2-50):idx2+150])}")

# ============================================================
# A Taste of Honey — AQA Act1S2 (Boy from Cardiff)
# ============================================================
print("\n=== A Taste of Honey AQA Act1S2 ===")
lid = '5b3111df-ed41-4d66-b6e1-938d472aff75'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD1 = 'a young Black sailor from Cardiff'
NEW1 = 'a young Black sailor'

if OLD1 in html:
    new_html = html.replace(OLD1, NEW1)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/a-taste-of-honey/act-1-scene-2',
               "Removed 'from Cardiff' — Cardiff is the joke about his ancestors' origins, not his hometown")
else:
    print(f"  WARN: '{OLD1}' not found in {lid}")
    idx = html.find('Cardiff')
    if idx >= 0:
        print(f"  Cardiff at {idx}: {repr(html[max(0,idx-100):idx+100])}")

# ============================================================
# A Taste of Honey — AQA Act 2 (pansified little freak)
# ============================================================
print("\n=== A Taste of Honey AQA Act2 ===")
lid = 'a7a18a44-94ab-4454-9dce-89decf924e66'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD_FREAK = "calling him a 'little freak'"
NEW_FREAK = "calling him a 'pansified little freak'"

if OLD_FREAK in html:
    new_html = html.replace(OLD_FREAK, NEW_FREAK)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/a-taste-of-honey/act-2',
               "Restored 'pansified' to Helen's insult — 'pansified little freak' is the accurate quote")
else:
    print(f"  WARN: '{OLD_FREAK}' not found in {lid}")
    idx = html.find('little freak')
    if idx >= 0:
        print(f"  'little freak' at {idx}: {repr(html[max(0,idx-100):idx+100])}")

# ============================================================
# A Taste of Honey — Eduqas Act 2 (pansified little freak)
# ============================================================
print("\n=== A Taste of Honey Eduqas Act2 ===")
lid = 'ce6affd5-7027-40c2-b46a-eed6537b7d60'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD_FREAK = "calling him a 'little freak'"
NEW_FREAK = "calling him a 'pansified little freak'"

if OLD_FREAK in html:
    new_html = html.replace(OLD_FREAK, NEW_FREAK)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/a-taste-of-honey/act-2',
               "Restored 'pansified' to Helen's insult — accurate quote is 'pansified little freak'")
else:
    print(f"  WARN: '{OLD_FREAK}' not found in {lid}")

# ============================================================
# A Taste of Honey — AQA Staging (18→19)
# ============================================================
print("\n=== A Taste of Honey AQA Staging ===")
lid = 'f379f8fa-a7a4-4421-bd39-457bf2917e44'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = 'the work of an 18-year-old'
NEW = 'the work of a 19-year-old'

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/a-taste-of-honey/staging',
               "Corrected Delaney's age at premiere from 18 to 19")
else:
    print(f"  WARN: '{OLD}' not found in {lid}")
    idx = html.find('18-year')
    if idx >= 0:
        print(f"  '18-year' at {idx}: {repr(html[max(0,idx-50):idx+100])}")

# ============================================================
# A Taste of Honey — Eduqas Context (18→19)
# ============================================================
print("\n=== A Taste of Honey Eduqas Context ===")
lid = 'fb8fea1a-2422-49af-8b5e-eacd4b2c0aee'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD_AGE = 'she was just 18 years old'
NEW_AGE = 'she was just 19 years old'

if OLD_AGE in html:
    html = html.replace(OLD_AGE, NEW_AGE)
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature-eduqas/a-taste-of-honey/context',
               "Corrected Delaney age from 18 to 19 at premiere")
else:
    print(f"  WARN: '{OLD_AGE}' not found in {lid}")
    idx = html.find('18 years')
    if idx >= 0:
        print(f"  '18 years' at {idx}: {repr(html[max(0,idx-50):idx+100])}")

save_partial()

# ============================================================
# An Inspector Calls — OCR Act 1 (misattributed Sheila quote)
# Two fixes: body text + Key Fact box
# ============================================================
print("\n=== An Inspector Calls OCR Act 1 ===")
lid = '07014cb8-5bfd-45f3-9e94-3fd18515edd2'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False

# Fix 1: "When the Inspector suggests that 'these girls aren't cheap labour — they're people,'"
OLD1 = "When the Inspector suggests that ‘these girls aren’t cheap labour — they’re people,’ Birling dismisses the comment entirely."
NEW1 = "When Sheila says ‘these girls aren’t cheap labour — they’re people,’ Birling dismisses her entirely."
if OLD1 in html:
    html = html.replace(OLD1, NEW1)
    changed = True
    print("  Applied Fix 1 (body text attribution)")
else:
    # Try with ASCII quotes
    import re as remod
    # Search case insensitively
    pat = r"When the Inspector suggests that ['‘]these girls aren['’]t cheap labour"
    m = remod.search(pat, html)
    if m:
        print(f"  Body text found at {m.start()}: {repr(html[m.start():m.start()+150])}")
    else:
        print(f"  WARN: Fix 1 not found")

# Fix 2: Key Fact box "The Inspector's line 'these girls aren't cheap labour — they're people'"
OLD2 = "The Inspector’s line ‘these girls aren’t cheap labour — they’re people’"
NEW2 = "Sheila’s line ‘these girls aren’t cheap labour — they’re people’"
if OLD2 in html:
    html = html.replace(OLD2, NEW2)
    changed = True
    print("  Applied Fix 2 (Key Fact attribution)")
else:
    # broader search
    idx = html.find("Inspector’s line")
    if idx >= 0:
        print(f"  'Inspector's line' at {idx}: {repr(html[max(0,idx-20):idx+200])}")
    else:
        # Try without curly quotes
        idx2 = html.find("Inspector's line")
        if idx2 >= 0:
            print(f"  straight quote at {idx2}: {repr(html[max(0,idx2-20):idx2+200])}")
        else:
            print(f"  WARN: Fix 2 'Key Fact Inspector line' not found")

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature-ocr/an-inspector-calls/act-1',
               "Fixed misattribution: 'these girls aren't cheap labour' is Sheila's line, not the Inspector's (both body text and Key Fact box)")

if not changed:
    # Try to find exact text
    idx = html.find("these girls aren")
    if idx >= 0:
        print(f"  Phrase at {idx}: {repr(html[max(0,idx-200):idx+200])}")

# ============================================================
# An Inspector Calls — Eduqas Act 1 (misattributed Sheila quote)
# ============================================================
print("\n=== An Inspector Calls Eduqas Act 1 ===")
lid = '34128216-f832-457e-913b-97342f703c3a'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# "The Inspector's rebuke is quiet but devastating: 'these girls aren't cheap labour — they're people.'"
OLD = "The Inspector’s rebuke is quiet but devastating: ‘these girls aren’t cheap labour — they’re people.’"
NEW = "Sheila’s challenge is direct and devastating: ‘these girls aren’t cheap labour — they’re people.’"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/an-inspector-calls/act-1',
               "Fixed misattribution: 'these girls aren't cheap labour' is Sheila's line not the Inspector's")
else:
    idx = html.find("these girls aren")
    if idx >= 0:
        print(f"  Context: {repr(html[max(0,idx-200):idx+200])}")
    else:
        print(f"  WARN: phrase not found at all in {lid}")

# ============================================================
# An Inspector Calls — AQA Act 1-2 (fabricated Gerald quote 'turning her out')
# ============================================================
print("\n=== An Inspector Calls AQA Act1-2 ===")
lid = '7830cb9d-e4f3-4c2c-85b1-a2daaed07fb4'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'left her — turning her out.' → rephrase to remove fabricated quote marks
OLD = "gave her money and ‘left her — turning her out.’"
NEW = "gave her money and ended the affair so he could focus on his business commitments."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/an-inspector-calls/act-1-2',
               "Removed fabricated quote 'left her — turning her out'; replaced with accurate paraphrase")
else:
    idx = html.find('turning her out')
    if idx >= 0:
        print(f"  'turning her out' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'turning her out' not found in {lid}")

# ============================================================
# An Inspector Calls — AQA Act 3 (Chief Constable error)
# ============================================================
print("\n=== An Inspector Calls AQA Act 3 ===")
lid = '8ae17eb2-d431-49eb-a42f-7dfe23bb5617'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = "They telephone the Chief Constable, who confirms there is no Inspector Goole on the force."
NEW = "Gerald makes independent enquiries and discovers there is no Inspector Goole on the local police force. The family also rings the Infirmary to confirm no girl has died."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/an-inspector-calls/act-3',
               "Corrected: Gerald makes independent enquiries (not 'telephoning the Chief Constable')")
else:
    idx = html.find('Chief Constable')
    if idx >= 0:
        print(f"  'Chief Constable' at {idx}: {repr(html[max(0,idx-200):idx+150])}")
    else:
        print(f"  WARN: 'Chief Constable' not found in {lid}")

# ============================================================
# An Inspector Calls — Edexcel Act 2 (fabricated 'adoring' quote)
# ============================================================
print("\n=== An Inspector Calls Edexcel Act 2 ===")
lid = 'd9f1b3a4-c2df-4196-b799-6a636594df49'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = "Eva ‘was very grateful’ and ‘gave me a look that was nothing less than adoring.’"
NEW = "Eva ‘was very grateful’ and, as Gerald later admits, ‘I became at once the most important person in her life.’"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-edexcel/an-inspector-calls/act-2',
               "Replaced fabricated 'adoring look' quote with Gerald's actual line from Act 2")
else:
    idx = html.find('adoring')
    if idx >= 0:
        print(f"  'adoring' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'adoring' not found in {lid}")

# ============================================================
# An Inspector Calls — Eduqas Act 2 (fabricated 'confess in public' quote)
# ============================================================
print("\n=== An Inspector Calls Eduqas Act 2 ===")
lid = 'ee389a4b-1087-4385-a313-2adbffb0df3d'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = "publicly shamed, and forced to ‘confess in public his responsibility.’"
NEW = "publicly shamed, and ‘dealt with very severely.’"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/an-inspector-calls/act-2',
               "Replaced fabricated 'confess in public his responsibility' with Mrs Birling's actual phrase 'dealt with very severely'")
else:
    idx = html.find('confess in public')
    if idx >= 0:
        print(f"  'confess in public' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'confess in public' not found in {lid}")

save_partial()

# ============================================================
# Animal Farm — Chapters 7-8 (anthem 'praising him' → 'praising Animal Farm')
# ============================================================
print("\n=== Animal Farm Chs 7-8 ===")
lid = '6e95a98a-bee9-44c4-8e4d-309adc1296e7'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Find "new anthem praising him" or similar
found = False
for OLD, NEW in [
    ('a new anthem praising him', 'a new anthem praising Animal Farm, composed by Minimus'),
    ('new anthem praising him', 'new anthem praising Animal Farm, composed by Minimus'),
    ('anthem praising Napoleon', 'anthem praising Animal Farm'),
]:
    if OLD in html:
        html = html.replace(OLD, NEW)
        found = True
        break

if found:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/animal-farm/chapters-7-8',
               "Corrected: the replacement anthem praises Animal Farm (not Napoleon personally); the Napoleon poem is a separate Ch 8 item")
else:
    idx = html.find('anthem')
    if idx >= 0:
        print(f"  'anthem' at {idx}: {repr(html[max(0,idx-100):idx+200])}")
    else:
        print(f"  WARN: no 'anthem' found in {lid}")

# ============================================================
# Animal Farm — Napoleon's Cult of Personality (poem replacing commandments)
# ============================================================
print("\n=== Animal Farm Napoleon's Cult ===")
lid = 'b3e6ed27-9f98-46e3-9f09-3d431f3572ea'
lesson = fetch_lesson(lid)
html = lesson['content_html']

found = False
for OLD, NEW in [
    ('replacing the Seven Commandments as the farm’s central text',
     'placed at the opposite end of the barn from the Seven Commandments'),
    ('replacing the Seven Commandments as the farm\'s central text',
     'placed at the opposite end of the barn from the Seven Commandments'),
    ('REPLACING the Seven Commandments',
     'placed at the opposite end of the barn from the Seven Commandments'),
]:
    if OLD in html:
        html = html.replace(OLD, NEW)
        found = True
        break

if found:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/animal-farm/napoleons-cult-of-personality',
               "Corrected: poem is placed at opposite end of barn from commandments, not replacing them")
else:
    idx = html.find('Seven Commandments')
    if idx >= 0:
        print(f"  First 'Seven Commandments' at {idx}: {repr(html[max(0,idx-100):idx+200])}")
    else:
        print(f"  WARN: no 'Seven Commandments' found in {lid}")

save_partial()

# ============================================================
# Anita and Me — AQA Context (Rivers of Blood — TV watching claim)
# ============================================================
print("\n=== Anita and Me AQA Context ===")
lid = '6d0790ff-0110-4edc-886e-af0fe4411f68'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# The issue: lesson claims Meena's family 'watches [Powell speech] on television'
# The novel actually has Meena's father say 'That Powell Bastard with his bloody rivers'
# — they hear about it but it's not necessarily watching on TV
# Find and soften the TV claim
OLD = "Meena’s family watches it on television"
NEW = "Meena’s father reacts furiously to Powell’s speech — his anger making a vivid impression on the young narrator"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/anita-and-me/context',
               "Corrected 'watches it on television' — the novel shows the father's angry reaction, not specifically TV watching")
else:
    idx = html.find('television')
    if idx >= 0:
        print(f"  'television' at {idx}: {repr(html[max(0,idx-200):idx+150])}")
    else:
        # May use different phrasing
        idx2 = html.find('Powell')
        if idx2 >= 0:
            print(f"  'Powell' at {idx2}: {repr(html[max(0,idx2-200):idx2+300])}")
        else:
            print(f"  WARN: neither 'television' nor 'Powell' found in {lid}")

# ============================================================
# Anita and Me — Character Analysis (Anita's father)
# ============================================================
print("\n=== Anita and Me Character Analysis ===")
lid = '66acc567-1445-4dad-83bf-703bad1ee8e9'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# The issue: 'Anita's father has left' — sources suggest father is Roberto,
# who is present (though absent/neglectful) in the novel
# Find in html
idx = html.find("Anita’s father has left")
if idx < 0:
    idx = html.find("Anita's father has left")

if idx >= 0:
    print(f"  Found at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    # Fix: father is present but largely absent/neglectful — not "has left"
    OLD = "Anita’s father has left"
    NEW = "Anita’s father Roberto is largely absent and uninvolved"
    if OLD in html:
        new_html = html.replace(OLD, NEW)
        update_lesson(lid, {'content_html': new_html})
        record_fix(lid, 'english-literature-aqa/anita-and-me/character-analysis',
                   "Corrected 'Anita's father has left' — father Roberto is present but absent/uninvolved")
    else:
        # Try straight quote
        OLD2 = "Anita's father has left"
        if OLD2 in html:
            new_html = html.replace(OLD2, "Anita's father Roberto is largely absent and uninvolved")
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature-aqa/anita-and-me/character-analysis',
                       "Corrected 'Anita's father has left' — father Roberto is present but absent/uninvolved")
else:
    print(f"  WARN: 'father has left' not found in {lid}")

# ============================================================
# Anita and Me — Ending & Growing Up (Meena 'nearly drowns')
# ============================================================
print("\n=== Anita and Me Ending ===")
lid = '7a6453f5-b9e3-41ae-b66a-75c135224644'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# The issue: lesson says Meena nearly drowns; actually Tracey falls in the pond
# and Meena breaks her leg falling from a horse
OLD = "where Meena nearly drowns after a horse bolts"
NEW = "where Meena falls from a bolting horse and breaks her leg"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/anita-and-me/the-ending',
               "Corrected: Meena breaks her leg falling from a horse; it is Tracey who falls in the pond")
else:
    idx = html.find('nearly drowns')
    if idx >= 0:
        print(f"  'nearly drowns' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        idx2 = html.find('horse')
        if idx2 >= 0:
            print(f"  'horse' at {idx2}: {repr(html[max(0,idx2-200):idx2+200])}")
        else:
            print(f"  WARN: nothing relevant found in {lid}")

# ============================================================
# Anita and Me — Racism Sam Lowbridge (fabricated quote 'We don't want...')
# ============================================================
print("\n=== Anita and Me Racism (98b8) ===")
lid = '98b8a08a-34a2-450e-aa9b-1a34905c881e'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'We don't want your lot round here!' — unverified fabricated quote
OLD = "‘We don’t want your lot round here!’"
NEW = ""  # just remove the fabricated quote entirely and rephrase

# Try to find in context
idx = html.find("We don’t want your lot")
if idx < 0:
    idx = html.find("We don't want your lot")

if idx >= 0:
    print(f"  Found at {idx}: {repr(html[max(0,idx-300):idx+200])}")
    # Remove the quotes but keep the gist
    for OLD_TRY in [
        "Sam publicly shouts racist abuse: ‘We don’t want your lot round here!’",
        "Sam publicly shouts racist abuse: ‘We don’t want your lot round here’",
        "shouts racist abuse: ‘We don’t want your lot round here!’",
    ]:
        if OLD_TRY in html:
            new_html = html.replace(OLD_TRY, "Sam makes openly racist statements targeting the village’s non-white residents")
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature-aqa/anita-and-me/racism',
                       "Removed unverified fabricated quote 'We don't want your lot round here!' — replaced with accurate paraphrase")
            break
    else:
        print(f"  WARN: could not match exact string for removal")
else:
    print(f"  WARN: 'We don't want your lot' not found in {lid}")

save_partial()

# ============================================================
# Anita and Me — Narrative Voice (opening line error)
# ============================================================
print("\n=== Anita and Me Narrative Voice ===")
lid = '9f0e34ed-17d2-4473-92af-313aaf5ab61e'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Lesson says opening line is 'I do not have many memories of Tollington before Anita Rutter'
# Actual opening line is 'I do not have many memories of my very early childhood'
OLD = "‘I do not have many memories of Tollington before Anita Rutter’"
NEW = "‘I do not have many memories of my very early childhood’"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/anita-and-me/narrative-voice',
               "Corrected opening line: actual text is 'I do not have many memories of my very early childhood' not 'of Tollington before Anita Rutter'")
else:
    # Try straight quotes
    for OLD_TRY in [
        "'I do not have many memories of Tollington before Anita Rutter'",
        "I do not have many memories of Tollington before Anita Rutter",
    ]:
        if OLD_TRY in html:
            new_html = html.replace(OLD_TRY, "‘I do not have many memories of my very early childhood’" if "'" in OLD_TRY else 'I do not have many memories of my very early childhood')
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature-aqa/anita-and-me/narrative-voice',
                       "Corrected opening line to match actual novel text")
            break
    else:
        idx = html.find('Tollington before Anita')
        if idx >= 0:
            print(f"  Found at {idx}: {repr(html[max(0,idx-100):idx+200])}")
        else:
            print(f"  WARN: 'Tollington before Anita Rutter' not found in {lid}")

# ============================================================
# Anita and Me — Context (c2e9 — Sam's speech at fete uses Smethwick slogan)
# ============================================================
print("\n=== Anita and Me Context (c2e9) ===")
lid = 'c2e90934-0470-49cb-8915-945c43c37131'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'If you want a nigger for a neighbour, vote Labour' — this is the 1964 Smethwick election
# campaign slogan, not Sam Lowbridge's dialogue in the novel
OLD1 = "‘If you want a nigger for a neighbour, vote Labour’"
OLD2 = "'If you want a nigger for a neighbour, vote Labour'"

found = False
for OLD in [OLD1, OLD2]:
    if OLD in html:
        # Context: it's presented as Sam's speech, but it's actually a historical campaign slogan
        # Fix: clarify that Sam echoes the infamous historical slogan
        idx = html.find(OLD)
        # Get surrounding context
        context = html[max(0,idx-300):idx+300]
        print(f"  Context: {repr(context)}")

        new_html = html.replace(OLD, "‘If you want a nigger for a neighbour, vote Labour’ — echoing the notorious slogan from the 1964 Smethwick by-election")
        update_lesson(lid, {'content_html': new_html})
        record_fix(lid, 'english-literature-aqa/anita-and-me/context',
                   "Clarified that 'If you want a nigger...' is the 1964 Smethwick election slogan echoed/referenced, not confirmed as Sam's exact words")
        found = True
        break

if not found:
    idx = html.find('nigger for a neighbour')
    if idx >= 0:
        print(f"  Found at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        print(f"  WARN: phrase not found in {lid}")

# ============================================================
# Anita and Me — Racism (c3e0 — Sam's speech at fete)
# ============================================================
print("\n=== Anita and Me Racism (c3e0) ===")
lid = 'c3e0ba3c-9e6a-456d-8835-be00b08fc4c2'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD1 = "‘If you want a nigger for a neighbour, vote Labour’"
OLD2 = "'If you want a nigger for a neighbour, vote Labour'"

found = False
for OLD in [OLD1, OLD2]:
    if OLD in html:
        new_html = html.replace(OLD, "‘If you want a nigger for a neighbour, vote Labour’ — echoing the notorious 1964 Smethwick election slogan")
        update_lesson(lid, {'content_html': new_html})
        record_fix(lid, 'english-literature-aqa/anita-and-me/racism-growing-apart',
                   "Clarified Sam's fete speech echoes the 1964 Smethwick slogan rather than being confirmed as his exact words")
        found = True
        break

if not found:
    idx = html.find('nigger for a neighbour')
    if idx >= 0:
        print(f"  Found at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        print(f"  WARN: phrase not found in {lid}")

# ============================================================
# Anita and Me — Context (d23d — Punjabi parents from Delhi)
# ============================================================
print("\n=== Anita and Me Context (d23d) ===")
lid = 'd23d4172-2f0d-4173-8128-7faf96f133e5'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Meera Syal was born in 1961 in Wolverhampton to Punjabi parents who had emigrated from Delhi'
# Sources confirm Wolverhampton + Punjabi parents, but no source confirms Delhi specifically
OLD = "Punjabi parents who had emigrated from Delhi"
NEW = "Punjabi parents who had emigrated from India"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/anita-and-me/context',
               "Changed 'from Delhi' to 'from India' — Delhi is not confirmed; all sources say India/Punjab")
else:
    idx = html.find('Delhi')
    if idx >= 0:
        print(f"  'Delhi' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'Delhi' not found in {lid}")

# ============================================================
# Anita and Me — Part 2 (d4682 — Anita's father has left)
# ============================================================
print("\n=== Anita and Me Part 2 (d4682) ===")
lid = 'd4682e10-5eac-4a36-addc-ae1712a5d0cd'
lesson = fetch_lesson(lid)
html = lesson['content_html']

for OLD, NEW in [
    ("Anita’s mother Deirdre is neglectful and frequently absent, her father has left",
     "Anita’s mother Deirdre is neglectful and frequently absent, and her father Roberto plays little active role in her life"),
    ("Anita's mother Deirdre is neglectful and frequently absent, her father has left",
     "Anita's mother Deirdre is neglectful and frequently absent, and her father Roberto plays little active role in her life"),
]:
    if OLD in html:
        new_html = html.replace(OLD, NEW)
        update_lesson(lid, {'content_html': new_html})
        record_fix(lid, 'english-literature-aqa/anita-and-me/part-2',
                   "Corrected 'father has left' — Roberto is present but largely absent/uninvolved")
        break
else:
    idx = html.find('father has left')
    if idx >= 0:
        print(f"  'father has left' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'father has left' not found in {lid}")

save_partial()

# ============================================================
# Anita and Me — Part 3 (d65d — Rivers of Blood + fete)
# ============================================================
print("\n=== Anita and Me Part 3 (d65d) ===")
lid = 'd65db752-979e-4192-9f80-d01ba8fa7dd8'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'The response to Enoch Powell's Rivers of Blood speech reveals that many villagers agree'
# The fix: make sure if we're paraphrasing, no quote marks; the text just needs to be accurate
idx = html.find("Rivers of Blood")
if idx >= 0:
    print(f"  Context: {repr(html[max(0,idx-300):idx+300])}")
    # The statement itself seems okay — it's describing community attitudes, not putting words in mouths
    # The audit flagged this but let's check if there's a fabricated quote around it
    # If no quotes around it, it's fine as commentary/context
    # No specific fix needed unless there's an issue with the fete quote too
    print(f"  Checking for fabricated fete quote...")
    for phrase in ["'We don't want your lot", "‘We don’t want your lot"]:
        if phrase in html:
            print(f"  Found fabricated quote — fixing...")
            # Replace fabricated Sam quote with paraphrase
            for OLD, NEW in [
                ("Sam Lowbridge makes openly racist statements [at the fete]. The response to Enoch Powell’s Rivers of Blood speech reveals that many villagers agree",
                 "Sam Lowbridge makes openly racist statements at the Spring Fete, and the response from many villagers reveals that his views are not uncommon in Tollington"),
            ]:
                if OLD in html:
                    html = html.replace(OLD, NEW)
                    update_lesson(lid, {'content_html': html})
                    record_fix(lid, 'english-literature-aqa/anita-and-me/part-3',
                               'Fixed Sam fete description; removed bracket notation; accurate paraphrase')
                    break
            break
    else:
        # Check if the actual text of the lesson is fine (just a factual statement about community response)
        print(f"  No fabricated quotes found — checking actual content...")
        # Read the sentence containing Rivers of Blood
        lines_around = html[max(0,idx-300):idx+400]
        if 'Rivers of Blood' in lines_around:
            # The triage says fix but canonical_truth is empty — it may just be a presentation note
            # The sentence is fine as historical context; no fix needed unless it's in quotes incorrectly
            print(f"  Content appears fine as historical paraphrase — no change needed")
else:
    print(f"  WARN: 'Rivers of Blood' not found in {lid}")

# ============================================================
# Anita and Me — Meena's World (d65d — opening scene with sweets from car)
# ============================================================
print("\n=== Anita and Me Meena's World (16761) ===")
lid = '16761122-7c38-4620-86b6-bc0bd665e1d0'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'The novel opens with Meena witnessing a man throw a bag of boiled sweets at an old woman from a passing car'
# GradeSaver says opening is about candy obtained at Ormerod's shop; the thrown-sweets-from-car detail is unconfirmed
OLD = "The novel opens with Meena witnessing a man throw a bag of boiled sweets at an old woman from a passing car. Meena’s response is to steal the sweets"
NEW = "The novel opens by introducing Meena as an unreliable narrator with a confessed tendency to steal and lie"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-aqa/anita-and-me/meenas-world',
               "Removed unverified 'boiled sweets thrown from car' opening scene — replaced with accurate general description of Meena as unreliable narrator")
else:
    # Try to find what's there
    idx = html.find('boiled sweets')
    if idx >= 0:
        print(f"  'boiled sweets' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        idx2 = html.find('novel opens')
        if idx2 >= 0:
            print(f"  'novel opens' at {idx2}: {repr(html[max(0,idx2-50):idx2+300])}")
        else:
            print(f"  WARN: neither 'boiled sweets' nor 'novel opens' found in {lid}")

save_partial()

# ============================================================
# Coram Boy — Context (0080 — Olivier Award error + first children's charity)
# ============================================================
print("\n=== Coram Boy Context (0080) ===")
lid = '0080a08b-a661-427c-97d5-f75528091143'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False

# Fix 1: "winning the Olivier Award for Best New Play" → "nominated for the Olivier Award for Best New Play"
OLD1 = "winning the Olivier Award for Best New Play"
NEW1 = "receiving four Olivier Award nominations including Best New Play"
if OLD1 in html:
    html = html.replace(OLD1, NEW1)
    changed = True
    print("  Applied Fix 1 (Olivier Award nomination vs win)")

# Fix 2: "Britain's first children's charity" → "the world's first incorporated charity"
OLD2 = "Britain’s first children’s charity"
NEW2 = "the world’s first incorporated charity and the UK’s oldest children’s charity"
if OLD2 in html:
    html = html.replace(OLD2, NEW2)
    changed = True
    print("  Applied Fix 2 (first children's charity → first incorporated charity)")
else:
    OLD2b = "Britain's first children's charity"
    if OLD2b in html:
        html = html.replace(OLD2b, "the world's first incorporated charity and the UK's oldest children's charity")
        changed = True
        print("  Applied Fix 2b (straight quotes)")

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/coram-boy/context',
               "Fixed: (1) Coram Boy was nominated not winner of Olivier Best New Play; (2) Foundling Hospital was first incorporated charity, not 'Britain's first children's charity'")
else:
    print(f"  WARN: could not find fixes in {lid}")
    idx = html.find('Olivier')
    if idx >= 0:
        print(f"  Olivier at {idx}: {repr(html[max(0,idx-50):idx+200])}")

# ============================================================
# Coram Boy — Character Analysis (5726 — Meshak 'sacrifices his life' error + Thomas Ledbury shot)
# ============================================================
print("\n=== Coram Boy Character Analysis (5726) ===")
lid = '5726e707-1192-4f4a-a2b3-c0dcab4c736f'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False

# Fix 1: "When he later sacrifices his life to protect Aaron" — Meshak dies of old age, not sacrifice
OLD1 = "When he later sacrifices his life to protect Aaron, he demonstrates that goodness is not dependent on intelligence, so"
NEW1 = "His act of protecting baby Aaron — defying his murderous father Otis — demonstrates that goodness is not dependent on intelligence, so"
if OLD1 in html:
    html = html.replace(OLD1, NEW1)
    changed = True
    print("  Applied Fix 1 (Meshak doesn't sacrifice his life)")
else:
    OLD1b = "When he later sacrifices his life to protect Aaron"
    idx = html.find(OLD1b)
    if idx >= 0:
        print(f"  Found partial at {idx}: {repr(html[max(0,idx-50):idx+200])}")

# Fix 2: Thomas Ledbury — lesson omits that he is shot and killed by Gaddarn
OLD2 = "Thomas becomes involved in uncovering the truth about Aaron’s identity and plays a practical role in bringing the novel"
NEW2 = "Thomas is shot and killed by Gaddarn (Otis) during the rescue of Aaron; his death is one of the novel's most shocking moments and"

if OLD2 in html:
    # Get rest of sentence to know how to complete
    idx = html.find(OLD2)
    rest = html[idx + len(OLD2):idx + len(OLD2) + 200]
    print(f"  Existing text after OLD2: {repr(rest[:100])}")
    html = html.replace(OLD2, NEW2)
    changed = True
    print("  Applied Fix 2 (Thomas Ledbury killed by Gaddarn)")
else:
    OLD2b = "Thomas becomes involved in uncovering the truth about Aaron's identity and plays a practical role in bringing the novel"
    if OLD2b in html:
        idx = html.find(OLD2b)
        rest = html[idx + len(OLD2b):idx + len(OLD2b) + 200]
        print(f"  Existing rest: {repr(rest[:100])}")
        new_html = html.replace(OLD2b, "Thomas is shot and killed by Gaddarn (Otis) during the rescue of Aaron; his death is one of the novel's most shocking moments and")
        html = new_html
        changed = True
        print("  Applied Fix 2b")
    else:
        idx = html.find('Thomas')
        if idx >= 0:
            print(f"  'Thomas' at {idx}: {repr(html[max(0,idx-20):idx+300])}")

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/coram-boy/character-analysis',
               "Fixed: (1) Meshak dies of old age not sacrifice; (2) Added that Thomas Ledbury is shot and killed by Gaddarn during rescue")

# ============================================================
# Coram Boy — Structure Setting (e1ca — Part 2 time gap)
# ============================================================
print("\n=== Coram Boy Structure (e1ca) ===")
lid = 'e1ca50ba-cc87-469d-8096-9ab29344fd21'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Part 1 is set in 1741 and Part 2 in 1750; lesson says 'early 1740s' and 'late 1740s'
found = False
for OLD, NEW in [
    ("Part 1 is set in the early 1740s and follows Meshak and Otis alongside the Ashbrook family. Part 2 jumps forward to the late 1740s",
     "Part 1 is set in 1741 and follows Meshak and Otis alongside the Ashbrook family. Part 2 jumps forward to 1750 — a nine-year gap"),
    ("Part 2 jumps forward to the late 1740s",
     "Part 2 jumps forward to 1750 — a nine-year gap"),
]:
    if OLD in html:
        html = html.replace(OLD, NEW)
        update_lesson(lid, {'content_html': html})
        record_fix(lid, 'english-literature/coram-boy/structure',
                   "Corrected dates: Part 1 = 1741, Part 2 = 1750 (nine-year gap, not 'early 1740s' / 'late 1740s')")
        found = True
        break

if not found:
    idx = html.find('1740')
    if idx >= 0:
        print(f"  '1740' at {idx}: {repr(html[max(0,idx-100):idx+300])}")
    else:
        idx2 = html.find('Part 1')
        if idx2 >= 0:
            print(f"  'Part 1' at {idx2}: {repr(html[max(0,idx2-20):idx2+300])}")
        else:
            print(f"  WARN: dates not found in {lid}")

save_partial()

# ============================================================
# DNA — Act 3: Adam Returns (cigarette torture not Act 3)
# ============================================================
print("\n=== DNA Act 3 Adam Returns (154b) ===")
lid = '154bf6a7-55b0-4e0c-b019-0cd62cc40712'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'she is the one who takes charge of torturing him with a cigarette'
# Cigarette torture is from Act 1's original bullying, not a new Act 3 scene
OLD = "she is the one who takes charge of torturing him with a cigarette"
NEW = "she is the one who takes charge of dealing with the unexpected return"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/dna/act-3',
               "Removed 'cigarette torture' as Act 3 action — cigarette torture was Act 1 backstory; Cathy's Act 3 violence is her handling of Adam's return")
else:
    idx = html.find('cigarette')
    if idx >= 0:
        print(f"  'cigarette' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        print(f"  WARN: 'cigarette' not found in {lid}")

# ============================================================
# DNA — Context: Youth Violence (821c — cigarette torture misplaced)
# ============================================================
print("\n=== DNA Context (821c) ===")
lid = '821cfde1-01a6-468b-813f-eab14045c901'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Cathy, who volunteers to threaten a postman and later tortures Adam with a cigarette'
# Cathy volunteers to threaten the postman (Act 2), and cigarette is Act 1 backstory
OLD = "volunteers to threaten a postman and later tortures Adam with a cigarette"
NEW = "volunteers to threaten the postman (Act 2) and involves herself in extreme acts throughout — reflecting Dennis Kelly’s point that ordinary people become capable of violence within a group"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/dna/context',
               "Removed 'tortures Adam with a cigarette' as Cathy's act — cigarettes were Act 1 pre-story; replaced with accurate description")
else:
    idx = html.find('cigarette')
    if idx >= 0:
        print(f"  'cigarette' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        print(f"  WARN: 'cigarette' not found in {lid}")

# ============================================================
# DNA — Acts 1-2 (b965 — shirt vs socks)
# ============================================================
print("\n=== DNA Acts 1-2 (b965) ===")
lid = 'b965df1d-3f86-4f4d-bdd6-5608754ac632'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = "setting his shirt on fire"
NEW = "setting his socks on fire"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/dna/acts-1-2',
               "Corrected: Adam was made to light his socks on fire (not his shirt) — confirmed by LitCharts Act 1")
else:
    idx = html.find('on fire')
    if idx >= 0:
        print(f"  'on fire' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'on fire' not found in {lid}")

# ============================================================
# DNA — Exam Technique (d5ea — 'Cathy going into television' embeds error)
# ============================================================
print("\n=== DNA Exam Technique (d5ea) ===")
lid = 'd5ea4ede-4a37-4095-9a7d-3ee1b71b6e3b'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Cathy going into television' — this embeds the error as a memorisable quotation
# Cathy's actual fate: she is rumoured to have killed a younger child, Phil goes silent, etc.
OLD = "Cathy going into ‘television.’"
NEW = "Cathy becoming ‘more and more extreme’ after Phil retreats."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/dna/exam-technique',
               "Removed 'Cathy going into television' as embedded memorisable quote — replaced with accurate description of her Act 4 trajectory")
else:
    # Try variants
    for OLD_TRY in [
        "Cathy going into 'television.'",
        "Cathy going into ‘television’",
        "going into 'television'",
        "going into ‘television’",
    ]:
        if OLD_TRY in html:
            new_html = html.replace(OLD_TRY, "Cathy becoming increasingly extreme after Phil retreats")
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature/dna/exam-technique',
                       "Removed 'Cathy going into television' as embedded quote — inaccurate; replaced with accurate Act 4 description")
            break
    else:
        idx = html.find('television')
        if idx >= 0:
            print(f"  'television' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
        else:
            print(f"  WARN: 'television' not found in {lid}")

save_partial()

# ============================================================
# Frankenstein — Pursuit & Ending (0581 — corrupted quote)
# ============================================================
print("\n=== Frankenstein Pursuit & Ending (0581) ===")
lid = '0581f441-6e06-475c-b1b3-36d8184b8673'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Another may succeed where I have failed' → 'yet another may succeed'
OLD = "‘Another may succeed where I have failed.’"
NEW = "‘yet another may succeed’"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/frankenstein/pursuit-ending',
               "Corrected Victor's quote: actual text is 'yet another may succeed' (no 'where I have failed')")
else:
    for OLD_TRY in [
        "Another may succeed where I have failed",
        "'Another may succeed where I have failed'",
    ]:
        if OLD_TRY in html:
            new_html = html.replace(OLD_TRY, "‘yet another may succeed’")
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature/frankenstein/pursuit-ending',
                       "Corrected Victor's quote to 'yet another may succeed'")
            break
    else:
        idx = html.find('succeed')
        if idx >= 0:
            print(f"  'succeed' at {idx}: {repr(html[max(0,idx-200):idx+150])}")
        else:
            print(f"  WARN: 'succeed' not found in {lid}")

# ============================================================
# Frankenstein — Key Themes (0a12 — 'Did I request thee' is epigraph, not Creature speech)
# ============================================================
print("\n=== Frankenstein Key Themes (0a12) ===")
lid = '0a12f1b6-4c0a-44f4-bbba-b4ead1ca5491'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Quote 'Did I request thee, Maker' is the title-page epigraph, not spoken by the Creature
OLD = "the Creature quotes Paradise Lost"
NEW = "the novel’s title-page epigraph draws from Paradise Lost"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/frankenstein/key-themes',
               "Corrected: 'Did I request thee' is the novel's title-page epigraph, not a speech by the Creature")
else:
    idx = html.find('request thee')
    if idx >= 0:
        print(f"  Context: {repr(html[max(0,idx-300):idx+200])}")
    else:
        print(f"  WARN: 'request thee' not found in {lid}")

# ============================================================
# Frankenstein — Creature's Story (346d — same epigraph issue)
# ============================================================
print("\n=== Frankenstein Creature's Story (346d) ===")
lid = '346dfdf8-2760-4122-9651-b750b7b520c9'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'The Creature asks: "Did I request thee, Maker, from my clay to mould me man?" — quoting Milton's Adam directly.'
# This is the epigraph, not a speech by the Creature in the story
OLD = "The Creature asks: ‘Did I request thee, Maker, from my clay to mould me man?’ — quoting Milton’s Adam directly."
NEW = "The novel’s title-page epigraph — ‘Did I request thee, Maker, from my clay to mould me Man?’ — is drawn from Milton’s Adam in Paradise Lost, setting up the theme of a creator’s responsibility to his creation."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/frankenstein/creatures-story',
               "Corrected: 'Did I request thee' is the title-page epigraph from Milton, not a speech by the Creature")
else:
    for OLD_TRY in [
        "The Creature asks: 'Did I request thee, Maker",
        "The Creature asks:",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial match at {idx}: {repr(html[max(0,idx-20):idx+300])}")
            break
    else:
        idx = html.find('request thee')
        if idx >= 0:
            print(f"  'request thee' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
        else:
            print(f"  WARN: 'request thee' not found in {lid}")

# ============================================================
# Frankenstein — Character Analysis (993b — Elizabeth 'adopted sister')
# ============================================================
print("\n=== Frankenstein Character Analysis (993b) ===")
lid = '993b71d3-a6ee-46fe-9ef8-ce6fd16e89b6'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Elizabeth is Victor's adopted sister and later his wife' — she is his COUSIN in 1818 edition
OLD = "Elizabeth is Victor’s adopted sister and later his wife"
NEW = "Elizabeth Lavenza is Victor’s cousin (adopted into the family) and later his wife"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/frankenstein/character-analysis',
               "Corrected: Elizabeth is Victor's cousin (1818 edition) not his adopted sister; she is adopted into the family but as a cousin, not a sibling")
else:
    for OLD_TRY in [
        "Elizabeth is Victor's adopted sister",
        "Victor’s adopted sister",
    ]:
        if OLD_TRY in html:
            new_html = html.replace(OLD_TRY, "Elizabeth Lavenza is Victor’s cousin (adopted into the family)" if "Elizabeth is" in OLD_TRY else "Victor’s cousin (adopted into the family)")
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature/frankenstein/character-analysis',
                       "Corrected: Elizabeth is Victor's cousin not adopted sister")
            break
    else:
        idx = html.find('Elizabeth')
        if idx >= 0:
            print(f"  'Elizabeth' at {idx}: {repr(html[max(0,idx-20):idx+200])}")
        else:
            print(f"  WARN: 'Elizabeth' not found in {lid}")

save_partial()

# ============================================================
# Henry V — Acts 1-2 (17bb — misattribution 'fracted and corroborate')
# ============================================================
print("\n=== Henry V Acts 1-2 (17bb) ===")
lid = '17bbf4d6-8468-4128-849e-cf49e2fcaeac'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Lesson attributes 'fracted and corroborate' to Mistress Quickly; it's Pistol's line (Act 2 Scene 1)
OLD = "Quickly says Falstaff’s heart was ‘fracted and corroborate’ (broken)."
NEW = "Pistol says Falstaff’s heart was ‘fracted and corroborate’ (broken and crushed) — a typically mangled Pistol malapropism in Act 2, Scene 1."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/henry-v/acts-1-2',
               "Corrected attribution: 'fracted and corroborate' is Pistol's line (Act 2 Scene 1), not Mistress Quickly's")
else:
    for OLD_TRY in [
        "Quickly says Falstaff's heart was 'fracted and corroborate'",
        "fracted and corroborate",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial at {idx}: {repr(html[max(0,idx-200):idx+200])}")
            break
    else:
        print(f"  WARN: 'fracted and corroborate' not found in {lid}")

# ============================================================
# Henry V — Act 5 (ff8f — Epilogue paraphrase with mixed quotes)
# ============================================================
print("\n=== Henry V Act 5 (ff8f) ===")
lid = 'ff8f86bd-7936-4f17-8c2a-9ca7fe88be9a'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'lived but a short time' and 'lost France and made his England bleed, / Which oft our stage hath shown'
# The actual Epilogue line is: 'Henry the Sixth, in infant bands crowned King / Of France and England, did this king succeed;
# Whose state so many had the managing, / That they lost France, and made his England bleed'
OLD = "Henry V ‘lived but a short time’ and his son, Henry VI, ‘lost France and made his England bleed, / Which oft our stage hath shown’"
NEW = "The Chorus notes that Henry V died young and his infant son Henry VI, left in the management of many, ‘lost France and made his England bleed’ — a sobering epilogue that undercuts the play’s triumphalism"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/henry-v/act-5',
               "Cleaned up Epilogue paraphrase — removed 'lived but a short time' (not exact text) and 'Which oft our stage hath shown' partial; kept the accurate 'lost France and made his England bleed' quote")
else:
    # Try without curly quotes
    for OLD_TRY in [
        "Henry V 'lived but a short time'",
        "lived but a short time",
        "lost France and made his England bleed",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial at {idx}: {repr(html[max(0,idx-200):idx+200])}")
            break
    else:
        print(f"  WARN: Epilogue content not found in {lid}")

save_partial()

# ============================================================
# Jane Eyre — Key Themes (bfd2 — Darcy quote misattributed to Rochester)
# ============================================================
print("\n=== Jane Eyre Key Themes (bfd2) ===")
lid = 'bfd272f4-821a-4a81-9b50-e5e3af499b80'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'I was in the middle before I knew that I had begun' is Darcy (P&P), NOT Rochester
OLD = "‘I was in the middle before I knew that I had begun’ (Rochester’s growth)."
NEW = ""  # Remove entirely — it's wrong text and wrong attribution

if OLD in html:
    # Find the context to know what to do with the surrounding sentence
    idx = html.find(OLD)
    context = html[max(0,idx-300):idx+len(OLD)+200]
    print(f"  Context: {repr(context)}")
    # Remove the wrong quote entirely
    new_html = html.replace(OLD + " Learn them all.", "Learn them all.")
    if new_html == html:
        # Try without 'Learn them all.'
        new_html = html.replace(OLD, "")
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/jane-eyre/key-themes',
               "Removed misattributed quote 'I was in the middle before I knew that I had begun' — this is Darcy in Pride & Prejudice, not Rochester in Jane Eyre")
else:
    for OLD_TRY in [
        "'I was in the middle before I knew that I had begun'",
        "I was in the middle before I knew that I had begun",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            context = html[max(0,idx-300):idx+len(OLD_TRY)+200]
            print(f"  Context: {repr(context)}")
            new_html = html.replace(OLD_TRY + " (Rochester’s growth). Learn them all.", "Learn them all.")
            if new_html == html:
                new_html = html.replace(OLD_TRY + " (Rochester's growth). Learn them all.", "Learn them all.")
            if new_html == html:
                new_html = html.replace(OLD_TRY, "")
            update_lesson(lid, {'content_html': new_html})
            record_fix(lid, 'english-literature/jane-eyre/key-themes',
                       "Removed misattributed Darcy quote from P&P falsely attributed to Rochester")
            break
    else:
        idx = html.find('middle before')
        if idx >= 0:
            print(f"  'middle before' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
        else:
            print(f"  WARN: quote not found in {lid}")

# ============================================================
# Jekyll and Hyde — Chapters 9-10 (241e — 'in the glass' not in text)
# ============================================================
print("\n=== Jekyll and Hyde Ch9-10 (241e) ===")
lid = '241ec110-09b6-448e-acab-91713c5f57c2'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'This, then, is the last time… that Henry Jekyll can think his own thoughts or see his own face in the glass'
# Actual text: 'This, then, is the last time, short of a miracle, that Henry Jekyll can think his own thoughts or see his own face'
# 'in the glass' is NOT in the original
OLD = "Henry Jekyll can think his own thoughts or see his own face in the glass"
NEW = "Henry Jekyll can think his own thoughts or see his own face"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/jekyll-and-hyde/chapters-9-10',
               "Removed 'in the glass' — not in the original Stevenson text; actual quote ends at 'see his own face'")
else:
    idx = html.find('in the glass')
    if idx >= 0:
        print(f"  'in the glass' at {idx}: {repr(html[max(0,idx-200):idx+100])}")
    else:
        print(f"  WARN: 'in the glass' not found in {lid}")

# ============================================================
# Jekyll and Hyde — Context Victorian Duality (7d48 — Dracula not 'earlier')
# ============================================================
print("\n=== Jekyll and Hyde Context (7d48) ===")
lid = '7d48ecbc-71d7-4623-98dc-06684907fdd2'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Earlier Gothic novels like Mary Shelley's Frankenstein (1818) and Bram Stoker's Dracula (1897)'
# Dracula (1897) was published AFTER Jekyll and Hyde (1886)
OLD = "Earlier Gothic novels like Mary Shelley’s Frankenstein (1818) and Bram Stoker’s Dracula (1897) shared similar concerns"
NEW = "Earlier Gothic works like Mary Shelley’s Frankenstein (1818) shared similar concerns, and later Gothic novels like Bram Stoker’s Dracula (1897) developed these themes further"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/jekyll-and-hyde/context',
               "Corrected: Dracula (1897) was published 11 years AFTER Jekyll and Hyde (1886) — cannot be called 'earlier'")
else:
    for OLD_TRY in [
        "Earlier Gothic novels like Mary Shelley's Frankenstein (1818) and Bram Stoker's Dracula (1897)",
        "Frankenstein (1818) and Bram Stoker",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial at {idx}: {repr(html[max(0,idx-50):idx+300])}")
            break
    else:
        idx = html.find('Dracula')
        if idx >= 0:
            print(f"  'Dracula' at {idx}: {repr(html[max(0,idx-200):idx+150])}")
        else:
            print(f"  WARN: 'Dracula' not found in {lid}")

save_partial()

# ============================================================
# Jekyll and Hyde — Ch 1-4 (ab8f — 'shattering' → 'shattered')
# ============================================================
print("\n=== Jekyll and Hyde Ch1-4 (ab8f) ===")
lid = 'ab8f788a-a891-4b6e-bce1-d75a1b52a9a1'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = "the bones were audibly shattering"
NEW = "the bones were audibly shattered"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/jekyll-and-hyde/chapters-1-4',
               "Corrected quote: Stevenson's text is 'audibly shattered' (past passive), not 'shattering' (present participle)")
else:
    idx = html.find('audibly')
    if idx >= 0:
        print(f"  'audibly' at {idx}: {repr(html[max(0,idx-100):idx+100])}")
    else:
        print(f"  WARN: 'audibly' not found in {lid}")

# ============================================================
# Jekyll and Hyde — Character Analysis (c111 — 'ausere' → 'austere')
# ============================================================
print("\n=== Jekyll and Hyde Character Analysis (c111) ===")
lid = 'c1111082-ed87-462b-b532-aa7ce03744d4'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Typo: 'ausere' → 'austere'
changed = False
for OLD, NEW in [
    ("‘ausere with himself’", "‘austere with himself’"),
    ("'ausere with himself'", "'austere with himself'"),
    ("ausere", "austere"),
]:
    if OLD in html:
        html = html.replace(OLD, NEW)
        changed = True
        break

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/jekyll-and-hyde/character-analysis',
               "Fixed typo: 'ausere' → 'austere' (Stevenson's actual word in the text)")
else:
    idx = html.find('ausere')
    if idx >= 0:
        print(f"  'ausere' at {idx}: {repr(html[max(0,idx-100):idx+100])}")
    else:
        print(f"  WARN: 'ausere' not found in {lid}")

# ============================================================
# Jekyll and Hyde — Ch 4-6 (ebf5 — cane owner: Jekyll not Utterson)
# ============================================================
print("\n=== Jekyll and Hyde Ch4-6 (ebf5) ===")
lid = 'ebf5e3eb-4848-440b-9b22-ab2251c0308b'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'The broken walking stick belonged to Utterson — he had given it to Jekyll as a gift years earlier.'
# Correct: The cane belonged to Jekyll (Utterson had given it to Jekyll as a gift)
# So at the time of murder the cane belonged to Jekyll, not Utterson
OLD = "The broken walking stick belonged to Utterson — he had given it to Jekyll as a gift years earlier."
NEW = "The broken walking stick had originally been Utterson’s gift to Jekyll, and was recognised by Utterson when it was presented to him as evidence."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/jekyll-and-hyde/chapters-4-6',
               "Corrected: the cane belonged to Jekyll (Utterson's old gift to him); lesson falsely said it 'belonged to Utterson'")
else:
    for OLD_TRY in [
        "The broken walking stick belonged to Utterson",
        "belonged to Utterson",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial at {idx}: {repr(html[max(0,idx-50):idx+200])}")
            break
    else:
        idx = html.find('walking stick')
        if idx >= 0:
            print(f"  'walking stick' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
        else:
            print(f"  WARN: 'walking stick' not found in {lid}")

save_partial()

# ============================================================
# Journey's End — Character Analysis (2042 — two misattributions)
# ============================================================
print("\n=== Journey's End Character Analysis (2042) ===")
lid = '2042d1a4-7334-454c-88bb-4d70f02c5f2a'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False

# Fix 1: 'the Colonel calls him the best company commander in the battalion' → Osborne says this
OLD1 = "the Colonel calls him ‘the best company commander in the battalion’"
NEW1 = "Osborne calls him ‘a long way the best company commander we’ve got’"
if OLD1 in html:
    html = html.replace(OLD1, NEW1)
    changed = True
    print("  Applied Fix 1 (Colonel→Osborne)")
else:
    OLD1b = "the Colonel calls him 'the best company commander in the battalion'"
    if OLD1b in html:
        html = html.replace(OLD1b, "Osborne calls him 'a long way the best company commander we've got'")
        changed = True
        print("  Applied Fix 1b")

# Fix 2: 'the one man I could talk to as a friend' attributed to Raleigh; it's Stanhope about Osborne
OLD2 = "Raleigh’s description of Stanhope as ‘the one man I could talk to as a friend’ establishes the schoolboy bond"
NEW2 = "Raleigh’s admiration for Stanhope is established early, though it is Stanhope who later describes Osborne as ‘the one man I could trust — my best friend — the one man I could talk to as man to man’"
if OLD2 in html:
    html = html.replace(OLD2, NEW2)
    changed = True
    print("  Applied Fix 2 (Raleigh→Stanhope speaks about Osborne)")
else:
    OLD2b = "Raleigh's description of Stanhope as 'the one man I could talk to as a friend' establishes the schoolboy bond"
    if OLD2b in html:
        html = html.replace(OLD2b, "Raleigh's admiration for Stanhope is established early, though it is Stanhope who later describes Osborne as 'the one man I could trust — my best friend — the one man I could talk to as man to man'")
        changed = True
        print("  Applied Fix 2b")

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/journeys-end/character-analysis',
               "Fixed two misattributions: (1) 'best company commander' is Osborne's line not the Colonel's; (2) 'one man I could talk to' is Stanhope about Osborne, not Raleigh about Stanhope")
else:
    idx = html.find('best company commander')
    if idx >= 0:
        print(f"  'best company commander' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        print(f"  WARN: not found in {lid}")

# ============================================================
# Journey's End — Key Themes (31b5 — two fixes)
# ============================================================
print("\n=== Journey's End Key Themes (31b5) ===")
lid = '31b57455-e90a-4bbd-9132-a5b0971fda54'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False

# Fix 1: 'It's the only way to forget' — unverified; actual Stanhope quote about drinking different
OLD1 = "Stanhope’s heroism is inseparable from his damage: ‘It’s the only way to forget.’"
NEW1 = "Stanhope’s heroism is inseparable from his damage. He drinks to endure what most cannot face."
if OLD1 in html:
    html = html.replace(OLD1, NEW1)
    changed = True
    print("  Applied Fix 1 (removed unverified 'It's the only way to forget')")
else:
    OLD1b = "Stanhope's heroism is inseparable from his damage: 'It's the only way to forget.'"
    if OLD1b in html:
        html = html.replace(OLD1b, "Stanhope's heroism is inseparable from his damage. He drinks to endure what most cannot face.")
        changed = True
        print("  Applied Fix 1b")

# Fix 2: 'the one man I could talk to as a friend' attributed to Raleigh
OLD2 = "Raleigh describes Stanhope as ‘the one man I could talk to as a friend,’"
NEW2 = "Stanhope describes Osborne as ‘the one man I could trust — my best friend — the one man I could talk to as man to man,’"
if OLD2 in html:
    html = html.replace(OLD2, NEW2)
    changed = True
    print("  Applied Fix 2 (Raleigh→Stanhope about Osborne)")
else:
    OLD2b = "Raleigh describes Stanhope as 'the one man I could talk to as a friend,'"
    if OLD2b in html:
        html = html.replace(OLD2b, "Stanhope describes Osborne as 'the one man I could trust — my best friend — the one man I could talk to as man to man,'")
        changed = True
        print("  Applied Fix 2b")
    else:
        idx = html.find('one man I could talk to')
        if idx >= 0:
            print(f"  'one man I could talk to' at {idx}: {repr(html[max(0,idx-200):idx+200])}")

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/journeys-end/key-themes',
               "Fixed two errors: (1) removed unverified 'It's the only way to forget' quote; (2) corrected 'one man I could talk to' to Stanhope about Osborne, not Raleigh about Stanhope")
else:
    print(f"  WARN: could not find fixes in {lid}")

# ============================================================
# Journey's End — Act 2: Tensions & the Raid (4b56 — corrupted Stanhope quote)
# ============================================================
print("\n=== Journey's End Act 2 (4b56) ===")
lid = '4b56556f-e5c8-42f0-9ef5-8fcdd75570d7'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# Corrupted quote: 'If you went — Loss of Raleigh's map will be — irreplaceable.'
# Actual: 'If you went — and left Osborne and Trotter and Raleigh and all the other men...'
OLD = "Stanhope tells Hibbert: ‘If you went — Loss of Raleigh’s map will be — irreplaceable.’"
NEW = "Stanhope tells Hibbert: ‘If you went — and left Osborne and Trotter and Raleigh and all the other men who are staying here — I’d rather spare you than any of them.’"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/journeys-end/act-2',
               "Replaced corrupted Stanhope quote ('Loss of Raleigh's map' nonsense) with his actual Act 2 Sc 2 speech to Hibbert")
else:
    for OLD_TRY in [
        "If you went — Loss of Raleigh",
        "If you went — Loss of Raleigh",
        "Loss of Raleigh's map will be — irreplaceable",
        "Loss of Raleigh’s map will be",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial at {idx}: {repr(html[max(0,idx-200):idx+200])}")
            break
    else:
        idx = html.find('Hibbert')
        if idx >= 0:
            print(f"  'Hibbert' at {idx}: {repr(html[max(0,idx-100):idx+300])}")
        else:
            print(f"  WARN: 'Hibbert' not found in {lid}")

save_partial()

# ============================================================
# Julius Caesar — Context (23dd — Antony speech not 'directly lifted' from Plutarch)
# ============================================================
print("\n=== Julius Caesar Context (23dd) ===")
lid = '23dd9de7-1127-4c7c-bd41-c6a2ca7e413e'
lesson = fetch_lesson(lid)
html = lesson['content_html']

OLD = "Some of Antony’s funeral speech is almost directly lifted from North’s translation, showing how closely Shakespeare worked from his sources."
NEW = "Shakespeare drew on North’s 1579 translation of Plutarch for the broad outline of events, though Antony’s funeral speech is Shakespeare’s own rhetorical invention — Plutarch’s account summarises the funeral in only a few lines."

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature/julius-caesar/context',
               "Corrected: Antony's speech is Shakespeare's own invention, not 'almost directly lifted' from Plutarch; Plutarch's account is very brief")
else:
    for OLD_TRY in [
        "Some of Antony's funeral speech is almost directly lifted from North's translation",
        "almost directly lifted from North",
        "directly lifted from North",
    ]:
        if OLD_TRY in html:
            idx = html.find(OLD_TRY)
            print(f"  Partial at {idx}: {repr(html[max(0,idx-100):idx+200])}")
            break
    else:
        idx = html.find('Plutarch')
        if idx >= 0:
            print(f"  'Plutarch' at {idx}: {repr(html[max(0,idx-100):idx+200])}")
        else:
            print(f"  WARN: 'Plutarch' not found in {lid}")

# ============================================================
# Lord of the Flies — Eduqas L1 Context (4327 — 'witnessed concentration camps' unverified)
# ============================================================
print("\n=== Lord of the Flies Eduqas Context (4327) ===")
lid = '43277330-f68f-42f6-b4c8-bbdafb7723f6'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'witnessed the liberation of concentration camps' — not confirmed in biographical record
OLD = "witnessed the liberation of concentration camps"
NEW = "witnessed the psychological collapse of ordinary men in extreme conditions"

if OLD in html:
    new_html = html.replace(OLD, NEW)
    update_lesson(lid, {'content_html': new_html})
    record_fix(lid, 'english-literature-eduqas/lord-of-the-flies/context',
               "Removed unverified 'witnessed the liberation of concentration camps' — Golding commanded LCT(R)460 on D-Day but no evidence he witnessed camp liberation")
else:
    idx = html.find('concentration camp')
    if idx >= 0:
        print(f"  'concentration camp' at {idx}: {repr(html[max(0,idx-200):idx+200])}")
    else:
        # Check full content
        idx2 = html.find('Golding')
        if idx2 >= 0:
            print(f"  'Golding' at {idx2}: {repr(html[max(0,idx2-50):idx2+300])}")
        else:
            print(f"  WARN: 'concentration camp' not found in {lid}")

# ============================================================
# Lord of the Flies — Edexcel L3 (f1e6 — 'Which is better...' misattributed to Ralph)
# ============================================================
print("\n=== Lord of the Flies Edexcel L3 (f1e6) ===")
lid = 'f1e60ae7-c6ac-467a-8019-cdea9ac55afe'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Which is better — to have rules and agree, or to hunt and kill?' attributed to Ralph; it's Piggy's line
# Find in content
idx = html.find('Which is better')
if idx >= 0:
    print(f"  'Which is better' at {idx}: {repr(html[max(0,idx-300):idx+200])}")
    # Look for the attribution
    context = html[max(0,idx-500):idx+300]
    if 'Ralph' in context:
        # Fix the attribution
        for OLD, NEW in [
            ("Ralph asks: ‘Which is better — to have rules and agree, or to hunt and kill?’",
             "Piggy asks: ‘Which is better — to have rules and agree, or to hunt and kill?’"),
            ("Ralph asks: 'Which is better — to have rules and agree, or to hunt and kill?'",
             "Piggy asks: 'Which is better — to have rules and agree, or to hunt and kill?'"),
            ("Ralph demands: ‘Which is better",
             "Piggy demands: ‘Which is better"),
            ("Ralph’s question: ‘Which is better",
             "Piggy’s question: ‘Which is better"),
            ("Ralph asks, ‘Which is better",
             "Piggy asks, ‘Which is better"),
            ("Ralph cries: ‘Which is better",
             "Piggy cries: ‘Which is better"),
        ]:
            if OLD in html:
                new_html = html.replace(OLD, NEW)
                update_lesson(lid, {'content_html': new_html})
                record_fix(lid, 'english-literature-edexcel/lord-of-the-flies/chapters-4-6',
                           "Corrected: 'Which is better — to have rules and agree, or to hunt and kill?' is Piggy's line (Ch 5), not Ralph's")
                break
        else:
            print(f"  WARN: could not find exact attribution pattern to fix")
            print(f"  Surrounding: {repr(context[-400:])}")
    else:
        print(f"  Ralph attribution not found in immediate context — may already be correct")
else:
    print(f"  WARN: 'Which is better' not found in {lid}")

save_partial()

# ============================================================
# Macbeth — Key Themes (13af — 'Incardnadine' → 'incarnadine')
# ============================================================
print("\n=== Macbeth Key Themes (13af) ===")
lid = '13affe23-f79d-4839-a453-4fa348cb7fea'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False
for OLD, NEW in [
    ('"Incardnadine"', '"incarnadine"'),
    ('‘Incardnadine’', '‘incarnadine’'),
    ('Incardnadine', 'incarnadine'),
]:
    if OLD in html:
        html = html.replace(OLD, NEW)
        changed = True

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/macbeth/key-themes',
               "Fixed spelling: 'Incardnadine' → 'incarnadine' (correct word from Act 2 Scene 2)")
else:
    idx = html.find('ncardnadine')
    if idx >= 0:
        print(f"  'ncardnadine' at {idx}: {repr(html[max(0,idx-50):idx+50])}")
    else:
        print(f"  WARN: 'Incardnadine' not found in {lid}")

# ============================================================
# Macbeth — Act 2: Duncan's Murder (3b2a — 'incardnadine' → 'incarnadine')
# ============================================================
print("\n=== Macbeth Act 2 (3b2a) ===")
lid = '3b2aecbd-8400-42d3-a42e-1d246da356fd'
lesson = fetch_lesson(lid)
html = lesson['content_html']

changed = False
for OLD, NEW in [
    ('"incardnadine"', '"incarnadine"'),
    ('‘incardnadine’', '‘incarnadine’'),
    ('incardnadine', 'incarnadine'),
]:
    if OLD in html:
        html = html.replace(OLD, NEW)
        changed = True

if changed:
    update_lesson(lid, {'content_html': html})
    record_fix(lid, 'english-literature/macbeth/act-2',
               "Fixed spelling: 'incardnadine' → 'incarnadine' (correct Shakespeare spelling)")
else:
    idx = html.find('ncardnadine')
    if idx >= 0:
        print(f"  'ncardnadine' at {idx}: {repr(html[max(0,idx-50):idx+50])}")
    else:
        print(f"  WARN: 'incardnadine' not found in {lid}")

save_partial()

# ============================================================
# My Name is Leon — Part 2 (1ce8 — Maureen described as Jamaican-British)
# ============================================================
print("\n=== My Name is Leon Part 2 (1ce8) ===")
lid = '1ce8bb53-1609-4416-8925-ed2ba513fbd2'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Maureen is a Jamaican-British woman' — need to verify; sources may say Caribbean/West Indian more generally
# The audit says 'Maureen is a Jamaican-British woman who has fostered many children... She cooks Caribbean food, uses Jamaican dialect'
# canonical_truth is empty, but source says GradeSaver confirms she cooks Caribbean food etc.
# This appears to be a flag to verify — if canonical is empty and source seems to confirm, may be okay
# The triage is 'fix' but the issue text == lesson_text and canonical is empty
# Let me just check what the lesson says and whether there's an actual error
idx = html.find('Jamaican')
if idx >= 0:
    print(f"  'Jamaican' at {idx}: {repr(html[max(0,idx-200):idx+300])}")
    # If it just says Jamaican-British that seems reasonable; no fix needed unless there's evidence she's not Jamaican
    print(f"  No canonical correction available — skipping this one (flagged as verify)")
else:
    idx2 = html.find('Maureen')
    if idx2 >= 0:
        print(f"  'Maureen' at {idx2}: {repr(html[max(0,idx2-20):idx2+300])}")

# ============================================================
# My Name is Leon — Character Analysis (a5fc — Tina as institutional system)
# ============================================================
print("\n=== My Name is Leon Character Analysis (a5fc) ===")
lid = 'a5fca6b5-d4e2-4b62-a6e9-fb322805bef7'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Tina represents the institutional system. She is not cruel — she is overworked, bound by policy'
# canonical_truth is empty; this may be an issue with how Tina is presented
# Without a canonical correction, let me check what's actually in the lesson
idx = html.find('Tina')
if idx >= 0:
    print(f"  'Tina' at {idx}: {repr(html[max(0,idx-50):idx+300])}")
    # The audit issue text matches lesson text — empty canonical means uncertain fix
    print(f"  No canonical correction provided — skipping (flagged as verify)")
else:
    print(f"  WARN: 'Tina' not found in {lid}")

# ============================================================
# My Name is Leon — Key Themes (c1a3 — 'Tufty's death signifies loss of a mentoring figure')
# ============================================================
print("\n=== My Name is Leon Key Themes (c1a3) ===")
lid = 'c1a3f04e-1edd-4db4-b027-7b4dd0e514ba'
lesson = fetch_lesson(lid)
html = lesson['content_html']

# 'Tufty's death signifies loss of a mentoring figure' — canonical_truth is empty
# Without canonical correction, check what's there
idx = html.find("Tufty")
if idx >= 0:
    print(f"  'Tufty' at {idx}: {repr(html[max(0,idx-100):idx+300])}")
    print(f"  No canonical correction provided — skipping (flagged as verify)")
else:
    print(f"  WARN: 'Tufty' not found in {lid}")

print("\n\n=== FINAL SAVE ===")
save_partial()

print(f"\n\nBatch A complete!")
print(f"Lessons modified: {len(lessons_modified)}")
print(f"Total fixes: {len(fixes)}")
print(f"\nModified lesson IDs:")
for lid in sorted(lessons_modified):
    print(f"  {lid}")
