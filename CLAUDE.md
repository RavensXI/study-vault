# StudyVault — Project Reference

Multi-subject GCSE revision site rebuilt from WordPress to static HTML. Opens directly in browser via `file://` protocol — no server, no build tools. Hosted on GitHub Pages via https://github.com/RavensXI/study-vault.

## Owner
Teacher: Tom Shaun, email: `t.shaun@unity.lancs.sch.uk`
Git config: user "Tom Shaun", email "tomshaun90@gmail.com"

## Current Status

### Branches
- **`main`** — live student-facing site. History content at root level. Single-subject, no login.
- **`platform`** (current) — multi-subject platform. History content under `history/` subfolder. Login system, subject picker, dashboard. Will eventually replace `main`.
- When merging `main` into `platform`, be aware of the path difference (root vs `history/`).

### What's done

**History (complete — 60 lessons across 4 units):**
- All lessons cross-referenced against teacher PPTs, readability-passed for GCSE students
- Hero images (Wikimedia Commons), infographic diagrams (Gemini API, ~71 total), practice questions (6/lesson, 360 total with AQA past paper tags), knowledge checks (5/lesson, 300 total)
- TTS narration: Conflict & Tension lessons 01–14 fully narrated, lesson 15 partial (1 clip). Qwen3-TTS generated locally on AMD RX 6800 using ICL mode with 30s reference clip. Other 3 units (45 lessons) not started. Player UI in place on all 60 lessons. See TTS Narration section.
- Accessibility toolbar (dark mode, dyslexia font, font sizing, Irlen overlays)
- Glossary tooltips, collapsible sections, timelines, key fact boxes, lightbox
- Embedded YouTube videos in sidebar (45 lessons — Conflict, Health, Elizabethan)
- Related Media sidebar (Lesson Podcast, curated Podcasts/Movies/TV/Docs, Study Tools)
- Exam Technique section (7 guide pages for every AQA question type + hub)
- Revision Techniques section (7 guide pages + hub, green theme)
- Page transitions, scroll progress bar, floating narration mini-player

**Platform features:**
- Root `index.html` — single-page app with login, subject picker, and dashboard views
- 3 demo accounts (emma/jake/guest, all password "revision" except guest/"guest")
- Subject picker: 25 GCSE subjects in 6 groups. History and Business are `active: true` with URLs; others show "Coming Soon"
- Dashboard: greeting + exam countdown, today's revision cards, progress stats, subject grid
- All state in localStorage — no backend

**Business Studies (Edexcel 1BS0) — partially built:**
- Landing page + Theme 1 and Theme 2 index pages (15 lesson cards each)
- One lesson built: Theme 1 Lesson 1 "Enterprise & New Business Ideas"
- `generate_diagram.py` helper script for Gemini API diagram generation

### Still TODO
- **Business Studies**: 29 more lessons (Theme 1 L02–L15, Theme 2 L01–L15)
- TTS narration — generate remaining ~46 lessons (finish Conflict 15, then Health, Elizabethan, America). Current Qwen3-TTS approach works but is slow. See TTS Narration section.
- PWA (service worker + manifest.json)
- Delete old v1 flat HTML files (conflict-tension.html, health-people.html, elizabethan.html, america.html)

### Future features (not started)
- Retrieval Practice — cross-lesson spaced repetition quiz (requires backend)
- Real auth backend (likely Supabase) for cross-device sync + teacher analytics
- Content for subjects beyond History and Business

---

## File Structure
```
Study Vault/
├── CLAUDE.md
├── index.html                ← Subject selection / login / dashboard (SPA)
├── css/style.css             ← All styling
├── js/main.js                ← All JS
├── images/                   ← padlock.svg, subject-{id}.jpg
├── fonts/opendyslexic-*/     ← OpenDyslexic woff2/woff
├── history/
│   ├── index.html            ← History landing page (4 unit cards)
│   ├── conflict-tension/     ← 15 lessons + hero images + diagrams
│   ├── health-people/        ← 15 lessons + hero images + diagrams
│   ├── elizabethan/          ← 15 lessons + hero images + diagrams
│   ├── america/              ← 15 lessons + hero images + diagrams
│   ├── exam-technique/       ← Hub + 7 guide pages (purple theme)
│   └── revision-technique/   ← Hub + 7 guide pages (green theme)
├── business/
│   ├── index.html            ← Business landing page (2 theme cards)
│   ├── theme-1/              ← 15 lesson cards, 1 lesson built
│   ├── theme-2/              ← 15 lesson cards, no lessons yet
│   ├── exam-technique/       ← placeholder
│   └── revision-technique/   ← placeholder
└── Spec and Materials/       ← Teacher PPTs (untracked)
    └── Lessons/{Health,America,Conflict,Elizabeth}/
```

