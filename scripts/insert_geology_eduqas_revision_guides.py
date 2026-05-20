"""
Insert Geology (GCSE Geology) revision technique guide pages into Supabase.
Subject slug: geology-eduqas
Subject ID: 80a6d0f4-f4bf-4166-b0c5-59d2310a3230
school_id: NULL (free tier)
guide_type: revision-technique (singular)
status: live
8 rows: 1 hub index + 7 individual technique pages
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://baipckgywpnwapobwtsy.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
GEOLOGY_SUBJECT_ID = '80a6d0f4-f4bf-4166-b0c5-59d2310a3230'
SLUG = 'geology-eduqas'

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

OTHER_TECHNIQUES_LINKS = f"""<a href="/guide/{SLUG}/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/{SLUG}/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/{SLUG}/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/{SLUG}/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/{SLUG}/revision-technique/interleaving">Interleaving</a>
<a href="/guide/{SLUG}/revision-technique/knowledge-organisers">Knowledge Organisers</a>
<a href="/guide/{SLUG}/revision-technique/timed-practice">Timed Practice</a>"""

pages = []

# ══════════════════════════════════════════════════════════════
# sort_order = 0 — HUB INDEX
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "index",
    "title": "Revision Techniques",
    "sort_order": 0,
    "content_html": """<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>Evidence-based strategies tailored to GCSE Geology. Geology rewards students who can recall factual detail precisely &mdash; the Mohs hardness scale 1&ndash;10, the 13 named geological periods from Cambrian to Quaternary, named plate boundaries and their associated features &mdash; and who can also interpret data under pressure: reading graphic logs, identifying structures on geological maps, and sequencing rock strata from cross-sections. The techniques below are chosen to match exactly those dual demands of factual recall and applied interpretation.</p>
</div>
</div>
<div class="guide-hub">

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these from day one</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/retrieval-practice">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself, don&rsquo;t just re-read. Brain dump the Mohs scale with one named mineral per hardness, or recall all 13 geological periods in order. Self-quizzing beats highlighting every time.</p>
</a>
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/spaced-repetition">
<span class="guide-question-marks">Distributed practice</span>
<h3>Spaced Repetition</h3>
<p>Revisit rocks and minerals, geological time, earth structure and hazards at 1, 3, 7, 14, 30-day gaps. Half-lives and named periods need spacing &mdash; they vanish without it.</p>
</a>
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/dual-coding">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>Combine words and visuals. Sketch the rock cycle with labelled process arrows, draw annotated cross-sections of plate boundaries, or create a graphic log from scratch. Diagram plus words sticks far better than text alone.</p>
</a>
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; to deepen understanding. Why does basalt have fine crystals while granite has coarse ones? Why do zone fossils have to be geographically widespread and time-limited? Turn memorised facts into understood explanations.</p>
</a>
</div>
</div>

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Consolidation Techniques</h2>
<span class="guide-paper-ref">Use these once you know the basics</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/interleaving">
<span class="guide-question-marks">Mixed practice</span>
<h3>Interleaving</h3>
<p>Mix igneous, sedimentary and metamorphic identification in one practice set rather than revising one rock type at a time. The exam tests discrimination &mdash; knowing which rock is which &mdash; not single-type recall.</p>
</a>
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/knowledge-organisers">
<span class="guide-question-marks">Structured notes</span>
<h3>Knowledge Organisers</h3>
<p>One A4 page per unit &mdash; the 4 plate-boundary types with named examples and motion arrows, or the key mineral properties with Mohs position. Redraw from memory. The base layer of every good revision routine.</p>
</a>
</div>
</div>

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Exam Preparation</h2>
<span class="guide-paper-ref">Final weeks &mdash; sharpen and apply</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/geology-eduqas/revision-technique/timed-practice">
<span class="guide-question-marks">Exam conditions</span>
<h3>Timed Practice</h3>
<p>Simulate the real thing. Timed rock identification and geological history sequencing under exam conditions. Time pressure, no notes, handwritten. Builds the exam skill, not just the content knowledge.</p>
</a>
</div>
</div>

