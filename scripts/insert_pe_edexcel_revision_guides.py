"""
Insert Physical Education (Edexcel 1PE0) revision technique guide pages into Supabase.
Subject slug: physical-education-edexcel
Subject ID: 3782ab12-5dd9-49c3-9811-8b899f465cd8
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://baipckgywpnwapobwtsy.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
PE_SUBJECT_ID = '3782ab12-5dd9-49c3-9811-8b899f465cd8'

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─────────────────────────────────────────────────────────────
# GUIDE PAGES — 1 hub + 7 individual technique pages
# ─────────────────────────────────────────────────────────────

pages = []

# ══════════════════════════════════════════════════════════════
# sort_order = 0 — HUB INDEX
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "index",
    "title": "Revision Techniques",
    "sort_order": 0,
    "status": "live",
    "content_html": """<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>Evidence-based strategies tailored to Edexcel Physical Education (1PE0). PE rewards students who can recall precise terminology &mdash; cardiac output formulae, muscle fibre types, lever classifications &mdash; and apply that knowledge to unfamiliar practical scenarios. Component 1 covers anatomy and physiology, movement analysis, physical training; Component 2 covers sports psychology, socio-cultural influences, health, fitness and well-being. Use the strategies below to build rock-solid recall across both components.</p>
</div>
</div>
<div class="guide-hub">

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these from day one</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself on definitions, formulae, and classifications rather than re-reading. Brain dumps on &ldquo;the 5 bone shapes&rdquo; or &ldquo;3 muscle fibre types&rdquo; reveal exactly what you don&rsquo;t know &mdash; and strengthen what you do.</p>
</a>
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition">
<span class="guide-question-marks">Distributed practice</span>
<h3>Spaced Repetition</h3>
<p>Revisit the same material at 1, 3, 7, 14, 30-day gaps. The cardiac output formula (CO&nbsp;=&nbsp;HR&nbsp;&times;&nbsp;SV) and the FITT principle need spacing to stick. Works better than cramming every time.</p>
</a>
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; to deepen understanding. Why do antagonistic pairs work &mdash; why does the triceps relax when the biceps contracts? How do slow-twitch fibres resist fatigue? Turn memorised facts into understood physiology.</p>
</a>
</div>
</div>

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Consolidation Techniques</h2>
<span class="guide-paper-ref">Use these once you know the basics</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/dual-coding">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>Combine words and visuals. Annotated skeletal diagrams labelled with joint types, lever-class flowcharts with anatomical examples, and the CO&nbsp;=&nbsp;HR&nbsp;&times;&nbsp;SV formula worked out with real numbers stick far better than text alone.</p>
</a>
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/interleaving">
<span class="guide-question-marks">Mixed practice</span>
<h3>Interleaving</h3>
<p>Alternate Component 1 (anatomy, movement, training) with Component 2 (psychology, socio-cultural, well-being) topics in one session. Trains you to identify exactly which area a question is testing &mdash; the discrimination skill the exam tests hardest.</p>
</a>
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers">
<span class="guide-question-marks">Structured notes</span>
<h3>Knowledge Organisers</h3>
<p>One page per body system. Skeletal, muscular, cardiovascular, respiratory &mdash; each gets its own organiser with key vocabulary, formulae, and a mini-diagram. The psychology terms sheet keeps all mental strategies in one place.</p>
</a>
</div>
</div>

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Exam Preparation</h2>
<span class="guide-paper-ref">Final weeks &mdash; sharpen and apply</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/physical-education-edexcel/revision-technique/timed-practice">
<span class="guide-question-marks">Exam conditions</span>
<h3>Timed Practice</h3>
<p>Simulate the real thing. Edexcel PE papers mix short-answer recall with extended 9-mark &lsquo;assess&rsquo; questions &mdash; practising under time pressure builds the judgement to switch between them confidently. Allow 2&ndash;3 min per 2-mark question and 12 min per 9-mark question including planning.</p>
</a>
</div>
</div>

</div>"""
})

# ══════════════════════════════════════════════════════════════
# OTHER TECHNIQUE LINK BLOCKS (sidebar, per page)
# ══════════════════════════════════════════════════════════════

OTHER_LINKS_EXCEPT_RETRIEVAL = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>"""

OTHER_LINKS_EXCEPT_SPACED = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>"""

OTHER_LINKS_EXCEPT_INTERLEAVING = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>"""

OTHER_LINKS_EXCEPT_DUAL = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>"""

OTHER_LINKS_EXCEPT_ELABORATIVE = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>"""

OTHER_LINKS_EXCEPT_KO = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>"""

OTHER_LINKS_EXCEPT_TIMED = """<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="/guide/physical-education-edexcel/revision-technique/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>"""

# ══════════════════════════════════════════════════════════════
# sort_order = 1 — RETRIEVAL PRACTICE
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "retrieval-practice",
    "title": "Retrieval Practice",
    "sort_order": 1,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Active recall</span>
