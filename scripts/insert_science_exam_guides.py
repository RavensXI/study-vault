"""
Insert AQA Combined Science (8464) exam technique guide pages into Supabase.
Inserts for both 'science' and 'separate-sciences' subject slugs (same question types).
"""

import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from scripts.lib.supabase_client import get_client

SCIENCE_ID = "02c2e32f-d2db-4eac-a5d4-f55973a2e31a"
SEPARATE_ID = "a9cc3d43-c51b-4ea9-aa15-0977d1b0daee"

# Accent colour for science guides
ACCENT = "#2563eb"  # Blue
ACCENT_MID = "#3b82f6"
ACCENT_LIGHT = "#60a5fa"

# ─────────────────────────────────────────────
# Hub page
# ─────────────────────────────────────────────
HUB_HTML = '''<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Exam Technique</h1>
<p>Step-by-step guides for every AQA GCSE Science question type. Learn the formula, study a model answer, and avoid the common mistakes that cost marks.</p>
</div>
</div>
<div class="guide-hub" style="grid-template-columns: 1fr; max-width: 780px;">
<div class="guide-paper" style="--paper-accent: #2563eb; --paper-light: #eff6ff;">
<div class="guide-paper-header">
<h2>AQA GCSE Combined Science: Trilogy (8464)</h2>
<span class="guide-paper-ref">6 Written Exams &mdash; Biology (2), Chemistry (2), Physics (2) &bull; 1 hour 15 minutes each &bull; 70 marks each</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="recall-1-mark.html">
<span class="guide-question-marks">1 mark</span>
<h3>Recall</h3>
<p>Name, state, or give a single fact. No explanation needed &mdash; precision and accuracy earn the mark.</p>
</a>
<a class="guide-question-card" href="describe-2-marks.html">
<span class="guide-question-marks">2 marks</span>
<h3>Describe</h3>
<p>State what happens in a process, pattern, or trend. Two clear points without needing to explain why.</p>
</a>
<a class="guide-question-card" href="calculate-2-marks.html">
<span class="guide-question-marks">2 marks</span>
<h3>Calculate</h3>
<p>Use a formula, substitute values, and show your working. Units and significant figures matter.</p>
</a>
<a class="guide-question-card" href="explain-3-marks.html">
<span class="guide-question-marks">3 marks</span>
<h3>Explain</h3>
<p>Give a reason or mechanism. Link cause to effect using scientific language &mdash; say what happens and why.</p>
</a>
<a class="guide-question-card" href="compare-and-explain-4-marks.html">
<span class="guide-question-marks">4 marks</span>
<h3>Compare and Explain</h3>
<p>Identify similarities or differences and explain the science behind them. Use comparative language throughout.</p>
</a>
<a class="guide-question-card" href="extended-response-6-marks.html">
<span class="guide-question-marks">6 marks</span>
<h3>Extended Response</h3>
<p>The highest-value question. Structure your answer logically, use scientific terminology, and build a clear argument or explanation.</p>
</a>
</div>
</div>
</div>'''

