"""
Insert revision technique guide pages for AQA Science (Combined + Separate Sciences).
9 pages: 1 hub + 8 technique guides.
Both subject_slugs share identical content.
"""

import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from scripts.lib.supabase_client import get_client

SCIENCE_ID = "02c2e32f-d2db-4eac-a5d4-f55973a2e31a"
SEPARATE_ID = "a9cc3d43-c51b-4ea9-aa15-0977d1b0daee"

# Accent colour for science guides
ACCENT = "#2563eb"
ACCENT_LIGHT = "#eff6ff"

# ── Hub page ──────────────────────────────────────────────────────────────────

HUB_HTML = f"""<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>Evidence-based strategies that actually work. Each technique is backed by cognitive science research and tailored to AQA Science revision &mdash; covering Biology, Chemistry, and Physics.</p>
</div>
</div>
<div class="guide-hub">
<!-- Foundation Techniques -->
<div class="guide-paper" style="--paper-accent: {ACCENT}; --paper-light: {ACCENT_LIGHT};">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these throughout your revision</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="retrieval-practice.html">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself, don&rsquo;t just re-read. Brain dumps and self-quizzing beat highlighting every time &mdash; essential for recalling equations, definitions, and processes under exam pressure.</p>
</a>
<a class="guide-question-card" href="spaced-repetition.html">
<span class="guide-question-marks">Scheduling</span>
<h3>Spaced Repetition</h3>
<p>Spread it out over days and weeks. Short sessions with gaps between them lock knowledge of chemical reactions, biological processes, and physics laws into long-term memory.</p>
</a>
<a class="guide-question-card" href="active-recall-flashcards.html">
<span class="guide-question-marks">Terminology</span>
<h3>Active Recall with Flashcards</h3>
<p>Science is packed with precise terminology &mdash; mitosis, electrolysis, specific heat capacity. Master definitions and key facts with systematic flashcard drilling.</p>
</a>
<a class="guide-question-card" href="mind-maps-diagrams.html">
<span class="guide-question-marks">Visual learning</span>
<h3>Mind Maps and Diagrams</h3>
<p>Combine words and visuals. Labelled cell diagrams, circuit symbols, and reaction pathways stick far better than text alone &mdash; and AQA expects you to draw them.</p>
</a>
</div>
</div>
<!-- Science-Specific Techniques -->
<div class="guide-paper" style="--paper-accent: {ACCENT}; --paper-light: {ACCENT_LIGHT};">
<div class="guide-paper-header">
<h2>Science-Specific Techniques</h2>
<span class="guide-paper-ref">Strategies designed for AQA Science revision</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="equation-practice-calculations.html">
<span class="guide-question-marks">Maths skills</span>
<h3>Equation Practice and Calculations</h3>
<p>Physics equations, chemistry calculations, and biology data analysis &mdash; at least 20% of your marks depend on mathematical skills. Practise rearranging, substituting, and using standard form.</p>
</a>
<a class="guide-question-card" href="required-practicals.html">
<span class="guide-question-marks">Practical skills</span>
<h3>Required Practicals Revision</h3>
<p>AQA has 21 required practicals across Biology, Chemistry, and Physics. You must know the method, variables, hazards, and how to evaluate results for each one.</p>
</a>
</div>
</div>
<!-- Exam Preparation -->
<div class="guide-paper" style="--paper-accent: {ACCENT}; --paper-light: {ACCENT_LIGHT};">
<div class="guide-paper-header">
<h2>Exam Preparation</h2>
<span class="guide-paper-ref">Final weeks before the exam &mdash; sharpen and apply</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="timed-practice-questions.html">
<span class="guide-question-marks">Exam readiness</span>
<h3>Practice Questions Under Timed Conditions</h3>
<p>Write like it&rsquo;s the real thing. Practise under timed conditions and self-mark against AQA mark schemes to understand exactly what examiners are looking for.</p>
</a>
<a class="guide-question-card" href="exam-paper-walkthroughs.html">
<span class="guide-question-marks">Strategy</span>
<h3>Exam Paper Walkthroughs</h3>
<p>Work through complete past papers question by question, analysing mark schemes and examiner reports to understand exactly how marks are awarded.</p>
</a>
</div>
</div>
</div>"""


# ── 1. Retrieval Practice ─────────────────────────────────────────────────────

