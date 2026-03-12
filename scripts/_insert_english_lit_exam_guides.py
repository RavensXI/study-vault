"""Insert English Literature (AQA 8702) exam technique guides into Supabase."""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

sb = get_client()
SUBJECT_ID = 'b3526a0a-254c-49e9-bb42-65aa3aadb2ea'

# ============================================================
# HUB PAGE
# ============================================================
hub_html = """<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Exam Technique Guides</h1>
<p>Step-by-step guides for every AQA GCSE English Literature question type. Learn the formula, study a model answer, and avoid the common mistakes that cost marks.</p>
</div>
</div>
<div class="guide-hub" style="grid-template-columns: 1fr; max-width: 780px;">
<div class="guide-paper" style="--paper-accent: #7c3aed; --paper-light: #f5f3ff;">
<div class="guide-paper-header">
<h2>AQA GCSE English Literature (8702)</h2>
<span class="guide-paper-ref">Paper 1 &amp; Paper 2</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="quote-analysis.html">
<span class="guide-question-marks">4 marks</span>
<h3>Quote Analysis</h3>
<p>Close reading of a specific moment in the text. Identify a technique, explain the effect, and link to context.</p>
</a>
<a class="guide-question-card" href="extract-analysis.html">
<span class="guide-question-marks">8 marks</span>
<h3>Extract Analysis</h3>
<p>Analyse how a writer uses language and structure in a given extract. Focus on AO1 and AO2.</p>
</a>
<a class="guide-question-card" href="extended-response.html">
<span class="guide-question-marks">12 marks</span>
<h3>Extended Response</h3>
<p>Explore how a character or theme is presented across the whole text using evidence from different parts.</p>
</a>
<a class="guide-question-card" href="essay-response.html">
<span class="guide-question-marks">30 + 4 SPaG</span>
<h3>Essay Response</h3>
<p>The full exam essay. Covers Paper 1 extract-based essays and Paper 2 essay-only questions. SPaG marks explained.</p>
</a>
<a class="guide-question-card" href="anthology-comparison.html">
<span class="guide-question-marks">30 marks</span>
<h3>Anthology Comparison (Poetry)</h3>
<p>Paper 2 Section B. Given one poem, compare with another of your choice. How to plan, structure and write your comparison.</p>
</a>
<a class="guide-question-card" href="unseen-poetry-analysis.html">
<span class="guide-question-marks">24 marks</span>
<h3>Unseen Poetry Analysis</h3>
<p>Paper 2 Section C Q1. How to tackle a poem you have never seen before in the exam.</p>
</a>
<a class="guide-question-card" href="unseen-poetry-comparison.html">
<span class="guide-question-marks">8 marks</span>
<h3>Unseen Poetry Comparison</h3>
<p>Paper 2 Section C Q2. Compare two unseen poems — a focused comparison written under time pressure.</p>
</a>
</div>
</div>
</div>"""