# ─────────────────────────────────────────────
# 1 mark — Recall
# ─────────────────────────────────────────────
RECALL_HTML = f'''<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">1 mark</span>
<h1>Recall Questions</h1>
<p class="guide-used-in">Used in: All papers (Biology, Chemistry, Physics)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>Recall questions test whether you know a specific fact, term, or piece of information. The examiner wants one precise answer &mdash; nothing more. These questions use command words like &ldquo;Name,&rdquo; &ldquo;State,&rdquo; &ldquo;Give,&rdquo; or &ldquo;What is.&rdquo;</p>
<h3>Marking</h3>
<table class="guide-levels">
<thead><tr><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<tr><td><strong>1</strong></td><td>A correct, specific answer that directly addresses the question</td></tr>
<tr><td>0</td><td>Vague, incorrect, or no response</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Read the question carefully</strong> &mdash; Identify exactly what is being asked. &ldquo;Name the organ&rdquo; and &ldquo;Name the organelle&rdquo; require very different answers.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Give the specific answer</strong> &mdash; Write the term, name, or fact. Use correct scientific terminology (e.g. &ldquo;mitochondria&rdquo; not &ldquo;the part that makes energy&rdquo;).</div></li>
<li class="guide-step"><span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Do not explain</strong> &mdash; This is worth 1 mark. Adding unnecessary explanation wastes time and cannot earn you extra marks.</div></li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: {ACCENT}; width: 100%;">Recall &mdash; 1 min</span>
</div>
<p>One minute maximum. Write your answer and move on. If you cannot remember, leave a gap and return at the end.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Model Answers</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>Name the type of bond formed when metals react with non-metals. [1 mark]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full mark</span>
<p>Ionic bond.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 1/1 &mdash; Clear, correct, no unnecessary detail.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>State the function of the ribosomes in a cell. [1 mark]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full mark</span>
<p>Ribosomes are the site of protein synthesis.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 1/1 &mdash; Uses the correct term &ldquo;protein synthesis.&rdquo;</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Give the unit used to measure electrical resistance. [1 mark]</p></div>
<div class="guide-model-paragraph guide-weak-answer"><span class="guide-annotation guide-annotation-weak">0 marks &mdash; wrong unit</span>
<p>Volts.</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full mark</span>
<p>Ohms (&Omega;).</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> A common confusion. Resistance is measured in ohms, not volts. Volts measure potential difference.</p></div>

</div></div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Confusing similar terms</strong> &mdash; &ldquo;Mitosis&rdquo; and &ldquo;meiosis,&rdquo; &ldquo;evaporation&rdquo; and &ldquo;condensation,&rdquo; &ldquo;current&rdquo; and &ldquo;voltage&rdquo; are commonly mixed up. Learn the precise definition of each.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Being vague</strong> &mdash; &ldquo;The thing that carries blood&rdquo; will not earn the mark. The examiner wants &ldquo;artery&rdquo; or &ldquo;vein&rdquo; (and the correct one for the context).</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Wasting time explaining</strong> &mdash; If a question says &ldquo;Name&rdquo; or &ldquo;State,&rdquo; it wants a fact, not an explanation. Extra detail earns no additional marks.</div></li>
</ul>
</div>

<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="extended-response-6-marks.html">&larr; Extended Response (6 marks)</a>
<a class="guide-nav-link guide-nav-next" href="describe-2-marks.html">Describe (2 marks) &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: {ACCENT}; width: 100%;" title="Recall: 1 min"></span>
</div>
<span class="guide-quick-ref-total">1 min total</span>
<h4>Formula</h4>
<ol class="guide-quick-ref-steps">
<li>Read the question carefully</li>
<li>Give the specific term or fact</li>
<li>Move on &mdash; do not explain</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>
<div class="sidebar-section guide-other">
<h4>Other Guides</h4>
<ul>
<li><a href="describe-2-marks.html">Describe &mdash; 2 marks</a></li>
<li><a href="calculate-2-marks.html">Calculate &mdash; 2 marks</a></li>
<li><a href="explain-3-marks.html">Explain &mdash; 3 marks</a></li>
<li><a href="compare-and-explain-4-marks.html">Compare and Explain &mdash; 4 marks</a></li>
<li><a href="extended-response-6-marks.html">Extended Response &mdash; 6 marks</a></li>
</ul>
</div>
</aside>'''

# ─────────────────────────────────────────────
# 2 marks — Describe
# ─────────────────────────────────────────────
DESCRIBE_HTML = f'''<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">2 marks</span>
<h1>Describe Questions</h1>
<p class="guide-used-in">Used in: All papers (Biology, Chemistry, Physics)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>&ldquo;Describe&rdquo; questions ask you to state what happens, what you see, or what a pattern or trend shows. You do not need to explain <em>why</em> &mdash; just state the facts clearly. These questions often relate to processes, trends in data, or what you would observe in a practical.</p>
<h3>Marking</h3>
<table class="guide-levels">
<thead><tr><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<tr><td><strong>2</strong></td><td>Two clear, correct descriptive points that address the question directly</td></tr>
<tr><td><strong>1</strong></td><td>One correct point or two vague points</td></tr>
<tr><td>0</td><td>No relevant description or an explanation instead of a description</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Identify what to describe</strong> &mdash; Is it a process (e.g. &ldquo;Describe how vaccination works&rdquo;), a trend (e.g. &ldquo;Describe the pattern in the graph&rdquo;), or an observation (e.g. &ldquo;Describe what you would see&rdquo;)?</div></li>
<li class="guide-step"><span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Make two distinct points</strong> &mdash; Each point should cover a different aspect. For a graph, state the trend and use data. For a process, state the steps in order.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Use scientific language but do not explain</strong> &mdash; The word &ldquo;because&rdquo; is a warning sign. If you catch yourself writing &ldquo;because,&rdquo; you are explaining, not describing.</div></li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: {ACCENT}; width: 100%;">Describe &mdash; 2 min</span>
</div>
<p>About two minutes. Write two clear sentences and move on.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Answer Templates</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Describing a trend</div>
<p class="guide-starter">&ldquo;As [variable X] increases, [variable Y] increases/decreases. For example, at [data point 1]&hellip; and at [data point 2]&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Describing a process</div>
<p class="guide-starter">&ldquo;First, [step 1 happens]. Then, [step 2 happens].&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Describing an observation</div>
<p class="guide-starter">&ldquo;You would see [observation 1]. The [substance/object] would [observation 2].&rdquo;</p>
</div>
</div></div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Model Answers</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>Describe the trend shown in the graph of enzyme activity against temperature. [2 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>As temperature increases from 10&deg;C to 37&deg;C, the rate of enzyme activity increases. Above 37&deg;C, the rate of activity decreases rapidly.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 2/2 &mdash; Two clear points about the trend, with data from the graph.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Describe the test for carbon dioxide gas. [2 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>Bubble the gas through limewater. If carbon dioxide is present, the limewater turns milky (cloudy).</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 2/2 &mdash; States the test and the positive result.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Describe the trend in the graph of stopping distance against speed. [2 marks]</p></div>
<div class="guide-model-paragraph guide-weak-answer"><span class="guide-annotation guide-annotation-weak">1 mark &mdash; no data</span>
<p>As speed goes up, stopping distance goes up because there is more kinetic energy.</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>As speed increases, stopping distance increases. The relationship is not linear &mdash; stopping distance increases more steeply at higher speeds (e.g. at 30 mph it is 23 m, but at 60 mph it is 73 m).</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> The weak answer uses &ldquo;because&rdquo; (explaining, not describing) and lacks data. The strong answer describes the pattern with specific values.</p></div>

</div></div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Explaining instead of describing</strong> &mdash; If the question says &ldquo;Describe,&rdquo; do not write &ldquo;because.&rdquo; State what happens, not why it happens.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Not using data from the graph</strong> &mdash; When describing a trend, quote specific values from the axes. &ldquo;It goes up&rdquo; is worth less than &ldquo;It increases from 20 to 85 between 0 and 60 seconds.&rdquo;</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Only making one point</strong> &mdash; Two marks means two points. Check you have stated two distinct observations or steps.</div></li>
</ul>
</div>

<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="recall-1-mark.html">&larr; Recall (1 mark)</a>
<a class="guide-nav-link guide-nav-next" href="calculate-2-marks.html">Calculate (2 marks) &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: {ACCENT}; width: 100%;" title="Describe: 2 min"></span>
</div>
<span class="guide-quick-ref-total">2 min total</span>
<h4>Formula</h4>
<ol class="guide-quick-ref-steps">
<li>Identify what to describe</li>
<li>Make two distinct points</li>
<li>Use data if a graph is given</li>
<li>Do not explain &mdash; just state</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>
<div class="sidebar-section guide-other">
<h4>Other Guides</h4>
<ul>
<li><a href="recall-1-mark.html">Recall &mdash; 1 mark</a></li>
<li><a href="calculate-2-marks.html">Calculate &mdash; 2 marks</a></li>
<li><a href="explain-3-marks.html">Explain &mdash; 3 marks</a></li>
<li><a href="compare-and-explain-4-marks.html">Compare and Explain &mdash; 4 marks</a></li>
<li><a href="extended-response-6-marks.html">Extended Response &mdash; 6 marks</a></li>
</ul>
</div>
</aside>'''

