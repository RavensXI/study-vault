"""
Section rewrite v2 — reads actual content from saved JSON files to ensure exact string matching.
Uses regex for more flexible matching where content has curly quotes.
"""
import sys, os, json, re
os.environ['PYTHONIOENCODING'] = 'utf-8'
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lib.supabase_client import get_client

sb = get_client()
HERE = os.path.dirname(os.path.abspath(__file__))
log = {"lessons_modified": [], "fixes": []}

def load(lesson_id):
    with open(os.path.join(HERE, f"{lesson_id}.json"), encoding='utf-8') as f:
        return json.load(f)

def record(lesson_id, title, fix_desc):
    log["fixes"].append({"lesson_id": lesson_id, "title": title, "fix": fix_desc})
    print(f"  [FIX] {fix_desc}")

def push(lesson_id, payload):
    sb.table("lessons").update(payload).eq("id", lesson_id).execute()
    if lesson_id not in log["lessons_modified"]:
        log["lessons_modified"].append(lesson_id)
    print(f"  -> Updated Supabase row {lesson_id}")

def assert_replaced(old_html, new_html, needle, context=""):
    """Verify that something changed."""
    if old_html == new_html:
        print(f"  [WARN] No change for: {context[:80]}")
    else:
        print(f"  [OK] Replaced: {context[:70]}")

# ─── 1. CORAM BOY "PART 3" ───────────────────────────────────────────────────
print("\n=== 1. CORAM BOY: Part 3: Discovery & Resolution ===")
CB_ID = "26985264-3dc8-48c5-9799-288d4fb42679"
d = load(CB_ID)
html = d["content_html"]
conc = d["conclusion_html"]
cards = list(d["flashcard_questions"])
kcs = list(d["knowledge_checks"])
changed = {}

# Fix h2 for n7 — Meshak’s Sacrifice (curly apostrophe)
old = 'Meshak’s Sacrifice</h2>'
new = 'Thomas Ledbury’s Sacrifice</h2>'
html2 = html.replace(old, new)
assert_replaced(html, html2, old, "n7 h2 Meshak's Sacrifice")
html = html2
record(CB_ID, d["title"], "h2 n7: 'Meshak’s Sacrifice' → 'Thomas Ledbury’s Sacrifice'")

# Fix collapsible span "The Significance of Meshak's Death"
old = 'The Significance of Meshak’s Death'
new = 'The Significance of Thomas Ledbury’s Death'
html2 = html.replace(old, new)
assert_replaced(html, html2, old, "collapsible span Meshak's Death")
html = html2
record(CB_ID, d["title"], "Collapsible span: Meshak’s Death → Thomas Ledbury’s Death")

# Fix n8 — "Meshak places himself between Otis and Aaron" paragraph
# Use regex to catch any apostrophe variants
pattern_n8 = r'(<p data-narration-id="n8">)Meshak’s story reaches its climax.*?</p>'
repl_n8 = (
    r'\1The novel’s climax turns on a moment of devastating '
    r'<dfn class="term" data-def="Giving up something precious, often one’s own life, for the sake of another.">sacrifice</dfn>'
    r' — but the hero who dies is not Meshak. It is Thomas Ledbury, Alexander’s loyal childhood friend, who is shot and '
    r'killed by Gaddarn (Otis) during the rescue of Aaron and Toby. Thomas comes to the waterfront to help free the boys, '
    r'and Gavin uses his death to show that ordinary decency, not great wealth or social standing, is what defines true '
    r'courage. Meshak, by contrast, survives the climax: having defied his father years earlier by saving the baby, he '
    r'lives to see Aaron safe. In the Epilogue, Meshak dies peacefully of old age, his final thoughts resting on the child '
    r'he once rescued. It is Thomas’s death, not Meshak’s, that constitutes the novel’s act of physical sacrifice.</p>'
)
html2 = re.sub(pattern_n8, repl_n8, html, flags=re.DOTALL)
assert_replaced(html, html2, "n8 Meshak places himself", "n8 Meshak sacrifice paragraph")
html = html2
record(CB_ID, d["title"], "n8: Thomas Ledbury shot; Meshak dies peacefully in Epilogue")

# Fix n9 — "Meshak's death is the novel's most powerful moment"
pattern_n9 = r'(<p data-narration-id="n9">)Meshak’s death is the novel’s most powerful moment.*?</p>'
repl_n9 = (
    r'\1Thomas Ledbury’s death is one of the novel’s most powerful moments. He is not '
    r'a grand or glamorous character — he is a reliable, loyal friend who acts when it matters most. Gavin uses his '
    r'death to argue that moral courage is found in ordinary people, not in the wealthy or powerful who failed Aaron '
    r'throughout his life. Yet Meshak’s arc carries its own profound weight. The character whom society would consider '
    r'the least valuable — a man with a learning disability, the son of a criminal — shows the deepest '
    r'<dfn class="term" data-def="The quality of being willing to do what is right regardless of personal cost.">selflessness</dfn>: '
    r'he saved Aaron as a baby at great personal risk, watched over him for years, and in the Epilogue dies peacefully '
    r'knowing the boy is safe. Together, Thomas and Meshak represent Gavin’s argument that human worth cannot be '
    r'measured by class, intelligence, or social standing.</p>'
)
html2 = re.sub(pattern_n9, repl_n9, html, flags=re.DOTALL)
assert_replaced(html, html2, "n9 Meshak's death most powerful moment", "n9 collapsible body")
html = html2
record(CB_ID, d["title"], "n9: Thomas death + Meshak peaceful Epilogue death")

