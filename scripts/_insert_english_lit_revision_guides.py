"""
Insert 9 revision technique guide pages for English Literature (AQA 8702) into Supabase.
Subject slug: english-literature
Subject ID: b3526a0a-254c-49e9-bb42-65aa3aadb2ea
"""

import sys
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

SUBJECT_ID = 'b3526a0a-254c-49e9-bb42-65aa3aadb2ea'

# ─────────────────────────────────────────────────────────────────────────────
# HUB PAGE
# ─────────────────────────────────────────────────────────────────────────────

HUB_HTML = """<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>Evidence-based strategies that actually work. Each technique is backed by cognitive science research and tailored to GCSE English Literature revision.</p>
</div>
</div>
<div class="guide-hub">
<!-- Foundation Techniques -->
<div class="guide-paper" style="--paper-accent: #7c3aed; --paper-light: #f5f3ff;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these throughout your revision</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="retrieval-practice.html">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself on quotes, characters, and context. Brain dumps beat re-reading every time.</p>
</a>
<a class="guide-question-card" href="quote-flashcards.html">
<span class="guide-question-marks">Quote memorisation</span>
<h3>Quote Flashcards</h3>
<p>Build, sort, and rehearse your quote bank. Essential for English Lit &mdash; you must quote from memory.</p>
</a>
<a class="guide-question-card" href="spaced-repetition.html">
<span class="guide-question-marks">Scheduling</span>
<h3>Spaced Repetition</h3>
<p>Spread your revision of each text across weeks. Short sessions with gaps lock quotes into long-term memory.</p>
</a>
<a class="guide-question-card" href="dual-coding.html">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>Combine words and visuals &mdash; character maps, theme webs, and plot timelines aid memory and essay planning.</p>
</a>
<a class="guide-question-card" href="knowledge-organisers.html">
<span class="guide-question-marks">Summarising</span>
<h3>Knowledge Organisers</h3>
<p>Condense each text onto one page. Creating it from memory is the most powerful part.</p>
</a>
</div>
</div>
<!-- Exam Preparation -->
<div class="guide-paper" style="--paper-accent: #7c3aed; --paper-light: #f5f3ff;">
<div class="guide-paper-header">
<h2>Exam Preparation</h2>
<span class="guide-paper-ref">Final weeks before the exam &mdash; sharpen and apply</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="elaborative-interrogation.html">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask &ldquo;why did the writer choose this?&rdquo; to turn shallow notes into analytical understanding.</p>
</a>
<a class="guide-question-card" href="interleaving.html">
<span class="guide-question-marks">Mixed practice</span>
<h3>Interleaving</h3>
<p>Mix texts and question types in one session. Harder in the moment, stronger in the exam.</p>
</a>
<a class="guide-question-card" href="timed-exam-practice.html">
<span class="guide-question-marks">Exam readiness</span>
<h3>Timed Exam Practice</h3>
<p>Write essays under real exam conditions and mark against AQA level descriptors.</p>
</a>
</div>
</div>
</div>"""

# ─────────────────────────────────────────────────────────────────────────────
# RETRIEVAL PRACTICE
# ─────────────────────────────────────────────────────────────────────────────

RETRIEVAL_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Active recall</span>
<h1>Retrieval Practice</h1>
<p class="guide-used-in">Test yourself, don&rsquo;t just re-read</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Retrieval practice means pulling information out of your memory rather than reading it back in. Every time you successfully recall a fact, a quote, or a writer&rsquo;s technique, that memory trace grows stronger. Re-reading your notes feels productive, but research consistently shows it creates a false sense of familiarity without building lasting knowledge.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead>
<tr><th>Study</th><th>Finding</th><th>Impact</th></tr>
</thead>
<tbody>
<tr>
<td><strong>Roediger &amp; Karpicke (2006)</strong></td>
<td>Students who practised retrieval remembered 80% after one week; re-readers remembered 36%</td>
<td>More than double the retention</td>
</tr>
<tr>
<td><strong>Dunlosky et al. (2013)</strong></td>
<td>Major review rated practice testing as HIGH utility &mdash; one of only two top-rated techniques</td>
<td>Strongest evidence of any revision strategy</td>
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
<strong>Read one topic</strong> &mdash; Spend 5 minutes reading through a section on one text, character, or theme. Don&rsquo;t highlight &mdash; just read to understand.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Close your notes</strong> &mdash; Put everything away. No peeking. This moment of struggle is where memory is built.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Brain dump on a blank page</strong> &mdash; Write everything you remember: quotes, characters, themes, context, writer&rsquo;s methods. Aim for 5&ndash;8 minutes. Use bullet points, sketches, diagrams &mdash; whatever helps.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Check and highlight gaps</strong> &mdash; Open your notes. Use a different colour to fill in what you missed or got wrong. Gaps are your revision priority.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Repeat on the gaps</strong> &mdash; Next session, focus specifically on the parts you couldn&rsquo;t recall. Keep cycling until the gaps are filled.
</div>
</li>
</ol>
</div>
<!-- Section 3: Timing -->
<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 28%;">Read<br/>5 min</span>
<span style="background: #8b5cf6; width: 44%;">Brain dump<br/>8 min</span>
<span style="background: #a78bfa; width: 28%;">Check gaps<br/>5 min</span>
</div>
<p>One full cycle takes about 18 minutes. Do 2&ndash;3 cycles per session, covering different texts or topics each time. Use retrieval practice as your default method &mdash; not an occasional extra.</p>
</div>
<!-- Section 4: Worked Example -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Macbeth &mdash; Ambition Brain Dump</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph guide-weak-answer">
<span class="guide-annotation guide-annotation-weak">First attempt &mdash; from memory only</span>
<p>Macbeth is ambitious. He wants to become king and kills Duncan to get there. Lady Macbeth pushes him into it. The witches tell him he&rsquo;ll be king. There&rsquo;s a quote about &ldquo;vaulting ambition&rdquo;. He becomes more violent as the play goes on and kills Banquo too. Shakespeare is showing that unchecked ambition is dangerous. There&rsquo;s something about Jacobean ideas of order&hellip;</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">After checking &mdash; gaps filled</span>
<p>Macbeth is ambitious. He wants to become king and kills Duncan to get there. Lady Macbeth pushes him &mdash; <strong>&ldquo;unsex me here&rdquo; shows she invokes supernatural forces to overcome her own moral restraint</strong>. The witches tell him he&rsquo;ll be king &mdash; <strong>Act 1, Scene 3: &ldquo;All hail, Macbeth, that shalt be king hereafter!&rdquo;</strong>. Macbeth himself identifies the danger in &ldquo;<strong>I have no spur / To prick the sides of my intent, but only / Vaulting ambition, which o&rsquo;erleaps itself&rdquo;</strong>. He becomes more violent &mdash; orders Banquo killed, massacres Macduff&rsquo;s family. <strong>Shakespeare, writing for a Jacobean audience who had just survived the Gunpowder Plot (1605), would have wanted to show the catastrophic consequences of challenging divinely appointed order.</strong> The play ends with Macbeth dead and Malcolm crowned &mdash; restoring the Great Chain of Being.</p>
</div>
<p><strong>What this reveals:</strong> The first attempt captured the broad idea but missed specific quotes, act and scene references, and historical context. These gaps are the focus of the next cycle.</p>
</div>
</div>
</div>
<!-- Section 5: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Re-reading instead of recalling</strong> &mdash; Reading your notes five times feels like revision but barely builds memory. Close the book and test yourself.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Peeking at quotes too soon</strong> &mdash; The struggle to remember is the learning. Looking up the quote the moment you get stuck skips the part that matters.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Only testing what you already know</strong> &mdash; It feels good to recall easy quotes, but the real gains come from practising the texts and themes you find hardest.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Not returning to the same topic</strong> &mdash; One brain dump is a start, not the finish. Revisit each text multiple times at increasing intervals (see Spaced Repetition).</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: close this page and write down everything you know about Scrooge from <em>A Christmas Carol</em>. Set a 6-minute timer. Then check your notes for gaps.</p>
</div>
<nav class="guide-nav">
<div></div>
<a class="guide-nav-link guide-nav-next" href="spaced-repetition.html">Spaced Repetition &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 28%;" title="Read: 5 min"></span>
<span style="background: #8b5cf6; width: 44%;" title="Brain dump: 8 min"></span>
<span style="background: #a78bfa; width: 28%;" title="Check gaps: 5 min"></span>
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
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# QUOTE FLASHCARDS
# ─────────────────────────────────────────────────────────────────────────────

