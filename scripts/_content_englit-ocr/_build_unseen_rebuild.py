# -*- coding: utf-8 -*-
"""
Build the six rebuilt english-literature-ocr / unseen-poetry lessons.

Narration IDs are written as data-narration-id="@" and renumbered n1..nN in
document order across content_html -> exam_tip_html -> conclusion_html, so the
set is always gapless and is a superset of the existing manifest ids (max n19).

Output: scripts/_content_englit-ocr/_unseen_rebuild.json
"""
import sys, os, json, re

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_unseen_rebuild.json")

SVG = ('<svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>')

RUBRIC_A = (
    "Mastering: Sustained, interwoven comparison of both poems with precise, embedded quotations and "
    "confident analysis of the effects of language, form and structure.\n"
    "Secure: Clear comparison of both poems throughout, with relevant quotations and explained analysis of method.\n"
    "Developing: Some comparison, often poem by poem, with supported comments on obvious techniques.\n"
    "Emerging: Simple comments on one or both poems; comparison and textual support are limited or missing."
)
RUBRIC_B = (
    "Mastering: Convincing personal argument about the poem, precisely quoted from memory, with sophisticated "
    "analysis of the poet's methods.\n"
    "Secure: Clear personal argument with accurate quotations and explained analysis of language, form or structure.\n"
    "Developing: Some understanding of the poem with basic support; analysis of method is limited.\n"
    "Emerging: Simple comments on the poem; quotations are absent, vague or inaccurate."
)

TYPE_A = "20 marks — Poetry Comparison"
TYPE_B = "20 marks — Single Poem Response"


def kf(tip, body):
    return ('<div class="key-fact" data-narration-id="@" data-revision-tip="%s">\n'
            '  <div class="key-fact-label">Key Fact</div>\n'
            '  <p>%s</p>\n</div>' % (tip, body))


def coll(title, paras):
    inner = "\n    ".join('<p data-narration-id="@">%s</p>' % p for p in paras)
    return ('<div class="collapsible">\n'
            '  <button class="collapsible-toggle" aria-expanded="false">\n'
            '    <span>%s</span>\n    %s\n  </button>\n'
            '  <div class="collapsible-content"><div class="collapsible-inner">\n    %s\n'
            '  </div></div>\n</div>' % (title, SVG, inner))


LESSONS = []

# ---------------------------------------------------------------- L1
L1_CONTENT = "\n\n".join([
 '<h2 data-narration-id="@">The Unseen Poem Never Arrives Alone</h2>',

 '<p data-narration-id="@">In some courses the unseen poem is a task on its own. In yours it is not. The unseen poem '
 'is printed <strong>beside a named poem from the anthology cluster you have studied</strong>, and the two are joined '
 'by a shared theme. Your job is to read the new poem quickly, then set it against a poem you already know well.</p>',

 '<p data-narration-id="@">Your class studies one <dfn class="term" data-def="A themed group of fifteen poems written '
 'since 1789, studied together for the poetry section of the exam.">anthology cluster</dfn> from a choice of three: '
 'Love and Relationships, Conflict, or Youth and Age. Each cluster holds fifteen poems written since 1789, mixing '
 'literary heritage poets such as Emily Bront&euml; and Lord Byron with modern voices. Whichever cluster you study, '
 'the unseen poem you meet in the exam will be chosen to link to it thematically.</p>',

 kf("Cover this and recall: how many marks is each part of the poetry section worth, and which one uses the unseen poem?",
    'The poetry section is worth <strong>40 marks</strong> and splits into two parts of <strong>20 marks</strong> each. '
    'Part (a) compares a named anthology poem with a thematically linked unseen poem &mdash; <strong>both are printed '
    'for you</strong>. Part (b) asks you to explore <strong>one other poem</strong> from your cluster, chosen by you and '
    'written about from memory. Part (b) involves no comparison at all.'),

 '<h2 data-narration-id="@">What the Question Actually Looks Like</h2>',

 '<p data-narration-id="@">Part (a) begins by naming both poems and telling you which is which. It then gives you a '
 'single comparative instruction &mdash; something like &ldquo;Compare how these poems present the wish for an end to '
 'conflict&rdquo; &mdash; followed by three bullet prompts:</p>',

 '<ul>\n<li data-narration-id="@">ideas and attitudes in each poem</li>\n'
 '<li data-narration-id="@">tone and atmosphere in each poem</li>\n'
 '<li data-narration-id="@">the effects of the language and structure used</li>\n</ul>',

 '<p data-narration-id="@">Those bullets are not decoration. They are the shape of a good answer, and they tell you '
 'that <strong>method</strong> matters as much as meaning. Part (b) then opens the field: &ldquo;Explore in detail one '
 'other poem from your anthology which presents&hellip;&rdquo; and repeats the theme in a slightly broader form.</p>',

 coll("The three clusters, and poems you might meet", [
   '<strong>Love and Relationships</strong> ranges from John Keats&rsquo;s sonnet &lsquo;Bright Star&rsquo; and Emily '
   'Bront&euml;&rsquo;s &lsquo;Love and Friendship&rsquo; to modern poems such as Rita Dove&rsquo;s &lsquo;Flirtation&rsquo; '
   'and James Fenton&rsquo;s &lsquo;In Paris with You&rsquo;.',
   '<strong>Conflict</strong> stretches from Mary Lamb&rsquo;s &lsquo;Envy&rsquo; and Lord Byron&rsquo;s &lsquo;The '
   'Destruction of Sennacherib&rsquo; to Denise Levertov, John Agard and Imtiaz Dharker. Note that the cluster is called '
   'Conflict, not War &mdash; a quarrel, an injustice or a divided mind all count.',
   '<strong>Youth and Age</strong> includes William Blake&rsquo;s &lsquo;Holy Thursday&rsquo; and Derek Walcott&rsquo;s '
   '&lsquo;Love After Love&rsquo;. Whatever your cluster, learn its fifteen poems by theme as well as by title &mdash; '
   'part (b) is chosen by you, so the poem you can argue with best is the poem you should pick.']),

 '<h2 data-narration-id="@">Which Skills Earn the Marks</h2>',

 '<p data-narration-id="@">Only two <dfn class="term" data-def="The skill areas an exam board marks a response against; '
 'in the poetry section only reading and response, and analysis of method, are credited.">assessment objectives</dfn> '
 'are credited in the poetry section. AO1 rewards a critical, informed personal response supported by textual '
 'references. AO2 rewards analysis of the language, form and structure a poet uses to create meanings and effects, '
 'with accurate terminology. In part (a), <strong>AO2 is the dominant objective</strong>. In part (b) the two carry '
 'equal weight.</p>',

 kf("Close this and list the two things that earn no marks at all in the poetry section, and say where each one is credited instead.",
    'Context is <strong>not</strong> assessed in the poetry section &mdash; you cannot know who wrote the unseen poem, '
    'so historical background earns nothing here. Neither is spelling, punctuation and grammar: that is credited in the '
    'Shakespeare section instead. Every mark in the poetry section comes from your reading of the poems and your '
    'analysis of how they work.'),

 '<h2 data-narration-id="@">What Examiners Reward</h2>',

 '<p data-narration-id="@">Reports on this paper are consistent about what separates strong answers. The best responses '
 'engage confidently with the unseen poem, make comparison <strong>continuous</strong> rather than saving it for a final '
 'paragraph, and comment on the <em>effect</em> of a technique rather than simply naming it. They also answer the exact '
 'wording of the task without repeating that wording so often that it becomes intrusive.</p>',

 '<p data-narration-id="@">One warning matters more than any other. Students often assume the two poets must agree. '
 'They frequently do not &mdash; and the differences between them are where the highest marks live. Read the unseen '
 'poem for how it <em>departs</em> from your anthology poem, not only for how it echoes it.</p>',

 coll("Four ways students lose marks before they write a word", [
   'Writing about only one of the two poems in part (a). However good the analysis, a one-poem answer cannot rise past '
   'the lower bands.',
   'Choosing a part (b) poem from a different cluster, or a poem that is no longer in the current anthology.',
   'Re-using the part (a) anthology poem in part (b). It must be a different poem.',
   'Comparing in part (b). Comparison is not required there, and it eats the time you need for close analysis of one poem.']),

 '<h2 data-narration-id="@">How This Unit Works</h2>',

 '<p data-narration-id="@">The next three lessons build the analytical toolkit: language and imagery, then form and '
 'structure, then <dfn class="term" data-def="The idea or attitude a poem explores beneath its surface subject, such as '
 'grief, endurance or injustice.">theme</dfn> and personal response. Lesson five puts them together into the skill this '
 'paper is really built around &mdash; linking an unfamiliar poem to the cluster you know. The final lesson turns all of '
 'it into a timed routine.</p>',
])

L1_TIP = ('<p data-narration-id="@">Read the task wording before you read either poem. The theme it names is the lens '
          'for everything that follows, and it stops you writing a general appreciation of the anthology poem instead '
          'of the answer the examiner asked for.</p>')