# Fix n11 — Otis "exposed and punished" but actually escapes
pattern_n11 = r'(<p data-narration-id="n11">The truth about Otis Gardiner’s child-collecting scheme.*?theatrical\.</p>)'
repl_n11 = (
    '<p data-narration-id="n11">The truth about Otis Gardiner’s child-collecting scheme is finally brought to light. '
    'His years of <dfn class="term" data-def="The act of pretending to be legitimate while committing crimes, as Otis does by posing as a Coram man.">deception</dfn> '
    '— posing as a Coram man, taking money from desperate mothers, ordering the burial of babies — are exposed. '
    'But Gavin deliberately refuses to give Otis a clean villain’s justice. He had already escaped hanging earlier in the '
    'novel by bribing officials to hang another man in his place, then reinvented himself as the wealthy Philip Gaddarn. '
    'In the climactic boat scene, Gaddarn falls or disappears overboard during the chaos of the rescue — his ultimate '
    'fate is left deliberately ambiguous. This is not accident or oversight: Gavin’s point is that the system which '
    'enabled Otis’s crimes remains intact even after he is gone.</p>'
)
html2 = re.sub(pattern_n11, repl_n11, html, flags=re.DOTALL)
assert_replaced(html, html2, "n11 Otis", "n11 Otis deception/downfall")
html = html2
record(CB_ID, d["title"], "n11: Otis escapes via bribery, becomes Gaddarn, disappears overboard")

# Fix n12 Key Fact — "Otis's downfall mirrors" paragraph inside key-fact
pattern_n12 = r'(data-narration-id="n12"[^>]*>\s*<div class="key-fact-label">Key Fact</div>\s*<p>)Otis’s downfall.*?</p>'
repl_n12 = (
    r'\1Gavin deliberately withholds clean justice for Otis. He escapes the noose by having an innocent man hanged '
    r'in his place, operates for years as Philip Gaddarn, and then vanishes into the water during the climax. His '
    r'ultimate fate is unknown. Gavin’s point is not that villainy always meets punishment, but that the social '
    r'and economic systems that made Otis’s crimes possible continue long after he is gone. The true drama of the '
    r'resolution belongs to Thomas Ledbury’s sacrifice and Aaron’s reunion with his parents.</p>'
)
html2 = re.sub(pattern_n12, repl_n12, html, flags=re.DOTALL)
assert_replaced(html, html2, "n12 key-fact Otis downfall", "n12 key-fact Otis")
html = html2
record(CB_ID, d["title"], "n12 key-fact: Otis escapes, Gaddarn, disappears overboard")

# Fix n14 — "Otis is exposed and punished"
pattern_n14 = r'(<p data-narration-id="n14">The novel’s ending offers a qualified sense.*?too high a cost\.</p>)'
repl_n14 = (
    '<p data-narration-id="n14">The novel’s ending offers a qualified sense of '
    '<dfn class="term" data-def="The final part of a narrative where conflicts are resolved and the story reaches a settled conclusion.">resolution</dfn>. '
    'Aaron is reunited with his birth parents. Otis’s crimes are exposed and Thomas Ledbury gives his life in the rescue. '
    'The buried babies are finally acknowledged. But Gavin does not present this as an uncomplicated happy ending. Thomas '
    'is dead. Aaron must absorb the shattering truth about his origins. The years he spent without a family cannot be '
    'returned. The other babies Otis buried are gone forever. And Otis himself — now Gaddarn — disappears '
    'overboard, his fate unknown, the system that created him unchanged. Justice comes, but it is partial, costly, and incomplete.</p>'
)
html2 = re.sub(pattern_n14, repl_n14, html, flags=re.DOTALL)
assert_replaced(html, html2, "n14 Otis exposed and punished", "n14 resolution paragraph")
html = html2
record(CB_ID, d["title"], "n14: 'Otis is exposed and punished' corrected; Thomas dies; Otis/Gaddarn disappears overboard")

# Fix n15 — "Meshak's goodness saves a life but costs his own"
pattern_n15 = r'(<p data-narration-id="n15">The ending asks the reader to hold two truths.*?society built on inequality\.</p>)'
repl_n15 = (
    '<p data-narration-id="n15">The ending asks the reader to hold two truths at once: that justice is possible, and '
    'that it is never complete. Aaron gains a family but has lost his foundling identity. Thomas Ledbury’s courage '
    'saves Aaron and Toby but costs him his life. Meshak survives to die peacefully in old age, his final peace a quiet '
    'form of redemption. Otis’s crimes are exposed, but he slips away rather than facing justice, and the system '
    'that enabled him — the class inequality, the lack of protection for vulnerable mothers and children — '
    'remains unchanged. Gavin refuses to offer simple comfort, instead leaving the reader to reflect on what real '
    'justice would look like in a society built on inequality.</p>'
)
html2 = re.sub(pattern_n15, repl_n15, html, flags=re.DOTALL)
assert_replaced(html, html2, "n15 Meshak goodness saves life", "n15 moral complexity")
html = html2
record(CB_ID, d["title"], "n15: Thomas dies; Meshak dies peacefully; Otis disappears without definitive punishment")

changed["content_html"] = html

