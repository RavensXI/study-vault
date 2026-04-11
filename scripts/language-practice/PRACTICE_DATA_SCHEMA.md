# Language Practice Data Schema

## Output Structure

Each lesson produces one JSON object:

```json
{
  "unit_slug": "people-and-lifestyle",
  "lesson_number": 1,
  "practice_data": { ... }
}
```

## practice_data Object

```json
{
  "method_card": {
    "title": "Lesson Title",
    "content": "<p>HTML content — key vocab table + grammar explanation. ~200-400 words.</p>",
    "steps": ["Step 1 imperative", "Step 2 imperative", "Step 3 imperative"]
  },
  "exam_context": {
    "paper": "Papers 1-4 (All skills)",
    "marks": "Various",
    "frequency": "Core topic across all papers"
  },
  "worked_examples": [
    {
      "difficulty": "bronze",
      "question": "Question text",
      "steps": [
        {"label": "Step 1", "content": "Explanation"},
        {"label": "Step 2", "content": "More explanation"},
        {"label": "Answer", "content": "Final answer", "isAnswer": true}
      ]
    }
  ],
  "problem_bank": {
    "bronze": [8 problems],
    "silver": [6 problems],
    "gold": [6 problems]
  },
  "ai_marking_prompts": {
    "translate_to_target": "System prompt for translation marking",
    "role_play": "System prompt for role play marking",
    "writing": "System prompt for extended writing marking"
  }
}
```

## Problem Types and Data Structures

### 1. vocab_match (Bronze)
```json
{
  "input_type": "vocab_match",
  "question": "Match the Spanish to the English meaning",
  "pairs": [
    {"left": "las vacaciones", "right": "the holidays"},
    {"left": "la playa", "right": "the beach"},
    {"left": "el vuelo", "right": "the flight"},
    {"left": "el equipaje", "right": "the luggage"},
    {"left": "tomar el sol", "right": "to sunbathe"},
    {"left": "el alojamiento", "right": "the accommodation"}
  ]
}
```
- 5-7 pairs per problem
- `left` = target language, `right` = English
- Use vocabulary FROM THIS LESSON only

### 2. gap_fill — with word bank (Bronze)
```json
{
  "input_type": "gap_fill",
  "question": "Complete the sentence",
  "sentence_parts": ["Ayer ", " a la playa con mi familia y ", " el sol todo el día."],
  "gaps": [
    {
      "answer": "fui",
      "accept": ["fui"],
      "rule": "Verb conjugation",
      "correct_explain": "<strong>fui</strong> is the <strong>yo</strong> form of <em>ir</em> in the preterite tense.",
      "wrong": {
        "fue": "<em>fue</em> is the <strong>él/ella</strong> form, not <strong>yo</strong>. First person preterite of ir = <strong>fui</strong>.",
        "ir": "<em>ir</em> is the infinitive. You need the preterite past tense because of <em>ayer</em> (yesterday)."
      }
    },
    {
      "answer": "tomamos",
      "accept": ["tomamos"],
      "rule": "Verb conjugation",
      "correct_explain": "<strong>tomamos</strong> is the nosotros form. 'Mi familia y yo' = we.",
      "wrong": {
        "tomaron": "<em>tomaron</em> is the ellos/ellas form (they). 'Mi familia y yo' = we → <strong>tomamos</strong>."
      }
    }
  ],
  "word_bank": ["fui", "fue", "ir", "tomamos", "tomaron"]
}
```
- `sentence_parts` are the pieces of the sentence between gaps (one more than gaps)
- Each gap has `answer`, `accept` (array of valid answers), `rule`, `correct_explain`, and `wrong` map
- `wrong` maps common mistakes to explanations — include 1-3 entries
- `word_bank` has the correct answers PLUS 1-3 distractors
- The `correct_explain` and `wrong` values use HTML: `<strong>` for correct forms, `<em>` for wrong forms

### 3. gap_fill — no word bank (Silver)
Same structure but:
- `word_bank` is `null` (not present)
- Add `"english": "My sister is very nice and has green eyes."` — the translated sentence with gap words bolded
- Students type freely — `accept` array should include common valid spellings

### 4. multiple_choice (Bronze)
```json
{
  "input_type": "multiple_choice",
  "question": "What does 'Me gusta ir de vacaciones a España' mean?",
  "options": ["I like going on holiday to Spain", "I went on holiday to Spain", "I will go on holiday to Spain", "I don't like going to Spain"],
  "solutions": [0]
}
```
- `solutions` is an array of correct option indices (usually just one: `[0]`)
- 4 options, one correct
- Test reading comprehension