L1_CONC = ('<h3 data-narration-id="@">Key Takeaways</h3>\n<ul>\n'
           '<li data-narration-id="@">The poetry section is 40 marks: part (a) compares a named anthology poem with a '
           'printed unseen poem for 20 marks; part (b) explores one other cluster poem for 20 marks.</li>\n'
           '<li data-narration-id="@">Only reading and response and analysis of method are credited &mdash; context and '
           'accuracy of spelling earn nothing in this section.</li>\n'
           '<li data-narration-id="@">Do not assume the two poets agree; the differences between them carry the highest '
           'marks.</li>\n</ul>')

LESSONS.append({
 "lesson_id": "23c00d1c-4563-4335-983f-737a8bf981ae",
 "lesson_number": 1,
 "title": "What is Unseen Poetry?",
 "description": "How the poetry section pairs an unseen poem with a named poem from your anthology cluster.",
 "content_html": L1_CONTENT,
 "exam_tip_html": L1_TIP,
 "conclusion_html": L1_CONC,
 "hero_image_caption": "An open book with pages fanned — discovering new poetry for the first time",
 "hero_keywords": ["open poetry book pages", "poetry anthology", "book pages close up"],
 "practice_questions": [
   {"text": "Compare how these poems present the passing of time. One poem is from your anthology cluster and the other is unseen. You should consider ideas and attitudes, tone and atmosphere, and the effects of language and structure. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems present a relationship that has changed. Write about both poems throughout your answer. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which presents an idea that is difficult to accept.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems present strong feeling. Give particular attention to the differences between the two poets' attitudes rather than only their similarities. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which presents a moment of change. Do not compare it with any other poem.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems present a place and what it means to the speaker. Use the three bullet prompts to shape your paragraphs. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
 ],
 "knowledge_checks": [
   {"type": "mcq", "q": "In the comparison part of the poetry section, how many poems are printed on the paper for you?",
    "options": ["Only the unseen poem", "Only the anthology poem", "Both the anthology poem and the unseen poem", "Neither — you work entirely from memory"], "correct": 2},
   {"type": "mcq", "q": "Which task does part (b) of the poetry section set?",
    "options": ["Compare the unseen poem with a second unseen poem", "Explore one other poem from your anthology cluster, chosen by you", "Compare the anthology poem with a Shakespeare extract", "Rewrite the unseen poem in your own words"], "correct": 1},
   {"type": "fill", "q": "Each anthology cluster contains fifteen poems written since the year _____.",
    "options": ["1789", "1832", "1901", "1945"], "correct": 0},
   {"type": "fill", "q": "In the comparison part of the poetry section, the dominant assessment objective is analysis of language, form and _____.",
    "options": ["context", "structure", "spelling", "biography"], "correct": 1},
   {"type": "match", "q": "Match each part of the poetry section to what it requires:",
    "left": ["Part (a), 20 marks", "Part (b), 20 marks", "The three bullet prompts"],
    "right": ["Compare a named anthology poem with a printed unseen poem", "Explore one other cluster poem of your own choice, from memory", "Ideas and attitudes, tone and atmosphere, effects of language and structure"],
    "order": [0, 1, 2]},
 ],
 "flashcard_questions": [
   {"q": "What is printed alongside the unseen poem in the comparison part of the poetry section?", "a": "A named poem from the anthology cluster the student has studied."},
   {"q": "How many marks is the whole poetry section of the paper worth?", "a": "40 marks, split into two parts of 20 marks each."},
   {"q": "Name the three thematic clusters offered in the poetry anthology.", "a": "Love and Relationships; Conflict; Youth and Age."},
   {"q": "How many poems are there in each anthology cluster?", "a": "Fifteen."},
   {"q": "From which year onwards were the anthology poems written?", "a": "1789."},
   {"q": "Which assessment objective is dominant in the comparison part of the poetry section?", "a": "AO2, the analysis of a poet's methods."},
   {"q": "How are the two objectives weighted in part (b) of the poetry section?", "a": "Equally: reading and response counts the same as analysis of method."},
   {"q": "Why does context earn no marks in the poetry section?", "a": "The poet of the unseen poem is not identified, so background knowledge cannot be credited."},
   {"q": "In which section of this paper is spelling, punctuation and grammar assessed?", "a": "The Shakespeare section, not the poetry section."},
   {"q": "Does part (b) of the poetry section require any comparison?", "a": "No. It asks for detailed exploration of a single poem."},
   {"q": "What happens to a part (a) answer that discusses only one of the two poems?", "a": "It cannot rise beyond the lower mark bands, however strong the analysis is."},
   {"q": "Why should you not assume the two poets in part (a) agree?", "a": "The unseen poem often takes a different view, and the differences carry high marks."},
   {"q": "Which cluster covers quarrels and injustice as well as war?", "a": "Conflict."},
 ],
 "glossary_terms": [
   {"term": "anthology cluster", "definition": "A themed group of fifteen poems written since 1789, studied together for the poetry section of the exam."},
   {"term": "assessment objectives", "definition": "The skill areas an exam board marks a response against; in the poetry section only reading and response, and analysis of method, are credited."},
   {"term": "theme", "definition": "The idea or attitude a poem explores beneath its surface subject, such as grief, endurance or injustice."},
 ],
})

# ---------------------------------------------------------------- L2
L2_CONTENT = "\n\n".join([
 '<h2 data-narration-id="@">Why Language Analysis Carries This Section</h2>',

 '<p data-narration-id="@">In the comparison part of the poetry section, analysis of the poet&rsquo;s methods is the '
 'dominant objective. That means marks follow the sentence in which you explain what a word <em>does</em>, not the '
 'sentence in which you name a device. Examiners describe the weaker habit exactly: feature-spotting. A response that '
 'lists metaphor, alliteration and enjambment without explaining any of their effects sits low in the bands, however '
 'many terms it uses.</p>',

 kf("Cover this and write the three-move sentence pattern from memory, then apply it to any image in a poem you know.",
    'Every analytical point should make three moves: <strong>quote</strong> a few words, say what those particular words '
    '<em>suggest</em>, then say <em>why that matters</em> to the idea the poet is building. Two images analysed this way '
    'beat ten techniques merely labelled.'),

 '<h2 data-narration-id="@">Imagery: What Is Being Transferred?</h2>',

 '<p data-narration-id="@">When you meet a simile or a metaphor, do not stop at naming it. Ask what qualities move from '
 'one thing to the other. Byron opens &lsquo;The Destruction of Sennacherib&rsquo; with &ldquo;The Assyrian came down '
 'like the wolf on the fold&rdquo;. The simile hands the army a predator&rsquo;s hunger and speed &mdash; but the more '
 'telling word is &ldquo;fold&rdquo;, which turns the victims into penned sheep: owned, counted, unable to run. The '
 'slaughter is made to feel not merely violent but routine.</p>',

 '<p data-narration-id="@">An <dfn class="term" data-def="A metaphor developed across several lines or a whole poem, so '
 'that one comparison controls the reader&rsquo;s understanding of the subject.">extended metaphor</dfn> deserves even '
 'more attention. If a single comparison runs through a poem, it is almost certainly carrying the poem&rsquo;s central '
 'idea, and it should anchor your response rather than appear as one point among many.</p>',

 coll("Personification, pathetic fallacy and symbol", [
   '<strong>Personification</strong> gives human life to something that has none. In Wordsworth&rsquo;s boat-stealing '
   'episode, &ldquo;a huge peak, black and huge&rdquo; seems to rise and stride after the boy. The mountain has not '
   'moved; the boy&rsquo;s guilt has. Personification here turns landscape into conscience.',
   '<strong>Pathetic fallacy</strong> is the narrower case where weather or season mirrors feeling. It is easy to spot '
   'and easy to waste. The mark comes from precision: not &ldquo;the rain shows sadness&rdquo; but what <em>kind</em> of '
   'sadness the particular weather implies.',
   '<strong>Symbol</strong> is an object that carries meaning beyond itself. Watch for anything a poet returns to. A '
   'repeated object in a short poem is rarely accidental.']),

 '<h2 data-narration-id="@">Connotation: The Word Behind the Word</h2>',

 '<p data-narration-id="@">The most useful habit in unseen analysis is testing a word&rsquo;s '
 '<dfn class="term" data-def="The feelings and associations a word carries beyond its literal dictionary meaning.">'
 'connotations</dfn> against its alternatives. Emily Dickinson begins &ldquo;There&rsquo;s a certain Slant of light&rdquo;. '
 'She could have written a beam, a shaft, a ray. &ldquo;Slant&rdquo; suggests something off-true, oblique, faintly wrong '
 '&mdash; and that crookedness prepares the reader for the pain the poem goes on to describe.</p>',

 '<p data-narration-id="@">Ask yourself: what would be lost if the poet had used the ordinary word instead? Your answer '
 'to that question is the analysis.</p>',

 '<p data-narration-id="@">Verbs repay this test more than any other word class. They carry the energy of a line, and '
 'poets choose them precisely. Whether a speaker <em>walks</em>, <em>drifts</em>, <em>trudges</em> or <em>strides</em> '
 'tells you almost everything about their state of mind, and the shift from an active verb to a passive construction '
 'often marks the moment a speaker loses control of their own story.</p>',

 '<h2 data-narration-id="@">Semantic Fields</h2>',

 '<p data-narration-id="@">A <dfn class="term" data-def="A group of words in a text that all belong to the same area of '
 'meaning, building a pattern the reader feels before noticing.">semantic field</dfn> is a cluster of words drawn from '
 'one area of life. Mary Lamb&rsquo;s &lsquo;Envy&rsquo; judges the envious mind with words of failed sight and '
 'sensation &mdash; the rose tree that cannot see &ldquo;its own red rose&rdquo; is called &ldquo;blind and senseless&rdquo;. '
 'Naming a semantic field is a strong move in an unseen poem because it lets you make one point about the whole text '
 'rather than a scattering of small ones.</p>',

 coll("Sound: how a line feels in the mouth", [
   '<strong>Sibilance</strong>, the repetition of soft s sounds, can hush a line or make it hiss. Context decides which.',
   '<strong>Plosives</strong> &mdash; b, d, p, t, k, g &mdash; stop the air abruptly and suit anger, force or shock.',
   '<strong>Vowel length</strong> changes pace. Keats opens with &ldquo;Bright star, would I were stedfast as thou '
   'art&rdquo;, and the long open vowels hold the line steady, imitating the fixed star the speaker envies. Short vowels '
   'would have hurried it and destroyed the effect.']),

 kf("Close this and rewrite one feature-spotting sentence into an analytical one about a poem you have studied.",
    '&ldquo;The poet uses sibilance&rdquo; earns nothing. &ldquo;The soft s sounds slow the line to a whisper, so the '
    'threat seems to creep rather than strike&rdquo; earns the mark. The difference is always the same: name the effect '
    'on the reader, and tie it to the poem&rsquo;s idea.'),

 '<h2 data-narration-id="@">Language Inside a Comparison</h2>',

 '<p data-narration-id="@">In the comparison part, resist analysing one poem&rsquo;s language completely before turning '
 'to the other. Put the two images beside each other in the same paragraph. If one poet reaches for a predator and the '
 'other for a machine, that contrast is itself a point about attitude &mdash; and it earns credit under both objectives '
 'at once.</p>',
])

L2_TIP = ('<p data-narration-id="@">Use tentative phrasing when a word can be read more than one way: &ldquo;this could '
          'suggest&rdquo;, &ldquo;perhaps the poet implies&rdquo;. Examiners credit responses that recognise other valid '
          'readings, and tentative phrasing lets you explore an unfamiliar poem without committing to a reading you '
          'cannot defend.</p>')

L2_CONC = ('<h3 data-narration-id="@">Key Takeaways</h3>\n<ul>\n'
           '<li data-narration-id="@">Analyse the effect of a technique, never merely its presence; naming devices earns '
           'nothing on its own.</li>\n'
           '<li data-narration-id="@">Test a word against the ordinary word the poet rejected &mdash; the difference is '
           'the connotation you should write about.</li>\n'
           '<li data-narration-id="@">Semantic fields let you make one strong point about a whole unseen poem instead of '
           'several small ones.</li>\n</ul>')

LESSONS.append({
 "lesson_id": "242f3166-ab45-4c6d-af73-6cc404d73088",
 "lesson_number": 2,
 "title": "Analysing Language & Imagery",
 "description": "Imagery, connotation, sound and semantic fields — the dominant skill in the poetry comparison.",
 "content_html": L2_CONTENT,
 "exam_tip_html": L2_TIP,
 "conclusion_html": L2_CONC,
 "hero_image_caption": "Printed poem with handwritten annotations — identifying language features in unseen text",
 "hero_keywords": ["annotated poem page", "handwritten notes on book", "close reading text"],
 "practice_questions": [
   {"text": "Compare how these poems use imagery to present danger. Analyse the qualities each image transfers to its subject. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster in which a single extended metaphor controls the reader's understanding.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems use sound to create atmosphere. Refer to specific words and explain the effect of the sounds they make. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which builds a strong semantic field. Explain what pattern of meaning the poet creates and why.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems present the natural world. Give close attention to the connotations of individual word choices in each poem. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems give human qualities to something that is not human, and what each poet gains by doing so. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
 ],
 "knowledge_checks": [
   {"type": "mcq", "q": "Which sentence shows analysis rather than feature-spotting?",
    "options": ["The poet uses sibilance in this line", "There is a metaphor in the second stanza", "The soft s sounds slow the line to a whisper, so the threat seems to creep", "The poem contains alliteration and enjambment"], "correct": 2},
   {"type": "mcq", "q": "What is the best reason to build a response around an extended metaphor in an unseen poem?",
    "options": ["It is the easiest device to name", "If a comparison runs through the poem it usually carries the central idea", "It always appears in the final stanza", "It proves the poem is modern"], "correct": 1},
   {"type": "fill", "q": "The feelings and associations a word carries beyond its dictionary meaning are its _____.",
    "options": ["syllables", "connotations", "denotations", "consonants"], "correct": 1},
   {"type": "fill", "q": "A group of words in a poem that all belong to the same area of meaning is called a semantic _____.",
    "options": ["frame", "field", "ladder", "chain"], "correct": 1},
   {"type": "match", "q": "Match each sound feature to the effect it commonly creates:",
    "left": ["Plosive consonants", "Long open vowels", "Sibilance"],
    "right": ["Abrupt, forceful, suited to anger or shock", "A held, unhurried line that resists movement", "A hush or a hiss, depending on context"],
    "order": [0, 1, 2]},
 ],
 "flashcard_questions": [
   {"q": "What three moves should every analytical point make?", "a": "Quote briefly, say what the words suggest, then explain why that matters to the poem's idea."},
   {"q": "What does the term feature-spotting describe?", "a": "Naming techniques without explaining any of their effects."},
   {"q": "When analysing a simile, what is the key question to ask?", "a": "What qualities are transferred from one thing to the other?"},
   {"q": "Which word in Byron's opening line turns the victims into penned sheep?", "a": "Fold."},
   {"q": "What is an extended metaphor?", "a": "A comparison developed across several lines or a whole poem."},
   {"q": "Why is an extended metaphor worth building a response around?", "a": "It usually carries the poem's central idea rather than a passing detail."},
   {"q": "What is pathetic fallacy?", "a": "Weather or season used to mirror a speaker's feelings."},
   {"q": "Which word does Dickinson choose instead of beam, shaft or ray?", "a": "Slant."},
   {"q": "What does that word choice suggest about the light?", "a": "Something off-true and oblique, preparing the reader for pain."},
   {"q": "What is a semantic field?", "a": "A cluster of words in a text drawn from one area of meaning."},
   {"q": "Why is spotting a semantic field useful in an unseen poem?", "a": "It supports one strong point about the whole text instead of several small ones."},
   {"q": "What effect do plosive consonants usually create in a line?", "a": "An abrupt, forceful sound suited to anger or shock."},
   {"q": "How should language be handled in the comparison part of the paper?", "a": "Place both poems' images side by side in the same paragraph."},
   {"q": "Why is tentative phrasing rewarded in unseen analysis?", "a": "It shows awareness that other readers could interpret the poem differently."},
 ],
 "glossary_terms": [
   {"term": "extended metaphor", "definition": "A metaphor developed across several lines or a whole poem, so that one comparison controls the reader's understanding of the subject."},
   {"term": "connotations", "definition": "The feelings and associations a word carries beyond its literal dictionary meaning."},
   {"term": "semantic field", "definition": "A group of words in a text that all belong to the same area of meaning, building a pattern the reader feels before noticing."},
 ],
})

# ---------------------------------------------------------------- L3
L3_CONTENT = "\n\n".join([
 '<h2 data-narration-id="@">The Half of the Objective Most Students Skip</h2>',

 '<p data-narration-id="@">The dominant objective in the comparison part names three things: language, <strong>form</strong> '
 'and <strong>structure</strong>. Most students write well about the first and almost nothing about the other two. That '
 'is the easiest place in the whole paper to pick up marks, because form and structure are visible before you have '
 'understood a single line.</p>',

 '<p data-narration-id="@"><dfn class="term" data-def="The overall type and shape a poem takes, such as a sonnet, a '
 'ballad or free verse.">Form</dfn> is the kind of poem it is. <dfn class="term" data-def="The order in which a poem '
 'releases its ideas and feelings, including where it turns, repeats and ends.">Structure</dfn> is the order in which '
 'it releases its ideas. Form is the container; structure is the journey inside it.</p>',

 kf("Cover this and name three things you can observe about a poem's shape before reading a single line.",
    'You can see the number of stanzas, whether the lines are regular or ragged, and whether the poem narrows or widens '
    'towards the end &mdash; all before you read a word. Those observations are already analysis of form, and in an '
    'unseen poem they buy you a point while you are still working out the meaning.'),

 '<h2 data-narration-id="@">Form: The Shape the Poet Chose</h2>',

 '<p data-narration-id="@">A sonnet promises fourteen lines and an argument that turns. Keats uses one for &ldquo;Bright '
 'star, would I were stedfast as thou art&rdquo;, and the tight, closed form suits a speaker longing for permanence. '
 'A ballad, with its regular beat and repeated refrain, suits storytelling and public grief. Free verse abandons a fixed '
 'pattern altogether, which can feel like natural speech &mdash; or like control breaking down.</p>',

 kf("Close this and explain why naming a poem's form earns no marks on its own.",
    'Never write &ldquo;this is a sonnet&rdquo; and stop. Naming a form earns nothing. The mark comes from the '
    'consequence: what does the form let this poet do, or stop them doing, that another shape would not?'),

 coll("Reading a poem's structure in four questions", [
   '<strong>Where does it begin and end emotionally?</strong> Track the feeling from the first line to the last. A poem '
   'that opens in anger and closes in exhaustion has a structure worth describing.',
   '<strong>Where is the turn?</strong> Look for a stanza break, a conjunction, or a shift of tense or pronoun.',
   '<strong>What repeats?</strong> Repetition of a word, a line or a grammatical pattern is structural, and it usually '
   'signals obsession, insistence or ritual.',
   '<strong>How do the final lines land?</strong> Resolution, refusal, or a deliberate failure to resolve &mdash; endings '
   'are the most quotable structural evidence you have.']),

 '<h2 data-narration-id="@">The Turn</h2>',

 '<p data-narration-id="@">A <dfn class="term" data-def="The point where a poem changes direction, tone or argument; in '
 'a sonnet it traditionally falls between the octave and the sestet.">volta</dfn> is the hinge of a poem. Emily '
 'Bront&euml;&rsquo;s &lsquo;Love and Friendship&rsquo; sets &ldquo;Love is like the wild rose-briar&rdquo; against '
 '&ldquo;Friendship like the holly-tree&rdquo;, then turns from the showy rose to the plant that will &ldquo;bloom most '
 'constantly&rdquo;. The turn is the argument. Find it and you have found what the poem is for.</p>',

 '<h2 data-narration-id="@">Line-Level Structure</h2>',

 '<p data-narration-id="@"><dfn class="term" data-def="Running a sentence over the end of a line without punctuation, so '
 'the reader moves on without pausing.">Enjambment</dfn> spills a sentence past the line break and hurries the reader '
 'onward; it can suggest breathlessness, overflow or a thought the speaker cannot contain. A '
 '<dfn class="term" data-def="A pause created inside a line by punctuation, breaking its momentum.">caesura</dfn> does '
 'the opposite, stopping a line in its middle. An end-stopped line closes cleanly and can feel controlled, final or '
 'stubborn.</p>',

 '<p data-narration-id="@">These are useful precisely because they need no knowledge of the poet. You can hear them on '
 'a first reading of an unfamiliar poem.</p>',

 '<p data-narration-id="@">Rhyme works the same way. A tight, regular '
 '<dfn class="term" data-def="The pattern of rhymes across a poem, usually written as letters such as ABAB.">rhyme '
 'scheme</dfn> can make a poem sound inevitable, settled, even smug &mdash; useful when a poet wants an argument to '
 'feel proved. Half-rhyme, where the sounds almost but do not quite match, unsettles the ear and often signals '
 'something the speaker cannot resolve. If a regular scheme suddenly breaks, that break is a structural event and '
 'deserves a sentence of its own.</p>',

 coll("Structure inside a comparison", [
   'Two poems on one theme are often built to do opposite things, and that contrast is one of the strongest comparative '
   'points available to you. One poem may tighten towards a controlled final couplet while the other loosens into '
   'fragments.',
   'Compare the <em>endings</em> directly. Where a poem chooses to stop tells you what its poet believes about the '
   'subject: whether the problem can be resolved, survived, or only stated.',
   'If both poems share a feature &mdash; both use enjambment, say &mdash; do not stop at the similarity. Ask what each '
   'poet uses it <em>for</em>. Identical methods put to different purposes make an excellent paragraph.']),

 '<h2 data-narration-id="@">Terminology You Can Always Use Safely</h2>',

 '<p data-narration-id="@">Stanza, quatrain, couplet, refrain, rhyme scheme, half-rhyme, enjambment, caesura, volta, '
 'free verse, first person, present tense. Every one of these can be applied to a poem you have never seen, and every '
 'one can be tied to an effect. Accurate terminology is credited &mdash; but only when it is attached to an explanation.</p>',
])

L3_TIP = ('<p data-narration-id="@">Give structure a paragraph of its own in the comparison, and put it early rather '
          'than last. Structural points are often the freshest thing in a script, and burying them under the final '
          'paragraph means they are the points you run out of time to make.</p>')

L3_CONC = ('<h3 data-narration-id="@">Key Takeaways</h3>\n<ul>\n'
           '<li data-narration-id="@">Form is the container and structure is the journey; the objective credits both '
           'alongside language.</li>\n'
           '<li data-narration-id="@">Locate the turn in each poem &mdash; it usually carries the argument.</li>\n'
           '<li data-narration-id="@">When two poems share a structural feature, compare what each poet uses it for '
           'rather than noting the similarity and moving on.</li>\n</ul>')

LESSONS.append({
 "lesson_id": "6ac8cb2a-b621-4d9a-9658-026e311f6fcd",
 "lesson_number": 3,
 "title": "Analysing Form & Structure",
 "description": "How a poem's shape and order build meaning, and how to compare two poems' structures.",
 "content_html": L3_CONTENT,
 "exam_tip_html": L3_TIP,
 "conclusion_html": L3_CONC,
 "hero_image_caption": "A solitary figure in landscape — lines and stanzas structure poetic form",
 "hero_keywords": ["lone figure landscape", "poetry manuscript stanzas", "open notebook lines"],
 "practice_questions": [
   {"text": "Compare how these poems are structured to move the reader from one feeling to another. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster whose form is central to its meaning. Explain what the chosen form allows the poet to do.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how the endings of these poems shape the reader's final impression of the subject. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems use repetition. Explain what each poet gains by returning to the same word or line. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which contains a clear turning point. Explain how the poem changes and why it matters.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems control pace through enjambment, caesura and end-stopped lines. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
 ],
 "knowledge_checks": [
   {"type": "mcq", "q": "What is the difference between form and structure?",
    "options": ["Form is the rhyme scheme; structure is the rhythm", "Form is the type and shape of poem; structure is the order in which ideas are released", "Form is the meaning; structure is the imagery", "They are two words for the same thing"], "correct": 1},
   {"type": "mcq", "q": "Two poems both use enjambment. What is the strongest comparative point to make?",
    "options": ["State that both poems use enjambment and move on", "Explain what each poet uses enjambment for", "Count the enjambed lines in each poem", "Say that enjambment always suggests freedom"], "correct": 1},
   {"type": "fill", "q": "The point where a poem changes direction, tone or argument is called the _____.",
    "options": ["stanza", "volta", "refrain", "caesura"], "correct": 1},
   {"type": "fill", "q": "A pause created inside a line by punctuation is called a _____.",
    "options": ["caesura", "couplet", "quatrain", "cadence"], "correct": 0},
   {"type": "match", "q": "Match each structural feature to its usual effect:",
    "left": ["Enjambment", "End-stopped line", "Repeated refrain"],
    "right": ["Hurries the reader on, suggesting overflow or breathlessness", "Closes cleanly, feeling controlled or final", "Signals insistence, obsession or ritual"],
    "order": [0, 1, 2]},
 ],
 "flashcard_questions": [
   {"q": "What does the term form mean when analysing a poem?", "a": "The overall type and shape of the poem, such as sonnet, ballad or free verse."},
   {"q": "What does the term structure mean when analysing a poem?", "a": "The order in which the poem releases its ideas and feelings."},
   {"q": "How many lines does a sonnet have?", "a": "Fourteen."},
   {"q": "Why does naming a poem's form earn no marks on its own?", "a": "The credit comes from explaining what that shape allows the poet to do."},
   {"q": "What is a volta in a poem?", "a": "The hinge where the poem changes direction, tone or argument."},
   {"q": "Which two plants does Emily Bronte set against each other in her poem on love?", "a": "The wild rose-briar and the holly-tree."},
   {"q": "What does enjambment do to the reader's pace?", "a": "It carries them past the line break without pausing."},
   {"q": "What effect does a caesura have on a line?", "a": "It stops the line in the middle, breaking its momentum."},
   {"q": "Why are line-level features so useful for an unseen poem?", "a": "They can be heard on a first reading without any knowledge of the poet."},
   {"q": "What should you look at first when comparing the structures of two poems?", "a": "Where each poem chooses to end."},
   {"q": "Name three structural observations you can make before reading a poem.", "a": "The number of stanzas; whether lines are regular or ragged; whether the poem narrows or widens."},
   {"q": "When is subject terminology actually credited?", "a": "Only when it is attached to an explanation of an effect."},
   {"q": "Where in the comparison should a structural paragraph go?", "a": "Early, so it is not lost when time runs short."},
 ],
 "glossary_terms": [
   {"term": "Form", "definition": "The overall type and shape a poem takes, such as a sonnet, a ballad or free verse."},
   {"term": "Structure", "definition": "The order in which a poem releases its ideas and feelings, including where it turns, repeats and ends."},
   {"term": "volta", "definition": "The point where a poem changes direction, tone or argument; in a sonnet it traditionally falls between the octave and the sestet."},
   {"term": "Enjambment", "definition": "Running a sentence over the end of a line without punctuation, so the reader moves on without pausing."},
   {"term": "caesura", "definition": "A pause created inside a line by punctuation, breaking its momentum."},
   {"term": "rhyme scheme", "definition": "The pattern of rhymes across a poem, usually written as letters such as ABAB."},
 ],
})

# ---------------------------------------------------------------- L4
L4_CONTENT = "\n\n".join([
 '<h2 data-narration-id="@">What a Personal Response Actually Means</h2>',

 '<p data-narration-id="@">The first assessment objective asks for a '
 '<dfn class="term" data-def="Writing that argues about a text and weighs interpretations, rather than retelling what '
 'happens in it.">critical style</dfn>, an informed personal response, and '
 'textual references used to support and illustrate interpretations. Notice the word <em>informed</em>. A personal '
 'response is not a feeling about the poem; it is an argument about what the poet is doing, held together by evidence. '
 'In part (b) of the poetry section this objective carries equal weight with analysis of method, so half of those twenty '
 'marks depend on having something to say.</p>',

 '<h2 data-narration-id="@">Subject Is Not Theme</h2>',

 '<p data-narration-id="@">The subject is what happens in the poem. The theme is what the poet wants you to think about '
 'it. A poem whose subject is a soldier&rsquo;s funeral may have grief as its theme, or waste, or the failure of ritual '
 'to comfort. Two poems can share a subject entirely and share no theme at all &mdash; which is exactly why the '
 'comparison part is worth writing carefully.</p>',

 kf("Cover this and write a one-sentence thesis for any poem you have studied, naming the poet's idea and one method.",
    'Before you write, compress your reading into a single <dfn class="term" data-def="A one-sentence statement of the '
    'argument a response will prove, written before the first paragraph.">thesis</dfn> sentence: what is this poet '
    'saying, and how? Every paragraph then proves that sentence. Examiners consistently note that the strongest '
    'responses show clear signs of planning and establish an argument in the opening lines.'),

 '<h2 data-narration-id="@">Read the Task Wording, Not the Poem Alone</h2>',

 '<p data-narration-id="@">Tasks in this section are precise. &ldquo;Presents a satisfying relationship&rdquo; is not the '
 'same as &ldquo;presents a relationship&rdquo;. &ldquo;The wish for an end to conflict&rdquo; is not the same as '
 '&ldquo;conflict&rdquo;. The qualifying words are the target, and they must shape which poem you choose in part (b) '
 'and which lines you quote.</p>',

 '<p data-narration-id="@">There is a matching warning. Examiners criticise responses that repeat the task wording so '
 'often it becomes intrusive, as well as those that ignore it entirely. Anchor the wording in your thesis and at the '
 'start of each paragraph, then let the analysis do the rest.</p>',

 coll("Turning a task phrase into a thesis", [
   'Take the task phrase and ask a question of it. If the task says &ldquo;presents a difficult memory&rdquo;, ask: '
   'difficult for whom, and why does the difficulty persist?',
   'Answer in one sentence that names an attitude, not a topic. &ldquo;The poet presents memory as a debt the speaker '
   'cannot repay, using the repeated imperative to make remembering feel like an order.&rdquo;',
   'Check that your sentence could be argued against. If nobody could disagree with your thesis, it is a summary rather '
   'than an interpretation.']),

 '<h2 data-narration-id="@">Tone and Attitude</h2>',

 '<p data-narration-id="@">Tone is the poem&rsquo;s voice; '
 '<dfn class="term" data-def="The speaker&rsquo;s position towards the subject, which may differ from the poet&rsquo;s '
 'own view.">attitude</dfn> is the position that voice takes. Keep the two apart. A poem can sound calm and still be '
 'furious. Watch for a <dfn class="term" data-def="A change of voice or mood partway through a poem, often marking a '
 'change in the speaker&rsquo;s thinking.">tonal shift</dfn> especially: a poem that begins tender and ends cold has '
 'given you a structural point and a thematic one in the same observation.</p>',

 '<p data-narration-id="@">Pronouns are the quickest route into attitude in an unfamiliar poem. A speaker who moves '
 'from <em>I</em> to <em>we</em> is claiming company; one who slides from <em>you</em> to <em>they</em> is stepping back '
 'from the subject. Tense does similar work: a poem told in the present tense makes an old wound feel current, while a '
 'sudden past tense can push a feeling safely out of reach. Both are observable in seconds and both point straight at '
 'what the speaker thinks.</p>',

 '<h2 data-narration-id="@">Other Readers, Other Readings</h2>',

 '<p data-narration-id="@">You are expected to recognise that different valid responses to a text are possible. This is '
 'not hedging. Offering a second reading &mdash; &ldquo;the silence could be grief, though it may equally be refusal&rdquo; '
 '&mdash; shows critical thinking, and it is safer than asserting one meaning for a poem you met four minutes ago.</p>',

 kf("Close this and recall what happens to a part (b) answer whose quotations are inaccurate.",
    'Part (b) is written from memory, and misquotation is expensive. Responses that lack textual support or misquote '
    'find the higher bands out of reach, particularly for analysis of method. Learn <strong>short</strong> quotations '
    'exactly &mdash; three or four words you can place perfectly beat a whole line you half-remember.'),

 coll("Building a quotation bank for your cluster", [
   'For each poem in your cluster, learn one quotation for the central idea, one for the strongest image, and one from '
   'the ending. Three per poem is enough to write a confident part (b) answer.',
   'Tag each quotation with a theme word rather than a poem title. When the task names a theme, you can then find your '
   'evidence by idea instead of hunting through titles under pressure.',
   'Test yourself by writing the quotation out, not by reading it. Recognition is not recall, and the exam asks for '
   'recall.']),
])

L4_TIP = ('<p data-narration-id="@">Choose your part (b) poem for the argument you can make about it, not for how much '
          'you can remember. A short poem you can interpret confidently produces a better answer than a famous one you '
          'can only summarise.</p>')

L4_CONC = ('<h3 data-narration-id="@">Key Takeaways</h3>\n<ul>\n'
           '<li data-narration-id="@">A personal response is an argument supported by evidence, not a reaction to the '
           'poem.</li>\n'
           '<li data-narration-id="@">Separate subject from theme, and let the qualifying words in the task decide what '
           'you write about.</li>\n'
           '<li data-narration-id="@">Learn short quotations exactly &mdash; part (b) is written from memory and '
           'misquotation blocks the higher bands.</li>\n</ul>')

LESSONS.append({
 "lesson_id": "bd2ead7e-c6d5-4738-90e9-fc0bef3c2dd3",
 "lesson_number": 4,
 "title": "Responding to Themes",
 "description": "Building an informed personal response: theme, thesis, tone and precise textual support.",
 "content_html": L4_CONTENT,
 "exam_tip_html": L4_TIP,
 "conclusion_html": L4_CONC,
 "hero_image_caption": "Poet speaking at a podium — exploring how writers communicate their ideas (Wikimedia Commons)",
 "hero_keywords": ["poet reading aloud", "poetry reading audience", "person writing notebook"],
 "practice_questions": [
   {"text": "Explore in detail one other poem from your anthology cluster which presents a loyalty that is tested. Begin with a one-sentence thesis and prove it.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems present an attitude the speaker finds hard to admit. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which presents a comfort that does not last. Support every point with a short, exact quotation.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems shift in tone, and what each shift reveals about the speaker's attitude. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which could reasonably be read in more than one way. Offer both readings and justify your preference.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Compare how these poems present a judgement the speaker makes about someone else. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
 ],
 "knowledge_checks": [
   {"type": "mcq", "q": "What makes a personal response informed rather than merely personal?",
    "options": ["It describes how the poem made you feel", "It is an argument about the poet's purpose supported by textual evidence", "It compares the poem to your own life", "It summarises the poem in your own words"], "correct": 1},
   {"type": "mcq", "q": "Which of these is a theme rather than a subject?",
    "options": ["A soldier's funeral", "A winter pond", "The failure of ritual to comfort the grieving", "Two people walking"], "correct": 2},
   {"type": "fill", "q": "A one-sentence statement of the argument your response will prove is called a _____.",
    "options": ["thesis", "summary", "refrain", "premise"], "correct": 0},
   {"type": "fill", "q": "Offering a second possible reading of a line shows that you recognise other _____ responses are possible.",
    "options": ["valid", "personal", "modern", "simple"], "correct": 0},
   {"type": "match", "q": "Match each planning step to what it produces:",
    "left": ["Question the task phrase", "Write one sentence naming an attitude", "Check the sentence could be argued against"],
    "right": ["A sharper focus than the poem's general topic", "A thesis every paragraph can prove", "Confirmation that it is an interpretation, not a summary"],
    "order": [0, 1, 2]},
 ],
 "flashcard_questions": [
   {"q": "What three things does the first assessment objective reward?", "a": "A critical style; an informed personal response; textual references that support interpretation."},
   {"q": "How are the two objectives weighted in part (b) of the poetry section?", "a": "Equally, so the argument matters as much as the method analysis."},
   {"q": "What is the difference between a poem's subject and its theme?", "a": "The subject is what happens; the theme is what the poet wants you to think about it."},
   {"q": "What is a thesis in an essay on poetry?", "a": "A one-sentence statement of the argument the response will prove."},
   {"q": "How can you test whether a thesis is an interpretation?", "a": "Check that somebody could reasonably disagree with it."},
   {"q": "Why do the qualifying words in a task matter so much?", "a": "They narrow the focus and decide which poem and which lines you should use."},
   {"q": "What is the risk of repeating the task wording too often?", "a": "Examiners find it intrusive and it replaces analysis with restatement."},
   {"q": "What is the difference between tone and attitude?", "a": "Tone is the poem's voice; attitude is the position that voice takes."},
   {"q": "Why is a tonal shift worth writing about?", "a": "It gives a structural point and a thematic point in one observation."},
   {"q": "Why is offering an alternative reading rewarded?", "a": "The specification expects candidates to recognise that different valid responses exist."},
   {"q": "How is part (b) of the poetry section written?", "a": "From memory, because the chosen poem is not printed on the paper."},
   {"q": "How many quotations per cluster poem are enough to prepare?", "a": "Three: one for the central idea, one for the strongest image, one from the ending."},
   {"q": "Why should quotations be tagged by theme rather than by title?", "a": "The task names a theme, so evidence is easier to find under pressure."},
   {"q": "Why is reading a quotation a poor way to revise it?", "a": "Recognition is not recall, and the exam demands recall."},
 ],
 "glossary_terms": [
   {"term": "thesis", "definition": "A one-sentence statement of the argument a response will prove, written before the first paragraph."},
   {"term": "attitude", "definition": "The speaker's position towards the subject, which may differ from the poet's own view."},
   {"term": "critical style", "definition": "Writing that argues about a text and weighs interpretations, rather than retelling what happens in it."},
   {"term": "tonal shift", "definition": "A change of voice or mood partway through a poem, often marking a change in the speaker's thinking."},
 ],
})

# ---------------------------------------------------------------- L5 (centrepiece)
L5_CONTENT = "\n\n".join([
 '<h2 data-narration-id="@">One Unseen Poem, One Cluster Poem, One Theme</h2>',

 '<p data-narration-id="@">This is the skill the poetry section is built around. You are given a named poem from your '
 'anthology cluster and an unfamiliar poem chosen to link to it, both printed on the paper, and a single instruction: '
 'compare how they present the theme the task names. Twenty marks turn on how well you hold the two poems together.</p>',

 kf("Cover this and recall what happens to an answer that discusses only one of the two poems, however good it is.",
    'A response that writes about only one of the two poems &mdash; the anthology poem or the unseen one &mdash; cannot '
    'rise beyond the lower mark bands, no matter how skilled the analysis. Both poems must be present throughout. '
    'Analysis of method is the dominant objective in this part, so the comparison must be about <em>how</em> each poet '
    'writes, not only about what each poem says.'),

 '<h2 data-narration-id="@">Step One: Read the Unseen Poem Through the Theme</h2>',

 '<p data-narration-id="@">Read the task first, then the unseen poem with that theme in your hand. You are not trying to '
 'understand everything the poem does; you are trying to find what it says about the one idea you have been asked about. '
 'Annotate only against that idea. Anything else is time you will want later.</p>',

 '<h2 data-narration-id="@">Step Two: Decide Whether They Agree</h2>',

 '<p data-narration-id="@">This is the decision that shapes the whole answer, and it is where responses most often go '
 'wrong. Students assume that because two poems are linked by theme, the poets must think alike. They frequently do '
 'not. A '
 '<dfn class="term" data-def="The shared idea that joins the unseen poem to the named anthology poem in the exam task; '
 'it does not mean the poets share a view.">thematic link</dfn> guarantees a common subject, not a common attitude.</p>',

 coll("Three kinds of connection worth writing about", [
   '<strong>Same idea, different feeling.</strong> Both poems may mourn a lost love, but one is bitter and one is calm. '
   'The shared idea gives you the paragraph; the difference in feeling gives you the point.',
   '<strong>Same feeling, different method.</strong> Both poems build unease &mdash; one through broken lines and '
   'caesura, the other through a widening stanza that will not close. Identical effects reached by opposite means make '
   'excellent comparative writing.',
   '<strong>Direct disagreement.</strong> Sometimes the unseen poem contradicts your anthology poem outright. Say so, '
   'plainly, and use the clash as the spine of the response. This is the strongest structure available to you.']),

 '<h2 data-narration-id="@">Step Three: Build a Grid in Five Minutes</h2>',

 '<p data-narration-id="@">Draw four rows down the margin of your answer booklet &mdash; idea and attitude, tone, '
 'language, structure &mdash; and two columns, one per poem. Fill it with short quotations only. Those four rows are the '
 'three bullet prompts the task gives you, split so that method has two rows instead of one. Each completed row is a '
 'paragraph, already comparative before you write a sentence.</p>',

 kf("Close this and draw the four-row comparison grid from memory, then fill it for any two poems you know.",
    'The grid is the plan. Four rows &mdash; idea and attitude, tone, language, structure &mdash; and two columns, one '
    'for the anthology poem and one for the unseen poem. Five minutes spent filling it saves you from the block '
    'structure that costs marks, because every row already contains both poems.'),

 '<h2 data-narration-id="@">Step Four: Write Alternately, Not in Blocks</h2>',

 '<p data-narration-id="@">The weakest structure discusses poem one for three paragraphs, then poem two for three '
 'paragraphs, then compares briefly at the end. The strongest is '
 '<dfn class="term" data-def="A comparison in which both texts appear inside every paragraph, rather than being handled '
 'in separate blocks.">interwoven comparison</dfn>: one comparative idea per paragraph, both poems inside it, evidence '
 'from each.</p>',

 '<p data-narration-id="@"><dfn class="term" data-def="Words such as whereas, similarly and by contrast that signal the '
 'relationship between two texts inside a single sentence.">Comparative connectives</dfn> carry that structure '
 '&mdash; <em>whereas</em>, <em>by contrast</em>, '
 '<em>similarly</em>, <em>where one poet does this, the other does that</em>. Use them honestly. A connective promising '
 'similarity in front of a point that is not similar reads worse than no connective at all.</p>',

 '<h2 data-narration-id="@">A Worked Comparison</h2>',

 '<p data-narration-id="@">Suppose the anthology poem is Emily Bront&euml;&rsquo;s &lsquo;Love and Friendship&rsquo; and '
 'the unseen poem is Thomas Hardy&rsquo;s &lsquo;Neutral Tones&rsquo;, with the task asking how the poems present love '
 'that has failed.</p>',

 coll("One interwoven paragraph, annotated", [
   'Both poets judge love through the natural world, but they reach opposite verdicts. Bront&euml; sets &ldquo;Love is '
   'like the wild rose-briar&rdquo; against &ldquo;Friendship like the holly-tree&rdquo;, using the seasonal cycle as a '
   'test that love fails and friendship survives: the holly will &ldquo;bloom most constantly&rdquo;. Hardy allows no '
   'such consolation. His speaker recalls how &ldquo;We stood by a pond that winter day&rdquo;, and the pond offers '
   'neither renewal nor endurance &mdash; only stillness.',
   'The comparison then moves to method. Bront&euml;&rsquo;s regular quatrains and simple similes make her argument feel '
   'settled, almost proverbial, as though the lesson has already been learned. Hardy&rsquo;s image of a sun that is '
   '&ldquo;white, as though chidden of God&rdquo; drains the scene of warmth and colour, so that the failure of love is '
   'presented not as a lesson but as a stain the speaker cannot wash out.',
   'Notice what the paragraph does not do. It never summarises either poem, it quotes no more than a handful of words at '
   'a time, and it never leaves one poem to fetch the other. Every sentence keeps both texts in view.']),

 '<h2 data-narration-id="@">Three Things Not to Do</h2>',

 '<p data-narration-id="@">Do not summarise the poems before comparing them; the examiner has both texts in front of '
 'them. Do not save comparison for the conclusion. And do not invent context for the unseen poem &mdash; you cannot know '
 'who wrote it or when, and background earns no marks in this section anyway.</p>',
])

L5_TIP = ('<p data-narration-id="@">Open with a comparative thesis, not with the anthology poem. A first sentence that '
          'names the relationship between the two poems &mdash; agreement, contrast, or a shared idea reached by '
          'different routes &mdash; tells the examiner immediately that the response is a comparison and not two essays '
          'stapled together.</p>')

L5_CONC = ('<h3 data-narration-id="@">Key Takeaways</h3>\n<ul>\n'
           '<li data-narration-id="@">Both poems must appear throughout; a response covering only one cannot pass the '
           'lower bands.</li>\n'
           '<li data-narration-id="@">A thematic link guarantees a shared subject, never a shared attitude &mdash; look '
           'for the disagreement.</li>\n'
           '<li data-narration-id="@">Plan with a four-row grid and write interwoven paragraphs rather than one poem '
           'after the other.</li>\n</ul>')

LESSONS.append({
 "lesson_id": "50585cf6-b6db-4202-b235-517ac8b8ff76",
 "lesson_number": 5,
 "title": "Linking the Unseen Poem to Your Anthology Cluster",
 "description": "Linking a printed unseen poem to your anthology cluster poem in one interwoven comparison.",
 "content_html": L5_CONTENT,
 "exam_tip_html": L5_TIP,
 "conclusion_html": L5_CONC,
 "hero_image_caption": "Open poetry book in natural setting — comparing unfamiliar texts side by side",
 "hero_keywords": ["two open books side by side", "poetry book outdoors", "reading two pages"],
 "practice_questions": [
   {"text": "Compare how these poems present the ending of love. Write about both poems in every paragraph. [In the exam, one poem is named from your anthology cluster and the other is unseen; both are printed.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems present a wish that cannot be granted. Build your response around the clearest disagreement between the two poets. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems create unease. Give particular attention to cases where the poets achieve a similar effect by opposite means. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems present the way people remember. Plan with a four-row grid before writing, then use one comparative idea per paragraph. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Compare how these poems present a person who is absent. Open with a comparative thesis that names the relationship between the two poems. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Explore in detail one other poem from your anthology cluster which presents a bond that survives hardship. Do not compare it with either poem above.",
    "type": TYPE_B, "marks": RUBRIC_B},
 ],
 "knowledge_checks": [
   {"type": "mcq", "q": "A student writes brilliantly about the unseen poem but never mentions the anthology poem. What happens to the mark?",
    "options": ["It is unaffected because the analysis is strong", "It cannot rise beyond the lower bands", "It is halved automatically", "It is treated as a rubric infringement and scored zero"], "correct": 1},
   {"type": "mcq", "q": "What does a thematic link between the two poems actually guarantee?",
    "options": ["That both poets share the same attitude", "That both poems use the same form", "That both poems address the same subject or idea", "That both poems were written in the same century"], "correct": 2},
   {"type": "fill", "q": "Writing about one poem and then the other in separate blocks is weak; the stronger approach is an _____ comparison.",
    "options": ["interwoven", "extended", "evaluative", "abbreviated"], "correct": 0},
   {"type": "fill", "q": "Because the poet of the unseen poem is not identified, you must never invent _____ for it.",
    "options": ["context", "imagery", "tone", "structure"], "correct": 0},
   {"type": "match", "q": "Match each kind of connection to an example of it:",
    "left": ["Same idea, different feeling", "Same feeling, different method", "Direct disagreement"],
    "right": ["Both poems mourn a lost love, but one is bitter and the other calm", "Both build unease — one through caesura, the other through a stanza that will not close", "Bronte trusts constancy where Hardy finds only coldness"],
    "order": [0, 1, 2]},
 ],
 "flashcard_questions": [
   {"q": "What two poems are printed for the comparison part of the poetry section?", "a": "A named poem from your anthology cluster and a thematically linked unseen poem."},
   {"q": "What is the mark ceiling for a comparison that covers only one of the two poems?", "a": "The lower bands, whatever the quality of the analysis."},
   {"q": "Which objective is dominant in the poetry comparison?", "a": "Analysis of the poet's methods rather than personal response."},
   {"q": "What should you read before reading the unseen poem?", "a": "The task, so you know which theme to annotate against."},
   {"q": "Does a thematic link mean the two poets share an attitude?", "a": "No. It guarantees only a shared subject or idea."},
   {"q": "Give the first of the three kinds of connection worth writing about.", "a": "Same idea, different feeling."},
   {"q": "What makes same feeling, different method a strong comparative point?", "a": "The poets reach one effect by opposite technical routes."},
   {"q": "What are the four rows of the comparison grid?", "a": "Idea and attitude; tone; language; structure."},
   {"q": "How long should the comparison grid take to complete?", "a": "About five minutes."},
   {"q": "Why does a completed grid row become a paragraph?", "a": "Each row already holds evidence from both poems, so the paragraph is comparative from the start."},
   {"q": "What is interwoven comparison?", "a": "Writing in which both poems appear inside every paragraph rather than in separate blocks."},
   {"q": "Why must comparative connectives be used honestly?", "a": "A word promising similarity in front of a contrasting point weakens the argument."},
   {"q": "Where should the comparison begin in your response?", "a": "In the opening thesis, not in the conclusion."},
   {"q": "Why should you avoid summarising the poems?", "a": "The examiner has both texts in front of them, so summary earns nothing."},
 ],
 "glossary_terms": [
   {"term": "thematic link", "definition": "The shared idea that joins the unseen poem to the named anthology poem in the exam task; it does not mean the poets share a view."},
   {"term": "interwoven comparison", "definition": "A comparison in which both texts appear inside every paragraph, rather than being handled in separate blocks."},
   {"term": "Comparative connectives", "definition": "Words such as whereas, similarly and by contrast that signal the relationship between two texts inside a single sentence."},
 ],
})

# ---------------------------------------------------------------- L6
L6_CONTENT = "\n\n".join([
 '<h2 data-narration-id="@">The Paper in Numbers</h2>',

 '<p data-narration-id="@">Everything in this lesson comes from three figures. The poetry and Shakespeare paper is '
 '<strong>two hours</strong> long, worth <strong>80 marks</strong>, and taken '
 '<dfn class="term" data-def="An exam sat without the set texts; no anthology and no play may be brought into the '
 'room.">closed text</dfn> &mdash; no anthology, no play, nothing on the desk. Eighty marks in a hundred and twenty '
 'minutes gives you exactly one and a half minutes per mark, and every timing below is that figure applied.</p>',

 kf("Cover this and recall the four numbers: paper length, total marks, marks per section, and marks per poetry part.",
    'Two hours. Eighty marks. Forty marks for the poetry section and forty for the Shakespeare section, so an even hour '
    'each. Inside the poetry hour, part (a) and part (b) are worth <strong>twenty marks each</strong> &mdash; so they '
    'deserve <strong>thirty minutes each</strong>, planning included.'),

 '<h2 data-narration-id="@">The Poetry Hour, Minute by Minute</h2>',

 '<div class="timeline" data-narration-id="@">\n'
 '  <div class="timeline-event"><div class="timeline-date">0&ndash;5 min</div><h4>Read the task, then both poems</h4>'
 '<p>Task first so you know the theme. Then read the anthology poem and the unseen poem, annotating only against that '
 'theme.</p></div>\n'
 '  <div class="timeline-event"><div class="timeline-date">5&ndash;8 min</div><h4>Fill the comparison grid</h4>'
 '<p>Idea and attitude, tone, language, structure &mdash; two columns, short quotations only.</p></div>\n'
 '  <div class="timeline-event"><div class="timeline-date">8&ndash;30 min</div><h4>Write part (a)</h4>'
 '<p>A comparative thesis, then three or four interwoven paragraphs. Both poems in every paragraph.</p></div>\n'
 '  <div class="timeline-event"><div class="timeline-date">30&ndash;34 min</div><h4>Choose and plan part (b)</h4>'
 '<p>Pick a different poem from your cluster and write your thesis sentence before you start.</p></div>\n'
 '  <div class="timeline-event"><div class="timeline-date">34&ndash;58 min</div><h4>Write part (b)</h4>'
 '<p>Detailed exploration of that single poem. No comparison.</p></div>\n'
 '  <div class="timeline-event"><div class="timeline-date">58&ndash;60 min</div><h4>Check and move on</h4>'
 '<p>Check quotations, then leave for the Shakespeare section on the hour whatever state the answer is in.</p></div>\n'
 '</div>',

 kf("Close this and explain why part (b) must not be rushed, using the mark allocation as your reason.",
    'Part (b) is the most commonly rushed answer on this paper. Examiners report that responses are often brief, as if '
    'timing had been forgotten under pressure. It carries exactly the same twenty marks as the comparison. A thin part '
    '(b) costs as much as a thin part (a), and it is the easier of the two to fix.'),

 '<h2 data-narration-id="@">Rubric Mistakes That Cost Whole Answers</h2>',

 '<p data-narration-id="@">A <dfn class="term" data-def="Breaking the instructions of the paper, such as writing about '
 'the wrong poem, which limits the mark however good the writing is.">rubric infringement</dfn> is not a failure of '
 'skill. It is a failure of reading the instructions, and it caps an answer that might otherwise have scored well. '
 'These four are the ones examiners see every year.</p>',

 coll("Four errors that are not about writing quality at all", [
   '<strong>Answering on only one poem in part (a).</strong> The comparison must cover the anthology poem and the unseen '
   'poem together.',
   '<strong>Choosing a part (b) poem from a different cluster</strong>, or one that has been removed from the current '
   'anthology. Check your cluster list before the exam, not during it.',
   '<strong>Re-using the part (a) anthology poem in part (b).</strong> The task says <em>one other poem</em>, and it '
   'means it.',
   '<strong>Comparing in part (b).</strong> No comparison is required there, and it steals the time you need for close '
   'analysis of one text.']),

 '<h2 data-narration-id="@">What a Strong Answer Looks Like on the Page</h2>',

 '<p data-narration-id="@">Length is not the mark. Examiners report very long scripts &mdash; some running to fifteen '
 'sides or more &mdash; whose quality was damaged by their quantity, with the same point restated through a parade of '
 'different quotations. Three or four developed, interwoven paragraphs beat eight thin ones.</p>',

 '<p data-narration-id="@">Keep quotations <dfn class="term" data-def="Placing a short quotation inside your own '
 'sentence rather than setting it out separately.">embedded</dfn> and short. Four well-placed words prove more than a '
 'copied-out stanza, and they leave room for the analysis that actually earns the mark.</p>',

 '<h2 data-narration-id="@">Two Practical Points About the Booklet</h2>',

 '<p data-narration-id="@">Spelling, punctuation and grammar are not assessed in the poetry section, so do not spend '
 'your final minutes proofreading. Legibility is a different matter: examiners regularly report scripts they struggle '
 'to decipher even when magnified. A mark cannot be given for a word that cannot be read.</p>',

 '<p data-narration-id="@">Label your answers clearly as part (a) and part (b), and start part (b) on a fresh page. It '
 'costs nothing and it removes any doubt about which poem belongs to which task.</p>',

 coll("A four-week timed practice plan", [
   '<strong>Week one.</strong> Untimed. Take an unfamiliar short poem, spend fifteen minutes filling a comparison grid '
   'against a cluster poem, and write nothing else. Grid practice is the highest-value drill there is.',
   '<strong>Week two.</strong> Thirty minutes for part (a) alone, twice. Mark yourself on one question only: does every '
   'paragraph contain both poems?',
   '<strong>Week three.</strong> Thirty minutes for part (b) alone, twice, on different cluster poems. Check your '
   'quotations against the text afterwards and count the misquotations.',
   '<strong>Week four.</strong> The full poetry hour, both parts, in one sitting, twice. This is the only drill that '
   'tests whether you can stop part (a) on time.']),

 '<h2 data-narration-id="@">The Final Check</h2>',

 '<p data-narration-id="@">Before you turn the page: does part (a) discuss both poems in every paragraph? Does part (b) '
 'cover a different poem from your own cluster, without comparison? Have you explained the effect of every method you '
 'named? If all three answers are yes, the answer is doing what the mark scheme asks.</p>',
])

L6_TIP = ('<p data-narration-id="@">Set a hard stop for part (a) at the thirty-minute mark and obey it. Almost every '
          'student who runs short on this paper does so because the comparison felt like it was going well. The marks '
          'you lose in a rushed part (b) are worth more than the marks you gain from a fourth comparison '
          'paragraph.</p>')

L6_CONC = ('<h3 data-narration-id="@">Key Takeaways</h3>\n<ul>\n'
           '<li data-narration-id="@">Two hours, eighty marks, closed text: one and a half minutes per mark, an hour for '
           'the poetry section, thirty minutes for each twenty-mark part.</li>\n'
           '<li data-narration-id="@">Part (b) carries the same marks as the comparison and is the answer most often '
           'rushed.</li>\n'
           '<li data-narration-id="@">Three or four developed interwoven paragraphs beat eight thin ones; length is not '
           'the mark.</li>\n</ul>')

LESSONS.append({
 "lesson_id": "d88323aa-2611-4bd2-80be-299975c28abd",
 "lesson_number": 6,
 "title": "Exam Technique & Timed Practice",
 "description": "The poetry hour minute by minute: mark-based timings, rubric traps and a four-week plan.",
 "content_html": L6_CONTENT,
 "exam_tip_html": L6_TIP,
 "conclusion_html": L6_CONC,
 "hero_image_caption": "Three clocks showing different times — managing exam timing across multiple questions (Photo: AlphaTradeZone / Pexels)",
 "hero_keywords": ["clock exam hall", "wall clock time", "student writing exam"],
 "practice_questions": [
   {"text": "In exactly 30 minutes: compare how these poems present a difficult decision. Stop when the time is up, whether or not you have finished. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "In exactly 30 minutes: explore in detail one other poem from your anthology cluster which presents an unwelcome truth. Write from memory, without your anthology.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Complete the full poetry hour in one sitting. Part (a): compare how these poems present the effect of the past on the present. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "Complete the full poetry hour in one sitting. Part (b): explore in detail one other poem from your cluster which presents an experience the speaker cannot share.",
    "type": TYPE_B, "marks": RUBRIC_B},
   {"text": "Spend only 5 minutes planning, then 25 minutes writing: compare how these poems present anger. Judge your answer solely on whether both poems appear in every paragraph. [In the exam, both poems are printed for you.]",
    "type": TYPE_A, "marks": RUBRIC_A},
   {"text": "In exactly 30 minutes: explore in detail one other poem from your anthology cluster which presents hope. Afterwards, check every quotation against the text and count your misquotations.",
    "type": TYPE_B, "marks": RUBRIC_B},
 ],
 "knowledge_checks": [
   {"type": "mcq", "q": "How long is the poetry and Shakespeare paper, and how many marks is it worth?",
    "options": ["90 minutes and 60 marks", "2 hours and 80 marks", "2 hours 15 minutes and 96 marks", "105 minutes and 80 marks"], "correct": 1},
   {"type": "mcq", "q": "How much of the paper should the poetry section take?",
    "options": ["30 minutes", "45 minutes", "60 minutes", "90 minutes"], "correct": 2},
   {"type": "fill", "q": "Eighty marks in a hundred and twenty minutes gives you one and a _____ minutes per mark.",
    "options": ["quarter", "half", "third", "fifth"], "correct": 1},
   {"type": "fill", "q": "The poetry and Shakespeare paper is taken _____ text, so no anthology is allowed on the desk.",
    "options": ["closed", "open", "annotated", "printed"], "correct": 0},
   {"type": "match", "q": "Match each stage of the poetry hour to its timing:",
    "left": ["Read the task and both poems", "Fill the comparison grid", "Write the comparison answer"],
    "right": ["The first 5 minutes", "Minutes 5 to 8", "Minutes 8 to 30"],
    "order": [0, 1, 2]},
 ],
 "flashcard_questions": [
   {"q": "How long is the poetry and Shakespeare paper?", "a": "Two hours."},
   {"q": "How many marks is the whole poetry and Shakespeare paper worth?", "a": "80 marks."},
   {"q": "How many minutes should you spend per mark on this paper?", "a": "One and a half."},
   {"q": "How many marks does each part of the poetry section carry?", "a": "Twenty marks each."},
   {"q": "How many minutes should each part of the poetry section take?", "a": "Thirty, including planning."},
   {"q": "What does closed text mean for this paper?", "a": "No anthology or play may be taken into the exam."},
   {"q": "What should you read before reading either poem?", "a": "The task, so you annotate against the right theme."},
   {"q": "Which answer on this paper is most often rushed?", "a": "Part (b) of the poetry section."},
   {"q": "Why is re-using the part (a) anthology poem in part (b) a mistake?", "a": "The task requires one other poem from the cluster."},
   {"q": "Is comparison required in part (b) of the poetry section?", "a": "No, and attempting it wastes time needed for close analysis."},
   {"q": "How many developed paragraphs should a comparison answer aim for?", "a": "Three or four, interwoven."},
   {"q": "Why does an unusually long script often score less well?", "a": "Quality is diluted as the same point is restated through more quotations."},
   {"q": "What does it mean to embed a quotation?", "a": "To place a few quoted words inside your own sentence."},
   {"q": "Why should you not proofread spelling in the poetry section?", "a": "Written accuracy is not assessed there, so the minutes are better spent elsewhere."},
   {"q": "Why does handwriting still matter even though accuracy is not assessed?", "a": "A mark cannot be given for a word the examiner cannot read."},
 ],
 "glossary_terms": [
   {"term": "embedded", "definition": "Placing a short quotation inside your own sentence rather than setting it out separately."},
   {"term": "closed text", "definition": "An exam sat without the set texts; no anthology and no play may be brought into the room."},
   {"term": "rubric infringement", "definition": "Breaking the instructions of the paper, such as writing about the wrong poem, which limits the mark however good the writing is."},
 ],
})


# ---------------------------------------------------------------- assemble
def renumber(lesson):
    counter = {"n": 0}

    def rep(_m):
        counter["n"] += 1
        return 'data-narration-id="n%d"' % counter["n"]

    for field in ("content_html", "exam_tip_html", "conclusion_html"):
        lesson[field] = re.sub(r'data-narration-id="@"', rep, lesson[field])
    return counter["n"]


out = []
for L in LESSONS:
    total = renumber(L)
    words = len(re.sub(r"<[^>]+>", " ", L["content_html"]).split())
    dfns = len(re.findall(r'class="term"', L["content_html"]))
    print("L%d %-46s words=%4d narration=n1..n%-3d dfn=%d gloss=%d fc=%d"
          % (L["lesson_number"], L["title"], words, total, dfns, len(L["glossary_terms"]), len(L["flashcard_questions"])))
    if total < 19:
        print("   !! narration max %d < 19 — existing manifest ids would be orphaned" % total)
    if dfns != len(L["glossary_terms"]):
        print("   !! dfn count %d != glossary_terms %d" % (dfns, len(L["glossary_terms"])))
    out.append(L)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\nWrote %s" % OUT)
