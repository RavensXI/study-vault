# StudyVault — Project Reference

Multi-subject GCSE revision site rebuilt from WordPress to static HTML. Opens directly in browser via `file://` protocol — no server, no build tools. Hosted on GitHub Pages via https://github.com/RavensXI/study-vault. Currently History only — Geography and English Literature are planned (Coming Soon cards on homepage).

## Owner
Teacher: Tom Shaun, email: `t.shaun@unity.lancs.sch.uk`
Git config: user "Tom Shaun", email "tomshaun90@gmail.com"

## Current Status
**Platform branch** — This branch extends the single-subject History site into a multi-subject GCSE revision platform. It is being developed separately from `main` so current students can keep using the live History site while platform features are built. The `main` branch has the live student-facing site (History only); this `platform` branch adds login, subject selection, a student dashboard, and moves all History content into a `history/` subfolder.

**Main branch** — Exam Technique guide pages (Phase 8 complete), plus all original History content at root level. See the `main` branch CLAUDE.md for full details on lesson content, practice questions, knowledge checks, etc.

**What's done:**
- Homepage with 4 unit cards and progress bars
- 4 unit contents/index pages with lesson cards and visited tracking
- 60 lesson pages across all 4 units (15 each), all with full GCSE content
- All 60 lessons cross-referenced against teacher classroom PowerPoints (100+ PPTs across all 4 units) — missing exam-relevant facts, dates, statistics, and key figures added
- Readability pass on all 60 lessons — shorter sentences, simpler vocabulary, tighter key takeaways for GCSE students (age 15-16, potentially lower reading ages)
- Glossary terms added/expanded across all lessons during cross-reference pass
- Glossary tooltip definitions trimmed to single-sentence definitions only (354 trimmed) — no contextual info that duplicates surrounding text
- Hero images on all 60 lesson pages (Wikimedia Commons, public domain/CC)
- Infographic diagrams on all 60 lesson pages (Gemini API generated, one per lesson minimum) — each replaces a text element (key fact box, collapsible, or bullet list) to avoid duplication
- Practice questions on all 60 lessons (6 per lesson, 360 total) with real AQA past paper questions tagged — see Practice Questions section below
- TTS narration player UI on all 60 lesson pages (player, mini-player, keyboard shortcuts, paragraph highlighting) — **audio files currently removed**, awaiting ElevenLabs regeneration (see TODO)
- Accessibility toolbar: dark mode, dyslexia font, font sizing, Irlen overlays
- Glossary tooltips, collapsible sections, timelines, key fact boxes
- Floating narration mini-player (appears when main player scrolls out of view)
- Auto-scroll suppression (if student scrolls away during narration, it stops following)
- Scroll progress bar on lesson pages
- Page transitions (JS fade-out/in with CSS animations, animationend fix for position:fixed)
- Interactive hero image position editor (`?hero-edit` URL param)
- Homepage scrolling quote ticker
- Lightbox for hero images and diagrams (click to expand)
- "Click to expand" hover hint on hero images
- Past paper badge (gold "Past paper" tag) on real exam questions
- Logo: inline SVG padlock icon replaces the period in "StudyVault." — uses `currentColor`, scales with text, adapts to dark mode (source SVG in `images/padlock.svg`)
- Mark scheme button positioned above content (not below) so students don't scroll to close
- Glossary tooltips no longer clipped inside open collapsible sections
- Embedded YouTube video players in sidebar (45 lessons across Conflict, Health, Elizabethan — America has no videos yet)
- Related Media sidebar sections on all 60 lessons — collapsible categories for Podcasts, Movies, TV Shows, Documentaries with curated, lesson-specific links (specific episode URLs for podcasts, JustWatch UK for video content)
- Lesson Podcast (NotebookLM-generated) added as first item in Related Media Podcasts collapsible on all 60 lessons
- Study Tools collapsible (NotebookLM link) added to Related Media on all 60 lessons
- Resources sidebar section removed (Podcast and Notebook consolidated into Related Media)
- Navigate sidebar section removed (redundant with top nav bar)
- Knowledge Check quizzes on all 60 lessons (5 questions per lesson, 300 total) — modal overlay with MCQ, fill-in-the-blank, and match-up question types. Best score saved to localStorage. See Knowledge Check section below.
- Exam Technique guide section — 1 hub page + 7 guide pages for every AQA question type (4/8/12/16+4 marks). Each guide has: What the Examiner Wants, Step-by-Step Formula, Timing breakdown, Paragraph Templates, Annotated Model Answer, Common Mistakes. "How do I answer this?" links appear dynamically on all 60 lessons' practice questions (JS-driven, no lesson HTML changes). Homepage banner links to hub. See Exam Technique section below.
- Multi-subject platform structure — History content moved into `history/` subfolder
- Student login system with 3 demo accounts (Emma, Jake, Guest)
- Subject picker — 25 GCSE subjects in 6 groups (Core, Sciences, Languages, Humanities, Creative & Practical, Business & Computing)
- Student dashboard with greeting, exam countdown, today's revision cards, progress stats, subject grid
- Subject card images for all 25 subjects (Unsplash/free stock photos)

**Still TODO:**
- TTS narration regeneration with ElevenLabs cloned voice — one unit per month (~$22/month on Creator plan, ~355k credits total). All 60 WAV and JSON files have been deleted; `<source src="">` and `window.narrationManifest` cleared in all HTML. The narration player UI remains in place ready for new audio. The 184 missing `data-narration-id` attributes on `<ul>`/`<ol>` elements have been fixed, so bullet lists will be included when audio is regenerated. Generation script: `generate_tts.py` (ElevenLabs version).
- PWA (service worker + manifest.json)
- Delete old v1 flat HTML files (conflict-tension.html, health-people.html, elizabethan.html, america.html)

**What didn't work — Gemini 2.5 Flash TTS (abandoned):**
Attempted using Gemini TTS (`gemini-2.5-flash-preview-tts`) as a cheap interim replacement (~$3–5 total for all 60 lessons). Script: `generate_tts_gemini.py`. Generated all 60 lessons with Charon/Kore voices + faster-whisper timestamp alignment. Two fatal issues:
1. **Progressive speedup** — the model progressively eliminates pauses as text gets longer. Silence between words drops from ~35% to ~15% over the course of a lesson, effectively doubling speech rate by the end. Affects ALL lessons, not just long ones. By the final minutes the audio is unintelligibly fast with a high-pitched screeching quality.
2. **Hard output cap at ~655 seconds** — 5 longer lessons (health L12, america L02/L07/L13/L14) hit an exact 31,446,330-byte ceiling. The model compresses all remaining text into the fixed output window, making the speedup even more extreme.
Batching into shorter API calls (~3000 chars each) was tried but still exhibited speedup within each batch, plus audible pace jumps between batches. Gemini TTS is unsuitable for long-form narration. ElevenLabs remains the only viable option.

