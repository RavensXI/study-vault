"""
Section rewrite for 5 lessons with clustered factual errors.
Does targeted find-and-replace on content_html + fixes flashcard/KC data.
Does NOT full-regen. Preserves narration IDs.
"""
import sys, os, json
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lib.supabase_client import get_client

sb = get_client()
log = {"lessons_modified": [], "fixes": []}

def record(lesson_id, title, fix_desc):
    log["fixes"].append({"lesson_id": lesson_id, "title": title, "fix": fix_desc})
    print(f"  [FIX] {fix_desc}")

def push(lesson_id, payload):
    sb.table("lessons").update(payload).eq("id", lesson_id).execute()
    if lesson_id not in log["lessons_modified"]:
        log["lessons_modified"].append(lesson_id)
    print(f"  -> Updated Supabase row {lesson_id}")


# ─── 1. CORAM BOY "PART 3" ────────────────────────────────────────────────────
print("\n=== 1. CORAM BOY: Part 3: Discovery & Resolution ===")
CB_ID = "26985264-3dc8-48c5-9799-288d4fb42679"
r = sb.table("lessons").select("id,title,content_html,conclusion_html,flashcard_questions,knowledge_checks").eq("id", CB_ID).single().execute()
d = r.data
html = d["content_html"]
conc = d["conclusion_html"]
cards = d["flashcard_questions"]
kcs = d["knowledge_checks"]

# Fix 1a: H2 "Meshak's Sacrifice" → rewrite the entire Meshak section (n7/n8) to correctly name Thomas Ledbury
old_meshak_h2 = '<h2 data-narration-id="n7">Meshak\'s Sacrifice</h2>'
new_meshak_h2 = '<h2 data-narration-id="n7">Thomas Ledbury\'s Sacrifice</h2>'
html = html.replace(old_meshak_h2, new_meshak_h2)
record(CB_ID, d["title"], "h2 n7: 'Meshak's Sacrifice' → 'Thomas Ledbury's Sacrifice'")

old_n8 = ('<p data-narration-id="n8">Meshak\'s story reaches its climax in Part 3 when he makes the ultimate '
          '<dfn class="term" data-def="Giving up something precious, often one\'s own life, for the sake of another.">sacrifice</dfn> '
          'to protect Aaron from Otis. Having defied his father once by saving the baby, Meshak now faces the consequences of '
          'that defiance. Otis, realising that Aaron\'s survival could expose his crimes, becomes a direct threat to the boy. '
          'Meshak places himself between Otis and Aaron, choosing to protect the child he saved even at the cost of his own life.</p>')
new_n8 = ('<p data-narration-id="n8">The novel\'s climax turns on a moment of devastating '
          '<dfn class="term" data-def="Giving up something precious, often one\'s own life, for the sake of another.">sacrifice</dfn> '
          '— but the hero who dies is not Meshak. It is Thomas Ledbury, Alexander\'s loyal childhood friend, who is shot and '
          'killed by Gaddarn (Otis) during the rescue of Aaron and Toby. Thomas comes to the waterfront to help free the boys, '
          'and Gavin uses his death to show that ordinary decency, not great wealth or social standing, is what defines true '
          'courage. Meshak, by contrast, survives the climax: having defied his father years earlier by saving the baby, he '
          'lives to see Aaron safe. In the Epilogue, Meshak dies peacefully of old age, his final thoughts resting on the child '
          'he once rescued. It is Thomas\'s death, not Meshak\'s, that constitutes the novel\'s act of physical sacrifice.</p>')
html = html.replace(old_n8, new_n8)
record(CB_ID, d["title"], "n8: corrected — Thomas Ledbury is shot by Gaddarn; Meshak dies peacefully in Epilogue")

# Fix 1b: Collapsible title "The Significance of Meshak's Death"
old_coll = '<span>The Significance of Meshak\'s Death</span>'
new_coll = '<span>The Significance of Thomas Ledbury\'s Death</span>'
html = html.replace(old_coll, new_coll)
record(CB_ID, d["title"], "Collapsible title: 'Meshak's Death' → 'Thomas Ledbury's Death'")

old_n9 = ('<p data-narration-id="n9">Meshak\'s death is the novel\'s most powerful moment. The character whom society would '
          'consider the least valuable — a man with a learning disability, the son of a criminal, someone with no status or '
          'wealth — turns out to be the most morally courageous person in the story. Gavin uses Meshak\'s sacrifice to make a '
          'devastating argument: that society\'s way of measuring human worth (by class, intelligence, wealth) is fundamentally '
          'wrong. Meshak\'s <dfn class="term" data-def="The quality of being willing to do what is right regardless of personal cost.">selflessness</dfn> '
          'contrasts sharply with every other character who has failed Aaron — from the mothers who handed babies to Otis, to '
          'the society that allowed child trafficking to flourish.</p>')
new_n9 = ('<p data-narration-id="n9">Thomas Ledbury\'s death is one of the novel\'s most powerful moments. He is not '
          'a grand or glamorous character — he is a reliable, loyal friend who acts when it matters most. Gavin uses his '
          'death to argue that moral courage is found in ordinary people, not in the wealthy or powerful who failed Aaron '
          'throughout his life. Yet Meshak\'s arc carries its own profound weight. The character whom society would consider '
          'the least valuable — a man with a learning disability, the son of a criminal — shows the deepest '
          '<dfn class="term" data-def="The quality of being willing to do what is right regardless of personal cost.">selflessness</dfn>: '
          'he saved Aaron as a baby at great personal risk, watched over him for years, and in the Epilogue dies peacefully '
          'knowing the boy is safe. Together, Thomas and Meshak represent Gavin\'s argument that human worth cannot be measured '
          'by class, intelligence, or social standing.</p>')
html = html.replace(old_n9, new_n9)
record(CB_ID, d["title"], "n9: corrected to reflect Thomas's sacrifice and Meshak's peaceful death in Epilogue")