# Conclusion fixes
old_c21 = 'Meshak’s sacrifice is the novel’s emotional climax — the character society values least proves to be the most morally courageous, challenging how we measure human worth.'
new_c21 = 'Thomas Ledbury’s death in the rescue is the novel’s act of physical sacrifice; Meshak’s arc ends peacefully in the Epilogue — together they challenge how society measures human worth.'
conc2 = conc.replace(old_c21, new_c21)
assert_replaced(conc, conc2, "conclusion n21 Meshak sacrifice", "conclusion n21")
conc = conc2
record(CB_ID, d["title"], "conclusion n21: Thomas/Meshak corrected")

old_c22 = 'The ending offers qualified justice: Aaron is reunited with his parents and Otis is exposed, but Meshak is dead, years are lost, and the system that enabled the crimes remains unchanged.'
new_c22 = 'The ending offers qualified justice: Aaron is reunited with his parents and Otis’s crimes are exposed, but Thomas Ledbury is dead, years are lost, Otis/Gaddarn disappears without definitive punishment, and the system that enabled the crimes remains unchanged.'
conc2 = conc.replace(old_c22, new_c22)
assert_replaced(conc, conc2, "conclusion n22", "conclusion n22")
conc = conc2
record(CB_ID, d["title"], "conclusion n22: Thomas/Otis corrected")
changed["conclusion_html"] = conc

# Flashcards
for i, fc in enumerate(cards):
    if 'How does Meshak die' in fc.get("q", ""):
        cards[i] = {
            "q": "How does Thomas Ledbury die in the novel’s climax?",
            "a": "He is shot and killed by Gaddarn (Otis) during the rescue of Aaron and Toby from the boat."
        }
        record(CB_ID, d["title"], "flashcard: Meshak death → Thomas Ledbury shot by Gaddarn")
    if 'Which character provides the novel' in fc.get("q", ""):
        cards[i] = {
            "q": "Who makes the physical sacrifice in the novel’s climax, and how does Meshak’s arc end?",
            "a": "Thomas Ledbury is shot dead saving Aaron; Meshak survives to die peacefully of old age in the Epilogue."
        }
        record(CB_ID, d["title"], "flashcard: moral centre → Thomas physical sacrifice + Meshak epilogue")
    if 'why is the novel' in fc.get("q", "").lower() and 'morally complex' in fc.get("q", "").lower():
        cards[i] = {
            "q": "Why is the novel’s ending described as morally complex, not simply happy?",
            "a": "Thomas dies; Otis/Gaddarn disappears overboard without definitive punishment; the unequal social system remains intact."
        }
        record(CB_ID, d["title"], "flashcard: moral complexity corrected")
changed["flashcard_questions"] = cards

# KCs
for i, kc in enumerate(kcs):
    for j, opt in enumerate(kc.get("options", [])):
        if "Meshak makes the ultimate sacrifice" in str(opt):
            kcs[i]["options"][j] = "Thomas Ledbury is shot saving Aaron and Toby"
            record(CB_ID, d["title"], "KC option: Meshak sacrifice → Thomas Ledbury shot")
changed["knowledge_checks"] = kcs

push(CB_ID, changed)


# ─── 2. JANE EYRE: GATESHEAD & LOWOOD ────────────────────────────────────────
print("\n=== 2. JANE EYRE (AQA): Gateshead & Lowood ===")
JE_ID = "2fe05d71-6399-483a-a753-1bdbda1322ed"
d = load(JE_ID)
html = d["content_html"]
gloss = list(d["glossary_terms"])
cards = list(d["flashcard_questions"])
kcs = list(d["knowledge_checks"])
changed = {}

# Fix the dfn for typhus — currently says 'often called ‘consumption,’'
# The DB content uses curly quotes around 'consumption'
old_typhus_dfn = 'An infectious disease, often called ‘consumption,’ that was a major killer in Victorian Britain, especially among the poor and malnourished.'
new_typhus_dfn = 'An acute infectious disease spread by lice and fleas, distinct from consumption (tuberculosis). Typhus caused deadly outbreaks in overcrowded institutions like workhouses and charity schools.'
html2 = html.replace(old_typhus_dfn, new_typhus_dfn)
assert_replaced(html, html2, "typhus dfn consumption", "typhus dfn")
html = html2
record(JE_ID, d["title"], "dfn tooltip: typhus ‘often called consumption’ corrected")

# Fix n11 — "killing many students — including Jane’s closest friend, Helen Burns"
pattern_n11 = r'(<p data-narration-id="n11">Conditions at Lowood are appalling.*?tuberculosis and died\.</p>)'
repl_n11 = (
    '<p data-narration-id="n11">Conditions at Lowood are appalling. The food is so poor that the girls are constantly '
    'hungry. In spring, a <dfn class="term" data-def="An acute infectious disease spread by lice and fleas, distinct '
    'from consumption (tuberculosis). Typhus caused deadly outbreaks in overcrowded institutions like workhouses and '
    'charity schools.">typhus</dfn> epidemic sweeps through the school, killing many students. Jane’s closest '
    'friend Helen Burns, however, does not die of typhus — she has been quietly dying of consumption (tuberculosis) '
    'throughout her time at Lowood. In Chapter 9, Jane steals away to Miss Temple’s room to be with Helen and wakes '
    'to find she has died with Jane’s arms around her neck. Brontë based these scenes on her own experience at '
    'the Clergy Daughters’ School at Cowan Bridge, where her sisters Maria and Elizabeth contracted tuberculosis. '
    'They were removed from the school and died at home in Haworth, their illness worsened by the school’s harsh '
    'conditions — the same disease that takes Helen Burns in the novel.</p>'
)
html2 = re.sub(pattern_n11, repl_n11, html, flags=re.DOTALL)
assert_replaced(html, html2, "n11 Helen Burns typhus", "n11 Lowood typhus/Helen")
html = html2
record(JE_ID, d["title"], "n11: Helen dies of consumption Ch.9 (not typhus); Brontë sisters context corrected")
changed["content_html"] = html