### Path conventions
- Root `index.html` → `css/style.css`, `js/main.js`
- Subject landing pages (e.g. `history/index.html`) → `../css/style.css`, `../js/main.js`
- Lesson/unit pages (e.g. `history/conflict-tension/lesson-01.html`) → `../../css/style.css`, `../../js/main.js`

---

## API Details

API keys are stored in environment variables — never commit them.

### Gemini API (diagrams)
- **Env var**: `GEMINI_API_KEY`
- **Model**: `gemini-3-pro-image-preview`
- **Cost**: ~$0.134 per image
- See `generate_diagram.py` for usage

### TTS Status: Qwen3-TTS working locally but slow
Qwen3-TTS runs on local AMD RX 6800 and has generated narration for Conflict & Tension lessons 01–10. Quality is acceptable but generation is slow. Looking for a faster model/approach to complete the remaining ~50 lessons.

### ElevenLabs TTS (paid fallback — best quality but expensive)
- **Env var**: `ELEVENLABS_API_KEY`
- **Voice ID**: `Nd6wm0mR1AWfjae7WcRB` (cloned voice)
- **Model**: `eleven_turbo_v2_5` (0.5 credits/char)
- **Script**: `generate_tts.py`
- **Quality**: Good voice cloning, but too expensive at scale (25 subjects, ~1000+ lessons)
- **Estimated cost**: ~$20-30 for 60 History lessons; hundreds for full site

---

## Unit Colour Themes

| Unit | Body class | Accent |
|------|-----------|--------|
| Conflict & Tension | `unit-conflict` | `#c44536` (terracotta) |
| Health & People | `unit-health` | `#0d9488` (teal) |
| Elizabethan | `unit-elizabethan` | `#b45309` (amber) |
| America | `unit-america` | `#2563eb` (blue) |
| Exam Technique | `unit-exam-technique` | `#7c3aed` (purple) |
| Revision Techniques | `unit-revision-technique` | `#16a34a` (green) |
| Business Theme 1 | `unit-business-1` | `#0891b2` (cyan) |
| Business Theme 2 | `unit-business-2` | `#059669` (emerald) |

---

## Lesson Page Template

Copy `history/conflict-tension/lesson-01.html` as the canonical template. Key structure:

```html
<body class="unit-UNITCLASS" data-unit="UNIT-SLUG" data-lesson="lesson-NN">
  <div class="scroll-progress"></div>
  <header class="page-header"><!-- Brand + nav --></header>
  <div class="lesson-page">
    <main class="lesson-content">
      <!-- lesson-header, hero image, a11y toolbar, narration player -->
      <article class="study-notes">
        <!-- Content with data-narration-id="n1", n2, etc. on every element -->
      </article>
      <div class="exam-tip" data-narration-id="nXX">...</div>
      <div class="conclusion" data-narration-id="nXX">...</div>
      <section class="practice-section" id="practice">...</section>
      <nav class="lesson-nav">...</nav>
    </main>
    <aside class="lesson-sidebar">
      <!-- Knowledge Check, Related Media, Video -->
    </aside>
  </div>
  <script src="../../js/main.js"></script>
  <script>
    window.narrationManifest = [];
    window.practiceQuestions = [ /* 6 questions */ ];
    window.knowledgeCheck = [ /* 5 questions */ ];
  </script>
</body>
```

### Content Components