# ─────────────────────────────────────────────
# 2 marks — Calculate
# ─────────────────────────────────────────────
CALCULATE_HTML = f'''<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">2 marks</span>
<h1>Calculate Questions</h1>
<p class="guide-used-in">Used in: All papers (Biology, Chemistry, Physics)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>Calculate questions test your ability to use scientific formulae, substitute values correctly, and arrive at a numerical answer with the right units. The examiner awards marks for your <strong>working</strong> as well as the final answer &mdash; so even if your arithmetic is wrong, a correct method can still earn marks.</p>
<h3>Marking</h3>
<table class="guide-levels">
<thead><tr><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<tr><td><strong>2</strong></td><td>Correct substitution into the formula AND correct final answer with appropriate units</td></tr>
<tr><td><strong>1</strong></td><td>Correct substitution but wrong calculation, OR correct formula stated but not applied, OR correct answer with no working shown</td></tr>
<tr><td>0</td><td>No relevant working and incorrect answer</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Write the formula</strong> &mdash; Write out the equation you need. In physics, the formula sheet is provided but you still need to select the right one. In chemistry, you may need to recall the formula (e.g. relative formula mass, moles calculations).</div></li>
<li class="guide-step"><span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Substitute the values</strong> &mdash; Replace each symbol with the numbers from the question. Check units match &mdash; convert if needed (e.g. km to m, minutes to seconds, cm&sup3; to dm&sup3;).</div></li>
<li class="guide-step"><span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Calculate and show your working</strong> &mdash; Write each step of the calculation. If you make an arithmetic error, the examiner can still award marks for your method if they can follow your working.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>State the answer with units</strong> &mdash; Write the final answer clearly, including the correct unit (e.g. J, N, mol, &Omega;). If the question asks you to give your answer to a certain number of significant figures or decimal places, do so.</div></li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: {ACCENT}; width: 100%;">Calculate &mdash; 2&ndash;3 min</span>
</div>
<p>About two to three minutes. Write the formula, substitute, calculate, and check your units.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Model Answers</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>A car has a mass of 1200 kg and is travelling at 15 m/s. Calculate the kinetic energy of the car. Use the equation: kinetic energy = 0.5 &times; mass &times; speed&sup2; [2 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>KE = 0.5 &times; m &times; v&sup2;<br/>
KE = 0.5 &times; 1200 &times; 15&sup2;<br/>
KE = 0.5 &times; 1200 &times; 225<br/>
KE = 135,000 J (or 135 kJ)</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 2/2 &mdash; Formula stated, values substituted correctly, correct answer with unit.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Calculate the relative formula mass (M<sub>r</sub>) of calcium carbonate (CaCO<sub>3</sub>). Relative atomic masses: Ca = 40, C = 12, O = 16. [2 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>M<sub>r</sub> = 40 + 12 + (16 &times; 3)<br/>
M<sub>r</sub> = 40 + 12 + 48<br/>
M<sub>r</sub> = 100</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 2/2 &mdash; Clear working, each element accounted for, correct final answer. No unit needed for relative formula mass.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>A resistor has a potential difference of 12 V across it and a current of 0.5 A flowing through it. Calculate the resistance. [2 marks]</p></div>
<div class="guide-model-paragraph guide-weak-answer"><span class="guide-annotation guide-annotation-weak">1 mark &mdash; no formula or working</span>
<p>24 &Omega;</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>R = V &divide; I<br/>
R = 12 &divide; 0.5<br/>
R = 24 &Omega;</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> The answer alone may only score 1 mark (or 2 if an &ldquo;allow&rdquo; applies). Always show working to guarantee full marks.</p></div>

</div></div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Common Unit Conversions</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<table class="guide-levels">
<thead><tr><th>From</th><th>To</th><th>Multiply by</th></tr></thead>
<tbody>
<tr><td>km</td><td>m</td><td>&times; 1000</td></tr>
<tr><td>cm</td><td>m</td><td>&divide; 100</td></tr>
<tr><td>g</td><td>kg</td><td>&divide; 1000</td></tr>
<tr><td>cm&sup3;</td><td>dm&sup3;</td><td>&divide; 1000</td></tr>
<tr><td>minutes</td><td>seconds</td><td>&times; 60</td></tr>
<tr><td>hours</td><td>seconds</td><td>&times; 3600</td></tr>
<tr><td>kJ</td><td>J</td><td>&times; 1000</td></tr>
<tr><td>kW</td><td>W</td><td>&times; 1000</td></tr>
</tbody>
</table>
</div></div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Not showing working</strong> &mdash; If you write only the final answer and it is wrong, you score zero. If you show correct substitution, you score at least 1 mark even with a calculation error.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Forgetting to convert units</strong> &mdash; A common error is using grams when the formula requires kilograms, or cm when it needs metres. Always check the units before substituting.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Missing units on the answer</strong> &mdash; &ldquo;135,000&rdquo; is incomplete. The examiner needs to see &ldquo;135,000 J.&rdquo; Some questions state the unit for you, but if they do not, you must provide it.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Using the wrong formula</strong> &mdash; Read the question carefully. &ldquo;Calculate the force&rdquo; and &ldquo;calculate the work done&rdquo; use different equations even though both involve force.</div></li>
</ul>
</div>

<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="describe-2-marks.html">&larr; Describe (2 marks)</a>
<a class="guide-nav-link guide-nav-next" href="explain-3-marks.html">Explain (3 marks) &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: {ACCENT}; width: 100%;" title="Calculate: 2-3 min"></span>
</div>
<span class="guide-quick-ref-total">2&ndash;3 min total</span>
<h4>Formula</h4>
<ol class="guide-quick-ref-steps">
<li>Write the formula</li>
<li>Substitute the values</li>
<li>Calculate step by step</li>
<li>State answer with units</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>
<div class="sidebar-section guide-other">
<h4>Other Guides</h4>
<ul>
<li><a href="recall-1-mark.html">Recall &mdash; 1 mark</a></li>
<li><a href="describe-2-marks.html">Describe &mdash; 2 marks</a></li>
<li><a href="explain-3-marks.html">Explain &mdash; 3 marks</a></li>
<li><a href="compare-and-explain-4-marks.html">Compare and Explain &mdash; 4 marks</a></li>
<li><a href="extended-response-6-marks.html">Extended Response &mdash; 6 marks</a></li>
</ul>
</div>
</aside>'''