# Fix 1c: Otis's fate — "exposed and punished" is wrong; he escapes, becomes Gaddarn, disappears overboard
old_n11 = ('<p data-narration-id="n11">The truth about Otis Gardiner\'s child-collecting scheme is finally brought to light. '
           'His years of <dfn class="term" data-def="The act of pretending to be legitimate while committing crimes, as Otis does by posing as a Coram man.">deception</dfn> '
           '— posing as a Coram man, taking money from desperate mothers, ordering the burial of babies — is exposed. '
           'Gavin does not give Otis a dramatic villain\'s downfall with speeches or spectacle. Instead, his exposure is almost '
           'bureaucratic, reinforcing the idea that his evil was always mundane and systematic rather than theatrical.</p>')
new_n11 = ('<p data-narration-id="n11">The truth about Otis Gardiner\'s child-collecting scheme is finally brought to light. '
           'His years of <dfn class="term" data-def="The act of pretending to be legitimate while committing crimes, as Otis does by posing as a Coram man.">deception</dfn> '
           '— posing as a Coram man, taking money from desperate mothers, ordering the burial of babies — are exposed. '
           'But Gavin deliberately refuses to give Otis a clean villain\'s justice. He had already escaped hanging earlier in the '
           'novel by bribing officials to hang another man in his place, then reinvented himself as the wealthy Philip Gaddarn. '
           'In the climactic boat scene, Gaddarn falls or disappears overboard during the chaos of the rescue — his ultimate '
           'fate is left deliberately ambiguous. This is not accident or oversight: Gavin\'s point is that the system which '
           'enabled Otis\'s crimes remains intact even after he is gone.</p>')
html = html.replace(old_n11, new_n11)
record(CB_ID, d["title"], "n11: corrected Otis's fate — escapes hanging via bribery, becomes Gaddarn, disappears overboard (ambiguous)")

# Fix 1d: n12 Key Fact about Otis's "quiet downfall"
old_n12_kf = ('<p>Otis\'s downfall mirrors the way his crimes were committed — without drama. Gavin makes a deliberate '
              'choice not to give the villain a grand ending, because the point is that real evil is often ordinary. The true '
              'drama belongs to Meshak\'s sacrifice and Aaron\'s reunion with his parents.</p>')
new_n12_kf = ('<p>Gavin deliberately withholds clean justice for Otis. He escapes the noose by having an innocent man hanged '
              'in his place, operates for years as Philip Gaddarn, and then vanishes into the water during the climax. His '
              'ultimate fate is unknown. Gavin\'s point is not that villainy always meets punishment, but that the social and '
              'economic systems that made Otis\'s crimes possible continue long after he is gone. The true drama of the '
              'resolution belongs to Thomas Ledbury\'s sacrifice and Aaron\'s reunion with his parents.</p>')
html = html.replace(old_n12_kf, new_n12_kf)
record(CB_ID, d["title"], "n12 key-fact: corrected Otis's escape, Gaddarn alias, disappears overboard")

# Fix 1e: n14 "Otis is exposed and punished"
old_n14 = ('<p data-narration-id="n14">The novel\'s ending offers a qualified sense of <dfn class="term" data-def="The final part of a narrative where conflicts are resolved and the story reaches a settled conclusion.">resolution</dfn>. '
           'Aaron is reunited with his birth parents. Otis is exposed and punished. The buried babies are acknowledged. '
           'But Gavin does not present this as an uncomplicated happy ending. Meshak is dead. The years Aaron spent without '
           'a family cannot be returned. The other babies Otis buried are gone forever. Justice comes, but it comes too late '
           'and at too high a cost.</p>')
new_n14 = ('<p data-narration-id="n14">The novel\'s ending offers a qualified sense of <dfn class="term" data-def="The final part of a narrative where conflicts are resolved and the story reaches a settled conclusion.">resolution</dfn>. '
           'Aaron is reunited with his birth parents. Otis\'s crimes are exposed and Thomas Ledbury gives his life in the rescue. '
           'The buried babies are finally acknowledged. But Gavin does not present this as an uncomplicated happy ending. Thomas '
           'is dead. Aaron must absorb the shattering truth about his origins. The years he spent without a family cannot be '
           'returned. The other babies Otis buried are gone forever. And Otis himself — now Gaddarn — disappears '
           'overboard, his fate unknown, the system that created him unchanged. Justice comes, but it is partial, costly, and incomplete.</p>')
html = html.replace(old_n14, new_n14)
record(CB_ID, d["title"], "n14: 'Otis is exposed and punished' → corrected; Thomas dies; Otis/Gaddarn disappears overboard")

# Fix 1f: n15 collapsible moral complexity — "Meshak's goodness saves a life but costs his own"
old_n15 = ('<p data-narration-id="n15">The ending asks the reader to hold two truths at once: that justice is possible, and '
           'that it is never complete. Aaron gains a family but has lost his foundling identity. Meshak\'s goodness saves a life '
           'but costs his own. Otis is punished but the system that enabled him — the class inequality, the lack of '
           'protection for vulnerable mothers and children — remains unchanged. Gavin refuses to offer simple comfort, '
           'instead leaving the reader to reflect on what real justice would look like in a society built on inequality.</p>')
new_n15 = ('<p data-narration-id="n15">The ending asks the reader to hold two truths at once: that justice is possible, and '
           'that it is never complete. Aaron gains a family but has lost his foundling identity. Thomas Ledbury\'s courage saves '
           'Aaron and Toby but costs him his life. Meshak survives to die peacefully in old age, his final peace a quiet form '
           'of redemption. Otis\'s crimes are exposed, but he slips away rather than facing justice, and the system that enabled '
           'him — the class inequality, the lack of protection for vulnerable mothers and children — remains unchanged. '
           'Gavin refuses to offer simple comfort, instead leaving the reader to reflect on what real justice would look like in '
           'a society built on inequality.</p>')
html = html.replace(old_n15, new_n15)
record(CB_ID, d["title"], "n15: 'Meshak's goodness saves a life but costs his own' → Thomas dies; Meshak dies peacefully")

# Fix 1g: conclusion bullet n21 "Meshak's sacrifice is the novel's emotional climax"
old_conc21 = ('<li data-narration-id="n21">Meshak\'s sacrifice is the novel\'s emotional climax — the character society '
              'values least proves to be the most morally courageous, challenging how we measure human worth.</li>')
new_conc21 = ('<li data-narration-id="n21">Thomas Ledbury\'s death in the rescue is the novel\'s act of physical sacrifice; '
              'Meshak\'s arc ends peacefully in the Epilogue — together they challenge how society measures human worth.</li>')