```html
<!-- Key Fact -->
<div class="key-fact" data-narration-id="nX">
  <div class="key-fact-label">Key Fact</div>
  <p>Content...</p>
</div>

<!-- Collapsible -->
<div class="collapsible">
  <button class="collapsible-toggle" aria-expanded="false">
    <span>Title</span>
    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </button>
  <div class="collapsible-content"><div class="collapsible-inner">
    <p data-narration-id="nX">Content...</p>
  </div></div>
</div>

<!-- Timeline -->
<div class="timeline" data-narration-id="nX">
  <div class="timeline-event">
    <div class="timeline-date">DATE</div>
    <h4>Title</h4><p>Description</p>
  </div>
</div>

<!-- Glossary term (single-sentence definition only) -->
<dfn class="term" data-def="Definition.">term</dfn>

<!-- Diagram -->
<figure class="diagram"><img src="diagram_name.jpg" alt="..."></figure>

<!-- Hero image -->
<figure class="lesson-hero-image">
  <img src="lesson-NN-hero.jpg" alt="..." style="object-position: center XX%;">
  <figcaption>Description</figcaption>
</figure>
```

Hero images: `object-fit: cover`, 280px desktop / 200px mobile. Use `?hero-edit` URL param to adjust position.

---

## Practice Questions

6 per lesson. Real past paper questions tagged with `pastPaper` property (gold badge). Use unicode escapes in JS: `\u2014` (em dash), `\u2013` (en dash), `\u2019`/`\u2018` (smart quotes).

**History (AQA) question types by unit:**
- **Conflict**: 3x "Write an account" (8 marks) + 3x "How far do you agree?" (16+4 SPaG)
- **Health**: Mix of "Explain significance" (8) + "Explain two ways similar" (8) + "Has [factor] been the main factor?" (16+4 SPaG)
- **Elizabethan**: 6x 8-mark only ("Explain what was important" / "Write an account")
- **America**: 2x "Describe two" (4) + 2x "In what ways" (8) + 2x "Which had more impact?" (12)

**Business (Edexcel) question types per lesson:**
- 1x Define (1 mark), 1x Outline (2), 2x Explain (3), 1x Discuss (6), 1x Justify/Evaluate (9 or 12)

### Exam Technique guide mapping
`getGuideUrl(type)` maps practice question type strings to guide files via substring matching:
- `'Describe two'` → `describe-two.html`
- `'Write an account'` → `write-an-account.html`
- `'Explain the significance'` / `'Explain what was important'` → `explain-significance.html`
- `'Explain two similarities'` → `explain-similarities.html`
- `'In what ways'` → `in-what-ways.html`
- `'Which had more impact'` → `which-had-more-impact.html`
- `'How far do you agree'` / `'Has '` → `factor-essay.html`

---

## Knowledge Check

5 per lesson. Three question types — standard mix: 2 MCQ + 2 fill-in-the-blank + 1 match-up.

```javascript
{ type: "mcq", q: "Question?", options: ["A", "B", "C", "D"], correct: 2 }          // 0-based index
{ type: "fill", q: "Sentence with _____.", options: ["w1", "w2", "w3", "w4"], correct: 1 }
{ type: "match", q: "Match:", left: ["A", "B", "C"], right: ["1", "2", "3"], order: [0, 1, 2] }
```

Best score saved to `studyvault-kc-{data-unit}/{data-lesson}` in localStorage.

---

## Sidebar Structure

Three sections in order: **Knowledge Check** (button → modal quiz), **Related Media** (collapsible categories), **Video** (YouTube embed, 45 lessons only).

Related Media order: Lesson Podcast (always first) → Podcasts → Movies → TV Shows → Documentaries → Study Tools (always last). Empty categories omitted. Links: podcast episodes use specific episode URLs; movies/TV use JustWatch UK; max ~3 items per category.

Do NOT add a "Key Facts" section to the sidebar. Sidebar uses `position: sticky; top: 5rem` — no independent scrolling.

See any existing lesson file for full HTML patterns.

---

## Business Studies (Edexcel 1BS0)

Two themes, 15 lessons each, 30 total. Body classes: `unit-business-1` / `unit-business-2`. Data attributes: `data-unit="business-theme-1"` / `"business-theme-2"`.

