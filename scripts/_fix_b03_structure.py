"""
Fix structural issues in b03 lesson files:
1. Flashcard enumerations - split or rephrase answers
2. Flashcard questions too short
3. Add second key-fact div to lessons that only have 1
4. Add more glossary entries where needed
"""
import json

# ---- Lesson 1: physical-emotional-and-social-wellbeing ----
# FC[0] 'Physical, emotional and social wellbeing.' - enumeration
# Fix: rephrase the question to make a non-enumeration answer
def fix_l01():
    path = 'scripts/_content_physical-education-edexcel/lessons/physical-emotional-and-social-wellbeing.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    fc = data['flashcard_questions']
    # FC[0] was "What are the three dimensions of health?" -> "Physical, emotional and social wellbeing."
    # Replace with two cards
    fc[0] = {"q": "What is meant by 'physical health'?", "a": "The condition of the body, its function and freedom from disease or injury."}
    fc.insert(1, {"q": "What is meant by 'emotional health'?", "a": "The ability to manage feelings and respond constructively to stress."})
    # cap at 15 cards
    data['flashcard_questions'] = fc[:15]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L01 flashcards')

# ---- Lesson 2: lifestyle-choices-and-sedentary-living ----
# FC[4] enumeration "It impairs reaction time, coordination and balance."
# FC[5] short q: "Define 'sedentary lifestyle'."
# FC[6] enumeration "Coronary heart disease, obesity and osteoporosis."
def fix_l02():
    path = 'scripts/_content_physical-education-edexcel/lessons/lifestyle-choices-and-sedentary-living.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    fc = data['flashcard_questions']
    # Fix FC[4] - split into one card about reaction time
    fc[4] = {"q": "How does alcohol affect reaction time in sport?", "a": "It slows the central nervous system, impairing reaction time and decision-making."}
    # Fix FC[5] - make question substantive
    fc[5] = {"q": "What characterises a sedentary lifestyle?", "a": "Little or no regular physical activity, typically involving prolonged sitting."}
    # Fix FC[6] - pick one consequence
    fc[6] = {"q": "Name one cardiovascular consequence of a sedentary lifestyle.", "a": "Increased risk of coronary heart disease due to reduced cardiovascular fitness."}
    data['flashcard_questions'] = fc
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L02 flashcards')

# ---- Lesson 3: diet-nutrition-and-hydration ----
# FC[3] short q: "Define hypertrophy."
# FC[10] short q + enumeration
def fix_l03():
    path = 'scripts/_content_physical-education-edexcel/lessons/diet-nutrition-and-hydration.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    fc = data['flashcard_questions']
    # Fix FC[3]
    fc[3] = {"q": "What is hypertrophy and what causes it in sport?", "a": "An increase in muscle fibre size, caused by resistance training and adequate protein intake."}
    # Fix FC[10] - split
    fc[10] = {"q": "Which macronutrient is the body's primary fuel source during moderate-to-high-intensity exercise?", "a": "Carbohydrates."}
    data['flashcard_questions'] = fc
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L03 flashcards')

# ---- Lesson 6: guidance-and-feedback-in-sport ----
# insufficient key-fact divs: found 1, need >=2
# Add a second key-fact block to content_html
def fix_l06():
    path = 'scripts/_content_physical-education-edexcel/lessons/guidance-and-feedback-in-sport.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    # The content already has one key-fact at n12. We need to add another.
    # Insert a second key-fact before exam_tip. Find the last paragraph and add after it.
    # We'll insert a second key-fact after the concurrent/terminal section (after n22)
    second_kf = (
        '\n\n<div class="key-fact" data-narration-id="n26" data-revision-tip="Without looking, state which feedback type is most appropriate for a beginner and which for an advanced performer, giving a reason for each choice.">\n'
        '  <div class="key-fact-label">Key Fact</div>\n'
        '  <p>Matching guidance and feedback to the learner&rsquo;s stage: beginners need visual/manual guidance and extrinsic terminal feedback (objective reference they cannot generate themselves). Advanced performers rely more on verbal cues, intrinsic feedback and concurrent feedback from specialist coaches.</p>\n'
        '</div>'
    )
    # Find a good insertion point - after the terminal feedback paragraph (n22)
    old_html = data['content_html']
    # Insert before the closing of the last collapsible content
    insert_after = '</div></div>\n</div>'  # end of last collapsible
    idx = old_html.rfind(insert_after)
    if idx != -1:
        data['content_html'] = old_html[:idx + len(insert_after)] + second_kf
    else:
        data['content_html'] = old_html + second_kf
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L06 key-facts')

# ---- Lesson 7: mental-preparation-for-performance ----
# FC[1] enumeration: "Mental rehearsal enriched with detailed sensory experience..."
# FC[9] enumeration: "Physical anxiety symptoms such as racing heart..."
def fix_l07():
    path = 'scripts/_content_physical-education-edexcel/lessons/mental-preparation-for-performance.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    fc = data['flashcard_questions']
    # Fix FC[1]
    fc[1] = {"q": "What makes imagery different from mental rehearsal?", "a": "Imagery adds rich sensory detail — sights, sounds and feel — to the mental simulation."}
    # Fix FC[9]
    fc[9] = {"q": "What is somatic anxiety?", "a": "Physical symptoms of anxiety such as racing heart or muscle tension."}
    data['flashcard_questions'] = fc
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L07 flashcards')