QUOTE_FLASHCARDS_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Quote memorisation</span>
<h1>Quote Flashcards</h1>
<p class="guide-used-in">Build your quote bank and learn it for life</p>
</div>
<!-- Section 1: Why Quotes Matter in English Lit -->
<div class="guide-section">
<h2>Why This Matters for English Literature</h2>
<p>AQA English Literature exams are closed-book &mdash; you are not allowed to bring your texts into the exam. This means you <em>must</em> memorise quotations. Students who can embed short, precise quotes earn higher marks because they can use textual evidence to support every analytical point they make.</p>
<p>Quote flashcards combine two powerful memory techniques: <strong>retrieval practice</strong> (testing yourself from memory) and <strong>spaced repetition</strong> (reviewing cards at increasing intervals). Used together, they are the single most effective way to build and retain your quote bank for all four AQA texts: <em>Macbeth</em>, <em>A Christmas Carol</em>, <em>Animal Farm</em>, and the Power &amp; Conflict poems.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>AQA examiners reward quotations that are concise (1&ndash;3 words from the text can be enough), well-chosen, and analysed in detail &mdash; not long passages copied out. A single powerful word with sharp analysis outscores a long quote with no comment.</p>
</div>
</div>
<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Curate your quotes</strong> &mdash; For each text, select 10&ndash;15 short quotations that cover the key themes. Favour quotes that are flexible &mdash; ones you can use for multiple themes or questions. For poetry, aim for 2&ndash;3 quotes per poem.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Make your flashcards</strong> &mdash; Front: the quote + speaker + act/stave/chapter. Back: theme it links to, language technique, and a one-sentence analytical comment. Physical cards work best (index cards), but apps like Anki work well too.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Sort into piles</strong> &mdash; After a test round, divide cards into three piles: Know it (green), Getting there (amber), Don&rsquo;t know (red). Spend most time on red cards next session.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Test both directions</strong> &mdash; Forwards (quote &rarr; explain) AND backwards (theme &rarr; recall a quote). Both directions appear in the exam in different forms.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Write them in context</strong> &mdash; Once you can recall a quote, practise writing it into a full analytical sentence or paragraph. Isolated memorisation without practice using it is incomplete revision.
</div>
</li>
</ol>
</div>
<!-- Section 3: Worked Example -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: A Christmas Carol Flashcard Set</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead>
<tr><th>Front of card</th><th>Back of card</th></tr>
</thead>
<tbody>
<tr>
<td><strong>&ldquo;Solitary as an oyster&rdquo;</strong><br/>Dickens, Stave 1</td>
<td><strong>Theme:</strong> Isolation / Scrooge&rsquo;s character<br/><strong>Technique:</strong> Simile<br/><strong>Analysis:</strong> The oyster is cold, hard-shelled, and enclosed &mdash; Dickens presents Scrooge as having deliberately sealed himself off from human warmth and compassion</td>
</tr>
<tr>
<td><strong>&ldquo;Mankind was my business&rdquo;</strong><br/>Marley&rsquo;s Ghost, Stave 1</td>
<td><strong>Theme:</strong> Social responsibility / redemption<br/><strong>Technique:</strong> Declarative statement<br/><strong>Analysis:</strong> Dickens uses Marley as a warning &mdash; his regret is Scrooge&rsquo;s potential future. The word &ldquo;business&rdquo; echoes Scrooge&rsquo;s commercial world but inverts its meaning</td>
</tr>
<tr>
<td><strong>&ldquo;The boy is Ignorance. The girl is Want.&rdquo;</strong><br/>Ghost of Christmas Present, Stave 3</td>
<td><strong>Theme:</strong> Social responsibility / poverty<br/><strong>Technique:</strong> Allegory / personification<br/><strong>Analysis:</strong> Dickens explicitly links poverty to ignorance &mdash; a direct message to middle-class Victorian readers about the consequences of ignoring the poor</td>
</tr>
</tbody>
</table>
<p><strong>Tip:</strong> The back of each card should contain enough for a full analytical point &mdash; not just a single word label. The analysis column is what turns a quote into marks.</p>
</div>
</div>
</div>
<!-- Section 4: Organising Your Quote Bank -->
<div class="guide-section">
<h2>Organising Your Quote Bank</h2>
<p>Sort your flashcards in two different ways &mdash; by <strong>theme</strong> and by <strong>character</strong>. The AQA exam will ask about both, so you need to be able to access your quotes from either angle.</p>
<table class="guide-levels">
<thead>
<tr><th>Text</th><th>Suggested themes to cover</th><th>Target quotes per theme</th></tr>
</thead>
<tbody>
<tr>
<td><em>Macbeth</em></td>
<td>Ambition, power, appearance vs reality, gender, the supernatural</td>
<td>3&ndash;4</td>
</tr>
<tr>
<td><em>A Christmas Carol</em></td>
<td>Redemption, social responsibility, poverty, Christmas/generosity</td>
<td>3&ndash;4</td>
</tr>
<tr>
<td><em>Animal Farm</em></td>
<td>Power/corruption, propaganda, equality, revolution</td>
<td>3&ndash;4</td>
</tr>
<tr>
<td>Power &amp; Conflict poems</td>
<td>Per poem: power, conflict, memory, nature, identity</td>
<td>2&ndash;3 per poem</td>
</tr>
</tbody>
</table>
</div>
<!-- Section 5: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Memorising too many quotes</strong> &mdash; 10&ndash;15 flexible quotes per text is better than 40 rigid ones. You need quotes you can actually deploy under pressure.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Memorising without analysing</strong> &mdash; A quote you can recall but can&rsquo;t analyse is useless in the exam. Every card must have an analytical comment on the back.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Not practising writing them in</strong> &mdash; Knowing a quote and being able to embed it fluently in an essay are different skills. Write practice paragraphs using each quote.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: make 5 flashcards for <em>Macbeth</em> right now &mdash; one quote for each of these themes: ambition, power, gender, the supernatural, appearance vs reality. Include the speaker, technique, and a one-sentence analysis on the back.</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="retrieval-practice.html">&larr; Retrieval Practice</a>
<a class="guide-nav-link guide-nav-next" href="spaced-repetition.html">Spaced Repetition &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>Card Format</h4>
<ul class="guide-quick-ref-steps">
<li>Front: quote + speaker + location</li>
<li>Back: theme + technique + analysis</li>
<li>Sort: know it / getting there / don&rsquo;t know</li>
<li>Test both directions</li>
<li>Practise writing them in</li>
</ul>
<h4>Target</h4>
<ul class="guide-quick-ref-steps">
<li>10&ndash;15 quotes per novel/play</li>
<li>2&ndash;3 quotes per poem</li>
</ul>
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
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# SPACED REPETITION
# ─────────────────────────────────────────────────────────────────────────────