### Theme 1: Investigating Small Business (spec 1.1–1.5)
1. Enterprise & New Business Ideas (1.1.1+1.1.2) ← **built**
2. The Role of Enterprise & Adding Value (1.1.3+1.1.4)
3. Customer Needs & Market Research (1.2.1+1.2.2)
4. Market Segmentation & Competition (1.2.3+1.2.4)
5. Business Aims & Objectives (1.3.1+1.3.2)
6. Revenue, Costs & Profit (1.3.3)
7. Break-Even Analysis (1.3.4)
8. Cash & Cash-Flow Forecasts (1.3.5)
9. Sources of Business Finance (1.4.1)
10. Business Ownership & Liability (1.4.2+1.4.3)
11. Business Location (1.4.4)
12. The Marketing Mix (1.4.5)
13. Business Plans (1.4.6)
14. Stakeholders & Technology (1.5.1+1.5.2)
15. Legislation, the Economy & External Influences (1.5.3+1.5.4)

### Theme 2: Building a Business (spec 2.1–2.5)
1. Business Growth (2.1.1)
2. Changing Aims & Objectives (2.1.2)
3. Globalisation (2.1.3+2.1.4)
4. Ethics & the Environment (2.1.5)
5. Product Design & the Product Life Cycle (2.2.1)
6. Pricing Strategies (2.2.2)
7. Promotion & Place (2.2.3+2.2.4)
8. Using the Marketing Mix (2.2.5)
9. Business Operations & Production (2.3.1)
10. Working with Suppliers (2.3.2)
11. Quality & Customer Service (2.3.3+2.3.4)
12. Business Calculations (2.4.1+2.4.2)
13. Understanding Business Performance (2.4.3)
14. Organisational Structures & Recruitment (2.5.1+2.5.2)
15. Training, Development & Motivation (2.5.3+2.5.4)

---

## Diagram Generation

**Design principles:** Infographics NOT illustrations. One concept per image. Minimal text (3-5 word labels). Let visuals do the work. Clean white background, landscape format. Use unit accent colour. Each diagram replaces a text element to avoid duplication.

**Prompt pattern:**
```
Create a clear educational diagram showing [SUBJECT].
Use a warm color palette with [UNIT ACCENT COLOR] as the primary color.
Keep text MINIMAL — short labels only, let the visuals communicate the concept.
Clean white background, landscape format, professional textbook quality.
Suitable for GCSE students aged 15-16. No watermarks.
```

Diagram filenames: `diagram_descriptive_name.jpg`. See `generate_diagram.py` for API usage.

---

## JS Features (main.js)

All initialised in `DOMContentLoaded`:
- `initScrollProgress()` — accent-coloured bar at page top
- `initCollapsibles()` — expand/collapse with animation
- `initVisitedTracking()` — localStorage `studyvault-visited`
- `initMobileNav()` — hamburger menu
- `initPracticeQuestions()` — random question selection, mark scheme display, past paper badges, guide links via `getGuideUrl()`
- `initNarration()` — play/pause, speed toggle, paragraph highlighting, mini-player, auto-scroll suppression
- `initAccessibility()` — dark mode, dyslexia font, font size, Irlen overlays (persisted in `studyvault-a11y`)
- `initGlossary()` — popup tooltips from `data-def`, hover/tap
- `initKnowledgeCheck()` — modal quiz overlay, best score in localStorage
- `initLightbox()` — click-to-expand on hero images and diagrams
- `initHeroEdit()` — `?hero-edit` URL param for position adjustment
- `initPageTransitions()` — fade-out/in on internal links
- `initRevisionTips()` — green lightbulb tips on `.key-fact`, `.timeline`, `.collapsible`
- `initNavIcons()` — pen (purple) / lightbulb (green) icons on nav links, pill-styled prev/next
- `initLessonNavBackSlot()` — back-link positioning on first/last lessons

---

## Design Rules
- Background: warm cream `#faf8f5`, not bright white
- Text: warm dark brown `#2d2a26`, not pure black
- Font: Inter (body) + Source Serif 4 (headings) via Google Fonts
- Cards: `border-radius: 16px`, soft warm shadows
- All data inlined in HTML (no fetch — `file://` CORS restrictions)
- Logo: inline SVG padlock replaces period in "StudyVault." — `currentColor`, scales with text
- Narration highlight: gold `#fef9e7` with `#e6b800` border
- Key takeaways: 2-3 bullets, not exhaustive lists

---

## Content Editing Conventions

**Scope:** Only edit within `<article class="study-notes">`, `<div class="exam-tip">`, and `<div class="conclusion">`. Never touch header, sidebar, nav, scripts.

