# Questions Pipeline — Practice Questions & Knowledge Checks

Reference for building practice questions and knowledge checks on lesson pages.

---

## Practice Questions

6 per lesson. Inlined in `window.practiceQuestions` array in the lesson's `<script>` block.

### Format

```javascript
window.practiceQuestions = [
  {
    type: "8 marks \u2014 Write an account",
    question: "Write an account of...",
    marks: 8,
    answer: "Students may include:\n\u2022 Point one\n\u2022 Point two\n\u2022 Point three",
    pastPaper: "AQA June 2019"   // optional — adds gold badge
  }
];
```

Use unicode escapes in JS: `\u2014` (em dash), `\u2013` (en dash), `\u2019`/`\u2018` (smart quotes).

Real past paper questions are tagged with `pastPaper` property (displays gold badge). Fill remaining with original questions in the exam board's style.

### Question Types by Subject

**History (AQA) — varies by unit:**
- **Conflict & Tension**: 3x "Write an account" (8 marks) + 3x "How far do you agree?" (16+4 SPaG)
- **Health & People**: Mix of "Explain significance" (8) + "Explain two ways similar" (8) + "Has [factor] been the main factor?" (16+4 SPaG)
- **Elizabethan**: 6x 8-mark only ("Explain what was important" / "Write an account")
- **America**: 2x "Describe two" (4) + 2x "In what ways" (8) + 2x "Which had more impact?" (12)

**Business (Edexcel) — same mix every lesson:**
- 1x Define (1 mark), 1x Outline (2), 2x Explain (3), 1x Discuss (6), 1x Justify/Evaluate (9 or 12)

**Geography (AQA) — same mix every lesson:**
- 1x Define (1 mark), 1x Describe (2), 1x Explain (4), 1x Explain (6), 1x Evaluate (9)

**Sport Science (OCR) — same mix every lesson:**
- 1x Identify (1 mark), 1x State (2), 1x Describe (3), 1x Explain (4), 1x Extended response (6), 1x Discuss* (8, QWC assessed)

---

## Exam Technique Guide Mapping

`getGuideUrl(type)` in `main.js` maps practice question type strings to exam technique guide files via substring matching. Order matters — more specific matches must come first.

**Subject-specific entries (matched first):**

| Substring | Guide File | Subject |
|-----------|-----------|---------|
| `'Describe two'` | `describe-two.html` | History |
| `'Write an account'` | `write-an-account.html` | History |
| `'Explain the significance'` | `explain-significance.html` | History |
| `'Explain what was important'` | `explain-significance.html` | History |
| `'Explain two similarities'` | `explain-similarities.html` | History |
| `'In what ways'` | `in-what-ways.html` | History |
| `'Which had more impact'` | `which-had-more-impact.html` | History |
| `'How far do you agree'` | `factor-essay.html` | History |
| `'Has '` | `factor-essay.html` | History |

**Generic entries (at end of array — match after subject-specific):**

| Substring | Guide File | Used by |
|-----------|-----------|---------|
| `'Identify'` | `identify-state.html` | Sport Science |
| `'State'` | `identify-state.html` | Sport Science |
| `'Extended response'` | `extended-response.html` | Sport Science |
| `'Describe'` | `describe.html` | Sport Science, Geography |
| `'Explain'` | `explain.html` | Sport Science, Geography, Business |
| `'Discuss'` | `discuss.html` | Sport Science, Business |

When adding a new subject, check whether existing entries already match its question types. Only add new entries if no existing substring matches. Place subject-specific entries before generic ones.

---

## Knowledge Checks

5 per lesson. Inlined in `window.knowledgeCheck` array. Standard mix: 2 MCQ + 2 fill-in-the-blank + 1 match-up.

### Format

```javascript
// Multiple choice (0-based index for correct answer)
{ type: "mcq", q: "Question?", options: ["A", "B", "C", "D"], correct: 2 }

// Fill in the blank
{ type: "fill", q: "Sentence with _____.", options: ["w1", "w2", "w3", "w4"], correct: 1 }

// Match up (order array maps left[i] → right[order[i]])
{ type: "match", q: "Match:", left: ["A", "B", "C"], right: ["1", "2", "3"], order: [0, 1, 2] }
```

Best score saved to `studyvault-kc-{data-unit}/{data-lesson}` in localStorage.

---

## Sourcing Questions

### Practice questions
1. Check exam board past papers first — real exam questions are always preferred
2. Tag with `pastPaper: "Board Month Year"` (e.g. `"AQA June 2019"`, `"OCR January 2024"`)
3. Fill remaining slots with original questions written in the exam board's style
4. Mark schemes should list 3–6 bullet points students might include
5. For essay-type questions, include structure guidance (e.g. "both sides of the argument")

### Knowledge checks
1. Should test factual recall from the lesson content
2. MCQs: one correct answer, three plausible distractors
3. Fill-in-the-blank: sentence from the lesson with a key term removed
4. Match-up: pair terms with definitions, dates with events, or causes with effects
5. Keep language simple and unambiguous