SPACED_REPETITION_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Scheduling</span>
<h1>Spaced Repetition</h1>
<p class="guide-used-in">Spread your revision to make it stick</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Spaced repetition is the practice of revisiting material at increasing time intervals &mdash; today, then in 3 days, then in a week, then in two weeks. This exploits a quirk of human memory called the <strong>spacing effect</strong>: revisiting information just as you&rsquo;re about to forget it produces a much stronger memory trace than re-reading it when it&rsquo;s still fresh.</p>
<p>For English Literature, spaced repetition is particularly powerful for quote memorisation and context learning. The quotes for <em>Macbeth</em>, <em>A Christmas Carol</em>, <em>Animal Farm</em>, and the Power &amp; Conflict poems are not things you can learn in one night before the exam &mdash; they require repeated exposure over weeks.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>Cepeda et al. (2006) found that spacing your revision sessions produces retention rates 10&ndash;30% higher than massed practice (&ldquo;cramming&rdquo;). For a closed-book exam where you must recall quotes from memory, this difference is decisive.</p>
</div>
</div>
<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Build your revision timetable early</strong> &mdash; Start at least 8 weeks before your exam. Plot out when you will cover each text for the first time, and mark return visits at increasing intervals.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>First pass &mdash; Week 1</strong> &mdash; Study one text per day (e.g. <em>Macbeth</em> on Monday, <em>A Christmas Carol</em> on Tuesday). Use retrieval practice: brain dumps, quote recall, theme summaries.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Return visit &mdash; 3 days later</strong> &mdash; Briefly test yourself on the same text again. Don&rsquo;t just re-read &mdash; cover your notes and recall. Fill gaps with a different colour pen.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Second return &mdash; 1 week later</strong> &mdash; Third exposure to the same material. By now some things will stick firmly; others will still be slipping. Focus your time on the quotes and context facts that keep disappearing.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Final pass &mdash; exam week</strong> &mdash; Quick review only. At this point you&rsquo;re consolidating, not learning new material. If gaps remain, prioritise the most flexible quotes that cover multiple themes.
</div>
</li>
</ol>
</div>
<!-- Section 3: Sample Timetable -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Sample 8-Week Spaced Repetition Timetable</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead>
<tr><th>Week</th><th>Focus</th><th>Activity</th></tr>
</thead>
<tbody>
<tr><td>Week 1</td><td>First pass: <em>Macbeth</em> + <em>A Christmas Carol</em></td><td>Brain dumps, quote flashcards (first make)</td></tr>
<tr><td>Week 2</td><td>First pass: <em>Animal Farm</em> + Power &amp; Conflict poems</td><td>Brain dumps, quote flashcards (first make)</td></tr>
<tr><td>Week 3</td><td>Return: <em>Macbeth</em> + <em>A Christmas Carol</em></td><td>Retrieval test &mdash; fill gaps</td></tr>
<tr><td>Week 4</td><td>Return: <em>Animal Farm</em> + poems; new essay practice</td><td>Retrieval test + timed paragraphs</td></tr>
<tr><td>Week 5</td><td>Second return: all texts; interleave themes</td><td>Mixed retrieval + essay plans</td></tr>
<tr><td>Week 6</td><td>Exam technique focus</td><td>Timed essays, mark against level descriptors</td></tr>
<tr><td>Week 7</td><td>Third return: weakest quotes + context</td><td>Flashcard red-pile focus</td></tr>
<tr><td>Week 8 (exam)</td><td>Final pass &mdash; consolidation only</td><td>Quick flashcard review, no new material</td></tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Section 4: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Starting too late</strong> &mdash; Spaced repetition only works if there&rsquo;s enough time between sessions. Starting revision two days before the exam makes spacing impossible.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Revising only your favourite text</strong> &mdash; The AQA exam covers all your set texts. You need spaced practice across <em>Macbeth</em>, <em>A Christmas Carol</em>, <em>Animal Farm</em>, and the poems &mdash; not just the one you enjoy most.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Re-reading without testing</strong> &mdash; Spacing your re-reads has minimal effect. You need to space your <em>retrieval attempts</em> &mdash; close your notes and test yourself each time.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: pick one text you&rsquo;ve revised recently and test yourself for 5 minutes without notes. Then write a return-visit reminder in your diary for 3 days&rsquo; time.</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="quote-flashcards.html">&larr; Quote Flashcards</a>
<a class="guide-nav-link guide-nav-next" href="interleaving.html">Interleaving &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>Spacing Schedule</h4>
<ol class="guide-quick-ref-steps">
<li>Study today</li>
<li>Return in 3 days</li>
<li>Return in 1 week</li>
<li>Return in 2 weeks</li>
<li>Final review: exam week</li>
</ol>
<h4>Key Rule</h4>
<ul class="guide-quick-ref-steps">
<li>Always test, never just re-read</li>
<li>Cover all texts equally</li>
<li>Start 8+ weeks before exams</li>
</ul>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# INTERLEAVING
# ─────────────────────────────────────────────────────────────────────────────