conc = conc.replace(old_conc21, new_conc21)
record(CB_ID, d["title"], "conclusion n21: corrected Meshak/Thomas distinction")

old_conc22 = ('<li data-narration-id="n22">The ending offers qualified justice: Aaron is reunited with his parents and Otis '
              'is exposed, but Meshak is dead, years are lost, and the system that enabled the crimes remains unchanged.</li>')
new_conc22 = ('<li data-narration-id="n22">The ending offers qualified justice: Aaron is reunited with his parents and '
              'Otis\'s crimes are exposed, but Thomas Ledbury is dead, years are lost, Otis/Gaddarn disappears without '
              'definitive punishment, and the system that enabled the crimes remains unchanged.</li>')
conc = conc.replace(old_conc22, new_conc22)
record(CB_ID, d["title"], "conclusion n22: corrected Thomas/Otis")

# Fix flashcards
for i, fc in enumerate(cards):
    if fc.get("q") == "How does Meshak die in the novel's climax?":
        cards[i] = {
            "q": "How does Thomas Ledbury die in the novel's climax?",
            "a": "He is shot and killed by Gaddarn (Otis) during the rescue of Aaron and Toby from the boat."
        }
        record(CB_ID, d["title"], "flashcard: 'How does Meshak die?' → corrected to Thomas Ledbury")
    if fc.get("q") == "Which character provides the novel's moral centre through self-sacrifice?":
        cards[i] = {
            "q": "Who makes the physical sacrifice in the novel's climax, and how does Meshak's arc end?",
            "a": "Thomas Ledbury is shot dead saving Aaron; Meshak survives to die peacefully of old age in the Epilogue."
        }
        record(CB_ID, d["title"], "flashcard: 'Meshak as moral centre' corrected to Thomas + Meshak epilogue")
    if fc.get("q") == "Why is the novel's ending described as morally complex, not simply happy?":
        cards[i] = {
            "q": "Why is the novel's ending described as morally complex, not simply happy?",
            "a": "Thomas dies; Otis/Gaddarn disappears overboard without definitive punishment; the unequal system remains intact."
        }
        record(CB_ID, d["title"], "flashcard: moral complexity — corrected Thomas death + Otis/Gaddarn fate")

# Fix knowledge checks
for i, kc in enumerate(kcs):
    if "Meshak makes the ultimate sacrifice" in str(kc.get("options", "")):
        for j, opt in enumerate(kc["options"]):
            if "Meshak makes the ultimate sacrifice" in opt:
                kcs[i]["options"][j] = "Thomas Ledbury is shot saving Aaron and Toby"
                record(CB_ID, d["title"], f"KC: option 'Meshak sacrifice' → 'Thomas Ledbury shot'")

push(CB_ID, {
    "content_html": html,
    "conclusion_html": conc,
    "flashcard_questions": cards,
    "knowledge_checks": kcs,
})


# ─── 2. JANE EYRE: GATESHEAD & LOWOOD ────────────────────────────────────────
print("\n=== 2. JANE EYRE (AQA): Gateshead & Lowood ===")
JE_ID = "2fe05d71-6399-483a-a753-1bdbda1322ed"
r = sb.table("lessons").select("id,title,content_html,glossary_terms,flashcard_questions,knowledge_checks").eq("id", JE_ID).single().execute()
d = r.data
html = d["content_html"]
gloss = d["glossary_terms"]
cards = d["flashcard_questions"]
kcs = d["knowledge_checks"]

# Fix 2a: dfn tooltip for typhus says "often called 'consumption'" — completely wrong
old_typhus_dfn = ('<dfn class="term" data-def="An infectious disease, often called \'consumption,\' that was a major killer '
                  'in Victorian Britain, especially among the poor and malnourished.">typhus</dfn>')
new_typhus_dfn = ('<dfn class="term" data-def="An acute infectious disease spread by lice and fleas, distinct from '
                  'consumption (tuberculosis). Typhus caused deadly outbreaks in overcrowded institutions like Lowood.">typhus</dfn>')
html = html.replace(old_typhus_dfn, new_typhus_dfn)
record(JE_ID, d["title"], "dfn tooltip: typhus no longer called 'consumption' — corrected to separate disease")

# Fix 2b: n11 text — Helen Burns killed by typhus + internal contradiction with Brontë's sisters
old_n11 = ('<p data-narration-id="n11">Conditions at Lowood are appalling. The food is so poor that the girls are '
           'constantly hungry. In spring, a <dfn class="term" data-def="An infectious disease spread by lice and fleas, '
           'distinct from consumption (tuberculosis). Typhus caused deadly outbreaks in overcrowded institutions like Lowood.">'
           'typhus</dfn> epidemic sweeps through the school, killing many students — including Jane\'s closest friend, '
           'Helen Burns. Brontë based these scenes on her own experience at the Clergy Daughters\' School, where her '
           'sisters Maria and Elizabeth contracted tuberculosis and died.</p>')
new_n11 = ('<p data-narration-id="n11">Conditions at Lowood are appalling. The food is so poor that the girls are constantly '
           'hungry. In spring, a <dfn class="term" data-def="An acute infectious disease spread by lice and fleas, distinct '
           'from consumption (tuberculosis). Typhus caused deadly outbreaks in overcrowded institutions like Lowood.">'
           'typhus</dfn> epidemic sweeps through the school, killing many students. Jane\'s closest friend Helen Burns, '
           'however, does not die of typhus — she has been quietly dying of consumption (tuberculosis) throughout her time '
           'at Lowood. In Chapter 9, Jane steals away to Miss Temple\'s room to be with Helen and wakes to find she has died '
           'with Jane\'s arms around her neck. Brontë based these scenes on her own experience at the Clergy Daughters\' '
           'School at Cowan Bridge, where her sisters Maria and Elizabeth contracted tuberculosis. They were removed from the '
           'school and died at home in Haworth, their illness worsened by the school\'s harsh conditions — the same '
           'disease that takes Helen Burns in the novel.</p>')
html = html.replace(old_n11, new_n11)
record(JE_ID, d["title"], "n11: Helen Burns dies of consumption (Ch.9), NOT typhus; Brontë sisters context corrected")