# ─────────────────────────────────────────────
# 3 marks — Explain
# ─────────────────────────────────────────────
EXPLAIN_HTML = f'''<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">3 marks</span>
<h1>Explain Questions</h1>
<p class="guide-used-in">Used in: All papers (Biology, Chemistry, Physics)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>&ldquo;Explain&rdquo; questions require you to give a reason or mechanism for something happening. Unlike &ldquo;Describe&rdquo; questions, you <strong>must</strong> say <em>why</em> or <em>how</em>. The examiner is looking for a chain of logic: cause &rarr; effect, or statement &rarr; reasoning.</p>
<h3>Marking</h3>
<table class="guide-levels">
<thead><tr><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<tr><td><strong>3</strong></td><td>Three valid points, or two well-developed points with a clear chain of reasoning</td></tr>
<tr><td><strong>2</strong></td><td>Two correct points or one point with good development</td></tr>
<tr><td><strong>1</strong></td><td>One basic relevant point</td></tr>
<tr><td>0</td><td>No scientifically correct points</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Identify the scientific concept</strong> &mdash; What topic area does this question relate to? What scientific principle explains the phenomenon?</div></li>
<li class="guide-step"><span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>State what happens</strong> &mdash; Start with a clear factual statement about the process or observation.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Explain why using scientific reasoning</strong> &mdash; Link the cause to the effect. Use &ldquo;This means that&hellip;&rdquo; or &ldquo;This is because&hellip;&rdquo; to build a chain of reasoning.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Develop or add a third point</strong> &mdash; Either develop one of your points further or add a third distinct reason. Use subject-specific terminology to show depth of understanding.</div></li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: {ACCENT}; width: 100%;">Explain &mdash; 3&ndash;4 min</span>
</div>
<p>About three to four minutes. Write a short paragraph with a clear chain of cause and effect.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Answer Templates</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Cause &rarr; Effect chain</div>
<p class="guide-starter">&ldquo;[Statement of what happens]. This is because [scientific reason]. This means that [consequence/further development].&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Three-point approach</div>
<p class="guide-starter">&ldquo;Firstly, [point 1 with reason]. Secondly, [point 2 with reason]. Additionally, [point 3 with reason].&rdquo;</p>
</div>
</div></div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Model Answers</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>Explain why the rate of photosynthesis increases as light intensity increases. [3 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>As light intensity increases, more light energy is available for the light-dependent reactions of photosynthesis. This means that more chlorophyll molecules can absorb light energy, increasing the rate at which water is split and ATP is produced. As a result, more glucose is synthesised per unit of time, until another factor such as carbon dioxide concentration or temperature becomes limiting.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 3/3 &mdash; Three linked points: more light energy available, more absorption by chlorophyll, and the idea of a limiting factor.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Explain why ionic compounds have high melting points. [3 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>Ionic compounds form a giant lattice structure made up of positive and negative ions. There are strong electrostatic forces of attraction between oppositely charged ions throughout the lattice. A large amount of energy is needed to overcome these many strong electrostatic forces, so the melting point is high.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 3/3 &mdash; Structure identified, nature of bonding explained, linked to energy required to break bonds.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Explain why a skydiver reaches terminal velocity. [3 marks]</p></div>
<div class="guide-model-paragraph guide-weak-answer"><span class="guide-annotation guide-annotation-weak">1 mark &mdash; lacks scientific detail</span>
<p>The skydiver stops accelerating because the air resistance is equal to gravity.</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>When the skydiver first jumps, the force of gravity (weight) is greater than the air resistance, so there is a resultant downward force causing acceleration. As speed increases, air resistance increases. Eventually, air resistance equals the weight of the skydiver, so the resultant force is zero and acceleration stops &mdash; the skydiver falls at a constant speed called terminal velocity.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> The weak answer gets the conclusion right but does not explain the process. The strong answer traces the chain: unbalanced forces &rarr; acceleration &rarr; increasing air resistance &rarr; balanced forces &rarr; constant speed.</p></div>

</div></div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Describing instead of explaining</strong> &mdash; &ldquo;The rate increases&rdquo; describes what happens but does not explain why. Always include the scientific reason using &ldquo;because&rdquo; or &ldquo;this means that.&rdquo;</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Missing the chain of reasoning</strong> &mdash; An explanation needs to link cause to effect. &ldquo;Ionic compounds have strong bonds so high melting points&rdquo; jumps from A to C. You must go through B: what <em>type</em> of bonds, and why they require a lot of energy to break.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Using vague language</strong> &mdash; Avoid &ldquo;the particles move around more.&rdquo; Be specific: &ldquo;The particles gain kinetic energy so collide more frequently and with greater energy.&rdquo;</div></li>
</ul>
</div>

<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="calculate-2-marks.html">&larr; Calculate (2 marks)</a>
<a class="guide-nav-link guide-nav-next" href="compare-and-explain-4-marks.html">Compare and Explain (4 marks) &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: {ACCENT}; width: 100%;" title="Explain: 3-4 min"></span>
</div>
<span class="guide-quick-ref-total">3&ndash;4 min total</span>
<h4>Formula</h4>
<ol class="guide-quick-ref-steps">
<li>Identify the scientific concept</li>
<li>State what happens</li>
<li>Say why (cause &rarr; effect)</li>
<li>Develop or add a third point</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>
<div class="sidebar-section guide-other">
<h4>Other Guides</h4>
<ul>
<li><a href="recall-1-mark.html">Recall &mdash; 1 mark</a></li>
<li><a href="describe-2-marks.html">Describe &mdash; 2 marks</a></li>
<li><a href="calculate-2-marks.html">Calculate &mdash; 2 marks</a></li>
<li><a href="compare-and-explain-4-marks.html">Compare and Explain &mdash; 4 marks</a></li>
<li><a href="extended-response-6-marks.html">Extended Response &mdash; 6 marks</a></li>
</ul>
</div>
</aside>'''

