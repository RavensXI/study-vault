# -*- coding: utf-8 -*-
"""Seed an OCR J352 poetry-cluster rebuild (Towards a World Unknown, Version 2).

Writes, per cluster: the build context doc (spec_md), the assessment-rules doc,
the source-text doc (fact-check authority), the deterministic quote-gate corpus,
plan.json, state.json and the driver config.

Ten poems per cluster are held in full (data/canonical_poems/ocr-*). Five per
cluster were introduced in Version 2 and are in copyright: for those the only
source is OCR's own Version 2 teacher guide, and the only quotable spans are the
curated allow-list below (every entry copied verbatim from that guide).

Usage:  python scripts/api_build/setup_ocr_cluster.py conflict
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = r"C:\Users\tshau\Documents\Study Vault"
SCRATCH = (r"C:\Users\tshau\AppData\Local\Temp\claude"
           r"\C--Users-tshau-Documents-Study-Vault"
           r"\88006801-843c-4d74-957a-5eebdef537b9\scratchpad\ocr")
POEMS = os.path.join(REPO, "data", "canonical_poems")
GUIDES = os.path.join(SCRATCH, "guides")
KIT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"

SUBJECT_ID = "641eba47-cb5b-4210-8c3e-29812629bbba"   # english-literature-ocr

# --------------------------------------------------------------------------
# Assessment context — every statement below is taken from the J352 spec
# (Version 3.0, Nov 2025) or the published J352/02 sample assessment materials.
# Nothing here is inferred.
# --------------------------------------------------------------------------
ASSESSMENT = """# OCR GCSE (9-1) English Literature J352 — component 02 assessment rules

These statements come from the OCR specification (Version 3.0) and from OCR's
published sample question paper and mark scheme for J352/02. They are the ONLY
authority on exam structure for this unit. Anything not stated here must not be
claimed.

## The paper
- Exploring poetry and Shakespeare is one of the two examined components of the
  GCSE. It is a CLOSED TEXT examination of two hours, worth 80 marks, and it
  carries 50% of the qualification.
- It has two sections. Poetry across time is worth 40 marks and 25% of the
  whole GCSE. The Shakespeare section is worth the other 40 marks.
- Students answer two questions in total: one on the poetry cluster they have
  studied and one on the Shakespeare play they have studied.

## The poetry question
- There is one question on each of the three clusters (Love and Relationships,
  Conflict, Youth and Age). Students answer the question on their own cluster.
- That question is split into two compulsory parts, a) and b). Both must be
  answered.
- The paper prints two poems above the question: the named poem from the OCR
  Poetry Anthology and an unseen poem thematically linked to it.
- Part a) is worth 20 marks. It asks students to COMPARE how the two printed
  poems present or explore a stated idea. It carries three bullet points telling
  students what to consider: ideas and attitudes in each poem; tone and
  atmosphere in each poem; the effects of the language and structure used.
- Part b) is worth 20 marks. It asks students to explore in detail ONE OTHER
  poem from their anthology, of their own choice, that treats a related idea.
  That poem is NOT printed on the paper.
- The paper advises students to spend about 45 minutes on part a) and about
  30 minutes on part b).

## Assessment objectives
- The qualification has four assessment objectives. AO1: read, understand and
  respond to texts, maintaining a critical style, developing an informed
  personal response, and using textual references including quotations. AO2:
  analyse the language, form and structure used by a writer to create meanings
  and effects, using relevant subject terminology. AO3: show understanding of
  the relationships between texts and the contexts in which they were written.
  AO4: use a range of vocabulary and sentence structures for clarity, purpose
  and effect, with accurate spelling and punctuation.
- The poetry section assesses AO1 and AO2 ONLY. AO3 and AO4 are not assessed in
  the poetry section, so there are no context marks and no marks for spelling
  and punctuation there.
- Across the two parts, part a) places more weight on AO2 than on AO1, and
  part b) weights AO1 and AO2 equally. OCR publishes no per-question mark split
  between the assessment objectives, so no such split may ever be stated.

## Hard limits on what may be claimed
- Do NOT state a per-AO mark allocation for either part. It does not exist.
- Do NOT reproduce, paraphrase or imitate OCR's level of response band
  descriptors, and never use "Level 1"-style band names.
- Do NOT invent extra parts, extra questions, a choice of poetry questions
  within a cluster, or timings other than the advice above.
- The anthology may not be taken into the exam.
"""

HOUSE_RULES = """## StudyVault house rules for this unit (non-negotiable)