# Fix glossary term for typhus
for i, g in enumerate(gloss):
    if g.get("term") == "typhus":
        gloss[i] = {
            "term": "typhus",
            "definition": "An acute infectious disease spread by lice and fleas. Distinct from consumption (tuberculosis) — typhus kills many Lowood students in spring, but Helen Burns dies separately of her pre-existing consumption in Chapter 9."
        }
        record(JE_ID, d["title"], "glossary: typhus definition corrected — no longer called 'consumption'")

# Fix flashcard that says typhus killed Helen Burns
for i, fc in enumerate(cards):
    if fc.get("q") == "What epidemic sweeps Lowood in spring?":
        cards[i] = {
            "q": "What epidemic sweeps Lowood in spring, and how does Helen Burns actually die?",
            "a": "A typhus epidemic kills many Lowood students, but Helen Burns dies separately of consumption (TB) in Chapter 9 — Jane holds her in her arms."
        }
        record(JE_ID, d["title"], "flashcard: typhus/Helen Burns question corrected")

# Fix any KC that names Helen Burns as typhus victim
for i, kc in enumerate(kcs):
    opts = kc.get("options", [])
    for j, opt in enumerate(opts):
        if "typhus" in str(opt).lower() and "Helen" in str(opt):
            kcs[i]["options"][j] = opt.replace(
                "typhus", "consumption (TB)"
            ).replace("Typhus", "Consumption (TB)")
            record(JE_ID, d["title"], f"KC option: typhus → consumption for Helen Burns")

push(JE_ID, {
    "content_html": html,
    "glossary_terms": gloss,
    "flashcard_questions": cards,
    "knowledge_checks": kcs,
})


# ─── 3. JOURNEY'S END: ACT 1 ─────────────────────────────────────────────────
print("\n=== 3. JOURNEY'S END (Edexcel): Act 1: Arrival in the Trenches ===")
JE2_ID = "c25f6db3-84f3-436c-bfbc-cf5a1fdc57e5"
r = sb.table("lessons").select("id,title,content_html,flashcard_questions,knowledge_checks").eq("id", JE2_ID).single().execute()
d = r.data
html = d["content_html"]
cards = d["flashcard_questions"]
kcs = d["knowledge_checks"]

# Fix 3a: n7 — fabricated quote "It's the only way to forget"; replace with real Act 1 line
old_n7 = ('<p data-narration-id="n7">When Stanhope finally appears, he is tense, irritable, and immediately reaches for '
          'the whisky. His line "It\'s the only way to forget" is one of the play\'s most important. It tells us that Stanhope '
          'is self-aware — he knows he is damaged — but has no other way to cope. The whisky is not a luxury; it is '
          'survival. Sherriff is showing that the war has pushed this young man beyond his limits, and alcohol is the only '
          'thing holding him together.</p>')
new_n7 = ('<p data-narration-id="n7">When Stanhope finally appears, he is tense, irritable, and immediately reaches for '
          'the whisky. His key Act 1 line captures the desperate necessity of the habit: "She doesn\'t know that if I went '
          'up those steps into the front line — without being doped with whiskey — I\'d go mad with fright." This '
          'tells us that Stanhope is self-aware — he knows he is damaged — but sees alcohol as his only means of '
          'functioning. The whisky is not a luxury; it is survival. Sherriff shows that the war has pushed this young man '
          'beyond his limits, and the prospect of facing the front line sober is, for Stanhope, unthinkable.</p>')
html = html.replace(old_n7, new_n7)
record(JE2_ID, d["title"], "n7: fabricated 'It's the only way to forget' → replaced with real Act 1 line (whisky / mad with fright)")

# Fix 3b: n8 — "You think there's no limit to what a man can bear?" is Act 3 S2, not Act 1
old_n8 = ('<p data-narration-id="n8">Stanhope\'s reaction to Raleigh\'s arrival is not pleasure but <dfn class="term" '
          'data-def="A feeling of intense worry or unease, often about an imminent event or something with an uncertain outcome.">'
          'anxiety</dfn>. He is terrified that Raleigh will write home and tell his sister — Stanhope\'s fiancée, '
          'Madge — about his drinking and deterioration. He says to Osborne: "You think there\'s no limit to what a man '
          'can bear?" This line reveals the immense pressure Stanhope is under. He has maintained a facade of competence for '
          'three years, and Raleigh\'s innocent admiration threatens to expose the truth.</p>')
new_n8 = ('<p data-narration-id="n8">Stanhope\'s reaction to Raleigh\'s arrival is not pleasure but <dfn class="term" '
          'data-def="A feeling of intense worry or unease, often about an imminent event or something with an uncertain outcome.">'
          'anxiety</dfn>. He is terrified that Raleigh will write home and tell his sister — Stanhope\'s fiancée, '
          'Madge — about his drinking and deterioration. He confides his fear to Osborne, revealing how precarious his '
          'grip on composure has become. He has maintained a facade of competence for three years, and Raleigh\'s innocent '
          'admiration threatens to expose the truth. Note: Stanhope\'s explosive outburst "To forget, you little fool — '
          'to forget! … You think there\'s no limit to what a man can bear?" belongs to Act 3 Scene 2, after Osborne\'s '
          'death — not Act 1.</p>')
html = html.replace(old_n8, new_n8)
record(JE2_ID, d["title"], "n8: 'You think there's no limit...' relocated to Act 3 S2 attribution note, not presented as Act 1 line")

# Fix 3c: n13 Key Fact — "the one man I could talk to as a friend" misattributed to Raleigh about Stanhope
old_n13 = ('<div class="key-fact" data-narration-id="n13" data-revision-tip="Cover this and explain: what does Raleigh '
           'remember about Stanhope, and why does Stanhope see Raleigh as a threat?">\n  <div class="key-fact-label">Key Fact</div>\n'
           '  <p>Raleigh remembers Stanhope as a school hero — "the one man I could talk to as a friend." Stanhope sees '
           'Raleigh as a threat who might expose his deterioration. This contrast between past innocence and present damage '
           'drives the play\'s emotional core.</p>\n</div>')