# ============================================================
# 1. QUOTE ANALYSIS — 4 marks
# ============================================================
quote_analysis_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">4 marks</span>
<h1>Quote Analysis</h1>
<p class="guide-used-in">Used in: Paper 1 Section A (Shakespeare), Paper 1 Section B (19th-century novel), Paper 2 Section A (modern prose/drama)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>Quote analysis questions ask you to look closely at a specific moment in the text — often a short extract or a single quotation highlighted in the question. The examiner wants to see you identifying a language technique, explaining the effect it creates on the reader, and linking your analysis to the writer's intentions or context. This is AO1 (critical response) and AO2 (language/form/structure) working together.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>AO2 is the dominant assessment objective here. Simply saying what happens (AO1 plot summary) without analysing HOW language works will not score well. Always zoom in on specific words and techniques.</p>
</div>
<h3>Mark Scheme Levels</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>4</strong></td><td>Clear technique identified, effect explained with subject terminology, brief contextual link or inference about writer's intention</td></tr>
<tr><td><strong>3</strong></td><td>Technique identified and effect explained, but contextual link is thin or absent</td></tr>
<tr><td><strong>2</strong></td><td>Some awareness of technique or effect, but mainly descriptive or paraphrase-based</td></tr>
<tr><td><strong>1</strong></td><td>Simple relevant comment on the text with no technical language</td></tr>
<tr><td><strong>0</strong></td><td>Nothing relevant</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Identify the technique</strong> — Name the specific literary or language technique the writer is using (e.g. metaphor, sibilance, semantic field, juxtaposition). Be precise — &ldquo;the writer uses language&rdquo; is not enough.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Embed the quotation</strong> — Weave a short, focused quotation into your sentence rather than copying out long chunks. One to five words is usually enough to anchor your point.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Explain the effect</strong> — What does this technique make the reader feel, think, or understand? Use phrases like &ldquo;this suggests&rdquo;, &ldquo;this implies&rdquo;, or &ldquo;the effect is&rdquo; to signal your analysis.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Link to context or intention</strong> — Connect your analysis to the writer&rsquo;s purpose or historical/social context. Why might the writer have made this choice? What were they trying to show about society, a character, or a theme?</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 20%;">Read &amp; select<br/>1 min</span>
<span style="background: #8b5cf6; width: 50%;">Write<br/>3 min</span>
<span style="background: #a78bfa; width: 30%;">Check<br/>1 min</span>
</div>
<p>You have roughly 4&ndash;5 minutes for a 4-mark quote analysis response. Keep it tight: one technique, one embedded quote, one explanation of effect, one contextual link. Do not write an essay &mdash; save your time for the higher-mark questions.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Paragraph Template (P-E-E-C)</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Point</div>
<p class="guide-starter">&ldquo;[Writer] uses [technique] when [character/narrator] says &lsquo;[short quote]&rsquo;&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Effect</div>
<p class="guide-starter">&ldquo;This suggests / implies / conveys [effect on reader / meaning]&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Context Link</div>
<p class="guide-starter">&ldquo;[Writer] may have chosen this because [contextual reason / writer&rsquo;s intention]&hellip;&rdquo;</p>
</div>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Answer</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>How does Priestley use language to present Mr Birling in this extract? [4 marks]<br/><em>(Extract includes: &ldquo;a man has to make his own way&rdquo;)</em></p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Technique + embedded quote</span>
<p>Priestley uses an imperative tone through Birling&rsquo;s assertion that &ldquo;a man has to make his own way&rdquo;, presenting him as someone who believes firmly in individual responsibility over community.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Effect explained</span>
<p>The modal verb &ldquo;has&rdquo; implies necessity and inevitability, suggesting Birling sees self-interest not just as sensible but as a law of nature &mdash; a view the inspector (and Priestley) will systematically undermine.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Context link</span>
<p>Writing in 1945 but setting the play in 1912, Priestley uses Birling to critique the capitalist attitudes that he believed had contributed to the social inequalities driving two world wars.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> 4/4 &mdash; Clear technique, embedded quotation, well-explained effect, strong contextual link.</p>
</div>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Weak vs Strong: Spot the Difference</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>How does Priestley use language to present Mr Birling? [4 marks]</p>
</div>
<h3>Weak Answer</h3>
<div class="guide-model-paragraph guide-weak-answer">
<span class="guide-annotation guide-annotation-weak">Plot retelling, no technique named</span>
<p>Mr Birling says &ldquo;a man has to make his own way&rdquo;. This shows he is selfish and doesn&rsquo;t care about other people. He is a bad person.</p>
</div>
<h3>Strong Answer</h3>
<div class="guide-model-paragraph">
<span class="guide-annotation">Technique + effect + context</span>
<p>Priestley uses an imperative through Birling&rsquo;s declaration that &ldquo;a man has to make his own way&rdquo;. The modal verb &ldquo;has&rdquo; conveys a sense of absolute necessity, implying Birling views self-reliance not as a choice but as a moral law. Priestley uses this to satirise the capitalist ruling class whose individualism, he believed, caused the social suffering symbolised by Eva Smith.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Naming a technique without explaining the effect</strong> &mdash; &ldquo;Priestley uses a metaphor&rdquo; scores 1 mark at most. You must say what that metaphor does to the reader.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Copying out a long quotation</strong> &mdash; Examiners reward analysis, not transcription. Embed just the key words so your explanation is the focus.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Telling the story</strong> &mdash; AO2 is about HOW the writer writes, not WHAT happens in the text. Avoid &ldquo;this shows he is mean&rdquo; without explaining the language that creates that impression.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Skipping the context link</strong> &mdash; For 4 marks you need all four elements. A brief contextual sentence lifts a 3-mark answer to 4.</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 20%;" title="Read: 1 min"></span>
<span style="background: #8b5cf6; width: 50%;" title="Write: 3 min"></span>
<span style="background: #a78bfa; width: 30%;" title="Check: 1 min"></span>
</div>
<span class="guide-quick-ref-total">5 min total</span>
<h4>P-E-E-C Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Point (technique + quote)</li>
<li>Effect (what it does)</li>
<li>Elaborate (deeper meaning)</li>
<li>Context link</li>
</ol>
<h4>Key AOs</h4>
<ul>
<li>AO1: Critical response &amp; reference</li>
<li>AO2: Language/form/structure analysis</li>
<li>AO3: Context link</li>
</ul>
</div>
</aside>"""

# ============================================================
# 2. EXTRACT ANALYSIS — 8 marks
# ============================================================
extract_analysis_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">8 marks</span>
<h1>Extract Analysis</h1>
<p class="guide-used-in">Used in: Paper 1 Section A (Shakespeare), Paper 2 Section A (modern prose/drama)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>Extract analysis questions give you a passage from the text and ask how the writer uses language and structure to achieve a particular effect. You are expected to analyse specific language choices (AO2) while also showing you understand the text&rsquo;s meaning and themes (AO1). The focus is on the extract itself, though brief links beyond it can strengthen your response.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>AO2 is the primary focus: examiners are looking for analysis of language (word choice, imagery, tone) and structure (how the extract is organised, sentence length, paragraph position). Do not write a general essay about the theme &mdash; anchor every point to the text.</p>
</div>
<h3>Mark Scheme Levels</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>Level</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>7&ndash;8</strong></td><td>Level 4</td><td>Perceptive, detailed analysis. Confident use of subject terminology. Convincing interpretation of writer&rsquo;s methods and their effects.</td></tr>
<tr><td><strong>5&ndash;6</strong></td><td>Level 3</td><td>Clear explanation of how the writer uses language/structure. Relevant use of subject terminology to support analysis.</td></tr>
<tr><td><strong>3&ndash;4</strong></td><td>Level 2</td><td>Some understanding of how language is used. Attempts to comment on effect. Terminology may be applied inconsistently.</td></tr>
<tr><td><strong>1&ndash;2</strong></td><td>Level 1</td><td>Simple comments. Mostly paraphrase or assertion without evidence of analysis.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Read the question focus</strong> &mdash; What does the question ask you to explore? A character&rsquo;s emotions? The atmosphere? A relationship? Keep that focus in mind throughout.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Annotate the extract</strong> &mdash; Underline three to four specific moments: a striking phrase, a pattern (e.g. repeated imagery), a structural choice (e.g. short sentence at a turning point). Each annotation becomes a paragraph.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Write focused analytical paragraphs</strong> &mdash; For each point: name the technique, embed a short quotation, explain the effect on the reader, and explore the writer&rsquo;s intention. Aim for two to three substantial paragraphs.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Comment on structure</strong> &mdash; As well as language, consider how the extract is structured. Where does tension build? What is the effect of the extract&rsquo;s opening or closing lines? Does sentence length vary for effect?</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Link beyond the extract briefly</strong> &mdash; A sentence or two connecting the extract to a wider theme or character development shows you know the whole text and can elevate a Level 3 to Level 4 response.</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 15%;">Read &amp; annotate<br/>2 min</span>
<span style="background: #8b5cf6; width: 60%;">Write<br/>7 min</span>
<span style="background: #a78bfa; width: 25%;">Check &amp; extend<br/>1 min</span>
</div>
<p>Spend around 10 minutes on an 8-mark extract question. Use two minutes to read and annotate, then seven minutes writing. Aim for two or three well-developed paragraphs rather than five thin ones.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Paragraph Template</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Language Point</div>
<p class="guide-starter">&ldquo;[Writer] creates [effect] through [technique]. The [word/phrase] &lsquo;[quote]&rsquo; suggests [meaning/effect], implying [deeper interpretation].&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Structure Point</div>
<p class="guide-starter">&ldquo;Structurally, [writer] places [detail] at the [opening/end/centre] of the extract. This [effect], mirroring [character&rsquo;s state/theme].&rdquo;</p>
</div>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Answer</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>How does Dickens use language and structure in this extract to present Scrooge&rsquo;s transformation? [8 marks]</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Language: technique + effect + interpretation</span>
<p>Dickens presents Scrooge&rsquo;s transformation through a shift in his use of exclamatory language. Where earlier passages are characterised by cold, clipped commands, the extract sees Scrooge cry out &ldquo;I am as light as a feather, I am as happy as an angel&rdquo;. The anaphoric repetition of &ldquo;I am&rdquo; conveys an almost childlike self-discovery &mdash; as though Scrooge is surprised by his own capacity for joy, having suppressed it for decades.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Structure: sentence length / pace</span>
<p>Structurally, Dickens accelerates the pace in this extract through a series of short, exclamatory sentences. The staccato rhythm &mdash; &ldquo;Glorious. Splendid. Magnificent.&rdquo; &mdash; mimics the burst of energy Scrooge feels, contrasting sharply with the measured, slow prose of the opening stave. This structural shift signals to the reader that the transformation is not just emotional but physical: Scrooge is literally reanimated.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> 7&ndash;8 &mdash; Perceptive analysis of language and structure, confident use of terminology (anaphora, staccato, stave), convincing interpretation.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Analysing only language, not structure</strong> &mdash; AO2 covers both language AND form/structure. Always include at least one structural observation (sentence length, positioning, shifts in tone, paragraph breaks).</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Writing a general essay about the theme</strong> &mdash; You must be anchored in the given extract. Every paragraph must reference specific words or moments from the passage.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Too many thin points</strong> &mdash; Two or three perceptive, well-developed paragraphs score higher than five surface-level observations. Depth beats breadth.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Vague effect statements</strong> &mdash; &ldquo;This creates tension&rdquo; needs developing. Tension in whom? What does it make the reader anticipate? Push every analysis one sentence further.</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 15%;" title="Read: 2 min"></span>
<span style="background: #8b5cf6; width: 60%;" title="Write: 7 min"></span>
<span style="background: #a78bfa; width: 25%;" title="Check: 1 min"></span>
</div>
<span class="guide-quick-ref-total">10 min total</span>
<h4>Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Read &amp; annotate (3&ndash;4 moments)</li>
<li>2&ndash;3 language paragraphs</li>
<li>1 structure paragraph</li>
<li>Brief link beyond extract</li>
</ol>
<h4>Key AOs</h4>
<ul>
<li>AO1: Critical response</li>
<li>AO2: Language &amp; structure (primary)</li>
</ul>
</div>
</aside>"""

