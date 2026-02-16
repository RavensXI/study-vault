# StudyVault — Project Reference

GCSE History revision site rebuilt from WordPress to static HTML. Opens directly in browser via `file://` protocol — no server, no build tools. Hosted on GitHub Pages via https://github.com/RavensXI/study-vault.

## Owner
Teacher: Tom Shaun, email: `t.shaun@unity.lancs.sch.uk`
Git config: user "Tom Shaun", email "tomshaun90@gmail.com"

## Current Status
**Phase 8 complete** — Exam Technique guide pages redesigned: two-column layout with sidebar, collapsible sections, styled tables, visible model answer annotations, and a Weak vs Strong comparison section on each guide. Hub page updated to grouped-by-paper layout.

**What's done:**
- Homepage with 4 unit cards and progress bars
- 4 unit contents/index pages with lesson cards and visited tracking
- 60 lesson pages across all 4 units (15 each), all with full GCSE content
- All 60 lessons cross-referenced against teacher classroom PowerPoints (100+ PPTs across all 4 units)
- Readability pass on all 60 lessons
- Glossary tooltip definitions trimmed to single-sentence definitions only (354 trimmed)
- Hero images on all 60 lesson pages (Wikimedia Commons, public domain/CC)
- Infographic diagrams on all 60 lesson pages (Gemini API generated, one per lesson minimum)
- Practice questions on all 60 lessons (6 per lesson, 360 total) with real AQA past paper questions tagged
- TTS narration player UI on all 60 lesson pages — **audio files currently removed**, awaiting ElevenLabs regeneration
- Accessibility toolbar: dark mode, dyslexia font, font sizing, Irlen overlays
- Glossary tooltips, collapsible sections, timelines, key fact boxes, lightbox, scroll progress bar
- Page transitions, floating narration mini-player, auto-scroll suppression
- Logo: inline SVG padlock icon in "StudyVault." — uses `currentColor`, adapts to dark mode
- Embedded YouTube video players in sidebar (45 lessons — America has no videos yet)
- Related Media sidebar sections on all 60 lessons (Podcasts, Movies, TV Shows, Documentaries, Study Tools)
- Knowledge Check quizzes on all 60 lessons (5 questions per lesson, 300 total)
- Exam Technique guide section — 1 hub page + 7 guide pages for every AQA question type

**Still TODO:**
- TTS narration regeneration with ElevenLabs cloned voice — one unit per month (~$22/month). Generation script: `generate_tts.py`. All 60 WAV/JSON files deleted; player UI remains ready.
- PWA (service worker + manifest.json)
- Delete old v1 flat HTML files (conflict-tension.html, health-people.html, elizabethan.html, america.html)

---

## File Structure
```
Study Vault/
├── CLAUDE.md                 ← This file
├── index.html                ← Homepage (4 unit cards + progress)
├── preview.html              ← Responsive preview tool (dev only)
├── css/style.css             ← All styling
├── js/main.js                ← All JS
├── images/padlock.svg        ← Logo lock icon source
├── fonts/opendyslexic-0.91.12/compiled/  ← OpenDyslexic woff2/woff
├── conflict-tension/         ← 15 lessons + hero images + diagrams
├── health-people/            ← 15 lessons + hero images + diagrams
├── elizabethan/              ← 15 lessons + hero images + diagrams
├── america/                  ← 15 lessons + hero images + diagrams
├── exam-technique/
│   ├── index.html            ← Hub page with 7 guide cards
│   ├── factor-essay.html     ← 16+4 SPaG: "How far do you agree?"
│   ├── write-an-account.html ← 8 marks: "Write an account"
│   ├── explain-significance.html ← 8 marks: "Explain significance/importance"
│   ├── which-had-more-impact.html ← 12 marks: "Which had more impact?"
│   ├── in-what-ways.html     ← 8 marks: "In what ways were lives affected?"
│   ├── explain-similarities.html ← 8 marks: "Explain two similarities"
│   └── describe-two.html     ← 4 marks: "Describe two"
│
│ TEACHER REFERENCE (not committed):
└── Spec and Materials/
    └── Lessons/ → Health/, America/, Conflict/, Elizabeth/ (note: "Elizabeth" not "Elizabethan")
```