new_n13 = ('<div class="key-fact" data-narration-id="n13" data-revision-tip="Cover this and explain: how does Raleigh describe '
           'Stanhope, and what do we learn about Stanhope\'s friendship with Osborne?">\n  <div class="key-fact-label">Key Fact</div>\n'
           '  <p>Raleigh hero-worships Stanhope from school: in his letter home, he calls him "the finest officer in the '
           'battalion — the men simply love him." Meanwhile, Stanhope\'s closest confidant is Osborne — it is '
           'Stanhope who, in Act 3 Scene 2 (after Osborne\'s death), cries out "the one man I could trust — my best '
           'friend — the one man I could talk to as man to man — who understood everything." These are two separate '
           'quotes by different characters in different acts. Stanhope sees Raleigh as a threat who might expose his '
           'deterioration — a contrast between past innocence and present damage that drives the play\'s emotional core.</p>\n</div>')
html = html.replace(old_n13, new_n13)
record(JE2_ID, d["title"], "n13 key-fact: 'the one man I could talk to as a friend' correctly attributed to Stanhope about Osborne (Act 3 S2)")

# Fix flashcards
for i, fc in enumerate(cards):
    if fc.get("q") == "Which Stanhope line justifies his drinking?":
        cards[i] = {
            "q": "Which Stanhope line from Act 1 justifies his drinking?",
            "a": "\"She doesn't know that if I went up those steps into the front line — without being doped with whiskey — I'd go mad with fright.\""
        }
        record(JE2_ID, d["title"], "flashcard: fabricated 'It's the only way to forget' → real Act 1 whisky line")
    if fc.get("q") == "Which Stanhope question to Osborne reveals his breaking point?":
        cards[i] = {
            "q": "In which act does Stanhope say 'To forget, you little fool — to forget! You think there's no limit to what a man can bear?'",
            "a": "Act 3 Scene 2 — after Osborne's death, addressed to Raleigh who refuses to eat at the celebration dinner. Not Act 1."
        }
        record(JE2_ID, d["title"], "flashcard: 'no limit to what a man can bear' correctly placed in Act 3 S2")
    if fc.get("q") == "How does Raleigh remember Stanhope from school?":
        cards[i] = {
            "q": "How does Raleigh describe Stanhope in his letter home?",
            "a": "\"The finest officer in the battalion — the men simply love him.\""
        }
        record(JE2_ID, d["title"], "flashcard: Raleigh's description corrected; misattributed 'one man I could talk to as a friend' removed")

# Fix knowledge checks
for i, kc in enumerate(kcs):
    # Fix "It's the only way to forget" fill-in
    if kc.get("type") == "fill" and "the only way to" in str(kc.get("q", "")):
        kcs[i] = {
            "q": "Stanhope says without whisky he would go _____ with fright if he went up into the front line.",
            "type": "fill",
            "correct": 2,
            "options": ["wild", "numb", "mad", "sick"]
        }
        record(JE2_ID, d["title"], "KC fill-in: 'the only way to forget' → correct Act 1 quote (mad with fright)")
    # Fix "the one man I could talk to as a friend" fill-in
    if kc.get("type") == "fill" and "one man I could talk to" in str(kc.get("q", "")):
        kcs[i] = {
            "q": "Stanhope says about Osborne in Act 3 Scene 2: 'the one man I could trust — my best _____ — the one man I could talk to as man to man.'",
            "type": "fill",
            "correct": 0,
            "options": ["friend", "captain", "soldier", "brother"]
        }
        record(JE2_ID, d["title"], "KC fill-in: corrected attribution — Stanhope about Osborne in Act 3 S2")

push(JE2_ID, {
    "content_html": html,
    "flashcard_questions": cards,
    "knowledge_checks": kcs,
})


# ─── 4. PIGEON ENGLISH: THE ENDING ───────────────────────────────────────────
print("\n=== 4. PIGEON ENGLISH (AQA): The Ending ===")
PE_ID = "39adc443-d361-4e63-8deb-72a86a0e1568"
r = sb.table("lessons").select("id,title,content_html,flashcard_questions,knowledge_checks").eq("id", PE_ID).single().execute()
d = r.data
html = d["content_html"]
cards = d["flashcard_questions"]
kcs = d["knowledge_checks"]

# Fix 4a: n3 — killer is Jordan, not "the Dell Farm Crew"
old_n3 = ('<p data-narration-id="n3">Harri is stabbed while running from the Dell Farm Crew. His investigation has brought '
          'him too close to the truth, and the gang silences him in the most direct way possible. Kelman describes the attack '
          'from Harri\'s perspective: the confusion, the pain, the failure to understand what is happening. Even in his final '
          'moments, Harri\'s innocence persists — he does not fully comprehend that he is dying.</p>')
new_n3 = ('<p data-narration-id="n3">Harri is stabbed in the stairwell by Jordan — a boy from the estate who kills him '
          'with a "war knife." The motive is not simply the investigation: Jordan\'s act is rooted in the dispute over Auntie '
          'Sonia\'s remote-control car and the ban Mamma placed on their friendship. Kelman describes the attack from Harri\'s '
          'perspective: the confusion, the pain, the failure to understand what is happening. Even in his final moments, '
          'Harri\'s innocence persists — he does not fully comprehend that he is dying.</p>')
html = html.replace(old_n3, new_n3)
record(PE_ID, d["title"], "n3: killer is Jordan (stairwell, war knife), not 'the Dell Farm Crew' collectively")

# Fix 4b: n4 Key Fact — same error
old_n4_kf = ('<p>Harri is killed by the Dell Farm Crew because his investigation brought him too close to the truth about '
             'the original murder. Kelman narrates the death from Harri\'s confused, innocent perspective — he does not '
             'fully understand what is happening to him. This choice makes the ending unbearably poignant: the reader understands '
             'the full horror that Harri cannot.</p>')
new_n4_kf = ('<p>Harri is killed by Jordan in the stairwell — not the Dell Farm Crew collectively. The immediate trigger '
             'is a personal dispute (the remote-control car, Mamma banning the friendship), though Harri\'s investigation into '
             'the estate murder has drawn dangerous attention to him. Kelman narrates the death from Harri\'s confused, innocent '
             'perspective — he does not fully understand what is happening to him. This choice makes the ending unbearably '
             'poignant: the reader understands the full horror that Harri cannot.</p>')
html = html.replace(old_n4_kf, new_n4_kf)
record(PE_ID, d["title"], "n4 key-fact: killer is Jordan (personal dispute), not the Dell Farm Crew")