# ============================================================
# 3. EXTENDED RESPONSE — 12 marks
# ============================================================
extended_response_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">12 marks</span>
<h1>Extended Response</h1>
<p class="guide-used-in">Used in: Paper 1 Section A (Shakespeare), Paper 1 Section B (19th-century novel), Paper 2 Section A (modern prose/drama)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>The 12-mark extended response asks you to explore how a writer presents a character, theme, or relationship across the whole text (or in relation to a given extract plus beyond). You need to select your own evidence and build a sustained, analytical argument. This tests AO1 (your own interpretation, supported by evidence) and AO2 (analysis of language, form, and structure) equally.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>You must show awareness of the whole text, not just one part. Use at least two or three separate moments from different points in the text to show a character or theme developing, changing, or remaining consistent.</p>
</div>
<h3>Mark Scheme Levels</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>Level</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>10&ndash;12</strong></td><td>Level 4</td><td>Perceptive, well-structured argument. Convincing analysis of methods. Evidence selected from across the text. Subject terminology used accurately and meaningfully.</td></tr>
<tr><td><strong>7&ndash;9</strong></td><td>Level 3</td><td>Clear, explained analysis. Evidence from different points in the text. Relevant use of terminology.</td></tr>
<tr><td><strong>4&ndash;6</strong></td><td>Level 2</td><td>Some relevant points. Evidence used but analysis may be surface-level. Partial coverage of the text.</td></tr>
<tr><td><strong>1&ndash;3</strong></td><td>Level 1</td><td>Simple observations. Limited or no textual evidence. Mainly plot retelling.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Plan before you write</strong> &mdash; Spend two minutes jotting down three to four moments from the text that show the character or theme in different ways. Think about beginning, middle, and end of the text for variety.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Write a direct opening</strong> &mdash; State your main argument in your opening sentence. Do not rewrite the question or start with a general statement. Tell the examiner your interpretation straight away.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Write analytical paragraphs (P-E-E-C)</strong> &mdash; For each moment you selected: make a Point about the character/theme, provide an Embedded quotation, Explain the effect of specific language choices, make a Context link to writer&rsquo;s purpose or social/historical context.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Show development or contrast</strong> &mdash; Does the character change? Does the theme develop? The strongest responses track a journey across the text, not just list separate observations.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Write a brief conclusion</strong> &mdash; One or two sentences restating your overall interpretation in light of your analysis. Avoid simply listing what you said &mdash; reach a final judgement.</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 15%;">Plan<br/>2 min</span>
<span style="background: #8b5cf6; width: 65%;">Write<br/>11 min</span>
<span style="background: #a78bfa; width: 20%;">Conclude &amp; check<br/>2 min</span>
</div>
<p>Approximately 15 minutes for a 12-mark question. Three well-developed paragraphs (each around 100&ndash;130 words) with a brief introduction and conclusion is the target. Do not exceed this &mdash; the essay-length questions are worth more marks per minute.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Answer</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>How does Priestley present the theme of responsibility in <em>An Inspector Calls</em>? [12 marks]</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Direct opening argument</span>
<p>Priestley presents responsibility as a moral obligation that the older generation wilfully avoids, using the younger characters and the Inspector to argue that collective accountability is the only path to social justice.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Paragraph 1: language analysis</span>
<p>Birling&rsquo;s dismissal of shared responsibility is established early through his bombastic monologue, in which he declares that &ldquo;a man has to make his own way&rdquo;. The modal verb &ldquo;has&rdquo; positions individualism as natural law rather than a choice, revealing a world view Priestley regarded as the root cause of social inequality. This is deliberately exposed as dangerous &mdash; Birling&rsquo;s confident pronouncements are shown to be wrong by the play&rsquo;s end.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Paragraph 2: development / contrast</span>
<p>In contrast, Sheila&rsquo;s arc enacts the acceptance of responsibility Priestley advocates. After the Inspector&rsquo;s interrogation, she tells her parents &ldquo;I know I&rsquo;m to blame and I&rsquo;m desperately sorry&rdquo;. The adverb &ldquo;desperately&rdquo; conveys genuine remorse rather than polite regret, suggesting that true responsibility requires emotional engagement, not just acknowledgement. Priestley may be implying that the younger generation, represented by Sheila, still has the capacity for moral growth.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Brief conclusion</span>
<p>Ultimately, Priestley uses the contrast between the Birlings&rsquo; resistance and Sheila&rsquo;s transformation to argue that responsibility is a choice society must consciously make &mdash; a message given urgent relevance by the play&rsquo;s 1945 audience, rebuilding after the collective catastrophe of the Second World War.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> 11&ndash;12 &mdash; Clear argument sustained across the text, perceptive language analysis, strong contextual links.</p>
</div>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Weak vs Strong: Spot the Difference</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<h3>Weak Opening</h3>
<div class="guide-model-paragraph guide-weak-answer">
<span class="guide-annotation guide-annotation-weak">Restates question, vague</span>
<p>In <em>An Inspector Calls</em>, Priestley presents responsibility in many different ways throughout the play.</p>
</div>
<h3>Strong Opening</h3>
<div class="guide-model-paragraph">
<span class="guide-annotation">Direct argument from line one</span>
<p>Priestley presents responsibility as a moral choice that the older Birlings evade while the younger generation &mdash; Sheila and Eric &mdash; begin to embrace it, suggesting that social change is possible but only through genuine self-reflection.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Using only one part of the text</strong> &mdash; A 12-mark response must show knowledge of the whole text. Draw evidence from at least two or three distinct moments.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Retelling the plot</strong> &mdash; &ldquo;Then the Inspector arrives and asks everyone questions&rdquo; is AO1 plot summary, not analysis. Every sentence should be making an analytical point.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Forgetting context</strong> &mdash; AO3 context marks are available here. Link to the writer&rsquo;s historical/social context in at least one or two paragraphs.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Vague opening sentence</strong> &mdash; &ldquo;Priestley presents responsibility in many ways&rdquo; wastes your first sentence. State your argument immediately.</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 15%;" title="Plan: 2 min"></span>
<span style="background: #8b5cf6; width: 65%;" title="Write: 11 min"></span>
<span style="background: #a78bfa; width: 20%;" title="Check: 2 min"></span>
</div>
<span class="guide-quick-ref-total">15 min total</span>
<h4>Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Direct opening argument</li>
<li>3 analytical paragraphs (P-E-E-C)</li>
<li>Brief conclusion</li>
</ol>
<h4>Key AOs</h4>
<ul>
<li>AO1: Argument + evidence</li>
<li>AO2: Language analysis</li>
<li>AO3: Context links</li>
</ul>
</div>
</aside>"""

# ============================================================
# 4. ESSAY RESPONSE — 30 marks + 4 SPaG
# ============================================================
essay_response_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">30 + 4 SPaG marks</span>
<h1>Essay Response</h1>
<p class="guide-used-in">Paper 1 Section A (Shakespeare, 30+4 SPaG) &bull; Paper 1 Section B (19th-century novel, 30+4 SPaG) &bull; Paper 2 Section A (modern prose/drama, 30 marks)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>The essay response is the highest-value question on each paper. You must write a sustained analytical essay exploring a theme, character, relationship, or writer&rsquo;s method across the whole text. AO1 (your argument and evidence), AO2 (language analysis), and AO3 (context) all count. On Paper 1 and Paper 2 Section A, an additional 4 marks are awarded for SPaG &mdash; spelling, punctuation, and grammar.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>SPaG marks (Paper 1 both sections and Paper 2 Section A only): these 4 marks reward accurate spelling of subject-specific vocabulary, correct use of punctuation (especially commas and apostrophes), and grammatically sound sentences. They are easy to earn if you proofread.</p>
</div>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>Paper 2 Section A (modern prose/drama) has two questions: one on a named character and one on a theme. You choose one. Both are 30 marks but do NOT carry SPaG marks &mdash; those are on Paper 2 Section A only for the prose/drama text you studied.</p>
</div>
<h3>Mark Scheme Levels (30 marks)</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>Level</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>25&ndash;30</strong></td><td>Level 4</td><td>Perceptive, coherent argument. Convincing analysis of language/structure/form. Well-selected evidence from across the text. Assured use of terminology. Strong contextual understanding (AO3).</td></tr>
<tr><td><strong>19&ndash;24</strong></td><td>Level 3</td><td>Clear, explained analysis. Good range of evidence. Relevant terminology. Context linked to the text&rsquo;s meaning.</td></tr>
<tr><td><strong>13&ndash;18</strong></td><td>Level 2</td><td>Some analytical points with supporting evidence. Coverage of the text but analysis may be surface-level or uneven.</td></tr>
<tr><td><strong>7&ndash;12</strong></td><td>Level 1</td><td>Simple observations with limited evidence. Mostly descriptive or plot-based.</td></tr>
<tr><td><strong>1&ndash;6</strong></td><td>Foundation</td><td>Very basic response. Little evidence. No clear argument.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Paper 1 vs Paper 2: Key Differences</h2>
<table class="guide-levels">
<thead>
<tr><th>Feature</th><th>Paper 1</th><th>Paper 2 Sec A</th></tr>
</thead>
<tbody>
<tr><td>Texts</td><td>Shakespeare + 19th-century novel</td><td>Modern prose or drama</td></tr>
<tr><td>Question format</td><td>Extract given + &ldquo;and the rest of the play/novel&rdquo;</td><td>No extract &mdash; whole text essay</td></tr>
<tr><td>SPaG marks</td><td>Yes (4 marks, both sections)</td><td>Yes (4 marks, Section A only)</td></tr>
<tr><td>Time suggested</td><td>~50 min per section</td><td>~45 min</td></tr>
</tbody>
</table>
<p>On Paper 1, you are given an extract to analyse first, then must go &ldquo;beyond&rdquo; it to discuss the rest of the text. On Paper 2 Section A, you write a whole-text essay with no extract provided &mdash; your choice of evidence is entirely your own.</p>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Decode the question carefully</strong> &mdash; Identify the key word (How? Why? To what extent?), the focus (character, theme, method), and any specific instruction (&ldquo;starting with this extract&rdquo;).</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Plan in two minutes</strong> &mdash; Note four or five key moments from across the text and a clear overarching argument. Your plan does not need full sentences &mdash; key words, moments, and quotes are enough.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Write a one-sentence thesis opening</strong> &mdash; State your argument directly. This tells the examiner your interpretation immediately and gives your essay a clear direction.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Write four to five analytical paragraphs</strong> &mdash; Each paragraph: Point (topic sentence), Evidence (embedded quotation), Explanation (language technique + effect), Context (writer&rsquo;s purpose/historical context). Show development: how does the theme/character shift across the text?</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Write a concise conclusion</strong> &mdash; Return to your thesis. Reflect on what your analysis shows about the writer&rsquo;s overall message. Avoid introducing new evidence here.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">6</span>
<div class="guide-step-body"><strong>Proofread for SPaG (Paper 1 / Paper 2 Sec A)</strong> &mdash; In the final two minutes, scan for spelling errors (especially names: Priestley, Dickens, Macbeth), misplaced apostrophes, and sentence fragments. SPaG marks are straightforward to earn.</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 8%;">Plan<br/>2 min</span>
<span style="background: #8b5cf6; width: 72%;">Write<br/>40 min</span>
<span style="background: #a78bfa; width: 20%;">Conclude &amp; SPaG<br/>8 min</span>
</div>
<p>Aim for 45&ndash;50 minutes on the 30-mark essay. Four to five developed paragraphs (each 120&ndash;150 words) plus introduction and conclusion. Quality over quantity &mdash; a focused 700-word essay with strong analysis beats a 1,200-word plot summary.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Introduction &amp; Paragraph</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>How does Shakespeare present ambition in <em>Macbeth</em>? Write about: how ambition is presented in this extract and how it is presented in the play as a whole. [30 + 4 SPaG marks]</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Thesis: one sentence, clear argument</span>
<p>Shakespeare presents ambition as an inherently destructive force that, once unleashed, corrupts not only the individual but all those around them, transforming Macbeth from a celebrated warrior into a tyrant driven by fear and paranoia.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Paragraph: P-E-E-C in action</span>
<p>In the extract, Macbeth&rsquo;s ambition is conveyed through the soliloquy&rsquo;s imagery of violence: the &ldquo;dagger of the mind&rdquo; is a metaphor that externalises his murderous intent, making his ambition a tangible, almost physical presence. The phrase &ldquo;proceeding from the heat-oppressed brain&rdquo; suggests a feverish loss of rational control, implying that ambition in Shakespeare&rsquo;s world is a kind of madness. Contextually, Jacobean audiences would have recognised the link between unchecked ambition and disorder &mdash; James I, for whom the play may have been performed, had survived the Gunpowder Plot, a real act of violent political ambition only months earlier.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> Strong Level 3/Level 4 opening. Clear thesis, confident AO2 analysis, relevant AO3 contextual link.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Starting with a vague introduction</strong> &mdash; &ldquo;Shakespeare wrote Macbeth in the Jacobean era&rdquo; wastes your opening. State your argument in sentence one.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Forgetting SPaG under time pressure</strong> &mdash; Reserve two minutes at the end specifically for proofreading. These 4 marks are easier to earn than analytical marks and students often lose them through rushing.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Only writing about the extract (Paper 1)</strong> &mdash; Paper 1 questions explicitly ask you to write about the extract AND the rest of the text. Evidence from elsewhere in the play/novel is required for Level 3 and above.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Context as background information only</strong> &mdash; Don&rsquo;t just mention when the text was written. Connect the context directly to the language choices: why would the writer make THIS choice for THAT audience at THAT time?</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 8%;" title="Plan: 2 min"></span>
<span style="background: #8b5cf6; width: 72%;" title="Write: 40 min"></span>
<span style="background: #a78bfa; width: 20%;" title="Conclude + SPaG: 8 min"></span>
</div>
<span class="guide-quick-ref-total">50 min total</span>
<h4>Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Thesis opening (1 sentence)</li>
<li>4&ndash;5 P-E-E-C paragraphs</li>
<li>Conclusion</li>
<li>SPaG proofread (2 min)</li>
</ol>
<h4>Key AOs</h4>
<ul>
<li>AO1: Argument + evidence</li>
<li>AO2: Language/structure/form</li>
<li>AO3: Context</li>
<li>SPaG: 4 marks (P1 + P2 Sec A)</li>
</ul>
</div>
</aside>"""