---

## API Details

API keys are stored in environment variables — never commit them to the repo.

### Gemini API
- **Environment variable**: `GEMINI_API_KEY`
- **Image model**: `gemini-3-pro-image-preview` (best text accuracy)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent`

### TTS — ElevenLabs
- **Environment variable**: `ELEVENLABS_API_KEY`
- **Voice ID**: `Nd6wm0mR1AWfjae7WcRB` (cloned voice)
- **Model**: `eleven_turbo_v2_5` (0.5 credits per character)
- **Script**: `generate_tts.py` — see script for full process details

---

## Unit Colour Themes

Each unit has a body class that sets CSS custom properties:

| Unit | Body class | Accent | Light BG | Badge |
|------|-----------|--------|----------|-------|
| Conflict & Tension | `unit-conflict` | `#c44536` (terracotta) | `#fdf2f0` | `#fce8e5` |
| Health & People | `unit-health` | `#0d9488` (teal) | `#f0fdfa` | `#ccfbf1` |
| Elizabethan | `unit-elizabethan` | `#b45309` (amber) | `#fffbeb` | `#fef3c7` |
| America | `unit-america` | `#2563eb` (blue) | `#eff6ff` | `#dbeafe` |
| Exam Technique | `unit-exam-technique` | `#7c3aed` (purple) | `#f5f3ff` | `#ede9fe` |

---

## Lesson Page Template

Every lesson page follows the same structure. **Copy `conflict-tension/lesson-01.html` as the template** — it has the full markup for header, nav, accessibility toolbar, narration player, sidebar, and scripts.

Key structural elements:
- `<body class="unit-UNITCLASS" data-unit="UNIT-SLUG" data-lesson="lesson-NN">`
- `<div class="scroll-progress">` at top
- `<div class="lesson-page">` wraps `<main class="lesson-content">` + `<aside class="lesson-sidebar">`
- Content goes in `<article class="study-notes">` with `data-narration-id="n1"`, `n2`, etc. on every element
- Three inline `<script>` blocks at bottom: `window.narrationManifest`, `window.practiceQuestions`, `window.knowledgeCheck`

### Content Components

**Key Fact box:**
```html
<div class="key-fact" data-narration-id="nX">
  <div class="key-fact-label">Key Fact</div>
  <p>Content here...</p>
</div>
```

**Collapsible section:**
```html
<div class="collapsible">
  <button class="collapsible-toggle" aria-expanded="false">
    <span>Toggle title</span>
    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </button>
  <div class="collapsible-content">
    <div class="collapsible-inner">
      <p data-narration-id="nX">Content...</p>
    </div>
  </div>
</div>
```

**Timeline:**
```html
<div class="timeline" data-narration-id="nX">
  <div class="timeline-event">
    <div class="timeline-date">DATE</div>
    <h4>Event title</h4>
    <p>Description</p>
  </div>
</div>
```

**Glossary term:**
```html
<dfn class="term" data-def="Single-sentence definition only — no context.">term</dfn>
```

**Diagram / Hero image:**
```html
<figure class="diagram">
  <img src="diagram_name.png" alt="Descriptive alt text">
</figure>

<figure class="lesson-hero-image">
  <img src="lesson-NN-hero.jpg" alt="..." style="object-position: center XX%;">
  <figcaption>Short description with attribution</figcaption>
</figure>
```

### Practice Questions Format

All 60 lessons have 6 practice questions each (360 total). Real past paper questions tagged with `pastPaper` property (renders gold badge). Each unit uses different AQA question types:

