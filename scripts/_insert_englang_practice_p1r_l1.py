"""
Insert practice_data for English Language Paper 1 Reading Lesson 1:
Explicit and Implicit Information.

20 problems (8 bronze, 7 silver, 5 gold), 6 passages, method card, 2 worked examples.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

LESSON_ID = 'b51e1320-7952-4e74-854e-14d58e95a96d'

# ============================================================
#  PASSAGES
# ============================================================
PASSAGES = [
    {
        "id": "p1",
        "label": "Extract A \u2014 Marcus",
        "text": "The corridor was empty. Marcus pressed his back against the cold wall and listened. Somewhere above him, a door slammed. He flinched. His hands were trembling, and he shoved them deep into his pockets, curling his fingers around the crumpled note his mother had given him that morning. \u201cYou\u2019ll be fine,\u201d she had said, smoothing down his collar with hands that shook as much as his did now. He hadn\u2019t believed her then. He certainly didn\u2019t believe her now. The fluorescent light above him flickered once, twice, then settled into a low, persistent hum. He took a breath and stepped forward."
    },
    {
        "id": "p2",
        "label": "Extract B \u2014 Gran\u2019s Kitchen",
        "text": "Gran\u2019s kitchen always smelled of flour and something sweet. She moved between the counter and the stove with a practised rhythm, humming a tune that belonged to another decade. \u201cPass me the sugar, love,\u201d she said, without turning around. Her hands were dusted white, the skin paper-thin over blue veins, but her grip on the wooden spoon was firm and sure. Through the window, the garden stretched out in lazy afternoon light. A blackbird sat on the fence, watching them both with one bright, curious eye. For a moment, everything was exactly as it had always been."
    },
    {
        "id": "p3",
        "label": "Extract C \u2014 Ellen",
        "text": "The house had been quiet for three days now. Ellen moved through the rooms like a visitor in a museum, careful not to disturb anything. His coat still hung on the back of the door, one sleeve longer than the other where the lining had come loose. She\u2019d meant to fix it. She\u2019d always meant to fix it. In the kitchen, the calendar showed last Tuesday, and she couldn\u2019t bring herself to tear off the page because his handwriting was there \u2014 \u201cdentist 2pm\u201d \u2014 in that cramped, impatient scrawl she\u2019d teased him about for forty years. She filled the kettle and stood at the window, watching the rain flatten the daffodils he had planted in October."
    },
    {
        "id": "p4",
        "label": "Extract D \u2014 Aisha",
        "text": "The bus shelter offered no real protection. Rain drove sideways through the open sides, speckling Aisha\u2019s school bag and the half-eaten sandwich she\u2019d given up on. Two older boys leaned against the far panel, their hoods up, voices low. One of them glanced at her and she looked away quickly, fixing her eyes on the timetable as though she hadn\u2019t already memorised every departure. The 42 was late. It was always late. She shifted her weight from one foot to the other and pulled her blazer tighter, though the thin fabric did nothing against the November cold. Across the road, the chippy\u2019s windows glowed warm and golden, and the smell of vinegar drifted across like a promise she couldn\u2019t afford."
    },
    {
        "id": "p5",
        "label": "Extract E \u2014 The Coastline",
        "text": "The sea was not the same sea he remembered. As a boy, it had roared \u2014 a vast, breathing thing that swallowed the horizon and threw stones at his feet like gifts. Now it lay flat and grey beneath a colourless sky, barely troubling the shore. He stood where the concrete ended and the sand began, his shoes sinking slightly, and thought about how the coastline had retreated since his last visit. Twenty feet, perhaps more. The caf\u00e9 where his father had bought him ice cream was rubble now, claimed by a winter storm three years ago. Nobody had rebuilt it. The seagulls still circled overhead, but their cries sounded less like laughter and more like complaint."
    },
    {
        "id": "p6",
        "label": "Extract F \u2014 Laura & Daniel",
        "text": "\u201cIt\u2019s fine,\u201d said Laura, setting her fork down with exaggerated care. Across the table, Daniel continued eating, his eyes fixed on something beyond her left shoulder. The pasta was overcooked \u2014 she\u2019d known it the moment she\u2019d drained it \u2014 but neither of them had mentioned it. The kitchen clock ticked with the steady patience of something that had outlasted every argument in this house. She thought about the text message she\u2019d seen that morning, the one he\u2019d deleted before she\u2019d finished reading it. \u201cHow was work?\u201d she asked, and the words landed between them like a stone dropped into still water. He looked up. Smiled. \u201cFine,\u201d he said. The clock ticked on."
    }
]

# ============================================================
#  METHOD CARD
# ============================================================
METHOD_CARD = {
    "title": "Explicit & Implicit Information",
    "content": "<p><strong>Explicit</strong> information is stated directly \u2014 you can underline the exact words. <strong>Implicit</strong> information is suggested through clues \u2014 you must infer the meaning from word choice, imagery, or detail.</p>",
    "steps": [
        "Read the specified lines carefully",
        "Ask yourself: \u201cCan I point to the exact words?\u201d",
        "If yes \u2192 EXPLICIT",
        "If no, but clues suggest it \u2192 IMPLICIT",
        "If no evidence at all \u2192 NOT SUPPORTED"
    ]
}

# ============================================================
#  EXAM CONTEXT
# ============================================================
EXAM_CONTEXT = {
    "paper": "Paper 1, Question 1",
    "marks": "4 marks",
    "time": "5 minutes max",
    "frequency": "Underpins all Paper 1 questions"
}

# ============================================================
#  WORKED EXAMPLES
# ============================================================
WORKED_EXAMPLES = [
    {
        "difficulty": "bronze",
        "question": "Is this information explicit or implicit?",
        "passage": "Gran\u2019s kitchen always smelled of flour and something sweet. She moved between the counter and the stove with a practised rhythm, humming a tune that belonged to another decade.",
        "steps": [
            {"label": "Statement", "content": "\u201cThe grandmother is cooking in her kitchen.\u201d"},
            {"label": "Step 1", "content": "Can I underline exact words? Yes \u2014 \u201cShe moved between the counter and the stove\u201d directly shows she is cooking."},
            {"label": "Step 2", "content": "\u201cKitchen\u201d is explicitly named. \u201cFlour\u201d confirms cooking."},
            {"label": "Answer", "content": "This is EXPLICIT \u2014 the text states it directly. You can point to the exact words.", "isAnswer": True}
        ]
    },
    {
        "difficulty": "silver",
        "question": "Is this information explicit or implicit?",
        "passage": "Marcus pressed his back against the cold wall and listened. His hands were trembling, and he shoved them deep into his pockets, curling his fingers around the crumpled note his mother had given him that morning.",
        "steps": [
            {"label": "Statement", "content": "\u201cMarcus is anxious about being in this building.\u201d"},
            {"label": "Step 1", "content": "Can I underline \u201canxious\u201d? No \u2014 the word isn\u2019t in the text."},
            {"label": "Step 2", "content": "But there are clues: \u201ctrembling\u201d hands, pressing against the wall, listening carefully. These suggest nervousness."},
            {"label": "Step 3", "content": "The \u201ccrumpled note\u201d implies he\u2019s been gripping it \u2014 a physical sign of worry."},
            {"label": "Answer", "content": "This is IMPLICIT \u2014 the text suggests anxiety through physical details, but never states it directly.", "isAnswer": True}
        ]
    }
]

# ============================================================
#  PROBLEM BANK
# ============================================================
BRONZE = [
    # B1: Traffic Light — Marcus (P1)
    {
        "input_type": "traffic_light",
        "passage_id": "p1",
        "question": "Sort each statement into the correct category.",
        "statements": [
            {"text": "Marcus is standing in a corridor.", "correct": "explicit", "explain": "The text states \u201cThe corridor was empty\u201d directly."},
            {"text": "His hands were trembling.", "correct": "explicit", "explain": "\u201cHis hands were trembling\u201d is stated word-for-word."},
            {"text": "Marcus is nervous about a new experience.", "correct": "implicit", "explain": "Trembling, flinching, and his mother\u2019s reassurance suggest nervousness, but the word isn\u2019t used."},
            {"text": "His mother is also worried about him.", "correct": "implicit", "explain": "Her hands \u201cshook as much as his\u201d implies shared anxiety."},
            {"text": "Marcus is being chased by someone.", "correct": "unsupported", "explain": "Nothing suggests he\u2019s being chased. The door slam is above him."},
            {"text": "The building is a hospital.", "correct": "unsupported", "explain": "A corridor and fluorescent light could be anywhere \u2014 the building is never identified."}
        ]
    },
    # B2: Highlight Evidence — Marcus (P1)
    {
        "input_type": "highlight_evidence",
        "passage_id": "p1",
        "question": "Highlight the phrase that shows Marcus received something from his mother.",
        "answer_text": "the crumpled note his mother had given him that morning",
        "explanation": "This explicitly states his mother gave him a note."
    },
    # B3: Connotation Picker — Marcus (P1)
    {
        "input_type": "connotation_picker",
        "passage_id": "p1",
        "question": "The word \u201ccrumpled\u201d describes the note Marcus is holding. Which connotations are relevant in this context?",
        "chips": [
            {"text": "Anxiety or nervousness", "correct": True},
            {"text": "Carelessness or disrespect", "correct": False},
            {"text": "Something repeatedly touched or gripped", "correct": True},
            {"text": "Age or decay", "correct": False},
            {"text": "Comfort from holding something familiar", "correct": True},
            {"text": "Anger or frustration", "correct": False}
        ]
    },
    # B4: Highlight Evidence — Gran (P2)
    {
        "input_type": "highlight_evidence",
        "passage_id": "p2",
        "question": "Highlight the phrase that shows the grandmother is elderly.",
        "answer_text": "the skin paper-thin over blue veins",
        "explanation": "This physical description explicitly shows age through thin skin and visible veins."
    },
    # B5: Traffic Light — Gran (P2)
    {
        "input_type": "traffic_light",
        "passage_id": "p2",
        "question": "Sort each statement into the correct category.",
        "statements": [
            {"text": "The kitchen smells of baking.", "correct": "explicit", "explain": "\u201cSmelled of flour and something sweet\u201d is stated directly."},
            {"text": "The grandmother is humming.", "correct": "explicit", "explain": "\u201cHumming a tune\u201d is stated word-for-word."},
            {"text": "The grandmother is getting older and frailer.", "correct": "implicit", "explain": "\u201cSkin paper-thin over blue veins\u201d suggests ageing, but \u201cfrailer\u201d is never stated \u2014 her grip is \u201cfirm and sure.\u201d"},
            {"text": "The narrator feels safe and comforted.", "correct": "implicit", "explain": "\u201cEverything was exactly as it had always been\u201d suggests comfort and stability, but the feeling isn\u2019t named."},
            {"text": "It is early morning.", "correct": "unsupported", "explain": "The text says \u201clazy afternoon light,\u201d not morning."},
            {"text": "The blackbird is the grandmother\u2019s pet.", "correct": "unsupported", "explain": "The blackbird is on the fence outside \u2014 nothing suggests it\u2019s a pet."}
        ]
    },
    # B6: Connotation Picker — Gran (P2)
    {
        "input_type": "connotation_picker",
        "passage_id": "p2",
        "question": "The grandmother moves with a \u201cpractised rhythm.\u201d Which connotations of \u201cpractised\u201d are relevant here?",
        "chips": [
            {"text": "Skill built through repetition", "correct": True},
            {"text": "Fake or insincere", "correct": False},
            {"text": "Confidence and ease", "correct": True},
            {"text": "Boredom or routine", "correct": False},
            {"text": "Years of experience", "correct": True},
            {"text": "Showing off to others", "correct": False}
        ]
    },
    # B7: Highlight Evidence — Marcus (P1)
    {
        "input_type": "highlight_evidence",
        "passage_id": "p1",
        "question": "Highlight the phrase that shows Marcus\u2019s mother tried to reassure him.",
        "answer_text": "You\u2019ll be fine",
        "explanation": "This is a direct quote showing her attempt to reassure him, even though she was also nervous."
    },
    # B8: Multiple choice — Gran (P2)
    {
        "input_type": "multiple_choice",
        "passage_id": "p2",
        "question": "Which of these statements is TRUE based on the passage?",
        "options": [
            "The grandmother is baking a cake for a birthday",
            "There is a bird watching from the garden fence",
            "The narrator is helping with the cooking",
            "The kitchen window is closed"
        ],
        "solutions": [1]
    }
]

SILVER = [
    # S1: Traffic Light — Aisha (P4)
    {
        "input_type": "traffic_light",
        "passage_id": "p4",
        "question": "Sort each statement \u2014 be careful, some are designed to trick you.",
        "statements": [
            {"text": "Aisha is waiting at a bus shelter.", "correct": "explicit", "explain": "Directly stated: \u201cThe bus shelter offered no real protection.\u201d"},
            {"text": "It is raining.", "correct": "explicit", "explain": "\u201cRain drove sideways\u201d is directly stated."},
            {"text": "Aisha feels intimidated by the older boys.", "correct": "implicit", "explain": "She \u201clooked away quickly\u201d suggests discomfort, but \u201cintimidated\u201d is never used."},
            {"text": "Aisha cannot afford to buy food from the chip shop.", "correct": "implicit", "explain": "\u201cA promise she couldn\u2019t afford\u201d implies financial limitation through metaphor."},
            {"text": "The older boys are planning to rob her.", "correct": "unsupported", "explain": "Hoods up and low voices might seem threatening, but nothing suggests criminal intent."},
            {"text": "Aisha has been waiting for over an hour.", "correct": "unsupported", "explain": "The bus is late, but no time frame is given."}
        ]
    },
    # S2: Connotation Picker — Aisha (P4)
    {
        "input_type": "connotation_picker",
        "passage_id": "p4",
        "question": "The smell of vinegar is described as \u201ca promise she couldn\u2019t afford.\u201d Which connotations of \u201cpromise\u201d are relevant here?",
        "chips": [
            {"text": "Something desirable but out of reach", "correct": True},
            {"text": "Warmth and comfort", "correct": True},
            {"text": "A binding agreement", "correct": False},
            {"text": "Temptation", "correct": True},
            {"text": "Hope that may be unfulfilled", "correct": True},
            {"text": "Danger or threat", "correct": False}
        ]
    },
    # S3: Evidence Match — Ellen (P3)
    {
        "input_type": "evidence_match",
        "passage_id": "p3",
        "question": "Match each claim about Ellen to the quote that supports it.",
        "claims": [
            "Ellen is grieving.",
            "She feels guilty about something undone.",
            "She is struggling to move forward.",
            "She still feels connected to him."
        ],
        "quotes": [
            {"text": "\u201cThe house had been quiet for three days now\u201d", "correctClaim": 0},
            {"text": "\u201cShe\u2019d meant to fix it. She\u2019d always meant to fix it.\u201d", "correctClaim": 1},
            {"text": "\u201cshe couldn\u2019t bring herself to tear off the page\u201d", "correctClaim": 2},
            {"text": "\u201cwatching the rain flatten the daffodils he had planted\u201d", "correctClaim": 3},
            {"text": "\u201cEllen moved through the rooms like a visitor\u201d", "correctClaim": -1}
        ]
    },
    # S4: AI Mark — Ellen (P3)
    {
        "input_type": "ai_mark",
        "passage_id": "p3",
        "question": "What is Ellen really thinking or feeling in this moment?",
        "quote": "\u201cShe\u2019d meant to fix it. She\u2019d always meant to fix it.\u201d",
        "marks": 4,
        "ai_prompt_key": "inference",
        "context": "Ellen is looking at her deceased partner\u2019s coat with a loose lining. The repeated \u201cmeant to\u201d suggests regret about small, everyday things left undone. Good answers will identify guilt, regret, or the painful weight of missed opportunities that can never be fulfilled now."
    },
    # S5: Highlight Evidence — Ellen (P3)
    {
        "input_type": "highlight_evidence",
        "passage_id": "p3",
        "question": "Highlight the phrase that shows Ellen cannot accept what has happened.",
        "answer_text": "she couldn\u2019t bring herself to tear off the page",
        "explanation": "This shows she is clinging to the past \u2014 even a calendar page with his handwriting feels too precious to remove."
    },
    # S6: Connotation Picker — Ellen (P3)
    {
        "input_type": "connotation_picker",
        "passage_id": "p3",
        "question": "Ellen moves through the rooms \u201clike a visitor in a museum.\u201d Which connotations of \u201cmuseum\u201d are relevant here?",
        "chips": [
            {"text": "Stillness and preservation", "correct": True},
            {"text": "Excitement and discovery", "correct": False},
            {"text": "Not belonging or feeling out of place", "correct": True},
            {"text": "Fragility \u2014 things that must not be touched", "correct": True},
            {"text": "A place for children to visit", "correct": False},
            {"text": "Everything frozen in time", "correct": True}
        ]
    },
    # S7: Misleading Summary — Aisha (P4)
    {
        "input_type": "misleading_summary",
        "passage_id": "p4",
        "question": "A student wrote this summary. Click on the underlined phrases that misinterpret the text.",
        "summaryParts": [
            {"text": "Aisha is waiting for a bus in bad weather. ", "wrong": False},
            {"text": "She is sharing her lunch with two older boys at the shelter. ", "wrong": True, "explain": "She hasn\u2019t shared anything \u2014 her sandwich is \u201chalf-eaten\u201d and the boys are separate from her, leaning against the far panel."},
            {"text": "The bus is running late, which seems to be a regular occurrence. ", "wrong": False},
            {"text": "She is too cold to eat and feels uncomfortable. ", "wrong": False},
            {"text": "She decides to go to the chip shop across the road to warm up. ", "wrong": True, "explain": "The smell is \u201ca promise she couldn\u2019t afford\u201d \u2014 she can\u2019t afford it. She stays at the shelter."}
        ]
    }
]

GOLD = [
    # G1: Misleading Summary — Coastline (P5)
    {
        "input_type": "misleading_summary",
        "passage_id": "p5",
        "question": "A student wrote this summary. Click on the underlined phrases that misinterpret the text.",
        "summaryParts": [
            {"text": "The narrator returns to a seaside town he visited as a child. ", "wrong": False},
            {"text": "He remembers the sea being exciting and full of life. ", "wrong": False},
            {"text": "He is pleased to see that nothing has changed since his childhood. ", "wrong": True, "explain": "The text shows the opposite \u2014 the sea is \u201cflat and grey,\u201d the coastline has retreated, and the caf\u00e9 is rubble."},
            {"text": "The caf\u00e9 has been replaced by a new building. ", "wrong": True, "explain": "\u201cNobody had rebuilt it.\u201d The text explicitly says it has NOT been replaced."},
            {"text": "The seagulls\u2019 cries no longer sound joyful to him. ", "wrong": False},
            {"text": "The narrator feels a deep sense of loss.", "wrong": False}
        ]
    },
    # G2: Evidence Match — Laura & Daniel (P6)
    {
        "input_type": "evidence_match",
        "passage_id": "p6",
        "question": "Match each claim about Laura and Daniel to the quote that supports it. One quote is a distractor.",
        "claims": [
            "Laura is suspicious of Daniel.",
            "There is hidden tension between them.",
            "Daniel is hiding something.",
            "The relationship has a long history of conflict."
        ],
        "quotes": [
            {"text": "\u201cthe text message she\u2019d seen\u2026 the one he\u2019d deleted\u201d", "correctClaim": 0},
            {"text": "\u201cthe words landed between them like a stone dropped into still water\u201d", "correctClaim": 1},
            {"text": "He looked up. Smiled. \u201cFine,\u201d he said.", "correctClaim": 2},
            {"text": "\u201cthe steady patience of something that had outlasted every argument\u201d", "correctClaim": 3},
            {"text": "\u201cThe pasta was overcooked\u201d", "correctClaim": -1}
        ]
    },
    # G3: AI Mark — Laura & Daniel (P6)
    {
        "input_type": "ai_mark",
        "passage_id": "p6",
        "question": "What is Laura really thinking or feeling when she asks this question?",
        "quote": "\u201cHow was work?\u201d she asked, and the words landed between them like a stone dropped into still water.",
        "marks": 4,
        "ai_prompt_key": "inference",
        "context": "Laura has seen a deleted text message. Her question isn\u2019t about work \u2014 it\u2019s a test. The simile \u201cstone dropped into still water\u201d suggests disrupting fragile calm. Good answers identify suspicion, the gap between said and meant, or testing Daniel\u2019s honesty."
    },
    # G4: Misleading Summary — Laura & Daniel (P6)
    {
        "input_type": "misleading_summary",
        "passage_id": "p6",
        "question": "A student wrote this summary. Click on the underlined phrases that misinterpret the text.",
        "summaryParts": [
            {"text": "Laura and Daniel are having dinner together. ", "wrong": False},
            {"text": "Laura is upset because the pasta is overcooked and Daniel hasn\u2019t complimented her cooking. ", "wrong": True, "explain": "Neither mentions the pasta. Laura\u2019s tension comes from the deleted text message, not the food."},
            {"text": "Daniel seems relaxed and comfortable during the meal. ", "wrong": True, "explain": "His eyes avoid hers, and his one-word \u201cFine\u201d is a performance, not genuine comfort."},
            {"text": "Laura asks about work as a way of testing Daniel\u2019s honesty. ", "wrong": False},
            {"text": "The clock suggests time passing uncomfortably.", "wrong": False}
        ]
    },
    # G5: AI Mark — Coastline (P5)
    {
        "input_type": "ai_mark",
        "passage_id": "p5",
        "question": "What does this comparison suggest about the narrator\u2019s feelings?",
        "quote": "As a boy, it had roared \u2014 a vast, breathing thing that swallowed the horizon and threw stones at his feet like gifts. Now it lay flat and grey beneath a colourless sky.",
        "marks": 4,
        "ai_prompt_key": "inference",
        "context": "The narrator contrasts his childhood memory of a powerful, exciting sea with the present flat, grey reality. The personification (\u201croared,\u201d \u201cbreathing,\u201d \u201cthrew stones like gifts\u201d) makes the past feel alive and generous, while the present is lifeless. Good answers identify nostalgia, loss, disappointment, or the idea that his childhood wonder has been replaced by a bleaker adult perspective."
    }
]

# ============================================================
#  AI MARKING PROMPTS
# ============================================================
AI_PROMPTS = {
    "inference": "You are a GCSE English Language examiner (AQA 8700). A student has been shown a quote from a fiction text and asked what the character is really thinking or feeling (implicit meaning). Mark their inference.\n\nAssess whether they:\n1. Correctly identified an implicit meaning (not just restated the text)\n2. Used evidence from the text to support their point\n3. Showed understanding beyond the surface level\n\nBe encouraging but honest. Respond in JSON:\n{\"quality\":\"excellent|good|needs_work|not_valid\",\"feedback\":\"2-3 sentences\",\"improvement\":\"optional suggestion\"}\n\nexcellent = perceptive inference with clear textual support\ngood = valid inference with some support\nneeds_work = partially valid but too vague or lacks evidence\nnot_valid = restates the text or misreads the meaning"
}

# ============================================================
#  ASSEMBLE AND INSERT
# ============================================================
practice_data = {
    "method_card": METHOD_CARD,
    "exam_context": EXAM_CONTEXT,
    "worked_examples": WORKED_EXAMPLES,
    "passages": PASSAGES,
    "problem_bank": {
        "bronze": BRONZE,
        "silver": SILVER,
        "gold": GOLD
    },
    "ai_marking_prompts": AI_PROMPTS,
    "related_videos": [
        {"title": "AQA Paper 1 Q1 Walkthrough", "url": "https://www.youtube.com/watch?v=sQ8vSr_K5YM", "channel": "Mr Bruff"},
        {"title": "Explicit vs Implicit Information", "url": "https://www.youtube.com/watch?v=5RjIx_FlXlY", "channel": "Mr Salles"}
    ],
    "topic_links": {
        "prerequisites": [],
        "next": [
            {"title": "Language Techniques \u2014 The Big 5", "slug": "paper-1-reading/2"}
        ]
    }
}

def main():
    sb = get_client()

    # Update the lesson with practice_data
    result = sb.table('lessons').update({
        'practice_data': practice_data
    }).eq('id', LESSON_ID).execute()

    if result.data:
        print(f"Successfully inserted practice_data for L1: Explicit & Implicit Information")
        print(f"  Passages: {len(PASSAGES)}")
        print(f"  Problems: {len(BRONZE)} bronze, {len(SILVER)} silver, {len(GOLD)} gold = {len(BRONZE)+len(SILVER)+len(GOLD)} total")
        print(f"  Worked examples: {len(WORKED_EXAMPLES)}")
    else:
        print("ERROR: Update returned no data")

if __name__ == '__main__':
    main()