# ============================================================
# 5. ANTHOLOGY COMPARISON — 30 marks
# ============================================================
anthology_comparison_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">30 marks</span>
<h1>Anthology Comparison (Poetry)</h1>
<p class="guide-used-in">Used in: Paper 2 Section B &mdash; Poetry Anthology</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>The anthology comparison question gives you one named poem from the AQA anthology and asks you to compare it with another poem of your choice from the same cluster. You must analyse how both poets present a theme (such as conflict, love, or power), using language analysis (AO2) and contextual understanding (AO3) to build a sustained comparison (AO1).</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>You choose which poem to compare it with. Spend 30 seconds deciding which poem gives you the most to say about the given theme &mdash; don&rsquo;t just pick your favourite. The best comparisons show both similarity and difference.</p>
</div>
<h3>Mark Scheme Levels (30 marks)</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>Level</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>25&ndash;30</strong></td><td>Level 4</td><td>Perceptive comparison of both poems. Convincing analysis of how each poet uses language/form/structure. Well-integrated contextual links. Argument is maintained throughout.</td></tr>
<tr><td><strong>19&ndash;24</strong></td><td>Level 3</td><td>Clear comparison with evidence from both poems. Explained analysis of language. Some contextual understanding.</td></tr>
<tr><td><strong>13&ndash;18</strong></td><td>Level 2</td><td>Points made about both poems but comparison may be implicit or uneven. Some language analysis.</td></tr>
<tr><td><strong>7&ndash;12</strong></td><td>Level 1</td><td>Simple points about one or both poems. Limited evidence. Mostly descriptive.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Choose your second poem</strong> &mdash; Pick the poem from the same cluster that gives you the richest comparison for the stated theme. Consider both similarities AND differences for a nuanced response.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Plan: two columns</strong> &mdash; Draw a quick two-column plan: left column for the named poem, right for your chosen poem. Note two or three language techniques from each, plus one structural or form observation each.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Write a comparative opening</strong> &mdash; Name both poems, state the theme, and give your overarching comparison argument in one or two sentences. Avoid treating the poems separately &mdash; connect them from the start.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Write comparative paragraphs</strong> &mdash; Each paragraph should discuss BOTH poems together around a shared idea, not one poem then the other in separate blocks. Use connectives: &ldquo;Similarly&hellip;&rdquo;, &ldquo;In contrast&hellip;&rdquo;, &ldquo;Whereas [Poem A]&hellip; [Poem B]&hellip;&rdquo;, &ldquo;Both poets&hellip;&rdquo;</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Analyse language and form in both poems</strong> &mdash; Comment on specific words, imagery, and techniques in each poem. Also consider form and structure: rhyme scheme, free verse, voice, stanza length. These are often where the comparison is most interesting.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">6</span>
<div class="guide-step-body"><strong>Link to context for each poet</strong> &mdash; Brief contextual links (poet&rsquo;s background, time of writing, social/historical circumstances) can elevate Level 3 to Level 4. Keep each context link brief but pointed.</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 10%;">Choose + plan<br/>3 min</span>
<span style="background: #8b5cf6; width: 75%;">Write<br/>38 min</span>
<span style="background: #a78bfa; width: 15%;">Conclude &amp; check<br/>4 min</span>
</div>
<p>Allow approximately 45 minutes. Four to five paragraphs comparing both poems is the target. The most common mistake is running out of time on the named poem and barely discussing the second &mdash; weave them together from the start to prevent this.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Comparison Sentence Starters</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Introducing similarity</div>
<p class="guide-starter">&ldquo;Both [Poem A] and [Poem B] present [theme] through [shared technique/idea]&hellip;&rdquo;</p>
<p class="guide-starter">&ldquo;Like [Poet A], [Poet B] uses [technique] to suggest&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Introducing contrast</div>
<p class="guide-starter">&ldquo;In contrast, whereas [Poem A] [approach], [Poem B] [different approach]&hellip;&rdquo;</p>
<p class="guide-starter">&ldquo;While [Poet A] presents [theme] as [X], [Poet B] portrays it as [Y]&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Comparing methods</div>
<p class="guide-starter">&ldquo;[Poet A] achieves [effect] through [technique], while [Poet B] relies instead on [technique]&hellip;&rdquo;</p>
</div>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Paragraph</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>Compare how poets present the effects of conflict. You must compare the poem printed below with one other poem from the anthology you have studied.<br/>[Named poem: &ldquo;Remains&rdquo; by Simon Armitage]</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Comparative opening: both poems + argument</span>
<p>Both &ldquo;Remains&rdquo; by Simon Armitage and &ldquo;War Photographer&rdquo; by Carol Ann Duffy explore the lasting psychological damage inflicted on those who witness conflict, suggesting that the effects of war extend far beyond the battlefield and into the domestic lives of those who return.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Comparative paragraph: weaving both poems together</span>
<p>Armitage uses visceral, colloquial language to convey the soldier&rsquo;s inability to escape his memories: the looter&rsquo;s image is described as &ldquo;dug in behind enemy lines&rdquo;, a military metaphor that suggests the trauma is now itself an occupying force in the speaker&rsquo;s mind. Similarly, Duffy&rsquo;s photographer finds that the suffering he has witnessed &ldquo;half-formed ghost[s]&rdquo; in his developing trays &mdash; the spectral imagery implying that the dead are never fully absent. Where Armitage emphasises the visceral, unprocessed nature of the trauma through present-tense narration, Duffy&rsquo;s third-person perspective creates a sense of detachment that reflects how the photographer must emotionally distance himself to survive.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> Level 4 &mdash; Integrated comparison, confident language analysis across both poems, distinct observations about form and perspective.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Writing about each poem separately</strong> &mdash; A &ldquo;Poem A then Poem B&rdquo; structure earns Level 2 at best. Examiners want to see continuous comparison. Weave both poems into every paragraph.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Choosing a poem you can&rsquo;t quote accurately</strong> &mdash; In the exam you must rely on memory for your chosen poem. Pick one you know well and have practised quoting from.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Focusing only on content, not methods</strong> &mdash; &ldquo;Both poems are about war&rdquo; is not enough. You must compare HOW language, structure, and form are used to present the theme.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Uneven coverage of the two poems</strong> &mdash; Both poems should receive broadly equal analytical attention. If you notice you&rsquo;ve written three paragraphs on the named poem and only one on your choice, adjust mid-essay.</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 10%;" title="Plan: 3 min"></span>
<span style="background: #8b5cf6; width: 75%;" title="Write: 38 min"></span>
<span style="background: #a78bfa; width: 15%;" title="Check: 4 min"></span>
</div>
<span class="guide-quick-ref-total">45 min total</span>
<h4>Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Choose your poem (30 sec)</li>
<li>Two-column plan</li>
<li>Comparative opening</li>
<li>4&ndash;5 paragraphs (both poems per para)</li>
<li>Conclusion</li>
</ol>
<h4>Connectives</h4>
<ul>
<li>Both poets&hellip;</li>
<li>Similarly&hellip; / Likewise&hellip;</li>
<li>In contrast&hellip; / Whereas&hellip;</li>
<li>While [A] presents&hellip; [B]&hellip;</li>
</ul>
</div>
</aside>"""

# ============================================================
# 6. UNSEEN POETRY ANALYSIS — 24 marks
# ============================================================
unseen_poetry_analysis_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">24 marks</span>
<h1>Unseen Poetry Analysis</h1>
<p class="guide-used-in">Used in: Paper 2 Section C &mdash; Question 1 (Unseen Poetry)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>The unseen poetry analysis question asks you to respond to a poem you have never studied before. You are given the poem in the exam paper. The examiner wants to see that you can apply your analytical skills to an unfamiliar text &mdash; identifying how language, structure, and form create meaning and effect. There is no &ldquo;right answer&rdquo;: your personal interpretation, backed by evidence, is exactly what is being tested.</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>You cannot revise the content of the unseen poem &mdash; but you CAN revise the skills. Practise applying language and structure analysis to poems you haven&rsquo;t studied. The more you practise the process, the more confident you&rsquo;ll be in the exam.</p>
</div>
<h3>Mark Scheme Levels (24 marks)</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>Level</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>21&ndash;24</strong></td><td>Level 4</td><td>Perceptive, sensitive analysis of how language, structure, and form work together. Convincing personal interpretation supported by well-chosen evidence. Confident use of subject terminology.</td></tr>
<tr><td><strong>15&ndash;20</strong></td><td>Level 3</td><td>Clear explanation of how the poet uses language and structure. Relevant evidence and terminology. Some awareness of form.</td></tr>
<tr><td><strong>9&ndash;14</strong></td><td>Level 2</td><td>Some analytical points with evidence. Terminology used but may not always enhance the analysis.</td></tr>
<tr><td><strong>1&ndash;8</strong></td><td>Level 1</td><td>Simple observations. Limited evidence. Mainly descriptive or focused on subject matter rather than method.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Read the poem twice</strong> &mdash; First read: get the overall meaning and mood. Second read: annotate for language (striking words, techniques, imagery) and structure (stanza length, rhyme, line breaks, shifts in tone or voice).</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Identify the tone and theme</strong> &mdash; What is the poem&rsquo;s emotional register? (Melancholic? Angry? Celebratory?) What is the central idea or message? This gives your analysis a direction before you start writing.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Choose three to four moments to analyse</strong> &mdash; Select specific moments where the language is particularly interesting, surprising, or purposeful. Avoid trying to comment on every single line &mdash; depth beats breadth.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Analyse language and structure together</strong> &mdash; For each moment, name the technique, embed the quotation, explain the effect, and say WHY the poet might have made that choice. Also comment on at least one structural feature (e.g. enjambment, caesura, stanza breaks, the volta if it&rsquo;s a sonnet).</div>
</li>
<li class="guide-step">
<span class="guide-step-number">5</span>
<div class="guide-step-body"><strong>Comment on form</strong> &mdash; Is it a sonnet, ballad, free verse, dramatic monologue? Does the form reinforce or contrast the content? Even one clear observation about form can earn marks.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">6</span>
<div class="guide-step-body"><strong>Write a conclusion with a personal response</strong> &mdash; AQA rewards genuine personal engagement. End with a sentence stating your overall interpretation of what the poem is doing and why you find the poet&rsquo;s approach effective.</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 15%;">Read &amp; annotate<br/>5 min</span>
<span style="background: #8b5cf6; width: 65%;">Write<br/>22 min</span>
<span style="background: #a78bfa; width: 20%;">Conclude &amp; check<br/>3 min</span>
</div>
<p>Allow approximately 30 minutes for 24 marks. Spend five minutes reading and annotating before you write a single word of your response. This is time well spent &mdash; students who rush to write without annotating produce thinner analysis.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotation Checklist</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<p>When you annotate an unseen poem, look for:</p>
<ul>
<li><strong>Imagery:</strong> metaphor, simile, personification, symbolism</li>
<li><strong>Sound devices:</strong> alliteration, sibilance, assonance, onomatopoeia</li>
<li><strong>Tone and mood:</strong> word choices that carry emotional weight (connotations)</li>
<li><strong>Repetition:</strong> anaphora, refrain, recurring imagery</li>
<li><strong>Structure:</strong> enjambment, caesura, line length variations, stanza breaks</li>
<li><strong>Form:</strong> sonnet, free verse, ballad, dramatic monologue, ode</li>
<li><strong>Voice:</strong> first person (personal)? second person (direct address)? Third person (detached)?</li>
<li><strong>Shifts:</strong> Does the tone, focus, or speaker change at any point? (Often at a volta or final stanza)</li>
</ul>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Paragraph</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-paragraph">
<span class="guide-annotation">Language: technique + effect</span>
<p>The poet uses an extended metaphor of drowning throughout the poem, culminating in the image of &ldquo;waves of silence pressing down&rdquo;. The verb &ldquo;pressing&rdquo; suggests an active, suffocating force, transforming emotional isolation into something physical and inescapable &mdash; as if grief is not merely felt but endured as a bodily experience.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Structure: enjambment</span>
<p>The enjambment that runs across stanzas three and four reinforces this sense of relentlessness: the lines spill forward without pause, mimicking the inability of the speaker to stop the tide of emotion even when they wish to.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Personal response</span>
<p>I find this technique particularly effective because it allows the poem to enact, not just describe, the experience of grief &mdash; placing the reader inside the sensation rather than observing it from outside.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> Level 4 &mdash; Perceptive language and structure analysis, personal response integrated, confident use of terminology.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Retelling what the poem is about</strong> &mdash; The examiner has read the poem. You must analyse HOW it achieves its effect, not WHAT it describes.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Only commenting on language, not structure or form</strong> &mdash; Structure and form observations are part of AO2 and often the most insightful points you can make. Always include at least one structural comment.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Panicking because you don&rsquo;t know the poem</strong> &mdash; Not knowing the poem is the point. Every student is in the same position. Apply your skills systematically using the annotation checklist.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Commenting on every single line</strong> &mdash; Select three to four key moments and analyse them in depth. Examiners reward analytical quality, not coverage of every technique in the poem.</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 15%;" title="Read + annotate: 5 min"></span>
<span style="background: #8b5cf6; width: 65%;" title="Write: 22 min"></span>
<span style="background: #a78bfa; width: 20%;" title="Conclude: 3 min"></span>
</div>
<span class="guide-quick-ref-total">30 min total</span>
<h4>What to Annotate</h4>
<ul>
<li>Striking word choices</li>
<li>Language techniques</li>
<li>Structural choices</li>
<li>Tone shifts / volta</li>
<li>Form</li>
</ul>
<h4>Key AOs</h4>
<ul>
<li>AO1: Personal response + evidence</li>
<li>AO2: Language &amp; structure analysis</li>
</ul>
</div>
</aside>"""