# ---- Lesson 8: engagement-patterns-in-sport ----
# FC[1] enumeration (5 factors listed), FC[3] enumeration, FC[4] enumeration
# insufficient key-fact divs
def fix_l08():
    path = 'scripts/_content_physical-education-edexcel/lessons/engagement-patterns-in-sport.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    fc = data['flashcard_questions']
    # Fix FC[1] - don't enumerate all 5 factors
    fc[1] = {"q": "Which personal factor most consistently predicts lower sport participation?", "a": "Socio-economic group, due to cost barriers affecting access to facilities and coaching."}
    # Fix FC[3] - rephrase to non-enumeration
    fc[3] = {"q": "Why does lower socio-economic group reduce sport participation?", "a": "High costs of club fees, equipment and transport create a financial access barrier."}
    # Fix FC[4] - rephrase
    fc[4] = {"q": "What typically causes the decline in sport participation between young adulthood and middle age?", "a": "Competing demands from work and family life reduce available leisure time."}
    data['flashcard_questions'] = fc

    # Add a second key-fact div to content_html
    second_kf = (
        '\n\n<div class="key-fact" data-narration-id="n21" data-revision-tip="Without looking, describe two specific interventions that have successfully increased participation for two different underrepresented groups.">\n'
        '  <div class="key-fact-label">Key Fact</div>\n'
        '  <p>Effective interventions to widen engagement include: women-only sessions and female role models (gender gap); walking football and community swimming (older adults); accessible facility design and adapted sport such as wheelchair basketball (disability); subsidised club fees and community sport programmes (lower socio-economic groups). Each intervention targets the specific barrier that limits that group.</p>\n'
        '</div>'
    )
    old_html = data['content_html']
    insert_after = '</div></div>\n</div>'
    idx = old_html.rfind(insert_after)
    if idx != -1:
        data['content_html'] = old_html[:idx + len(insert_after)] + second_kf
    else:
        data['content_html'] = old_html + second_kf

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L08 flashcards and key-facts')

# ---- Lesson 9: commercialisation-sponsorship-and-the-media ----
# FC[0] enumeration, FC[4] enumeration
# insufficient key-fact divs
# insufficient dfn glossary entries (found 2, need >=3)
def fix_l09():
    path = 'scripts/_content_physical-education-edexcel/lessons/commercialisation-sponsorship-and-the-media.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    fc = data['flashcard_questions']
    # Fix FC[0] - enumeration
    fc[0] = {"q": "What is the golden triangle in sport?", "a": "The mutually reinforcing relationship between sport, sponsorship and the media."}
    # Fix FC[4] - enumeration
    fc[4] = {"q": "How does commercialisation benefit elite performers financially?", "a": "Elite athletes earn income from salary, endorsements and sponsorship deals."}
    data['flashcard_questions'] = fc

    # Add second key-fact
    second_kf = (
        '\n\n<div class="key-fact" data-narration-id="n18" data-revision-tip="Cover this and list two positive and two negative impacts of commercialisation on spectators.">\n'
        '  <div class="key-fact-label">Key Fact</div>\n'
        '  <p>Spectator impact: positive &mdash; wider access to sport through broadcast media; higher quality spectacle due to commercial investment. Negative &mdash; rising ticket prices excluding lower-income fans; pay-per-view subscriptions creating cost barriers; matches scheduled for broadcast convenience rather than fan travel needs.</p>\n'
        '</div>'
    )
    old_html = data['content_html']
    insert_after = '</div></div>\n</div>'
    idx = old_html.rfind(insert_after)
    if idx != -1:
        data['content_html'] = old_html[:idx + len(insert_after)] + second_kf
    else:
        data['content_html'] = old_html + second_kf

    # Add a third dfn term to content and glossary
    # Add inline dfn for 'media' into a paragraph, and add glossary entry
    data['content_html'] = data['content_html'].replace(
        'Sport in the Commercial World</h2>',
        'Sport in the Commercial World</h2>'
    )
    # Add 'media' as a dfn in the golden triangle section if not already there
    if '"media"' not in data['content_html'] and 'class="term"' in data['content_html']:
        data['content_html'] = data['content_html'].replace(
            'the <dfn class=\"term\" data-def=\"The mutually reinforcing relationship between sport, sponsorship and the media, in which each element benefits from and depends on the others.\">golden triangle</dfn>',
            'the <dfn class=\"term\" data-def=\"The mutually reinforcing relationship between sport, sponsorship and the media, in which each element benefits from and depends on the others.\">golden triangle</dfn>. The <dfn class=\"term\" data-def=\"Broadcast platforms, online channels, newspapers and other communication channels that distribute sport content to audiences.\">media</dfn> in this context includes television broadcasters, streaming services and online platforms'
        )
        data['glossary_terms'].append({"term": "media", "definition": "Broadcast platforms, online channels, newspapers and other communication channels that distribute sport content to audiences."})

    # Simpler approach: just add a third glossary entry without modifying html
    if len(data['glossary_terms']) < 3:
        data['glossary_terms'].append({"term": "commercialisation", "definition": "The process by which sport becomes increasingly driven by financial and commercial interests, including sponsorship, broadcasting rights and merchandise."})

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L09 flashcards, key-facts, glossary')