### 5. translate — to English (Bronze/Silver)
```json
{
  "input_type": "translate",
  "direction": "to_english",
  "source_text": "Me gusta mucho ir de vacaciones a España con mi familia.",
  "target_lang": "es",
  "model_answers": ["I really like going on holiday to Spain with my family."],
  "hints": ["me gusta = I like", "vacaciones = holidays"],
  "marks": 4,
  "ai_system_prompt": "You are a GCSE Spanish examiner marking a translation from Spanish to English. The student is translating: '{source}'. Model answer: '{model}'. Accept any valid translation that conveys the same meaning. Be encouraging but specific. Respond in JSON: {\"quality\":\"excellent|good|needs_work|not_valid\",\"feedback\":\"2-3 sentences\",\"improvement\":\"optional specific suggestion\"}"
}
```
- `hints` can be null for Gold tier
- `target_lang`: "es", "fr", or "de"
- For Bronze: include hints. For Silver/Gold: hints can be null.

### 6. translate — to target language (Silver/Gold)
```json
{
  "input_type": "translate",
  "direction": "to_target",
  "source_text": "I went to the beach yesterday with my friends and we swam in the sea.",
  "target_lang": "es",
  "model_answers": ["Ayer fui a la playa con mis amigos y nadamos en el mar."],
  "hints": ["beach = la playa", "yesterday = ayer", "to swim = nadar"],
  "marks": 4,
  "ai_system_prompt": "You are a GCSE Spanish examiner marking a translation from English to Spanish. Source: '{source}'. Model answer: '{model}'. Accept any grammatically correct translation that conveys the same meaning. Check: verb conjugations, gender agreement, word order. Respond in JSON: {\"quality\":\"excellent|good|needs_work|not_valid\",\"feedback\":\"2-3 sentences about grammar accuracy\",\"improvement\":\"optional specific correction\"}"
}
```

### 7. dictation (all tiers)
```json
{
  "input_type": "dictation",
  "question": "Listen and type what you hear",
  "audio_text": "Fui de vacaciones a España el verano pasado.",
  "correct_text": "Fui de vacaciones a España el verano pasado.",
  "translation": "I went on holiday to Spain last summer.",
  "max_plays": 2,
  "strict_accents": false
}
```
- `audio_text` = what TTS will read (same as correct_text usually)
- Bronze: 5-8 words, `strict_accents: false`
- Silver: 8-12 words, `strict_accents: false`
- Gold: 12-20 words, `strict_accents: true`
- Use natural, exam-level sentences from this lesson's topic
- `audio_url` will be added later by the audio generation script

### 8. sentence_builder (Silver/Gold)
```json
{
  "input_type": "sentence_builder",
  "question": "Build the sentence in Spanish",
  "english": "Yesterday I went to the beach with my family.",
  "correct_order": ["Ayer", "fui", "a", "la", "playa", "con", "mi", "familia."],
  "distractors": ["fue", "el"],
  "distractor_labels": {
    "fue": "wrong verb form — fue is él/ella, not yo",
    "el": "wrong gender — playa is feminine, needs la not el"
  }
}
```
- Silver: 0-1 distractors. Gold: 2-3 distractors.
- `correct_order` is the exact array of words in correct order
- `distractors` are wrong forms of words that test grammar
- `distractor_labels` explains WHY each distractor is wrong
- Include punctuation attached to the last word (e.g., "familia.")

### 9. spot_correct (Silver)
```json
{
  "input_type": "spot_correct",
  "question": "Find and fix the grammatical error",
  "sentence": "Mi hermano es muy simpática y tiene los ojos verdes.",
  "error_word": "simpática",
  "correction": "simpático",
  "accept_corrections": ["simpático"],
  "error_type": "Gender agreement",
  "explanation": "<strong>hermano</strong> is masculine, so the adjective must end in <strong>-o</strong>, not <strong>-a</strong>.",
  "translation": "My brother is very nice and has green eyes."
}
```
- ONE error per sentence (not multiple)
- Error types: Gender agreement, Verb conjugation, Ser vs Estar, Article gender, Adjective agreement, Word order, Preposition
- `error_word` must be an exact word from the sentence
- `accept_corrections` can include multiple valid fixes

### 10. role_play (Gold)
```json
{
  "input_type": "role_play",
  "question": "Role Play",
  "scenario": "You are on holiday in Spain and go to a restaurant for dinner with your family. The waiter comes to your table.",
  "scenario_icon": "🍽️",
  "target_lang": "es",
  "bullets": [
    {
      "prompt": "Greet the waiter and ask for a table for four people.",
      "model_answer": "¡Buenas tardes! ¿Tiene una mesa para cuatro personas, por favor?",
      "note": "greeting + ¿Tiene...? (polite request) + para cuatro personas"
    },
    {
      "prompt": "Order a still water and ask to see the menu.",
      "model_answer": "Me gustaría un agua sin gas, por favor. ¿Puedo ver la carta?",
      "note": "me gustaría (conditional = polite) + ¿Puedo...? (can I)"
    },
    {
      "prompt": "Say what you ate and give your opinion.",
      "model_answer": "Comí la paella y estaba muy rica. ¡Me encantó!",
      "note": "comí (preterite) + estaba (imperfect for description) + opinion"
    },
    {
      "prompt": "Ask for the bill and say you will come back next year.",
      "model_answer": "¿Me puede traer la cuenta, por favor? Volveremos el año que viene.",
      "note": "la cuenta (bill) + volveremos (future, nosotros)"
    }
  ],
  "marks": 10,
  "ai_system_prompt": "You are a GCSE Spanish examiner marking a role play. The student was given a scenario and bullet points to respond to in Spanish. For each bullet, assess: (1) Did they communicate the required information? (2) Is the Spanish grammatically accurate? Award marks out of 10 total. Be encouraging. Respond in JSON: {\"quality\":\"excellent|good|needs_work|not_valid\",\"feedback\":\"Per-bullet feedback\",\"improvement\":\"Key grammar point to revise\"}"
}
```
- 3-4 bullets per scenario
- Each bullet has a clear communication task
- Model answers show exam-quality Spanish
- Notes explain the key grammar/vocab used
- Scenarios should match AQA Paper 2 format