# ============================================================
# 7. UNSEEN POETRY COMPARISON — 8 marks
# ============================================================
unseen_poetry_comparison_html = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">8 marks</span>
<h1>Unseen Poetry Comparison</h1>
<p class="guide-used-in">Used in: Paper 2 Section C &mdash; Question 2 (Unseen Poetry)</p>
</div>

<div class="guide-section">
<h2>What the Examiner Wants</h2>
<p>Question 2 of the unseen poetry section gives you a second short poem and asks you to compare it with the first poem (from Question 1) on a specific focus. You need to write a focused comparison of how both poets use language and form to present a particular idea or feeling. This tests AO1 (comparison with evidence) and AO2 (analysis of language and form).</p>
<div class="key-fact">
<div class="key-fact-label">Key Fact</div>
<p>This question is only 8 marks &mdash; keep it brief and focused. You do not need to analyse the second poem in as much depth as in Question 1. Aim for two or three comparison points, not a full essay.</p>
</div>
<h3>Mark Scheme Levels</h3>
<table class="guide-levels">
<thead>
<tr><th>Marks</th><th>Level</th><th>What You Need</th></tr>
</thead>
<tbody>
<tr><td><strong>7&ndash;8</strong></td><td>Level 4</td><td>Perceptive comparison of how both poets use language/form/structure. Convincing analysis with well-chosen evidence from both poems.</td></tr>
<tr><td><strong>5&ndash;6</strong></td><td>Level 3</td><td>Clear comparison. Evidence from both poems. Relevant language analysis.</td></tr>
<tr><td><strong>3&ndash;4</strong></td><td>Level 2</td><td>Some comparison. Points made about both poems but not always clearly linked. Some evidence used.</td></tr>
<tr><td><strong>1&ndash;2</strong></td><td>Level 1</td><td>Simple comments on one or both poems. Mostly descriptive. Little comparison.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step">
<span class="guide-step-number">1</span>
<div class="guide-step-body"><strong>Read the second poem and the question focus</strong> &mdash; The question will specify a focus (e.g. &ldquo;how the poets present sadness&rdquo;). Note two or three moments from each poem that relate to that focus.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">2</span>
<div class="guide-step-body"><strong>Identify a similarity and a difference</strong> &mdash; The best 8-mark responses show both. What do the poets agree on or share? Where do they diverge in approach, tone, or method?</div>
</li>
<li class="guide-step">
<span class="guide-step-number">3</span>
<div class="guide-step-body"><strong>Write two or three integrated comparison paragraphs</strong> &mdash; Each paragraph discusses BOTH poems together. Use comparative connectives: &ldquo;Similarly&hellip;&rdquo;, &ldquo;In contrast&hellip;&rdquo;, &ldquo;Whereas Poem 1&hellip; Poem 2&hellip;&rdquo;. Keep paragraphs tight and focused.</div>
</li>
<li class="guide-step">
<span class="guide-step-number">4</span>
<div class="guide-step-body"><strong>Analyse language briefly in each poem</strong> &mdash; Embed a short quotation from each and explain the technique/effect. You don&rsquo;t need the depth of Question 1 &mdash; one technique per poem per paragraph is enough.</div>
</li>
</ol>
</div>