**Future features (planned but not started):**
- Retrieval Practice — cross-lesson spaced repetition quiz (separate from per-lesson Knowledge Check). Would dynamically select questions from lessons the student studied days/weeks ago. Requires backend.
- Student logins and database — needed for spaced repetition, cross-device progress sync, and teacher analytics. Likely Supabase (free tier) + Vercel/Netlify hosting. Essentially zero cost at school scale.
- Multi-school licensing — potential to sell to other schools (£500–1,500/year per subject). Platform could allow other teachers to create content for their subjects.

---

## File Structure
```
Study Vault/
├── CLAUDE.md                 ← This file
├── index.html                ← NEW: subject selection homepage (History + Coming Soon cards)
├── preview.html              ← Responsive preview tool (dev only)
├── css/style.css             ← All styling
├── js/main.js                ← All JS
├── images/padlock.svg            ← Logo lock icon source (inline SVG used in all pages)
├── fonts/opendyslexic-0.91.12/compiled/  ← OpenDyslexic woff2/woff
├── history/
│   ├── index.html            ← History landing page (4 unit cards + progress + quotes)
│   ├── conflict-tension/
│   │   ├── index.html            ← Unit contents page
│   │   ├── lesson-01.html … lesson-15.html  ← All 15 lessons (full content)
│   │   ├── Versailles_1919.jpg              ← Hero images (various naming)
│   │   ├── lesson 2 hero.jpg … etc
│   │   └── diagram_*.png                    ← Infographic diagrams (15 files)
│   ├── health-people/
│   │   ├── index.html
│   │   ├── lesson-01.html … lesson-15.html  ← All 15 lessons (full content)
│   │   ├── lesson-01-hero.jpg … lesson-15-hero.jpg  ← Hero images
│   │   └── diagram_*.png                    ← Infographic diagrams (21 files)
│   ├── elizabethan/
│   │   ├── index.html
│   │   ├── lesson-01.html … lesson-15.html  ← All 15 lessons (full content)
│   │   ├── lesson-01-hero.jpg … lesson-15-hero.jpg  ← Hero images
│   │   └── diagram_*.png                    ← Infographic diagrams (20 files)
│   ├── america/
│   │   ├── index.html
│   │   ├── lesson-01.html … lesson-15.html  ← All 15 lessons (full content)
│   │   ├── lesson-01-hero.jpg … lesson-15-hero.jpg  ← Hero images
│   │   └── diagram_*.png                    ← Infographic diagrams (15 files)
│   └── exam-technique/
│       ├── index.html            ← Hub page with 7 guide cards
│       ├── factor-essay.html     ← 16+4 SPaG: "How far do you agree?" (Conflict, Health)
│       ├── write-an-account.html ← 8 marks: "Write an account" (Conflict, Elizabethan)
│       ├── explain-significance.html ← 8 marks: "Explain significance/importance" (Health, Elizabethan)
│       ├── which-had-more-impact.html ← 12 marks: "Which had more impact?" (America)
│       ├── in-what-ways.html     ← 8 marks: "In what ways were lives affected?" (America)
│       ├── explain-similarities.html ← 8 marks: "Explain two similarities" (Health)
│       └── describe-two.html     ← 4 marks: "Describe two" (America)
│
│ OLD v1 FILES (to be deleted):
├── conflict-tension.html
├── health-people.html
├── elizabethan.html
├── america.html
│
│ TEACHER REFERENCE (not committed — .gitignore or just leave untracked):
└── Spec and Materials/
    ├── Lessons/
    │   ├── Health/          ← 15+ .pptx files
    │   ├── America/         ← 45+ .pptx files
    │   ├── Conflict/        ← 35 .pptx files
    │   └── Elizabeth/       ← 16 .pptx files (note: folder is "Elizabeth" not "Elizabethan")
    ├── Health Past Exams/   ← 7 sittings (AQA 8145/2A/A)
    ├── Elizabeth Past Exams/ ← 7 sittings (AQA 8145/2B/C)
    └── America Past Exams/  ← 7 sittings (AQA 8145/1A/D)
```

### Path conventions after history/ migration
- **Lesson/unit pages** reference CSS/JS as `../../css/style.css` and `../../js/main.js`
- **`history/index.html`** references CSS/JS as `../css/style.css` and `../js/main.js`
- **Root `index.html`** references CSS/JS as `css/style.css` and `js/main.js`
- **`../index.html`** links in lesson/unit pages naturally resolve to `history/index.html` (correct)
- **`../exam-technique/`** in JS `getGuideUrl()` resolves to `history/exam-technique/` (correct)

---

## Platform Features (this branch only)

### Branch relationship
- **`main`** — live student-facing site. History content at root level (`conflict-tension/`, `health-people/`, etc.). Single-subject, no login.
- **`platform`** — multi-subject platform. History content under `history/` subfolder. Login system, subject picker, dashboard. Will eventually replace `main` when ready.
- When merging `main` improvements into `platform`, be aware of the path difference (root vs `history/` subfolder).

### Student Login System

The root `index.html` is a single-page app with three views: login, subject picker, and dashboard. All state is in localStorage — no backend.

**Three demo accounts:**
```javascript
var demoUsers = [
  { username: 'emma', password: 'revision', name: 'Emma Wilson',
    defaults: ['history','english-lit','maths','combined-science','geography','french','fine-art'],
    examDate: '2026-05-11',
    stats: { lessons: 14, totalLessons: 60, avgScore: 78, streak: 5 },
    todayRevision: [
      { subject: 'History', lesson: 'The Abyssinia Crisis', tag: 'new', color: '#c44536', url: 'history/conflict-tension/lesson-09.html' },
      { subject: 'English Lit', lesson: 'An Inspector Calls: Themes', tag: 'revisit', color: '#7c3aed' },
      { subject: 'Geography', lesson: 'Urban Challenges in the UK', tag: 'new', color: '#059669' },
      { subject: 'French', lesson: 'School and Education Vocabulary', tag: 'new', color: '#1d4ed8' }
    ]
  },
  { username: 'jake', password: 'revision', name: 'Jake Morris',
    defaults: ['history','english-lang','maths','physics','computer-science','sport-science','business'],
    examDate: '2026-05-11',
    stats: { lessons: 9, totalLessons: 60, avgScore: 65, streak: 3 },
    todayRevision: [
      { subject: 'History', lesson: 'America and the Boom', tag: 'new', color: '#c44536', url: 'history/america/lesson-01.html' },
      { subject: 'Physics', lesson: 'Energy Stores and Transfers', tag: 'revisit', color: '#0284c7' },
      { subject: 'Computer Science', lesson: 'Binary and Data Representation', tag: 'new', color: '#4f46e5' },
      { subject: 'Maths', lesson: 'Quadratic Equations', tag: 'new', color: '#2563eb' }
    ]
  },
  { username: 'guest', password: 'guest', name: 'Guest Student',
    defaults: null, examDate: '2026-05-11', stats: null, todayRevision: null }
];
```

