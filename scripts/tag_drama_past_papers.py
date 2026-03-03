"""
Extract real OCR GCSE Drama (J316/04) past paper questions and tag them
in the Drama lesson practice questions in Supabase.

Papers with both question paper + mark scheme: June 2022, 2023, 2024, 2025
Papers with question paper only: November 2021

Maps Blood Brothers Section A questions to lessons:
- Costume → L4 (Costume Design)
- Voice → L7 (Voice & Physicality)
- Physicality → L7 (Voice & Physicality)
- Staging → L5 (Set & Staging)
- Lighting → L6 (Lighting, Sound & Atmosphere)
- Sound → L6 (Lighting, Sound & Atmosphere)
- Set design → L5 (Set & Staging)
- Director/Semiotics → L8 (The Director's Vision)
- Actor preparation/performance → L7 (Voice & Physicality)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
import pdfplumber
from supabase import create_client

# ─── Config ──────────────────────────────────────────────────────────────────

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(BASE)
PDF_DIR = os.path.join(PROJECT, "Spec and Materials", "Drama", "For TSH")

BLOOD_BROTHERS_UNIT_ID = "78edc667-c874-441a-98e0-2d99737c4060"
RISE_UP_UNIT_ID = "ea068fee-59c6-4c13-a842-05da92509418"

sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])


# ─── Manually curated past paper questions ────────────────────────────────────
# Each paper's Section A questions have been read from the PDFs and matched
# to the Blood Brothers character/line where applicable.
# The mark scheme guidance has been distilled into concise level descriptors.

PAST_PAPER_QUESTIONS = []

# ═══════════════════════════════════════════════════════════════════════════════
# NOVEMBER 2021 (no mark scheme file available — use generic level descriptors)
# ═══════════════════════════════════════════════════════════════════════════════

PAST_PAPER_QUESTIONS.extend([
    {
        "paper": "OCR November 2021",
        "topic": "voice",
        "lesson": 7,
        "text": "Select the character Mrs Johnstone from Blood Brothers. Describe two ways an actor playing this role could use voice effectively to perform the line: 'Mickey. Don\u2019t shoot Eddie. He\u2019s your brother. You had a twin brother.'",
        "type": "4 marks \u2014 Voice Skills",
        "marks": (
            "Level 2 (3\u20134 marks): Detailed description of two vocal techniques with clear explanation of how each communicates meaning. "
            "E.g. The actor could use a desperate, pleading tone with rising pitch on 'Don\u2019t shoot Eddie' to convey urgency and fear. "
            "A sudden drop in volume and a trembling voice on 'You had a twin brother' would show the weight of the secret being revealed, "
            "with a long pause before 'twin brother' to let the shock land for both Mickey and the audience.\n\n"
            "Level 1 (1\u20132 marks): Basic identification of one vocal technique with limited explanation. E.g. She would shout because she is scared."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "lighting",
        "lesson": 6,
        "text": "Explain two ways lighting could be used to develop the mood and atmosphere in one key moment in Blood Brothers.",
        "type": "4 marks \u2014 Lighting/Sound Design",
        "marks": (
            "Level 2 (3\u20134 marks): Two clearly explained lighting effects linked to mood/atmosphere at a specific moment. "
            "E.g. In the final scene, a harsh red wash could flood the stage to symbolise blood and danger, creating an atmosphere of impending tragedy. "
            "A tight spotlight on Mrs Johnstone isolated from the rest of the stage would draw the audience\u2019s focus to her horror and helplessness.\n\n"
            "Level 1 (1\u20132 marks): Basic identification of lighting with limited connection to mood. E.g. Use a spotlight to show the character."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "physicality",
        "lesson": 7,
        "text": "Choose a character from Blood Brothers. Suggest three ways an actor playing this character could use physicality for their performance at any moment in the performance text. Complete the boxes identifying the physicality the actor could use at that moment with an explanation for your choice.",
        "type": "6 marks \u2014 Physicality/Movement",
        "marks": (
            "2 marks per physicality (1 for identification + 1 for explanation), to a maximum of 6 marks.\n\n"
            "Level 2 (5\u20136 marks): Three clearly identified physical skills (gesture, gait, posture, facial expression, proximity, levels) "
            "each with a justified explanation linked to character and moment. E.g. Mickey as an adult could use hunched shoulders and a slow, heavy gait "
            "to show the weight of depression. Proximity \u2014 standing far from Linda with arms crossed to show emotional distance.\n\n"
            "Level 1 (1\u20132 marks): One or two basic physical skills identified with limited explanation."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "staging",
        "lesson": 5,
        "text": "Choose a staging style you could use to perform Blood Brothers. Explain three advantages and/or disadvantages of staging the performance in this way.",
        "type": "6 marks \u2014 Staging Type",
        "marks": (
            "2 marks per advantage/disadvantage (to a maximum of 6).\n\n"
            "2 marks: Identified aspect of the staging style with a potential advantage/disadvantage and some explanation to justify.\n"
            "1 mark: A potential advantage/disadvantage given with little or no attempt at justifying.\n\n"
            "Advantages might include: good sightlines, proximity of actors and audience, immersive atmosphere. "
            "Disadvantages might include: limited entrances/exits, set design restrictions, audience distraction."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "costume",
        "lesson": 4,
        "text": "Select the character Mr Lyons from Blood Brothers. Describe briefly three suitable items of costume for this character. Give a reason for using each item. Suggest how it will help to tell the audience about the character.",
        "type": "6 marks \u2014 Costume Design",
        "marks": (
            "2 marks per costume item (1 for identification + 1 for explanation), to a maximum of 6 marks.\n\n"
            "E.g. A well-tailored dark suit to show his wealth and status as a businessman. A blue tie to symbolise his Conservative political alignment "
            "and contrast with the Johnstone family\u2019s association with red/Labour. Polished leather shoes to communicate that he takes pride in his "
            "appearance and has the money to maintain it."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "director",
        "lesson": 8,
        "text": "Semiotics are used to provide visual clues to the audience. As a director, justify how you would use semiotics for the opening scene/section of Blood Brothers.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished description of how a range of signs and symbols may be used in the opening. "
            "Very clear explanation of how semiotics provide visual clues to the audience. E.g. The Narrator in a formal black suit symbolises fate/death. "
            "Mrs Johnstone\u2019s worn pink dress and bare legs communicate poverty but warmth. The two houses on opposite sides of the stage (SL/SR) "
            "immediately establish the class divide. A single magpie sound effect foreshadows superstition.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation of some signs and symbols with some connection to audience understanding.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation of one or two signs/symbols."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "sound",
        "lesson": 6,
        "text": "Discuss how sound can be used to communicate meaning to the audience in Blood Brothers. Give examples from the performance text, although not from the opening scene/section, to justify your answer.",
        "type": "8 marks \u2014 Lighting/Sound Design",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished selection of sound examples with very clear explanation of how they communicate meaning. "
            "E.g. The recurring magpie cackle (non-diegetic) reminds the audience of the superstition motif. Musical underscoring during "
            "'Marilyn Monroe' shows Mrs Johnstone\u2019s optimism. A gunshot sound effect in the final scene creates visceral shock. "
            "The song 'Tell Me It\u2019s Not True' uses diegetic music to communicate grief.\n\n"
            "Level 2 (4\u20136 marks): Clear identification of sound with some valid explanation.\n\n"
            "Level 1 (1\u20133 marks): Limited identification and explanation of sound."
        ),
    },
    {
        "paper": "OCR November 2021",
        "topic": "set",
        "lesson": 5,
        "text": "Explain how a set designer could show historical and/or cultural context at one key moment in Blood Brothers. As part of your answer, roughly sketch an annotated design to help explain the layout of the set.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of how set design communicates historical/cultural context. "
            "E.g. For the Skelmersdale relocation scene, the set could show a 1970s council estate with a playground, small gardens, "
            "and a bus stop \u2014 reflecting the real overspill estates built to move Liverpool families out of the slums. "
            "Faded red brick flats on the backdrop communicate working-class housing. Cultural context shown through a corner shop "
            "with period-appropriate signage and a milk float.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some historical/cultural detail.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with little or no contextual understanding."
        ),
    },
])

# ═══════════════════════════════════════════════════════════════════════════════
# JUNE 2022
# ═══════════════════════════════════════════════════════════════════════════════

PAST_PAPER_QUESTIONS.extend([
    {
        "paper": "OCR June 2022",
        "topic": "physicality",
        "lesson": 7,
        "text": "Select the character Mrs Johnstone from Blood Brothers. Identify two physical movements the character could use when saying the line: 'Tell me it\u2019s not true. Say it\u2019s just a story.' Explain how each movement communicates meaning.",
        "type": "4 marks \u2014 Physicality/Movement",
        "marks": (
            "1 mark for accurately identified physical movement, to a maximum of 2 marks. "
            "1 mark for explanation of how the movement communicates meaning, to a maximum of 2 marks.\n\n"
            "Blood Brothers \u2014 Mrs Johnstone: Her movements communicate that she is strong-willed, hardened to life\u2019s challenges, "
            "determined and stubborn but with a vulnerable side.\n"
            "\u2022 Feet apart \u2014 dominant, defiant, disbelieving.\n"
            "\u2022 Arms folded, or spread out pleading for it not to be true.\n"
            "\u2022 Stock still, or moving wildly about in despair.\n"
            "\u2022 Hunched shoulders, trying to be smaller, avoiding reality.\n"
            "\u2022 Turns away, refusing to watch the deaths.\n"
            "\u2022 Direct address to audience, arms outstretched begging for help."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "costume",
        "lesson": 4,
        "text": "Using the character Mrs Johnstone from Blood Brothers, suggest two appropriate items of costume for this character. Explain why each item of costume is appropriate for the character.",
        "type": "4 marks \u2014 Costume Design",
        "marks": (
            "1 mark for identified appropriate costume, to a maximum of 2 marks. "
            "1 mark for why the costume is appropriate, to a maximum of 2 marks.\n\n"
            "Blood Brothers \u2014 Mrs Johnstone: Costumes appropriate for a working-class housewife living hand to mouth on an estate.\n"
            "\u2022 Housewife clothes: skirt, torn stockings or bare legs, cardigan, scarf round head \u2014 all scruffy, worn, dirty.\n"
            "\u2022 Archetypal working-class married woman of the 1950s/60s, so period-appropriate garments.\n"
            "\u2022 Clothes for housework and child-minding, nothing fancy.\n"
            "\u2022 Slippers, even outdoors."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "staging",
        "lesson": 5,
        "text": "You are performing Blood Brothers on a thrust stage. Explain three advantages and/or disadvantages of performing on this style of stage. Give examples from the performance text to justify your response.",
        "type": "6 marks \u2014 Staging Type",
        "marks": (
            "2 marks per advantage/disadvantage (to a maximum of 6).\n"
            "2 marks: Identified aspect with justification. 1 mark: Advantage/disadvantage with little justification.\n\n"
            "Advantages: good sightlines, proximity of actors and audience, action moves forward into audience, "
            "creates intimate/threatening/comic atmosphere, actors feel immersed.\n"
            "Disadvantages: actors may feel intimidated, limited entrances/exits, audience may be distracted, "
            "set has design restrictions (viewed from many angles), every error becomes obvious.\n\n"
            "Note for Blood Brothers: Harder to find advantages with this style of play (it suits proscenium arch)."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "lighting",
        "lesson": 6,
        "text": "Choose a dramatic moment from Blood Brothers. As a lighting designer, describe three lighting effects you could use to create mood and atmosphere. Explain how the lighting creates mood and atmosphere.",
        "type": "6 marks \u2014 Lighting/Sound Design",
        "marks": (
            "1 mark for identifying a valid lighting effect, to a maximum of 3 marks. "
            "1 mark for each explanation of how the lighting creates mood and atmosphere, to a maximum of 3 marks.\n\n"
            "Answers should show knowledge of different forms: strobe, flashing, slow fades, coloured gels, blackouts, "
            "gobos, spotlights, pools of light, cross fades \u2014 all at different levels.\n"
            "Mood and atmosphere will vary by moment chosen: gloom, high tension, sadness, comedy, changes as plot unfolds.\n"
            "Candidates should tie lighting effects to a particular dramatic moment in the text."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "sound",
        "lesson": 6,
        "text": "As a sound designer, explain how you could create tension in the closing scene/section of Blood Brothers. Give examples from the performance text to justify your response.",
        "type": "6 marks \u2014 Lighting/Sound Design",
        "marks": (
            "Level 3 (5\u20136 marks): Accomplished selection of ways sound could be used in the closing scenes. "
            "Very clear explanation of how sound creates tension.\n\n"
            "Level 2 (3\u20134 marks): Clear ways sound could be used. Some valid explanation of tension.\n\n"
            "Level 1 (1\u20132 marks): Limited identification and explanation of sound in closing scenes.\n\n"
            "Sound might include voices, music, sound effects. Must reference the closing scenes/section."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "voice_physicality",
        "lesson": 7,
        "text": "Select the character Mickey from Blood Brothers. Describe the vocal and physical skills an actor playing Mickey could use to show emotion in one key moment. Give examples from the performance text to justify your response.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of how an actor would communicate emotion in a key moment. "
            "Accomplished understanding of physical and vocal skills to convey meaning with relevant examples from the text.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation of emotion. Clear understanding of physical and vocal skills "
            "with some justification and examples.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation of emotion and use of physical/vocal skills. "
            "Limited understanding with few examples.\n\n"
            "Focus is on vocal and physical skills: voice, mime, non-verbal communication, facial expression, proxemics, use of levels."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "director",
        "lesson": 8,
        "text": "Semiotics are used to provide visual clues to the audience. As a director, justify how you would use semiotics for one key moment of Blood Brothers.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished description of how a range of signs and symbols may be used in one key moment. "
            "Very clear explanation of how they provide visual clues to the audience.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation of some signs and symbols in one key moment.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation of one or two signs/symbols.\n\n"
            "Signs and symbols may include: scenery/set, stage furniture, props, masks/mime, staging, music/song, "
            "costume/personal items, lighting/sound, special effects."
        ),
    },
    {
        "paper": "OCR June 2022",
        "topic": "set",
        "lesson": 5,
        "text": "Give an example of a set design that could be used for the opening scene/section of Blood Brothers. Justify how the set design communicates meaning to the audience. Roughly sketch an annotated design to help explain the layout of the set.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation and justification of how set design communicates meaning "
            "in the opening scene/section. Effective examples from the text.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation and justification with some effective examples.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation/justification with few examples.\n\n"
            "Set design includes: backdrop, flies, scenery, staging, set lighting, furniture, and levels."
        ),
    },
])

# ═══════════════════════════════════════════════════════════════════════════════
# JUNE 2023
# ═══════════════════════════════════════════════════════════════════════════════

PAST_PAPER_QUESTIONS.extend([
    {
        "paper": "OCR June 2023",
        "topic": "physicality",
        "lesson": 7,
        "text": "Choose the character Mickey from Blood Brothers and the line: 'How old are y\u2019, Eddie?' Identify one facial expression and one movement the actor would use when saying this line. Explain how the facial expression and movement communicate meaning to the audience.",
        "type": "4 marks \u2014 Physicality/Movement",
        "marks": (
            "1 mark for accurately identified facial expression, 1 mark for identified movement (max 2 marks). "
            "1 mark for explanation of facial expression, 1 mark for explanation of movement (max 2 marks).\n\n"
            "Blood Brothers \u2014 Mickey: Mickey is seven years old meeting Eddie for the first time. "
            "His facial expressions and movements show curiosity, excitement, and childlike energy.\n"
            "\u2022 Wide-eyed expression of surprise/curiosity when realising they are the same age.\n"
            "\u2022 Animated hand gestures, jumping up and down with excitement.\n"
            "\u2022 Leaning forward eagerly, open mouth, broad grin.\n"
            "\u2022 Fidgeting, unable to stand still \u2014 showing childish energy."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "voice",
        "lesson": 7,
        "text": "Using the character Mickey from Blood Brothers, identify two ways an actor could use voice to show the character\u2019s personality at any moment in the performance text. Explain how each way of using voice shows the character\u2019s personality.",
        "type": "4 marks \u2014 Voice Skills",
        "marks": (
            "1 mark for identified vocal technique, to a maximum of 2 marks. "
            "1 mark for explanation of how it shows personality, to a maximum of 2 marks.\n\n"
            "Blood Brothers \u2014 Mickey: Vocal skills should reflect Mickey\u2019s personality at the chosen moment.\n"
            "\u2022 As a child: fast pace, high pitch, loud volume \u2014 showing energy and enthusiasm.\n"
            "\u2022 As a teenager: mumbling, dropping words, lower pitch \u2014 showing awkwardness and insecurity.\n"
            "\u2022 As an adult: slow pace, monotone delivery, quiet volume \u2014 showing depression and defeat.\n"
            "\u2022 In the final scene: shouting, cracking voice, erratic pace \u2014 showing desperation and anger."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "sound",
        "lesson": 6,
        "text": "Identify three sound effects you could use to create drama in one key moment of Blood Brothers. Describe what each sound effect communicates to the audience.",
        "type": "6 marks \u2014 Lighting/Sound Design",
        "marks": (
            "1 mark for identifying a valid sound effect, to a maximum of 3 marks. "
            "1 mark for description of what it communicates, to a maximum of 3 marks.\n\n"
            "Sound effects should be appropriate to the moment chosen and create a dramatic effect.\n"
            "\u2022 Gunshot \u2014 communicates violence and the fatal conclusion.\n"
            "\u2022 Magpie cackle \u2014 reinforces the superstition motif and sense of foreboding.\n"
            "\u2022 Heartbeat sound \u2014 builds tension and shows a character\u2019s fear.\n"
            "\u2022 Police sirens \u2014 communicate danger and the consequences of Sammy\u2019s crime.\n"
            "\u2022 Musical underscoring \u2014 creates mood (e.g. eerie music for the Narrator\u2019s warnings)."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "costume",
        "lesson": 4,
        "text": "You are the costume designer for Blood Brothers. Choose one character from the performance text. Identify three items of costume this character could wear that will show the audience something about their character. Explain what each item of costume shows the audience about the character.",
        "type": "6 marks \u2014 Costume Design",
        "marks": (
            "1 mark for identified costume item, to a maximum of 3 marks. "
            "1 mark for explanation of what it shows, to a maximum of 3 marks.\n\n"
            "Costume items should be appropriate for the character\u2019s age, class, time period, and personality. "
            "E.g. for Mickey as a child: grey shorts with darned patches (poverty), home-knitted socks (handmade = no money), "
            "scuffed leather shoes (well-worn = family cannot afford new). Red jumper to symbolise Labour/working class.\n"
            "For Edward: pressed grey shorts (quality material), manufactured socks, polished shoes, blue jumper (Conservative/wealth)."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "set",
        "lesson": 5,
        "text": "Describe how a set design could be used to communicate a setting (place and time) for one key moment in Blood Brothers.",
        "type": "6 marks \u2014 Staging Type",
        "marks": (
            "Level 3 (5\u20136 marks): Accomplished description of set design that clearly communicates place and time. "
            "Detailed reference to specific set elements and their semiotic meaning.\n\n"
            "Level 2 (3\u20134 marks): Clear description with some connection to place and time.\n\n"
            "Level 1 (1\u20132 marks): Limited description with basic reference to setting.\n\n"
            "E.g. For Mrs Johnstone\u2019s kitchen: a simple wooden table and mismatched chairs (poverty), "
            "a catalogue on the table (buying on credit), faded wallpaper (1960s period), bright colours despite poverty "
            "(reflects her cheerful personality). A truck could be used to wheel the set piece on and off."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "voice_physicality",
        "lesson": 7,
        "text": "You are an actor playing a character in the closing scene/section of Blood Brothers. Explain what skills you would use to communicate your role to the audience.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of acting skills (vocal and physical) used in the closing scene. "
            "Detailed understanding of how skills communicate the role to the audience with effective examples.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation of skills with some justification and examples.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with few examples.\n\n"
            "Skills include: voice (tone, pace, pitch, volume, accent, pause, emphasis), physicality (gesture, posture, "
            "facial expression, movement, proximity, levels), and how these communicate character and emotion."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "staging",
        "lesson": 5,
        "text": "You are staging a version of Blood Brothers. Explain why your chosen type of stage is suitable for performing the text.",
        "type": "8 marks \u2014 Staging Type",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of why the staging type is suitable, with detailed reference "
            "to specific scenes, technical requirements, and audience experience.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some relevant examples from the text.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to staging.\n\n"
            "Consider: sightlines, entrances/exits, set changes between multiple locations, audience proximity, "
            "technical capabilities (fly loft, wings, lighting rigs), and how the staging supports the play\u2019s themes."
        ),
    },
    {
        "paper": "OCR June 2023",
        "topic": "lighting",
        "lesson": 6,
        "text": "As a lighting designer, explain how you would use lighting to develop drama in the opening scene/section of Blood Brothers.",
        "type": "8 marks \u2014 Lighting/Sound Design",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of how lighting develops drama in the opening. "
            "Detailed understanding of lighting techniques (colour, intensity, direction, type) and their dramatic effect.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some relevant lighting examples.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to lighting.\n\n"
            "The opening begins with the flash-forward deaths then rewinds. Lighting could include: a cold blue/white wash "
            "for the death tableau, a slow crossfade to warm amber for the flashback, a spotlight on the Narrator, "
            "gobos to create shadow patterns suggesting fate and foreboding."
        ),
    },
])

# ═══════════════════════════════════════════════════════════════════════════════
# JUNE 2024
# ═══════════════════════════════════════════════════════════════════════════════

PAST_PAPER_QUESTIONS.extend([
    {
        "paper": "OCR June 2024",
        "topic": "costume",
        "lesson": 4,
        "text": "Choose the character Mrs Lyons from Blood Brothers. Suggest two items of costume the actor could wear in one key moment. Explain what each item of costume shows about the character.",
        "type": "4 marks \u2014 Costume Design",
        "marks": (
            "1 mark for accurately identifying an item of costume, to a maximum of 2 marks. "
            "1 mark for explaining what the costume shows about the character, to a maximum of 2 marks.\n\n"
            "Blood Brothers \u2014 Mrs Lyons: Costume should reflect her wealth, formality, and psychological state.\n"
            "\u2022 A well-tailored grey suit \u2014 showing her formal, controlled nature and wealth.\n"
            "\u2022 High heels \u2014 showing she does not have to do physical work.\n"
            "\u2022 As she deteriorates: black skirt and top to symbolise mourning/madness, wild unkempt hair, "
            "mismatched shoes to show she no longer cares about appearance.\n"
            "\u2022 A red cardigan to symbolise her anger and mistrust of Mrs Johnstone."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "voice",
        "lesson": 7,
        "text": "Using the character Mrs Lyons from Blood Brothers, select the line: 'I curse the day I met you. You ruined me.' Suggest two different ways the actor playing this role could use their voice to deliver the line effectively. Explain how using the voice in this way would tell something about the character to the audience.",
        "type": "4 marks \u2014 Voice Skills",
        "marks": (
            "1 mark for identifying a vocal technique, to a maximum of 2 marks. "
            "1 mark for explaining what it communicates, to a maximum of 2 marks.\n\n"
            "Blood Brothers \u2014 Mrs Lyons delivering 'I curse the day I met you. You ruined me.'\n"
            "\u2022 A venomous, hissing tone on 'curse' \u2014 showing her hatred and bitterness towards Mrs Johnstone.\n"
            "\u2022 Rising volume building to a shout on 'ruined me' \u2014 showing she has lost control of her emotions.\n"
            "\u2022 A sharp, clipped accent emphasising every word \u2014 showing her upper-class background even in anger.\n"
            "\u2022 A cracking, trembling voice \u2014 suggesting she is on the verge of a breakdown."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "physicality",
        "lesson": 7,
        "text": "Choose a character from Blood Brothers. Identify three facial expressions you would use as an actor playing this character to show what the character is feeling at one key moment. Explain how the facial expression shows what the character is feeling.",
        "type": "6 marks \u2014 Physicality/Movement",
        "marks": (
            "1 mark for identified facial expression, to a maximum of 3 marks. "
            "1 mark for explanation of what it shows, to a maximum of 3 marks.\n\n"
            "Facial expressions should be appropriate to the character and moment chosen. "
            "E.g. for Mickey in the final scene:\n"
            "\u2022 Wide, staring eyes \u2014 showing shock and disbelief at the truth about his twin.\n"
            "\u2022 Clenched jaw with teeth bared \u2014 showing barely contained rage and betrayal.\n"
            "\u2022 Tears streaming, mouth open in a silent scream \u2014 showing overwhelming grief and despair."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "lighting",
        "lesson": 6,
        "text": "Suggest three ways lighting would create atmosphere for the closing scene/section of Blood Brothers. Explain how each lighting effect creates atmosphere.",
        "type": "6 marks \u2014 Lighting/Sound Design",
        "marks": (
            "1 mark for identifying a lighting effect, to a maximum of 3 marks. "
            "1 mark for explanation of atmosphere created, to a maximum of 3 marks.\n\n"
            "Lighting for the closing scene (the shooting) should create tension, tragedy, and finality.\n"
            "\u2022 A harsh red wash flooding the stage \u2014 symbolising blood, danger, and the violence of the deaths.\n"
            "\u2022 A tight spotlight narrowing on Mickey as he holds the gun \u2014 isolating him and showing his desperation.\n"
            "\u2022 A sudden snap to blackout after the gunshots \u2014 creating shock and finality for the audience.\n"
            "\u2022 A slow fade to a cold blue wash for the aftermath \u2014 creating a sense of emptiness and grief."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "staging",
        "lesson": 5,
        "text": "You are performing Blood Brothers on a proscenium arch stage. Explain three advantages and/or disadvantages of using this stage for the performance text.",
        "type": "6 marks \u2014 Staging Type",
        "marks": (
            "2 marks per advantage/disadvantage (to a maximum of 6).\n"
            "2 marks: Identified aspect with justification. 1 mark: Advantage/disadvantage with little justification.\n\n"
            "Advantages: clear frame for audience, fly loft for scenery changes (many locations), "
            "wings for smooth entrances/exits, supports a composite set with Johnstone/Lyons houses on opposite sides, "
            "lighting rig allows complex design.\n"
            "Disadvantages: distance between audience and actors may reduce intimacy, "
            "4th wall limits direct address (though the Narrator breaks it), single viewpoint."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "voice_physicality",
        "lesson": 7,
        "text": "Choose one character from Blood Brothers. As an actor, explain how you would prepare to perform this character for one scene/section of the performance text.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of preparation, covering research (context, playwright\u2019s intentions), "
            "vocal and physical choices, character development, and rehearsal techniques.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation of preparation with some relevant detail.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to preparation.\n\n"
            "Preparation might include: reading the script closely, researching the social/historical context, "
            "analysing the character\u2019s journey, developing a backstory, experimenting with vocal delivery and physicality, "
            "working with other actors on proxemics and relationships."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "director",
        "lesson": 8,
        "text": "As a director, identify the mood you want to communicate for one key moment in Blood Brothers. You must not use the closing scene/section. Explain how you would create the mood.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of how to create a specific mood using a range of "
            "directorial tools (blocking, pace, actor direction, design elements). Effective examples from the text.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some relevant examples.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to mood.\n\n"
            "The mood must be identified and linked to a specific moment. The director should consider: "
            "how actors deliver lines, blocking and proxemics, lighting, sound, set, and costume choices."
        ),
    },
    {
        "paper": "OCR June 2024",
        "topic": "set",
        "lesson": 5,
        "text": "Design a set for the closing scene/section of Blood Brothers. Justify your design. Roughly sketch an annotated design to help explain the layout of the set.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished justification of set design for the closing scene. "
            "Detailed understanding of how set communicates meaning (the council chamber, the confrontation, the deaths). "
            "Effective use of levels, furniture, backdrop, and staging.\n\n"
            "Level 2 (4\u20136 marks): Clear justification with some effective examples.\n\n"
            "Level 1 (1\u20133 marks): Limited justification with basic reference to set.\n\n"
            "The closing scene takes place in the council chamber/town hall. Set might include: "
            "a lectern for Edward, formal seating, the Johnstone and Lyons houses visible in the background "
            "to remind the audience of the class divide that caused the tragedy."
        ),
    },
])

# ═══════════════════════════════════════════════════════════════════════════════
# JUNE 2025
# ═══════════════════════════════════════════════════════════════════════════════

PAST_PAPER_QUESTIONS.extend([
    {
        "paper": "OCR June 2025",
        "topic": "props",
        "lesson": 5,  # props relate to set/staging
        "text": "Select the character Mickey from Blood Brothers. Suggest two props the actor could use during a performance. Explain briefly what the use of the prop shows the audience about the character.",
        "type": "4 marks \u2014 Staging Type",
        "marks": (
            "1 mark for accurately identifying a suitable prop, to a maximum of 2 marks. "
            "1 mark for explaining what the prop shows, to a maximum of 2 marks.\n\n"
            "Blood Brothers \u2014 Mickey: Props should be appropriate to the character at relevant points.\n"
            "\u2022 As a child: a toy gun (Sammy\u2019s air pistol) \u2014 foreshadows the violence that will end his life.\n"
            "\u2022 As an adult: a bottle of antidepressant pills \u2014 shows his mental health decline and dependency.\n"
            "\u2022 As a child: sweets shared with Eddie \u2014 shows the innocence of their friendship.\n"
            "\u2022 The locket given by Mrs Johnstone \u2014 symbolises the secret bond between the twins."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "physicality",
        "lesson": 7,
        "text": "Choose a character from Blood Brothers. As an actor, describe how you would show two relevant emotions during the closing scene/section of the performance text.",
        "type": "4 marks \u2014 Physicality/Movement",
        "marks": (
            "1 mark for identifying a relevant emotion/physical approach, to a maximum of 2 marks. "
            "1 mark for describing how it is shown, to a maximum of 2 marks.\n\n"
            "Two emotions should be clearly identified and described with physical/vocal detail for the closing scene. "
            "E.g. as Mickey: (1) Rage \u2014 shaking hands gripping the gun, heavy rapid breathing, wild staring eyes, "
            "aggressive stance with feet planted wide. (2) Despair \u2014 collapsing to knees after learning the truth, "
            "tears streaming, voice cracking, reaching out towards Eddie."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "physicality",
        "lesson": 7,
        "text": "Choose a character who appears in the opening scene/section of Blood Brothers. Describe how an actor playing this role could use the way they sit or walk to show the audience three things about this character.",
        "type": "6 marks \u2014 Physicality/Movement",
        "marks": (
            "2 marks per point (1 for identifying the physicality + 1 for what it shows), to a maximum of 6.\n\n"
            "The way a character sits or walks (gait, posture, pace, rhythm) communicates status, mood, and personality.\n"
            "E.g. for the Narrator in the opening: slow, deliberate walk to centre stage \u2014 shows authority and control. "
            "Upright, straight-backed posture \u2014 shows formality and gravitas. Measured, even pace \u2014 suggests inevitability "
            "of fate. For Mrs Johnstone: quick, light steps \u2014 shows energy despite hardship. Tired slump when sitting \u2014 "
            "shows exhaustion of raising many children."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "sound",
        "lesson": 6,
        "text": "As a sound designer, explain three sound effects you would use to show the social, historical or cultural context of Blood Brothers. Give examples from the performance text to justify your answer.",
        "type": "6 marks \u2014 Lighting/Sound Design",
        "marks": (
            "1 mark for identified sound effect, to a maximum of 3 marks. "
            "1 mark for linking to social/historical/cultural context, to a maximum of 3 marks.\n\n"
            "Sound effects should demonstrate understanding of context.\n"
            "\u2022 Factory machinery sounds \u2014 historical context of industrial Liverpool in the 1960s\u201370s.\n"
            "\u2022 Beatles music playing on a radio \u2014 cultural context of 1960s Liverpool.\n"
            "\u2022 Children playing in the street \u2014 social context of working-class neighbourhood life.\n"
            "\u2022 Dole queue ambience / crowd murmuring \u2014 historical context of mass unemployment under Thatcher.\n"
            "\u2022 Church bells \u2014 cultural/religious context of Catholic working-class Liverpool."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "staging",
        "lesson": 5,
        "text": "You are staging Blood Brothers on a stage of your choice. Explain three advantages and/or disadvantages for performing the text on this type of stage.",
        "type": "6 marks \u2014 Staging Type",
        "marks": (
            "2 marks per advantage/disadvantage (to a maximum of 6).\n"
            "2 marks: Identified aspect with justification. 1 mark: Advantage/disadvantage with little justification.\n\n"
            "The candidate chooses the stage type. Common choices for Blood Brothers:\n"
            "Proscenium arch \u2014 advantages: fly loft, wings, supports composite set, clear audience viewpoint.\n"
            "Thrust \u2014 advantages: audience proximity, immersive; disadvantages: limited sight lines from sides.\n"
            "In the round \u2014 advantages: intimate; disadvantages: set restrictions, no backdrop."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "costume",
        "lesson": 4,
        "text": "Choose a main character whose appearance changes in Blood Brothers. Explain how you would use costume, hair, makeup or masks to show the change of appearance for this character in two scenes/sections from the performance text.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of how costume/hair/makeup changes communicate "
            "character development across two scenes. Detailed semiotic analysis.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some relevant detail across two scenes.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to appearance change.\n\n"
            "E.g. Mickey: As a child \u2014 grey shorts with patches, scuffed shoes, home-knitted red jumper (poverty, innocence). "
            "As an adult after prison \u2014 faded, oversized clothes hanging off a thinner frame, unwashed hair, pale makeup "
            "with dark circles under eyes (depression, defeat, the toll of prison and medication). "
            "The contrast shows the audience how circumstances have destroyed Mickey."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "director",
        "lesson": 8,
        "text": "As a director, explain how you would direct one key moment in Blood Brothers to create a sense of sadness for the audience.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of directorial choices to create sadness. "
            "Covers actor direction (vocal/physical guidance), blocking, design elements (lighting, sound, set), "
            "and audience impact. Effective examples from the text.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some relevant directorial choices.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to creating sadness.\n\n"
            "E.g. For 'Tell Me It\u2019s Not True': direct Mrs Johnstone to sing slowly with a breaking voice, "
            "isolated in a single spotlight while the rest of the stage is in darkness. Other characters frozen "
            "in tableau. Slow, mournful music underscoring. The audience should feel the weight of the tragedy."
        ),
    },
    {
        "paper": "OCR June 2025",
        "topic": "voice_physicality",
        "lesson": 7,
        "text": "You are the actor playing a character of your choice from Blood Brothers. After learning your lines, explain how you would prepare to perform as this character before the performance.",
        "type": "8 marks \u2014 Extended Explanation",
        "marks": (
            "Level 3 (7\u20138 marks): Accomplished explanation of preparation covering: script analysis, "
            "character research, vocal and physical experimentation, rehearsal techniques, and understanding "
            "of the playwright\u2019s intentions.\n\n"
            "Level 2 (4\u20136 marks): Clear explanation with some relevant preparation techniques.\n\n"
            "Level 1 (1\u20133 marks): Limited explanation with basic reference to preparation.\n\n"
            "Preparation might include: hot-seating the character, researching 1960s\u201380s Liverpool, "
            "developing a character profile (age, class, motivations), vocal warm-ups, physical characterisation "
            "exercises, running scenes with other actors, watching professional productions for inspiration."
        ),
    },
])


# ─── Lesson mapping ──────────────────────────────────────────────────────────
# Map questions to lessons. Group by lesson number, then select the best 3
# per lesson from different papers to maximise variety.

def select_questions_for_lesson(lesson_num, all_questions):
    """Select up to 3 past paper questions for this lesson, from different papers."""
    lesson_qs = [q for q in all_questions if q["lesson"] == lesson_num]

    # Prefer diversity of papers
    selected = []
    papers_used = set()

    # First pass: one per paper
    for q in lesson_qs:
        if q["paper"] not in papers_used and len(selected) < 3:
            selected.append(q)
            papers_used.add(q["paper"])

    # Second pass: fill remaining slots if needed
    for q in lesson_qs:
        if q not in selected and len(selected) < 3:
            selected.append(q)

    return selected


def main():
    # Get current lessons
    bb_lessons = sb.table('lessons').select(
        'id, lesson_number, slug, practice_questions'
    ).eq('unit_id', BLOOD_BROTHERS_UNIT_ID).order('lesson_number').execute()

    lesson_map = {l['lesson_number']: l for l in bb_lessons.data}

    # Count questions by lesson
    print("Questions available per Blood Brothers lesson:")
    for ln in range(1, 9):
        qs = [q for q in PAST_PAPER_QUESTIONS if q["lesson"] == ln]
        papers = set(q["paper"] for q in qs)
        print(f"  L{ln}: {len(qs)} questions from {len(papers)} papers: {', '.join(sorted(papers))}")

    print()

    # For each lesson, replace up to 3 of the 6 practice questions
    updates = {}
    for lesson_num in range(1, 9):
        lesson = lesson_map.get(lesson_num)
        if not lesson:
            print(f"WARNING: No lesson found for L{lesson_num}")
            continue

        current_qs = lesson['practice_questions'] or []
        past_paper_qs = select_questions_for_lesson(lesson_num, PAST_PAPER_QUESTIONS)

        if not past_paper_qs:
            print(f"L{lesson_num}: No past paper questions available, skipping")
            continue

        # Build new question list: keep first (6 - len(past_paper_qs)) original questions,
        # then append past paper questions
        num_to_keep = 6 - len(past_paper_qs)

        # Keep original questions (those without pastPaper tag)
        originals = [q for q in current_qs if not q.get('pastPaper')]
        kept = originals[:num_to_keep]

        # Format past paper questions
        tagged = []
        for q in past_paper_qs:
            tagged.append({
                "text": q["text"],
                "type": q["type"],
                "marks": q["marks"],
                "pastPaper": q["paper"]
            })

        new_qs = kept + tagged
        updates[lesson_num] = {
            "id": lesson['id'],
            "questions": new_qs,
            "past_paper_count": len(tagged),
            "original_count": len(kept),
        }

        print(f"L{lesson_num}: Keeping {len(kept)} originals + {len(tagged)} past paper = {len(new_qs)} total")
        for t in tagged:
            print(f"  + [{t['pastPaper']}] {t['text'][:80]}...")

    print()

    # Apply updates to Supabase
    print("Updating Supabase...")
    for lesson_num, update in sorted(updates.items()):
        result = sb.table('lessons').update({
            'practice_questions': update['questions']
        }).eq('id', update['id']).execute()

        if result.data:
            print(f"  L{lesson_num}: Updated ({update['past_paper_count']} past papers + {update['original_count']} originals)")
        else:
            print(f"  L{lesson_num}: UPDATE FAILED")

    print()
    print("Done! All Blood Brothers lessons updated with past paper questions.")


if __name__ == '__main__':
    main()
