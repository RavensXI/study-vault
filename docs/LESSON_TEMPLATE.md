# Lesson Template — Building Lesson Pages

Reference for building new lesson pages. Copy `history/conflict-tension/lesson-01.html` as the canonical template.

---

## Page Structure

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

---

## Content Components

### Key Fact

```html
<div class="key-fact" data-narration-id="nX">
  <div class="key-fact-label">Key Fact</div>
  <p>Content...</p>
</div>
```

### Collapsible

```html
<div class="collapsible">
  <button class="collapsible-toggle" aria-expanded="false">
    <span>Title</span>
    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </button>
  <div class="collapsible-content"><div class="collapsible-inner">
    <p data-narration-id="nX">Content...</p>
  </div></div>
</div>
```

### Timeline

```html
<div class="timeline" data-narration-id="nX">
  <div class="timeline-event">
    <div class="timeline-date">DATE</div>
    <h4>Title</h4><p>Description</p>
  </div>
</div>
```

### Glossary Term

Single-sentence definitions only.

```html
<dfn class="term" data-def="Definition.">term</dfn>
```

### Diagram

```html
<figure class="diagram"><img src="diagram_name.jpg" alt="..."></figure>
```

Full width, 720px max. Place at content-relevant locations, well away from other images (15+ lines of content between). See `DIAGRAM_PIPELINE.md` for the creation process.

### Hero Image

```html
<figure class="lesson-hero-image">
  <img src="lesson-NN-hero.jpg" alt="..." style="object-position: center XX%;">
  <figcaption>Description</figcaption>
</figure>
```

`object-fit: cover`, 280px desktop / 200px mobile. Use `?hero-edit` URL param to adjust position.

---

## Content Editing Conventions

**Scope:** Only edit within `<article class="study-notes">`, `<div class="exam-tip">`, and `<div class="conclusion">`. Never touch header, sidebar, nav, scripts.

**Preserve:** All `data-narration-id` attributes, all `<dfn class="term" data-def="...">` glossary terms, HTML structure, HTML entities (`&mdash;` `&ndash;` `&rsquo;` etc.).

**Readability (GCSE age 15-16):** Short sentences, active voice, minimal filler, concrete over abstract, 2-3 key takeaways.

**Cross-referencing PPTs:** Read with `python -m markitdown "filepath"` (.pptx only). Add exam-relevant facts/dates/names only. Weave naturally into existing sections.

**PPT folder locations:**
- History Health → `Spec and Materials/Lessons/Health/`
- History America → `Spec and Materials/Lessons/America/`
- History Conflict → `Spec and Materials/Lessons/Conflict/`
- History Elizabethan → `Spec and Materials/Lessons/Elizabeth/` (note: "Elizabeth" not "Elizabethan")
- Sport Science → `Spec and Materials/OCR Sport Science/`

---

## Narration IDs

Every visible content element gets a sequential `data-narration-id` attribute (`n1`, `n2`, `n3`...). These map to WAV files in the narration manifest. Even if narration hasn't been generated yet, the IDs must be present.

---

## Path Conventions

- Root `index.html` → `css/style.css`, `js/main.js`
- Subject landing pages (e.g. `history/index.html`) → `../css/style.css`, `../js/main.js`
- Lesson/unit pages (e.g. `history/conflict-tension/lesson-01.html`) → `../../css/style.css`, `../../js/main.js`