**Auth flow:**
1. User enters username/password → matched against `demoUsers` array
2. On match: `{ username, name }` saved to `localStorage` key `studyvault-user`
3. Demo data (stats, todayRevision, examDate) saved to `studyvault-demo-{username}`
4. If user has saved subjects → go to dashboard. If not (or guest) → go to subject picker
5. Sign out clears the user key and shows login again

**Helper functions in index.html:**
- `getUser()` / `setUser(u)` / `clearUser()` — manage `studyvault-user` in localStorage
- `findDemoUser(username)` — look up a demo user by username
- `getDemoData()` / `saveDemoData(demo)` — manage `studyvault-demo-{username}` in localStorage
- `getSaved()` / `save(ids)` — manage `studyvault-subjects-{username}` in localStorage

### Subject Picker

25 GCSE subjects across 6 groups. Cards show subject image, name, and exam board. Students toggle cards to select/deselect. "Continue" button requires at least one selection.

**Subject groups:**
| Group | Subjects |
|-------|----------|
| Core | English Language (AQA), English Literature (AQA), Mathematics (Edexcel) |
| Sciences | Combined Science Trilogy (AQA), Biology (AQA), Chemistry (AQA), Physics (AQA) |
| Languages | French (AQA), German (AQA), Spanish (AQA) |
| Humanities | Geography (AQA), **History (AQA)** ← only active subject, Religious Studies (AQA) |
| Creative & Practical | Fine Art, Textiles, Photography, D&T, Food, Drama (OCR), Music (Eduqas), Music Tech (NCFE) |
| Business & Computing | Business (Edexcel), Computer Science (OCR), Creative iMedia (OCR), Sport Science (OCR) |

Only History has `active: true` and a `url` property. All other subjects render as "Coming Soon" cards (greyed out, non-clickable).

**Subject images:** `images/subject-{id}.jpg` — one per subject. Downloaded from Unsplash via `download_subject_images.py`. History image uses the existing hero style.

### Student Dashboard

Visible after login when subjects are saved. Four sections top to bottom:

**1. Greeting + Exam Countdown**
- Time-of-day greeting: "Good morning, Emma" / "Good afternoon" / "Good evening"
- Countdown pill: "84 days until your first exam" (AQA GCSEs start May 11, 2026)

**2. Today's Revision Panel**
- 3-4 cards in horizontal row. Each shows subject colour accent, subject name, lesson title, tag ("New" green / "Revisit" amber)
- History cards have URLs and are clickable links. Other subjects are greyed-out divs
- Guest user sees "Select your subjects to get started"

**3. Progress Stats Row**
- 3 stat cards: Lessons completed (X / 60 with progress bar), Avg quiz score (% with colour: green ≥70, amber ≥50, red <50), Best streak (X days)
- Hidden for guest user (no stats)

**4. Subject Cards Grid**
- Shows only the user's selected subjects (not all 25)
- History card shows progress bar with lesson count
- Other subjects show "Coming Soon" badge
- "Change subjects" and "Sign out" buttons above the grid

### CSS for platform features

All platform CSS is in `css/style.css`. Key class patterns:

**Login:** `.login-section`, `.login-box`, `.login-field`, `.login-btn`, `.login-error`, `.login-demo`, `.login-demo-account`

**Subject picker:** `.subject-picker`, `.picker-intro`, `.picker-group`, `.picker-group-label`, `.picker-group-cards`, `.picker-card`, `.picker-card.selected`, `.picker-card-image`, `.picker-card-name`, `.picker-card-board`, `.picker-card-check`, `.picker-continue-btn`

**Dashboard:** `.dashboard`, `.dashboard-greeting-row`, `.dashboard-greeting`, `.greeting-text`, `.dashboard-countdown`, `.dashboard-section-title`, `.dashboard-today`, `.today-cards`, `.today-card`, `.today-card--disabled`, `.today-card-subject`, `.today-card-lesson`, `.today-tag`, `.today-tag--new`, `.today-tag--revisit`, `.dashboard-stats`, `.stat-card`, `.stat-value`, `.stat-total`, `.stat-label`, `.stat-bar`, `.stat-bar-fill`, `.stat-good`, `.stat-ok`, `.stat-low`, `.dashboard-actions`, `.dashboard-action-btn`, `.dashboard-signout-btn`

**Subject cards:** `.subject-grid`, `.subject-card`, `.subject-card--coming-soon`, `.unit-card-image`, `.unit-card-body`, `.subject-progress`, `.subject-progress-bar`, `.subject-progress-fill`, `.subject-progress-label`, `.coming-soon-badge`

All have dark mode variants via `body.dark-mode` selectors. Mobile responsive breakpoints at 960px and 768px.

### What's still needed on this branch
- Merge latest `main` changes (exam technique hub redesign, guide page improvements) into platform branch — adjust paths from root to `history/` subfolder
- Eventually: real authentication backend (likely Supabase), cross-device progress sync
- Eventually: content for other subjects beyond History
- Eventually: replace `main` with `platform` as the live site

---

## API Details

API keys are stored in environment variables — never commit them to the repo.

### Gemini API
- **Environment variable**: `GEMINI_API_KEY`
- **Image model**: `gemini-3-pro-image-preview` (best text accuracy)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent`
- **Cost**: ~$0.134 per image

### TTS (Text-to-Speech) — ElevenLabs
- **Environment variable**: `ELEVENLABS_API_KEY`
- **Provider**: ElevenLabs (Creator plan, $22/month, 107k credits/month + extra usage enabled)
- **Voice ID**: `Nd6wm0mR1AWfjae7WcRB` (cloned voice)
- **Model**: `eleven_turbo_v2_5` (0.5 credits per character)
- **Output format**: Raw PCM 24kHz 16-bit mono → converted to WAV via Python
- **Generation script**: `generate_tts.py` (Python, uses ElevenLabs REST API)

---

## Unit Colour Themes

Each unit has a body class that sets CSS custom properties:

| Unit | Body class | Accent | Light BG | Badge |
|------|-----------|--------|----------|-------|
| Conflict & Tension | `unit-conflict` | `#c44536` (terracotta) | `#fdf2f0` | `#fce8e5` |
| Health & People | `unit-health` | `#0d9488` (teal) | `#f0fdfa` | `#ccfbf1` |
| Elizabethan | `unit-elizabethan` | `#b45309` (amber) | `#fffbeb` | `#fef3c7` |
| America | `unit-america` | `#2563eb` (blue) | `#eff6ff` | `#dbeafe` |

