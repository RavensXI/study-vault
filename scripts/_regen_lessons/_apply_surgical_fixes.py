"""
Surgical misquote fix script.
Applies 31 targeted fixes across 23 lessons.
Updates Supabase directly and writes _surgical_fix_log.json.
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_SERVICE_KEY']
sb = create_client(url, key)

with open('C:/Users/tshau/Documents/Study Vault/scripts/_regen_lessons/_lessons_cache.json', encoding='utf-8') as f:
    lessons = json.load(f)

fixes_applied = []
lessons_modified = []

def apply_fix(lesson_id, old_fragment, new_fragment, intended_poem, old_quote, new_quote, strategy, reasoning, subject_slug, lesson_slug):
    html = lessons[lesson_id]['content_html']
    if old_fragment not in html:
        print(f'  WARNING: fragment not found in {lesson_id[:8]}: {repr(old_fragment[:60])}')
        return False
    count = html.count(old_fragment)
    if count > 1:
        print(f'  WARNING: fragment found {count} times in {lesson_id[:8]}, replacing first only')
    new_html = html.replace(old_fragment, new_fragment, 1)
    lessons[lesson_id]['content_html'] = new_html
    fixes_applied.append({
        'lesson_id': lesson_id,
        'subject_slug': subject_slug,
        'lesson_slug': lesson_slug,
        'intended_poem': intended_poem,
        'old_quote': old_quote,
        'new_quote_or_paraphrase': new_quote,
        'strategy': strategy,
        'reasoning': reasoning
    })
    if lesson_id not in lessons_modified:
        lessons_modified.append(lesson_id)
    print(f'  OK: [{old_quote[:50]}] -> [{new_quote[:50]}]')
    return True

print('=== FIX 1: Letters from Yorkshire (681ee296) ===')
apply_fix(
    '681ee296-a685-4427-afa7-edc642737065',
    '“Is it enough to say that what he sees / I see?”',
    '“Is your life more real because you dig and sow?”',
    'Letters from Yorkshire',
    'Is it enough to say that what he sees / I see?',
    'Is your life more real because you dig and sow?',
    'canonical_swap',
    'Fabricated rhetorical question replaced with actual canonical rhetorical question from stanza 3; both interrogate connection across distance.',
    'english-literature-aqa', 'lesson-03'
)

print()
print('=== FIX 2a: Singh Song! – watching my bride (705185df) ===')
# Old: 'watching my bride — making chapatti after chapatti.'
# Canonical: the poem describes sharing chapatti together (vee share in chapatti) but has no watching/making phrase
# Context: 'The couple sit on the shop steps "watching my bride — making chapatti after chapatti."'
# Paraphrase: remove the quote and rephrase as paraphrase
apply_fix(
    '705185df-1eb7-4748-90d9-b1b32c60187c',
    'The couple sit on the shop steps “watching my bride — making chapatti after chapatti.” The mundane domestic detail (chapattis)',
    'The couple share food and domestic life: “vee share in chapatti / vee share in di chutney.” The mundane domestic detail (chapattis)',
    'Singh Song!',
    'watching my bride — making chapatti after chapatti.',
    'vee share in chapatti / vee share in di chutney.',
    'line_substitution',
    'Fabricated watching/making phrase replaced with actual canonical lines describing the shared domestic ritual.',
    'english-literature-aqa', 'lesson-04'
)

print()
print('=== FIX 2b: Singh Song! – Toronto plane-Loss (705185df) ===')
# Old: 'her eyes are black kohl / her hair is Toronto plane-Loss.'
# Canonical bride description: 'my bride / she hav a red crew cut / and she wear a Tartan sari'
apply_fix(
    '705185df-1eb7-4748-90d9-b1b32c60187c',
    '“her eyes are black kohl / her hair is Toronto plane-Loss.”',
    '“my bride / she hav a red crew cut / and she wear a Tartan sari.”',
    'Singh Song!',
    'her eyes are black kohl / her hair is Toronto plane-Loss.',
    'my bride / she hav a red crew cut / and she wear a Tartan sari.',
    'line_substitution',
    'Completely fabricated description (“Toronto plane-Loss” does not exist in the poem) replaced with the canonical bride description.',
    'english-literature-aqa', 'lesson-04'
)

print()
print('=== FIX 3a: Winter Swans – like swans (86689ccf) ===')
# Old: '“our hands, like swans, / settled after flight”'
# Canonical: 'like a pair of wings settling after flight'
apply_fix(
    '86689ccf-2ffb-4d6a-9dc7-c1579371e050',
    '“our hands, like swans, / settled after flight”',
    '“our hands … folded, one over the other, / like a pair of wings settling after flight”',
    'Winter Swans',
    'our hands, like swans, / settled after flight',
    'our hands … folded, one over the other, / like a pair of wings settling after flight',
    'canonical_swap',
    'Lesson substituted “like swans” for the actual simile “like a pair of wings”; ellipsis retains the discovery framing while preserving canonical wording.',
    'english-literature-aqa', 'lesson-05'
)

print()
print('=== FIX 3b: Climbing My Grandfather – place my ear (86689ccf) ===')
# Old: '"I place my ear to his chest and I can hear / the distant, accurate, rocking of his heart."'
# Canonical Climbing My Grandfather has: 'knowing / the slow pulse of his good heart.'
# The analysis uses 'accurate' as a key adjective - paraphrase needed since we can't keep the analysis
apply_fix(
    '86689ccf-2ffb-4d6a-9dc7-c1579371e050',
    '“I place my ear to his chest and I can hear / the distant, accurate, rocking of his heart.” The adjective “accurate” is unusual for a heartbeat — it suggests reliability, precision, and trustworthiness.',
    '“knowing / the slow pulse of his good heart.” The adjective “good” is deceptively simple — it suggests moral worth, kindness, and reliability. The word “slow” implies steadiness and age.',
    'Climbing My Grandfather',
    'I place my ear to his chest and I can hear / the distant, accurate, rocking of his heart.',
    'knowing / the slow pulse of his good heart.',
    'line_substitution',
    'Fabricated heart quote replaced with the actual canonical final lines; analysis rewritten around the real adjective “good” which supports the same argument about emotional discovery.',
    'english-literature-aqa', 'lesson-05'
)

print()
print('=== FIX 4: Winter Swans – like swans (d904aa40) exam bank ===')
apply_fix(
    'd904aa40-afe9-4066-9414-2b1ac053b921',
    '“our hands, like swans, / settled after flight” — reconciliation through nature.',
    '“our hands … folded, one over the other, / like a pair of wings settling after flight” — reconciliation through nature.',
    'Winter Swans',
    'our hands, like swans, / settled after flight',
    'our hands … folded, one over the other, / like a pair of wings settling after flight',
    'canonical_swap',
    'Same misquote as lesson-05 corrected in exam bank; “like swans” replaced with canonical “like a pair of wings”.',
    'english-literature-aqa', 'lesson-08'
)

print()
print('=== FIX 5: Remains – blood-shadow wanders (0769b2c1) ===')
apply_fix(
    '0769b2c1-32b0-405e-9a26-3d073fb42f3b',
    '“his blood-shadow wanders the streets of his home town”',
    '“His blood-shadow stays on the street”',
    'Remains',
    'his blood-shadow wanders the streets of his home town',
    'His blood-shadow stays on the street',
    'canonical_swap',
    'Canonical has “stays on the street” (haunting immobility); the lesson’s “wanders the streets” inverts the meaning and adds fabricated detail.',
    'english-literature-aqa', 'remains-and-war-photographer'
)

print()
print('=== FIX 6a: Poppies – tissue paper white (0e4206cb) ===')
# Old: '"the poppy had crimped petals, the paper red / bleeding through their tissue paper white"'
# Canonical: 'I pinned one onto your lapel, crimped petals, / spasms of paper red, disrupting a blockade / of yellow bias binding around your blazer.'
# The lesson analysis: 'The poppy becomes a symbol linking remembrance (red poppy), blood ("bleeding"), and fragility ("tissue paper")'
# Need to replace both the quote AND adjust the analysis slightly
apply_fix(
    '0e4206cb-013c-4d14-a555-3760a96c0b9d',
    '“the poppy had crimped petals, the paper red / bleeding through their tissue paper white” — The poppy becomes a symbol linking remembrance (red poppy), blood (“bleeding”), and fragility (“tissue paper”). The verb “bleeding” is visceral — even the symbol of reme',
    '“I pinned one onto your lapel, crimped petals, / spasms of paper red, disrupting a blockade / of yellow bias binding around your blazer” — The poppy becomes a symbol linking remembrance (red), violence (“spasms”), and disruption. The noun “spasms” is visceral — it suggests involuntary convulsion, even the symbol of reme',
    'Poppies',
    'the poppy had crimped petals, the paper red / bleeding through their tissue paper white',
    'I pinned one onto your lapel, crimped petals, / spasms of paper red, disrupting a blockade / of yellow bias binding around your blazer',
    'canonical_swap',
    'Fabricated hybrid image replaced with canonical opening description of the pinned poppy; analysis adjusted to match the actual word “spasms”.',
    'english-literature-aqa', 'tissue-and-poppies'
)

print()
print('=== FIX 6b: Poppies – gilt wire trembling (0e4206cb) ===')
# Old: '"I traced / the gilt wire trembling, crimped petals"'
# Canonical: 'On reaching the top of the hill I traced / the inscriptions on the war memorial, / leaned against it like a wishbone.'
apply_fix(
    '0e4206cb-013c-4d14-a555-3760a96c0b9d',
    '“I traced / the gilt wire trembling, crimped petals” — The mother touches the poppy delicately, as if touching her son. “Trembling” reveals her suppressed emotion. The sensory detail of touch makes the scene',
    '“On reaching the top of the hill I traced / the inscriptions on the war memorial, / leaned against it like a wishbone” — The mother traces the memorial as a surrogate act of touching her son. “Wishbone” reveals her fragile hope. The physical gesture of leaning makes the scene',
    'Poppies',
    'I traced / the gilt wire trembling, crimped petals',
    'On reaching the top of the hill I traced / the inscriptions on the war memorial, / leaned against it like a wishbone',
    'canonical_swap',
    'Fabricated “gilt wire trembling” replaced with the actual “I traced” passage from the canonical poem; analysis adjusted to match the real imagery.',
    'english-literature-aqa', 'tissue-and-poppies'
)

print()
print('=== FIX 7: War Photographer (Satyamurti) – viewfinder (5d00f939) ===')
apply_fix(
    '5d00f939-f7b6-4c71-8346-125758700059',
    '“The reassurance of the viewfinder, / the smells of chemicals and ordinary life.” The “viewfinder” acts as a barrier between the photographer and reality — a protective frame that allows them to cope. Yet the “reassurance” i',
    '“The reassurance of the frame” — a distancing mechanism that allows the photographer to cope. The “frame” creates a protected window on suffering. Yet the “reassurance” i',
    'War Photographer',
    'The reassurance of the viewfinder, / the smells of chemicals and ordinary life.',
    'The reassurance of the frame',
    'canonical_swap',
    'Canonical Satyamurti opens “The reassurance of the frame”; the lesson substituted “viewfinder” and fabricated the second line about chemicals (conflating with Duffy’s War Photographer).',
    'english-literature-edexcel', 'lesson-02'
)

print()
print('=== FIX 8: Baillie (d5821e85) – shakes so sore ===')
# Old: '"Your head, it shakes so sore, / And yet your leg, and then your other leg, / You know you cannot stretch them on the floor"'
# Canonical: 'Grand-dad, they say you’re old and frail, / Your stocked legs begin to fail:'
apply_fix(
    'd5821e85-e717-484a-9ba5-4c917cf64c75',
    '“Your head, it shakes so sore, / And yet your leg, and then your other leg, / You know you cannot stretch them on the floor” — the child catalogues the grandfather’s physical deterioration with innocent directness.',
    '“Grand-dad, they say you’re old and frail, / Your stocked legs begin to fail” — the child catalogues the grandfather’s physical deterioration with innocent directness.',
    'A Child to his Sick Grandfather',
    'Your head, it shakes so sore, / And yet your leg, and then your other leg, / You know you cannot stretch them on the floor',
    'Grand-dad, they say you’re old and frail, / Your stocked legs begin to fail',
    'line_substitution',
    'Fabricated three-line description replaced with the canonical opening couplet, which performs the same function of cataloguing decline.',
    'english-literature-edexcel', 'lesson-02'
)

print()
print('=== FIX 9: One Flesh – two shall become one flesh (9de8bdfe) ===')
# Old: 'The title alludes to the Christian marriage vow: "and the two shall become one flesh" (Genesis 2:24).'
# The lesson already notes Genesis 2:24 but puts it in quotation marks as if Jennings wrote it.
# Fix: make clear it’s quoting Genesis, not the poem itself.
apply_fix(
    '9de8bdfe-ed46-4093-a26a-c45e56155be5',
    'The title alludes to the Christian marriage vow: “and the two shall become one flesh” (Genesis 2:24).',
    'The title alludes to the Biblical phrase from Genesis 2:24 (“and they shall be one flesh”) — though Jennings’ poem inverts the ideal, showing a couple who are physically apart rather than united.',
    'One Flesh',
    'and the two shall become one flesh',
    '[paraphrase — attributed to Genesis, not Jennings]',
    'paraphrase_remove',
    'The Genesis phrase was presented as if it were a line from Jennings’ poem; rewritten to correctly attribute the Biblical allusion while noting Jennings inverts it.',
    'english-literature-edexcel', 'lesson-03'
)

print()
print('=== FIX 10a: Baillie exam bank – shakes so sore (4fb42f8b) ===')
# Old: '• “Your head, it shakes so sore” — innocent directness cataloguing decline'
apply_fix(
    '4fb42f8b-e4c2-47ff-9468-d771ac307748',
    '• “Your head, it shakes so sore” — innocent directness cataloguing decline (AO2: voice).',
    '• “Grand-dad, they say you’re old and frail” — innocent directness cataloguing decline (AO2: voice).',
    'A Child to his Sick Grandfather',
    'Your head, it shakes so sore',
    'Grand-dad, they say you’re old and frail',
    'line_substitution',
    'Fabricated line replaced with the canonical opening address; the poem function (voice of innocent directness) is preserved.',
    'english-literature-edexcel', 'lesson-08'
)

print()
print('=== FIX 10b: Baillie exam bank – You shall have my chair (4fb42f8b) ===')
# Old: '• “You shall have my chair” — child’s inadequate comfort (AO2: dramatic irony).'
# Canonical: 'When through the house you shift your stand, / I’ll lead you kindly by the hand;'
apply_fix(
    '4fb42f8b-e4c2-47ff-9468-d771ac307748',
    '• “You shall have my chair” — child’s inadequate comfort (AO2: dramatic irony).',
    '• “I’ll lead you kindly by the hand” — child’s tender, inadequate comfort (AO2: voice).',
    'A Child to his Sick Grandfather',
    'You shall have my chair',
    'I’ll lead you kindly by the hand',
    'line_substitution',
    'Fabricated comfort gesture replaced with the canonical equivalent (stanza 6) showing the child’s gentle practical care.',
    'english-literature-edexcel', 'lesson-08'
)

print()
print('=== FIX 11: In Romney Marsh – a mile or two (b6562ab2) ===')
# Old: '"Masts of ships, a mile or two, / Sailed through the sunset tall and fair"'
# Canonical: 'Masts in the offing wagged their tops; / The swinging waves pealed on the shore;'
apply_fix(
    'b6562ab2-0b6d-49ac-8cbe-1e38f632b5a0',
    '“Masts of ships, a mile or two, / Sailed through the sunset tall and fair” — personification makes the ships part of the natural scene.',
    '“Masts in the offing wagged their tops; / The swinging waves pealed on the shore” — personification makes the ships part of the natural scene.',
    'In Romney Marsh',
    'Masts of ships, a mile or two, / Sailed through the sunset tall and fair',
    'Masts in the offing wagged their tops; / The swinging waves pealed on the shore',
    'canonical_swap',
    'Fabricated mast image replaced with the actual canonical quatrain; the analysis point about personification still holds.',
    'english-literature-edexcel', 'lesson-02'
)

print()
print('=== FIX 12a: Stewart Island – only living creature (800fe93e) ===')
# Old: '"But for the birds I might have been / the only living creature on the island."'
# Not in canonical. The lesson uses this to say the landscape feels prehistoric and alienating.
# Canonical Stewart Island: the poem describes a hotel manager’s wife, a mad seagull attacking a child, and the speaker deciding to leave the country.
# Paraphrase: remove quote, keep the argument
apply_fix(
    '800fe93e-d68d-41a7-81a6-ff17fe5a715c',
    'a place so untouched and wild that it feels prehistoric: “But for the birds I might have been / the only living creature on the island.” The landscape is beautiful but alienating — the speaker is a visitor, not a native.',
    'a place beautiful but uncomfortable: the children collect shells and get bitten by sandflies; a seagull attacks. The landscape is vivid but alienating — the speaker is a visitor, not a native, and ends the poem having decided to leave the country.',
    'Stewart Island',
    'But for the birds I might have been / the only living creature on the island.',
    '[paraphrase — removed fabricated quote; content drawn from canonical poem]',
    'paraphrase_remove',
    'Fabricated “only living creature” quote removed; replaced with accurate paraphrase of the canonical poem’s actual events (sandflies, mad seagull, decision to leave).',
    'english-literature-edexcel', 'lesson-03'
)

print()
print('=== FIX 12b: Stewart Island – raft of resting shags (800fe93e) ===')
# Old: '"a raft of resting shags," "silver tree trunks."'
# Canonical Stewart Island has no shags (seabirds).
# The poem mentions 'mad seagull'. 'silver tree trunks' also not in canonical.
# Paraphrase - keep the observation about precise language but use real details
apply_fix(
    '800fe93e-d68d-41a7-81a6-ff17fe5a715c',
    'The poem uses precise, observational language: “a raft of resting shags,” “silver tree trunks.” Adcock does not romanticise the island; she presents it as real, detailed and slightly uncomfortable.',
    'The poem uses precise, observational language: Adcock notes the “fine bay” and “white sand,” but also the sandflies that bite the children and the seagull that attacks. Adcock does not romanticise the island; she presents it as real, detailed and slightly uncomfortable.',
    'Stewart Island',
    'a raft of resting shags',
    '[paraphrase — removed fabricated quote; replaced with accurate canonical details]',
    'paraphrase_remove',
    'Fabricated “raft of resting shags” and “silver tree trunks” removed; replaced with accurate details actually in the canonical poem.',
    'english-literature-edexcel', 'lesson-03'
)

print()
print('=== FIX 13: Postcard from a Travel Snob – do not send postcards (73dc71b5) ===')
# Old: '"I do not send postcards of sunsets to those back home"'
# Canonical opens: 'I do not wish that anyone were here.'
apply_fix(
    '73dc71b5-ff23-4971-b403-bface667a402',
    '“I do not send postcards of sunsets to those back home”',
    '“I do not wish that anyone were here”',
    'Postcard from a Travel Snob',
    'I do not send postcards of sunsets to those back home',
    'I do not wish that anyone were here.',
    'canonical_swap',
    'Fabricated postcard-of-sunsets line replaced with the actual canonical opening line, which makes the same point about the speaker’s exclusionary snobbery.',
    'english-literature-edexcel', 'lesson-05'
)

print()
print('=== FIX 14a: Stewart Island exam bank – raft of resting shags (175d5a2f) ===')
# Old: '“a raft of resting shags” (precise observation) • Speaker as visitor, not native • Free verse reflecting casual, detached exploration'
apply_fix(
    '175d5a2f-60ea-4fdc-9897-72ed6417b50c',
    '“a raft of resting shags” (precise observation) • Speaker as visitor, not native • Free verse reflecting casual, detached exploration',
    'precise observational detail (sandflies, a seagull attack, the hotel manager’s wife) • Speaker as visitor, not native • Free verse reflecting casual, detached exploration',
    'Stewart Island',
    'a raft of resting shags',
    '[paraphrase — removed fabricated quote; summarised actual poem details]',
    'paraphrase_remove',
    'Fabricated “raft of resting shags” removed from exam bank; replaced with accurate summary of the poem’s actual observational details.',
    'english-literature-edexcel', 'lesson-08'
)

print()
print('=== FIX 14b: Absence exam bank – I am the one whose want (175d5a2f) ===')
# Old: '"I am the one whose want / Has made this landscape poorer"'
# Canonical: 'It was because the place was just the same / That made your absence seem a savage force,'
apply_fix(
    '175d5a2f-60ea-4fdc-9897-72ed6417b50c',
    '“I am the one whose want / Has made this landscape poorer” (grief changes the landscape) • Double meaning of “want” (desire + lack) • Tight tercets (compressed emotion)',
    '“It was because the place was just the same / That made your absence seem a savage force” (grief changes the landscape) • The unchanged setting intensifies loss • Tight tercets (compressed emotion)',
    'Absence',
    'I am the one whose want / Has made this landscape poorer',
    'It was because the place was just the same / That made your absence seem a savage force',
    'line_substitution',
    'Fabricated “want … poorer” line replaced with the actual canonical tercet that makes the same point about grief transforming the landscape.',
    'english-literature-edexcel', 'lesson-08'
)

print()
print('=== FIX 15: The Émigrée – takes me dancing (2b9901df) ===')
# Old: '"my city takes me dancing."'
# Canonical: 'My city takes me dancing through the city / of walls.'
# The lesson truncated the quote, removing 'through the city / of walls' which is crucial to meaning
apply_fix(
    '2b9901df-aa06-4169-87f5-1bfaf199d583',
    '“my city takes me dancing.”',
    '“My city takes me dancing through the city / of walls.”',
    'The Émigrée',
    'my city takes me dancing.',
    'My city takes me dancing through the city / of walls.',
    'canonical_swap',
    'Truncated quote restored to full canonical form; the omitted “through the city / of walls” is crucial — it shows the memory navigating through oppressive reality, not just dancing freely.',
    'english-literature-ocr', 'lesson-02'
)

print()
print('=== FIX 16: The Émigrée exam bank – takes me dancing (e80168e3) ===')
apply_fix(
    'e80168e3-1eb6-4ff0-8e16-624a2511a13e',
    '“my city takes me dancing” |',
    '“My city takes me dancing through the city / of walls” |',
    'The Émigrée',
    'my city takes me dancing',
    'My city takes me dancing through the city / of walls',
    'canonical_swap',
    'Same truncated quote in exam bank restored to full canonical form.',
    'english-literature-ocr', 'lesson-08'
)

print()
print('=== FIX 17: I Wanna Be Yours – combined refrain (cade3aa6) ===')
# Old: 'The refrain "I don’t wanna be hers, I wanna be yours" strips love down'
# The canonical has these on TWO separate lines; the lesson presented them as a combined refrain with a comma
# However, 'i don’t wanna be hers' IS in the canonical (penultimate line)
# The fabrication is the comma joining them into one line.
# Fix: present them as separate lines
apply_fix(
    'cade3aa6-1bb2-4f55-908d-d37426e876a8',
    'The refrain “I don’t wanna be hers, I wanna be yours” strips love down to its simplest expression: exclusive devotion.',
    'The closing lines “i don’t wanna be hers” and “i wanna be yours” strip love down to its simplest expression: exclusive devotion.',
    'I Wanna Be Yours',
    'I don\'t wanna be hers, I wanna be yours',
    'i don\'t wanna be hers [and] i wanna be yours (as separate lines)',
    'canonical_swap',
    'The two lines are separate in the canonical poem; the lesson joined them with a comma into a single fabricated refrain. Fixed to present them as the two distinct closing lines they are.',
    'english-literature-ocr', 'lesson-04'
)

print()
print('=== FIX 18: I Wanna Be Yours exam bank – I don’t wanna be hers (afc96b91) ===')
# The exam bank lists: '"I don’t wanna be hers"' as a standalone quote.
# This IS verbatim in the canonical (penultimate line). The only issue is capitalisation (canonical uses lowercase 'i').
apply_fix(
    'afc96b91-baea-46fd-87f3-2e81ea7be23e',
    '“I don’t wanna be hers”',
    '“i don’t wanna be hers”',
    'I Wanna Be Yours',
    'I don\'t wanna be hers',
    'i don\'t wanna be hers',
    'canonical_swap',
    'Capitalisation corrected to match canonical lowercase; the line is in the poem but Clarke uses lowercase throughout.',
    'english-literature-ocr', 'lesson-08'
)

print()
print('=== FIX 19: The Bluebell/Eden Rock – missing “that” (be0ab045) ===')
# The lesson: 'Causley’s "I had not thought it would be like this"'
# Canonical Eden Rock: 'I had not thought that it would be like this.'
# The word 'that' is missing
apply_fix(
    'be0ab045-6828-4d1e-8452-df6bd5779f21',
    'Causley’s “I had not thought it would be like this”',
    'Causley’s “I had not thought that it would be like this”',
    'Eden Rock',
    'I had not thought it would be like this',
    'I had not thought that it would be like this',
    'canonical_swap',
    'The canonical final line of Eden Rock includes the word “that”; the lesson omitted it, creating a misquote.',
    'english-literature-ocr', 'lesson-05'
)

print()
print('=== FIX 20: Farther/Walker – build a table (efb4be31) ===')
# Old: 'Walker (1979) presents memory as identity-building: "He taught me how to build a table."'
# 'Farther' by Owen Sheers is about climbing a hill with his father; no table-building.
# The lesson references 'Walker (1979)' in the OCR Youth and Age context.
# OCR Youth and Age has 'red-roses' by Anne Sexton (not Alice Walker) and 'farther' by Owen Sheers.
# The 'Walker' attribution is itself unclear - but the quote is fabricated regardless.
# Paraphrase: rephrase as the lesson’s example-based comparison does not need a direct quote
apply_fix(
    'efb4be31-f7b3-404f-aca8-e5280651b9df',
    'Walker (1979) presents memory as identity-building: “He taught me how to build a table.” Writing as a Black American feminist, Walker transforms practical lessons into symbols of self-reliance. Memory is empowering because it connects to heritage.',
    'Sheers (2000) presents memory as identity-building: in “Farther,” the act of climbing a hill with his father is both physical effort and emotional inheritance. Sheers transforms a shared walk into a symbol of continuity. Memory is empowering because it connects to heritage.',
    'Farther',
    'He taught me how to build a table.',
    '[paraphrase — removed fabricated quote; replaced with accurate paraphrase of Farther]',
    'paraphrase_remove',
    'Fabricated “build a table” quote removed; the lesson’s comparison point (memory as identity-building through practical inheritance) rephrased accurately using Sheers’ Farther.',
    'english-literature-ocr', 'lesson-06'
)

print()
print('=== FIX 21: The Manhunt (Eduqas) – cicada shell (47b7f5e1) ===')
# Old: '"I’m still / as a cicada shell." The simile suggests the speaker has outgrown her former self'
# Not in Manhunt (Armitage). The Manhunt is narrated by Laura, the wife of an injured soldier.
# The lesson appears to confuse this with a different poem (possibly Afternoons by Larkin).
# Paraphrase: remove quote, keep the thematic point about the wife’s changed relationship
apply_fix(
    '47b7f5e1-9ed6-49a9-92a1-bcf81bb686fd',
    'The hurricane outside provides a backdrop that makes domestic safety feel precious: “I’m still / as a cicada shell.” The simile suggests the speaker has outgrown her former self, leaving behind an empty shell of adolescent fantasy for something real.',
    'The poem traces the wife’s painstaking, patient exploration of her husband’s body after injury. Armitage’s verb “trace”, repeated throughout, suggests tender, careful mapping of damage. The domestic relationship is transformed — what was once effortless now requires deliberate attention.',
    'The Manhunt',
    'I\'m still / as a cicada shell.',
    '[paraphrase — removed fabricated quote; replaced with accurate description of Manhunt]',
    'paraphrase_remove',
    'Fabricated cicada image removed; the lesson appeared to confuse Manhunt with a different poem. Replaced with an accurate thematic description of Armitage’s poem.',
    'english-literature-eduqas', 'lesson-01'
)

print()
print('=== FIX 22a: The Prelude (Eduqas) – went alone (fa8bcfab) ===')
# Old: '"I went alone / Into the night, and through the meadows"'
# Canonical Eduqas excerpt is the winter skating scene: 'And in the frosty season, when the sun / Was set'
# The lesson uses this as 'the confident tone of adventure'
apply_fix(
    'fa8bcfab-c09a-4046-b5a4-d0e051b222cf',
    '“I went alone / Into the night, and through the meadows” — the confident tone of adventure.',
    '“And in the frosty season, when the sun / Was set” — the confident setting-out on the ice.',
    'Excerpt from The Prelude',
    'I went alone / Into the night, and through the meadows',
    'And in the frosty season, when the sun / Was set',
    'line_substitution',
    'Fabricated nighttime meadow walk replaced with actual canonical opening of the skating excerpt; analysis adjusted to match the winter skating scene.',
    'english-literature-eduqas', 'lesson-03'
)

print()
print('=== FIX 22b: Living Space (fa8bcfab) – daring the air to be kind ===')
# Old: '"daring the air to be kind"'
# Canonical: 'and even dared to place / these eggs in a wire basket, / fragile curves of white / hung out over the dark edge'
apply_fix(
    'fa8bcfab-c09a-4046-b5a4-d0e051b222cf',
    'Dharker’s final image of eggs hung from a nail — “daring the air to be kind” — symbolises the fragile hope of people living in precarious conditions. The eggs represent both vulnerability (they could break) and life (they contain new beginnings)',
    'Dharker’s final image of eggs “hung out over the dark edge” — “and even dared to place / these eggs in a wire basket, / fragile curves of white” — symbolises the fragile hope of people living in precarious conditions. The eggs represent both vulnerability (they could break) and life (they contain new beginnings)',
    'Living Space',
    'daring the air to be kind',
    'and even dared to place / these eggs in a wire basket, / fragile curves of white',
    'canonical_swap',
    'Fabricated “daring the air to be kind” replaced with the actual canonical egg image; the analysis point about fragile hope is preserved.',
    'english-literature-eduqas', 'lesson-03'
)

print()
print('=== FIX 23a: The Manhunt exam bank (8cfb8271) – cicada shell ===')
apply_fix(
    '8cfb8271-de6d-479d-85ec-6a7612a62143',
    '“I’m still / as a cicada shell” — outgrown her former self for something real.',
    'tender, patient exploration — the verb “trace” repeated throughout maps the husband’s damage.',
    'The Manhunt',
    'I\'m still / as a cicada shell',
    '[paraphrase — removed fabricated quote; replaced with accurate description]',
    'paraphrase_remove',
    'Fabricated cicada image removed from exam bank; replaced with accurate description of the canonical poem’s repeated tracing motif.',
    'english-literature-eduqas', 'lesson-08'
)

print()
print('=== FIX 23b: Living Space exam bank (8cfb8271) – daring the air to be kind ===')
apply_fix(
    '8cfb8271-de6d-479d-85ec-6a7612a62143',
    '“daring the air to be kind” — fragile hope personified.',
    '“and even dared to place / these eggs in a wire basket” — fragile hope enacted.',
    'Living Space',
    'daring the air to be kind',
    'and even dared to place / these eggs in a wire basket',
    'canonical_swap',
    'Fabricated “daring the air to be kind” replaced in exam bank with canonical egg-placement image.',
    'english-literature-eduqas', 'lesson-08'
)

print()
print(f'=== SUMMARY ===')
print(f'Fixes applied: {len(fixes_applied)}')
print(f'Lessons modified: {len(lessons_modified)}')
print()

# Now update Supabase for each modified lesson
print('=== UPDATING SUPABASE ===')
for lesson_id in lessons_modified:
    new_html = lessons[lesson_id]['content_html']
    try:
        result = sb.table('lessons').update({'content_html': new_html}).eq('id', lesson_id).execute()
        print(f'  Updated {lesson_id[:8]}... OK ({len(new_html)} chars)')
    except Exception as e:
        print(f'  ERROR updating {lesson_id[:8]}: {e}')

print()
print('=== WRITING LOG ===')
log = {
    'lessons_modified': lessons_modified,
    'fixes_applied': fixes_applied
}
import os
os.makedirs('C:/Users/tshau/Documents/Study Vault/scripts/_regen_lessons', exist_ok=True)
with open('C:/Users/tshau/Documents/Study Vault/scripts/_regen_lessons/_surgical_fix_log.json', 'w', encoding='utf-8') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print('Log written to _surgical_fix_log.json')