<h1>Retrieval Practice</h1>
<p class="guide-used-in">Test yourself &mdash; don&rsquo;t just re-read.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Retrieval practice is the act of pulling information out of your memory, rather than pushing it in. It sounds simple but it is the most powerful revision technique we have &mdash; stronger than highlighting, stronger than re-reading, stronger than watching videos. The harder the retrieval feels, the more your long-term memory is strengthening.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Roediger &amp; Karpicke (2006)</strong></td><td>Students who self-tested once remembered 50% more a week later than those who re-read four times.</td><td>Self-testing &gt; re-reading, even when it feels harder.</td></tr>
<tr><td><strong>Karpicke &amp; Blunt (2011)</strong></td><td>Retrieval practice beat concept-mapping and elaborative study on a delayed test by ~50%.</td><td>Works better than other &ldquo;active&rdquo; strategies that feel productive.</td></tr>
<tr><td><strong>Agarwal et al. (2017)</strong></td><td>Low-stakes retrieval quizzes raised GCSE-equivalent test scores by an average of one grade.</td><td>Short regular quizzing moves your real exam score.</td></tr>
<tr><td><strong>Smith et al. (2016)</strong></td><td>Students who practised retrieval scored higher even on questions testing information they didn&rsquo;t specifically retrieve.</td><td>Builds the skill of remembering itself, not just the facts.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Study a chunk of content</strong> &mdash; read through a StudyVault lesson, watch a video, or cover a topic in class. Don&rsquo;t try to memorise. Just understand.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Close everything</strong> &mdash; book shut, tab closed, notes flipped over. The whole point is that you cannot see the material.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Write down everything you can remember</strong> &mdash; no looking back. This is called a &ldquo;brain dump.&rdquo; Write until you run out. It should feel uncomfortable.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Check against the source</strong> &mdash; open the lesson. Mark what you missed in a different colour. Don&rsquo;t just glance &mdash; properly compare.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Target the gaps</strong> &mdash; re-study only the parts you missed. Not the whole lesson again. Just the holes.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Retest tomorrow</strong> &mdash; hit the same topic again within 24 hours. The second attempt is where the learning locks in.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>After studying the skeletal system, close your notes and write down all five bone shapes (long, short, flat, irregular, sesamoid) with one example and one function for each. Then add the four joint types (ball-and-socket, hinge, pivot, condyloid) and name an anatomical site for each. Check what you missed and rewrite only those entries tomorrow.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>After covering muscle fibre types, put your notes away and write out all three types (Type I, Type IIa, Type IIx) with their speed, fatigue resistance, and a sporting example for each. Add the three axes of movement (sagittal, frontal, vertical) and the planes each movement occurs in. The gaps you find are exactly what the examiner will ask about.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Peeking.</strong> If you look back during the brain dump, you&rsquo;re not doing retrieval &mdash; you&rsquo;re doing copying. Harder is better.</li>
<li><strong>Only doing it once.</strong> One pass strengthens memory a little. Spaced repeats strengthen it permanently. Come back to the same topic 2&ndash;3 times over a week.</li>
<li><strong>Doing it too soon after studying.</strong> If you retrieve while the material is still in short-term memory, it&rsquo;s too easy to count. Leave at least 30 minutes between studying and testing.</li>
<li><strong>Stopping when it feels difficult.</strong> Desirable difficulty is the whole point. If it feels easy, your memory isn&rsquo;t being challenged and you&rsquo;re not learning.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Build it in <strong>every week</strong>, from the start of Year 10 through to your exams. Aim for 15&ndash;20 minutes per subject, two or three times a week. The last two weeks before an exam is when retrieval practice becomes your main tool &mdash; swap passive reading for brain dumps and flashcards. On StudyVault, the Knowledge Check and Flashcard buttons in every lesson sidebar are retrieval practice in disguise &mdash; use them.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 25%;" title="Study: 5 min"></span>
<span style="background: #22c55e; width: 40%;" title="Brain dump: 8 min"></span>
<span style="background: #4ade80; width: 35%;" title="Check &amp; gaps: 7 min"></span>
</div>
<span class="guide-quick-ref-total">~20 minutes per topic</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Study one topic</li>
<li>Close everything</li>
<li>Brain dump from memory</li>
<li>Check gaps</li>
<li>Re-study only the gaps</li>
<li>Retest tomorrow</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_RETRIEVAL + """</div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 2 — SPACED REPETITION
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "spaced-repetition",
    "title": "Spaced Repetition",
    "sort_order": 2,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Distributed practice</span>
<h1>Spaced Repetition</h1>
<p class="guide-used-in">Forget, then retrieve &mdash; that&rsquo;s where the learning happens.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>The brain remembers things better when you review them just as you&rsquo;re about to forget them. Cram everything the night before and it&rsquo;s gone within a week. Revisit the same material on day one, day three, day seven, day fourteen and it sticks for months. This is the single biggest difference between students who peak in mocks and students who peak in the real exam.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Ebbinghaus (1885)</strong></td><td>Without revisiting, 50% of what you learn is lost within an hour and 80% within a day.</td><td>The forgetting curve is real &mdash; and steeper than most students realise.</td></tr>
<tr><td><strong>Cepeda et al. (2006)</strong></td><td>Meta-analysis of 254 studies: spaced practice beat massed practice in 259 out of 271 comparisons.</td><td>Spacing works across ages, subjects, and skills.</td></tr>
<tr><td><strong>Kang (2016)</strong></td><td>Optimal gap &asymp; 10&ndash;20% of the time until the test. For a May exam, that means revisiting material every 3&ndash;6 weeks from Year 10.</td><td>You can plan exactly when to revisit a topic.</td></tr>
<tr><td><strong>Sisti et al. (2007)</strong></td><td>Neurons form stronger connections during the &ldquo;almost forgotten&rdquo; moment of retrieval.</td><td>Struggling to recall IS the learning, not a sign you&rsquo;ve failed.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Learn a topic today</strong> &mdash; read the lesson, watch the video, write notes. Mark it in a diary or app with today&rsquo;s date.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Review in 24 hours</strong> &mdash; do a retrieval practice brain dump, or redo the knowledge check. 5&ndash;10 minutes.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Review again in 3 days</strong> &mdash; if you got it right yesterday, push the gap. Repeat the retrieval.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Review again in 7 days</strong> &mdash; by now the material is consolidating into long-term memory.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Review again in 2&ndash;3 weeks</strong> &mdash; gap the next review to 14 days, then 30, then 60.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>If you fail a review</strong> &mdash; reset the schedule. Back to day 1. Don&rsquo;t skip the reset &mdash; it&rsquo;s the point of the system.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Plan a four-week cycle that rotates through the four main areas weekly: anatomy and movement in week one, physical training principles in week two, sports psychology in week three, and health and well-being in week four. Each week you revisit the previous week&rsquo;s area briefly before moving on, so no topic gets more than seven days without a recall attempt.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>When you first learn the cardiac output formula (CO&nbsp;=&nbsp;HR&nbsp;&times;&nbsp;SV), write a worked example with real numbers and put it in your flashcard deck. Review it tomorrow, in three days, in a week. By the time Component 1 arrives, calculating stroke volume from given cardiac output and heart rate values will feel automatic rather than stressful.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Reviewing too often.</strong> If it&rsquo;s easy, the gap is too short. Make it harder by stretching the interval.</li>
<li><strong>Reviewing too late.</strong> If you&rsquo;ve completely forgotten, you&rsquo;re essentially re-learning from scratch &mdash; you lose the benefit of spacing.</li>
<li><strong>No written schedule.</strong> Spaced repetition works only if you actually do the reviews. Use a calendar, the StudyVault flashcard system, or a simple Leitner box.</li>
<li><strong>Skipping resets when you fail.</strong> If you couldn&rsquo;t recall the material, you haven&rsquo;t learnt it &mdash; regardless of how far through the schedule you were.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>This is the organising principle of your whole revision year &mdash; not a technique you pull out near the exam. From the first lesson of Year 10, log every topic you cover and schedule reviews at 1 day, 3 days, 7 days, 14 days, and 30 days. The StudyVault flashcard system does this automatically via the Leitner method &mdash; questions move between five boxes with intervals of 1, 2, 4, 7, and 14 days. When a card comes up, do it. When it doesn&rsquo;t, don&rsquo;t.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 20%;" title="Day 1"></span>
<span style="background: #22c55e; width: 20%;" title="Day 3"></span>
<span style="background: #4ade80; width: 20%;" title="Day 7"></span>
<span style="background: #86efac; width: 20%;" title="Day 14"></span>
<span style="background: #bbf7d0; width: 20%;" title="Day 30"></span>
</div>
<span class="guide-quick-ref-total">5 touches per topic, across a month</span>
<h4>Intervals</h4>
<ol class="guide-quick-ref-steps">
<li>Learn today</li>
<li>Retest tomorrow</li>
<li>Retest day 3</li>
<li>Retest day 7</li>
<li>Retest day 14</li>
<li>Retest day 30</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_SPACED + """</div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 3 — INTERLEAVING
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "interleaving",
    "title": "Interleaving",
    "sort_order": 3,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Mixed practice</span>
