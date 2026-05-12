"""
Insert 9 revision-technique guide pages for history-ocr (OCR GCSE History J410).
Subject ID: 0ba3a850-1759-410f-97fc-347a78bd5e3a

8 standard guides + 1 history-specific "Source Skills Drill" (OPACT technique).
Source Skills Drill is OCR-specific: Components 1 and 3 both have source
comparison / utility questions — practising OPACT against primary sources from
the period is the single highest-leverage discipline-specific skill.
"""

import os
from supabase import create_client

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_SERVICE_KEY')
sb = create_client(url, key)

SUBJECT_ID = '0ba3a850-1759-410f-97fc-347a78bd5e3a'
GUIDE_TYPE = 'revision-technique'
SLUG = 'history-ocr'

# ── Sidebar "Other Techniques" shared block ───────────────────────────────────
SIDEBAR_OTHER = """<!-- Other Techniques -->
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>📚 Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/retrieval-practice">
<strong>Retrieval Practice</strong>
<span>Active recall</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/spaced-repetition">
<strong>Spaced Repetition</strong>
<span>Scheduling</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/interleaving">
<strong>Interleaving</strong>
<span>Mixed practice</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/dual-coding">
<strong>Dual Coding</strong>
<span>Visual learning</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/elaborative-interrogation">
<strong>Elaborative Interrogation</strong>
<span>Deep thinking</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/knowledge-organisers">
<strong>Knowledge Organisers</strong>
<span>Summarising</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/timed-practice">
<strong>Timed Practice</strong>
<span>Exam readiness</span>
</a>
<a class="sidebar-media-item" href="/guide/history-ocr/revision-technique/source-skills-drill">
<strong>Source Skills Drill</strong>
<span>OPACT technique</span>
</a>
</div>
</div>
</div>"""

VIDEO_BLOCK = """<!-- Video Placeholder -->
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>"""


# ─── 0. HUB (index) ──────────────────────────────────────────────────────────
hub_html = """<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>Evidence-based strategies that actually work. Each technique is backed by cognitive science research and tailored to GCSE History revision.</p>
</div>
</div>
<div class="guide-hub">
<!-- Foundation Techniques -->
<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/retrieval-practice">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself, don't just re-read. Brain dumps and self-quizzing build stronger memories than re-reading your notes ever could.</p>
</a>
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/spaced-repetition">
<span class="guide-question-marks">Scheduling</span>
<h3>Spaced Repetition</h3>
<p>Spread your revision over days and weeks. Short sessions with gaps between them lock historical knowledge into long-term memory.</p>
</a>
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/dual-coding">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>Combine words and visuals to remember more. Timelines, cause-and-consequence flowcharts and comparison tables stick better than text alone.</p>
</a>
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/knowledge-organisers">
<span class="guide-question-marks">Summarising</span>
<h3>Knowledge Organisers</h3>
<p>Condense each topic onto one page. The act of creating it — from memory — is where the learning happens.</p>
</a>
</div>
</div>
<!-- Exam Preparation -->
<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Exam Preparation</h2>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/elaborative-interrogation">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask "why?" and "how?" to deepen understanding. Build causal chains that turn historical facts into exam-ready explanations.</p>
</a>
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/interleaving">
<span class="guide-question-marks">Mixed practice</span>
<h3>Interleaving</h3>
<p>Mix time periods and question types per session. It feels harder, but the research shows it produces stronger recall on exam day.</p>
</a>
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/timed-practice">
<span class="guide-question-marks">Exam readiness</span>
<h3>Timed Practice</h3>
<p>Write like it's the real thing. Practise under timed conditions and self-mark against the mark scheme to build exam technique.</p>
</a>
<a class="guide-question-card" href="/guide/history-ocr/revision-technique/source-skills-drill">
<span class="guide-question-marks">OPACT technique</span>
<h3>Source Skills Drill</h3>
<p>Practise reading primary sources using the OPACT framework — Origin, Purpose, Audience, Content, Tone. The skill that separates good History students from great ones.</p>
</a>
</div>
</div>
</div>"""