**Preserve:** All `data-narration-id` attributes, all `<dfn class="term" data-def="...">` glossary terms (single-sentence definitions), HTML structure, HTML entities (`&mdash;` `&ndash;` `&rsquo;` etc.).

**Readability (GCSE age 15-16):** Short sentences, active voice, minimal filler, concrete over abstract, 2-3 key takeaways.

**Cross-referencing PPTs:** Read with `python -m markitdown "filepath"` (.pptx only). Add exam-relevant facts/dates/names only. Weave naturally into existing sections.

**PPT folders:** Health → `Spec and Materials/Lessons/Health/`, America → `.../America/`, Conflict → `.../Conflict/`, Elizabethan → `.../Elizabeth/` (note: "Elizabeth" not "Elizabethan")

---

## TTS Narration

### Current status (19 Feb 2026)
Qwen3-TTS (`Qwen3-TTS-12Hz-1.7B-Base`) running locally on AMD RX 6800 (CPU mode, ~6x real-time). Uses ICL voice cloning with a 30-second reference clip for accent preservation.

**Narration progress:**

| Unit | Lessons done | Notes |
|------|-------------|-------|
| Conflict & Tension 01–14 | 14/15 | Fully working — audio files + manifest correct |
| Conflict & Tension 15 | partial | 1 audio clip generated, batch was stopped early |
| Health & People | 0/15 | Not started |
| Elizabethan | 0/15 | Not started |
| America | 0/15 | Not started |

Audio file naming convention: `narration_lesson-NN_nX.wav` (e.g. `narration_lesson-01_n1.wav`). Files live in the unit folder alongside lesson HTML (e.g. `conflict-tension/narration_lesson-01_n1.wav`).

### Models tried

| Model | Result | Notes |
|-------|--------|-------|
| **Qwen3-TTS** (local AMD RX 6800) | **Working — current approach** | Acceptable voice quality. Slow generation but functional. Generated Conflict lessons 01–10 locally. |
| **Qwen3-TTS** (RunPod RTX 4090) | Too slow | ~14x real-time. Stock `qwen-tts` barely uses GPU (3%). Community fork (`dffdeeq/Qwen3-TTS-streaming`) tried with `torch.compile` — spent 30+ min compiling, never finished. |
| **Chatterbox TTS** | Bad voice quality | Fast generation but terrible voice cloning — "someone doing a bad English accent". Zero-shot cloning doesn't work for every voice. |
| **GPT-SoVITS v2Pro** (fine-tuned) | Mediocre + truncation | Trained on 6 min of teacher's voice. Voice somewhat recognisable but not convincing. Consistently truncates output. Chinese-first model. |

**Not yet tried:**
- **F5-TTS** — English-focused, good voice cloning reported, 15x real-time on GPU. Worth testing next.
- **Professional narration** — hire a narrator or use a non-cloned AI voice.

### Voice cloning config
- **Reference audio**: `voicebox-test/voice_sample_30s.wav` (30s crop of teacher reading, 24kHz mono)
- **ICL mode**: `x_vector_only_mode=False` with reference transcript in `REF_TEXT` constant — preserves Lancashire accent
- **Model**: `Qwen/Qwen3-TTS-12Hz-1.7B-Base` via `qwen-tts` package
- 10s clip was too thin (accent lost), 59s was too slow to process on CPU. 30s is the sweet spot.

### Infrastructure
- `generate_narration.py` — batch script wired for Qwen3-TTS. Extracts `data-narration-id` text from HTML, generates per-chunk WAV via ICL voice cloning, updates `window.narrationManifest`. Skips existing audio files. Has UTF-8 encoding fix for Windows.
- `voicebox-test/voice_sample_30s.wav` — 30s reference clip (the one that works)
- `voicebox-test/voice_sample.wav` — full 58.9s reference (too slow for CPU prompt building)
- `voicebox-test/new test clone.m4a` — original 30s voice sample (m4a format)
- `voicebox-test/new test appeasement.m4a` — 6 min voice sample (teacher reading lesson content)
- `runpod/` — setup scripts for RunPod cloud GPU (setup.sh, run_all.sh, pack_for_upload.sh, pack_results.sh)
- `test_gptsovits.py` — standalone GPT-SoVITS inference script