# Fix 4c: n8 Damilola Taylor — "stabbed to death" → broken glass / femoral artery
old_damilola = ('<p data-narration-id="n8">The ending deliberately echoes Damilola Taylor\'s death. Like Damilola, Harri '
                'is a young immigrant boy killed on a council estate. Like Damilola, his death is the result of gang violence '
                'targeting a vulnerable child. Kelman wrote the novel eleven years after Damilola\'s murder, and the ending '
                'forces the reader to confront an uncomfortable truth: in those eleven years, nothing fundamental changed. '
                'Children are still dying in the same circumstances.</p>')
new_damilola = ('<p data-narration-id="n8">The ending deliberately echoes the death of Damilola Taylor, a ten-year-old '
                'Nigerian boy who died in November 2000 on a Peckham estate after being attacked with a broken glass bottle '
                '— a shard severed his femoral artery and he bled to death. Like Damilola, Harri is a young immigrant '
                'boy killed on a council estate, his death the result of violence that institutions failed to prevent. Kelman '
                'wrote the novel eleven years after Damilola\'s death, and the ending forces the reader to confront an '
                'uncomfortable truth: in those eleven years, nothing fundamental changed. Children are still dying in the '
                'same circumstances.</p>')
html = html.replace(old_damilola, new_damilola)
record(PE_ID, d["title"], "n8: Damilola Taylor death — 'stabbed' → broken glass / severed femoral artery (bled to death)")

# Fix flashcard Q1 — killer is Jordan not Dell Farm Crew
for i, fc in enumerate(cards):
    if fc.get("q") == "How does Harri die in Pigeon English?":
        cards[i] = {
            "q": "How does Harri die in Pigeon English?",
            "a": "Stabbed in the stairwell by Jordan with a war knife — a personal dispute, though linked to Harri's dangerous investigation."
        }
        record(PE_ID, d["title"], "flashcard: 'Stabbed by the Dell Farm Crew' → 'stabbed by Jordan'")

# Fix KCs — the "correct" reason for death is "investigation" but the who-did-it needs accuracy
for i, kc in enumerate(kcs):
    if kc.get("q") == "Why is Harri killed?":
        # Current correct option (1) says "investigation brings him close to truth" — acceptable but add Jordan note
        # The existing correct=1 option already partially fits; just update the actual wording of option 1
        kcs[i]["options"][1] = "He is stabbed by Jordan in a personal dispute that intersects with his investigation"
        record(PE_ID, d["title"], "KC: correct answer updated — Jordan stabs Harri, not 'Dell Farm Crew' gang")

# Fix conclusion bullets
conc_html = r.data.get("conclusion_html", "") if "conclusion_html" in r.data else ""
# We didn't fetch conclusion_html in this call, need to get it
r2 = sb.table("lessons").select("conclusion_html").eq("id", PE_ID).single().execute()
conc = r2.data["conclusion_html"]
old_conc18 = ('<li data-narration-id="n18">Harri is killed because his investigation brought him too close to the truth '
              '— Kelman narrates the death from Harri\'s confused, innocent perspective to maximise the reader\'s horror.</li>')
new_conc18 = ('<li data-narration-id="n18">Harri is killed by Jordan in the stairwell — Kelman narrates the death from '
              'Harri\'s confused, innocent perspective to maximise the reader\'s horror.</li>')
conc = conc.replace(old_conc18, new_conc18)
record(PE_ID, d["title"], "conclusion n18: corrected killer to Jordan")

push(PE_ID, {
    "content_html": html,
    "conclusion_html": conc,
    "flashcard_questions": cards,
    "knowledge_checks": kcs,
})

# Also fix the 'hutious' meaning in Pigeon English "Harri's World" (lesson 2) and "Character Analysis" / "Key Themes"
# Lesson 2: Harri's World — 9abb3b24
print("\n=== 4b. PIGEON ENGLISH: Harri's World (hutious fix) ===")
PE2_ID = "9abb3b24-d5be-4a40-8fd8-7a44b8f14dd1"
r = sb.table("lessons").select("id,title,content_html,flashcard_questions,knowledge_checks,conclusion_html").eq("id", PE2_ID).single().execute()
d = r.data
html2 = d["content_html"]
cards2 = d["flashcard_questions"]
conc2 = d["conclusion_html"]

# Fix n2: '"hutious" for something brilliant' → 'hutious' means scary/frightening
old_n2_pe2 = ('He marvels at escalators, is fascinated by pigeons, and creates his own ranking system ("hutious" for '
              'something brilliant, "bo-styles" for cool).')
new_n2_pe2 = ('He marvels at escalators, is fascinated by pigeons, and creates his own vocabulary to describe his world '
              '("hutious" for something scary or frightening, "bo-styles" for cool).')
html2 = html2.replace(old_n2_pe2, new_n2_pe2)
record(PE2_ID, d["title"], "n2: 'hutious = brilliant' → 'hutious = scary/frightening'")

# Fix flashcard Q4: 'hutious' means 'brilliant'
for i, fc in enumerate(cards2):
    if "hutious" in fc.get("q", "") and "brilliant" in fc.get("a", ""):
        cards2[i] = {
            "q": fc["q"],
            "a": "'Hutious' means scary or frightening."
        }
        record(PE2_ID, d["title"], "flashcard: 'hutious = brilliant' → 'hutious = scary/frightening'")
    if "hutious" in fc.get("a", "") and "brilliant" in fc.get("a", ""):
        cards2[i]["a"] = cards2[i]["a"].replace("brilliant", "scary/frightening")
        record(PE2_ID, d["title"], "flashcard: hutious answer corrected in combined slang flashcard")

push(PE2_ID, {
    "content_html": html2,
    "flashcard_questions": cards2,
})

# Lesson 6: Character Analysis — aad20898 (hutious in n2 and flashcard)
print("\n=== 4c. PIGEON ENGLISH: Character Analysis (hutious fix) ===")
PE3_ID = "aad20898-d4c7-4b15-9ed3-a431d3d2499c"
r = sb.table("lessons").select("id,title,content_html,flashcard_questions").eq("id", PE3_ID).single().execute()
d = r.data
html3 = d["content_html"]
cards3 = d["flashcard_questions"]