</div>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 1 — RETRIEVAL PRACTICE
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "retrieval-practice",
    "title": "Retrieval Practice",
    "sort_order": 1,
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
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>After studying the Mohs hardness scale, close the book and write down all ten hardness levels with one named mineral for each &mdash; from talc at 1 through to diamond at 10. Check what you missed, rewrite only those entries, and test yourself again tomorrow. Most students can get 1&ndash;6 easily; 7&ndash;10 need extra retrieval passes.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>After covering geological time, brain-dump the 13 named periods from Cambrian to Quaternary in order, with an approximate start date for each. Check your sequence and dates against the source. The periods students most often drop are Ordovician, Silurian, and Carboniferous &mdash; target those gaps specifically on the next pass.</p>
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
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/geology-eduqas/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/geology-eduqas/revision-technique/interleaving">Interleaving</a>
<a href="/guide/geology-eduqas/revision-technique/knowledge-organisers">Knowledge Organisers</a>
<a href="/guide/geology-eduqas/revision-technique/timed-practice">Timed Practice</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 2 — SPACED REPETITION
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "spaced-repetition",
    "title": "Spaced Repetition",
    "sort_order": 2,
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
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Radioactive decay half-lives are high-stakes recall: carbon-14 has a half-life of 5,730 years; uranium-238 has a half-life of 4.47 billion years. These are the kind of precise figures that vanish if you only see them once. Schedule retrieval at 1 day, 3 days, 7 days, and 14 days after first studying absolute dating &mdash; the spacing forces your brain to rebuild the connection each time rather than just recognising it.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>The 13 geological periods feel manageable when you first read them, but students lose Ordovician, Silurian, and Devonian within days if they don&rsquo;t revisit. After learning the stratigraphic column, space your reviews: brain-dump the periods tomorrow, again at day 3, again at day 7. Each time you recall the sequence under mild pressure, the memory trace deepens.</p>
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
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/geology-eduqas/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/geology-eduqas/revision-technique/interleaving">Interleaving</a>
<a href="/guide/geology-eduqas/revision-technique/knowledge-organisers">Knowledge Organisers</a>
<a href="/guide/geology-eduqas/revision-technique/timed-practice">Timed Practice</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 3 — INTERLEAVING
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "interleaving",
    "title": "Interleaving",
    "sort_order": 3,
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Mixed practice</span>
<h1>Interleaving</h1>
<p class="guide-used-in">Mix topics in one session &mdash; don&rsquo;t block them.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Most students revise by blocking &mdash; an hour on algebra, an hour on geometry, an hour on statistics. It feels productive and the topic seems clear by the end. Interleaving is the opposite: you jump between topics inside a single session. It feels worse at the time, and you&rsquo;ll make more mistakes. But when the real exam arrives, you will be dramatically better at knowing <em>which</em> technique to apply &mdash; and that is usually the hardest part of any exam question.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Rohrer &amp; Taylor (2007)</strong></td><td>Students who interleaved maths topics scored 43% higher on delayed tests than blocked-practice students.</td><td>Same time spent &mdash; huge difference in exam performance.</td></tr>
<tr><td><strong>Birnbaum et al. (2013)</strong></td><td>Interleaved learners felt LESS confident during practice but performed BETTER in the test.</td><td>If revision feels too easy, interleave.</td></tr>
<tr><td><strong>Bjork &amp; Bjork (2011)</strong></td><td>Desirable difficulties &mdash; including interleaving &mdash; create durable long-term learning at the cost of short-term performance.</td><td>Short-term struggle is the price of long-term gain.</td></tr>
<tr><td><strong>Taylor &amp; Rohrer (2010)</strong></td><td>Benefit was largest when topics looked superficially similar &mdash; students learnt to DISTINGUISH them.</td><td>Most useful where students confuse similar techniques.</td></tr>
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
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Build a mixed practice set with specimens or descriptions from all three rock families: igneous (granite, basalt, pumice), sedimentary (sandstone, limestone, mudstone), and metamorphic (slate, schist, marble). Do not group them by type. For each one, identify the rock, state its origin, and name one key mineral or texture that gives it away. The exam tests discrimination &mdash; knowing what the rock is when no label is provided.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Mix questions on plate boundaries across a single session: a divergent boundary question (Mid-Atlantic Ridge), a convergent subduction question (Andes), a continental collision question (Himalayas), and a conservative boundary question (San Andreas Fault). Each has different features, hazards, and associated rock types. Interleaving forces you to identify which boundary type applies before you can answer &mdash; exactly what the exam requires.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Random, not related.</strong> Interleaving History with Maths is just subject-switching. Interleave WITHIN a subject &mdash; related topics that students confuse.</li>
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
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/geology-eduqas/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/geology-eduqas/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/geology-eduqas/revision-technique/knowledge-organisers">Knowledge Organisers</a>
<a href="/guide/geology-eduqas/revision-technique/timed-practice">Timed Practice</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 4 — DUAL CODING
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "dual-coding",
    "title": "Dual Coding",
    "sort_order": 4,
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
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Pick a topic with relationships</strong> &mdash; causes and effects, timelines, comparisons, processes. Dual coding shines when there&rsquo;s structure to capture.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Choose the right visual format</strong> &mdash; timeline for chronology, flowchart for processes, comparison table for differences, mind map for themes, annotated diagram for systems.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Draw it yourself</strong> &mdash; by hand or in a simple tool. Don&rsquo;t just photocopy one from a textbook. The act of creating the visual forces your brain to organise the information.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Keep text minimal</strong> &mdash; labels, not sentences. The text and the visual should say different things. Duplicate labels distract (&ldquo;redundancy effect&rdquo;).</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Revisit blank versions</strong> &mdash; print or redraw your visual with the labels removed. Fill them in from memory. This combines dual coding with retrieval practice.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Compare versions over time</strong> &mdash; a week later, redraw from memory. Spot the bits you missed.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Sketch the rock cycle as a circular flowchart with labelled arrows for every transition process: weathering and erosion, transportation, deposition and compaction/cementation (sedimentary), heat and pressure (metamorphic), melting and crystallisation (igneous). Minimise text &mdash; each arrow gets a process name only. Redraw it from memory a week later and check how many process labels you placed correctly.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Create an annotated cross-section of a stratigraphic sequence: draw horizontal strata, label the rock types in each layer, add a fault cutting across them, mark the unconformity surface, and indicate relative age with arrows. The visual forces you to apply the laws of superposition, original horizontality, and cross-cutting relationships simultaneously &mdash; far more effective than reading definitions of each principle separately.</p>
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
<p>Mid-revision cycle &mdash; after you&rsquo;ve learnt the basic facts and are starting to see connections. Before the exam, try a &ldquo;one-page summary&rdquo; for each unit combining a key diagram with 5&ndash;10 labelled points. Carry these in your bag. Use the night before.</p>
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
<li>Timeline</li>
<li>Flowchart</li>
<li>Comparison table</li>
<li>Mind map</li>
<li>Annotated diagram</li>
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
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/geology-eduqas/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/geology-eduqas/revision-technique/interleaving">Interleaving</a>
<a href="/guide/geology-eduqas/revision-technique/knowledge-organisers">Knowledge Organisers</a>
<a href="/guide/geology-eduqas/revision-technique/timed-practice">Timed Practice</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 5 — ELABORATIVE INTERROGATION
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "elaborative-interrogation",
    "title": "Elaborative Interrogation",
    "sort_order": 5,
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
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>After each fact, ask &ldquo;why?&rdquo;</strong> &mdash; why is this true? Why does it matter? Why did the author include it?</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Then ask &ldquo;how?&rdquo;</strong> &mdash; how does this connect to the topic? How does it lead to what comes next? How would you explain it to someone else?</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Try to answer out loud</strong> &mdash; even if your answer is wrong, the attempt activates deeper processing. Write your answer in the margin.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Check your answer against the source</strong> &mdash; does the text support your explanation? If not, update it. The correction matters more than the first guess.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Build chains</strong> &mdash; once you&rsquo;ve asked &ldquo;why?&rdquo; once, ask it again of your answer. Push until you hit a genuinely fundamental fact. This is where deep understanding forms.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>You learn that basalt forms fine crystals and granite forms coarse ones. Ask &ldquo;why?&rdquo;: because cooling rate controls crystal size. Ask &ldquo;why?&rdquo; again: slow cooling (deep intrusive) gives ions more time to migrate and join a growing crystal lattice; rapid cooling (extrusive at surface) freezes ions in place before crystals can grow. Now ask &ldquo;how does this explain pumice?&rdquo;: volcanic glass forms when magma is quenched so rapidly that no crystal structure develops at all. One chain of &ldquo;whys&rdquo; connects three rock types through a single principle.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>You learn that zone fossils must be geographically widespread and time-limited. Ask &ldquo;why geographically widespread?&rdquo;: so the same species can be found in rock layers across different locations, enabling correlation. Ask &ldquo;why time-limited?&rdquo;: if the species survived too long, its presence wouldn&rsquo;t narrow down when the rock formed. Ask &ldquo;how does this explain why ammonites make better zone fossils than sharks?&rdquo;: ammonites evolved rapidly, producing distinct species over short time intervals, while sharks changed little over hundreds of millions of years.</p>
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
<p>Any time you&rsquo;re covering conceptual material &mdash; not just listing facts. Particularly powerful with cause-and-effect topics (history, science, economics) and with analytical subjects (English literature, RE) where the exam rewards explanation over recall. Build it into every lesson revisit, not as a separate session.</p>
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
<li>Why now and not before?</li>
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
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/geology-eduqas/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/geology-eduqas/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/geology-eduqas/revision-technique/interleaving">Interleaving</a>
<a href="/guide/geology-eduqas/revision-technique/knowledge-organisers">Knowledge Organisers</a>
<a href="/guide/geology-eduqas/revision-technique/timed-practice">Timed Practice</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 6 — KNOWLEDGE ORGANISERS
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "knowledge-organisers",
    "title": "Knowledge Organisers",
    "sort_order": 6,
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
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>One topic per organiser</strong> &mdash; a unit, a theme, a text, a module. Not a whole paper. Too broad and it becomes a dense textbook page.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Divide the page into 4&ndash;6 sections</strong> &mdash; typically: Key Vocabulary, Key Facts / Dates, Core Concepts, Key Quotations or Examples, Connections to Other Topics. The structure forces you to categorise.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Keep it to one side of A4</strong> &mdash; the constraint is the point. If it doesn&rsquo;t fit, the material isn&rsquo;t yet compressed into the essentials.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Use tiny structural visuals</strong> &mdash; a mini-timeline, a 2&times;2 grid, a small flowchart. Dual coding applies: words + visuals beat words alone.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Redraw it from memory weekly</strong> &mdash; this is where the learning is. A finished organiser you never revisit is wasted. The redrawn one is retrieval practice in disguise.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Annotate over time</strong> &mdash; when you learn something new that fits, add it. When a connection becomes clearer, draw the link. The organiser evolves.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>One A4 page for the four plate-boundary types: divide into four quadrants, one per boundary (divergent, convergent oceanic-continental, convergent continental-continental, conservative). Each quadrant has: the boundary name, a named real-world example, a simple motion-arrow sketch, and the key resulting geology or hazard (e.g. mid-ocean ridge / rift valley; Andes / subduction trench; Himalayas / fold mountains; San Andreas / strike-slip fault). Redraw from memory weekly &mdash; the motion arrows are usually where students slip.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>One A4 page for mineral identification: draw a table with columns for Hardness (Mohs), Cleavage/Fracture, Colour/Streak, Lustre, and Named Mineral. Populate it for eight key minerals &mdash; quartz, feldspar, mica, calcite, halite, pyrite, olivine, talc. Leave the mineral column blank when you redraw it. This organiser doubles as a retrieval practice tool: cover the mineral column, fill from memory, then check.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Copying the textbook.</strong> A dense page of 8pt text isn&rsquo;t a knowledge organiser &mdash; it&rsquo;s a photocopy. Compress ruthlessly.</li>
<li><strong>One page per subject.</strong> Too much, too diffuse. One page per topic / unit / theme.</li>
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
<li>Key Facts / Dates</li>
<li>Core Concepts</li>
<li>Key Quotations / Examples</li>
<li>Connections to Other Topics</li>
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
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/geology-eduqas/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/geology-eduqas/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/geology-eduqas/revision-technique/interleaving">Interleaving</a>
<a href="/guide/geology-eduqas/revision-technique/timed-practice">Timed Practice</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 7 — TIMED PRACTICE
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": GEOLOGY_SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "timed-practice",
    "title": "Timed Practice",
    "sort_order": 7,
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
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Match the exam mark-to-time ratio</strong> &mdash; if the real paper gives 1 mark per minute, give yourself the same. If you go over, stop and mark what you have.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Remove distractions</strong> &mdash; phone in another room, no music, no snacks, no notes. The real exam hall has none of these.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Handwrite</strong> &mdash; the exam is handwritten. Typing is faster and feels more productive, but it doesn&rsquo;t train the same skill. Your hand will hurt on the day and that&rsquo;s normal.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Mark with the mark scheme honestly</strong> &mdash; use StudyVault&rsquo;s per-question mark schemes or a teacher-provided one. Be harsh on yourself &mdash; underscoring now prevents overconfidence later.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Do a full paper under conditions a month before the exam</strong> &mdash; uninterrupted, correct time, no music. One per subject, one per week in the final stretch.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Geology Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>Take a 30-minute timed section covering rock identification and geological history sequencing: set a timer, attempt the questions with no notes, and stop when time expires. Mark honestly against the mark scheme. Focus on whether you correctly identified the rock type from description, assigned the right period to the fossil evidence, and sequenced the events in the cross-section using the law of superposition and cross-cutting relationships. Note where you ran out of time &mdash; that pacing is the data.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>Sit a full past paper under exam conditions six weeks before the exam: no notes, correct time allocation, handwritten, silent room. When you mark it, pay particular attention to the data-interpretation questions &mdash; graphic logs, geological maps, and cross-sections &mdash; since these are where unpractised students lose the most marks. Use the result to prioritise which of the five units needs the most retrieval and spaced repetition in the remaining weeks.</p>
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
<p>From 10 weeks out, do at least one timed practice per subject per week &mdash; usually a single section at first, building to full papers. In the final month, do at least one full timed paper per subject. Always mark it against the actual scheme and note your pace.</p>
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
<h4>Build-up schedule</h4>
<ol class="guide-quick-ref-steps">
<li>One question, timed</li>
<li>One section, timed</li>
<li>Half a paper, timed</li>
<li>Full paper, timed</li>
<li>Full paper, exam conditions</li>
<li>Mock week, all papers</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content"><a href="/guide/geology-eduqas/revision-technique/retrieval-practice">Retrieval Practice</a>
<a href="/guide/geology-eduqas/revision-technique/spaced-repetition">Spaced Repetition</a>
<a href="/guide/geology-eduqas/revision-technique/dual-coding">Dual Coding</a>
<a href="/guide/geology-eduqas/revision-technique/elaborative-interrogation">Elaborative Interrogation</a>
<a href="/guide/geology-eduqas/revision-technique/interleaving">Interleaving</a>
<a href="/guide/geology-eduqas/revision-technique/knowledge-organisers">Knowledge Organisers</a></div>
</div>
</div>
</aside>"""
})

# ══════════════════════════════════════════════════════════════
# INSERT
# ══════════════════════════════════════════════════════════════
print(f"Inserting {len(pages)} guide pages for geology-eduqas...")

for page in pages:
    slug = page["slug"]
    # Upsert: delete existing row for this subject+type+slug, then insert
    sb.table("guide_pages").delete().eq("subject_id", GEOLOGY_SUBJECT_ID).eq("guide_type", "revision-technique").eq("slug", slug).execute()
    result = sb.table("guide_pages").insert(page).execute()
    if result.data:
        print(f"  [OK] {slug}")
    else:
        print(f"  [FAIL] {slug} — {result}")

# ══════════════════════════════════════════════════════════════
# VERIFY
# ══════════════════════════════════════════════════════════════
verify = sb.table("guide_pages").select("slug,title,sort_order").eq("subject_id", GEOLOGY_SUBJECT_ID).eq("guide_type", "revision-technique").order("sort_order").execute()
print(f"\nVerification — {len(verify.data)} rows in guide_pages:")
for row in verify.data:
    print(f"  sort_order={row['sort_order']}  slug={row['slug']}  title={row['title']}")