# ─── 1. RETRIEVAL PRACTICE ───────────────────────────────────────────────────
retrieval_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Active recall</span>
<h1>Retrieval Practice</h1>
<p class="guide-used-in">Test yourself, don't just re-read</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Retrieval practice means pulling information out of your memory rather than putting it back in. Every time you successfully recall a fact, name, or date, the memory trace becomes stronger. Re-reading your notes feels productive because the information looks familiar — but familiarity is not the same as knowing. History exams reward precise recall of specific dates, key figures, and causal chains: retrieval practice is how you build that precision.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Roediger &amp; Karpicke (2006)</strong></td>
<td>Students who practised retrieval remembered 80% after one week; those who re-read remembered 36%</td>
<td>More than double the retention</td>
</tr>
<tr>
<td><strong>Dunlosky et al. (2013)</strong></td>
<td>Major review of 10 revision strategies rated practice testing as HIGH utility</td>
<td>One of only two top-rated techniques</td>
</tr>
<tr>
<td><strong>Karpicke &amp; Blunt (2011)</strong></td>
<td>Retrieval practice outperformed concept mapping for learning complex texts</td>
<td>Works for narrative subjects, not just science</td>
</tr>
<tr>
<td><strong>EEF Cognitive Science Report (2021)</strong></td>
<td>Recommended retrieval practice as one of six key principles for effective learning</td>
<td>Endorsed for UK classroom use</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Read one topic</strong> — Spend 5 minutes reading through a single lesson. Don't highlight yet — just read to understand.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Close your notes</strong> — Put everything away. No peeking. This is the moment where learning happens.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Brain dump on a blank page</strong> — Write down everything you can recall: dates, names, causes, consequences, historians' arguments. Aim for 5–8 minutes.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Check and highlight gaps</strong> — Open your notes and compare. Use a different colour to fill in anything you missed. These gaps are your priority for next session.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Repeat on the gaps</strong> — Next session, focus your retrieval attempt on the parts you couldn't remember. Keep cycling until the gaps are gone.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 28%;">Read<br/>5 min</span>
<span style="background: #22c55e; width: 44%;">Brain dump<br/>8 min</span>
<span style="background: #4ade80; width: 28%;">Check gaps<br/>5 min</span>
</div>
<p>One full cycle takes about 18 minutes. Do 2–3 cycles per revision session, covering different topics. Use retrieval practice every time you revise — it should be your default method, not an occasional extra.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Cuban Missile Crisis Brain Dump</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph guide-weak-answer">
<span class="guide-annotation guide-annotation-weak">First attempt — from memory only</span>
<p>The Cuban Missile Crisis was in 1962. Khrushchev put missiles in Cuba. Kennedy found out from a spy plane and set up a blockade. They nearly went to war but eventually Khrushchev agreed to remove the missiles. Kennedy secretly agreed not to invade Cuba and to remove missiles from somewhere in Europe.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">After checking — gaps filled in green</span>
<p>The Cuban Missile Crisis lasted thirteen days in <strong>October 1962</strong>. Khrushchev placed Soviet missiles in Cuba, partly to deter a second US invasion after the <strong>Bay of Pigs failure (April 1961)</strong>. Kennedy was informed on <strong>14 October</strong> when U-2 reconnaissance photographs confirmed missile sites. His ExComm advisers debated air strikes and invasion; Kennedy chose a <strong>naval quarantine</strong> instead. <strong>Black Saturday (27 October)</strong> was the most dangerous moment — a U-2 was shot down over Cuba and a US Navy submarine was depth-charged. The crisis resolved when Khrushchev agreed to withdraw missiles in exchange for a public US pledge not to invade Cuba and a <strong>secret agreement to remove Jupiter missiles from Turkey</strong>. The hotline between Washington and Moscow followed in <strong>1963</strong>.</p>
</div>
<p><strong>What this reveals:</strong> The first attempt had the outline but missed ExComm, Black Saturday, the Jupiter missile deal and the 1963 hotline. These details become the focus of the next retrieval cycle.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Re-reading instead of recalling</strong> — Reading your notes five times feels like revision but barely strengthens memory. Close the book and test yourself.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Peeking at notes too soon</strong> — The struggle to remember is the point. If you look the moment you get stuck, you skip the part that builds memory.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Only testing what you already know</strong> — It feels good to recall easy facts, but the real gains come from practising the topics you find hardest.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Not returning to the same topic</strong> — One brain dump is a start, not the finish. You need to revisit each topic multiple times at increasing intervals (see Spaced Repetition).</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<div></div>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/spaced-repetition">Spaced Repetition →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 28%;" title="Read: 5 min"></span>
<span style="background: #22c55e; width: 44%;" title="Brain dump: 8 min"></span>
<span style="background: #4ade80; width: 28%;" title="Check gaps: 5 min"></span>
</div>
<span class="guide-quick-ref-total">18 min per cycle</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Read one topic</li>
<li>Close your notes</li>
<li>Brain dump from memory</li>
<li>Check and highlight gaps</li>
<li>Repeat on the gaps</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 2. SPACED REPETITION ────────────────────────────────────────────────────
spaced_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Scheduling</span>
<h1>Spaced Repetition</h1>
<p class="guide-used-in">Spread it out over days and weeks</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Your brain forgets things on a predictable curve. Hermann Ebbinghaus discovered this in 1885: without review, you lose about 70% of new information within 24 hours. But each time you revisit material at the right moment — just as you're about to forget — the memory becomes stronger and lasts longer. History is a content-heavy subject: with 12 units and over 117 lessons across different centuries and continents, spacing is the only practical strategy that gets everything into long-term memory before exam day.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Ebbinghaus (1885)</strong></td>
<td>Discovered the forgetting curve — memory decays exponentially without review</td>
<td>Foundation of all spacing research</td>
</tr>
<tr>
<td><strong>Cepeda et al. (2006)</strong></td>
<td>Meta-analysis of 254 studies confirmed spacing produces stronger long-term retention than massing</td>
<td>Effect holds across ages and subjects</td>
</tr>
<tr>
<td><strong>Dunlosky et al. (2013)</strong></td>
<td>Distributed practice rated HIGH utility across all learning contexts</td>
<td>One of only two top-rated techniques</td>
</tr>
<tr>
<td><strong>Bjork &amp; Bjork (1992)</strong></td>
<td>"Desirable difficulties" — spacing feels harder but produces deeper learning</td>
<td>Explains why cramming feels effective but isn't</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>List all your topics</strong> — Write out every lesson across your units. You have around 117 lessons — group them by unit to manage the volume.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Build a 6-week timetable</strong> — Start at least 6 weeks before your exam. Schedule 2–3 topics per day, 30–45 minutes per session.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Schedule at increasing intervals</strong> — After studying a topic, revisit it at Day 1, Day 3, Day 7, Day 14, then Day 30. Each review gets shorter because you remember more.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Traffic-light after each test</strong> — After each retrieval attempt, rate the topic: <strong style="color: #16a34a;">Green</strong> (confident), <strong style="color: #f59e0b;">Amber</strong> (some gaps), <strong style="color: #dc2626;">Red</strong> (major gaps). Reds get shorter intervals.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Adjust your spacing</strong> — Move green topics to longer gaps (14–30 days). Keep red topics on short cycles (1–3 days) until they become amber or green.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 16%;">Day 1<br/>Study</span>
<span style="background: #22c55e; width: 16%;">Day 2<br/>Review</span>
<span style="background: #4ade80; width: 16%;">Day 4<br/>Review</span>
<span style="background: #86efac; width: 20%;">Day 8<br/>Review</span>
<span style="background: #bbf7d0; color: #14532d; width: 32%;">Day 22<br/>Review</span>
</div>
<p>Plan once, then follow the schedule daily. Each review session uses retrieval practice (brain dumps or self-quizzing) — not re-reading. Start 6–8 weeks before your exam to give every topic at least 4 review cycles.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: 6-Week Schedule for Soweto Uprising</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Week 1 — Initial study + Day 1 review</span>
<p><strong>Monday:</strong> Study the Soweto Uprising for 20 minutes. Brain dump key facts: Afrikaans Medium Decree (1974), 16 June 1976, Hector Pieterson killed, Steve Biko dies in police custody September 1977, BCM organisations banned October 1977, approximately 600–700 deaths in the protest wave.</p>
<p><strong>Tuesday:</strong> 10-minute retrieval — write down everything from yesterday. Rate: <strong style="color: #f59e0b;">Amber</strong> (forgot the BCM ban date and Tsietsi Mashinini's role as student leader).</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Week 2 — Day 7 review</span>
<p><strong>Monday:</strong> 8-minute retrieval. Now confident on the main chronology and key figures. Can also connect Biko's death to the Anti-Apartheid Movement's growing international pressure. Rate: <strong style="color: #16a34a;">Green</strong>. Move to 14-day gap.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Week 4 — Day 21 review</span>
<p><strong>Monday:</strong> 5-minute retrieval. Still solid. Quick check confirms all key content intact — including the Sam Nzima photograph as a source the exam might use. Rate: <strong style="color: #16a34a;">Green</strong>. Final review scheduled for exam week.</p>
</div>
<p><strong>Total time on this topic:</strong> about 53 minutes across 6 weeks — far more effective than one 53-minute cram the night before.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Cramming the night before</strong> — Massed practice creates short-term familiarity that fades within days. Spacing the same total time across weeks produces lasting memory.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Revising the same topic every day</strong> — Daily repetition of the same material gives diminishing returns. Space it out and use the gaps to cover other units.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Ignoring weaker topics</strong> — It is tempting to keep reviewing what you already know. Use the traffic-light system to force yourself back to red topics.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Starting too late</strong> — Spacing only works if you start early enough to fit in multiple review cycles. Six weeks is the minimum; eight is better.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/retrieval-practice">← Retrieval Practice</a>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/interleaving">Interleaving →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 16%;" title="Day 1: Study"></span>
<span style="background: #22c55e; width: 16%;" title="Day 2: Review"></span>
<span style="background: #4ade80; width: 16%;" title="Day 4: Review"></span>
<span style="background: #86efac; width: 20%;" title="Day 8: Review"></span>
<span style="background: #bbf7d0; width: 32%;" title="Day 22: Review"></span>
</div>
<span class="guide-quick-ref-total">Ongoing — plan once, daily sessions</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>List all topics</li>
<li>Build 6-week timetable</li>
<li>Schedule at increasing intervals</li>
<li>Traffic-light each topic</li>
<li>Adjust spacing by confidence</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 3. INTERLEAVING ─────────────────────────────────────────────────────────
interleaving_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Mixed practice</span>
<h1>Interleaving</h1>
<p class="guide-used-in">Mix topics and question types in one session</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Most students revise one topic until they feel confident, then move on to the next. This "blocked practice" feels effective but produces fragile knowledge — you can recall a topic immediately after studying it, but the memory fades quickly. Interleaving means deliberately mixing topics, time periods, and question types within a single session. It feels harder, which is exactly why it works: your brain has to retrieve and distinguish between different bodies of knowledge, and that effort builds stronger, more durable memories.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Rohrer &amp; Taylor (2007)</strong></td>
<td>Students who interleaved topics scored 43% higher on delayed tests than those who blocked</td>
<td>Large effect on long-term retention</td>
</tr>
<tr>
<td><strong>Kornell &amp; Bjork (2008)</strong></td>
<td>Interleaving improved category learning — students could identify new examples better</td>
<td>Builds transferable pattern recognition</td>
</tr>
<tr>
<td><strong>Pan et al. (2019)</strong></td>
<td>Interleaving produced durable learning even when students initially felt less confident</td>
<td>Counteracts the "illusion of knowing"</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Pick three topics from different units</strong> — Choose one topic from your period study, one from your depth study, and one from your thematic study. Make sure you have already studied all three at least once.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Set 12-minute blocks</strong> — Spend exactly 12 minutes on each topic, then switch — even if you feel like you haven't finished. The switch is the point.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Use retrieval in each block</strong> — Don't re-read. Brain dump what you know, answer a practice question, or reconstruct a timeline from memory.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Mix question types too</strong> — In one session, do a short outline answer, a source-analysis paragraph, and a cause-and-consequence explanation. Variety in question type mirrors what the real exam will demand.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Review gaps at the end</strong> — After the session, note one gap from each topic. These become priorities for the next session's retrieval.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 33%;">Topic A<br/>12 min</span>
<span style="background: #22c55e; width: 33%;">Topic B<br/>12 min</span>
<span style="background: #4ade80; width: 34%;">Topic C<br/>12 min</span>
</div>
<p>A 36-minute session covers three topics with meaningful retrieval on each. Use interleaving for consolidation sessions — after you have studied all the topics in a unit at least once. Early in your revision, blocked practice helps you learn new content; later on, interleaving locks it in.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Period Study + Depth Study + Thematic Study</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Block A — 12 minutes on International Relations (period study)</span>
<p>Brain dump the reasons Kennedy chose a naval blockade over an air strike during the Cuban Missile Crisis. List: legality of quarantine vs air strike; risk of Soviet casualties in a strike; advice split in ExComm (General Taylor vs McNamara); time for Khrushchev to back down without humiliation. Check notes. Missing: the role of Robert Kennedy in pushing for the blockade option. Add to gap list.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Block B — 12 minutes on Germany 1925–1955 (depth study)</span>
<p>Practice question: explain two reasons why the Nazi Party's support grew rapidly between 1929 and 1932. Write two PEEL paragraphs (Point–Evidence–Explain–Link). Check against notes — one paragraph needs a specific election percentage (37.3% in July 1932). Add to gap list.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Block C — 12 minutes on Migration to Britain (thematic study)</span>
<p>Reconstruct a timeline of migration to Spitalfields from memory: Huguenots (1685 onwards) → Irish (early 1800s) → Eastern European Jews (1880s–1914) → Bangladeshi community (1970s onwards). Focus on the Brick Lane building that was in turn a Huguenot chapel, a synagogue, then a mosque — the single most exam-relevant architectural symbol for the thematic study.</p>
</div>
<p><strong>Why this works:</strong> Switching between a Cold War crisis, Nazi electoral history, and London migration history forces you to organise and distinguish three completely different bodies of knowledge. That retrieval effort is what builds durable memory.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Treating feeling confused as a sign it isn't working</strong> — Interleaving is supposed to feel harder. The difficulty is the mechanism; it is not a sign to go back to blocked practice.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Mixing topics you haven't studied yet</strong> — Interleaving works for consolidation, not first learning. Study each topic in a unit before you start mixing it with others.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Re-reading instead of retrieving in each block</strong> — The power of interleaving comes from retrieval, not from flicking between different sets of notes.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Only mixing within one time period</strong> — History exams cover multiple eras. Mix across your period study, depth study, and thematic study to mirror real exam demands.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/spaced-repetition">← Spaced Repetition</a>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/dual-coding">Dual Coding →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 33%;" title="Topic A: 12 min"></span>
<span style="background: #22c55e; width: 33%;" title="Topic B: 12 min"></span>
<span style="background: #4ade80; width: 34%;" title="Topic C: 12 min"></span>
</div>
<span class="guide-quick-ref-total">36 min for 3 topics</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Pick 3 topics from different units</li>
<li>Set 12-minute blocks</li>
<li>Use retrieval in each block</li>
<li>Mix question types too</li>
<li>Review gaps at the end</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 4. DUAL CODING ──────────────────────────────────────────────────────────
dual_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Visual learning</span>
<h1>Dual Coding</h1>
<p class="guide-used-in">Combine words and visuals to remember more</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Your brain processes words and images through separate channels. When you encode information in both — reading about a cause and also drawing a flowchart — you create two memory pathways instead of one. If one pathway fades, the other can still retrieve the information. History is particularly suited to dual coding: timelines, cause-and-consequence chains, comparison tables and annotated maps all translate naturally into visual formats that reinforce factual knowledge.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Paivio (1971)</strong></td>
<td>Dual coding theory — information stored in both verbal and visual memory is recalled better than either alone</td>
<td>Foundational theory for visual learning</td>
</tr>
<tr>
<td><strong>Mayer (2009)</strong></td>
<td>Multimedia learning principles — people learn better from words and pictures together than from words alone</td>
<td>Words + visuals outperform words only</td>
</tr>
<tr>
<td><strong>Clark &amp; Paivio (1991)</strong></td>
<td>Dual coding consistently enhanced learning across different tasks, ages, and content types</td>
<td>Works for narrative and analytical subjects</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Pick a topic</strong> — Choose one lesson or a key concept. Read through it to refresh your memory.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Identify the structure</strong> — What kind of information is this? Causes leading to one event → flowchart. A sequence of events → annotated timeline. Two regimes to compare → table with columns. Long-term change → change-and-continuity graph.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Choose the right visual format</strong> — Match the format to the content. A chain of escalating crises needs a flowchart; the spread of Soviet control across Eastern Europe needs a labelled map; comparing two depth study options needs a table.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Draw it from memory</strong> — Close your notes and create the visual from what you remember. Use short labels (3–5 words max) and arrows to show connections.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Check and annotate</strong> — Open your notes and fill in anything you missed using a different colour. Add brief annotations explaining WHY each connection exists.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 20%;">Read<br/>5 min</span>
<span style="background: #22c55e; width: 12%;">Plan<br/>3 min</span>
<span style="background: #4ade80; width: 44%;">Draw<br/>12 min</span>
<span style="background: #86efac; width: 24%;">Check<br/>5 min</span>
</div>
<p>One visual takes about 25 minutes to create properly. Create 1–2 per revision session. Your visuals become revision tools in later sessions — try to recreate them from memory as a retrieval exercise.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Road to War 1930–1939 Flowchart</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Step 1: identify structure — this is a cause-and-consequence chain</span>
<p>The tensions of the 1930s involve a sequence of crises that build on each other. A flowchart shows the escalation clearly — each event weakens the League or emboldens Hitler, making the next crisis more likely.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Step 2: flowchart drawn from memory</span>
<p><strong>1931 — Manchuria crisis</strong> (League fails to act) → <strong>1935 — Abyssinia invaded</strong> (League issues sanctions but they fail) → <strong>1936 — Rhineland remilitarised</strong> (Britain and France back down) → <strong>1938 — Anschluss with Austria</strong> (no response) → <strong>Sept 1938 — Munich Agreement</strong> (Sudetenland given to Hitler) → <strong>Mar 1939 — Czechoslovakia dismembered</strong> → <strong>Aug 1939 — Nazi-Soviet Pact</strong> → <strong>1 Sept 1939 — Poland invaded</strong></p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">After checking — additions in a different colour</span>
<p>Missing: the <strong>1936 Spanish Civil War</strong> as Germany and Italy's military testing ground; the <strong>1937 Neville Chamberlain becomes PM</strong> (appeasement peaks); a note that <strong>examiner reports warn against mixing 1920s and 1930s crises</strong> — Vilna, Corfu and Aaland are not part of this chain.</p>
</div>
<p><strong>Why this works:</strong> The flowchart makes the escalation pattern visible. In your exam essay you can mentally picture the chain and use each box as a linked paragraph of evidence.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Too much text on visuals</strong> — If your diagram has full sentences, it's just notes in boxes. Keep labels to 3–5 words and let the structure do the work.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Copying instead of drawing from memory</strong> — Looking at your notes while drawing defeats the purpose. Close them first, then check. Gaps in your diagram reveal gaps in your knowledge.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Using the wrong format</strong> — Don't draw a flowchart for content that is really a comparison. Match the visual format to the structure of the knowledge.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Drawing once and never returning to it</strong> — In later sessions, try to recreate your visual from memory without looking at the original. The recreation attempt is as valuable as the original drawing.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/interleaving">← Interleaving</a>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/elaborative-interrogation">Elaborative Interrogation →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 20%;" title="Read: 5 min"></span>
<span style="background: #22c55e; width: 12%;" title="Plan: 3 min"></span>
<span style="background: #4ade80; width: 44%;" title="Draw: 12 min"></span>
<span style="background: #86efac; width: 24%;" title="Check: 5 min"></span>
</div>
<span class="guide-quick-ref-total">25 min per visual</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Pick a topic</li>
<li>Identify the structure</li>
<li>Choose the right format</li>
<li>Draw it from memory</li>
<li>Check and annotate</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 5. ELABORATIVE INTERROGATION ────────────────────────────────────────────
elaborative_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Deep thinking</span>
<h1>Elaborative Interrogation</h1>
<p class="guide-used-in">Ask "why?" and "how?" to deepen understanding</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Most students revise by memorising facts: dates, names, events. But History exams reward <em>explanation</em> — you need to say WHY things happened and HOW one event connects to another. Elaborative interrogation forces you to ask these questions during revision, which builds the deeper understanding that turns a basic recall answer into a top-band response. For OCR History in particular, the high-mark questions (25-mark essays, the 24-mark change-and-continuity essay) all demand causal chains, not lists of facts.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Pressley et al. (1987)</strong></td>
<td>Students who asked "why?" while reading recalled 72% of material vs. 37% for those who just read</td>
<td>Nearly double the recall</td>
</tr>
<tr>
<td><strong>Dunlosky et al. (2013)</strong></td>
<td>Elaborative interrogation rated MODERATE utility — highly effective when students already have background knowledge</td>
<td>Ideal for revision, not first learning</td>
</tr>
<tr>
<td><strong>Chi et al. (1994)</strong></td>
<td>Self-explanation — explaining material to yourself — produced better learning than simply studying examples</td>
<td>Explaining builds understanding</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Read a section of your notes</strong> — Pick one lesson or part of a lesson. Read through it once to remind yourself of the content.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Stop at each key fact</strong> — Every time you hit an important cause, consequence, or turning point, pause. Don't just move on.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Ask "Why?" or "How?"</strong> — Why did this happen? How does it connect to what came before? Why did this decision have this consequence? How might historians disagree about its significance?</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Answer from memory first</strong> — Try to explain the answer in your own words before checking your notes. Write it down in one or two sentences.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Build a causal chain</strong> — Link your "why" answers together: A happened because of B, which led to C, which caused D. This is exactly the structure the 25-mark essays reward.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">6</span>
<div class="guide-step-body"><strong>Self-test</strong> — Close your notes and try to reconstruct the causal chain from memory. Check for gaps.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 20%;">Read<br/>3 min</span>
<span style="background: #22c55e; width: 40%;">Why/How<br/>6 min</span>
<span style="background: #4ade80; width: 26%;">Chain<br/>4 min</span>
<span style="background: #86efac; width: 14%;">Test<br/>2 min</span>
</div>
<p>Each topic takes about 15 minutes with this method. Use it after you have already studied a topic at least once — you need some background knowledge for the "why" questions to work. Best combined with retrieval practice: do a brain dump first, then use elaborative interrogation on the parts you recalled.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Why Did Nazi Support Collapse Between November 1932 and January 1933?</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Fact → Why question → Answer</span>
<p><strong>Fact:</strong> Nazi vote share fell from 37.3% in July 1932 to 33.1% in November 1932, yet Hitler became Chancellor in January 1933.</p>
<p><strong>Why?</strong> Why did Nazi support fall just before Hitler came to power?</p>
<p><strong>Answer:</strong> By late 1932, some voters who had backed the Nazis in protest during the crisis years began to look elsewhere as the most acute economic panic eased. The Nazi Party was also running short of money and showing internal strain. This drop was a warning sign that the window of opportunity was narrowing.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Building the causal chain</span>
<p><strong>How</strong> did Hitler become Chancellor despite falling support? → Elite miscalculation: von Papen persuaded President Hindenburg that Hitler could be controlled as Chancellor with conservatives holding most cabinet posts. Papen thought he could use Hitler's mass movement while keeping power himself.</p>
<p><strong>Why</strong> did that calculation prove wrong? → Hitler quickly outmanoeuvred the conservatives — the Reichstag Fire Decree (28 February 1933) and the Enabling Act (23 March 1933) removed constitutional constraints before the conservatives could reassert themselves.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Complete causal chain</span>
<p>Electoral fatigue → Nazi vote falls November 1932 → fear of window closing → Papen–Hitler deal → Hindenburg appoints Hitler Chancellor 30 January 1933 → Reichstag Fire → Enabling Act → dictatorship secured</p>
</div>
<p><strong>Why this works:</strong> Instead of just memorising "Hitler appointed 30 January 1933", you now understand the political mechanism — exactly what the "explain why" and essay questions demand.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Only asking "what" questions</strong> — "What happened at Munich?" tests recall but doesn't build understanding. Always push to "why" and "how".</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Accepting vague answers</strong> — "Because things got worse" is not an explanation. Push yourself to give specific causal reasons with named evidence.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Skipping the self-test</strong> — Building the causal chain is only half the work. You need to close your notes and reconstruct it from memory to lock it in.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Not connecting across lessons</strong> — The best causal chains link events from different topics. The Great Depression connects to Nazi rise, which connects to appeasement, which connects to the outbreak of war.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/dual-coding">← Dual Coding</a>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/knowledge-organisers">Knowledge Organisers →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 20%;" title="Read: 3 min"></span>
<span style="background: #22c55e; width: 40%;" title="Why/How: 6 min"></span>
<span style="background: #4ade80; width: 26%;" title="Chain: 4 min"></span>
<span style="background: #86efac; width: 14%;" title="Test: 2 min"></span>
</div>
<span class="guide-quick-ref-total">15 min per topic</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Read a section</li>
<li>Stop at each key fact</li>
<li>Ask "Why?" / "How?"</li>
<li>Answer from memory</li>
<li>Build causal chain</li>
<li>Self-test the chain</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 6. KNOWLEDGE ORGANISERS ─────────────────────────────────────────────────
ko_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Summarising</span>
<h1>Knowledge Organisers</h1>
<p class="guide-used-in">Structure knowledge into single pages</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>A knowledge organiser (KO) is a single A4 page that captures the essential facts, dates, names, and concepts for one topic. The act of creating it — deciding what counts as essential and laying it out from memory — is far more valuable than reading a pre-made version. For History, KOs are especially powerful because you can test yourself by covering one column at a time: dates → events, events → causes, names → roles. The constraint of a single page forces you to prioritise, which is itself an exam skill.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Ausubel (1960)</strong></td>
<td>Advance organisers — structured summaries given before learning — significantly improved retention</td>
<td>Structure aids encoding and retrieval</td>
</tr>
<tr>
<td><strong>Kornell &amp; Bjork (2007)</strong></td>
<td>Creating study materials from memory outperforms reading pre-made materials for long-term retention</td>
<td>Making it yourself is part of the learning</td>
</tr>
<tr>
<td><strong>EEF Metacognition Report (2018)</strong></td>
<td>Self-regulation strategies — including summarising and planning — rated high utility for GCSE-age students</td>
<td>Endorsed for secondary classroom</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Pick one topic or lesson</strong> — One A4 page covers one lesson or one sub-section. Don't try to fit a whole unit onto one page.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Draw the structure first</strong> — Divide your page into sections: Key Dates, Key People, Key Events, Causes, Consequences, Historians' Views. Adjust the sections to fit the topic.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Fill it from memory</strong> — Close your notes and fill in as much as you can. Use bullet points, short phrases, and dates — not full sentences.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Check and add in a different colour</strong> — Open your notes. Add anything you missed in a contrasting colour. These additions show exactly what you didn't know.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Test yourself using the KO</strong> — Cover one column. Say the hidden information aloud or write it on a scrap of paper. Repeat with different columns covered.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 15%;">Structure<br/>5 min</span>
<span style="background: #22c55e; width: 45%;">Fill from memory<br/>15 min</span>
<span style="background: #4ade80; width: 25%;">Check &amp; add<br/>8 min</span>
<span style="background: #86efac; width: 15%;">Test<br/>5 min</span>
</div>
<p>One KO takes about 33 minutes to create properly. Build them gradually — one or two per session — so that by exam time you have a full set for every unit. Recreate them from memory in your final revision week as a high-intensity retrieval exercise.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Dissolution of the Monasteries Knowledge Organiser</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">KO structure for the English Reformation unit</span>
<p><strong>Key Dates</strong> | 1535 — Valor Ecclesiasticus; 1536 — First Suppression Act; Oct 1536 — Lincolnshire Rising; Oct 1536–Feb 1537 — Pilgrimage of Grace; 1539 — Second Suppression Act; 1540 — Glastonbury (last major house closed)</p>
<p><strong>Key People</strong> | Thomas Cromwell (directed dissolution); Richard Layton and Thomas Legh (royal visitors); Robert Aske (Pilgrimage of Grace leader); Abbot Richard Whiting (executed 1539)</p>
<p><strong>Causes</strong> | Henry needed money; Cromwell wanted reform; visitors compiled Comperta reports on monastic "abuses"; opportunity to reward loyal nobles with land grants</p>
<p><strong>Consequences</strong> | c.825 monasteries dissolved; monks pensioned or dispersed; social provision (hospitals, schools) disrupted for the poor; land redistributed to nobility and gentry; cultural loss (libraries, art)</p>
<p><strong>Resistance</strong> | Pilgrimage of Grace — largest rebellion of the century; 30,000 marchers in north England; Pontefract Articles (Oct 1536); Henry pardoned then executed leaders after second rising (1537)</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Self-test — cover the right-hand column</span>
<p>Cover everything to the right of the pipe symbols. Say or write the answers from memory before uncovering. Focus the next session on any row where you hesitated.</p>
</div>
<p><strong>Why this works:</strong> The KO forces you to decide what is essential — a decision that embeds the knowledge. Testing yourself column by column converts the KO into a self-quizzing tool.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Downloading or printing a pre-made KO</strong> — Reading someone else's KO is passive. Making your own from memory is where the learning happens.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Writing full sentences</strong> — KOs should be dense with facts, not paragraphs. If you're writing full sentences, you're making notes, not a knowledge organiser.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Never testing yourself with the KO</strong> — Creating the KO is only half the value. Cover columns and quiz yourself to convert it into a retrieval practice tool.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Trying to fit too much on one page</strong> — If you can't read it clearly, it won't help you. One lesson or sub-topic per page is the right scope.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/elaborative-interrogation">← Elaborative Interrogation</a>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/timed-practice">Timed Practice →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 15%;" title="Structure: 5 min"></span>
<span style="background: #22c55e; width: 45%;" title="Fill from memory: 15 min"></span>
<span style="background: #4ade80; width: 25%;" title="Check &amp; add: 8 min"></span>
<span style="background: #86efac; width: 15%;" title="Test: 5 min"></span>
</div>
<span class="guide-quick-ref-total">33 min per knowledge organiser</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Pick one topic</li>
<li>Draw the structure</li>
<li>Fill from memory</li>
<li>Check and add in different colour</li>
<li>Test using covered columns</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 7. TIMED PRACTICE ───────────────────────────────────────────────────────
timed_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Exam readiness</span>
<h1>Timed Practice</h1>
<p class="guide-used-in">Simulated exam conditions</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Knowing the content is not the same as being able to perform under exam conditions. Many students enter their History exam having never written an answer under timed pressure — and then discover on the day that they run out of time or freeze. Timed practice is the only way to build the exam-day skills that knowledge alone cannot give you: pacing, structure, decision-making under pressure, and the habit of starting to write even when you don't feel fully ready.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Butler &amp; Roediger (2007)</strong></td>
<td>Students who practised on exam-like questions performed significantly better on real exams than those who studied without testing</td>
<td>Practice testing transfers to real performance</td>
</tr>
<tr>
<td><strong>Rawson &amp; Dunlosky (2011)</strong></td>
<td>The format of practice matters — practising in the same conditions as the test maximises transfer</td>
<td>Exam-like practice beats generic revision</td>
</tr>
<tr>
<td><strong>EEF Metacognition Report (2018)</strong></td>
<td>Self-monitoring and self-assessment strategies rated high utility for GCSE-age students</td>
<td>Marking your own work builds awareness</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Choose the question type</strong> — Pick a question that matches your exam: a 5-mark outline, 10-mark explain, 25-mark essay, or 24-mark change-and-continuity essay. Know the mark allocation before you start.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Set a strict timer</strong> — A general rule for History is: 1 minute per mark. So a 10-mark question gets 10 minutes; a 25-mark essay gets 25 minutes. Set the timer before you pick up your pen.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Plan for 2 minutes</strong> — Spend the first 2 minutes making a brief plan: key argument, main evidence points, counter-argument. Write it in your answer booklet, then cross it through when done.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Write, don't stop</strong> — Once you start, keep writing. If you get stuck, move to your next point and come back. The examiner rewards what is on the page, not what was in your head.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Self-mark against the mark scheme</strong> — After the timer, look up the mark scheme criteria. Highlight any level descriptor that matches what you wrote. Be honest: if you didn't provide specific evidence, you can't claim the marks for it.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">6</span>
<div class="guide-step-body"><strong>Identify one improvement</strong> — Write one sentence at the bottom of your answer: what single change would move you up one mark level? Implement it in your next attempt.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 8%;">Plan<br/>2 min</span>
<span style="background: #22c55e; width: 70%;">Write<br/>marks × 1 min</span>
<span style="background: #4ade80; width: 22%;">Mark<br/>5 min</span>
</div>
<p>Do at least one timed answer per revision session in the final four weeks before your exam. Start with shorter questions (5–10 marks) to build fluency, then move to full essay questions (24–25 marks). Keep every timed answer in a folder — comparing early and late attempts is one of the most motivating things you can do.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: 25-Mark Essay on Yalta, Potsdam and the Origins of the Cold War</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">2-minute plan (written on scrap, then crossed through)</span>
<p><strong>Question:</strong> "The Soviet Union was entirely responsible for the origins of the Cold War." How far do you agree with this interpretation?</p>
<p><strong>Plan:</strong> Agree — Soviet salami tactics, Berlin Blockade, expansionism 1945–48. Disagree — US atomic diplomacy, Truman Doctrine as provocative containment, revisionist historians (Williams). Counter — post-revisionist (Gaddis): both powers share responsibility but USSR's actions in Eastern Europe were the immediate trigger. Conclusion: Partially agree — USSR's actions were the proximate cause but US policy escalated tensions. Schools: Orthodox vs Revisionist vs Post-revisionist.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Self-marking against mark scheme level descriptors</span>
<p><strong>L4 (21–25):</strong> Sustained analytical argument, detailed factual support, considers multiple interpretations, deploys scholars/schools by name. → Check: Did I name Gaddis and Williams? Did I use specific dates (Yalta Feb 1945, Potsdam Jul 1945, Czech coup Feb 1948)? Did I actually reach a judgement, or did I just list both sides?</p>
<p><strong>Improvement for next attempt:</strong> I listed the historiographic schools but did not quote a specific phrase from either. Next time, include one line from each school's core argument to show I understand the position, not just the label.</p>
</div>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Not using a timer</strong> — Practising without timing yourself is not timed practice. The constraint of time is the point; without it, you're just writing an essay.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Only practising questions you feel confident about</strong> — Avoid easy questions in timed practice. The ones that feel hardest are the ones where timed pressure will hit you on exam day.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Not self-marking honestly</strong> — Giving yourself full marks because you "roughly covered" the points doesn't help. Apply the level descriptors strictly — that's how the actual examiner will read it.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Leaving timed practice to the last week</strong> — You need enough attempts to see genuine improvement. Start timed practice at least four weeks before your exam.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/knowledge-organisers">← Knowledge Organisers</a>
<a class="guide-nav-link guide-nav-next" href="/guide/history-ocr/revision-technique/source-skills-drill">Source Skills Drill →</a>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 8%;" title="Plan: 2 min"></span>
<span style="background: #22c55e; width: 70%;" title="Write: 1 min per mark"></span>
<span style="background: #4ade80; width: 22%;" title="Mark: 5 min"></span>
</div>
<span class="guide-quick-ref-total">Marks × 1 min + 7 min</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Choose the question type</li>
<li>Set a strict timer (1 min per mark)</li>
<li>Plan for 2 minutes</li>
<li>Write — don't stop</li>
<li>Self-mark against mark scheme</li>
<li>Identify one improvement</li>
</ol>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── 8. SOURCE SKILLS DRILL (OCR-specific) ───────────────────────────────────
source_html = """
<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">OPACT technique</span>
<h1>Source Skills Drill</h1>
<p class="guide-used-in">Practise OPACT against primary sources from the period</p>
</div>
<div class="guide-section">
<h2>Why Source Skills Matter for This Qualification</h2>
<p>Source analysis appears in multiple sections of this qualification. In the period study and depth study components, utility questions ask you to evaluate how useful a source is as evidence. In the British depth study, a 25-mark essay requires you to integrate two sources into an extended argument. The skill that unlocks both is the ability to read beyond a source's content to its <strong>Origin, Purpose, Audience, Content, and Tone</strong> — the OPACT framework. Most students can describe what a source says; the higher bands reward students who can explain why the source says what it says and what that tells a historian about its value and its limits.</p>
<h3>The OPACT Framework</h3>
<table class="guide-levels">
<thead>
<tr><th>Letter</th><th>Question to ask</th><th>What to look for</th></tr>
</thead>
<tbody>
<tr>
<td><strong>O — Origin</strong></td>
<td>Who created this, when, and where?</td>
<td>Author's identity, date, country, context of production</td>
</tr>
<tr>
<td><strong>P — Purpose</strong></td>
<td>Why was this created?</td>
<td>To persuade, inform, record, entertain, justify, celebrate, condemn</td>
</tr>
<tr>
<td><strong>A — Audience</strong></td>
<td>Who was it made for?</td>
<td>Public audience, private diary, government official, foreign power, own supporters</td>
</tr>
<tr>
<td><strong>C — Content</strong></td>
<td>What does it actually say or show?</td>
<td>Specific details, claims, omissions — what is not said can be as revealing as what is</td>
</tr>
<tr>
<td><strong>T — Tone</strong></td>
<td>What is the emotional register?</td>
<td>Angry, celebratory, defensive, neutral, propagandistic, fearful</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Drill Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Find a short primary source</strong> — Textbook sources, past paper sources, or any document from the period you are studying. Aim for 50–100 words of text or one image/poster. You need just one source per 15-minute drill.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Read or study it for 2 minutes</strong> — Resist the urge to write immediately. Read the source at least twice. Underline or circle specific phrases that seem significant.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Work through OPACT in writing</strong> — Write one or two sentences for each letter. Do not skip any — even if you feel the Audience entry is short, write something. Each letter trains a different analytical habit.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Write a utility sentence</strong> — Combine your OPACT notes into one exam-style sentence: "This source is useful for studying [topic] because [specific content point] and because its [origin/purpose] means the author had [reason to be reliable/reason to have biases]."</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Check against the examiner's mark scheme</strong> — Look at the mark scheme for a utility question. Does your response make an inference from the source's content? Does it address provenance? Both are required for the higher bands.</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #16a34a; width: 14%;">Read<br/>2 min</span>
<span style="background: #22c55e; width: 52%;">OPACT notes<br/>8 min</span>
<span style="background: #4ade80; width: 20%;">Utility sentence<br/>3 min</span>
<span style="background: #86efac; width: 14%;">Check<br/>2 min</span>
</div>
<p>One drill takes about 15 minutes. Do one source per session, targeting sources from different time periods and different types (political speech, propaganda poster, private letter, official report, newspaper extract). Over six weeks of twice-weekly drills, you will have practised OPACT on around twelve different sources — enough to build genuine fluency.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Applying OPACT to a Nazi Propaganda Poster</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Source: a 1936 NSDAP election poster showing a strong male figure above the slogan "Ein Volk, Ein Reich, Ein Führer" with a swastika flag in the background</span>
<p><strong>Origin:</strong> Produced by the Reich Ministry of Public Enlightenment and Propaganda under Joseph Goebbels, 1936. This places it after the consolidation of power (Enabling Act 1933) but before the outbreak of war — during the period when the regime was projecting unity and strength for internal and international audiences.</p>
<p><strong>Purpose:</strong> To reinforce the Führerprinzip — the idea that Hitler embodied the will of the German nation. The poster aims to manufacture consensus and present opposition as un-German.</p>
<p><strong>Audience:</strong> Primarily the German public. The visual format (poster) and simple slogan suggest a mass audience, including less literate viewers. The aesthetic of strength would appeal to the Volksgemeinschaft ideal.</p>
<p><strong>Content:</strong> The slogan "One People, One Reich, One Leader" directly links national unity to Hitler's personal leadership. The absence of any political programme or policy argument is deliberate — the message is emotional, not rational. The swastika flag frames this as a statement of identity.</p>
<p><strong>Tone:</strong> Triumphalist, unifying, authoritarian. The tone excludes — implicitly, those who are not part of "Ein Volk" (Jews, Roma, political opponents) do not exist in this image's world.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Exam-style utility sentence</span>
<p>This source is useful for studying how the Nazi regime used propaganda to maintain support because its content directly illustrates the Führerprinzip ideology that underpinned Hitler's personal popularity (as described by Ian Kershaw's "Hitler Myth" thesis); however, as a piece of official government propaganda designed for mass consumption, it tells us more about the image the regime wanted to project than about genuine popular opinion — it cannot be used to measure actual levels of support.</p>
</div>
<p><strong>Why this works:</strong> The utility sentence makes an inference from the content (Führerprinzip), links to a named historian (Kershaw), and then addresses the provenance limitation — exactly the structure the mark scheme rewards at the top band.</p>
</div>
</div>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Applying OPACT to a Cold War Speech</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Source: an extract from Khrushchev's letter to Kennedy during the Cuban Missile Crisis, 26 October 1962</span>
<p><strong>Origin:</strong> Written by Soviet Premier Nikita Khrushchev on 26 October 1962 — the 12th day of the crisis, one day before Black Saturday. This is a private diplomatic communication, not a public speech.</p>
<p><strong>Purpose:</strong> To propose a negotiated settlement (withdrawal of Soviet missiles in exchange for a US pledge not to invade Cuba) while avoiding public humiliation for either side.</p>
<p><strong>Audience:</strong> Kennedy alone initially, though Khrushchev would have known that historians and future leaders might eventually read it. The private audience is significant: Khrushchev could be more flexible in private than he could in public.</p>
<p><strong>Content:</strong> The letter uses emotional language ("do not pull the knot of war tighter") and appeals to shared responsibility for humanity. It implicitly acknowledges that both sides must back down, not just the USSR.</p>
<p><strong>Tone:</strong> Urgent, almost pleading — notably different from the public bluster of Khrushchev's earlier statements in the crisis. The private tone suggests Khrushchev was genuinely alarmed.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Exam-style utility sentence</span>
<p>This source is useful for studying the resolution of the Cuban Missile Crisis because as a private diplomatic communication it reveals Khrushchev's genuine fear of escalation more honestly than his public statements — the pleading tone suggests the Soviet leadership was not as confident as their public posture implied; its limitation as evidence is that it reflects only Khrushchev's perspective on Day 12 and cannot tell us about the internal debates within the Kremlin or the role of the Jupiter missile deal in shaping his offer.</p>
</div>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Describing the source instead of analysing it</strong> — "The source says that Khrushchev was worried" is description. "The emotional tone of Khrushchev's letter suggests he was more alarmed than his public statements indicate" is analysis. Push beyond the surface.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Treating provenance as a standard disclaimer</strong> — "This source is biased because it is propaganda" earns no marks. You need to explain specifically how the purpose shapes the content and what that means for the source's value as evidence.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Ignoring the Content letter</strong> — Many students focus entirely on Origin and Purpose and neglect to quote or reference specific phrases from the source itself. Examiners expect you to make inferences from the actual text.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">❌</span>
<div><strong>Only practising sources from one topic</strong> — OPACT is a transferable analytical skill, but you need to apply it across different time periods, source types, and contexts to build genuine fluency. Vary your practice.</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="/guide/history-ocr/revision-technique/timed-practice">← Timed Practice</a>
<div></div>
</nav>
<a class="back-link" href="/guide/history-ocr/revision-technique">← Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 14%;" title="Read: 2 min"></span>
<span style="background: #22c55e; width: 52%;" title="OPACT notes: 8 min"></span>
<span style="background: #4ade80; width: 20%;" title="Utility sentence: 3 min"></span>
<span style="background: #86efac; width: 14%;" title="Check: 2 min"></span>
</div>
<span class="guide-quick-ref-total">15 min per source</span>
<h4>OPACT</h4>
<ol class="guide-quick-ref-steps">
<li><strong>O</strong>rigin — who, when, where</li>
<li><strong>P</strong>urpose — why was this made</li>
<li><strong>A</strong>udience — who for</li>
<li><strong>C</strong>ontent — what does it say</li>
<li><strong>T</strong>one — emotional register</li>
</ol>
<h4>Utility sentence structure</h4>
<p style="font-size: 0.85rem; line-height: 1.5;">Useful for [topic] because [content point] + because [origin/purpose shapes reliability] + limitation: [what it cannot tell us]</p>
</div>
""" + VIDEO_BLOCK + SIDEBAR_OTHER + """
</aside>"""


# ─── INSERT ALL ROWS ─────────────────────────────────────────────────────────
rows = [
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "index",
        "title": "Revision Techniques",
        "content_html": hub_html,
        "sort_order": 0,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "retrieval-practice",
        "title": "Retrieval Practice",
        "content_html": retrieval_html,
        "sort_order": 1,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "spaced-repetition",
        "title": "Spaced Repetition",
        "content_html": spaced_html,
        "sort_order": 2,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "interleaving",
        "title": "Interleaving",
        "content_html": interleaving_html,
        "sort_order": 3,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "dual-coding",
        "title": "Dual Coding",
        "content_html": dual_html,
        "sort_order": 4,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "elaborative-interrogation",
        "title": "Elaborative Interrogation",
        "content_html": elaborative_html,
        "sort_order": 5,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "knowledge-organisers",
        "title": "Knowledge Organisers",
        "content_html": ko_html,
        "sort_order": 6,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "timed-practice",
        "title": "Timed Practice",
        "content_html": timed_html,
        "sort_order": 7,
    },
    {
        "subject_id": SUBJECT_ID,
        "guide_type": GUIDE_TYPE,
        "slug": "source-skills-drill",
        "title": "Source Skills Drill",
        "content_html": source_html,
        "sort_order": 8,
    },
]

print(f"Inserting {len(rows)} revision-technique guides for history-ocr...")

for row in rows:
    result = (
        sb.table("guide_pages")
        .upsert(row, on_conflict="subject_id,guide_type,slug")
        .execute()
    )
    print(f"  OK {row['slug']} (sort_order {row['sort_order']})")

print(f"\nDone. {len(rows)} rows inserted/upserted.")
print("Hub URL: https://www.studyvault.co.uk/guide/history-ocr/revision-technique")
