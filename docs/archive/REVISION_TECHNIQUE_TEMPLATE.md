# Revision Technique Guide Page — HTML Template

> **API Integration:** This template is injected into guide generation prompts. Agents fill in the `{{PLACEHOLDER}}` fields with subject-specific content. Do NOT change the HTML structure, class names, or element order.

---

## Hub Page Template

The hub page lists all revision technique guide pages. Green accent is FIXED for all subjects.

```html
<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>{{INTRO_TEXT — e.g. "Evidence-based strategies that actually work. Each technique is backed by cognitive science research and tailored to GCSE History revision."}}</p>
</div>
</div>
<div class="guide-hub">
<!-- Foundation Techniques -->
<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these throughout your revision</span>
</div>
<div class="guide-paper-questions">
<!-- MUST include retrieval-practice, dual-coding, elaborative-interrogation -->
<a class="guide-question-card" href="/guide/{{SUBJECT_SLUG}}/revision-technique/retrieval-practice">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself, don&rsquo;t just re-read. Brain dumps and self-quizzing beat highlighting every time.</p>
</a>
<a class="guide-question-card" href="/guide/{{SUBJECT_SLUG}}/revision-technique/dual-coding">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>{{SUBJECT_SPECIFIC_DESCRIPTION — e.g. "Combine words and visuals. Timelines, flowcharts, and comparison tables stick better than text alone."}}</p>
</a>
<a class="guide-question-card" href="/guide/{{SUBJECT_SLUG}}/revision-technique/elaborative-interrogation">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; to deepen understanding. Build chains that turn facts into explanations.</p>
</a>
<!-- Additional foundation techniques if needed -->
</div>
</div>
<!-- Subject-Specific Techniques -->
<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>{{SUBJECT_NAME}}-Specific Techniques</h2>
<span class="guide-paper-ref">Techniques tailored to this subject</span>
</div>
<div class="guide-paper-questions">
<!-- REPEAT for each subject-specific technique: -->
<a class="guide-question-card" href="/guide/{{SUBJECT_SLUG}}/revision-technique/{{SLUG}}">
<span class="guide-question-marks">{{BADGE_TEXT}}</span>
<h3>{{TECHNIQUE_NAME}}</h3>
<p>{{DESCRIPTION}}</p>
</a>
<!-- END REPEAT -->
</div>
</div>
<!-- Exam Preparation -->
<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Exam Preparation</h2>
<span class="guide-paper-ref">Final weeks before the exam &mdash; sharpen and apply</span>
</div>
<div class="guide-paper-questions">
<!-- REPEAT for exam prep techniques: -->
<a class="guide-question-card" href="/guide/{{SUBJECT_SLUG}}/revision-technique/{{SLUG}}">
<span class="guide-question-marks">{{BADGE_TEXT}}</span>
<h3>{{TECHNIQUE_NAME}}</h3>
<p>{{DESCRIPTION}}</p>
</a>
<!-- END REPEAT -->
</div>
</div>
</div>
```

**Rules:**
- Use `--paper-accent: #16a34a; --paper-light: #f0fdf4;` for ALL sections (green, fixed)
- MUST have three sections: Foundation, Subject-Specific, Exam Preparation
- Foundation MUST include `retrieval-practice`, `dual-coding`, `elaborative-interrogation` (hardcoded in main.js)
- All links MUST be absolute: `/guide/{subject-slug}/revision-technique/{slug}`
- Use `guide-paper-questions` (NOT `guide-question-grid`)
- Each card needs `guide-question-marks` + `<h3>` + `<p>`

---

## Individual Guide Page Template

Each individual revision technique guide page follows this exact structure.

```html
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">{{BADGE — e.g. "Active recall"}}</span>
<h1>{{TECHNIQUE_NAME}}</h1>
<p class="guide-used-in">{{TAGLINE — e.g. "Test yourself, don't just re-read"}}</p>
</div>

<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>{{RESEARCH_INTRO — 2-3 sentences explaining the cognitive science behind this technique}}</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<!-- REPEAT for 3-4 research studies: -->
<tr>
<td><strong>{{AUTHOR_YEAR}}</strong></td>
<td>{{FINDING}}</td>
<td>{{IMPACT}}</td>
</tr>
<!-- END REPEAT -->
</tbody>
</table>
</div>

<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<!-- REPEAT for each step (typically 4-6): -->
<li class="guide-step">
<span class="guide-step-number">{{N}}</span>
<div class="guide-step-body">
<strong>{{STEP_TITLE}}</strong> — {{STEP_DETAIL — subject-specific instructions}}
</div>
</li>
<!-- END REPEAT -->
</ol>
</div>

<!-- Section 3: Subject-Specific Examples (COLLAPSIBLE) -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>{{SUBJECT_NAME}} Examples</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
</button>
<div class="collapsible-content"><div class="collapsible-inner">
<!-- 2-3 concrete examples of applying this technique to this subject -->
<div class="guide-template">
<div class="guide-template-label">{{EXAMPLE_LABEL — e.g. "Example 1: Recording Equipment"}}</div>
<p>{{EXAMPLE_DETAIL}}</p>
</div>
<!-- More examples... -->
</div></div>
</div>

<!-- Section 4: Common Pitfalls -->
<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<!-- REPEAT: -->
<li><strong>{{PITFALL}}</strong> — {{WHY_AND_HOW_TO_AVOID}}</li>
<!-- END REPEAT -->
</ul>
</div>

<!-- Section 5: Weekly Schedule Suggestion -->
<div class="guide-section">
<h2>When to Use This</h2>
<p>{{SCHEDULING_ADVICE — when in the revision cycle this technique works best, how often, how long per session}}</p>
</div>
</main>

<aside class="lesson-sidebar">
<!-- Quick Reference -->
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<!-- Coloured segments showing time split. Use green shades. -->
<span style="background: #16a34a; width: {{PCT}}%;" title="{{LABEL}}: {{TIME}}"></span>
<span style="background: #22c55e; width: {{PCT}}%;" title="{{LABEL}}: {{TIME}}"></span>
<span style="background: #4ade80; width: {{PCT}}%;" title="{{LABEL}}: {{TIME}}"></span>
</div>
<span class="guide-quick-ref-total">{{TOTAL_TIME}} per cycle</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<!-- REPEAT (short versions of steps): -->
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

<!-- Other Techniques -->
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
</button>
<div class="sidebar-collapsible-content">
<!-- REPEAT for each OTHER technique page (exclude the current one): -->
<a href="/guide/{{SUBJECT_SLUG}}/revision-technique/{{SLUG}}" class="sidebar-media-item">
<strong>{{TECHNIQUE_NAME}}</strong>
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
- Green colour shades for sidebar bar: `#16a34a`, `#22c55e`, `#4ade80`
- "Other Techniques" sidebar MUST list all other revision technique pages (not including itself)
- All links must be absolute: `/guide/{subject-slug}/revision-technique/{slug}`
- The three foundation techniques (retrieval-practice, dual-coding, elaborative-interrogation) follow the same template but with universal research + subject-specific examples