# ─────────────────────────────────────────────
# 4 marks — Compare and Explain
# ─────────────────────────────────────────────
COMPARE_HTML = f'''<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">4 marks</span>
<h1>Compare and Explain Questions</h1>
<p class="guide-used-in">Used in: All papers (Biology, Chemistry, Physics)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>These questions ask you to identify similarities or differences between two things and then explain <em>why</em> those differences or similarities exist. The examiner is looking for two skills: accurate comparison <strong>and</strong> scientific reasoning. You need comparative language (&ldquo;whereas,&rdquo; &ldquo;however,&rdquo; &ldquo;both&rdquo;) alongside clear scientific explanations.</p>
<h3>Marking</h3>
<table class="guide-levels">
<thead><tr><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<tr><td><strong>4</strong></td><td>Two clear comparisons, each with a developed scientific explanation</td></tr>
<tr><td><strong>3</strong></td><td>Two comparisons with one well-explained, or one very well-developed comparison plus a second basic point</td></tr>
<tr><td><strong>2</strong></td><td>Two basic comparisons without explanation, or one comparison with explanation</td></tr>
<tr><td><strong>1</strong></td><td>One basic comparison or one relevant scientific point</td></tr>
<tr><td>0</td><td>No relevant comparison or scientific content</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Identify what you are comparing</strong> &mdash; Read the question to establish the two things being compared (e.g. two organisms, two materials, two processes, two data sets).</div></li>
<li class="guide-step"><span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>State the first comparison using comparative language</strong> &mdash; Use &ldquo;whereas,&rdquo; &ldquo;however,&rdquo; &ldquo;in contrast&rdquo; or &ldquo;both&rdquo; to make the comparison explicit. Do not write about each thing separately &mdash; put them together in one sentence.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Explain the scientific reason for the first comparison</strong> &mdash; Link the difference or similarity to the underlying science. Use &ldquo;This is because&hellip;&rdquo;</div></li>
<li class="guide-step"><span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Repeat for a second comparison + explanation</strong> &mdash; Make a second distinct point comparing the two things, then explain it scientifically. This earns the remaining marks.</div></li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: {ACCENT}; width: 25%;">Plan<br/>1 min</span>
<span style="background: {ACCENT_MID}; width: 75%;">Write<br/>4 min</span>
</div>
<p>About five minutes total. Spend a minute identifying two comparison points before writing.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Answer Templates</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Comparison + explanation</div>
<p class="guide-starter">&ldquo;[Thing A] has/does [feature], whereas [Thing B] has/does [different feature]. This is because [scientific reason].&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Similarity + explanation</div>
<p class="guide-starter">&ldquo;Both [Thing A] and [Thing B] [shared feature]. This is because they both [scientific reason].&rdquo;</p>
</div>
</div></div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Model Answers</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>Compare the structures of animal cells and plant cells. Explain the differences. [4 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>Plant cells have a cell wall made of cellulose, whereas animal cells do not have a cell wall. This is because the cell wall provides structural support and rigidity to the plant, allowing it to stand upright without a skeleton. Additionally, plant cells contain chloroplasts, whereas animal cells do not. This is because plants make their own glucose by photosynthesis, which requires chloroplasts to absorb light energy, while animals obtain glucose by eating food.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> 4/4 &mdash; Two clear comparisons (cell wall, chloroplasts), both using comparative language, each with a developed scientific explanation.</p></div>

<hr style="margin: 1.5rem 0; border: none; border-top: 1px solid #e5e2de;"/>

<div class="guide-model-question"><p>Compare the properties of metals and non-metals. Explain the differences. [4 marks]</p></div>
<div class="guide-model-paragraph guide-weak-answer"><span class="guide-annotation guide-annotation-weak">2 marks &mdash; comparison without explanation</span>
<p>Metals conduct electricity but non-metals do not. Metals are shiny and non-metals are dull.</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Full marks</span>
<p>Metals are good conductors of electricity, whereas most non-metals are insulators. This is because metals have delocalised electrons that are free to move through the structure and carry charge. In contrast, metals are malleable (can be bent into shape), whereas non-metals are brittle. This is because the layers of metal ions can slide over each other while maintaining the metallic bonding, but in non-metals the rigid covalent bonds break when force is applied.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> The weak answer states two comparisons but explains neither. The strong answer pairs each comparison with the underlying scientific reason.</p></div>

</div></div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Writing about each thing separately</strong> &mdash; &ldquo;Metals conduct electricity. Non-metals do not.&rdquo; This is two separate statements, not a comparison. Use &ldquo;whereas&rdquo; or &ldquo;however&rdquo; to link them.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Comparing without explaining</strong> &mdash; Stating the differences earns only half the marks. You must explain <em>why</em> the differences exist using scientific reasoning.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Making the same point twice</strong> &mdash; &ldquo;Metals are good conductors&rdquo; and &ldquo;non-metals are bad conductors&rdquo; is one comparison, not two. Find a genuinely different property for your second point.</div></li>
</ul>
</div>

<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="explain-3-marks.html">&larr; Explain (3 marks)</a>
<a class="guide-nav-link guide-nav-next" href="extended-response-6-marks.html">Extended Response (6 marks) &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: {ACCENT}; width: 25%;" title="Plan: 1 min"></span>
<span style="background: {ACCENT_MID}; width: 75%;" title="Write: 4 min"></span>
</div>
<span class="guide-quick-ref-total">5 min total</span>
<h4>Formula</h4>
<ol class="guide-quick-ref-steps">
<li>Identify the two things to compare</li>
<li>State comparison 1 + explain why</li>
<li>State comparison 2 + explain why</li>
<li>Use comparative language throughout</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>
<div class="sidebar-section guide-other">
<h4>Other Guides</h4>
<ul>
<li><a href="recall-1-mark.html">Recall &mdash; 1 mark</a></li>
<li><a href="describe-2-marks.html">Describe &mdash; 2 marks</a></li>
<li><a href="calculate-2-marks.html">Calculate &mdash; 2 marks</a></li>
<li><a href="explain-3-marks.html">Explain &mdash; 3 marks</a></li>
<li><a href="extended-response-6-marks.html">Extended Response &mdash; 6 marks</a></li>
</ul>
</div>
</aside>'''