**Conflict & Tension** (AQA 8145/1A/B): 3x "Write an account" (8m) + 3x "How far do you agree?" (16m+4 SPaG)
**Health & the People** (AQA 8145/2A/A): Mix of "Explain significance" (8m), "Explain similarities" (8m), "Has [factor] been main factor?" (16m+4 SPaG)
**Elizabethan** (AQA 8145/2B/C): Mix of "Explain what was important" (8m) + "Write an account" (8m)
**America** (AQA 8145/1A/D): 2x "Describe two" (4m) + 2x "In what ways" (8m) + 2x "Which had more impact" (12m)

```javascript
window.practiceQuestions = [
  {
    type: "8 marks \u2014 Write an account",
    pastPaper: "AQA June 2022",  // only on real exam questions
    text: "Write an account of...",
    marks: "All historically relevant...\n\nLevel 4 (7\u20138 marks): Complex analysis..."
  }
];
```

**Important:** Use unicode escapes in JS strings (`\u2014` em dash, `\u2013` en dash, `\u2019`/`\u2018` smart quotes, `\u2022` bullet). Past paper question text must use exact AQA wording.

### Knowledge Check Format

All 60 lessons have 5 questions (300 total). Three types:

```javascript
// MCQ — correct is 0-based index. 4 options in 2x2 grid.
{ type: "mcq", q: "Question?", options: ["A", "B", "C", "D"], correct: 2 }

// Fill-in-the-blank — options shuffled as pill buttons. Blank shown as _____.
{ type: "fill", q: "Sentence with a _____.", options: ["wrong1", "correct", "wrong2", "wrong3"], correct: 1 }

// Match-up — left fixed, right in shuffled dropdowns. order[i] = correct right index for left[i].
{ type: "match", q: "Match:", left: ["A", "B", "C"], right: ["1", "2", "3"], order: [0, 1, 2] }
```

**Standard mix per lesson:** 2 MCQ + 2 fill-in-the-blank + 1 match-up. Best score saved to localStorage `studyvault-kc-{data-unit}/{data-lesson}`.

---

## Exam Technique Section

7 guide pages in `exam-technique/` covering every AQA question type. Accessible from homepage banner and "How do I answer this?" links on practice questions.

| File | Marks | Question Type | Units |
|------|-------|--------------|-------|
| `factor-essay.html` | 16+4 SPaG | "How far do you agree?" / "Has [factor] been the main factor?" | Conflict, Health |
| `write-an-account.html` | 8 | "Write an account of..." | Conflict, Elizabethan |
| `explain-significance.html` | 8 | "Explain the significance/importance..." | Health, Elizabethan |
| `which-had-more-impact.html` | 12 | "Which had more impact?" | America |
| `in-what-ways.html` | 8 | "In what ways were lives affected?" | America |
| `explain-similarities.html` | 8 | "Explain two ways... similar" | Health |
| `describe-two.html` | 4 | "Describe two..." | America |

Guide pages use the same `lesson-page` two-column layout as lessons. Each contains: What the Examiner Wants, Step-by-Step Formula, Timing, Paragraph Templates (collapsible), Annotated Model Answer (collapsible), Weak vs Strong comparison (collapsible), Common Mistakes. Sidebar has Quick Reference card, Video placeholder, and Other Guides collapsible. See any guide HTML for the full pattern.

### JS guide link mapping
`getGuideUrl(type)` maps practice question `type` strings to guide filenames via substring matching:
- `'Describe two'` → `describe-two.html`
- `'Write an account'` → `write-an-account.html`
- `'Explain the significance'` / `'Explain what was important'` → `explain-significance.html`
- `'Explain two similarities'` → `explain-similarities.html`
- `'In what ways'` → `in-what-ways.html`
- `'Which had more impact'` → `which-had-more-impact.html`
- `'How far do you agree'` / `'Has '` (trailing space) → `factor-essay.html`

---

## Image Generation

### Design principles for diagrams
- **Break up text, don't add more** — primarily visual, labels 3-5 words max
- **Don't double up** — if a diagram covers a key-fact box or bullet list, remove the text element
- **One clear concept per image** — pick one visual idea and commit
- **Use the unit accent colour** — see Unit Colour Themes table
- **Clean and professional** — textbook infographic style, white background, landscape format