<h1>Interleaving</h1>
<p class="guide-used-in">Mix topics in one session &mdash; don&rsquo;t block them.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Most students revise by blocking &mdash; an hour on anatomy, an hour on training principles, an hour on sports psychology. It feels productive and the topic seems clear by the end. Interleaving is the opposite: you jump between topics inside a single session. It feels worse at the time, and you&rsquo;ll make more mistakes. But when the real exam arrives, you will be dramatically better at knowing <em>which</em> technique to apply &mdash; and that is usually the hardest part of any exam question.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Rohrer &amp; Taylor (2007)</strong></td><td>Students who interleaved topics scored 43% higher on delayed tests than blocked-practice students.</td><td>Same time spent &mdash; huge difference in exam performance.</td></tr>
<tr><td><strong>Birnbaum et al. (2013)</strong></td><td>Interleaved learners felt LESS confident during practice but performed BETTER in the test.</td><td>If revision feels too easy, interleave.</td></tr>
<tr><td><strong>Bjork &amp; Bjork (2011)</strong></td><td>Desirable difficulties &mdash; including interleaving &mdash; create durable long-term learning at the cost of short-term performance.</td><td>Short-term struggle is the price of long-term gain.</td></tr>
<tr><td><strong>Taylor &amp; Rohrer (2010)</strong></td><td>Benefit was largest when topics looked superficially similar &mdash; students learnt to DISTINGUISH them.</td><td>Most useful where students confuse similar concepts.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Pick 3&ndash;5 related topics</strong> &mdash; topics that share a paper, a theme, or a question type. Similar enough that students confuse them.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Make a mixed problem set</strong> &mdash; 10&ndash;15 questions drawn randomly from all the topics. Don&rsquo;t tell yourself which topic each question belongs to.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Attempt each question cold</strong> &mdash; first step is identifying what&rsquo;s being asked. That identification is the skill you&rsquo;re training.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Mark after every question</strong> &mdash; note which topic each one was. Pay attention to mis-identifications &mdash; those are the highest-value gaps.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Rebuild a new mixed set tomorrow</strong> &mdash; same topics, different questions. Different order. Over time, misclassifications drop.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Expect to feel worse than blocked practice</strong> &mdash; that&rsquo;s the right feeling. Your exam self will thank you.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Within a single revision session, alternate between Component 1 and Component 2 content: answer a question on lever systems, then one on arousal theory, then one on training methods (FITT principle), then one on barriers to participation. This forces your brain to switch contexts in the same way the exam paper does &mdash; topics are never neatly grouped on the actual paper.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Mix up questions on the three muscle fibre types, the three axes of movement, and the five components of fitness in one set. All three are list-based classification topics that students muddle under pressure. Interleaving them until you can answer any one cold &mdash; without being &ldquo;in the zone&rdquo; for that topic &mdash; is exactly what exam conditions require.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Random, not related.</strong> Interleaving PE with English is just subject-switching. Interleave WITHIN PE &mdash; related topics that students confuse.</li>
<li><strong>Giving up when it feels hard.</strong> The discomfort is the signal that it&rsquo;s working. Don&rsquo;t revert to blocked practice because interleaving feels slow.</li>
<li><strong>Labelling the topic at the top of each question.</strong> Defeats the point &mdash; the identification IS the training.</li>
<li><strong>Using it too early in learning.</strong> You need baseline familiarity with each topic first. Interleaving is for consolidation, not first exposure.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Once you&rsquo;ve covered a handful of related topics &mdash; usually partway through a term &mdash; start weaving them into mixed practice sessions. Very useful in the final 8&ndash;10 weeks before exams when you&rsquo;re moving from learning to applying. Full past papers are the ultimate interleaving exercise, because they force you to identify question types cold.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 40%;" title="Mixed practice"></span>
<span style="background: #22c55e; width: 30%;" title="Mark &amp; identify"></span>
<span style="background: #4ade80; width: 30%;" title="Fix mis-identifications"></span>
</div>
<span class="guide-quick-ref-total">~30&ndash;45 minutes per session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Pick 3&ndash;5 related topics</li>
<li>Build a mixed set</li>
<li>Attempt cold</li>
<li>Mark &amp; note topic</li>
<li>Fix misclassifications</li>
<li>Expect discomfort</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_INTERLEAVING + """</div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 4 — DUAL CODING
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "dual-coding",
    "title": "Dual Coding",
    "sort_order": 4,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Visual learning</span>
<h1>Dual Coding</h1>
<p class="guide-used-in">Combine words and visuals &mdash; your memory uses both.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Your brain stores words and images in two separate memory systems, and information is much better remembered when BOTH are used. Dual coding is not the same as &ldquo;being a visual learner&rdquo; &mdash; learning-styles theory has been debunked. Everyone benefits from combining words with visuals, regardless of any self-reported style preference.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Paivio (1971)</strong></td><td>Original dual-coding theory: verbal and visual memory traces are separate and additive.</td><td>Two routes to recall is better than one.</td></tr>
<tr><td><strong>Mayer (2001, 2014)</strong></td><td>Multimedia learning research across 300+ studies: well-designed words+visuals combinations produce ~40% better transfer than words alone.</td><td>Well-placed visuals turn passive reading into active learning.</td></tr>
<tr><td><strong>Dunlosky et al. (2013)</strong></td><td>Dual coding is one of the few techniques rated &ldquo;effective in most contexts&rdquo; by the Association for Psychological Science.</td><td>Evidence-backed across age groups and subjects.</td></tr>
<tr><td><strong>Castro-Alonso et al. (2019)</strong></td><td>Student-generated visuals (drawing) produced bigger gains than pre-made visuals.</td><td>Draw it yourself, don&rsquo;t just look at a diagram.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Pick a topic with relationships</strong> &mdash; causes and effects, processes, comparisons, classifications. Dual coding shines when there&rsquo;s structure to capture.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Choose the right visual format</strong> &mdash; annotated diagram for anatomy, flowchart for physiological processes, comparison table for muscle fibre types, worked formula for calculations.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Draw it yourself</strong> &mdash; by hand or in a simple tool. Don&rsquo;t just photocopy one from a textbook. The act of creating the visual forces your brain to organise the information.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Keep text minimal</strong> &mdash; labels, not sentences. The text and the visual should say different things. Duplicate labels distract (&ldquo;redundancy effect&rdquo;).</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Revisit blank versions</strong> &mdash; print or redraw your visual with the labels removed. Fill them in from memory. This combines dual coding with retrieval practice.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Compare versions over time</strong> &mdash; a week later, redraw from memory. Spot the bits you missed.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Draw a blank skeleton and annotate each major joint with its joint type (ball-and-socket, hinge, pivot, condyloid) and one example movement at that joint. Add arrows showing the agonist and antagonist muscles for one selected movement &mdash; for example, elbow flexion with the biceps brachii contracting and triceps brachii relaxing. Cover it and redraw from memory the next day.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Create a lever-system diagram for each class (1st, 2nd, 3rd) with the fulcrum, effort, and load clearly positioned and a real anatomical example labelled: 1st class &mdash; neck extension (fulcrum at atlas joint); 2nd class &mdash; calf raise (fulcrum at ball of foot); 3rd class &mdash; bicep curl (fulcrum at elbow). Alongside, write out CO&nbsp;=&nbsp;HR&nbsp;&times;&nbsp;SV with a worked example using realistic resting and exercise values.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Decorative visuals.</strong> A picture that looks nice but doesn&rsquo;t convey information adds cognitive load without the benefit.</li>
<li><strong>Copying someone else&rsquo;s.</strong> The learning happens while you make it. A textbook diagram is useful for reference, not for dual coding.</li>
<li><strong>Too much text.</strong> If your &ldquo;mind map&rdquo; is paragraphs joined by lines, it&rsquo;s still just text. Keep labels to 2&ndash;4 words.</li>
<li><strong>Only making it once.</strong> One-off diagrams are useful. Ones you redraw from memory over weeks are powerful.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Mid-revision cycle &mdash; after you&rsquo;ve learnt the basic facts and are starting to see connections. Before the exam, try a &ldquo;one-page summary&rdquo; for each body system (skeletal, muscular, cardiovascular, respiratory) combining a key diagram with 5&ndash;10 labelled points. Carry these in your bag. Use the night before.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 30%;" title="Plan structure"></span>
<span style="background: #22c55e; width: 45%;" title="Draw &amp; label"></span>
<span style="background: #4ade80; width: 25%;" title="Blank redraw"></span>
</div>
<span class="guide-quick-ref-total">~30 minutes per visual</span>
<h4>Formats</h4>
<ol class="guide-quick-ref-steps">
<li>Annotated diagram</li>
<li>Flowchart</li>
<li>Comparison table</li>
<li>Worked formula</li>
<li>Mind map</li>
<li>Venn / 2&times;2 grid</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_DUAL + """</div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 5 — ELABORATIVE INTERROGATION
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "elaborative-interrogation",
    "title": "Elaborative Interrogation",
    "sort_order": 5,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Deep thinking</span>