# Fix glossary
for i, g in enumerate(gloss):
    if g.get("term") == "typhus":
        gloss[i] = {
            "term": "typhus",
            "definition": "An acute infectious disease spread by lice and fleas. Distinct from consumption (tuberculosis) — typhus kills many Lowood students in spring, but Helen Burns dies separately of her pre-existing consumption in Chapter 9."
        }
        record(JE_ID, d["title"], "glossary: typhus definition corrected (not consumption)")
changed["glossary_terms"] = gloss

# Fix flashcard about typhus killing Helen Burns
for i, fc in enumerate(cards):
    if 'epidemic sweeps Lowood' in fc.get("q", ""):
        cards[i] = {
            "q": "What epidemic sweeps Lowood in spring, and how does Helen Burns actually die?",
            "a": "A typhus epidemic kills many Lowood students, but Helen Burns dies separately of consumption (TB) in Chapter 9 — Jane holds her as she dies."
        }
        record(JE_ID, d["title"], "flashcard: typhus/Helen Burns corrected")
    # Also fix any flashcard that mentions typhus killing Helen
    if "Helen Burns" in fc.get("a", "") and "typhus" in fc.get("a", "").lower():
        old_ans = fc["a"]
        new_ans = old_ans.replace("typhus", "consumption (TB)")
        if new_ans != old_ans:
            cards[i]["a"] = new_ans
            record(JE_ID, d["title"], "flashcard answer: typhus → consumption for Helen Burns")
changed["flashcard_questions"] = cards

push(JE_ID, changed)


# ─── 3. JOURNEY'S END: ACT 1 ─────────────────────────────────────────────────
print("\n=== 3. JOURNEY'S END (Edexcel): Act 1: Arrival in the Trenches ===")
JE2_ID = "c25f6db3-84f3-436c-bfbc-cf5a1fdc57e5"
d = load(JE2_ID)
html = d["content_html"]
cards = list(d["flashcard_questions"])
kcs = list(d["knowledge_checks"])
changed = {}

# Fix n7 — fabricated quote "It’s the only way to forget"
# Real Act 1 line: "She doesn't know that if I went up those steps..."
pattern_n7 = r'(<p data-narration-id="n7">When Stanhope finally appears.*?holding him together\.</p>)'
repl_n7 = (
    '<p data-narration-id="n7">When Stanhope finally appears, he is tense, irritable, and immediately reaches for '
    'the whisky. His key Act 1 line captures the desperate necessity of the habit: “She doesn’t know that '
    'if I went up those steps into the front line — without being doped with whiskey — I’d go mad '
    'with fright.” This tells us that Stanhope is self-aware — he knows he is damaged — but sees '
    'alcohol as his only means of functioning. The whisky is not a luxury; it is survival. Sherriff shows that the '
    'war has pushed this young man beyond his limits, and the prospect of facing the front line sober is, for '
    'Stanhope, unthinkable.</p>'
)
html2 = re.sub(pattern_n7, repl_n7, html, flags=re.DOTALL)
assert_replaced(html, html2, "n7 only way to forget", "n7 Stanhope drinking")
html = html2
record(JE2_ID, d["title"], "n7: fabricated ‘only way to forget’ → real Act 1 quote (mad with fright)")

# Fix n8 — "You think there’s no limit to what a man can bear?" is Act 3 S2, not Act 1
pattern_n8 = r'(<p data-narration-id="n8">Stanhope’s reaction to Raleigh’s arrival.*?Stanhope’s thinking\.</p>)'
repl_n8 = (
    '<p data-narration-id="n8">Stanhope’s reaction to Raleigh’s arrival is not pleasure but '
    '<dfn class="term" data-def="A feeling of intense worry or unease, often about an imminent event or something with an uncertain outcome.">anxiety</dfn>. '
    'He is terrified that Raleigh will write home and tell his sister — Stanhope’s fiancée, '
    'Madge — about his drinking and deterioration. He confides his fear to Osborne, revealing how '
    'precarious his grip on composure has become. He has maintained a facade of competence for three years, and '
    'Raleigh’s innocent admiration threatens to expose the truth. Note: Stanhope’s explosive outburst '
    '“To forget, you little fool — to forget! … You think there’s no limit to what a man '
    'can bear?” belongs to Act 3 Scene 2, after Osborne’s death — not Act 1.</p>'
)
html2 = re.sub(pattern_n8, repl_n8, html, flags=re.DOTALL)
assert_replaced(html, html2, "n8 no limit to what a man can bear", "n8 Stanhope anxiety")
html = html2
record(JE2_ID, d["title"], "n8: ‘no limit to what a man can bear’ attributed to Act 3 S2, not Act 1")