old_n2_pe3 = ('mixes Ghanaian English, London playground slang, and his own invented words ("hutious," "bo-styles," '
              '"asweh"). His voice is warm')
new_n2_pe3 = ('mixes Ghanaian English, London playground slang, and his own invented words ("hutious" for scary/frightening, '
              '"bo-styles" for cool, "asweh" as an oath). His voice is warm')
html3 = html3.replace(old_n2_pe3, new_n2_pe3)
record(PE3_ID, d["title"], "n2: hutious listed without meaning — now glossed as scary/frightening")

# Fix flashcard "'Hutious' (brilliant) and 'bo-styles' (cool)"
for i, fc in enumerate(cards3):
    if "hutious" in fc.get("a","").lower() and "brilliant" in fc.get("a","").lower():
        cards3[i]["a"] = cards3[i]["a"].replace("'Hutious' (brilliant)", "'Hutious' (scary/frightening)")
        record(PE3_ID, d["title"], "flashcard: 'Hutious (brilliant)' → 'Hutious (scary/frightening)'")

push(PE3_ID, {
    "content_html": html3,
    "flashcard_questions": cards3,
})


# ─── 5. PRINCESS & THE HUSTLER: ACT 1 ────────────────────────────────────────
print("\n=== 5. PRINCESS & THE HUSTLER (AQA): Act 1: The Family & the Dream ===")
PH_ID = "263021cb-1ef8-4ff0-a975-2049493a0bba"
r = sb.table("lessons").select("id,title,content_html,conclusion_html,flashcard_questions,knowledge_checks").eq("id", PH_ID).single().execute()
d = r.data
html = d["content_html"]
conc = d["conclusion_html"]
cards = d["flashcard_questions"]
kcs = d["knowledge_checks"]

# Fix 5a: n2 — Wendell NOT present at the start; his return is the inciting incident
old_n2_ph = ('<p data-narration-id="n2"><em>Princess &amp; The Hustler</em> opens with a sense of energy and warmth. '
             'We meet Princess, a ten-year-old girl with a vivid imagination and an unshakeable optimism. She lives in '
             'St Pauls, Bristol, with her mother <dfn class="term" data-def="Princess\'s mother, a protective and hardworking '
             'Jamaican woman who prioritises her children\'s safety and future.">Mavis</dfn>, her father <dfn class="term" '
             'data-def="Princess\'s father, known as \'the hustler\' for his ambitious schemes and dreams of business success.">'
             'Wendell</dfn>, and her older brother <dfn class="term" data-def="Princess\'s older brother, a teenager '
             'navigating questions of identity and belonging in 1960s Bristol.">Junior</dfn>. From the first scene, Odimba '
             'establishes this as a family held together by love but tested by the world outside their door.</p>')
new_n2_ph = ('<p data-narration-id="n2"><em>Princess &amp; The Hustler</em> opens with a sense of energy and warmth. We '
             'meet Princess, a ten-year-old girl with a vivid imagination and an unshakeable optimism. The play is set during '
             'the Bristol Bus Boycott of 1963. At the opening, Princess lives in St Pauls with her mother '
             '<dfn class="term" data-def="Princess\'s mother, a protective and hardworking Jamaican woman who prioritises her '
             'children\'s safety and future.">Mavis</dfn> and her older brother <dfn class="term" data-def="Princess\'s older '
             'brother, a teenager navigating questions of identity and belonging in 1960s Bristol.">Junior</dfn>. Her father '
             '<dfn class="term" data-def="Princess\'s father, known as \'the hustler\' — absent for approximately ten '
             'years at the play\'s opening, whose unexpected return is the inciting incident of Act 1.">Wendell</dfn> has been '
             'absent for roughly a decade. His unexpected return partway through Act 1 is the catalyst for the play\'s central '
             'conflict: he arrives with <dfn class="term" data-def="Wendell\'s mixed-race half-daughter by another woman, '
             'approximately one year younger than Princess, whose identity is a central theme of the play.">Lorna</dfn>, '
             'his mixed-race daughter by another woman. Mavis initially refuses to have Wendell in the house but accepts Lorna '
             '— and Princess and Lorna quickly form a bond that becomes central to the play\'s identity theme.</p>')
html = html.replace(old_n2_ph, new_n2_ph)
record(PH_ID, d["title"], "n2: Wendell absent at play's start; his return + Lorna's introduction is the inciting incident; Bristol Bus Boycott 1963 named")

# Fix 5b: n12 — "His hustle is not criminal" → his past DID include crime (driven there by discrimination)
old_n12_ph = ('<p data-narration-id="n12">Wendell is the play\'s title character — "the hustler." He is charismatic, '
              'ambitious, and full of ideas for making money and building a better life. His <dfn class="term" data-def="'
              'Ambitious plans or schemes, often involving risk, aimed at achieving financial success or social advancement.">'
              'hustle</dfn> is not criminal; it is the entrepreneurial drive of a man locked out of legitimate employment by '
              'racism. If the bus company won\'t hire him, he\'ll make his own way.</p>')
new_n12_ph = ('<p data-narration-id="n12">Wendell is the play\'s title character — "the hustler." He is charismatic, '
              'ambitious, and full of energy. His <dfn class="term" data-def="Ambitious plans or schemes, often involving '
              'risk. For Wendell, hustle included a criminal past driven by the racist denial of legitimate work.">hustle</dfn> '
              'has a darker history than it first appears: Mavis reveals in Act 2 that after Jamaican military service, '
              'Wendell was promised a decent job in England but given a much lower position. The systematic discrimination '
              'he faced pushed him towards criminal activity — a fact Odimba presents as a systemic failure, not a '
              'personal moral choice. The boycott represents Wendell\'s attempt to move from individual criminality driven '
              'by exclusion to collective legitimate action.</p>')
html = html.replace(old_n12_ph, new_n12_ph)
record(PH_ID, d["title"], "n12: corrected — Wendell's hustle DID include criminal past (driven by racist job discrimination)")