<h1>Elaborative Interrogation</h1>
<p class="guide-used-in">Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; until the facts become explanations.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Facts in isolation are fragile. Facts connected by explanations survive. Elaborative interrogation is the habit of asking &ldquo;why is that true?&rdquo; and &ldquo;how does that work?&rdquo; about every fact you learn &mdash; and forcing yourself to answer. The answer doesn&rsquo;t need to be perfect. The act of trying to answer is what builds the mental connections that turn memorised facts into understood explanations.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Pressley et al. (1988)</strong></td><td>Asking &ldquo;why?&rdquo; during reading boosted recall by 40&ndash;70% compared to silent reading.</td><td>Works even when the answer is imperfect.</td></tr>
<tr><td><strong>Dunlosky et al. (2013)</strong></td><td>Rated &ldquo;moderate utility&rdquo; in the APS review &mdash; robust across subjects and ages, especially when applied to new material that builds on existing knowledge.</td><td>Best for consolidating material you half-know.</td></tr>
<tr><td><strong>Smith &amp; Holliday (2006)</strong></td><td>Science students who self-explained while studying scored significantly higher on transfer questions requiring application.</td><td>Builds the ability to USE the knowledge, not just recall it.</td></tr>
<tr><td><strong>Chi et al. (1994)</strong></td><td>Self-explanation was a stronger predictor of understanding than prior knowledge.</td><td>Even weaker students catch up by explaining to themselves.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Study a chunk of content</strong> &mdash; a lesson, a paragraph, a key fact. Anything where facts are being introduced.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>After each fact, ask &ldquo;why?&rdquo;</strong> &mdash; why is this true? Why does it matter? Why does this happen in the body?</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Then ask &ldquo;how?&rdquo;</strong> &mdash; how does this connect to performance? How does it lead to what comes next physiologically? How would you explain it to someone who has never studied PE?</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Try to answer out loud</strong> &mdash; even if your answer is wrong, the attempt activates deeper processing. Write your answer in the margin.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Check your answer against the source</strong> &mdash; does the lesson support your explanation? If not, update it. The correction matters more than the first guess.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Build chains</strong> &mdash; once you&rsquo;ve asked &ldquo;why?&rdquo; once, ask it again of your answer. Push until you hit a genuinely fundamental physiological principle. This is where deep understanding forms.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Fact: when the biceps brachii contracts, the triceps brachii relaxes. Ask WHY: because antagonistic pairs work by reciprocal inhibition &mdash; the nervous system suppresses the opposing muscle to allow smooth movement. Ask HOW: the motor neurones to the agonist activate while an inhibitory signal prevents the antagonist from contracting simultaneously. That chain of &ldquo;why&rdquo; turns a one-line fact into an explanation you can apply to any joint action question.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Fact: Type I (slow-twitch) muscle fibres are used in endurance events; Type IIx (fast-twitch) in explosive power events. Ask WHY: Type I fibres have more mitochondria and myoglobin, so they generate energy aerobically and resist fatigue. Ask WHY Type IIx fibres fatigue faster: they rely on anaerobic glycolysis, which produces lactic acid as a by-product. That chain explains not just what the fibres do but why &mdash; exactly what a 6-mark exam question demands.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Accepting &ldquo;I don&rsquo;t know&rdquo;.</strong> Take a guess. Even a wrong guess activates the processing. Then check and correct.</li>
<li><strong>One &ldquo;why?&rdquo; and moving on.</strong> The real gains come from the third or fourth &ldquo;why?&rdquo;, when you hit the fundamentals.</li>
<li><strong>Only asking the obvious questions.</strong> Push toward the explanations your teacher never gave you &mdash; those are where genuine learning happens.</li>
<li><strong>Skipping the check.</strong> Unchecked wrong answers reinforce misunderstanding. Always verify against the source.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Any time you&rsquo;re covering conceptual material &mdash; not just listing facts. Particularly powerful with cause-and-effect physiology (why cardiac output increases during exercise, why the body shunts blood to working muscles) and with applied scenarios where the exam gives you a sport and asks you to explain a physiological response. Build it into every lesson revisit, not as a separate session.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 20%;" title="Read fact"></span>
<span style="background: #22c55e; width: 45%;" title="Ask why/how, answer"></span>
<span style="background: #4ade80; width: 35%;" title="Check &amp; build chain"></span>
</div>
<span class="guide-quick-ref-total">Adds ~50% to reading time, transforms recall</span>
<h4>Questions to ask</h4>
<ol class="guide-quick-ref-steps">
<li>Why is this true?</li>
<li>How does it work?</li>
<li>Why does it matter?</li>
<li>How does it connect?</li>
<li>Why does this happen in the body?</li>
<li>How would I explain this to a friend?</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_ELABORATIVE + """</div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 6 — KNOWLEDGE ORGANISERS
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "knowledge-organisers",
    "title": "Knowledge Organisers",
    "sort_order": 6,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Structured notes</span>
<h1>Knowledge Organisers</h1>
<p class="guide-used-in">One page per topic &mdash; the whole picture at a glance.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>A knowledge organiser is a single side of A4 that captures everything a student needs to know about a topic &mdash; key vocabulary, essential facts, core concepts, and connections between them. Used properly, it becomes the base layer of your revision: the thing you keep coming back to, the thing you redraw from memory, the thing you carry on the bus. Used badly, it becomes a wall of dense text that nobody reads.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Willingham (2017)</strong></td><td>Students need to store facts in long-term memory before they can think critically about them. Knowledge organisers are the storage scaffold.</td><td>Not old-fashioned &mdash; cognitive prerequisite for analysis.</td></tr>
<tr><td><strong>Counsell (2018)</strong></td><td>Used in UK schools to reduce cognitive load by pre-structuring the material students encounter.</td><td>Reduces working memory demand during lessons.</td></tr>
<tr><td><strong>Sweller (1988)</strong></td><td>Cognitive Load Theory: well-organised schemas free up working memory for higher-order tasks.</td><td>A well-designed organiser makes hard questions easier.</td></tr>
<tr><td><strong>Oakes &amp; Griffin (2017)</strong></td><td>Students who made their OWN organisers outperformed those given finished ones.</td><td>Making is learning. Receiving is not.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>One topic per organiser</strong> &mdash; one body system, one training principle, one mental strategy. Not a whole component. Too broad and it becomes a dense textbook page.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Divide the page into 4&ndash;6 sections</strong> &mdash; typically: Key Vocabulary, Key Facts / Formulae, Core Concepts, Anatomical Examples, Connections to Performance. The structure forces you to categorise.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Keep it to one side of A4</strong> &mdash; the constraint is the point. If it doesn&rsquo;t fit, the material isn&rsquo;t yet compressed into the essentials.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Use tiny structural visuals</strong> &mdash; a mini-skeleton outline, a lever diagram, a formula box. Dual coding applies: words + visuals beat words alone.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Redraw it from memory weekly</strong> &mdash; this is where the learning is. A finished organiser you never revisit is wasted. The redrawn one is retrieval practice in disguise.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Annotate over time</strong> &mdash; when you learn something new that fits, add it. When a connection becomes clearer, draw the link. The organiser evolves.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Create one A4 organiser for each body system: skeletal (5 bone shapes + examples, 4 joint types + sites, key bones labelled), muscular (3 fibre types with speed/fatigue/sport, agonist/antagonist pairs, key muscles labelled), cardiovascular (CO&nbsp;=&nbsp;HR&nbsp;&times;&nbsp;SV with values, cardiac changes during exercise, blood redistribution), respiratory (lung volumes, gaseous exchange, breathing rate changes). Four organisers, one per system &mdash; the backbone of Component 1 revision.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Build a &ldquo;psychology terms&rdquo; organiser for Component 2 that captures all the mental strategies (goal-setting, imagery, self-talk, arousal control) with a one-line definition and a sporting scenario for each. Add a second mini-section listing the barriers to participation (cost, access, social influences, disability) with one counter-strategy each. Redraw it without looking the night before the exam.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Copying the textbook.</strong> A dense page of 8pt text isn&rsquo;t a knowledge organiser &mdash; it&rsquo;s a photocopy. Compress ruthlessly.</li>
<li><strong>One page per component.</strong> Too much, too diffuse. One page per body system or topic area.</li>
<li><strong>Making one and never revisiting.</strong> The value is in the redrawing &mdash; not the original creation.</li>
<li><strong>Using a downloaded one instead of making your own.</strong> Research is clear: making beats receiving. Teacher-provided organisers are useful for structure only.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Start one at the beginning of each topic, as you&rsquo;re learning it. Refine as your understanding grows. Redraw the whole set from memory in the final month before exams &mdash; one topic per day. Carry a folder of your organisers to every revision session. Use them as the spine of retrieval practice: cover the organiser, brain-dump, then check.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 35%;" title="Plan &amp; structure"></span>
<span style="background: #22c55e; width: 35%;" title="Compress onto A4"></span>
<span style="background: #4ade80; width: 30%;" title="Redraw weekly"></span>
</div>
<span class="guide-quick-ref-total">~45 minutes to create, 15 to redraw</span>
<h4>Sections</h4>
<ol class="guide-quick-ref-steps">
<li>Key Vocabulary</li>
<li>Key Facts / Formulae</li>
<li>Core Concepts</li>
<li>Anatomical Examples</li>
<li>Connections to Performance</li>
<li>Common Misconceptions</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_KO + """</div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 7 — TIMED PRACTICE
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": PE_SUBJECT_ID,
    "school_id": None,
    "guide_type": "revision-technique",
    "slug": "timed-practice",
    "title": "Timed Practice",
    "sort_order": 7,
    "status": "live",
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Exam conditions</span>
<h1>Timed Practice</h1>
<p class="guide-used-in">Simulate the real thing &mdash; including the time pressure.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Knowing the content is only half of an exam. The other half is managing time, reading questions accurately under pressure, writing neatly when your hand hurts, and staying calm when you don&rsquo;t know one of the questions. These are all skills &mdash; and like any skill, they need practice. Timed practice is how you build them.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Soderstrom &amp; Bjork (2015)</strong></td><td>Transfer-appropriate processing: performance is best when the practice conditions closely match the test conditions.</td><td>Practise in the conditions you&rsquo;ll be tested in.</td></tr>
<tr><td><strong>Agarwal et al. (2017)</strong></td><td>Students who did timed practice tests scored higher even on unseen questions.</td><td>Builds generalisable exam skill, not just familiarity.</td></tr>
<tr><td><strong>Yerkes &amp; Dodson (1908)</strong></td><td>Performance is best at MODERATE arousal &mdash; some pressure helps, too much hurts.</td><td>Simulated pressure builds tolerance for real pressure.</td></tr>
<tr><td><strong>Hinze &amp; Rapp (2014)</strong></td><td>Students who experienced test-like practice reported 30% less exam anxiety.</td><td>Familiarity reduces fear. Fear reduces performance.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Start small</strong> &mdash; begin with one timed question or one section. Don&rsquo;t jump straight to full papers. Build the muscle gradually.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Match the Edexcel mark-to-time ratio</strong> &mdash; roughly 1 mark per minute. 2-mark &lsquo;Describe&rsquo; questions: 2&ndash;3 minutes. 6-mark &lsquo;Discuss&rsquo; questions: 8 minutes. 9-mark &lsquo;Assess&rsquo; questions: 12 minutes including 2 minutes&rsquo; planning.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Remove distractions</strong> &mdash; phone in another room, no music, no snacks, no notes. The real exam hall has none of these.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Handwrite</strong> &mdash; the exam is handwritten. Typing is faster and feels more productive, but it doesn&rsquo;t train the same skill. Your hand will hurt on the day and that&rsquo;s normal.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Mark with the mark scheme honestly</strong> &mdash; use StudyVault&rsquo;s per-question mark schemes or a teacher-provided one. Be harsh on yourself &mdash; underscoring now prevents overconfidence later.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Do a full paper under conditions a month before the exam</strong> &mdash; uninterrupted, correct time, no music. One per subject, one per week in the final stretch.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Physical Education Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>For a 2-mark &lsquo;Describe&rsquo; question, set a 3-minute timer and write your answer before it expires. For a 6-mark &lsquo;Discuss&rsquo; question, allow 8 minutes: 1 minute to plan three distinct points, then write at pace. Check your answer against the mark scheme &mdash; are you hitting the command word? A &lsquo;Discuss&rsquo; needs developed points with evidence; a &lsquo;Describe&rsquo; needs accurate recall only.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>For a 9-mark &lsquo;Assess&rsquo; question, allow exactly 12 minutes: 2 minutes to plan (list three advantages and two disadvantages of the training method in the question stem), then write in continuous prose. In the final minute, check you have made a judgement &mdash; &lsquo;Assess&rsquo; always requires a supported conclusion, not just a list. Practise this structure repeatedly until the timing feels natural rather than rushed.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Stopping when the timer runs out and ignoring the unfinished bit.</strong> Note what you&rsquo;d have written &mdash; that&rsquo;s the data about your pace.</li>
<li><strong>Using notes during &ldquo;timed&rdquo; practice.</strong> It&rsquo;s not timed practice &mdash; it&rsquo;s open-book practice. Useful, but different.</li>
<li><strong>Only doing it in the last fortnight.</strong> Too late &mdash; you&rsquo;ve not left time to fix the weaknesses the practice reveals.</li>
<li><strong>Not marking honestly.</strong> Marking your own work gently protects feelings now and destroys results later.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>From 10 weeks out, do at least one timed practice per subject per week &mdash; usually a single section at first, building to full papers. In the final month, do at least one full timed paper per subject. Always mark it against the actual Edexcel scheme and note your pace &mdash; the 9-mark questions are where most students drop marks by running out of time.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 15%;" title="Setup"></span>
<span style="background: #22c55e; width: 60%;" title="Attempt under time"></span>
<span style="background: #4ade80; width: 25%;" title="Mark &amp; review"></span>
</div>
<span class="guide-quick-ref-total">Paper time + ~30 min marking</span>
<h4>Edexcel PE time guide</h4>
<ol class="guide-quick-ref-steps">
<li>2-mark Describe &mdash; 2&ndash;3 min</li>
<li>4-mark Explain &mdash; 5 min</li>
<li>6-mark Discuss &mdash; 8 min</li>
<li>9-mark Assess &mdash; 12 min (plan 2)</li>
<li>Full paper, timed</li>
<li>Full paper, exam conditions</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">""" + OTHER_LINKS_EXCEPT_TIMED + """</div>
</div>
</div>
</aside>"""
})

# ─────────────────────────────────────────────────────────────
# INSERT
# ─────────────────────────────────────────────────────────────

print(f"Inserting {len(pages)} guide pages for physical-education-edexcel...")

for page in pages:
    # Check for existing row
    existing = sb.table('guide_pages').select('id').eq('subject_id', PE_SUBJECT_ID).eq('slug', page['slug']).eq('guide_type', 'revision-technique').execute()
    if existing.data:
        print(f"  SKIP (exists): {page['slug']}")
        continue

    # guide_pages has no school_id or status column — strip them
    row = {k: v for k, v in page.items() if k not in ('school_id', 'status')}
    result = sb.table('guide_pages').insert(row).execute()
    if result.data:
        print(f"  OK: {page['slug']} (id={result.data[0]['id']})")
    else:
        print(f"  ERROR inserting {page['slug']}: {result}")

print("Done.")