<div class="guide-section">
<h2>Timing</h2>
<div class="guide-timing-bar">
<span style="background: #7c3aed; width: 20%;">Read &amp; note<br/>2 min</span>
<span style="background: #8b5cf6; width: 65%;">Write<br/>10 min</span>
<span style="background: #a78bfa; width: 15%;">Check<br/>2 min</span>
</div>
<p>Allow around 10&ndash;15 minutes. Two or three focused comparison paragraphs is all you need for 8 marks. Do not write a full essay &mdash; this is a compact, focused comparison task.</p>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Comparison Sentence Starters</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Similarity</div>
<p class="guide-starter">&ldquo;Both poems present [theme/feeling] through [shared technique], suggesting&hellip;&rdquo;</p>
<p class="guide-starter">&ldquo;Like the first poem, the second poet uses [technique] to convey&hellip;&rdquo;</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Difference</div>
<p class="guide-starter">&ldquo;In contrast to [Poem 1&rsquo;s approach], [Poem 2] uses [different technique], creating&hellip;&rdquo;</p>
<p class="guide-starter">&ldquo;Whereas [Poem 1] presents [feeling] as [X], [Poem 2] portrays it as [Y]&hellip;&rdquo;</p>
</div>
</div>
</div>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle">
<span>Annotated Model Answer</span>
<svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div class="collapsible-content">
<div class="collapsible-inner">
<div class="guide-model-question">
<p>In this poem, how does the poet present loneliness? Compare this with how loneliness is presented in the poem from Question 1. [8 marks]</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Similarity: both poems + evidence</span>
<p>Both poems present loneliness as a physical sensation rather than an emotional state. In Poem 1, the &ldquo;weight of empty rooms&rdquo; uses tactile imagery to make isolation feel bodily and oppressive. Similarly, the second poet describes &ldquo;cold settling in the bones&rdquo;, a metaphor that transforms emotional isolation into physical discomfort &mdash; both poets suggesting that loneliness cannot be separated from the body.</p>
</div>
<div class="guide-model-paragraph">
<span class="guide-annotation">Difference: form and structure</span>
<p>However, the two poems differ significantly in form. Poem 1&rsquo;s fragmented free verse &mdash; with frequent caesura and short, broken lines &mdash; mimics the fractured inner life of the speaker, whereas the second poem&rsquo;s regular quatrains and consistent rhyme scheme create an impression of resigned acceptance, as though loneliness has become so familiar it now feels ordered and inevitable.</p>
</div>
<div class="guide-model-mark">
<p><strong>Examiner:</strong> 7&ndash;8 &mdash; Integrated comparison, evidence from both poems, analysis of both language and form, similarity and difference both discussed.</p>
</div>
</div>
</div>
</div>