**Generation process:** extract `data-narration-id` elements → normalise text → build voice prompt from 30s reference (ICL mode) → generate per-chunk WAV → update `window.narrationManifest` in HTML.

---

## YouTube Videos

Channel: `@UnityCollegeHistory`. Three playlists mapped 1:1 to lessons (Elizabethan, Health, Conflict — 15 each). America has no videos. Video IDs are already embedded in each lesson's sidebar HTML.

## Conflict & Tension Hero Images
Conflict hero images use older naming (e.g. `Versailles_1919.jpg`, `lesson 2 hero.jpg` with spaces). Other units use `lesson-NN-hero.jpg`.

---

## OpenClaw (Agent Automation)

OpenClaw runs in WSL2 Ubuntu as a systemd user service under the `tshau` account. It provides a Telegram bot and scheduled research agents.

### Setup
- **Config**: `~/.openclaw/openclaw.json` (in Ubuntu/WSL)
- **Gateway**: `ws://127.0.0.1:18789`, systemd service `openclaw-gateway`
- **Model**: `claude-sonnet-4-6` (default for all agents)
- **Auth**: Anthropic API key (`sk-ant-api03-...`) — billed via console.anthropic.com credits
- **WSL persistence**: `.wslconfig` set with `autoMemoryReclaim=false` to keep gateway alive

### Telegram Bot
- **Bot**: `@tom_shaun_bot`
- **Token**: *(store in `~/.openclaw/openclaw.json` — never commit)*
- **User ID**: `8504241823`
- **DM policy**: allowlist (only Tom's account)
- **Binding**: DMs route to `main` agent

### Agents
| Agent | Role |
|-------|------|
| `main` | Default Telegram responder. Handles DMs, weekly digest compilation, file access, general questions. |
| `research-tts` | Daily TTS/voice cloning research (cron, no direct Telegram access). |
| `research-tech` | Daily EdTech/dev tools research (cron, no direct Telegram access). |
| `orchestrator` | Unused — merged into main agent. |
| `file-access` | Unused — merged into main agent. |

Agent instructions: `~/.openclaw/agents/{agent-id}/agent/AGENT.md`

### Cron Jobs
| Job | Schedule | Agent | What it does |
|-----|----------|-------|-------------|
| TTS Research Daily | 8:00am daily (Europe/London) | `research-tts` | Scans for new TTS models, voice cloning breakthroughs, AMD GPU compatibility |
| Tech Research Daily | 8:05am daily (Europe/London) | `research-tech` | Scans for EdTech tools, static site innovations, AI in education |
| Weekly Digest | Monday 9:00am (Europe/London) | `main` | Compiles findings from both research agents into a Telegram summary |

### Common commands (run in Ubuntu)
```bash
openclaw status              # Check gateway + channels
openclaw logs --follow       # Live gateway logs
openclaw cron list           # List scheduled jobs
systemctl --user restart openclaw-gateway   # Restart gateway
nano ~/.openclaw/agents/research-tts/agent/AGENT.md  # Edit agent instructions
```

### Research Log Pipeline
Two research agents run daily and write findings to log files in the Study Vault directory:
- **`tts-research-log.md`** — TTS/voice cloning developments (from `research-tts` agent, 8am daily)
- **`tech-research-log.md`** — EdTech/dev tools developments (from `research-tech` agent, 8:05am daily)

These logs are NOT sent to Telegram. They are written for Claude Code to read during conversations:
- **Narration / TTS discussions** → read `tts-research-log.md` for recent model releases, benchmarks, AMD compatibility
- **Website / platform development** → read `tech-research-log.md` for relevant tools, PWA updates, hosting options, EdTech innovations
- **Any new feature or architectural decision** → check both logs in case something relevant has landed

When any of these topics come up, **read the relevant log file(s) first** before making recommendations.

The **weekly digest** (Monday 9am, `main` agent) reads both logs and sends a short nudge to Tom's Telegram with highlights.

### WSL Keep-Alive
OpenClaw runs in WSL2 Ubuntu. A VBS script in the Windows Startup folder (`shell:startup/keep-wsl-alive.vbs`) runs `wsl -d Ubuntu -- sleep infinity` on login to prevent WSL from shutting down the distro. If cron jobs aren't firing, check that Ubuntu is running: `wsl -l -v`.