# ─────────────────────────────────────────────
# 6 marks — Extended Response
# ─────────────────────────────────────────────
EXTENDED_HTML = f'''<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">6 marks</span>
<h1>Extended Response Questions</h1>
<p class="guide-used-in">Used in: All papers (Biology, Chemistry, Physics)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>The 6-mark extended response is the highest-value question on each paper. It is marked using a <strong>levels of response</strong> mark scheme, which means the examiner reads your whole answer and decides which level it fits into. There is an asterisk (*) next to the question to show that quality of written communication is assessed. The examiner wants a logically structured, detailed answer that uses scientific terminology accurately and builds a clear argument or explanation.</p>
<h3>Level Descriptors</h3>
<table class="guide-levels">
<thead><tr><th>Level</th><th>Marks</th><th>What You Need</th></tr></thead>
<tbody>
<tr><td><strong>Level 3</strong></td><td>5&ndash;6</td><td>Detailed, coherent explanation with a logical structure; accurate and relevant scientific terminology; all key points addressed; clear line of reasoning throughout</td></tr>
<tr><td><strong>Level 2</strong></td><td>3&ndash;4</td><td>Some relevant scientific points with some explanation; logical sequence attempted but may lack coherence; some scientific terminology used</td></tr>
<tr><td><strong>Level 1</strong></td><td>1&ndash;2</td><td>Simple, basic statements; limited scientific vocabulary; disorganised or list-like response</td></tr>
<tr><td></td><td>0</td><td>No relevant scientific content</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Formula</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Plan before you write (2&ndash;3 minutes)</strong> &mdash; Jot down 4&ndash;5 key scientific points you need to include. Put them in a logical order. This planning stage is the difference between Level 2 and Level 3.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Write a brief opening statement</strong> &mdash; One sentence that shows you understand the question and sets the direction of your answer.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Develop each point in a logical sequence</strong> &mdash; Each point should connect to the next. Use connectives: &ldquo;This means that&hellip;,&rdquo; &ldquo;As a result&hellip;,&rdquo; &ldquo;Furthermore&hellip;,&rdquo; &ldquo;However&hellip;&rdquo; to build a chain of reasoning. Use correct scientific terminology throughout.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>If it&rsquo;s an evaluation question</strong> &mdash; Discuss advantages <em>and</em> disadvantages, or arguments for <em>and</em> against. Reach a conclusion or judgement supported by your scientific reasoning.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Re-read your answer</strong> &mdash; Check that your answer flows logically, uses correct spelling of scientific terms, and addresses every part of the question.</div></li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: {ACCENT}; width: 20%;">Plan<br/>2 min</span>
<span style="background: {ACCENT_MID}; width: 65%;">Write<br/>7 min</span>
<span style="background: {ACCENT_LIGHT}; width: 15%;">Check<br/>1 min</span>
</div>
<p>About ten minutes total. This is the biggest question on the paper &mdash; do not rush it. Planning is essential for a Level 3 response.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Useful Connectives and Phrases</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Building a chain of reasoning</div>
<p class="guide-starter">&ldquo;This means that&hellip; / As a result&hellip; / Therefore&hellip; / Consequently&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Adding points</div>
<p class="guide-starter">&ldquo;Furthermore&hellip; / In addition&hellip; / Another factor is&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Evaluating / contrasting</div>
<p class="guide-starter">&ldquo;However&hellip; / On the other hand&hellip; / A disadvantage of this is&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Concluding</div>
<p class="guide-starter">&ldquo;Overall&hellip; / In conclusion&hellip; / The most significant factor is&hellip; because&hellip;&rdquo;</p>
</div>
</div></div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Model Answer</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>Describe how the body responds to a bacterial infection and explain how vaccination can prevent the disease from developing. [6 marks]</p></div>
<div class="guide-model-paragraph"><span class="guide-annotation">Level 3 &mdash; 6 marks</span>
<p>When bacteria enter the body, white blood cells detect foreign antigens on the surface of the pathogens. Lymphocytes are activated and produce specific antibodies that are complementary in shape to the antigens on the bacteria. These antibodies bind to the antigens, causing the bacteria to clump together (agglutination) so that they can be destroyed by phagocytes, which engulf and digest the pathogens.</p>
<p>After the infection has been cleared, memory lymphocytes remain in the blood. If the same pathogen enters the body again, these memory cells recognise the antigen and produce the correct antibodies much more quickly and in greater quantities. This is called the secondary immune response, and it is usually fast enough to destroy the pathogen before symptoms develop.</p>
<p>Vaccination works by introducing a dead or weakened form of the pathogen (or just its antigens) into the body. This stimulates the immune system to produce antibodies and memory cells without causing the disease. As a result, if the person is later exposed to the live pathogen, their immune system can mount a rapid secondary response, preventing the disease from developing.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> Level 3, 6/6 &mdash; Comprehensive and logically sequenced. Covers initial immune response, memory cells, secondary response, and how vaccination exploits this. Accurate scientific terminology throughout (antigens, lymphocytes, antibodies, phagocytes, memory cells, secondary immune response). Clear line of reasoning from infection to vaccination.</p></div>

</div></div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Weak Answer &mdash; What Not to Do</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">

<div class="guide-model-question"><p>Describe how the body responds to a bacterial infection and explain how vaccination can prevent the disease from developing. [6 marks]</p></div>
<div class="guide-model-paragraph guide-weak-answer"><span class="guide-annotation guide-annotation-weak">Level 1 &mdash; 2 marks</span>
<p>White blood cells fight off the bacteria. They make antibodies. A vaccine has a dead version of the pathogen. It helps your body fight it next time.</p></div>
<div class="guide-model-mark"><p><strong>Examiner:</strong> Level 1 &mdash; basic statements with no development or chain of reasoning. No explanation of how antibodies work, no mention of memory cells, no link between vaccination and the secondary immune response. List-like rather than a coherent explanation.</p></div>

</div></div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>No plan = disorganised answer</strong> &mdash; Students who skip planning almost always produce Level 1&ndash;2 responses because their points are jumbled and lack a logical flow. Spend two minutes planning.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Writing a list of facts</strong> &mdash; The examiner is assessing your ability to construct a coherent explanation, not list bullet points. Use full sentences and connectives to build an argument.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Vague scientific language</strong> &mdash; &ldquo;White blood cells fight bacteria&rdquo; is Level 1. &ldquo;Lymphocytes produce specific antibodies complementary to the pathogen&rsquo;s antigens&rdquo; is Level 3. Precision matters.</div></li>
<li class="guide-mistake"><span class="guide-mistake-icon">\u274c</span><div><strong>Not answering every part of the question</strong> &mdash; If the question says &ldquo;describe AND explain,&rdquo; you must do both. Ignoring half the question caps you at Level 2 regardless of quality.</div></li>
</ul>
</div>

<nav class="guide-nav">
<a class="guide-nav-link guide-nav-prev" href="compare-and-explain-4-marks.html">&larr; Compare and Explain (4 marks)</a>
<a class="guide-nav-link guide-nav-next" href="recall-1-mark.html">Recall (1 mark) &rarr;</a>
</nav>
<a class="back-link" href="index.html">&larr; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: {ACCENT}; width: 20%;" title="Plan: 2 min"></span>
<span style="background: {ACCENT_MID}; width: 65%;" title="Write: 7 min"></span>
<span style="background: {ACCENT_LIGHT}; width: 15%;" title="Check: 1 min"></span>
</div>
<span class="guide-quick-ref-total">10 min total</span>
<h4>Must Cover</h4>
<ol class="guide-quick-ref-steps">
<li>Plan 4&ndash;5 key points</li>
<li>Brief opening statement</li>
<li>Develop points in logical sequence</li>
<li>Use scientific terminology</li>
<li>Evaluate if required (pros/cons)</li>
<li>Re-read and check</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"></polygon></svg>
<span>Video walkthrough coming soon</span>
</div>
</div>
<div class="sidebar-section guide-other">
<h4>Other Guides</h4>
<ul>
<li><a href="recall-1-mark.html">Recall &mdash; 1 mark</a></li>
<li><a href="describe-2-marks.html">Describe &mdash; 2 marks</a></li>
<li><a href="calculate-2-marks.html">Calculate &mdash; 2 marks</a></li>
<li><a href="explain-3-marks.html">Explain &mdash; 3 marks</a></li>
<li><a href="compare-and-explain-4-marks.html">Compare and Explain &mdash; 4 marks</a></li>
</ul>
</div>
</aside>'''


