# Exam Technique Guide Page — HTML Template

> **API Integration:** This template is injected into guide generation prompts. Agents fill in the `{{PLACEHOLDER}}` fields with subject-specific content. Do NOT change the HTML structure, class names, or element order.

---

## Hub Page Template

The hub page lists all exam technique guide pages for the subject. Purple accent is FIXED for all subjects.

```html
<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Exam Technique</h1>
<p>{{INTRO_TEXT — e.g. "The AQA History exam tests source analysis, explanation and essay writing. These guides break down each question type so you know exactly how to pick up maximum marks."}}</p>
</div>
</div>
<div class="guide-hub">
<div class="guide-paper" style="--paper-accent: #7c3aed; --paper-light: #f5f3ff;">
<div class="guide-paper-header">
<h2>{{SECTION_TITLE — e.g. "Paper 1 Questions" or "Question Types"}}</h2>
<span class="guide-paper-ref">{{SECTION_SUBTITLE — e.g. "All question types from the exam"}}</span>
</div>
<div class="guide-paper-questions">
<!-- REPEAT for each guide page: -->
<a class="guide-question-card" href="/guide/{{SUBJECT_SLUG}}/exam-technique/{{SLUG}}">
<span class="guide-question-marks">{{MARKS — e.g. "4 marks"}}</span>
<h3>{{QUESTION_TYPE_NAME — e.g. "Describe Two"}}</h3>
<p>{{SHORT_DESCRIPTION — one sentence explaining this question type}}</p>
</a>
<!-- END REPEAT -->
</div>
</div>
<!-- Add more guide-paper sections if questions are grouped by paper -->
</div>
```

**Rules:**
- Use `--paper-accent: #7c3aed; --paper-light: #f5f3ff;` for ALL sections (purple, fixed)
- All links MUST be absolute: `/guide/{subject-slug}/exam-technique/{slug}`
- Each card needs `guide-question-marks` (marks badge), `<h3>` (title), `<p>` (description)
- Use `guide-paper-questions` (NOT `guide-question-grid`)

---

## Individual Guide Page Template

Each individual exam technique guide page follows this exact structure.

```html
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">{{MARKS — e.g. "4 marks"}}</span>
<h1>{{QUESTION_TYPE_NAME — e.g. "Describe Two"}}</h1>
<p class="guide-used-in">{{USED_IN — e.g. "Used in: America, 1920–1973" or "All content areas"}}</p>
</div>

<!-- Section 1: What the Examiner Wants -->
<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>{{EXAMINER_EXPLANATION — what this question tests, what AOs it targets}}</p>
<h3>Level Descriptors (Simplified)</h3>
<table class="guide-levels">
<thead><tr><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<!-- REPEAT for each mark level, highest to lowest: -->
<tr><td><strong>{{MARKS}}</strong></td><td>{{DESCRIPTOR}}</td></tr>
<!-- END REPEAT -->
</tbody>
</table>
</div>

<!-- Section 2: Step-by-Step Formula -->
<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<!-- REPEAT for each step: -->
<li class="guide-step">
<span class="guide-step-number">{{N}}</span>
<div class="guide-step-body">
<strong>{{STEP_TITLE}}</strong> — {{STEP_DETAIL}}
</div>
</li>
<!-- END REPEAT -->
</ol>
</div>

<!-- Section 3: Timing -->
<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<!-- Segments must add up to 100% width. Use #7c3aed shades. -->
<span style="background: #7c3aed; width: {{PCT}}%;">{{LABEL}}<br/>{{TIME}}</span>
<span style="background: #8b5cf6; width: {{PCT}}%;">{{LABEL}}<br/>{{TIME}}</span>
<span style="background: #a78bfa; width: {{PCT}}%;">{{LABEL}}<br/>{{TIME}}</span>
</div>
<p>{{TIMING_ADVICE}}</p>
</div>

<!-- Section 4: Paragraph Templates (COLLAPSIBLE) -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Paragraph Templates</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
</button>
<div class="collapsible-content"><div class="collapsible-inner">
<!-- REPEAT for each paragraph template: -->
<div class="guide-template">
<div class="guide-template-label">{{LABEL — e.g. "Point 1"}}</div>
<p class="guide-starter">"{{SENTENCE_STARTER}}"</p>
<p class="guide-starter">"{{FOLLOW_UP_STARTER}}"</p>
</div>
<!-- END REPEAT -->
</div></div>
</div>

<!-- Section 5: Annotated Model Answer (COLLAPSIBLE) -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Answer</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
</button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-model-question">
<p>{{EXAMPLE_QUESTION}}</p>
</div>
<!-- REPEAT for each annotated paragraph: -->
<div class="guide-model-paragraph">
<span class="guide-annotation">{{ANNOTATION — e.g. "Point 1 + Detail"}}</span>
<p>{{MODEL_ANSWER_PARAGRAPH}}</p>
</div>
<!-- END REPEAT -->
</div></div>
</div>

<!-- Section 6: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<!-- REPEAT: -->
<li><strong>{{MISTAKE}}</strong> — {{WHY_ITS_A_PROBLEM}}</li>
<!-- END REPEAT -->
</ul>
</div>
</main>

<aside class="lesson-sidebar">
<!-- Quick Reference -->
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<!-- Coloured bar segments matching timing section -->
<span style="background: #7c3aed; width: {{PCT}}%; border-radius: 4px 0 0 4px;" title="{{LABEL}}: {{TIME}}"></span>
<span style="background: #8b5cf6; width: {{PCT}}%;" title="{{LABEL}}: {{TIME}}"></span>
<span style="background: #a78bfa; width: {{PCT}}%; border-radius: 0 4px 4px 0;" title="{{LABEL}}: {{TIME}}"></span>
</div>
<span class="guide-quick-ref-total">{{TOTAL_TIME}} total</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<!-- REPEAT for each step (short versions): -->
<li>{{SHORT_STEP}}</li>
<!-- END REPEAT -->
</ol>
</div>

<!-- Video placeholder -->
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>

<!-- Other Guides -->
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false">
<span>&#128221; Other Guides</span>
<svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
</button>
<div class="sidebar-collapsible-content">
<!-- REPEAT for each OTHER guide page (exclude the current one): -->
<a href="/guide/{{SUBJECT_SLUG}}/exam-technique/{{SLUG}}" class="sidebar-media-item">
<strong>{{QUESTION_TYPE_NAME}}</strong>
<span>{{MARKS}}</span>
</a>
<!-- END REPEAT -->
</div>
</div>
</div>
</aside>
```

**Rules:**
- Do NOT change class names, element order, or nesting structure
- Fill in ONLY the `{{PLACEHOLDER}}` values
- Timing bar segments must add to 100%
- Purple colour shades: `#7c3aed`, `#8b5cf6`, `#a78bfa`
- "Other Guides" sidebar MUST list all other guide pages for this subject (not including itself)
- All links must be absolute paths: `/guide/{subject-slug}/exam-technique/{slug}`