---

## Lesson Page Template

Every lesson page follows this exact structure. Copy `conflict-tension/lesson-01.html` as the template.

### HTML skeleton
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson N: TITLE - StudyVault</title>
  <link rel="stylesheet" href="../../css/style.css">
</head>
<body class="unit-UNITCLASS" data-unit="UNIT-SLUG" data-lesson="lesson-NN">

  <div class="scroll-progress"></div>

  <header class="page-header">
    <!-- Brand + nav (see lesson-01 for full markup) -->
  </header>
  <div class="mobile-overlay"></div>

  <div class="lesson-page">
    <main class="lesson-content">

      <div class="lesson-header">
        <span class="lesson-number">Lesson N of TOTAL</span>
        <h1>TITLE</h1>
      </div>

      <!-- Hero image -->
      <figure class="lesson-hero-image">
        <img src="lesson-NN-hero.jpg" alt="..." style="object-position: center XX%;">
        <figcaption>Description</figcaption>
      </figure>

      <!-- Accessibility Toolbar (copy from lesson-01 exactly) -->
      <div class="a11y-toolbar">...</div>

      <!-- Narration Player (copy from lesson-01 exactly) -->
      <div class="narration-player">...</div>

      <!-- Study Notes -->
      <article class="study-notes">
        <!-- Content with data-narration-id="n1", n2, etc. on every element -->
        <!-- Use: h2, h3, p, .key-fact, .exam-tip, .collapsible, .timeline, .diagram -->
        <!-- Use: <dfn class="term" data-def="...">word</dfn> for glossary terms -->
      </article>

      <!-- Exam Tip -->
      <div class="exam-tip" data-narration-id="nXX">...</div>

      <!-- Conclusion with Key Takeaways (2-3 bullets) -->
      <div class="conclusion" data-narration-id="nXX">
        <h2>Conclusion</h2>
        <p>Summary paragraph...</p>
        <h3>Key Takeaways</h3>
        <ul>
          <li><strong>Point:</strong> Explanation</li>
        </ul>
      </div>

      <!-- Practice Questions -->
      <section class="practice-section" id="practice">...</section>

      <!-- Prev/Next Nav -->
      <nav class="lesson-nav">...</nav>

      <a href="index.html" class="back-link">← Back to UNIT NAME</a>

    </main>

    <aside class="lesson-sidebar">
      <!-- Knowledge Check, Related Media, Video (see lesson-01) -->
    </aside>
  </div>

  <script src="../../js/main.js"></script>
  <script>
    window.narrationManifest = [ /* timestamp data */ ];
    window.practiceQuestions = [ /* question bank */ ];
    window.knowledgeCheck = [ /* 5 quiz questions */ ];
  </script>
</body>
</html>
```

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

**Diagram:**
```html
<figure class="diagram">
  <img src="diagram_name.png" alt="Descriptive alt text">
</figure>
```

**Hero image:**
```html
<figure class="lesson-hero-image">
  <img src="lesson-NN-hero.jpg" alt="Descriptive alt text" style="object-position: center XX%;">
  <figcaption>Short description with attribution</figcaption>