# ─────────────────────────────────────────────
# All guides definition
# ─────────────────────────────────────────────
GUIDES = [
    {"slug": "index",                          "title": "Exam Technique",                                  "content_html": HUB_HTML,      "sort_order": 0},
    {"slug": "recall-1-mark",                  "title": "1 Mark \u2014 Recall Questions",                  "content_html": RECALL_HTML,    "sort_order": 1},
    {"slug": "describe-2-marks",               "title": "2 Marks \u2014 Describe Questions",               "content_html": DESCRIBE_HTML,  "sort_order": 2},
    {"slug": "calculate-2-marks",              "title": "2 Marks \u2014 Calculate Questions",              "content_html": CALCULATE_HTML, "sort_order": 3},
    {"slug": "explain-3-marks",                "title": "3 Marks \u2014 Explain Questions",                "content_html": EXPLAIN_HTML,   "sort_order": 4},
    {"slug": "compare-and-explain-4-marks",    "title": "4 Marks \u2014 Compare and Explain Questions",    "content_html": COMPARE_HTML,   "sort_order": 5},
    {"slug": "extended-response-6-marks",      "title": "6 Marks \u2014 Extended Response Questions",      "content_html": EXTENDED_HTML,  "sort_order": 6},
]


def main():
    sb = get_client()

    for subject_id, subject_name in [(SCIENCE_ID, "science"), (SEPARATE_ID, "separate-sciences")]:
        print(f"\n{'='*60}")
        print(f"Inserting guides for: {subject_name} ({subject_id})")
        print(f"{'='*60}")

        for guide in GUIDES:
            row = {
                "subject_id": subject_id,
                "guide_type": "exam-technique",
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

    print("\nDone! Inserted 7 guides x 2 subjects = 14 rows total.")


if __name__ == "__main__":
    main()