### Prompt pattern
```
Create a clear educational diagram showing [SUBJECT].
Use a warm color palette with [UNIT ACCENT COLOR] as the primary color.
Keep text MINIMAL — short labels only, let the visuals communicate the concept.
Clean white background, landscape format, professional textbook quality.
Suitable for GCSE students aged 15-16.
No watermarks.
```

---

## JS Features (main.js)

All initialised in `DOMContentLoaded`:
- `initScrollProgress()` — accent-coloured bar at page top
- `initCollapsibles()` — expand/collapse with smooth animation
- `initVisitedTracking()` — localStorage `studyvault-visited`
- `initMobileNav()` — hamburger menu
- `initPracticeQuestions()` — random question selection, mark scheme display, past paper badges, guide links
- `initNarration()` — play/pause, progress, speed toggle, paragraph highlighting, mini-player, auto-scroll suppression
- `initAccessibility()` — dark mode, dyslexia font, font size, Irlen overlays (persisted in `studyvault-a11y`)
- `initGlossary()` — popup tooltips from `data-def` attributes
- `initKnowledgeCheck()` — modal quiz overlay, best score in localStorage
- `initLightbox()` — click-to-expand on hero images and diagrams
- `initHeroEdit()` — `?hero-edit` URL param for adjusting hero image positions
- `initPageTransitions()` — fade-out/in between internal pages

---

## Design Rules
- Background: warm cream `#faf8f5`, not bright white
- Text: warm dark brown `#2d2a26`, not pure black
- Font: Inter (body) + Source Serif 4 (headings) via Google Fonts
- Cards: `border-radius: 16px`, soft warm shadows
- All data inlined in HTML (not fetched) due to file:// CORS restrictions
- Narration highlight: gold `#fef9e7` with `#e6b800` border
- Hero images: `object-fit: cover`, 280px desktop / 200px mobile

## Sidebar Structure
Three sections in order: **Knowledge Check** (button → modal quiz), **Related Media** (collapsible categories: Lesson Podcast first, Study Tools last), **Video** (YouTube iframe, 45 lessons — not America). See `conflict-tension/lesson-01.html` for full HTML patterns.

Do NOT add a "Key Facts" section to the sidebar. The sidebar does NOT scroll independently — `position: sticky; top: 5rem`.

### Related Media link conventions
- **Podcasts**: specific episode URLs (BBC Sounds, Spotify, etc.) — never generic show pages
- **Movies/TV/Documentaries**: JustWatch UK links (`justwatch.com/uk/movie/SLUG`)
- Max ~3 items per category. Only include categories with genuine content.

---

## Content Editing Conventions

**Scope:** Only edit within `<article class="study-notes">`, `<div class="exam-tip">`, and `<div class="conclusion">`. Never touch header, sidebar, nav, scripts, or structural markup.

**Preserve:**
- All `data-narration-id` attributes (TTS paragraph highlighting)
- All `<dfn class="term" data-def="...">` glossary terms — single concise sentence definitions
- HTML structure: collapsibles, timelines, key-fact boxes, diagrams
- HTML entities: `&mdash;` `&ndash;` `&rsquo;` `&lsquo;` `&ldquo;` `&rdquo;` `&amp;`

**Readability targets (GCSE age 15-16):**
- Short sentences, active voice, minimal filler
- Prefer concrete over abstract
- Key takeaways: 2-3 tight bullets, not exhaustive lists

**Cross-referencing against teacher PPTs:**
- Read PPTs with `python -m markitdown "filepath"` (only .pptx, not old .ppt)
- Only add exam-relevant content: specific facts, dates, names, statistics
- Weave additions naturally into existing sections

## Conflict & Tension Hero Images
Note: Conflict hero images use older naming (e.g. `Versailles_1919.jpg`, `lesson 2 hero.jpg` with spaces). Other units use `lesson-NN-hero.jpg`.