### 11. reorder (Silver)
```json
{
  "input_type": "reorder",
  "question": "Put these words in the correct order to form a sentence",
  "items": ["playa", "a", "fui", "Ayer", "la"],
  "correct_order": [3, 2, 1, 4, 0]
}
```
- `items` are shuffled words
- `correct_order` maps position → items index
- Keep sentences short (5-8 words)

### 12. ai_mark / ai_write (Gold — extended writing)
```json
{
  "input_type": "ai_mark",
  "question": "Write 40-50 words in Spanish describing your last holiday. Include: where you went, what you did, your opinion, and what you would do differently.",
  "marks": 8,
  "ai_system_prompt": "You are a GCSE Spanish examiner marking extended writing. Mark on: Communication (did they address all bullet points?), Range of language (variety of tenses, vocab, connectives), Accuracy (grammar, spelling, accents). The student was asked to write 40-50 words about their last holiday. Be encouraging and formative. Respond in JSON: {\"quality\":\"excellent|good|needs_work|not_valid\",\"feedback\":\"3-4 sentences covering each criterion\",\"improvement\":\"One specific grammar point to work on\"}"
}
```

## Tier Distribution Per Lesson (20 problems total)

### Bronze (8 problems):
1. vocab_match (6-7 pairs from lesson vocab)
2. vocab_match (6-7 different pairs)
3. gap_fill with word_bank (grammar focus)
4. gap_fill with word_bank (vocab focus)
5. multiple_choice (reading comprehension)
6. multiple_choice (reading comprehension)
7. translate to_english (short sentence, with hints)
8. dictation (5-8 words, strict_accents: false)

### Silver (6 problems):
9. gap_fill NO word_bank (with English prompt, verb focus)
10. spot_correct (one grammar error)
11. sentence_builder (0-1 distractors)
12. translate to_target (with vocab hints)
13. dictation (8-12 words, strict_accents: false)
14. reorder (5-8 words)

### Gold (6 problems):
15. translate to_target (NO hints, complex sentence with multiple tenses)
16. sentence_builder (2-3 distractors)
17. role_play (3-4 bullets)
18. ai_mark (40-50 word writing task)
19. dictation (12-20 words, strict_accents: true, multi-clause)
20. [one of: translate/gap_fill/spot_correct with Higher-only grammar like subjunctive, passive, complex tenses]

## Worked Examples (2-3 per lesson)

Include worked examples showing HOW to approach the skills:
1. One translation example (how to break down a sentence)
2. One grammar example (how to identify the right verb form/gender/tense)
3. Optionally one reading comprehension example

## Method Card Content

The method card condenses the lesson's article content into:
1. **Key vocab table** in HTML: `<table><tr><th>Spanish</th><th>English</th></tr><tr><td>word</td><td>translation</td></tr></table>` — 10-15 most important items
2. **Grammar focus**: The lesson's main grammar point, explained in 2-3 sentences with examples
3. **Model paragraph**: A 2-3 sentence example showing vocab + grammar in use, with English translation

Steps should be 3-5 imperative instructions like:
- "Learn the key vocabulary for [topic]"
- "Master the [tense] for [verb group]"
- "Practice translating sentences using [structure]"

## Quality Rules

1. ALL target language text MUST be grammatically correct
2. Translations must be accurate
3. Vocab pairs must match the lesson's vocabulary (read the content file)
4. Gap fill wrong-answer explanations must be specific and educational
5. Dictation sentences should use natural, exam-style language
6. Role play scenarios should be realistic (restaurant, hotel, doctor, school, shop)
7. Error sentences for spot_correct must have exactly ONE error — the rest must be correct
8. Sentence builder correct_order must produce a grammatically valid sentence
9. Distractors must be plausible wrong forms (wrong conjugation, wrong gender, wrong tense)
10. Gold tier problems should test Higher content (conditional, subjunctive for Spanish, compound tenses)

## AI Marking Prompts

Include a shared `ai_marking_prompts` object. The prompts use `{source}` and `{model}` placeholders that the front-end substitutes. Write prompts that:
- Accept multiple valid translations
- Check grammar accuracy
- Are encouraging but honest
- Respond in the required JSON format