RETRIEVAL_PRACTICE_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Active recall</span>
<h1>Retrieval Practice</h1>
<p class="guide-used-in">Test yourself, don&rsquo;t just re-read</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Retrieval practice means pulling information out of your memory rather than putting it back in. Every time you successfully recall a fact, the memory trace gets stronger. Re-reading your notes feels productive, but it creates a false sense of confidence &mdash; the information looks familiar without actually being learned. For Science, where you need to recall equations, definitions, processes, and experimental methods under exam pressure, retrieval practice is essential.</p>
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
<td>Retrieval practice outperformed concept mapping for learning science texts</td>
<td>Works even for complex scientific material</td>
</tr>
<tr>
<td><strong>EEF Cognitive Science Report (2021)</strong></td>
<td>Recommended retrieval practice as one of six key principles for effective learning</td>
<td>Endorsed for UK classroom use</td>
</tr>
</tbody>
</table>
</div>
<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Read one topic</strong> &mdash; Spend 5 minutes reading through a single topic, such as cell structure, bonding, or energy transfers. Don&rsquo;t highlight or make notes yet &mdash; just read to understand.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Close your notes</strong> &mdash; Put everything away. No peeking. This is the crucial moment where learning actually happens.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Brain dump on a blank page</strong> &mdash; Write down everything you can remember about the topic. Include key terms, equations, diagrams, processes, and examples. Use bullet points, sketches, or tables &mdash; whatever comes to mind. Aim for 5&ndash;8 minutes.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Check and highlight gaps</strong> &mdash; Open your notes and compare. Use a different colour pen to fill in anything you missed or got wrong. These gaps are your priority for next time.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Repeat on the gaps</strong> &mdash; Next session, focus your retrieval attempt on the parts you couldn&rsquo;t remember. Keep cycling until the gaps are filled.
</div>
</li>
</ol>
</div>
<!-- Section 3: When and How Often -->
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 28%;">Read<br/>5 min</span>
<span style="background: #3b82f6; width: 44%;">Brain dump<br/>8 min</span>
<span style="background: #60a5fa; width: 28%;">Check gaps<br/>5 min</span>
</div>
<p>One full cycle takes about 18 minutes. Do 2&ndash;3 cycles per revision session, covering different topics. Use retrieval practice every time you revise &mdash; it should be your default method, not an occasional extra.</p>
</div>
<!-- Section 4: Worked Example (COLLAPSIBLE) -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Cell Biology Brain Dump</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph guide-weak-answer">
<span class="guide-annotation guide-annotation-weak">First attempt &mdash; from memory only</span>
<p>Cells have a nucleus, cell membrane, and cytoplasm. Plant cells also have a cell wall and chloroplasts. Mitosis is cell division. DNA is in the nucleus. Cells need energy from respiration&hellip;</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">After checking &mdash; gaps filled in green</span>
<p>Cells have a nucleus <strong>(contains genetic material as chromosomes)</strong>, cell membrane <strong>(selectively permeable, controls what enters and leaves)</strong>, and cytoplasm <strong>(where most chemical reactions take place)</strong>. Plant cells also have a cell wall <strong>(made of cellulose, provides structural support)</strong>, chloroplasts <strong>(contain chlorophyll for photosynthesis)</strong>, <strong>and a permanent vacuole (filled with cell sap, maintains turgor pressure)</strong>. Mitosis is cell division <strong>(produces two genetically identical diploid daughter cells; stages: prophase, metaphase, anaphase, telophase)</strong>. DNA is in the nucleus <strong>(as a double helix; DNA is a polymer of nucleotides)</strong>. Cells need energy from respiration <strong>(aerobic: glucose + oxygen &rarr; carbon dioxide + water; C&#8326;H&#8321;&#8322;O&#8326; + 6O&#8322; &rarr; 6CO&#8322; + 6H&#8322;O)</strong>.</p>
</div>
<p><strong>What this reveals:</strong> The first attempt had the right structures but missed specific functions, the stages of mitosis, the equation for aerobic respiration, and the permanent vacuole. These gaps become the focus of the next retrieval attempt.</p>
</div>
</div>
</div>
<!-- Section 5: Quick-Fire Questions (COLLAPSIBLE) -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Quick-Fire Science Retrieval Questions</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<p>Use these to test yourself without notes. Cover the answers, then check:</p>
<ul>
<li>Name the three states of matter and describe the particle arrangement in each.</li>
<li>Write the word equation and balanced symbol equation for photosynthesis.</li>
<li>What are the differences between ionic, covalent, and metallic bonding?</li>
<li>State Newton&rsquo;s three laws of motion and give an example of each.</li>
<li>Name three types of specialised cell and explain how each is adapted to its function.</li>
<li>What is the reactivity series? List the first five metals in order.</li>
<li>Describe the structure of the atom, including the charges and masses of subatomic particles.</li>
<li>Write the equation for calculating speed, and rearrange it to find distance.</li>
<li>Explain the difference between aerobic and anaerobic respiration.</li>
<li>What happens during electrolysis of an ionic compound?</li>
</ul>
</div>
</div>
</div>
<!-- Section 6: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Re-reading instead of recalling</strong> &mdash; Reading your notes five times feels like revision but barely strengthens memory. Close the book and test yourself.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Peeking at notes too soon</strong> &mdash; The struggle to remember is the point. If you look at your notes the moment you get stuck, you skip the part that builds memory.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Only testing what you already know</strong> &mdash; It feels good to recall photosynthesis perfectly, but the real gains come from practising the topics you find hardest &mdash; like balancing equations or remembering the reactivity series.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Not returning to the same topic</strong> &mdash; One brain dump is a start, not the finish. You need to revisit each topic multiple times at increasing intervals (see Spaced Repetition).
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<div></div>
<a class="guide-nav-link guide-nav-next" href="spaced-repetition.html">Spaced Repetition &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 28%;" title="Read: 5 min"></span>
<span style="background: #3b82f6; width: 44%;" title="Brain dump: 8 min"></span>
<span style="background: #60a5fa; width: 28%;" title="Check gaps: 5 min"></span>
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
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 2. Spaced Repetition ──────────────────────────────────────────────────────

SPACED_REPETITION_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Scheduling</span>
<h1>Spaced Repetition</h1>
<p class="guide-used-in">Spread it out over days and weeks</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Spaced repetition is the practice of reviewing material at gradually increasing intervals. Instead of cramming everything the night before, you revisit topics after 1 day, then 3 days, then 7 days, then 14 days. Each time you revisit, the memory gets stronger and lasts longer. For Science, where you need to retain hundreds of definitions, equations, and processes across Biology, Chemistry, and Physics, spacing is the difference between short-term cramming and genuine understanding.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Ebbinghaus (1885)</strong></td>
<td>Without review, 70% of information is forgotten within 24 hours</td>
<td>Forgetting is rapid without spacing</td>
</tr>
<tr>
<td><strong>Cepeda et al. (2006)</strong></td>
<td>Spacing study sessions produced 10&ndash;30% better recall than massed practice</td>
<td>Consistent across all subjects</td>
</tr>
<tr>
<td><strong>Dunlosky et al. (2013)</strong></td>
<td>Distributed practice rated as HIGH utility &mdash; one of only two top-rated strategies</td>
<td>Strong evidence across hundreds of studies</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Create a topic list</strong> &mdash; Write out every topic you need to revise for each paper (Biology Paper 1, Chemistry Paper 2, etc.). Use the AQA specification checklist to make sure nothing is missed.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Assign topics to days</strong> &mdash; Spread topics across your revision calendar. Don&rsquo;t do all of Biology in one week &mdash; interleave Biology, Chemistry, and Physics topics each day.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Use the 1-3-7-14 rule</strong> &mdash; After first learning a topic, review it after 1 day, then 3 days, then 7 days, then 14 days. Each review can be shorter than the last &mdash; a 5-minute retrieval quiz is enough for the later reviews.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Mark confidence levels</strong> &mdash; After each review, rate the topic as Red (can&rsquo;t remember), Amber (partial recall), or Green (solid). Red topics get reviewed sooner; green topics can be spaced further apart.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Track with a revision timetable</strong> &mdash; Use a calendar, spreadsheet, or app (Anki is excellent for flashcards with built-in spacing). Colour-code by subject so you can see the balance at a glance.
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 40%;">Day 1: Learn<br/>20 min</span>
<span style="background: #3b82f6; width: 20%;">Day 2: Review<br/>10 min</span>
<span style="background: #60a5fa; width: 20%;">Day 4: Review<br/>5 min</span>
<span style="background: #93c5fd; width: 20%;">Day 8+: Quick test<br/>5 min</span>
</div>
<p>Start spacing at least 8 weeks before the exam. The earlier you begin, the more review cycles you can fit in. Even 10 minutes a day on previously covered topics makes a huge difference.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Two-Week Spacing Plan</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead>
<tr><th>Day</th><th>New Topic</th><th>Review Topics</th></tr>
</thead>
<tbody>
<tr><td>Mon Week 1</td><td>Cell structure (Bio)</td><td>&mdash;</td></tr>
<tr><td>Tue Week 1</td><td>Atomic structure (Chem)</td><td>Cell structure (Day 1)</td></tr>
<tr><td>Wed Week 1</td><td>Energy stores (Phys)</td><td>&mdash;</td></tr>
<tr><td>Thu Week 1</td><td>Cell division (Bio)</td><td>Cell structure (Day 3), Atomic structure (Day 1)</td></tr>
<tr><td>Fri Week 1</td><td>Bonding (Chem)</td><td>Energy stores (Day 1)</td></tr>
<tr><td>Mon Week 2</td><td>Waves (Phys)</td><td>Cell structure (Day 7), Cell division (Day 3), Bonding (Day 1)</td></tr>
<tr><td>Fri Week 2</td><td>Infection (Bio)</td><td>Cell structure (Day 14), Atomic structure (Day 7), Energy stores (Day 7)</td></tr>
</tbody>
</table>
<p><strong>Notice:</strong> By Week 2, you are reviewing 3&ndash;4 old topics alongside each new one. This overlap is normal and keeps everything fresh.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Cramming the night before</strong> &mdash; Massed practice feels productive but fades fast. Spaced practice feels harder in the moment but lasts much longer.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Only revising one subject per day</strong> &mdash; Doing &ldquo;all Biology on Monday&rdquo; reduces the spacing effect. Mix subjects within each session.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Skipping the hard topics</strong> &mdash; The topics you find hardest need more frequent review, not less. Use your RAG ratings to prioritise.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="retrieval-practice.html">&#8592; Retrieval Practice</a>
<a class="guide-nav-link guide-nav-next" href="active-recall-flashcards.html">Active Recall with Flashcards &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 40%;" title="Day 1: Learn 20 min"></span>
<span style="background: #3b82f6; width: 20%;" title="Day 2: Review 10 min"></span>
<span style="background: #60a5fa; width: 20%;" title="Day 4: Review 5 min"></span>
<span style="background: #93c5fd; width: 20%;" title="Day 8+: Quick test 5 min"></span>
</div>
<span class="guide-quick-ref-total">1-3-7-14 day intervals</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Create a topic list</li>
<li>Assign topics to days</li>
<li>Use the 1-3-7-14 rule</li>
<li>Mark confidence (RAG)</li>
<li>Track with a timetable</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 3. Active Recall with Flashcards ──────────────────────────────────────────

ACTIVE_RECALL_FLASHCARDS_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Terminology</span>
<h1>Active Recall with Flashcards</h1>
<p class="guide-used-in">Master definitions, equations, and key facts</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Flashcards force active recall &mdash; you see a prompt and must generate the answer from memory before flipping the card. This is far more effective than passively reading definitions. Science is terminology-heavy: you need precise definitions (osmosis, electrolysis, electromagnetic induction), equations (for Physics calculations), and factual knowledge (functions of organelles, properties of groups in the periodic table). Flashcards are the most efficient way to drill this material.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Kornell (2009)</strong></td>
<td>Students who used flashcards with spacing scored significantly higher than those who studied notes</td>
<td>Flashcards + spacing is a powerful combination</td>
</tr>
<tr>
<td><strong>Dunlosky et al. (2013)</strong></td>
<td>Practice testing (including flashcards) rated HIGH utility for long-term retention</td>
<td>Works across all subjects and age groups</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Create cards by topic</strong> &mdash; Group your flashcards by topic (e.g. &ldquo;B1 Cell Biology&rdquo;, &ldquo;C5 Chemical Changes&rdquo;, &ldquo;P7 Electromagnetism&rdquo;). Put a question or term on the front and the answer on the back. Keep answers concise &mdash; no more than 2&ndash;3 bullet points.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Include different card types</strong> &mdash; Mix definitions (&ldquo;What is osmosis?&rdquo;), equations (&ldquo;Write the equation for GPE&rdquo;), processes (&ldquo;Describe the stages of mitosis&rdquo;), and application cards (&ldquo;Why does ice float?&rdquo;). Variety prevents rote memorisation without understanding.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Say the answer out loud before flipping</strong> &mdash; This is crucial. Looking at the back too quickly turns flashcards into passive re-reading. Force yourself to produce an answer, even if it&rsquo;s wrong.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Sort into three piles</strong> &mdash; After each session, sort cards into Got It, Nearly, and Not Yet. Next session, start with Not Yet, then Nearly, then a quick run through Got It to maintain confidence.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Use Anki or Quizlet for digital spacing</strong> &mdash; Apps like Anki automatically schedule cards using spaced repetition algorithms. Cards you get wrong appear more frequently; cards you know well appear less often.
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 35%;">Create cards<br/>15 min</span>
<span style="background: #3b82f6; width: 40%;">Drill session<br/>15 min</span>
<span style="background: #60a5fa; width: 25%;">Sort &amp; review<br/>5 min</span>
</div>
<p>Spend 15 minutes creating cards, then 15&ndash;20 minutes drilling. Do short flashcard sessions daily &mdash; 10 minutes on the bus, 15 minutes before bed. Little and often beats long marathon sessions.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Example Flashcards for Each Science</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<h3>Biology</h3>
<table class="guide-levels">
<thead><tr><th>Front</th><th>Back</th></tr></thead>
<tbody>
<tr><td>Define osmosis</td><td>The diffusion of water from a dilute solution to a concentrated solution through a partially permeable membrane</td></tr>
<tr><td>Name 4 subcellular structures found only in plant cells</td><td>Cell wall, chloroplasts, permanent vacuole, (some have) plasmodesmata</td></tr>
<tr><td>What is the role of the mitochondria?</td><td>Site of aerobic respiration &mdash; where most energy is released from glucose</td></tr>
</tbody>
</table>
<h3>Chemistry</h3>
<table class="guide-levels">
<thead><tr><th>Front</th><th>Back</th></tr></thead>
<tbody>
<tr><td>What is an ionic bond?</td><td>Transfer of electrons from a metal to a non-metal, forming oppositely charged ions held by electrostatic attraction</td></tr>
<tr><td>Reactivity series: top 5 metals</td><td>Potassium, Sodium, Lithium, Calcium, Magnesium (Please Stop Licking Cold Magnets)</td></tr>
<tr><td>What is a catalyst?</td><td>A substance that increases the rate of a reaction without being used up; it provides an alternative reaction pathway with lower activation energy</td></tr>
</tbody>
</table>
<h3>Physics</h3>
<table class="guide-levels">
<thead><tr><th>Front</th><th>Back</th></tr></thead>
<tbody>
<tr><td>Write the equation for kinetic energy</td><td>KE = &frac12; &times; m &times; v&sup2;</td></tr>
<tr><td>State Newton&rsquo;s Second Law</td><td>Force = mass &times; acceleration (F = ma). The acceleration is proportional to the resultant force and inversely proportional to mass.</td></tr>
<tr><td>What is specific heat capacity?</td><td>The amount of energy needed to raise the temperature of 1 kg of a substance by 1&deg;C. Equation: &Delta;E = mc&Delta;&theta;</td></tr>
</tbody>
</table>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Making cards too detailed</strong> &mdash; A card with a paragraph-long answer becomes passive reading. Keep answers to 1&ndash;3 key points.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Only making definition cards</strong> &mdash; Definitions are useful, but you also need cards for equations, processes, practical methods, and application questions.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Flipping too quickly</strong> &mdash; You must attempt an answer before flipping. The effort of retrieval is what builds the memory.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="spaced-repetition.html">&#8592; Spaced Repetition</a>
<a class="guide-nav-link guide-nav-next" href="mind-maps-diagrams.html">Mind Maps and Diagrams &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 35%;" title="Create cards: 15 min"></span>
<span style="background: #3b82f6; width: 40%;" title="Drill session: 15 min"></span>
<span style="background: #60a5fa; width: 25%;" title="Sort &amp; review: 5 min"></span>
</div>
<span class="guide-quick-ref-total">35 min per session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Create cards by topic</li>
<li>Mix card types</li>
<li>Say answer before flipping</li>
<li>Sort into 3 piles</li>
<li>Use Anki for digital spacing</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 4. Mind Maps and Diagrams ─────────────────────────────────────────────────

MIND_MAPS_DIAGRAMS_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Visual learning</span>
<h1>Mind Maps and Diagrams</h1>
<p class="guide-used-in">Combine words and visuals to deepen understanding</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Dual coding &mdash; combining verbal and visual information &mdash; creates two memory pathways instead of one. When you draw a diagram of cell structure, you process the information both as text (the labels and descriptions) and as a spatial image (the positions and relationships). This makes the memory stronger and more accessible during exams. In AQA Science, you are often asked to draw, label, or interpret diagrams, so this technique directly improves your exam performance.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Paivio (1986)</strong></td>
<td>Dual coding theory: information encoded both verbally and visually is remembered better than either alone</td>
<td>Two memory traces are stronger than one</td>
</tr>
<tr>
<td><strong>Mayer (2009)</strong></td>
<td>Students learn more deeply from words and pictures than from words alone</td>
<td>Multimedia learning principle</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Identify what to draw</strong> &mdash; Not all topics need diagrams. Focus on: cell structures, organ systems, circuit diagrams, reaction profiles, wave diagrams, the electromagnetic spectrum, the periodic table trends, and practical set-ups.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Draw from memory first</strong> &mdash; Close your notes and sketch the diagram from memory. Label everything you can. This combines dual coding with retrieval practice for maximum effect.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Check and annotate</strong> &mdash; Open your notes and add missing labels, correct errors, and annotate with extra detail (functions, equations, or explanations) in a different colour.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Use mind maps for connections</strong> &mdash; For topics with lots of linked concepts (e.g. &ldquo;Infection and Response&rdquo;), create a mind map with the main topic in the centre and branches for subtopics. Use colour, icons, and arrows to show relationships.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Practise exam-style diagrams</strong> &mdash; AQA expects you to draw circuit diagrams, reaction profiles, ray diagrams, and practical set-ups. Practise these with correct symbols and labels until you can produce them quickly under timed conditions.
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 30%;">Draw from memory<br/>8 min</span>
<span style="background: #3b82f6; width: 35%;">Check &amp; annotate<br/>7 min</span>
<span style="background: #60a5fa; width: 35%;">Mind map links<br/>10 min</span>
</div>
<p>Use this technique whenever a topic has a visual element. Spend 20&ndash;25 minutes per topic. Return to the same diagram a few days later and draw it from memory again to check retention.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Key Diagrams You Must Know for AQA Science</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<h3>Biology</h3>
<ul>
<li>Animal and plant cell structure (with labels and functions)</li>
<li>The lock and key model of enzyme action</li>
<li>The heart (chambers, valves, blood vessels)</li>
<li>The digestive system (organs and their functions)</li>
<li>DNA structure (double helix with base pairs)</li>
<li>Mitosis stages (chromosomes, cell division)</li>
</ul>
<h3>Chemistry</h3>
<ul>
<li>Dot and cross diagrams (ionic and covalent bonding)</li>
<li>Reaction profiles (exothermic and endothermic)</li>
<li>Electrolysis set-up (electrodes, electrolyte, products)</li>
<li>Periodic table trends (atomic radius, reactivity, electronegativity)</li>
<li>Chromatography set-up</li>
</ul>
<h3>Physics</h3>
<ul>
<li>Circuit diagrams (using standard symbols)</li>
<li>Ray diagrams (reflection, refraction, lenses)</li>
<li>The electromagnetic spectrum (order, wavelength, frequency)</li>
<li>Wave diagrams (transverse and longitudinal, amplitude, wavelength)</li>
<li>Sankey diagrams (energy transfers)</li>
<li>Force diagrams (resultant forces, free body diagrams)</li>
</ul>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Copying diagrams instead of drawing from memory</strong> &mdash; Copying is passive. Draw from memory first, then check. The errors you make are the most valuable part.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Making mind maps too decorative</strong> &mdash; Spending 30 minutes on artistic lettering isn&rsquo;t revision. Keep it quick and focus on the content and connections.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Forgetting labels on diagrams</strong> &mdash; An unlabelled diagram earns no marks. Always add labels, units, and annotations.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="active-recall-flashcards.html">&#8592; Active Recall with Flashcards</a>
<a class="guide-nav-link guide-nav-next" href="timed-practice-questions.html">Practice Questions Under Timed Conditions &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 30%;" title="Draw from memory: 8 min"></span>
<span style="background: #3b82f6; width: 35%;" title="Check &amp; annotate: 7 min"></span>
<span style="background: #60a5fa; width: 35%;" title="Mind map links: 10 min"></span>
</div>
<span class="guide-quick-ref-total">25 min per topic</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Identify what to draw</li>
<li>Draw from memory first</li>
<li>Check and annotate</li>
<li>Mind map for connections</li>
<li>Practise exam-style diagrams</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 5. Practice Questions Under Timed Conditions ─────────────────────────────

TIMED_PRACTICE_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Exam readiness</span>
<h1>Practice Questions Under Timed Conditions</h1>
<p class="guide-used-in">Write like it&rsquo;s the real thing</p>
</div>
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Practising under exam conditions trains your brain to retrieve and apply knowledge under pressure. It also builds time management skills &mdash; in AQA Science papers, you have roughly one minute per mark, so a 6-mark question should take about 6 minutes. Without timed practice, students routinely spend too long on low-mark questions and run out of time on the high-value extended responses.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Roediger &amp; Karpicke (2006)</strong></td>
<td>Testing under exam-like conditions improved long-term retention by 50% compared to re-reading</td>
<td>Exam simulation produces real learning</td>
</tr>
<tr>
<td><strong>AQA Chief Examiner Reports</strong></td>
<td>Time management is consistently cited as a reason students underperform &mdash; especially on 6-mark questions</td>
<td>Timed practice directly addresses the most common exam weakness</td>
</tr>
</tbody>
</table>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Choose your question set</strong> &mdash; Start with individual questions on one topic, then build up to full papers. Use AQA past papers, the StudyVault practice questions, or your teacher&rsquo;s question bank.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Set a timer</strong> &mdash; Allow roughly 1 minute per mark. A 1-mark question gets 1 minute; a 6-mark question gets 6 minutes. For a full paper (70 marks in 75 minutes for Higher), that&rsquo;s just over a minute per mark.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Write in exam conditions</strong> &mdash; No notes, no phone, no distractions. Use pen on paper (not a screen). This simulates the real exam environment and trains your handwriting speed.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Self-mark against the mark scheme</strong> &mdash; This is the most important step. Don&rsquo;t just check if your answer is &ldquo;about right&rdquo; &mdash; compare it word by word against the mark scheme. Note which marking points you hit and which you missed.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Rewrite missed questions</strong> &mdash; For any question where you dropped marks, rewrite the answer immediately using the mark scheme as a guide. This corrective feedback cements the correct response.
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 50%;">Timed questions<br/>20 min</span>
<span style="background: #3b82f6; width: 30%;">Self-mark<br/>10 min</span>
<span style="background: #60a5fa; width: 20%;">Rewrite gaps<br/>10 min</span>
</div>
<p>Start with single-topic question sets (20 minutes), then progress to half-papers and full papers in the final weeks. Aim for at least 2 timed sessions per week across all three sciences.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Self-Marking a 6-Mark Question</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<p><strong>Question:</strong> Describe the process of natural selection. [6 marks]</p>
<div class="guide-model-paragraph guide-weak-answer">
<span class="guide-annotation guide-annotation-weak">Student&rsquo;s timed answer (5 minutes)</span>
<p>Animals that are better adapted survive. They pass on their genes. Over time, the species changes. The ones that are not adapted die. This is survival of the fittest.</p>
</div>
<p><strong>Mark scheme check:</strong></p>
<ul>
<li>&#10004; Organisms with advantageous characteristics are more likely to survive (1 mark)</li>
<li>&#10004; They reproduce and pass on genes/alleles (1 mark)</li>
<li>&#10060; <strong>Missing:</strong> Variation exists within a population (1 mark)</li>
<li>&#10060; <strong>Missing:</strong> There is competition for resources (1 mark)</li>
<li>&#10060; <strong>Missing:</strong> Over many generations, the advantageous allele becomes more common (1 mark)</li>
<li>&#10060; <strong>Missing:</strong> This may lead to speciation if populations become isolated (1 mark)</li>
</ul>
<p><strong>Score: 2/6.</strong> The answer has the right idea but misses four specific marking points. Rewrite including: variation, competition, &ldquo;over many generations&rdquo;, and allele frequency change.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Spending too long on low-mark questions</strong> &mdash; A 1-mark question needs a single word or short phrase. Don&rsquo;t write a paragraph.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Skipping the self-marking step</strong> &mdash; Without checking against the mark scheme, you don&rsquo;t know what you&rsquo;re missing. Self-marking is where the learning happens.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Only practising topics you like</strong> &mdash; It feels comfortable answering questions on your favourite topics, but you need to target your weakest areas for the biggest improvement.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="mind-maps-diagrams.html">&#8592; Mind Maps and Diagrams</a>
<a class="guide-nav-link guide-nav-next" href="equation-practice-calculations.html">Equation Practice and Calculations &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 50%;" title="Timed questions: 20 min"></span>
<span style="background: #3b82f6; width: 30%;" title="Self-mark: 10 min"></span>
<span style="background: #60a5fa; width: 20%;" title="Rewrite gaps: 10 min"></span>
</div>
<span class="guide-quick-ref-total">40 min per session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Choose question set</li>
<li>Set timer (1 min/mark)</li>
<li>Write in exam conditions</li>
<li>Self-mark against mark scheme</li>
<li>Rewrite missed questions</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 6. Equation Practice and Calculations ─────────────────────────────────────

EQUATION_PRACTICE_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Maths skills</span>
<h1>Equation Practice and Calculations</h1>
<p class="guide-used-in">At least 20% of your marks depend on maths</p>
</div>
<div class="guide-section">
<h2>Why This Matters</h2>
<p>AQA Science papers allocate at least 20% of marks to mathematical skills. In Physics, this can rise to 40%. You need to recall equations (some are given on the equation sheet, others must be memorised), rearrange them, substitute values with correct units, and present answers to an appropriate number of significant figures. In Chemistry, you&rsquo;ll calculate relative formula masses, moles, concentrations, and atom economy. In Biology, maths questions involve magnification, percentages, and data analysis. Students who don&rsquo;t practise calculations lose easy marks.</p>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Learn which equations must be memorised</strong> &mdash; AQA provides an equation sheet in the exam, but not all equations are on it. For Higher tier Physics, you must memorise equations like F = ma, E = mc&Delta;&theta;, and V = IR. Make flashcards for the &ldquo;recall&rdquo; equations and drill them until automatic.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Practise rearranging</strong> &mdash; Use the formula triangle method or algebraic rearranging. For every equation, practise making each variable the subject. For example: speed = distance &divide; time can become distance = speed &times; time, or time = distance &divide; speed.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Convert units before substituting</strong> &mdash; Always convert to SI units: km to m, g to kg, mA to A, kJ to J, cm&sup2; to m&sup2;. Write the conversion next to the value before substituting into the equation.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Show every step of working</strong> &mdash; Write the equation, substitute values with units, calculate, and state the unit of the answer. Even if the final number is wrong, you can earn marks for correct method.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Check significant figures and standard form</strong> &mdash; Give answers to an appropriate number of significant figures (usually 2 or 3 s.f.) and use standard form for very large or very small numbers (e.g. 3.0 &times; 10&#8312; m/s).
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 30%;">Equation recall<br/>5 min</span>
<span style="background: #3b82f6; width: 40%;">Calculation practice<br/>15 min</span>
<span style="background: #60a5fa; width: 30%;">Check &amp; correct<br/>5 min</span>
</div>
<p>Spend 20&ndash;25 minutes per session. Start with equation recall (flashcards or brain dump), then work through 5&ndash;8 calculation questions. Practise at least 3 times per week &mdash; maths skills fade quickly without regular use.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Key Equations You Must Memorise (AQA Higher)</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<h3>Physics &mdash; Must Recall (not on equation sheet)</h3>
<table class="guide-levels">
<thead><tr><th>Quantity</th><th>Equation</th></tr></thead>
<tbody>
<tr><td>Speed</td><td>v = s &divide; t</td></tr>
<tr><td>Acceleration</td><td>a = &Delta;v &divide; t</td></tr>
<tr><td>Newton&rsquo;s Second Law</td><td>F = m &times; a</td></tr>
<tr><td>Weight</td><td>W = m &times; g</td></tr>
<tr><td>Work done</td><td>W = F &times; s</td></tr>
<tr><td>Kinetic energy</td><td>KE = &frac12; &times; m &times; v&sup2;</td></tr>
<tr><td>GPE</td><td>GPE = m &times; g &times; h</td></tr>
<tr><td>Power</td><td>P = E &divide; t</td></tr>
<tr><td>Efficiency</td><td>Efficiency = useful output &divide; total input</td></tr>
<tr><td>Charge</td><td>Q = I &times; t</td></tr>
<tr><td>Potential difference</td><td>V = I &times; R</td></tr>
<tr><td>Power (electrical)</td><td>P = V &times; I</td></tr>
<tr><td>Energy transferred</td><td>E = Q &times; V</td></tr>
<tr><td>Density</td><td>&rho; = m &divide; V</td></tr>
<tr><td>Specific heat capacity</td><td>&Delta;E = m &times; c &times; &Delta;&theta;</td></tr>
<tr><td>Wave speed</td><td>v = f &times; &lambda;</td></tr>
<tr><td>Pressure</td><td>p = F &divide; A</td></tr>
</tbody>
</table>
<h3>Chemistry &mdash; Key Calculations</h3>
<ul>
<li>Relative formula mass (M<sub>r</sub>) = sum of relative atomic masses</li>
<li>Moles = mass &divide; M<sub>r</sub></li>
<li>Concentration (g/dm&sup3;) = mass &divide; volume</li>
<li>Atom economy = (M<sub>r</sub> of desired product &divide; M<sub>r</sub> of all products) &times; 100</li>
<li>Percentage yield = (actual yield &divide; theoretical yield) &times; 100</li>
</ul>
<h3>Biology &mdash; Key Calculations</h3>
<ul>
<li>Magnification = image size &divide; actual size</li>
<li>Percentage change = (change &divide; original) &times; 100</li>
<li>Mean, median, mode, and range from data tables</li>
</ul>
</div>
</div>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Multi-Step Physics Calculation</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<p><strong>Question:</strong> A 0.5 kg ball is dropped from a height of 12 m. Calculate its speed just before hitting the ground. Assume g = 10 m/s&sup2; and no air resistance. [3 marks]</p>
<div class="guide-model-paragraph">
<span class="guide-annotation">Model answer</span>
<p><strong>Step 1:</strong> GPE lost = m &times; g &times; h = 0.5 &times; 10 &times; 12 = 60 J<br/>
<strong>Step 2:</strong> KE gained = GPE lost = 60 J (conservation of energy)<br/>
<strong>Step 3:</strong> KE = &frac12; &times; m &times; v&sup2; &rarr; v&sup2; = 2 &times; KE &divide; m = 2 &times; 60 &divide; 0.5 = 240 &rarr; v = &radic;240 = <strong>15.5 m/s</strong> (3 s.f.)</p>
</div>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Forgetting unit conversions</strong> &mdash; Using km instead of m, or g instead of kg, gives answers out by factors of 1000. Always convert first.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Not showing working</strong> &mdash; An answer without working earns 0 marks if the number is wrong. Show every step to pick up method marks.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Missing the unit of the answer</strong> &mdash; Always state the unit (J, N, m/s, mol). Marks are often lost for missing units.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="timed-practice-questions.html">&#8592; Practice Questions Under Timed Conditions</a>
<a class="guide-nav-link guide-nav-next" href="required-practicals.html">Required Practicals Revision &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 30%;" title="Equation recall: 5 min"></span>
<span style="background: #3b82f6; width: 40%;" title="Calculation practice: 15 min"></span>
<span style="background: #60a5fa; width: 30%;" title="Check &amp; correct: 5 min"></span>
</div>
<span class="guide-quick-ref-total">25 min per session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Learn which equations to memorise</li>
<li>Practise rearranging</li>
<li>Convert units first</li>
<li>Show every step</li>
<li>Check sig figs &amp; standard form</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 7. Required Practicals Revision ───────────────────────────────────────────

REQUIRED_PRACTICALS_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Practical skills</span>
<h1>Required Practicals Revision</h1>
<p class="guide-used-in">Know the method, variables, hazards, and evaluation for every practical</p>
</div>
<div class="guide-section">
<h2>Why This Matters</h2>
<p>AQA has 21 required practicals across Biology, Chemistry, and Physics (8 Biology, 8 Chemistry, 10 Physics for Separate Sciences; fewer for Combined). Questions about required practicals appear on every paper and can account for 15% of the total marks. You don&rsquo;t repeat the experiments in the exam &mdash; but you must know the method, the variables, the equipment, the hazards, how to improve accuracy, and how to evaluate the results. These are some of the most predictable marks on the paper if you revise them properly.</p>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>List all required practicals</strong> &mdash; Use the AQA specification to create a checklist of every required practical for your course. Tick each one off as you revise it. Don&rsquo;t rely on memory &mdash; use the spec.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>For each practical, write a summary covering</strong> &mdash; (a) Aim: what the practical tests; (b) Method: step-by-step procedure; (c) Variables: independent, dependent, and control variables; (d) Equipment: key apparatus including resolution; (e) Hazards and precautions; (f) Expected results and how to process data; (g) How to improve accuracy and reliability.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Draw the set-up from memory</strong> &mdash; Many practicals require a labelled diagram in the exam. Practise drawing the apparatus set-up with labels until you can do it quickly and accurately.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Answer past paper practical questions</strong> &mdash; AQA reuses practical contexts. Practise questions from past papers that are based on required practicals &mdash; you&rsquo;ll see the same practical tested in different ways.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Learn the key vocabulary</strong> &mdash; Examiners expect precise terminology: &ldquo;reproducible&rdquo; (different people get the same results), &ldquo;repeatable&rdquo; (same person gets same results), &ldquo;resolution&rdquo; (smallest interval on a measuring instrument), &ldquo;anomalous&rdquo; (a result that doesn&rsquo;t fit the pattern).
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 30%;">Summary notes<br/>10 min</span>
<span style="background: #3b82f6; width: 30%;">Draw set-up<br/>5 min</span>
<span style="background: #60a5fa; width: 40%;">Past paper Qs<br/>15 min</span>
</div>
<p>Cover 2&ndash;3 practicals per revision session (30 minutes). Cycle through all 21 over 2&ndash;3 weeks, then review the ones you found hardest.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Full List of AQA Required Practicals</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<h3>Biology</h3>
<ol>
<li>Microscopy &mdash; using a light microscope to observe cells</li>
<li>Microbiology &mdash; effect of antiseptics/antibiotics on bacterial growth</li>
<li>Osmosis &mdash; effect of sugar solutions on plant tissue</li>
<li>Food tests &mdash; testing for starch, glucose, protein, and lipids</li>
<li>Enzymes &mdash; effect of pH on enzyme activity (amylase)</li>
<li>Photosynthesis &mdash; effect of light intensity on rate of photosynthesis</li>
<li>Reaction time &mdash; measuring the effect of a factor on reaction time</li>
<li>Plant responses &mdash; effect of light or gravity on seedling growth</li>
</ol>
<h3>Chemistry</h3>
<ol>
<li>Making salts &mdash; preparation of a pure, dry sample of a soluble salt</li>
<li>Electrolysis &mdash; electrolysis of aqueous solutions</li>
<li>Temperature changes &mdash; investigating exothermic and endothermic reactions</li>
<li>Rates of reaction &mdash; effect of concentration on rate (e.g. sodium thiosulfate)</li>
<li>Chromatography &mdash; separating and identifying substances using paper chromatography</li>
<li>Water purification &mdash; analysis and purification of water samples</li>
<li>Identifying ions &mdash; flame tests and chemical tests for ions</li>
<li>Titration &mdash; finding the concentration of an acid or alkali (Higher/Separate only)</li>
</ol>
<h3>Physics</h3>
<ol>
<li>Specific heat capacity &mdash; measuring the specific heat capacity of a material</li>
<li>Thermal insulation &mdash; investigating the effectiveness of different materials</li>
<li>Resistance &mdash; investigating factors affecting resistance of a wire</li>
<li>I-V characteristics &mdash; for a filament lamp, diode, and fixed resistor</li>
<li>Density &mdash; measuring the density of regular and irregular objects</li>
<li>Force and extension &mdash; investigating Hooke&rsquo;s law</li>
<li>Acceleration &mdash; investigating the effect of force on acceleration</li>
<li>Waves &mdash; measuring the frequency, wavelength, and speed of waves in a ripple tank</li>
<li>Light &mdash; investigating reflection and refraction of light</li>
<li>Radiation &mdash; investigating how the amount of infrared radiation absorbed/emitted depends on surface colour</li>
</ol>
</div>
</div>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Osmosis Practical Summary</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead><tr><th>Component</th><th>Detail</th></tr></thead>
<tbody>
<tr><td><strong>Aim</strong></td><td>Investigate the effect of sugar solution concentration on the mass of potato cylinders</td></tr>
<tr><td><strong>Independent variable</strong></td><td>Concentration of sugar solution (e.g. 0.0, 0.2, 0.4, 0.6, 0.8, 1.0 mol/dm&sup3;)</td></tr>
<tr><td><strong>Dependent variable</strong></td><td>Change in mass of potato cylinder</td></tr>
<tr><td><strong>Control variables</strong></td><td>Volume of solution, size/type of potato cylinder, temperature, time left in solution</td></tr>
<tr><td><strong>Equipment</strong></td><td>Potato, cork borer, balance (0.01 g), boiling tubes, sugar solutions, ruler</td></tr>
<tr><td><strong>Hazard</strong></td><td>Sharp cork borer &mdash; cut away from body on a cutting board</td></tr>
<tr><td><strong>Expected results</strong></td><td>In dilute solutions: potato gains mass (water enters by osmosis). In concentrated solutions: potato loses mass (water leaves by osmosis). At the isotonic point: no change.</td></tr>
<tr><td><strong>Improving accuracy</strong></td><td>Repeat 3 times per concentration and calculate mean. Blot potato dry before weighing. Use same potato for consistency.</td></tr>
</tbody>
</table>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Confusing independent and dependent variables</strong> &mdash; The independent variable is what you change; the dependent variable is what you measure. Get these the wrong way round and you lose marks on the very first line.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Forgetting control variables</strong> &mdash; Every practical has variables that must be kept the same for a fair test. &ldquo;To make it a fair test&rdquo; is not enough &mdash; you must name the specific variables you controlled.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Not mentioning repeats</strong> &mdash; &ldquo;Repeat 3 times and calculate the mean&rdquo; is expected in almost every practical method. It improves reliability and helps identify anomalies.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="equation-practice-calculations.html">&#8592; Equation Practice and Calculations</a>
<a class="guide-nav-link guide-nav-next" href="exam-paper-walkthroughs.html">Exam Paper Walkthroughs &#8594;</a>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 30%;" title="Summary notes: 10 min"></span>
<span style="background: #3b82f6; width: 30%;" title="Draw set-up: 5 min"></span>
<span style="background: #60a5fa; width: 40%;" title="Past paper Qs: 15 min"></span>
</div>
<span class="guide-quick-ref-total">30 min per session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>List all required practicals</li>
<li>Write summary for each</li>
<li>Draw set-up from memory</li>
<li>Answer past paper questions</li>
<li>Learn key vocabulary</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="exam-paper-walkthroughs.html"><strong>Exam Paper Walkthroughs</strong><span>Strategy</span></a>
</div>
</div>
</div>
</aside>"""


# ── 8. Exam Paper Walkthroughs ────────────────────────────────────────────────

EXAM_PAPER_WALKTHROUGHS_HTML = f"""<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Strategy</span>
<h1>Exam Paper Walkthroughs</h1>
<p class="guide-used-in">Work through complete papers to master exam technique</p>
</div>
<div class="guide-section">
<h2>Why This Matters</h2>
<p>Doing individual questions builds knowledge, but only complete paper walkthroughs build exam strategy. A walkthrough means working through an entire past paper, question by question, understanding why each answer earns marks. You learn how AQA structures papers, how topics are tested in different ways, and how to pace yourself across the full 75 minutes. Examiner reports reveal what thousands of students got wrong &mdash; learning from their mistakes prevents you from making the same ones.</p>
</div>
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Gather materials</strong> &mdash; Download a full past paper, the corresponding mark scheme, and the examiner&rsquo;s report from AQA&rsquo;s website. You need all three for a proper walkthrough.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Attempt the paper under timed conditions</strong> &mdash; Set a timer for 75 minutes (Higher tier), close your notes, and write your answers on paper. This gives you a baseline score and highlights which topics you need to revise.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Mark with the mark scheme</strong> &mdash; Go through every question. For each one, circle the marking points you hit and highlight the ones you missed. Calculate your total score and grade boundary.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Read the examiner&rsquo;s report for each question</strong> &mdash; The report tells you what most students got wrong and what examiners were looking for. Note the common misconceptions and the specific phrases that earned marks.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Rewrite your weakest answers</strong> &mdash; Pick the 3&ndash;5 questions where you lost the most marks. Rewrite each answer using the mark scheme as a model. Then close the mark scheme and try again from memory.
</div>
</li>
</ol>
</div>
<div class="guide-section">
<h2>When and How Often</h2>
<div class="guide-timing-bar">
<span style="background: #2563eb; width: 45%;">Attempt paper<br/>75 min</span>
<span style="background: #3b82f6; width: 25%;">Mark &amp; review<br/>30 min</span>
<span style="background: #60a5fa; width: 30%;">Rewrite weak answers<br/>20 min</span>
</div>
<p>Do one full paper walkthrough per subject per week in the final 4&ndash;6 weeks before exams. That&rsquo;s about 2 hours per walkthrough including marking and rewriting. Earlier in your revision, use individual topic questions instead.</p>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>AQA Science Paper Structure</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<h3>Combined Science (Trilogy)</h3>
<table class="guide-levels">
<thead><tr><th>Paper</th><th>Topics</th><th>Time</th><th>Marks</th></tr></thead>
<tbody>
<tr><td>Biology Paper 1</td><td>Cell biology, Organisation, Infection, Bioenergetics</td><td>75 min</td><td>70</td></tr>
<tr><td>Biology Paper 2</td><td>Homeostasis, Inheritance, Ecology</td><td>75 min</td><td>70</td></tr>
<tr><td>Chemistry Paper 1</td><td>Atomic structure, Bonding, Quantitative chemistry, Chemical changes, Energy changes</td><td>75 min</td><td>70</td></tr>
<tr><td>Chemistry Paper 2</td><td>Rates, Organic chemistry, Chemical analysis, Atmosphere, Using resources</td><td>75 min</td><td>70</td></tr>
<tr><td>Physics Paper 1</td><td>Energy, Electricity, Particle model, Atomic structure</td><td>75 min</td><td>70</td></tr>
<tr><td>Physics Paper 2</td><td>Forces, Waves, Electromagnetism</td><td>75 min</td><td>70</td></tr>
</tbody>
</table>
<h3>Question Types</h3>
<ul>
<li><strong>Multiple choice</strong> &mdash; typically 1 mark each, scattered throughout</li>
<li><strong>Short answer</strong> &mdash; 1&ndash;3 marks, test recall and application</li>
<li><strong>Calculation</strong> &mdash; 2&ndash;4 marks, show working for method marks</li>
<li><strong>Extended response</strong> &mdash; 6 marks, need a structured, logical answer</li>
</ul>
</div>
</div>
</div>
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Where to Find Past Papers</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<ul>
<li><strong>AQA website</strong> &mdash; <em>aqa.org.uk</em> &rarr; Subjects &rarr; Science &rarr; Assessment resources (free, official papers)</li>
<li><strong>Your teacher</strong> &mdash; may have additional practice papers or compiled question booklets by topic</li>
<li><strong>Physics &amp; Maths Tutor</strong> &mdash; organised by topic with mark schemes (physicsandmathstutor.com)</li>
</ul>
<p><strong>Important:</strong> Always use the mark scheme and examiner report alongside the paper. The paper alone is only a third of the value.</p>
</div>
</div>
</div>
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Doing papers without marking them</strong> &mdash; The learning happens when you compare your answer to the mark scheme. Unanswered marking is wasted practice.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Ignoring the examiner&rsquo;s report</strong> &mdash; The report tells you exactly what examiners expect. Students who read these consistently outperform those who don&rsquo;t.
</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10060;</span>
<div>
<strong>Starting with full papers too early</strong> &mdash; If you haven&rsquo;t revised the content yet, a full paper is demoralising and inefficient. Build knowledge first with topic-based questions, then progress to full papers.
</div>
</li>
</ul>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="required-practicals.html">&#8592; Required Practicals Revision</a>
<div></div>
</nav>
<a class="back-link" href="index.html">&#8592; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #2563eb; width: 45%;" title="Attempt paper: 75 min"></span>
<span style="background: #3b82f6; width: 25%;" title="Mark &amp; review: 30 min"></span>
<span style="background: #60a5fa; width: 30%;" title="Rewrite: 20 min"></span>
</div>
<span class="guide-quick-ref-total">~2 hours per walkthrough</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Gather paper + mark scheme + report</li>
<li>Attempt under timed conditions</li>
<li>Mark against mark scheme</li>
<li>Read examiner&rsquo;s report</li>
<li>Rewrite weakest answers</li>
</ol>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="active-recall-flashcards.html"><strong>Active Recall with Flashcards</strong><span>Terminology</span></a>
<a class="sidebar-media-item" href="mind-maps-diagrams.html"><strong>Mind Maps and Diagrams</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="timed-practice-questions.html"><strong>Practice Questions Under Timed Conditions</strong><span>Exam readiness</span></a>
<a class="sidebar-media-item" href="equation-practice-calculations.html"><strong>Equation Practice and Calculations</strong><span>Maths skills</span></a>
<a class="sidebar-media-item" href="required-practicals.html"><strong>Required Practicals Revision</strong><span>Practical skills</span></a>
</div>
</div>
</div>
</aside>"""


# ── All guides with metadata ──────────────────────────────────────────────────

GUIDES = [
    {"slug": "index",                       "title": "Revision Techniques",                       "sort_order": 0, "content_html": HUB_HTML},
    {"slug": "retrieval-practice",           "title": "Retrieval Practice",                        "sort_order": 1, "content_html": RETRIEVAL_PRACTICE_HTML},
    {"slug": "spaced-repetition",            "title": "Spaced Repetition",                         "sort_order": 2, "content_html": SPACED_REPETITION_HTML},
    {"slug": "active-recall-flashcards",     "title": "Active Recall with Flashcards",             "sort_order": 3, "content_html": ACTIVE_RECALL_FLASHCARDS_HTML},
    {"slug": "mind-maps-diagrams",           "title": "Mind Maps and Diagrams",                    "sort_order": 4, "content_html": MIND_MAPS_DIAGRAMS_HTML},
    {"slug": "timed-practice-questions",     "title": "Practice Questions Under Timed Conditions", "sort_order": 5, "content_html": TIMED_PRACTICE_HTML},
    {"slug": "equation-practice-calculations","title": "Equation Practice and Calculations",       "sort_order": 6, "content_html": EQUATION_PRACTICE_HTML},
    {"slug": "required-practicals",          "title": "Required Practicals Revision",              "sort_order": 7, "content_html": REQUIRED_PRACTICALS_HTML},
    {"slug": "exam-paper-walkthroughs",      "title": "Exam Paper Walkthroughs",                   "sort_order": 8, "content_html": EXAM_PAPER_WALKTHROUGHS_HTML},
]


def main():
    sb = get_client()

    for subject_label, subject_id in [("Science", SCIENCE_ID), ("Separate Sciences", SEPARATE_ID)]:
        print(f"\n{'='*60}")
        print(f"Inserting revision technique guides for {subject_label} ({subject_id})")
        print(f"{'='*60}")

        for guide in GUIDES:
            row = {
                "subject_id": subject_id,
                "guide_type": "revision-technique",
                "slug": guide["slug"],
                "title": guide["title"],
                "content_html": guide["content_html"],
                "sort_order": guide["sort_order"],
            }

            try:
                result = sb.table("guide_pages").upsert(
                    row,
                    on_conflict="subject_id,guide_type,slug"
                ).execute()

                print(f"  [OK] {guide['slug']} (sort_order={guide['sort_order']})")
            except Exception as e:
                print(f"  [FAIL] {guide['slug']}: {e}")

    # Verify counts
    print("\n\nVerification:")
    for subject_label, subject_id in [("Science", SCIENCE_ID), ("Separate Sciences", SEPARATE_ID)]:
        r = sb.table("guide_pages").select("slug,title,sort_order").eq("subject_id", subject_id).eq("guide_type", "revision-technique").order("sort_order").execute()
        print(f"\n{subject_label} ({len(r.data)} guides):")
        for g in r.data:
            print(f"  {g['sort_order']} | {g['slug']} | {g['title']}")


if __name__ == "__main__":
    main()