# Fix 5c: n13 — "his ambition is a response to exclusion, not recklessness" is partly fine but the hustle-as-purely-legitimate framing needs adjusting
old_n13_ph = ('<p data-narration-id="n13">Yet Wendell\'s dreams also create tension. His schemes don\'t always work out, '
              'and Mavis worries about financial stability. Odimba presents him sympathetically — his ambition is a '
              '<em>response</em> to exclusion, not recklessness. The audience understands that in a fair society, Wendell\'s '
              'energy and intelligence would find legitimate outlets. The system\'s failure to offer him opportunity is the '
              'real problem.</p>')
new_n13_ph = ('<p data-narration-id="n13">Yet Wendell\'s return creates immediate tension — and not just because he '
              'arrives with Lorna. Mavis knows the truth of his past, and the audience gradually learns it too. Odimba '
              'presents his criminal history with compassion rather than condemnation: his ambition is a <em>response</em> '
              'to exclusion, and his involvement in the Bristol Bus Boycott represents genuine transformation. The system\'s '
              'failure to offer him legitimate opportunity is the root cause — but Odimba does not pretend his past '
              'choices carried no cost.</p>')
html = html.replace(old_n13_ph, new_n13_ph)
record(PH_ID, d["title"], "n13: Wendell's return tension includes Lorna; criminal past acknowledged with compassion")

# Fix 5d: n14 Key Fact — reclaimed "hustler" framing needs nuancing
old_n14_ph = ('<div class="key-fact" data-revision-tip="Close this and recall: how does Odimba reclaim the word \'hustler\' '
              'in this play? What does it represent instead of dishonesty?" data-narration-id="n14">\n  '
              '<div class="key-fact-label">Key Fact</div>\n  <p>The word "hustler" is reclaimed in this play. Rather than '
              'suggesting dishonesty, it represents resourcefulness and refusal to accept defeat — a survival strategy '
              'in a society that denies you legitimate opportunity.</p>\n</div>')
new_n14_ph = ('<div class="key-fact" data-revision-tip="Close this and recall: how does Odimba present the word \'hustler\' '
              'in this play? What does it represent, and what complicates a purely positive reading?" data-narration-id="n14">\n  '
              '<div class="key-fact-label">Key Fact</div>\n  <p>The word "hustler" carries a double meaning in the play. It '
              'represents resourcefulness and refusal to accept defeat — a survival strategy in a society that denies '
              'legitimate opportunity. But it also acknowledges that Wendell\'s past included criminal activity, driven there '
              'by racist exclusion after his Jamaican military service. Odimba does not simply redeem the word; she insists '
              'we understand the systemic causes behind it.</p>\n</div>')
html = html.replace(old_n14_ph, new_n14_ph)
record(PH_ID, d["title"], "n14 key-fact: 'hustler' framing nuanced — acknowledges criminal past with systemic cause")

# Fix 5e: n33 conclusion — "Wendell (father, the hustler)" should note he's returning, not present from start
old_conc33 = ('<li data-narration-id="n33">Act 1 introduces the family: Princess (optimistic dreamer), Mavis (protective '
              'realist), Wendell (ambitious hustler), and Junior (frustrated teenager).</li>')
new_conc33 = ('<li data-narration-id="n33">Act 1 introduces the family: Princess (optimistic dreamer), Mavis (protective '
              'realist), Junior (frustrated teenager) — and the inciting incident of Wendell\'s return after ten years, '
              'arriving with his mixed-race daughter Lorna.</li>')
conc = conc.replace(old_conc33, new_conc33)
record(PH_ID, d["title"], "conclusion n33: Wendell framed as returning, not present from start; Lorna named")

# Fix flashcards
for i, fc in enumerate(cards):
    if fc.get("q") == "Who are the four family members introduced in Act 1?":
        cards[i] = {
            "q": "Who are the family members at the start of the play, and who arrives as the inciting incident?",
            "a": "Princess, Mavis and Junior are at home at the play's opening. Wendell (the hustler) returns after roughly ten years, arriving with his mixed-race daughter Lorna."
        }
        record(PH_ID, d["title"], "flashcard: family at start — Wendell absent until return; Lorna named")
    if fc.get("q") == "How does Odimba present Wendell's 'hustle'?":
        cards[i] = {
            "q": "How does Odimba present Wendell's 'hustle'?",
            "a": "With compassion but complexity: his past included criminal activity driven by racist job discrimination after Jamaican military service; the boycott represents his move towards legitimate collective action."
        }
        record(PH_ID, d["title"], "flashcard: Wendell's hustle — corrected to include criminal past context")
    if fc.get("q") == "How does Odimba reclaim the word 'hustler' in this play?":
        cards[i] = {
            "q": "What double meaning does the word 'hustler' carry in the play?",
            "a": "Resourcefulness and refusal to accept defeat, but also acknowledgement of a criminal past caused by systemic racism — the boycott moves Wendell from one to the other."
        }
        record(PH_ID, d["title"], "flashcard: 'hustler' double meaning — resourcefulness + criminal past context")

# Fix KCs
for i, kc in enumerate(kcs):
    if "schemes" in str(kc.get("options", "")) and "criminal" in str(kc.get("options", "")):
        # Fix the fill-in about Wendell's hustle
        for j, opt in enumerate(kc.get("options", [])):
            if opt == "criminal activity":
                # this was the wrong option before, now it's actually partly true — update correct pointer and options
                kcs[i]["correct"] = j  # criminal activity IS part of it
                kcs[i]["q"] = "Wendell's past hustle included _____ activity, driven by racist discrimination after Jamaican military service."
                record(PH_ID, d["title"], "KC: Wendell's hustle fill-in corrected — criminal activity driven by discrimination")
                break
    if kc.get("type") == "match" and "Wendell" in str(kc.get("left", "")):
        for j, left in enumerate(kc.get("left", [])):
            if left == "Wendell" or left == "Princess":
                pass  # match structure is fine — character roles are still correct in broad strokes
    # Fix "Mavis passes on _____ heritage" — this is fine as-is

push(PH_ID, {
    "content_html": html,
    "conclusion_html": conc,
    "flashcard_questions": cards,
    "knowledge_checks": kcs,
})


# ─── WRITE LOG ────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_section_rewrite_log.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print(f"\n\nDONE. {len(log['lessons_modified'])} lessons updated. {len(log['fixes'])} fixes applied.")
print(f"Log written to: {out_path}")
print("\nLessons modified:")
for lid in log["lessons_modified"]:
    print(f"  {lid}")