</figure>
```
Hero images use `object-fit: cover` at 280px height (200px mobile). Use `?hero-edit` URL param to interactively drag-adjust positions, then copy the values.

### Practice Questions Format

All 60 lessons have 6 practice questions each (360 total). Questions use AQA past paper wording where available. Real past paper questions are tagged with `pastPaper` property which renders a gold "Past paper" badge via `showQuestion()` in main.js.

Each unit uses different AQA exam paper question types:

**Conflict & Tension** (AQA 8145/1A/B — Paper 1 Section A):
- 3x Q03 "Write an account of..." (8 marks)
- 3x Q04 "'Statement.' How far do you agree?" (16 marks +4 SPaG)
- Q04s draw from fixed factor pools: Treaty (L01–L04), League (L05–L09), WWII causes (L10–L15)

**Health & the People** (AQA 8145/2A/A — Paper 2 Section A):
- Mix of Q02 "Explain the significance of..." (8 marks) and Q03 "Explain two ways similar..." (8 marks)
- Q04 "Has [factor] been the main factor in...?" (16 marks +4 SPaG)
- Q04 factors: science & technology, individual, war, chance, religion, government, communication

**Elizabethan England** (AQA 8145/2B/C — Paper 2 Section B):
- Mix of Q02 "Explain what was important about..." (8 marks) and Q03 "Write an account of..." (8 marks)
- 6x 8-mark only (Q04 site-based essay skipped — site changes annually)

**America 1920–1973** (AQA 8145/1A/D — Paper 1 Section A):
- 2x Q04 "Describe two..." (4 marks)
- 2x Q05 "In what ways were the lives of... affected by...?" (8 marks)
- 2x Q06 "Which of the following had more impact: bullet A / bullet B?" (12 marks)

Mark schemes follow official AQA structure with Level 4/3/2/1/0 descriptors and indicative content examples at each level.

```javascript
window.practiceQuestions = [
  {
    type: "8 marks \u2014 Write an account",
    pastPaper: "AQA June 2022",  // only on real exam questions
    text: "Write an account of...",
    marks: "All historically relevant...\n\nLevel 4 (7\u20138 marks): Complex analysis..."
  },
  {
    type: "16 marks (+4 SPaG) \u2014 How far do you agree?",
    text: "\u2018Statement.\u2019 How far do you agree?...",
    marks: "All historically relevant...\n\nLevel 4 (13\u201316 marks): Complex explanation...\n\nSPaG: High performance (4 marks):..."
  }
];
```

**Important:** Use unicode escapes in JS strings (`\u2014` em dash, `\u2013` en dash, `\u2019`/`\u2018` smart quotes, `\u2022` bullet). Past paper question text must use exact AQA wording.

### Knowledge Check Format

All 60 lessons have a 5-question Knowledge Check quiz (300 total). Questions are selection-based only — no free-text input. Three question types:

**MCQ (multiple choice):**
```javascript
{ type: "mcq", q: "Question text?", options: ["A", "B", "C", "D"], correct: 2 }
```
- `correct` is a 0-based index into the `options` array
- 4 options displayed in a 2x2 grid
- Distractors should be plausible but clearly wrong for students who read the lesson

**Fill-in-the-blank:**
```javascript
{ type: "fill", q: "Sentence with a _____ in it.", options: ["wrong1", "correct", "wrong2", "wrong3"], correct: 1 }
```
- `correct` is a 0-based index into the `options` array
- Options displayed as shuffled pill buttons below the sentence
- The blank `_____` is highlighted in the sentence

**Match-up:**
```javascript
{ type: "match", q: "Match each X to its Y:", left: ["A", "B", "C", "D"], right: ["1", "2", "3", "4"], order: [0, 1, 2, 3] }
```
- `left` labels are fixed; `right` options appear in shuffled dropdowns
- `order` maps each left index to its correct right index (i.e. left[0] matches right[order[0]])
- Typically 3–4 pairs per match question

**Standard mix per lesson:** 2 MCQ + 2 fill-in-the-blank + 1 match-up = 5 questions.

**Quiz behaviour:**
- Questions presented one at a time in a modal overlay
- Immediate feedback (correct/incorrect) with colour coding after each answer
- Next button focused with 50ms delay (prevents Enter key bleed-through from answer selection)
- Results screen shows score out of 5 with retry option
- Best score saved to localStorage key `studyvault-kc-{data-unit}/{data-lesson}` (e.g. `studyvault-kc-conflict-tension/lesson-02`)
- Score badge displayed on sidebar button after first attempt
- Fill-in-the-blank and match-up options are shuffled each time for variety

```javascript
window.knowledgeCheck = [
  { type: "mcq", q: "Question?", options: ["A", "B", "C", "D"], correct: 2 },
  { type: "fill", q: "Sentence with _____.", options: ["w1", "w2", "w3", "w4"], correct: 1 },
  { type: "match", q: "Match:", left: ["A", "B", "C"], right: ["1", "2", "3"], order: [0, 1, 2] },
  { type: "mcq", q: "Question?", options: ["A", "B", "C", "D"], correct: 0 },
  { type: "fill", q: "Another _____.", options: ["w1", "w2", "w3", "w4"], correct: 3 }
];
```

---

## Exam Technique Section

7 guide pages covering every AQA question type, plus a hub page. Accessible from the homepage banner and via "How do I answer this?" links on every lesson's practice questions.

### Guide pages

| File | Marks | Question Type | Units |
|------|-------|--------------|-------|
| `factor-essay.html` | 16+4 SPaG | "How far do you agree?" / "Has [factor] been the main factor?" | Conflict, Health |
| `write-an-account.html` | 8 | "Write an account of..." | Conflict, Elizabethan |
| `explain-significance.html` | 8 | "Explain the significance..." / "Explain what was important..." | Health, Elizabethan |
| `which-had-more-impact.html` | 12 | "Which had more impact?" | America |
| `in-what-ways.html` | 8 | "In what ways were lives affected?" | America |
| `explain-similarities.html` | 8 | "Explain two ways... similar" | Health |
| `describe-two.html` | 4 | "Describe two..." | America |

### Each guide contains
1. **What the Examiner Wants** — plain English + simplified level descriptors
2. **Step-by-Step Formula** — numbered steps (`.guide-steps` / `.guide-step` / `.guide-step-number`)
3. **Timing** — minutes breakdown with visual bar (`.guide-timing-bar`)
4. **Paragraph Templates** — sentence starters (`.guide-template` / `.guide-template-label` / `.guide-starter`)
5. **Annotated Model Answer** — with examiner callouts (`.guide-model-question` / `.guide-model-paragraph` / `.guide-annotation` / `.guide-model-mark`)
6. **Common Mistakes** — what to avoid (`.guide-mistakes` / `.guide-mistake` / `.guide-mistake-icon`)

### JS integration
`getGuideUrl(type)` in `initPracticeQuestions()` maps practice question `type` strings to guide filenames via substring matching. The link is inserted dynamically after the question type badge (and past-paper tag if present) as a `<a class="practice-guide-link" target="_blank">`. No lesson HTML files are modified.

Type string → guide mapping:
- `'Describe two'` → `describe-two.html`
- `'Write an account'` → `write-an-account.html`
- `'Explain the significance'` → `explain-significance.html`
- `'Explain what was important'` → `explain-significance.html`
- `'Explain two similarities'` → `explain-similarities.html`
- `'In what ways'` → `in-what-ways.html`
- `'Which had more impact'` → `which-had-more-impact.html`
- `'How far do you agree'` → `factor-essay.html`
- `'Has '` (with trailing space) → `factor-essay.html` (catches all Health factor variants)

### Theme
Purple: accent `#7c3aed`, light `#f5f3ff`, badge `#ede9fe`. Body class: `unit-exam-technique`. Dark mode variants included.

---

## TTS Narration Generation

**Current state:** All narration audio has been removed. WAV files, JSON manifests, and HTML references (`<source src="">`, `window.narrationManifest`) are all cleared. The narration player UI remains in all 60 lesson pages, ready for new audio. The 184 previously-missing `data-narration-id` attributes on `<ul>`/`<ol>` elements have been fixed.

**Plan:** Regenerate with ElevenLabs cloned voice (`generate_tts.py`) one unit per month (~$22/month on Creator plan, ~355k credits total).