INTERLEAVING_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Mixed practice</span>
<h1>Interleaving</h1>
<p class="guide-used-in">Mix texts and topics in one session</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Interleaving means mixing different texts, themes, or question types within a single revision session &mdash; instead of spending an hour on only <em>Macbeth</em>, you might spend 20 minutes on <em>Macbeth</em>, then 20 on <em>A Christmas Carol</em>, then 20 on a Power &amp; Conflict poem. This feels harder and less productive in the moment, but produces significantly stronger recall when it counts.</p>
<p>Psychologists call this the <strong>interleaving effect</strong>. It works because switching between texts forces your brain to actively retrieve the right information and distinguish between similar ideas &mdash; exactly what you need to do in the exam when you must compare texts or choose the right quote.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>Rohrer &amp; Taylor (2007) found that students who interleaved different problem types scored 43% on a final test compared to 20% for students who practised in blocks. For English Lit, where you must hold four texts in your head simultaneously, interleaving is especially valuable.</p>
</div>
</div>
<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Plan your session in chunks</strong> &mdash; Divide your revision time into 20-minute blocks, one per text or theme. A 60-minute session might cover <em>Macbeth</em> power + <em>Animal Farm</em> power + a Power &amp; Conflict poem.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Use a theme as the thread</strong> &mdash; Pick one overarching theme (e.g. power, corruption, redemption) and explore it across different texts in the same session. This builds the comparative thinking the AQA exam rewards.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Switch without warning</strong> &mdash; When the timer goes off, stop mid-thought if necessary and switch. The abruptness forces your brain to &ldquo;save&rdquo; where it was and pick it up next time.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Mix question types too</strong> &mdash; Vary between quote recall, essay plans, context brain dumps, and analytical paragraphs in the same session. Don&rsquo;t only ever do one type of activity.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Embrace the difficulty</strong> &mdash; It will feel less smooth than blocking. That feeling of effort is the learning happening. Trust the process.
</div>
</li>
</ol>
</div>
<!-- Section 3: Worked Example -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: A 60-Minute Interleaved Session on Power</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead>
<tr><th>Time</th><th>Text</th><th>Activity</th></tr>
</thead>
<tbody>
<tr><td>0&ndash;20 min</td><td><em>Macbeth</em> &mdash; Power</td><td>Brain dump: all quotes about power / ambition you can recall. Check gaps.</td></tr>
<tr><td>20&ndash;40 min</td><td><em>Animal Farm</em> &mdash; Power</td><td>Write an analytical paragraph on Napoleon&rsquo;s use of power using at least two quotes.</td></tr>
<tr><td>40&ndash;60 min</td><td>Power &amp; Conflict poem &mdash; &ldquo;Ozymandias&rdquo;</td><td>Flashcard test: recall all quotes. Write a 3-sentence comparison to <em>Macbeth</em>.</td></tr>
</tbody>
</table>
<p><strong>Outcome:</strong> By the end of this session you&rsquo;ve practised power as a theme across three different texts, built comparative thinking, and used three different revision activities (brain dump, essay paragraph, flashcard + comparison). This is far more exam-ready than spending 60 minutes only on <em>Macbeth</em>.</p>
</div>
</div>
</div>
<!-- Section 4: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Staying in one text because it feels comfortable</strong> &mdash; The ease of blocking is an illusion. If you only ever revise one text per session, you aren&rsquo;t building the mental agility the exam requires.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Interleaving without retrieval</strong> &mdash; Just reading about different texts isn&rsquo;t interleaving &mdash; it&rsquo;s varied re-reading. Each chunk must involve actively recalling or applying knowledge.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Switching too rapidly</strong> &mdash; 5-minute chunks are too short for English Literature. You need at least 15&ndash;20 minutes per switch to build depth, not just surface familiarity.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: set two 20-minute timers. First: recall everything you know about the theme of corruption in <em>Animal Farm</em>. Second: recall everything about ambition in <em>Macbeth</em>. Then write one sentence comparing the two.</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="spaced-repetition.html">&larr; Spaced Repetition</a>
<a class="guide-nav-link guide-nav-next" href="dual-coding.html">Dual Coding &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>Session Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Pick a theme (e.g. power)</li>
<li>20 min per text on that theme</li>
<li>Mix activity types per chunk</li>
<li>Embrace the difficulty</li>
</ol>
<h4>Works Best For</h4>
<ul class="guide-quick-ref-steps">
<li>Cross-text comparison</li>
<li>Quote recall across texts</li>
<li>Theme revision</li>
</ul>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# DUAL CODING
# ─────────────────────────────────────────────────────────────────────────────