# ---- Lesson 10: ethical-behaviour-and-deviance-in-sport ----
# insufficient key-fact divs
def fix_l10():
    path = 'scripts/_content_physical-education-edexcel/lessons/ethical-behaviour-and-deviance-in-sport.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    second_kf = (
        '\n\n<div class="key-fact" data-narration-id="n18" data-revision-tip="Without looking, write the key definition that distinguishes deviance from gamesmanship, and give one sporting example of each.">\n'
        '  <div class="key-fact-label">Key Fact</div>\n'
        '  <p>Gamesmanship uses tactics that are technically within the rules but violate their spirit (e.g. feigning injury to waste time). Deviance breaks the rules, ethics or law (e.g. intentional violent contact, match fixing, banned substance use). The critical distinction is legality: gamesmanship is legal but unsporting; deviance is a rule violation.</p>\n'
        '</div>'
    )
    old_html = data['content_html']
    insert_after = '</div></div>\n</div>'
    idx = old_html.rfind(insert_after)
    if idx != -1:
        data['content_html'] = old_html[:idx + len(insert_after)] + second_kf
    else:
        data['content_html'] = old_html + second_kf
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L10 key-facts')

# ---- Lesson 11: performance-enhancing-drugs-recap-and-application ----
# insufficient key-fact divs
def fix_l11():
    path = 'scripts/_content_physical-education-edexcel/lessons/performance-enhancing-drugs-recap-and-application.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    second_kf = (
        '\n\n<div class="key-fact" data-narration-id="n18" data-revision-tip="Cover this and write the primary performance benefit and one health risk for: (1) anabolic steroids, (2) EPO, (3) beta blockers.">\n'
        '  <div class="key-fact-label">Key Fact</div>\n'
        '  <p>Three commonly tested PEDs: anabolic steroids (benefit: rapid muscle growth; risk: liver damage, hormonal disruption); EPO (benefit: increased red blood cell count and endurance; risk: increased blood viscosity, stroke); beta blockers (benefit: reduced tremor for precision sports; risk: bradycardia, impaired aerobic capacity in endurance sports).</p>\n'
        '</div>'
    )
    old_html = data['content_html']
    insert_after = '</div></div>\n</div>'
    idx = old_html.rfind(insert_after)
    if idx != -1:
        data['content_html'] = old_html[:idx + len(insert_after)] + second_kf
    else:
        data['content_html'] = old_html + second_kf
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L11 key-facts')

# ---- Lesson 13: revision-synthesis ----
# insufficient dfn glossary entries (found 1, need >=3)
def fix_l13():
    path = 'scripts/_content_physical-education-edexcel/lessons/revision-synthesis-component-2-synoptic-practice.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    # Add two more dfn terms to content_html and glossary
    # Add dfn for 'balanced argument' and 'sporting application' in context
    # Simpler: just add glossary entries for terms already used in the lesson
    existing_terms = {g['term'] for g in data['glossary_terms']}
    if 'evaluate' not in existing_terms:
        data['glossary_terms'].append({
            "term": "evaluate",
            "definition": "An exam command word requiring a reasoned, balanced judgement that considers evidence both for and against a position and reaches a supported conclusion."
        })
    if 'balanced argument' not in existing_terms:
        data['glossary_terms'].append({
            "term": "balanced argument",
            "definition": "An argument that considers multiple perspectives or both sides of an issue, rather than presenting only one viewpoint."
        })
    # Also add dfn tags in content_html for these terms
    html = data['content_html']
    if '<dfn class="term" data-def=' not in html or html.count('<dfn class="term"') < 3:
        # Add two inline dfn tags in the content
        html = html.replace(
            'reach a <strong>justified conclusion</strong>',
            'reach a <dfn class="term" data-def="A reasoned judgement that is explicitly supported by evidence and reasoning from the argument.">justified conclusion</dfn>'
        )
        html = html.replace(
            'a <strong>balanced</strong>',
            'a <dfn class="term" data-def="An argument that considers multiple perspectives or both sides of an issue, rather than presenting only one viewpoint.">balanced</dfn>'
        )
        # If replacements didn't find the strings, add dfn for evaluate command word
        if html.count('<dfn class="term"') < 3:
            html = html.replace(
                'The <strong>Evaluate</strong> command word',
                'The <dfn class="term" data-def="An exam command word requiring a reasoned judgement that considers evidence for and against and reaches a supported conclusion.">Evaluate</dfn> command word'
            )
    data['content_html'] = html
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Fixed L13 glossary')

fix_l01()
fix_l02()
fix_l03()
fix_l06()
fix_l07()
fix_l08()
fix_l09()
fix_l10()
fix_l11()
fix_l13()
print('All structural fixes done')