# Fix n13 Key Fact — "the one man I could talk to as a friend" misattributed
pattern_n13 = r'(data-narration-id="n13"[^>]*>\s*<div class="key-fact-label">Key Fact</div>\s*<p>)Raleigh remembers Stanhope as a school hero.*?</p>'
repl_n13 = (
    r'\1Raleigh hero-worships Stanhope from school: in his letter home, he calls him “the finest officer '
    r'in the battalion — the men simply love him.” Meanwhile, Stanhope’s closest confidant is '
    r'Osborne — it is Stanhope who, in Act 3 Scene 2 (after Osborne’s death), cries out “the one '
    r'man I could trust — my best friend — the one man I could talk to as man to man — who '
    r'understood everything.” These are two separate quotes by different characters in different acts. '
    r'Stanhope sees Raleigh as a threat who might expose his deterioration — a contrast between past '
    r'innocence and present damage that drives the play’s emotional core.</p>'
)
html2 = re.sub(pattern_n13, repl_n13, html, flags=re.DOTALL)
assert_replaced(html, html2, "n13 Raleigh one man I could talk to", "n13 key-fact attribution")
html = html2
record(JE2_ID, d["title"], "n13 key-fact: ‘one man I could talk to’ correctly attributed to Stanhope about Osborne (Act 3 S2)")
changed["content_html"] = html

# Fix flashcards
for i, fc in enumerate(cards):
    q = fc.get("q", "")
    a = fc.get("a", "")
    if "It’s the only way to forget" in a or "only way to forget" in a.lower():
        cards[i] = {
            "q": "Which Stanhope line from Act 1 reveals why he drinks?",
            "a": "“She doesn’t know that if I went up those steps into the front line — without being doped with whiskey — I’d go mad with fright.”"
        }
        record(JE2_ID, d["title"], "flashcard: fabricated ‘only way to forget’ → real Act 1 quote")
    if "no limit to what a man can bear" in a or "no limit to what a man can bear" in q:
        cards[i] = {
            "q": "In which act does Stanhope say “To forget, you little fool — to forget! You think there’s no limit to what a man can bear?”",
            "a": "Act 3 Scene 2 — after Osborne’s death, addressed to Raleigh who refuses to eat at the celebration dinner. Not Act 1."
        }
        record(JE2_ID, d["title"], "flashcard: ‘no limit’ correctly placed in Act 3 S2")
    if "one man I could talk to as a friend" in a:
        cards[i] = {
            "q": "How does Raleigh describe Stanhope in his letter home from Act 1?",
            "a": "“The finest officer in the battalion — the men simply love him.”"
        }
        record(JE2_ID, d["title"], "flashcard: Raleigh’s description corrected; misattributed quote removed")
changed["flashcard_questions"] = cards

# Fix KCs
for i, kc in enumerate(kcs):
    q = kc.get("q", "")
    opts = kc.get("options", [])
    # Fix "It's the only way to ___" fill-in
    if kc.get("type") == "fill" and ("only way to" in q.lower() or "forget" in str(opts).lower()):
        kcs[i] = {
            "q": "Stanhope says without whisky he would go _____ with fright if he faced the front line.",
            "type": "fill",
            "correct": 2,
            "options": ["wild", "numb", "mad", "sick"]
        }
        record(JE2_ID, d["title"], "KC fill-in: ‘only way to forget’ → correct Act 1 quote (mad with fright)")
    # Fix "the one man I could talk to as a _____" fill-in
    if kc.get("type") == "fill" and "one man I could talk to as a" in q:
        kcs[i] = {
            "q": "Complete Stanhope’s tribute to Osborne in Act 3 Scene 2: “the one man I could trust — my best friend — the one man I could talk to as _____ to man.”",
            "type": "fill",
            "correct": 0,
            "options": ["man", "friend", "soldier", "brother"]
        }
        record(JE2_ID, d["title"], "KC fill-in: corrected attribution — Stanhope about Osborne in Act 3 S2")
changed["knowledge_checks"] = kcs

push(JE2_ID, changed)


# ─── 4. PIGEON ENGLISH: THE ENDING ───────────────────────────────────────────
print("\n=== 4. PIGEON ENGLISH (AQA): The Ending ===")
PE_ID = "39adc443-d361-4e63-8deb-72a86a0e1568"
d = load(PE_ID)
html = d["content_html"]
conc = d["conclusion_html"]
cards = list(d["flashcard_questions"])
kcs = list(d["knowledge_checks"])
changed = {}

# Fix n3 — killer is Jordan, not "the Dell Farm Crew"
pattern_n3 = r'(<p data-narration-id="n3">)Harri is stabbed while running from the Dell Farm Crew.*?</p>'
repl_n3 = (
    r'\1Harri is stabbed in the stairwell by Jordan — a boy from the estate who kills him with a “war '
    r'knife.” The motive is not simply the murder investigation: Jordan’s act is rooted in the dispute '
    r'over Auntie Sonia’s remote-control car and the ban Mamma placed on their friendship. Kelman describes '
    r'the attack from Harri’s perspective: the confusion, the pain, the failure to understand what is '
    r'happening. Even in his final moments, Harri’s innocence persists — he does not fully comprehend '
    r'that he is dying.</p>'
)
html2 = re.sub(pattern_n3, repl_n3, html, flags=re.DOTALL)
assert_replaced(html, html2, "n3 Dell Farm Crew stab Harri", "n3 killer")
html = html2
record(PE_ID, d["title"], "n3: killer is Jordan (stairwell, war knife), not ‘the Dell Farm Crew’ collectively")