<div class="guide-section">
<h2>Common Mistakes</h2>
<ul class="guide-mistakes">
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Writing about each poem separately</strong> &mdash; &ldquo;First poem: [paragraph]. Second poem: [paragraph]&rdquo; is not a comparison. Interweave them in each paragraph.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Writing too much</strong> &mdash; This is 8 marks, not 24. Two or three focused paragraphs is the target. Spending 20+ minutes on this wastes time you need elsewhere in the exam.</div>
</li>
<li class="guide-mistake">
<span class="guide-mistake-icon">&#10007;</span>
<div><strong>Only noting similarities</strong> &mdash; The most insightful comparisons show both similarity and difference. Even a subtle contrast in tone, form, or emotional effect is worth pointing out.</div>
</li>
</ul>
</div>

<a class="back-link" href="index.html">&#8592; Back to Exam Technique</a>
</main>
<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c3aed; width: 20%;" title="Read: 2 min"></span>
<span style="background: #8b5cf6; width: 65%;" title="Write: 10 min"></span>
<span style="background: #a78bfa; width: 15%;" title="Check: 2 min"></span>
</div>
<span class="guide-quick-ref-total">15 min total</span>
<h4>Structure</h4>
<ol class="guide-quick-ref-steps">
<li>Read both poems + note focus</li>
<li>1 similarity + 1 difference</li>
<li>2&ndash;3 integrated paragraphs</li>
</ol>
<h4>Connectives</h4>
<ul>
<li>Both poems&hellip; / Similarly&hellip;</li>
<li>In contrast&hellip; / Whereas&hellip;</li>
<li>Unlike [Poem 1]&hellip;</li>
</ul>
</div>
</aside>"""

# ============================================================
# INSERT ALL PAGES
# ============================================================
pages = [
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'index',
        'title': 'Exam Technique',
        'content_html': hub_html,
        'sort_order': 0,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'quote-analysis',
        'title': 'Quote Analysis — 4 marks',
        'content_html': quote_analysis_html,
        'sort_order': 1,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'extract-analysis',
        'title': 'Extract Analysis — 8 marks',
        'content_html': extract_analysis_html,
        'sort_order': 2,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'extended-response',
        'title': 'Extended Response — 12 marks',
        'content_html': extended_response_html,
        'sort_order': 3,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'essay-response',
        'title': 'Essay Response — 30 + 4 SPaG marks',
        'content_html': essay_response_html,
        'sort_order': 4,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'anthology-comparison',
        'title': 'Anthology Comparison — 30 marks',
        'content_html': anthology_comparison_html,
        'sort_order': 5,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'unseen-poetry-analysis',
        'title': 'Unseen Poetry Analysis — 24 marks',
        'content_html': unseen_poetry_analysis_html,
        'sort_order': 6,
    },
    {
        'subject_id': SUBJECT_ID,
        'guide_type': 'exam-technique',
        'slug': 'unseen-poetry-comparison',
        'title': 'Unseen Poetry Comparison — 8 marks',
        'content_html': unseen_poetry_comparison_html,
        'sort_order': 7,
    },
]

print(f"Inserting {len(pages)} guide pages for English Literature (AQA 8702)...")
for page in pages:
    result = sb.table('guide_pages').upsert(
        page,
        on_conflict='subject_id,guide_type,slug'
    ).execute()
    if result.data:
        print(f"  OK: {page['guide_type']}/{page['slug']} — {page['title']}")
    else:
        print(f"  ERROR on {page['slug']}: {result}")

print("\nDone. Verifying inserted rows...")
verify = sb.table('guide_pages').select('slug,title,sort_order').eq('subject_id', SUBJECT_ID).eq('guide_type', 'exam-technique').order('sort_order').execute()
for row in verify.data:
    print(f"  [{row['sort_order']}] {row['slug']} — {row['title']}")
