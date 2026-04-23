# Revision Technique Templates

Seven canonical templates for revision-technique guide pages. Each is backed by cognitive-science research. Agents fill in **only** the `{{SUBJECT_NAME}}`, `{{SUBJECT_SLUG}}`, `{{SUBJECT_EXAMPLE_1}}`, `{{SUBJECT_EXAMPLE_2}}` placeholders — they do NOT rewrite pedagogy, rephrase research, or invent new techniques. Canonical wording is locked.

One agent per subject build. Reads all 7 templates, fills subject-appropriate examples, inserts into `guide_pages` table.

## Hub page

`hub.html` — the index page at `/guide/{subject-slug}/revision-technique/`. Links to all 7 technique pages plus any optional subject-specific technique.

## Fixed techniques (always generated)

1. `retrieval-practice.html` — testing yourself as the act of learning
2. `spaced-repetition.html` — distributing practice over time
3. `interleaving.html` — mixing topics/skills in one session
4. `dual-coding.html` — combining words and visuals
5. `elaborative-interrogation.html` — asking why and how
6. `knowledge-organisers.html` — structuring knowledge into single pages
7. `timed-practice.html` — simulated exam conditions

## Optional subject-specific

A subject may add ONE extra technique that genuinely suits its domain (e.g. "Practising Calculations" for Science, "Vocabulary Laddering" for MFL). The planning agent decides whether to include one based on the subject's character.

## Rules

- Hub colour is fixed: `#16a34a` / `#f0fdf4` (green) for all subjects
- All links are absolute: `/guide/{subject-slug}/revision-technique/{slug}`
- HTML structure matches `<main class="lesson-content">` + `<aside class="lesson-sidebar">` as required by `guide-loader.js`
- The sidebar "Other Techniques" links list is populated by the agent at insert time (excluding the current page)
- Placeholders use `{{DOUBLE_BRACE}}` syntax; any unfilled placeholder in shipped content is a bug

## Placeholder reference

| Placeholder | Filled with | Example |
|---|---|---|
| `{{SUBJECT_NAME}}` | Subject name as student sees it | "Religious Education" |
| `{{SUBJECT_SLUG}}` | URL slug | "religious-education" |
| `{{SUBJECT_EXAMPLE_1}}` | First worked example — specific, short paragraph | See individual templates |
| `{{SUBJECT_EXAMPLE_2}}` | Second worked example | See individual templates |

Examples should:
- Use real subject content (real topics, real question types for the exam board)
- Be concrete and specific, not generic ("for History" rather than "a lesson")
- Show the technique in action, not describe it
- Be 2-4 sentences each

Example quality bar (retrieval practice, RE):

> *"After studying the Five Pillars of Islam, close the book and write down all five from memory, with one sentence explaining each. Check what you got wrong and rewrite only the missed ones tomorrow."*

NOT:

> *"You could use retrieval practice to help you remember things for Religious Education."*