# Fix n4 Key Fact — same error
pattern_n4 = r'(data-narration-id="n4"[^>]*>\s*<div class="key-fact-label">Key Fact</div>\s*<p>)Harri is killed by the Dell Farm Crew.*?</p>'
repl_n4 = (
    r'\1Harri is killed by Jordan in the stairwell — not the Dell Farm Crew collectively. The immediate '
    r'trigger is a personal dispute (the remote-control car, Mamma banning the friendship), though Harri’s '
    r'investigation into the estate murder has drawn dangerous attention to him. Kelman narrates the death from '
    r'Harri’s confused, innocent perspective — he does not fully understand what is happening to him. '
    r'This choice makes the ending unbearably poignant: the reader understands the full horror that Harri cannot.</p>'
)
html2 = re.sub(pattern_n4, repl_n4, html, flags=re.DOTALL)
assert_replaced(html, html2, "n4 key-fact Dell Farm Crew kills Harri", "n4 key-fact killer")
html = html2
record(PE_ID, d["title"], "n4 key-fact: killer is Jordan (personal dispute + investigation)")

# Fix n8 Damilola Taylor — "stabbed to death" → broken glass / femoral artery
pattern_n8_pe = r'(<p data-narration-id="n8">The ending deliberately echoes Damilola Taylor’s death.*?same circumstances\.</p>)'
repl_n8_pe = (
    '<p data-narration-id="n8">The ending deliberately echoes the death of Damilola Taylor, a ten-year-old '
    'Nigerian boy who died in November 2000 on a Peckham estate after being attacked with a broken glass bottle '
    '— a shard severed his femoral artery and he bled to death. Like Damilola, Harri is a young immigrant '
    'boy killed on a council estate, his death the result of violence that institutions failed to prevent. Kelman '
    'wrote the novel eleven years after Damilola’s death, and the ending forces the reader to confront an '
    'uncomfortable truth: in those eleven years, nothing fundamental changed. Children are still dying in the '
    'same circumstances.</p>'
)
html2 = re.sub(pattern_n8_pe, repl_n8_pe, html, flags=re.DOTALL)
assert_replaced(html, html2, "n8 Damilola stabbed to death", "n8 Damilola Taylor")
html = html2
record(PE_ID, d["title"], "n8: Damilola died from broken glass/severed femoral artery (bled to death), not stabbed")
changed["content_html"] = html

# Fix conclusion
old_conc18 = 'Harri is killed because his investigation brought him too close to the truth — Kelman narrates the death from Harri’s confused, innocent perspective to maximise the reader’s horror.'
new_conc18 = 'Harri is killed by Jordan in the stairwell — Kelman narrates the death from Harri’s confused, innocent perspective to maximise the reader’s horror.'
conc2 = conc.replace(old_conc18, new_conc18)
assert_replaced(conc, conc2, "conclusion n18 investigation", "conclusion n18")
conc = conc2
record(PE_ID, d["title"], "conclusion n18: killer is Jordan, not investigation motive")
changed["conclusion_html"] = conc

# Fix flashcards
for i, fc in enumerate(cards):
    if 'How does Harri die' in fc.get("q", "") and 'Dell Farm Crew' in fc.get("a", ""):
        cards[i] = {
            "q": "How does Harri die in Pigeon English?",
            "a": "Stabbed in the stairwell by Jordan with a war knife — a personal dispute that intersected with his dangerous investigation."
        }
        record(PE_ID, d["title"], "flashcard: ‘Dell Farm Crew’ → Jordan stabs Harri")
changed["flashcard_questions"] = cards

# Fix KCs
for i, kc in enumerate(kcs):
    if kc.get("q") == "Why is Harri killed?":
        kcs[i]["options"][1] = "He is stabbed by Jordan in a personal dispute that intersects with his murder investigation"
        record(PE_ID, d["title"], "KC correct answer: Jordan stabs Harri (not ‘Dell Farm Crew’)")
changed["knowledge_checks"] = kcs

push(PE_ID, changed)

# ─── 4b. HUTIOUS — Harri's World ─────────────────────────────────────────────
print("\n=== 4b. PIGEON ENGLISH: Harri's World (hutious = scary) ===")
PE2_ID = "9abb3b24-d5be-4a40-8fd8-7a44b8f14dd1"
d = load(PE2_ID)
html = d["content_html"]
cards = list(d["flashcard_questions"])
changed = {}

# Fix n2 — 'hutious' for something brilliant
old_pe2_n2 = 'hutious” for something brilliant'
new_pe2_n2 = 'hutious” for something scary or frightening'
html2 = html.replace(old_pe2_n2, new_pe2_n2)
assert_replaced(html, html2, "hutious brilliant n2", "n2 hutious meaning")
html = html2
record(PE2_ID, d["title"], "n2: hutious = scary/frightening (not brilliant)")
changed["content_html"] = html

# Fix flashcards mentioning hutious = brilliant
for i, fc in enumerate(cards):
    a = fc.get("a", "")
    q = fc.get("q", "")
    if "hutious" in a.lower() and "brilliant" in a.lower():
        cards[i]["a"] = a.replace("brilliant", "scary or frightening")
        record(PE2_ID, d["title"], "flashcard: hutious = scary/frightening")
    if "hutious" in q.lower() and "brilliant" in q.lower():
        cards[i]["q"] = q.replace("brilliant", "scary or frightening")
        record(PE2_ID, d["title"], "flashcard question: hutious corrected")
    # Fix the answer that says "What Harri slang word means 'brilliant'?"
    if "brilliant" in q and "hutious" in a:
        cards[i] = {
            "q": "What does Harri’s slang word ‘hutious’ mean?",
            "a": "Scary or frightening."
        }
        record(PE2_ID, d["title"], "flashcard: hutious = brilliant → hutious = scary/frightening")