DUAL_CODING_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Visual learning</span>
<h1>Dual Coding</h1>
<p class="guide-used-in">Combine words and visuals to remember more</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Dual coding is the practice of pairing verbal information with visual representations. When you process information in two forms simultaneously &mdash; words and images &mdash; you create two separate memory traces instead of one. This means you have twice as many &ldquo;hooks&rdquo; to retrieve the information from during the exam.</p>
<p>Allan Paivio&rsquo;s dual coding theory (1971) showed that memory is stronger when both verbal and visual processing systems are engaged. For English Literature, this means creating character maps, theme diagrams, plot timelines, and annotated images &mdash; not just re-reading linear notes.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>Dual coding doesn&rsquo;t mean adding decorative doodles to your notes. The visuals must <em>represent the content</em> &mdash; a character map showing relationships, a timeline showing Scrooge&rsquo;s transformation, a theme web connecting quotes to ideas. Irrelevant pictures are distraction, not dual coding.</p>
</div>
</div>
<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Choose a visual format for each text</strong> &mdash; Different content suits different visuals. See the worked examples below for ideas specific to each AQA text.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Start from memory</strong> &mdash; Try to create the visual without looking at your notes first. Blank spaces tell you what to focus on. Only then check and fill gaps.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Add quotes to the visual</strong> &mdash; A character map for Macbeth should include key quotes near each character or connection. This anchors the language to the visual.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Recreate, don&rsquo;t redecorate</strong> &mdash; The next time you revise this text, recreate the visual from memory on a blank page. Don&rsquo;t just add colour to an existing diagram &mdash; that&rsquo;s passive, not active.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Use your visuals for essay planning</strong> &mdash; In the exam, a quick sketch of a theme web or character map before writing can help you structure your essay and recall quotes under pressure.
</div>
</li>
</ol>
</div>
<!-- Section 3: Visual Types for English Lit -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Examples: Visuals for Each AQA Text</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead>
<tr><th>Text</th><th>Visual type</th><th>What to include</th></tr>
</thead>
<tbody>
<tr>
<td><em>Macbeth</em></td>
<td>Character relationship map</td>
<td>All main characters in circles, arrows showing relationships, key quotes on the arrows, power dynamics annotated</td>
</tr>
<tr>
<td><em>A Christmas Carol</em></td>
<td>Transformation timeline</td>
<td>Scrooge at start vs end of each stave, key quotes at each stage, the three ghosts + what they show him, Victorian social context</td>
</tr>
<tr>
<td><em>Animal Farm</em></td>
<td>Power hierarchy diagram</td>
<td>The animals arranged in a pyramid by power, Napoleon&rsquo;s key actions at each stage, quotes about equality/propaganda, parallels to Russian Revolution</td>
</tr>
<tr>
<td>Power &amp; Conflict poems</td>
<td>Thematic web per poem</td>
<td>Poem title at centre, key themes as branches, one quote per theme, poet&rsquo;s technique labelled (e.g. &ldquo;enjambment in &lsquo;Exposure&rsquo; mirrors exhaustion&rdquo;)</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Section 4: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Spending too long making it look beautiful</strong> &mdash; Neat, coloured diagrams are satisfying but the learning is in creating them from memory, not in the colour-coding. Aesthetics are secondary.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Drawing without quotes</strong> &mdash; A character map without quotations is just a diagram of names. The quotes are essential &mdash; that&rsquo;s what makes it English Literature dual coding.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Creating a visual once and never returning to it</strong> &mdash; Recreate your visuals from memory on a blank page each time you revise. The retrieval attempt is the learning &mdash; just looking at an old diagram is passive.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: draw a blank spider diagram with &ldquo;Scrooge&rdquo; in the centre. Add 5 branches for 5 key character traits. From memory, add one quote to each branch. Then check your notes for what you missed.</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="interleaving.html">&larr; Interleaving</a>
<a class="guide-nav-link guide-nav-next" href="elaborative-interrogation.html">Elaborative Interrogation &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>Visual Types</h4>
<ul class="guide-quick-ref-steps">
<li><em>Macbeth</em>: character map</li>
<li><em>Christmas Carol</em>: transformation timeline</li>
<li><em>Animal Farm</em>: power hierarchy</li>
<li>Poems: thematic web per poem</li>
</ul>
<h4>Key Rules</h4>
<ul class="guide-quick-ref-steps">
<li>Always include quotes</li>
<li>Create from memory first</li>
<li>Recreate, don&rsquo;t redecorate</li>
</ul>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# ELABORATIVE INTERROGATION
# ─────────────────────────────────────────────────────────────────────────────

ELABORATIVE_INTERROGATION_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Deep thinking</span>
<h1>Elaborative Interrogation</h1>
<p class="guide-used-in">Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; about writer&rsquo;s choices</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>Elaborative interrogation is a revision technique where you ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; about the facts you&rsquo;re learning, rather than simply accepting them. It forces you to generate explanations &mdash; which builds deeper, more flexible understanding than passive note-taking.</p>
<p>For English Literature, this technique is transformative. Instead of noting that Shakespeare uses a soliloquy, you ask: <em>Why does Shakespeare choose a soliloquy here? What does it achieve that dialogue cannot? How does it position the audience?</em> This kind of questioning is exactly what AQA examiners reward in Level 4 and Level 5 responses.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>Dunlosky et al. (2013) rated elaborative interrogation as MODERATE utility &mdash; more effective than re-reading or summarising. For English Literature, where analysis of writer&rsquo;s choices is the core assessment objective (AO2), it is particularly powerful.</p>
</div>
</div>
<!-- Section 2: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Identify a writer&rsquo;s choice</strong> &mdash; Pick a specific technique, structural decision, word choice, or character action from one of your set texts.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Ask &ldquo;Why did the writer choose this?&rdquo;</strong> &mdash; Don&rsquo;t accept the surface answer. Push deeper. Why a metaphor and not a simile? Why place this scene here in the structure? Why give this character these exact words?
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Ask &ldquo;What effect does it have on the reader?&rdquo;</strong> &mdash; Connect the technique to its impact. How does it make the reader feel? What does it make them think about the character or theme?
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Ask &ldquo;How does this connect to context?&rdquo;</strong> &mdash; What does this choice reveal about the writer&rsquo;s intentions, historical context, or the audience&rsquo;s values and beliefs at the time?
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Write your answer as an analytical chain</strong> &mdash; Technique &rarr; effect &rarr; context &rarr; significance. This is the structure of a Level 5 AQA paragraph.
</div>
</li>
</ol>
</div>
<!-- Section 3: Worked Example -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Elaborative Interrogation on &ldquo;Ozymandias&rdquo;</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<p><strong>Starting fact:</strong> Shelley uses a framing narrative in &ldquo;Ozymandias&rdquo; &mdash; the poem is told by a traveller who met someone else who saw the statue. The poet never speaks directly.</p>
<p><strong>Why did Shelley choose this?</strong></p>
<p>The multiple layers of narration (Shelley &rarr; speaker &rarr; traveller &rarr; sculptor) distance Ozymandias from the reader. The tyrant&rsquo;s boasts have been filtered through layers of time and retelling &mdash; they reach us as an echo, not a voice. This structurally enacts the poem&rsquo;s theme: power fades, voices are silenced, and what remains is fragmentary and distant.</p>
<p><strong>What effect does it have?</strong></p>
<p>It makes Ozymandias&rsquo;s arrogance seem even more pathetic. His boast &mdash; &ldquo;Look on my Works, ye Mighty, and despair!&rdquo; &mdash; was meant to intimidate, but it now survives only as a recorded quotation about a broken statue in an empty desert. The gap between his intended audience (&ldquo;ye Mighty&rdquo;) and the actual audience (us, reading a poem) is devastatingly ironic.</p>
<p><strong>How does this connect to context?</strong></p>
<p>Shelley was a Romantic poet who opposed tyranny and the abuse of power. Writing in 1818, he was responding to the autocracies of Europe (Napoleon had only just fallen). The framing narrative allows him to critique tyranny without naming a living ruler &mdash; the historical distance of ancient Egypt makes his political point safer but no less clear.</p>
</div>
</div>
</div>
<!-- Section 4: Key Questions to Ask -->
<div class="guide-section">
<h2>Key Questions to Ask About Any Writer&rsquo;s Choice</h2>
<table class="guide-levels">
<thead>
<tr><th>Question</th><th>What it unlocks</th></tr>
</thead>
<tbody>
<tr><td>Why this technique and not another?</td><td>Specificity of analysis &mdash; shows you understand what the technique <em>does</em></td></tr>
<tr><td>Why at this point in the text?</td><td>Structural analysis &mdash; AO1 + AO2 marks for structure</td></tr>
<tr><td>What would be lost without it?</td><td>Forces you to articulate the exact effect</td></tr>
<tr><td>What does this reveal about the writer&rsquo;s intentions?</td><td>AO3 context marks &mdash; links technique to purpose</td></tr>
<tr><td>How might a contemporary reader have responded?</td><td>Historical/contextual relevance &mdash; AO3</td></tr>
</tbody>
</table>
</div>
<!-- Section 5: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Naming the technique without asking why</strong> &mdash; &ldquo;Shelley uses a metaphor&rdquo; is not analysis. &ldquo;Shelley uses the metaphor of a &lsquo;shattered visage&rsquo; to suggest that Ozymandias&rsquo;s identity &mdash; his face, his power, his legacy &mdash; has been literally and figuratively broken by time&rdquo; is analysis.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Stopping at effect without reaching context</strong> &mdash; AQA&rsquo;s top mark bands require linking writer&rsquo;s choices to context (AO3). Always push your &ldquo;why&rdquo; questions all the way to the writer&rsquo;s intentions and historical moment.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Using it only for revision, not for reading</strong> &mdash; Elaborative interrogation is most powerful when practised while you first read the texts. Build the habit of asking &ldquo;why?&rdquo; as you encounter any writer&rsquo;s choice for the first time.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: open <em>A Christmas Carol</em> to the scene where Scrooge is shown his own neglected grave. Ask: why does Dickens withhold Scrooge&rsquo;s name until the end? What effect does this have on the reader? How does it link to Dickens&rsquo;s message about social redemption?</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="dual-coding.html">&larr; Dual Coding</a>
<a class="guide-nav-link guide-nav-next" href="knowledge-organisers.html">Knowledge Organisers &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>The Core Questions</h4>
<ol class="guide-quick-ref-steps">
<li>Why this technique?</li>
<li>Why here in the text?</li>
<li>What effect on the reader?</li>
<li>How does context explain it?</li>
<li>What are the writer&rsquo;s intentions?</li>
</ol>
<h4>Assessment Objectives</h4>
<ul class="guide-quick-ref-steps">
<li>AO1: argument + quotes</li>
<li>AO2: language/structure analysis</li>
<li>AO3: context + intentions</li>
</ul>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE ORGANISERS
# ─────────────────────────────────────────────────────────────────────────────