- British English spelling and punctuation throughout.
- Never reproduce or paraphrase an exam board's level descriptors. Where the
  lesson needs to talk about how answers are banded, use StudyVault's neutral
  vocabulary only: Top band, Upper-mid band, Mid band, Lower-mid band, Low band.
  Never write "Level 4", "Level 5" or similar.
- Never use board paper codes or specification codes in student-facing text.
  Write "the poetry section", "part a)", "part b)", "the comparison task",
  "the second part". NEVER write "J352", "component 02", "Section A",
  "Paper 1", "Paper 2" or any similar shorthand anywhere in the lesson.
- Never name the exam board as an actor ("OCR wants...", "the examiner is
  looking for..."). Describe the task, not the board's supposed preferences.
- practice_questions: exactly 6 per lesson. The "marks" field is the StudyVault
  rubric as a string, using Mastering / Secure / Developing / Emerging. Never a
  number, never a board level descriptor. A rubric must never credit context or
  spelling and punctuation: the poetry section assesses AO1 and AO2 only.
- knowledge_checks: exactly 5 per lesson, and exactly this mix — 2 of type
  "mcq", 2 of type "fill", 1 of type "match". Use the canonical shapes: an mcq
  carries "options" plus "correct" (the integer index); never an "answers"
  array.
- flashcard_questions: 12 per lesson (the platform validator rejects fewer than
  8 or more than 15). Follow FLASHCARD_RULES.md: use at least two of the English
  Literature card types (character to defining quote, quote to speaker, quote to
  one-line analysis, theme to evidence, technique to example). Each answer is 30
  words or fewer, no two cards in the deck share an answer, no answer is a list
  of items ("X, Y and Z"), and no answer restates its own question. A one-word
  answer is only allowed when the question begins What / Who / When / Which /
  Name / Give / State, or the answer is a number or a date. Never write an
  essay-style card ("How does the poet present...").
- description: under 100 characters.
- Question fields (practice text, knowledge checks, flashcards, glossary) are
  plain text with real unicode characters. Only the *_html fields use entities.
- Write for GCSE students aged 15 to 16.
"""

# --------------------------------------------------------------------------
# The clusters. Order is the OCR anthology's own ordering principle: poets in
# order of birth year (verified against the 2020 printed contents, which is
# strictly chronological), with the five Version 2 poems merged into that order.
# --------------------------------------------------------------------------
CLUSTERS = {
    "conflict": {
        "unit_slug": "poetry-conflict",
        "unit_name": "Poetry: Conflict",
        "subtitle": "All fifteen poems of the OCR Conflict cluster",
        "accent": "#2563eb",
        "folder": "ocr-conflict",
        "theme": "Conflict",
        "removed": [
            ("A Poison Tree", "William Blake"),
            ("The Man He Killed", "Thomas Hardy"),
            ("Anthem for Doomed Youth", "Wilfred Owen"),
            ("Punishment", "Seamus Heaney"),
            ("Phrase Book", "Jo Shapcott"),
        ],
        "poems": [
            {"t": "Envy", "p": "Mary Lamb", "d": "1764-1847", "f": "envy",
             "desc": "Lamb's rose-tree that cannot bear violets: discontent, envy and self-acceptance."},
            {"t": "Boat Stealing", "p": "William Wordsworth", "d": "1770-1850", "f": "boat-stealing",
             "desc": "Wordsworth's stolen boat and the looming peak: guilt, awe and a boy's inner conflict."},
            {"t": "The Destruction of Sennacherib", "p": "Lord Byron", "d": "1788-1824",
             "f": "the-destruction-of-sennacherib",
             "desc": "Byron's galloping account of an army destroyed in a night: power, faith and sudden ruin."},
            {"t": "Songs for the People", "p": "Frances E. W. Harper", "d": "1825-1911", "g": "songs-for-the-people",
             "desc": "Harper's ballad vision of songs that silence war: peace, justice and a music for all."},
            {"t": "There's a Certain Slant of Light", "p": "Emily Dickinson", "d": "1830-1886",
             "f": "there-s-a-certain-slant-of-light",
             "desc": "Dickinson's oppressive winter light: despair, difference and a hurt that leaves no scar."},
            {"t": "Colonization in Reverse", "p": "Louise Bennett", "d": "1919-2006", "g": "colonization-in-reverse",
             "desc": "Bennett's comic Windrush reversal in Jamaican Creole: migration, empire and turned tables."},
            {"t": "Vergissmeinnicht", "p": "Keith Douglas", "d": "1920-1944", "f": "vergissmeinnicht",
             "desc": "Douglas returns to a dead gunner and his girlfriend's photograph: love, decay and war."},
            {"t": "What Were They Like?", "p": "Denise Levertov", "d": "1923-1997", "f": "what-were-they-like",
             "desc": "Levertov's questions and answers about a destroyed Vietnamese culture: erasure and silence."},
            {"t": "Lament", "p": "Gillian Clarke", "d": "b. 1937", "f": "lament",
             "desc": "Clarke's litany of Gulf War casualties, human and animal: ecological grief and blame."},
            {"t": "Flag", "p": "John Agard", "d": "b. 1949", "f": "flag",
             "desc": "Agard's question-and-answer on the cloth that makes men die: patriotism and conscience."},
            {"t": "Honour Killing", "p": "Imtiaz Dharker", "d": "b. 1954", "f": "honour-killing",
             "desc": "Dharker strips off veil, skin and country: oppression, identity and a new geography."},
            {"t": "Partition", "p": "Sujata Bhatt", "d": "b. 1956", "f": "partition",
             "desc": "Bhatt's doctor sewing wounds after 1947: trauma, silence and a divided homeland."},
            {"t": "Papa-T", "p": "Fred D'Aguiar", "d": "b. 1960", "g": "papa-t",
             "desc": "D'Aguiar's grandfather reciting Tennyson in Guyana: memory, empire and a dissenting voice."},
            {"t": "We Lived Happily during the War", "p": "Ilya Kaminsky", "d": "b. 1977",
             "g": "we-lived-happily-during-the-war",
             "desc": "Kaminsky's confession of comfortable silence: complicity, money and the guilt of not acting."},
            {"t": "Thirteen", "p": "Caleb Femi", "d": "b. 1990", "g": "thirteen",
             "desc": "Femi's boy stopped by police at thirteen: prejudice, lost promise and stars turned dark."},
        ],
    },
    "love-and-relationships": {
        "unit_slug": "poetry-love-and-relationships",
        "unit_name": "Poetry: Love and Relationships",
        "subtitle": "All fifteen poems of the OCR Love and Relationships cluster",
        "accent": "#1e40af",
        "folder": "ocr-love-and-relationships",
        "theme": "Love and Relationships",
        "removed": [
            ("A Broken Appointment", "Thomas Hardy"),
            ("Fin de Fete", "Charlotte Mew"),
            ("The Sorrow of True Love", "Edward Thomas"),
            ("An Arundel Tomb", "Philip Larkin"),
            ("Long Distance II", "Tony Harrison"),
        ],
        "poems": [
            {"t": "A Song", "p": "Helen Maria Williams", "d": "1761-1827", "f": "a-song",
             "desc": "Williams's speaker prizes her lover's heart above riches while he braves the sea for gain."},
            {"t": "Bright Star", "p": "John Keats", "d": "1795-1821", "f": "bright-star",
             "desc": "Keats's sonnet longs for a star's steadfastness while resting on his love: desire and death."},
            {"t": "Now", "p": "Robert Browning", "d": "1812-1889", "f": "now",
             "desc": "Browning compresses a whole life into one moment of meeting: intensity and the eternal now."},
            {"t": "Love and Friendship", "p": "Emily Bronte", "d": "1818-1848", "f": "love-and-friendship",
             "desc": "Bronte sets the sweet rose-briar of love against the constant holly of friendship."},
            {"t": "Looking at Your Hands", "p": "Martin Carter", "d": "1927-1997", "g": "looking-at-your-hands",
             "desc": "Carter's protest poem joins love and politics: hands, dreams and changing the world."},
            {"t": "Love After Love", "p": "Derek Walcott", "d": "1930-2017", "f": "love-after-love",
             "desc": "Walcott greets the self at your own door: recovery, self-love and a feast of return."},
            {"t": "Morning Song", "p": "Sylvia Plath", "d": "1932-1963", "f": "morning-song",
             "desc": "Plath's new mother listens in the night: distance, tenderness and an unsettling love."},
            {"t": "Poem for My Love", "p": "June Jordan", "d": "1936-2002", "g": "poem-for-my-love",
             "desc": "Jordan's late love poem of stars, night and possibility: calm, wonder and the body."},
            {"t": "I Wouldn't Thank You for a Valentine", "p": "Liz Lochhead", "d": "b. 1947",
             "f": "i-wouldn-t-thank-you-for-a-valentine",
             "desc": "Lochhead's comic rejection of romance cliches: independence and a sharper kind of love."},
            {"t": "In Paris With You", "p": "James Fenton", "d": "b. 1949", "f": "in-paris-with-you",
             "desc": "Fenton's bruised speaker refuses romance and offers the present tense instead."},
            {"t": "Flirtation", "p": "Rita Dove", "d": "b. 1952", "g": "flirtation",
             "desc": "Dove's peeled orange and quiet night: the wordless beginning of an attraction."},
            {"t": "Warming Her Pearls", "p": "Carol Ann Duffy", "d": "b. 1955", "f": "warming-her-pearls",
             "desc": "Duffy's maid warms her mistress's pearls: desire, class and unspoken longing."},
            {"t": "Dusting the Phone", "p": "Jackie Kay", "d": "b. 1961", "f": "dusting-the-phone",
             "desc": "Kay's speaker waits obsessively for a call: longing, hope and the ache of modern love."},
            {"t": "The Perseverance", "p": "Raymond Antrobus", "d": "b. 1986", "g": "the-perseverance",
             "desc": "Antrobus waits outside his father's pub: deafness, love and the patience a bond demands."},
            {"t": "Lullaby", "p": "Fatimah Asghar", "d": "b. 1990", "g": "lullaby",
             "desc": "Asghar imagines her dead parents dancing in the underworld: grief turned to celebration."},
        ],
    },
    "youth-and-age": {
        "unit_slug": "poetry-youth-and-age",
        "unit_name": "Poetry: Youth and Age",
        "subtitle": "All fifteen poems of the OCR Youth and Age cluster",
        "accent": "#3b82f6",
        "folder": "ocr-youth-and-age",
        "theme": "Youth and Age",
        "removed": [
            ("When I have fears that I may cease to be", "John Keats"),
            ("Spring and Fall: to a Young Child", "Gerard Manley Hopkins"),
            ("Ode", "Arthur O'Shaughnessy"),
            ("Red Roses", "Anne Sexton"),
            ("Farther", "Owen Sheers"),
        ],
        "poems": [
            {"t": "Holy Thursday", "p": "William Blake", "d": "1757-1827", "f": "holy-thursday",
             "desc": "Blake's charity children fill St Paul's: innocence, pity and the adults who watch them."},
            {"t": "The Bluebell", "p": "Anne Bronte", "d": "1820-1849", "f": "the-bluebell",
             "desc": "Bronte's single bluebell recalls a free childhood and sharpens an adult's thankless life."},
            {"t": "Midnight on the Great Western", "p": "Thomas Hardy", "d": "1840-1928",
             "f": "midnight-on-the-great-western",
             "desc": "Hardy's journeying boy travels alone towards a world unknown: innocence and mystery."},
            {"t": "Out, Out", "p": "Robert Frost", "d": "1874-1963", "f": "out-out",
             "desc": "Frost's boy loses his hand to a buzz-saw: sudden death and the world that moves on."},
            {"t": "Theme for English B", "p": "Langston Hughes", "d": "1901-1967", "g": "theme-for-english-b",
             "desc": "Hughes's student writes a page for his instructor: race, youth and what makes a self true."},
            {"t": "Baby Song", "p": "Thom Gunn", "d": "1929-2004", "f": "baby-song",
             "desc": "Gunn's newborn complains at the cold, bright world: birth, comfort and separation."},
            {"t": "You're", "p": "Sylvia Plath", "d": "1932-1963", "f": "you-re",
             "desc": "Plath's riddling images of an unborn child: expectation, humour and fierce affection."},
            {"t": "Cold Knap Lake", "p": "Gillian Clarke", "d": "b. 1937", "f": "cold-knap-lake",
             "desc": "Clarke's drowned girl pulled from the lake: memory, doubt and what childhood keeps."},
            {"t": "My First Weeks", "p": "Sharon Olds", "d": "b. 1942", "f": "my-first-weeks",
             "desc": "Olds recalls a first fortnight of plenty, then rationed nights: appetite and character."},
            {"t": "Venus's-flytraps", "p": "Yusef Komunyakaa", "d": "b. 1947", "f": "venus-s-flytraps",
             "desc": "Komunyakaa's five-year-old among tall yellow flowers: danger, questions and secrets."},
            {"t": "Love", "p": "Kate Clanchy", "d": "b. 1965", "f": "love",
             "desc": "Clanchy's mother meets her strange, fragile newborn: awe, ignorance and the start of love."},
            {"t": "Happy Birthday Moon", "p": "Raymond Antrobus", "d": "b. 1986", "g": "happy-birthday-moon",
             "desc": "Antrobus and his father read together: deafness, patience and finally hearing each other."},
            {"t": "Prayer", "p": "Zaffar Kunial", "d": "b. circa 1987", "g": "prayer",
             "desc": "Kunial links his own birth to his mother's death: breath, faith and two languages."},
            {"t": "Tea With Our Grandmothers", "p": "Warsan Shire", "d": "b. 1988", "g": "tea-with-our-grandmothers",
             "desc": "Shire commemorates two grandmothers from Somalia to Wales: survival, food and language."},
            {"t": "Equilibrium", "p": "Theresa Lola", "d": "b. 1994", "g": "equilibrium",
             "desc": "Lola sets her brother's birth against her grandfather's decline: the cycle of life."},
        ],
    },
}

# --------------------------------------------------------------------------
# Curated quotable spans for the five guide-only poems in each cluster.
# EVERY entry appears verbatim inside OCR's Version 2 teacher guide for that
# poem. Titles, book titles, biographical labels and OCR's own commentary are
# deliberately excluded. Where OCR mis-transcribes a line from another writer
# it is excluded and the reason recorded in EXCLUDED.
# --------------------------------------------------------------------------
QUOTABLE = {
    "colonization-in-reverse": [
        "tun history upside dung", "de motherlan", "motherlan",
        "bag an baggage", "loyalty", "Miss Mattie",
    ],
    "papa-t": [
        "no-nonsense recitals", "our sweet seasalter", "good lickin",
        "that tongue", "tin-soldiering", "to hear", "to disobey",
        # Tennyson, quoted by OCR as the poem D'Aguiar's grandfather recites:
        "do and die",
    ],
    "we-lived-happily-during-the-war": [
        "We lived happily during the war", "they bombed other people's houses",
        "Not enough", "of money", "America was falling", "invisible house",
        "forgive us", "falling",
    ],
    "thirteen": [
        "horizon in the east", "black holes", "thirteen", "stars",
        "You will watch the two men cast lots for your organs",
    ],
    "songs-for-the-people": [
        "songs for the people", "more abundant life", "hearts of men",
        "bright and restful mansions",
    ],
    "looking-at-your-hands": [
        "dear friend", "looking at your hands", "dream to change the world",
        "a room without a light", "walking in the sun", "hands", "fire",
    ],
    "poem-for-my-love": [
        "womanly mirage", "possibility", "stars",
    ],
    "flirtation": [
        "no need to say anything", "a tulip on a wedgewood plate",
        "walking through", "topiary",
    ],
    "the-perseverance": [
        "man overstanding", "having the big picture", "overstanding",
        "perseverance", "serves",
    ],
    "lullaby": [
        "their way back", "light the underworld", "winks the dark",
        "dirt skies and worm stars",
    ],
    "theme-for-english-b": [
        "I hear New York too", "Bessie, bop, or Bach", "instructor", "true", "bop",
    ],
    "happy-birthday-moon": [
        "really hear each other", "white space", "I'd like to be the Moon",
    ],
    "prayer": [
        "hurled language's hurt", "God's breath in man returning to his birth",
        "heaven and earth", "birth",
    ],
    "tea-with-our-grandmothers": [
        "tally of surviving",
    ],
    "equilibrium": [
        "numbered", "wailed",
    ],
}

EXCLUDED = {
    "papa-t": ["'stormed at with shock and shell' — OCR mis-transcribes Tennyson "
               "('The Charge of the Light Brigade'). Never quote Tennyson in this lesson."],
    "songs-for-the-people": ["'clash of sabres' and 'new songs' — OCR's paraphrase, not "
                             "reliably the poem's wording."],
    "theme-for-english-b": ["every span containing 'coloured' — OCR anglicises Hughes's "
                            "American spelling, so those spans are not verbatim. Paraphrase "
                            "instead: the speaker is the only Black student in his class."],
}


def read(p):
    return io.open(p, encoding="utf-8").read()


def build_source_doc(cl):
    """The fact-check authority: ten full poem texts plus OCR's guides plus the
    curated allow-lists."""
    c = CLUSTERS[cl]
    out = ["# SOURCE TEXTS — OCR Poetry Anthology, %s cluster (Version 2)" % c["theme"], "",
           "This document is the ONLY source for quotations in this unit.", "",
           "Ten poems appear below as FULL TEXT. Five appear as GUIDE ONLY: those poems are",
           "in copyright and their text is not reproduced here, so OCR's own teacher-guide",
           "commentary is given instead, followed by the exact list of spans that may be",
           "quoted from them. A quotation from a GUIDE ONLY poem that is not on its list is",
           "a fabrication.", ""]
    for i, p in enumerate(c["poems"], 1):
        head = "\n\n" + "=" * 78 + "\nPOEM %d: %s — %s (%s)\n" % (i, p["t"], p["p"], p["d"])
        if "f" in p:
            out.append(head + "STATUS: FULL TEXT\n" + "=" * 78 + "\n")
            out.append(read(os.path.join(POEMS, c["folder"], p["f"] + ".txt")).strip())
        else:
            out.append(head + "STATUS: GUIDE ONLY (poem text not reproduced)\n" + "=" * 78 + "\n")
            out.append(read(os.path.join(GUIDES, c["folder"], p["g"] + ".md")).strip())
            out.append("\n--- QUOTABLE SPANS for '%s' (the complete list; nothing else from "
                       "this poem may be placed inside quotation marks) ---" % p["t"])
            for s in QUOTABLE[p["g"]]:
                out.append("  * %s" % s)
            for note in EXCLUDED.get(p["g"], []):
                out.append("  ! DO NOT QUOTE: %s" % note)
    return "\n".join(out) + "\n"


GATE_EXCLUDE = {
    "papa-t": ["shock and shell"],
    "songs-for-the-people": ["clash of sabres", "new songs"],
    "theme-for-english-b": ["coloured"],
}

_SPAN_RE = re.compile(
    "‘([^’]{2,400})’|“([^”]{2,400})”|\"([^\"]{2,400})\"")


def guide_quoted_spans(path, exclude):
    """Every span OCR itself places inside quotation marks in a teacher guide,
    minus the spans we refuse to let anyone quote. Extracted mechanically so no
    span is ever retyped by hand."""
    text = read(path)
    for marker in ("Links for further research", "Need to get in touch?"):
        i = text.find(marker)
        if i > 0:
            text = text[:i]
    out = []
    for m in _SPAN_RE.finditer(text):
        s = next(g for g in m.groups() if g)
        s = re.sub(r"\s+", " ", s).strip()
        if any(bad.casefold() in s.casefold() for bad in exclude):
            continue
        if s not in out:
            out.append(s)
    return out


def build_gate_corpus(cl):
    """Deterministic gate corpus: the ten full poem texts, the curated quotable
    spans for the five guide-only poems, and every other span OCR's own guide
    places inside quotation marks (persona names, book titles, interview quotes
    the lesson may legitimately attribute). OCR's running prose is deliberately
    NOT included, so commentary cannot be passed off as a line of verse, and the
    spans we refuse to trust are filtered out entirely."""
    c = CLUSTERS[cl]
    parts = []
    for p in c["poems"]:
        if "f" in p:
            parts.append(read(os.path.join(POEMS, c["folder"], p["f"] + ".txt")))
        else:
            spans = list(QUOTABLE[p["g"]])
            spans += [s for s in guide_quoted_spans(
                os.path.join(GUIDES, c["folder"], p["g"] + ".md"),
                GATE_EXCLUDE.get(p["g"], [])) if s not in spans]
            parts.append("\n".join(spans))
    return "\n\n".join(parts) + "\n"


def build_context(cl):
    c = CLUSTERS[cl]
    lines = [
        "# OCR GCSE English Literature (J352) — Poetry Anthology: %s — build context" % c["theme"],
        "",
        ASSESSMENT,
        "",
        "## The cluster",
        "",
        "The OCR Poetry Anthology is called *Towards a World Unknown*. Its content was",
        "updated for first teaching in September 2022 (Version 2) and first examined in",
        "June 2024. The %s cluster now contains exactly these fifteen poems, and this" % c["theme"],
        "unit teaches one lesson on each, in this order:",
        "",
    ]
    for i, p in enumerate(c["poems"], 1):
        lines.append("%2d. %s — %s (%s)" % (i, p["t"], p["p"], p["d"]))
    lines += [
        "",
        "### Poems REMOVED from this cluster in Version 2 — never teach or mention them",
        "",
    ]
    for t, p in c["removed"]:
        lines.append("- %s — %s" % (t, p))
    lines += [
        "",
        "These five are no longer on the specification. Naming one as an anthology poem,",
        "or offering it as a comparison partner, would send students to revise material",
        "they cannot be assessed on. Poems from other boards' anthologies (AQA Power and",
        "Conflict, AQA Love and Relationships, the Edexcel clusters, the Eduqas anthology)",
        "are equally out of scope. The only poems that may be named as anthology poems are",
        "the fifteen listed above.",
        "",
        "## Sources and the quotation rule",
        "",
        "The SOURCE TEXTS section below is the only place a quotation may come from.",
        "",
        "- Ten of the fifteen poems are given in FULL TEXT. Quote freely from them, in",
        "  short phrases of roughly two to eight words, always copied character for",
        "  character. Never reproduce a whole stanza or a whole poem.",
        "- Five of the fifteen are in copyright and are given as OCR's own teaching",
        "  commentary instead, followed by a closed list of QUOTABLE SPANS. For those five",
        "  poems you may place inside quotation marks ONLY a span from that list. Every",
        "  other statement about the poem must be drawn from what the commentary supports:",
        "  its situation, its speaker, its themes, the poet's life, and the formal features",
        "  the commentary names (for example a pantoum, a ballad stanza, enjambment between",
        "  named stanzas, a stated simile or metaphor). Do not invent a line, do not invent",
        "  a stanza count, and do not describe wording you have not been given.",
        "- CRITICAL: the lesson must read as a complete, confident lesson on the poem, the",
        "  same as the other ten. Never tell the student that source material was limited,",
        "  never label a poem as guide-based, never write anything like 'read the full poem",
        "  in your anthology because we cannot print it here', and never apologise for the",
        "  amount of quotation. Write with authority about what you do know. Quoting a",
        "  little and analysing well is normal for a poetry lesson.",
        "- The structural reference lesson supplied to you elsewhere is from a different",
        "  board's anthology. Match its shape only. Never quote or name any poem from it.",
        "",
        "## What each lesson contains",
        "",
        "One lesson, one poem. Cover: what happens in the poem and who speaks it; the poet",
        "and the context that shaped it; the themes it develops within the %s idea;" % c["theme"],
        "its form and structure; its key language and imagery, taught through short exact",
        "quotations with real analysis of effect; and the comparison work. OCR's own",
        "'Connections and contrasts with other anthology poems' lists appear in the source",
        "material for the five newer poems and are a good guide to the pairings students",
        "should know; for every lesson, name at least three OTHER poems from the fifteen",
        "and say precisely what a comparison of methods would draw out.",
        "",
        "CRITICAL — what those pairings are FOR. The paper never asks students to compare",
        "two anthology poems. Part a) always compares the printed anthology poem with the",
        "printed unseen poem; part b) explores one other anthology poem on its own. So",
        "in-cluster pairings are revision links — they help a student choose and prepare a",
        "part b) poem, and they build the comparison muscle that part a) needs. Say that.",
        "Never present a two-anthology-poem comparison as an exam task, and never write a",
        "practice question that asks for one.",
        "",
        "Because part a) pairs the printed anthology poem with an UNSEEN poem, every lesson",
        "should also build transferable comparison skill: how to read an unfamiliar poem",
        "quickly for its ideas and attitudes, tone and atmosphere, and the effects of",
        "language and structure, and how to hold two poems in balance rather than writing",
        "about them one after the other. Because part b) asks for one other anthology poem",
        "from memory, the lesson should flag the highest-value short quotations to learn.",
        "",
        HOUSE_RULES,
        "",
        "## SOURCE TEXTS",
        "",
        build_source_doc(cl),
    ]
    return "\n".join(lines)


def build_plan(cl):
    c = CLUSTERS[cl]
    lessons = []
    for i, p in enumerate(c["poems"], 1):
        title = "%s — %s" % (p["t"], p["p"])
        if len(title) > 46:
            title = p["t"]
        lessons.append({
            "number": i,
            "title": title,
            "description": p["desc"],
            "spec_references": ["Poetry across time"],
            "section_markers": ["POEM %d: %s — %s" % (i, p["t"], p["p"])],
        })
    return {
        "subject": {"name": "English Literature", "slug": "english-literature-ocr",
                    "exam_board": "OCR", "spec_code": "J352", "school_id": None},
        "article_units": [{
            "name": c["unit_name"], "slug": c["unit_slug"], "subtitle": c["subtitle"],
            "body_class": "unit-" + c["unit_slug"],
            "accent": c["accent"], "accent_light": c["accent"] + "22",
            "accent_badge": c["accent"] + "33",
            "lesson_count": 15, "lessons": lessons,
        }],
        "practice_units": [],
        "question_type_names": ["20 marks — Anthology and Unseen Comparison",
                                "20 marks — Single Poem Exploration"],
        "teaching_brief": {
            "unit_shape": ("One lesson per anthology poem, fifteen in all, in anthology order. "
                           "No skills lessons and no overview lessons."),
            "per_lesson": ("The poem's situation and speaker; the poet and the context that "
                           "shaped the poem; its themes within the %s idea; form and structure; "
                           "key language and imagery taught through short exact quotations with "
                           "analysis of effect; at least three named comparison partners from the "
                           "other fourteen poems in this cluster with the specific method or idea "
                           "each comparison would draw out; and how the poem serves both parts of "
                           "the poetry question." % c["theme"]),
            "quotations": ("Verbatim from the supplied source texts only, two to eight words, in "
                           "quotation marks. For the five poems supplied as commentary plus a "
                           "quotable-span list, quote ONLY from that list. Never quote a poem "
                           "outside the fifteen. Never quote from memory."),
            "practice_mix": ("6 practice questions per lesson, alternating the two registered "
                             "types. A comparison question ALWAYS pairs THIS poem with an UNSEEN "
                             "poem, described only by its theme or situation (for example 'an "
                             "unseen poem in which a speaker regrets staying silent') — never "
                             "with a second anthology poem, because the paper never sets that "
                             "task. A single-poem question explores ONE anthology poem on its "
                             "own. Mark schemes use the StudyVault rubric, reward only response, "
                             "textual reference and analysis of language, form and structure, and "
                             "never award credit for context, since the poetry section assesses "
                             "AO1 and AO2 only."),
            "audience": ("GCSE students aged 15 to 16 revising for a closed-text exam. The named "
                         "poem in part a) is printed on the paper, but the poem chosen for "
                         "part b) is not, so short memorable quotations matter."),
        },
    }


def main(cl):
    if cl not in CLUSTERS:
        raise SystemExit("unknown cluster: %s (want one of %s)" % (cl, ", ".join(CLUSTERS)))
    c = CLUSTERS[cl]
    run_dir = os.path.join(SCRATCH, "run-" + cl)
    os.makedirs(run_dir, exist_ok=True)

    ctx = os.path.join(SCRATCH, "context_%s.md" % cl)
    src = os.path.join(SCRATCH, "source_%s.md" % cl)
    gate = os.path.join(SCRATCH, "gate_%s.txt" % cl)
    rules = os.path.join(SCRATCH, "assessment_j352_02.md")

    io.open(ctx, "w", encoding="utf-8").write(build_context(cl))
    io.open(src, "w", encoding="utf-8").write(build_source_doc(cl))
    io.open(gate, "w", encoding="utf-8").write(build_gate_corpus(cl))
    io.open(rules, "w", encoding="utf-8").write(ASSESSMENT)

    plan = build_plan(cl)
    io.open(os.path.join(run_dir, "plan.json"), "w", encoding="utf-8").write(
        json.dumps(plan, ensure_ascii=False, indent=1))

    scope = ("OCR GCSE English Literature J352, poetry component, '%s' cluster of the OCR "
             "Poetry Anthology 'Towards a World Unknown' Version 2 (first teaching September "
             "2022). The cluster contains exactly these fifteen poems: %s. Any other poem "
             "named as an anthology poem is out of scope, including the five withdrawn in "
             "Version 2 (%s) and any poem from another board's anthology."
             % (c["theme"],
                "; ".join("'%s' by %s" % (p["t"], p["p"]) for p in c["poems"]),
                "; ".join("'%s' by %s" % (t, p) for t, p in c["removed"])))

    cfg = {
        "slug": "english-literature-ocr-" + cl,
        "subject_slug": "english-literature-ocr",
        "subject_name": "English Literature",
        "exam_board": "OCR",
        "spec_code": "J352",
        "spec_md": ctx,
        "factcheck_context_doc": src,
        "quote_gate_corpus": gate,
        "assessment_rules_doc": rules,
        "scope_statement": scope,
        "reference_lesson": os.path.join(KIT, "reference_lesson.json"),
        "docs_dir": os.path.join(REPO, "docs"),
        "validator": os.path.join(REPO, "scripts", "_validate_content_json.py"),
        "factcheck_out_dir": os.path.join(REPO, "scripts", "_fact_check"),
        "run_dir": run_dir,
    }
    cfg_path = os.path.join(REPO, "scripts", "api_build", "config_englit-ocr-%s.json" % cl)
    io.open(cfg_path, "w", encoding="utf-8").write(json.dumps(cfg, indent=1))

    st_path = os.path.join(run_dir, "state.json")
    st = json.load(io.open(st_path, encoding="utf-8")) if os.path.exists(st_path) else {}
    st["subject_id"] = SUBJECT_ID
    io.open(st_path, "w", encoding="utf-8").write(json.dumps(st, indent=1))

    print("cluster:", cl)
    print("  context   %s (%d chars)" % (ctx, os.path.getsize(ctx)))
    print("  source    %s (%d chars)" % (src, os.path.getsize(src)))
    print("  gate      %s (%d chars)" % (gate, os.path.getsize(gate)))
    print("  config    %s" % cfg_path)
    print("  run_dir   %s" % run_dir)
    print("  lessons   %d" % len(plan["article_units"][0]["lessons"]))


if __name__ == "__main__":
    main(sys.argv[1])