changed["flashcard_questions"] = cards

push(PE2_ID, changed)

# ─── 4c. HUTIOUS — Character Analysis ───────────────────────────────────────
print("\n=== 4c. PIGEON ENGLISH: Character Analysis (hutious fix) ===")
PE3_ID = "aad20898-d4c7-4b15-9ed3-a431d3d2499c"
d = load(PE3_ID)
html = d["content_html"]
cards = list(d["flashcard_questions"])
changed = {}

# Fix n2 — hutious listed without correct meaning
old_pe3_n2 = '(“hutious,” “bo-styles,” “asweh”)'
new_pe3_n2 = '(“hutious” for scary/frightening, “bo-styles” for cool, “asweh” as an oath)'
html2 = html.replace(old_pe3_n2, new_pe3_n2)
assert_replaced(html, html2, "hutious bo-styles asweh n2", "n2 slang meaning")
html = html2
record(PE3_ID, d["title"], "n2: hutious glossed as scary/frightening")
changed["content_html"] = html

# Fix flashcard
for i, fc in enumerate(cards):
    a = fc.get("a", "")
    if "'Hutious' (brilliant)" in a or "‘Hutious’ (brilliant)" in a:
        cards[i]["a"] = a.replace("(brilliant)", "(scary/frightening)")
        record(PE3_ID, d["title"], "flashcard: Hutious (brilliant) → Hutious (scary/frightening)")
changed["flashcard_questions"] = cards

push(PE3_ID, changed)


# ─── 5. PRINCESS & THE HUSTLER: ACT 1 ────────────────────────────────────────
print("\n=== 5. PRINCESS & THE HUSTLER (AQA): Act 1: The Family & the Dream ===")
PH_ID = "263021cb-1ef8-4ff0-a975-2049493a0bba"
d = load(PH_ID)
html = d["content_html"]
conc = d["conclusion_html"]
cards = list(d["flashcard_questions"])
kcs = list(d["knowledge_checks"])
changed = {}

# Fix n2 — "She lives in St Pauls, Bristol, with her mother Mavis, her father Wendell, and her older brother Junior"
# Wendell is NOT there at the start
pattern_n2_ph = r'(<p data-narration-id="n2"><em>Princess &amp; The Hustler</em> opens with a sense of energy and warmth\..*?held together by love but tested by the world outside their door\.</p>)'
repl_n2_ph = (
    '<p data-narration-id="n2"><em>Princess &amp; The Hustler</em> opens with a sense of energy and warmth. We '
    'meet Princess, a ten-year-old girl with a vivid imagination and an unshakeable optimism. The play is set '
    'during the Bristol Bus Boycott of 1963. At the opening, Princess lives in St Pauls with her mother '
    '<dfn class="term" data-def="Princess’s mother, a protective and hardworking Jamaican woman who prioritises her children’s safety and future.">Mavis</dfn> '
    'and her older brother '
    '<dfn class="term" data-def="Princess’s older brother, a teenager navigating questions of identity and belonging in 1960s Bristol.">Junior</dfn>. '
    'Her father <dfn class="term" data-def="Princess’s father, known as ‘the hustler’ — absent for approximately ten years at the play’s opening, whose unexpected return is the inciting incident of Act 1.">Wendell</dfn> '
    'has been absent for roughly a decade. His unexpected return partway through Act 1 is the catalyst for the '
    'play’s central conflict: he arrives with '
    '<dfn class="term" data-def="Wendell’s mixed-race half-daughter by another woman, approximately one year younger than Princess, whose identity is a central theme of the play.">Lorna</dfn>, '
    'his mixed-race daughter by another woman. Mavis initially refuses to have Wendell in the house but accepts '
    'Lorna — and Princess and Lorna quickly form a bond that becomes central to the play’s identity theme.</p>'
)
html2 = re.sub(pattern_n2_ph, repl_n2_ph, html, flags=re.DOTALL)
assert_replaced(html, html2, "n2 lives with Mavis Wendell Junior", "n2 family intro")
html = html2
record(PH_ID, d["title"], "n2: Wendell absent at start; return is inciting incident; Lorna introduced; Bristol Bus Boycott 1963 named")

# Fix n12 — "His hustle is not criminal"
pattern_n12_ph = r'(<p data-narration-id="n12">Wendell is the play’s title character.*?make his own way\.</p>)'
repl_n12_ph = (
    '<p data-narration-id="n12">Wendell is the play’s title character — “the hustler.” He is '
    'charismatic, ambitious, and full of energy. His '
    '<dfn class="term" data-def="Ambitious plans or schemes, often involving risk. For Wendell, hustle included a criminal past driven by the racist denial of legitimate work.">hustle</dfn> '
    'has a darker history than it first appears: Mavis reveals in Act 2 that after Jamaican military service, '
    'Wendell was promised a decent job in England but given a much lower position. The systematic discrimination '
    'he faced pushed him towards criminal activity — a fact Odimba presents as a systemic failure, not a '
    'personal moral choice. The boycott represents Wendell’s attempt to move from individual criminality '
    'driven by exclusion to collective legitimate action.</p>'
)
html2 = re.sub(pattern_n12_ph, repl_n12_ph, html, flags=re.DOTALL)
assert_replaced(html, html2, "n12 hustle not criminal", "n12 Wendell hustle")
html = html2
record(PH_ID, d["title"], "n12: Wendell’s hustle includes criminal past (driven by discrimination after Jamaican military service)")