KNOWLEDGE_ORGANISERS_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Summarising</span>
<h1>Knowledge Organisers</h1>
<p class="guide-used-in">Condense each text to one page &mdash; then test yourself</p>
</div>
<!-- Section 1: What the Research Says -->
<div class="guide-section">
<h2>What the Research Says</h2>
<p>A knowledge organiser is a single page that captures the essential content for one text or topic &mdash; key quotes, character summaries, themes, context, and writer&rsquo;s techniques &mdash; arranged visually so you can see the whole picture at once. The act of <em>creating</em> one from memory is where the learning happens, not the reading of a finished one.</p>
<p>Knowledge organisers work because they force you to prioritise, compress, and organise information &mdash; three cognitively demanding tasks that build durable memory. For English Literature, a well-made knowledge organiser becomes the backbone of your revision: the source material for your retrieval practice, flashcard making, and essay planning.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>A knowledge organiser should take 20&ndash;30 minutes to create from scratch (with notes available). If it takes much longer, you&rsquo;re including too much detail. If it takes much less, you&rsquo;re leaving out too much. The constraint of one page forces difficult prioritisation decisions &mdash; and those decisions are the learning.</p>
</div>
</div>
<!-- Section 2: What to Include -->
<div class="guide-section">
<h2>What to Include on an English Literature Knowledge Organiser</h2>
<table class="guide-levels">
<thead>
<tr><th>Section</th><th>Content</th><th>Space allocation</th></tr>
</thead>
<tbody>
<tr><td><strong>Key quotes</strong></td><td>10&ndash;12 short quotes, theme labelled next to each one</td><td>~40% of page</td></tr>
<tr><td><strong>Character summary</strong></td><td>Main characters, one-line description, key relationship to theme</td><td>~20% of page</td></tr>
<tr><td><strong>Themes</strong></td><td>4&ndash;5 themes with a brief one-sentence summary of how the text treats each</td><td>~20% of page</td></tr>
<tr><td><strong>Context</strong></td><td>3&ndash;4 bullet points of essential historical/biographical context</td><td>~10% of page</td></tr>
<tr><td><strong>Writer&rsquo;s techniques</strong></td><td>Key recurring techniques with one brief example each</td><td>~10% of page</td></tr>
</tbody>
</table>
</div>
<!-- Section 3: Worked Example -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Worked Example: Animal Farm Knowledge Organiser Plan</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<p><strong>Key Quotes (arrange by theme):</strong></p>
<ul>
<li>Power: &ldquo;All animals are equal, but some animals are more equal than others&rdquo;</li>
<li>Propaganda: &ldquo;Four legs good, two legs bad&rdquo; / &ldquo;Napoleon is always right&rdquo;</li>
<li>Corruption: &ldquo;The creatures outside looked from pig to man, and from man to pig&rdquo;</li>
<li>Hope vs despair: &ldquo;Man is the only creature that consumes without producing&rdquo;</li>
</ul>
<p><strong>Characters:</strong> Napoleon (Stalin: ruthless dictator), Snowball (Trotsky: idealist exiled), Squealer (propaganda minister), Boxer (loyal working class), Old Major (Marx/Lenin: revolutionary idealist).</p>
<p><strong>Themes:</strong> Power corrupts &mdash; Napoleon becomes indistinguishable from man. Propaganda &mdash; Squealer rewrites history. Revolution betrayed &mdash; Animalism becomes Pig supremacy. Exploitation of the working class &mdash; Boxer is sent to the knacker&rsquo;s.</p>
<p><strong>Context:</strong> Published 1945. Orwell fought in Spanish Civil War &mdash; saw Stalinist betrayal of socialist ideals. Direct allegory of Russian Revolution (1917) and Stalinist USSR. Written as warning about totalitarianism.</p>
<p><strong>Techniques:</strong> Allegory (animals = political figures), dramatic irony (reader knows what characters don&rsquo;t), repetition of the Seven Commandments (shows gradual corruption), cyclical structure (farm ends as it began &mdash; under oppression).</p>
</div>
</div>
</div>
<!-- Section 4: How to Use Your Knowledge Organiser -->
<div class="guide-section">
<h2>How to Use Your Knowledge Organiser for Revision</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Create it first (with notes)</strong> &mdash; Make your first knowledge organiser with your notes available. Focus on selecting and organising, not on memorising.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Recreate it from memory</strong> &mdash; A week later, use a blank piece of paper to recreate your knowledge organiser without notes. Compare it to the original and fill in gaps.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Use it as your flashcard source</strong> &mdash; Every quote on the organiser should have a flashcard. Use the organiser to check you&rsquo;ve covered all the themes.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Test a partner</strong> &mdash; If you&rsquo;re revising with someone else, use each other&rsquo;s knowledge organisers to quiz each other. Cover the answers and ask questions from the organiser.
</div>
</li>
</ol>
</div>
<!-- Section 5: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Copying out a teacher&rsquo;s knowledge organiser without testing yourself on it</strong> &mdash; A printed knowledge organiser you read passively is worthless. You must recreate yours from memory to build retention.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Including too much</strong> &mdash; If it doesn&rsquo;t fit on one page, you&rsquo;ve included too much. Cut ruthlessly. The constraint is the point.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Making one and never returning to it</strong> &mdash; Knowledge organisers should be remade from memory at spaced intervals (see Spaced Repetition). Each recreation reveals new gaps.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: set a 25-minute timer and create a one-page knowledge organiser for <em>A Christmas Carol</em> &mdash; from memory first, then check your notes. Include quotes, characters, themes, context, and techniques.</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="elaborative-interrogation.html">&larr; Elaborative Interrogation</a>
<a class="guide-nav-link guide-nav-next" href="timed-exam-practice.html">Timed Exam Practice &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>One Page Covers</h4>
<ul class="guide-quick-ref-steps">
<li>Key quotes (labelled by theme)</li>
<li>Character summaries</li>
<li>Main themes</li>
<li>Historical context</li>
<li>Writer&rsquo;s techniques</li>
</ul>
<h4>Process</h4>
<ol class="guide-quick-ref-steps">
<li>Create with notes</li>
<li>Recreate from memory</li>
<li>Fill gaps</li>
<li>Repeat at intervals</li>
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
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="timed-exam-practice.html"><strong>Timed Exam Practice</strong><span>Exam readiness</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# TIMED EXAM PRACTICE
# ─────────────────────────────────────────────────────────────────────────────