### ElevenLabs process (generate_tts.py)
1. Extract narrable text from the HTML (every element with `data-narration-id`)
2. Skip visual-only elements (`.key-fact-label`, `.exam-tip-label`)
3. Normalise text for speech (strip quotes, convert parentheses to commas, `&` → "and", `vs.` → "versus", rate slashes → "per", etc.)
4. Generate TTS for each chunk individually via ElevenLabs API
5. Concatenate all chunks into a single WAV with 0.4s silence padding between chunks
6. Record start/end timestamps for each chunk → output JSON manifest
7. Inline the manifest as `window.narrationManifest` in the HTML (fetch() doesn't work on file://)
8. Auto-fill `<source src="">` with the correct WAV filename

### Key details
- Output is raw PCM 24000Hz 16-bit signed little-endian mono
- Must write WAV header manually (44 bytes)
- Each chunk's duration = len(pcm_bytes) / (24000 * 2)
- Add 0.4s silence (padding) between chunks
- Manifest JSON: `[{ "id": "n1", "start": 0.0, "end": 1.57 }, ...]`
- Previous run used ~211k credits across all 60 lessons; next run will be higher due to the 184 newly-tagged bullet lists

---

## Image Generation

### Design principles for in-lesson diagrams
These images sit between sections of lesson text. Their job is to provide **visual relief** and make key concepts memorable at a glance.

- **Break up text, don't add more** — the image should be primarily visual (portraits, colour, layout). Labels should be 3–5 words max per element. If it's just text with icons, it's not doing its job.
- **Don't double up** — if a diagram covers the same content as a nearby key-fact box or bullet list, remove the text element. Never show the same information twice.
- **One clear concept per image** — don't combine two metaphors (e.g. pendulum + flowchart). Pick one visual idea and commit to it.
- **Let visuals do the heavy lifting** — use colour intensity, size, and spatial position to convey meaning (e.g. colour-coded borders showing Catholic vs Protestant). The student should grasp the point before reading any labels.
- **Clean and professional** — textbook infographic style. White background, not cluttered. Landscape/wide format works best in the lesson layout.
- **Use the unit accent colour** — amber (#b45309) for Elizabethan, teal (#0d9488) for Health, terracotta (#c44536) for Conflict, blue (#2563eb) for America.

### Prompt pattern for diagrams
```
Create a clear educational diagram showing [SUBJECT].
Use a warm color palette with [UNIT ACCENT COLOR] as the primary color.
Keep text MINIMAL — short labels only, let the visuals communicate the concept.
Clean white background, landscape format, professional textbook quality.
Suitable for GCSE students aged 15-16.
No watermarks.
```

### API call
```python
import urllib.request, json, base64
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": "prompt here"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}
req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=120)
data = json.loads(resp.read())
for part in data["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        img_bytes = base64.b64decode(part["inlineData"]["data"])
        with open("output.png", "wb") as f:
            f.write(img_bytes)
```

---

## JS Features (main.js)

All initialised in `DOMContentLoaded`:
- `initScrollProgress()` — thin accent-coloured bar at page top
- `initCollapsibles()` — expand/collapse with smooth animation (also handles sidebar collapsibles for Related Media)
- `initVisitedTracking()` — localStorage `studyvault-visited`, marks lessons visited
- `initMobileNav()` — hamburger menu for mobile
- `initPracticeQuestions()` — random question selection, AI clipboard marking, email to teacher, formatted mark scheme display, past paper badge rendering via `pastPaper` property, "How do I answer this?" guide links via `getGuideUrl()` type-string mapping
- `initNarration()` — play/pause, progress bar, speed toggle (1x/1.25x/1.5x/0.75x), paragraph highlighting, collapsed section shimmer, keyboard shortcuts (Space=play/pause, Left/Right=skip 5s), floating mini-player when main player out of view, auto-scroll suppression when user scrolls away
- `initAccessibility()` — dark mode toggle, dyslexia font toggle (OpenDyslexic), font size A-/A+ (3 steps), Irlen overlay colours (6 options), all persisted in localStorage `studyvault-a11y`
- `initGlossary()` — creates popup tooltips from `data-def` attributes, hover on desktop, tap on mobile, viewport flip detection
- `initKnowledgeCheck()` — sidebar button opens modal quiz overlay, 5 questions per lesson (MCQ, fill-in-the-blank, match-up), best score saved to localStorage `studyvault-kc-{unit}/{lesson}`, score badge on sidebar button
- `initLightbox()` — click-to-expand on hero images and diagrams, overlay with close button
- `initHeroEdit()` — activated via `?hero-edit` URL param, drag hero images to adjust object-position, copy values button
- `initPageTransitions()` — intercepts internal link clicks, fades out page, then navigates; new page fades in via CSS animation

---

## Design Rules
- Background: warm cream `#faf8f5`, not bright white
- Text: warm dark brown `#2d2a26`, not pure black
- Font: Inter (body) + Source Serif 4 (headings) via Google Fonts
- Cards: `border-radius: 16px`, soft warm shadows
- All data is inlined in HTML (not fetched) due to file:// CORS restrictions
- No search feature — students navigate via unit contents pages
- Narration highlight colour: gold `#fef9e7` with `#e6b800` border (distinct from key fact boxes)
- Key takeaways: 2-3 central points, not exhaustive bullet lists
- Hero images: `object-fit: cover`, 280px height desktop, 200px mobile, with "click to expand" hover hint
- Page transitions: JS-driven fade-out (200ms) then CSS fade-in (300ms) with subtle vertical shift
- Homepage quote ticker: `width: max-content` on track, `margin-right: 3rem` on items, 120s animation duration

## Sidebar Structure
The lesson sidebar contains up to three sections in this order:
- **Knowledge Check** — single button (brain icon) that opens a modal quiz overlay. Uses `.sidebar-knowledge-check` / `.knowledge-check-btn` / `.knowledge-check-score` classes. Score badge appears after first attempt.
- **Related Media** — collapsible categories: Lesson Podcast (first, always present), then curated Podcasts, Movies, TV Shows, Documentaries, and Study Tools (NotebookLM link, always last). Empty categories are omitted. Uses `.sidebar-collapsible` / `.sidebar-collapsible-toggle` / `.sidebar-collapsible-content` / `.sidebar-media-item` classes.
- **Video** — embedded YouTube player (16:9 responsive iframe via `.sidebar-video` padding-bottom trick). Present on 45 lessons (Conflict, Health, Elizabethan). Not present on America lessons (no videos yet). Only works on HTTPS (GitHub Pages), shows Error 153 on `file://`.

Do NOT add a "Key Facts" section to the sidebar. Key facts appear inline in the main content area only.
The sidebar does NOT scroll independently — it uses `position: sticky; top: 5rem`. Content must fit without requiring its own scrollbar.

### Knowledge Check sidebar HTML pattern
```html
<div class="sidebar-section sidebar-knowledge-check">
  <button class="knowledge-check-btn" id="knowledge-check-btn">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a7 7 0 0 1 7 7c0 2.38-1.19 4.47-3 5.74V17a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2v-2.26C6.19 13.47 5 11.38 5 9a7 7 0 0 1 7-7z"/><line x1="10" y1="22" x2="14" y2="22"/></svg>
    <span class="knowledge-check-label">Knowledge Check</span>
    <span class="knowledge-check-score" id="knowledge-check-score"></span>
  </button>
</div>
```

### Related Media HTML pattern
```html
<div class="sidebar-section sidebar-media">
  <div class="sidebar-section-title">Related Media</div>
  <!-- Lesson Podcast always first -->
  <div class="sidebar-collapsible">
    <button class="sidebar-collapsible-toggle" aria-expanded="false">
      <span>&#127911; Lesson Podcast</span>
      <svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="sidebar-collapsible-content">
      <a href="URL" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">
        <strong>AI-Powered Study Notes</strong>
        <span>Two hosts discuss this lesson&rsquo;s content</span>
      </a>
    </div>
  </div>
  <!-- Then Podcasts, Movies (&#127916;), TV Shows (&#128250;), Documentaries (&#127909;) -->
  <!-- Study Tools always last -->
  <div class="sidebar-collapsible">
    <button class="sidebar-collapsible-toggle" aria-expanded="false">
      <span>&#128218; Study Tools</span>
      <svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="sidebar-collapsible-content">
      <a href="URL" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">
        <strong>Interactive Notebook</strong>
        <span>Chat with an AI tutor about this lesson</span>
      </a>
    </div>
  </div>
</div>
```

### Embedded Video HTML pattern
```html
<div class="sidebar-section">
  <div class="sidebar-section-title">Video</div>
  <div class="sidebar-video">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID" title="Video title" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
</div>
```

### Related Media link conventions
- **Lesson Podcast**: Always first collapsible. Links to NotebookLM-generated podcast for this lesson. Present on all 60 lessons.
- **Podcasts**: Link to specific episode URLs (BBC Sounds, Spotify, Apple Podcasts, Acast) — never generic show pages
- **Movies/TV/Documentaries**: Link to JustWatch UK (`justwatch.com/uk/movie/SLUG` or `justwatch.com/uk/tv-series/SLUG`)
- **Study Tools**: Always last collapsible. Links to NotebookLM interactive notebook for this lesson. Present on all 60 lessons.
- Only include categories that have genuine content for that lesson
- Max ~3 items per category

## Content Editing Conventions

When editing lesson content (cross-referencing, readability, additions):

**Scope:** Only edit within `<article class="study-notes">`, `<div class="exam-tip">`, and `<div class="conclusion">`. Never touch header, sidebar, nav, scripts, or structural markup.

**Preserve:**
- All `data-narration-id` attributes (used for TTS paragraph highlighting)
- All `<dfn class="term" data-def="...">` glossary terms — keep definitions as single concise sentences (no context that duplicates surrounding text)
- HTML structure: collapsibles, timelines, key-fact boxes, diagrams
- HTML entities: `&mdash;` `&ndash;` `&rsquo;` `&lsquo;` `&ldquo;` `&rdquo;` `&amp;`

**Readability targets (GCSE age 15-16):**
- Short sentences, active voice, minimal filler
- Cut phrases like "it is important to note that", "this meant that", "as a result of this"
- Prefer concrete over abstract
- Key takeaways: 2-3 tight bullets, not exhaustive lists

**Cross-referencing against teacher PPTs:**
- Read PPTs with `python -m markitdown "filepath"` (only .pptx, not old .ppt)
- Only add exam-relevant content: specific facts, dates, names, statistics, anecdotes
- Don't add everything from the PPT — use editorial judgment on what matters for the exam
- Weave additions naturally into existing sections rather than bolting on new paragraphs
- Add new `<dfn>` glossary terms where appropriate

**PPT folder mapping:**
- Health PPTs → `Spec and Materials/Lessons/Health/`
- America PPTs → `Spec and Materials/Lessons/America/`
- Conflict PPTs → `Spec and Materials/Lessons/Conflict/`
- Elizabethan PPTs → `Spec and Materials/Lessons/Elizabeth/` (note: "Elizabeth" not "Elizabethan")

## Infographic Diagrams

All 60 lessons have at least one infographic diagram generated via Gemini API (`gemini-3-pro-image-preview`). Each diagram replaces a text element (key fact box, collapsible, or bullet list) to avoid duplication. Diagrams use the unit accent colour.

**Design principles:** Infographics NOT illustrations. One concept per image. Let visuals do the work. Replace the text element the diagram covers. Keep text minimal and bold. Clean white background.

**Diagram counts:** Elizabethan 20, Health 21, Conflict 15 (6 pre-existing + 9 new), America 15. Total: ~71 diagram PNGs.

### Elizabethan (amber #b45309)
| Lesson | Filename | Concept |
|--------|----------|---------|
| L01 | `diagram_1558_problems.png` | Four problems Elizabeth faced in 1558 |
| L02 | `diagram_three_churches.png` | Catholic vs Church of England vs Puritan |
| L03 | `diagram_tudor_religion.png` | Tudor religious changes Henry VIII → Elizabeth |
| L04 | `diagram_elizabeth_dilemma.png` | Marriage dilemma — pros/cons |
| L05 | `diagram_suitors.png` | Key suitors comparison |
| L06 | `diagram_archbishops.png` | Parker vs Grindal vs Whitgift |
| L07 | `diagram_prophesying.png` | Puritan challenge escalation |
| L08 | `diagram_plots_escalation.png` | Catholic plots escalating 1569–1586 |
| L09 | `diagram_northern_rebellion.png` | Northern Rebellion chain of events |
| L10 | `diagram_babington_plot.png` | Babington Plot trap |
| L11 | `diagram_threats_comparison.png` | Mary vs Puritans vs Spain threat comparison |
| L12 | `diagram_spain_causes.png` | Causes of war with Spain |
| L13 | `diagram_armada_ships.png` | English vs Spanish fleet comparison |
| L14 | `diagram_great_chain.png` | Great Chain of Being / social hierarchy |
| L14 | `diagram_golden_age.png` | Elizabethan Golden Age culture |
| L15 | `diagram_categories_poor.png` | Categories of the poor |
| + | `diagram_bess_hardwick.png` | Hardwick Hall architecture |
| + | `diagram_drake_voyage.png` | Drake's circumnavigation route |
| + | `diagram_essex_arc.png` | Earl of Essex rise and fall |
| + | `diagram_privateers.png` | Privateering and exploration |

### Conflict & Tension (terracotta #c44536)
| Lesson | Filename | Concept |
|--------|----------|---------|
| L01 | `diagram_peacemakers.png` (pre-existing) | Big Three at Versailles |
| L02 | `diagram_treaty_terms.png` (pre-existing) | Treaty of Versailles terms |
| L03 | `diagram_ubrat.png` | U BRAT mnemonic for German losses |
| L04 | `diagram_league_structure.png` (pre-existing) | League of Nations structure |
| L05 | `diagram_disputes_map.png` (pre-existing) | 1920s border disputes |
| L06 | `diagram_league_scorecard.png` | League successes vs failures |
| L07 | `diagram_1920s_agreements.png` | Locarno/Dawes/Kellogg-Briand comparison |
| L08 | `diagram_manchuria_failures.png` | 5 reasons League failed over Manchuria |
| L09 | `diagram_abyssinia_dominoes.png` | Cascade of Abyssinia consequences |
| L10 | `diagram_hitler_aims.png` | Hitler's four foreign policy aims |
| L11 | `diagram_rhineland.png` (pre-existing) | Rhineland remilitarisation |
| L12 | `diagram_sudetenland.png` (pre-existing) | Sudetenland crisis map |
| L13 | `diagram_stalin_dilemma.png` | Nazi-Soviet Pact — two options |
| L14 | `diagram_poland_pincer.png` | Invasion of Poland pincer movement |
| L15 | `diagram_war_responsibility.png` | Four causes of WWII pyramid |

### Health & the People (teal #0d9488)
| Lesson | Filename | Concept |
|--------|----------|---------|
| L01 | `diagram_four_humours.png` | Four humours wheel |
| L02 | `diagram_church_help_hinder.png` | Church helped vs hindered medicine |
| L03 | `diagram_urine_chart.png` | Medieval urine diagnosis chart |
| L03 | `diagram_three_problems_surgery.png` | Pain, infection, bleeding triangle |
| L04 | `diagram_black_death_causes.png` | Four believed causes of plague |
| L05 | `diagram_vesalius_anatomy.png` | Galen vs Vesalius comparison |
| L06 | `diagram_continuity_change.png` | Old beliefs vs new science |
| L07 | `diagram_inoculation_vs_vaccination.png` | Inoculation vs vaccination |
| L08 | `diagram_swan_neck_flask.png` | Pasteur's germ theory experiment |
| L09 | `diagram_black_period_surgery.png` | Black Period death rate paradox |
| L09 | `diagram_mobile_xray_unit.png` | WWI medical innovations (4 panels) |
| L10 | `diagram_industrial_city_conditions.png` | Industrial city cross-section |
| L10 | `diagram_john_snow_cholera_map.png` | Cholera deaths around Broad St pump |
| L10 | `diagram_bazalgette_sewers.png` | London sewer system cross-section |
| L11 | `diagram_magic_bullets_timeline.png` | Salvarsan → Prontosil → Penicillin |
| L12 | `diagram_rowntree_poverty_cycle.png` | Poverty cycle line graph |
| L12 | `diagram_beveridge_five_giants.png` | Five Giants of the welfare state |
| L13 | `diagram_nhs_three_principles.png` | Universal, comprehensive, free |
| L14 | `diagram_nightingale_scutari.png` | Scutari before/after (42% → 2%) |
| L14 | `diagram_modern_surgery_tech.png` | Open vs keyhole vs robotic surgery |
| L15 | `diagram_lifestyle_diseases.png` | Lifestyle factors → diseases |

### America (blue #2563eb)
| Lesson | Filename | Concept |
|--------|----------|---------|
| L01 | `diagram_cycle_of_prosperity.png` | Reinforcing cycle of 1920s boom |
| L02 | `diagram_women_before_after.png` | Women before vs after 1920 |
| L03 | `diagram_prohibition_failure.png` | Six reasons Prohibition failed |
| L04 | `diagram_immigration_quotas.png` | Declining immigration quotas |
| L05 | `diagram_wall_street_crash.png` | Wall Street Crash statistics |
| L06 | `diagram_depression_statistics.png` | Great Depression key numbers |
| L07 | `diagram_new_deal_three_rs.png` | Relief, Recovery, Reform framework |
| L08 | `diagram_wwii_economic_transformation.png` | Economy before/after WWII |
| L09 | `diagram_postwar_boom.png` | Post-war boom indicators |
| L10 | `diagram_cold_war_escalation.png` | Cold War fears timeline 1945–1953 |
| L11 | `diagram_jim_crow_segregation.png` | Five areas of Jim Crow segregation |
| L12 | `diagram_civil_rights_legislation.png` | CRA 1964 vs VRA 1965 |
| L13 | `diagram_poverty_reduction.png` | Great Society poverty reduction |
| L14 | `diagram_womens_inequality_1960s.png` | Gender inequality statistics |
| L15 | `diagram_america_progress_1920_1973.png` | Continuing inequality by 1973 |

## Conflict & Tension Hero Images
Note: Conflict & Tension hero images use older naming (e.g. `Versailles_1919.jpg`, `lesson 2 hero.jpg` with spaces). The other three units use the standardised `lesson-NN-hero.jpg` format.

## YouTube Videos

YouTube channel: `@UnityCollegeHistory`. Three playlists mapped 1:1 to lessons. America has no videos yet.

### Elizabethan playlist
| Lesson | Video ID | Title |
|--------|----------|-------|
| L01 | `jBlT4iaZiBM` | Elizabeth I: The Survivor Princess |
| L02 | `q5u6PkvY1KI` | Elizabeth's Religious Gamble: The Middle Way |
| L03 | `TY4lAmYwieg` | How Queen Elizabeth I Built Her Government |
| L04 | `TXySXMDhaKQ` | The Virgin Queen: Elizabeth I's Great Marriage Gamble |
| L05 | `hgZwdWBo4iU` | Elizabeth's Shadow War: The Catholic Threat |
| L06 | `hgZwdWBo4iU` | Elizabeth's Shadow War: The Catholic Threat (shared with L05) |
| L07 | `187ln1rpyJs` | Elizabeth and the Puritan Threat |
| L08 | `Wl6cXxEHBW8` | Beyond Religion: The True Causes of the Spanish Armada |
| L09 | `Kx-9dp47VwY` | The Spanish Armada: England's Greatest Test |
| L10 | `S8H5N-IeKZ4` | The Poor in Elizabethan England: A Queendom in Crisis |
| L11 | `6uvqxXlc2F8` | Elizabeth's Sea Dogs: How England Challenged an Empire |
| L12 | `1oRTq9OUSdY` | Elizabethan Ladder: Society, Status, Survival |
| L13 | `6Qj3RLLE3MM` | The Essex Rebellion: A Traitor's End |
| L14 | `pCpr-Zm8sdo` | Elizabeth I: Surviving the Storm |
| L15 | `CrNoLc0mbJU` | The Elizabethan Era: A Golden Age? |

### Health playlist (HEA01–HEA15, 1:1 match)
Video IDs: `igCU6PvpDZY`, `NVicBNFMa_Q`, `0nCsFBNNWw8`, `tk950Wvz6m4`, `i-MOSPzhQNs`, `AViNthWtn3I`, `TSIrB6jKRFI`, `dAAXmF5_SeM`, `3u01-dgpcXM`, `NbVrrLBuZ_A`, `GSGIu9oabgw`, `X1i7JZc6oCg`, `OZD1OrTW3FM`, `Mu4eArqX4k8`, `73iq6z1YlEQ`

### Conflict playlist (CON01–CON15, 1:1 match)
Video IDs: `HaRlcssG83c`, `fIqCkdDb4bM`, `x6t_2KzsmZM`, `hYmRq_MWoGg`, `CLyAvsE-NkU`, `JY3bWdvU5q0`, `PFIz_yAuod0`, `ItX4Hjbtu6Q`, `N4AM_Am5Afs`, `bIXpmmIsTIM`, `iuC4QeJ8wpI`, `6lFVLu4_gfE`, `1BrBqoqbh7M`, `JwLL3Yr-lxI`, `IKXH7rpym0o`