# Fix n13 — "his ambition is a response to exclusion"
pattern_n13_ph = r'(<p data-narration-id="n13">Yet Wendell’s dreams also create tension.*?real problem\.</p>)'
repl_n13_ph = (
    '<p data-narration-id="n13">Yet Wendell’s return creates immediate tension — and not just because '
    'he arrives with Lorna. Mavis knows the truth of his past, and the audience gradually learns it too. Odimba '
    'presents his criminal history with compassion rather than condemnation: his ambition is a <em>response</em> '
    'to exclusion, and his involvement in the Bristol Bus Boycott represents genuine transformation. The '
    'system’s failure to offer him legitimate opportunity is the root cause — but Odimba does not '
    'pretend his past choices carried no cost.</p>'
)
html2 = re.sub(pattern_n13_ph, repl_n13_ph, html, flags=re.DOTALL)
assert_replaced(html, html2, "n13 Wendell dreams create tension", "n13 Wendell tension/past")
html = html2
record(PH_ID, d["title"], "n13: Wendell’s return tension includes Lorna; criminal past acknowledged compassionately")

# Fix n14 Key Fact — "hustler" reclaimed as purely positive
pattern_n14_ph = r'(data-narration-id="n14"[^>]*>\s*<div class="key-fact-label">Key Fact</div>\s*<p>)The word “hustler” is reclaimed in this play.*?</p>'
repl_n14_ph = (
    r'\1The word “hustler” carries a double meaning in the play. It represents resourcefulness and '
    r'refusal to accept defeat — a survival strategy in a society that denies legitimate opportunity. '
    r'But it also acknowledges that Wendell’s past included criminal activity, driven there by racist '
    r'exclusion after his Jamaican military service. Odimba does not simply redeem the word; she insists we '
    r'understand the systemic causes behind it.</p>'
)
html2 = re.sub(pattern_n14_ph, repl_n14_ph, html, flags=re.DOTALL)
assert_replaced(html, html2, "n14 hustler reclaimed", "n14 key-fact hustler")
html = html2
record(PH_ID, d["title"], "n14 key-fact: ‘hustler’ double meaning — also criminal past with systemic cause")
changed["content_html"] = html

# Fix conclusion
old_c33 = 'Act 1 introduces the family: Princess (optimistic dreamer), Mavis (protective realist), Wendell (ambitious hustler), and Junior (frustrated teenager).'
new_c33 = 'Act 1 introduces the family: Princess (optimistic dreamer), Mavis (protective realist), Junior (frustrated teenager) — and the inciting incident of Wendell’s return after ten years, arriving with his mixed-race daughter Lorna.'
conc2 = conc.replace(old_c33, new_c33)
assert_replaced(conc, conc2, "conclusion n33 four family members", "conclusion n33")
conc = conc2
record(PH_ID, d["title"], "conclusion n33: Wendell returning/Lorna named")
changed["conclusion_html"] = conc

# Fix flashcards
for i, fc in enumerate(cards):
    q = fc.get("q", "")
    a = fc.get("a", "")
    if "four family members introduced" in q.lower():
        cards[i] = {
            "q": "Who are at home at the play’s opening, and who arrives as the inciting incident?",
            "a": "Princess, Mavis and Junior are at home. Wendell (the hustler) returns after roughly ten years, arriving with his mixed-race daughter Lorna."
        }
        record(PH_ID, d["title"], "flashcard: family at start — Wendell absent; Lorna named")
    if "Wendell’s ‘hustle’" in q or "Wendell's 'hustle'" in q:
        cards[i] = {
            "q": "How does Odimba present Wendell’s ‘hustle’?",
            "a": "With compassion but complexity: his past included criminal activity driven by racist job discrimination after Jamaican military service; the boycott represents his move towards legitimate collective action."
        }
        record(PH_ID, d["title"], "flashcard: Wendell’s hustle — criminal past context")
    if "reclaim" in q.lower() and "hustler" in q.lower():
        cards[i] = {
            "q": "What double meaning does the word ‘hustler’ carry in the play?",
            "a": "Resourcefulness and refusal to accept defeat, but also acknowledgement of a criminal past caused by systemic racism — the boycott moves Wendell from one to the other."
        }
        record(PH_ID, d["title"], "flashcard: hustler double meaning corrected")
changed["flashcard_questions"] = cards

# Fix KCs
for i, kc in enumerate(kcs):
    q = kc.get("q", "")
    opts = kc.get("options", [])
    # Fix "Wendell is called the hustler because of his ambitious _____ and refusal to accept defeat"
    if "hustler" in q.lower() and "criminal" in str(opts).lower() and kc.get("type") == "fill":
        kcs[i] = {
            "q": "Wendell’s past hustle included _____ activity, driven by racist job discrimination after his Jamaican military service.",
            "type": "fill",
            "correct": 0,
            "options": ["criminal", "entrepreneurial", "violent", "political"]
        }
        record(PH_ID, d["title"], "KC: Wendell’s hustle — criminal activity driven by discrimination")
changed["knowledge_checks"] = kcs

push(PH_ID, changed)


# ─── WRITE LOG ────────────────────────────────────────────────────────────────
out_path = os.path.join(HERE, "_section_rewrite_log.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print(f"\n\nDONE. {len(log['lessons_modified'])} lessons updated. {len(log['fixes'])} fixes applied.")
print(f"Log written to: {out_path}")
print("\nLessons modified:")
for lid in log["lessons_modified"]:
    print(f"  {lid}")