TIMED_EXAM_PRACTICE_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Exam readiness</span>
<h1>Timed Exam Practice</h1>
<p class="guide-used-in">Write essays under real exam conditions</p>
</div>
<!-- Section 1: What It Is -->
<div class="guide-section">
<h2>What Is Timed Exam Practice?</h2>
<p>Timed exam practice means sitting down and writing a full essay response under the same time pressure you&rsquo;ll face on the day &mdash; no notes, no phone, with a timer running and the aim of producing a marked, assessed piece of writing.</p>
<p>For AQA English Literature (8702), this means practising your timed essay responses for both papers. Paper 1 (Shakespeare + 19th-century novel) gives you 1 hour 45 minutes for two essays. Paper 2 (modern text + poetry) gives you 2 hours 15 minutes for three questions. Knowing the content is not enough &mdash; you must also be able to produce structured, analytical essays under significant time pressure, from memory.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>AQA English Literature is a closed-book exam. You will not have access to your texts. This means timed essay practice must include the recall of quotations from memory &mdash; not just practising essay structure with a book open in front of you. Both skills must be practised together.</p>
</div>
</div>
<!-- Section 2: Why It Works -->
<div class="guide-section">
<h2>Why It Works</h2>
<p>Psychologists call this &ldquo;transfer-appropriate processing&rdquo;: your brain recalls information most reliably when the conditions during recall match the conditions during learning. If you always revise in a relaxed, untimed way with notes available, you are training your brain for a different situation than the one you&rsquo;ll face in the exam. Simulating exam conditions &mdash; the time pressure, the closed-book format, the formal written response &mdash; builds the exact neural pathways you&rsquo;ll need on the day.</p>
<p>Timed practice also reveals things that no other revision technique can: how long your introductions are taking, whether you run out of relevant quotes halfway through, whether your argument holds together under pressure, and how you manage your time across multiple questions.</p>
</div>
<!-- Section 3: Step-by-Step Method -->
<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body">
<strong>Gather a past paper question</strong> &mdash; Use official AQA past papers from the AQA website, or ask your teacher for practice questions. Use a question you haven&rsquo;t practised on before.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body">
<strong>Set up exam conditions</strong> &mdash; Find a quiet space. Put your phone away (or use it only as a timer). No notes, no texts, no looking things up. Sit at a desk. This is a simulation &mdash; treat it seriously.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body">
<strong>Plan first (5 minutes)</strong> &mdash; Spend 5 minutes on a quick essay plan: identify your main argument, select 3&ndash;4 quotes you&rsquo;ll use, note the techniques and context you&rsquo;ll discuss. A plan prevents rambling and saves time overall.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body">
<strong>Write under the time limit</strong> &mdash; A 30-mark AQA essay should take around 45&ndash;50 minutes. A 20-mark essay takes around 30&ndash;35 minutes. Stick to your allocated time even if you&rsquo;re mid-paragraph when the timer goes off.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body">
<strong>Mark it against level descriptors</strong> &mdash; After writing, use the AQA mark scheme to assess your response. Be honest. Identify which level descriptors you reached and which you didn&rsquo;t. This is more valuable than just knowing your mark.
</div>
</li>
<li class="guide-step">
<span class="guide-step-number">6</span>
<div class="guide-step-body">
<strong>Write a &lsquo;what to do next time&rsquo; note</strong> &mdash; After marking, write 2&ndash;3 specific improvements for your next timed attempt. Be precise: &ldquo;Include the Jacobean context for power in <em>Macbeth</em>&rdquo; is better than &ldquo;more context&rdquo;.
</div>
</li>
</ol>
</div>
<!-- Section 4: Time Management Guide -->
<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>AQA English Literature &mdash; Timing Guide</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<table class="guide-levels">
<thead>
<tr><th>Paper</th><th>Question</th><th>Marks</th><th>Time</th></tr>
</thead>
<tbody>
<tr><td>Paper 1</td><td>Shakespeare (Macbeth extract + whole text)</td><td>30 + 4 SPaG</td><td>~50 min</td></tr>
<tr><td>Paper 1</td><td>19th-century novel (A Christmas Carol)</td><td>30</td><td>~45 min</td></tr>
<tr><td>Paper 2</td><td>Modern text (Animal Farm)</td><td>30</td><td>~45 min</td></tr>
<tr><td>Paper 2</td><td>Poetry: named poem + unseen comparison</td><td>30</td><td>~50 min</td></tr>
<tr><td>Paper 2</td><td>Unseen poem</td><td>24</td><td>~35 min</td></tr>
</tbody>
</table>
<p><strong>Timing rule:</strong> Allocate approximately 1 minute per mark, plus 5 minutes for planning. Spend any remaining time checking &mdash; not adding new material.</p>
</div>
</div>
</div>
<!-- Section 5: Common Mistakes -->
<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Practising with your book open</strong> &mdash; This is not exam practice &mdash; it&rsquo;s essay writing. The exam is closed-book. Your timed practice must also be closed-book.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Not marking your own work</strong> &mdash; Writing essays without assessing them against mark schemes means you can&rsquo;t identify patterns in your own weaknesses. Marking yourself is harder than having a teacher do it &mdash; which is exactly why it builds more insight.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Only practising essays on your favourite texts</strong> &mdash; You must be equally confident in all your set texts. Prioritise the texts you find hardest.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Writing so much that you run out of time on other questions</strong> &mdash; A brilliant answer to one question that leaves two questions unanswered will not pass. Practise stopping on time.</div>
</li>
</ul>
</div>
<div class="key-fact">
<div class="key-fact-label">Quick Start</div>
<p>Try it now: take an AQA past paper question on <em>Macbeth</em>, set a 45-minute timer, put away all notes and books, and write a full essay response. Then mark it using the AQA level descriptors.</p>
</div>
<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="knowledge-organisers.html">&larr; Knowledge Organisers</a>
<div></div>
</nav>
<a class="back-link" href="index.html">&larr; Back to Revision Techniques</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<h4>Session Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Get a past paper question</li>
<li>Set up exam conditions</li>
<li>Plan (5 min)</li>
<li>Write (timed)</li>
<li>Mark against level descriptors</li>
<li>Write &lsquo;next time&rsquo; note</li>
</ol>
<h4>Timing Rule</h4>
<ul class="guide-quick-ref-steps">
<li>~1 minute per mark</li>
<li>+5 min for planning</li>
<li>Closed book, no notes</li>
</ul>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button aria-expanded="false" class="sidebar-collapsible-toggle">
<span>&#128218; Other Techniques</span>
<svg class="sidebar-collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="sidebar-collapsible-content">
<a class="sidebar-media-item" href="retrieval-practice.html"><strong>Retrieval Practice</strong><span>Active recall</span></a>
<a class="sidebar-media-item" href="quote-flashcards.html"><strong>Quote Flashcards</strong><span>Quote memorisation</span></a>
<a class="sidebar-media-item" href="spaced-repetition.html"><strong>Spaced Repetition</strong><span>Scheduling</span></a>
<a class="sidebar-media-item" href="interleaving.html"><strong>Interleaving</strong><span>Mixed practice</span></a>
<a class="sidebar-media-item" href="dual-coding.html"><strong>Dual Coding</strong><span>Visual learning</span></a>
<a class="sidebar-media-item" href="elaborative-interrogation.html"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>
<a class="sidebar-media-item" href="knowledge-organisers.html"><strong>Knowledge Organisers</strong><span>Summarising</span></a>
</div>
</div>
</div>
</aside>"""

# ─────────────────────────────────────────────────────────────────────────────
# ALL PAGES TO INSERT
# ─────────────────────────────────────────────────────────────────────────────

PAGES = [
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'index',
        'title': 'Revision Techniques',
        'content_html': HUB_HTML,
        'sort_order': 0,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'retrieval-practice',
        'title': 'Retrieval Practice',
        'content_html': RETRIEVAL_HTML,
        'sort_order': 1,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'quote-flashcards',
        'title': 'Quote Flashcards',
        'content_html': QUOTE_FLASHCARDS_HTML,
        'sort_order': 2,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'spaced-repetition',
        'title': 'Spaced Repetition',
        'content_html': SPACED_REPETITION_HTML,
        'sort_order': 3,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'interleaving',
        'title': 'Interleaving',
        'content_html': INTERLEAVING_HTML,
        'sort_order': 4,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'dual-coding',
        'title': 'Dual Coding',
        'content_html': DUAL_CODING_HTML,
        'sort_order': 5,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'elaborative-interrogation',
        'title': 'Elaborative Interrogation',
        'content_html': ELABORATIVE_INTERROGATION_HTML,
        'sort_order': 6,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'knowledge-organisers',
        'title': 'Knowledge Organisers',
        'content_html': KNOWLEDGE_ORGANISERS_HTML,
        'sort_order': 7,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'revision-technique',
        'slug': 'timed-exam-practice',
        'title': 'Timed Exam Practice',
        'content_html': TIMED_EXAM_PRACTICE_HTML,
        'sort_order': 8,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# INSERT INTO SUPABASE
# ─────────────────────────────────────────────────────────────────────────────

def main():
    sb = get_client()
    print(f"Inserting {len(PAGES)} revision technique guide pages for English Literature...")

    for page in PAGES:
        slug = page['slug']
        try:
            result = sb.table('guide_pages').upsert(
                page,
                on_conflict='subject_id,guide_type,slug'
            ).execute()
            if result.data:
                print(f"  OK  {slug}")
            else:
                print(f"  ??  {slug} — no data returned")
        except Exception as e:
            print(f"  ERR {slug}: {e}")

    print("\nDone. Verifying...")
    check = sb.table('guide_pages').select('slug,title,sort_order').eq(
        'subject_id', SUBJECT_ID
    ).eq('guide_type', 'revision-technique').order('sort_order').execute()
    print(f"Total revision-technique pages for english-literature: {len(check.data)}")
    for row in check.data:
        print(f"  [{row['sort_order']}] {row['slug']} — {row['title']}")

if __name__ == '__main__':
    main()
