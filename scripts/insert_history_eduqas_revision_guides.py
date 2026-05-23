"""
Insert History (Eduqas) revision technique guide pages into Supabase.
Subject slug: history-eduqas
Subject ID: looked up dynamically by slug at runtime.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://baipckgywpnwapobwtsy.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

SLUG = 'history-eduqas'

# ─────────────────────────────────────────────────────────────
# Resolve subject_id by slug
# ─────────────────────────────────────────────────────────────
result = sb.table('subjects').select('id,name').eq('slug', SLUG).single().execute()
if not result.data:
    print(f"ERROR: subject with slug '{SLUG}' not found in Supabase.")
    sys.exit(1)
SUBJECT_ID = result.data['id']
print(f"Resolved subject_id: {SUBJECT_ID}  ({result.data['name']})")

# ─────────────────────────────────────────────────────────────
# SIDEBAR LINK BLOCKS (one per page, excluding self)
# ─────────────────────────────────────────────────────────────

BASE = f'/guide/{SLUG}/revision-technique'

ALL_LINKS = {
    'retrieval-practice':        f'<a class="sidebar-media-item" href="{BASE}/retrieval-practice"><strong>Retrieval Practice</strong><span>Active recall</span></a>',
    'spaced-repetition':         f'<a class="sidebar-media-item" href="{BASE}/spaced-repetition"><strong>Spaced Repetition</strong><span>Distributed practice</span></a>',
    'interleaving':              f'<a class="sidebar-media-item" href="{BASE}/interleaving"><strong>Interleaving</strong><span>Mixed practice</span></a>',
    'dual-coding':               f'<a class="sidebar-media-item" href="{BASE}/dual-coding"><strong>Dual Coding</strong><span>Visual learning</span></a>',
    'elaborative-interrogation': f'<a class="sidebar-media-item" href="{BASE}/elaborative-interrogation"><strong>Elaborative Interrogation</strong><span>Deep thinking</span></a>',
    'knowledge-organisers':      f'<a class="sidebar-media-item" href="{BASE}/knowledge-organisers"><strong>Knowledge Organisers</strong><span>Structured notes</span></a>',
    'timed-practice':            f'<a class="sidebar-media-item" href="{BASE}/timed-practice"><strong>Timed Practice</strong><span>Exam conditions</span></a>',
}

def other_links(exclude):
    return '\n'.join(v for k, v in ALL_LINKS.items() if k != exclude)

OTHER_LINKS_EXCEPT_RETRIEVAL        = other_links('retrieval-practice')
OTHER_LINKS_EXCEPT_SPACED           = other_links('spaced-repetition')
OTHER_LINKS_EXCEPT_INTERLEAVING     = other_links('interleaving')
OTHER_LINKS_EXCEPT_DUAL             = other_links('dual-coding')
OTHER_LINKS_EXCEPT_ELABORATIVE      = other_links('elaborative-interrogation')
OTHER_LINKS_EXCEPT_KO               = other_links('knowledge-organisers')
OTHER_LINKS_EXCEPT_TIMED            = other_links('timed-practice')

# ─────────────────────────────────────────────────────────────
# GUIDE PAGES — 1 hub + 7 individual technique pages
# ─────────────────────────────────────────────────────────────

pages = []

# ══════════════════════════════════════════════════════════════
# sort_order = 0 — HUB INDEX
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "index",
    "title": "Revision Techniques",
    "sort_order": 0,
    "content_html": f"""<div class="unit-page-header">
<div class="unit-page-header-inner">
<h1>Revision Techniques</h1>
<p>Evidence-based strategies tailored to GCSE History. The exam rewards students who can recall precise dates, named individuals and key terms; analyse sources and competing interpretations using contextual knowledge; and build structured arguments across the second-order concepts of cause, consequence, change, continuity, significance, similarity and difference. These techniques are chosen to match exactly those demands.</p>
</div>
</div>
<div class="guide-hub">

<div class="guide-paper" style="--paper-accent: #7c2d12; --paper-light: #fef7ed;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these from day one</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="{BASE}/retrieval-practice">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself on exact dates, named figures and key treaties rather than re-reading. Brain dumps reveal whether you can recall the Treaty of Br&eacute;tigny (1360), the Statute of Labourers (1351), or the Enabling Act (1933) under pressure &mdash; and lock in what you can name.</p>
</a>
<a class="guide-question-card" href="{BASE}/spaced-repetition">
<span class="guide-question-marks">Distributed practice</span>
<h3>Spaced Repetition</h3>
<p>Revisit chronologies, turning-point judgements and second-order concept frameworks at 1, 3, 7, 14 and 30-day gaps. Works far better than cramming and prevents the &lsquo;I knew this last week&rsquo; failure on exam day.</p>
</a>
<a class="guide-question-card" href="{BASE}/dual-coding">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>Combine words and visuals. A cause-and-consequence map for the Black Death, a change/continuity diagram across crime &amp; punishment&rsquo;s three eras, or a quick sketch of the Royal Dockyards at Chatham sticks far better than text alone.</p>
</a>
</div>
</div>

<div class="guide-paper" style="--paper-accent: #7c2d12; --paper-light: #fef7ed;">
<div class="guide-paper-header">
<h2>Stretch Techniques</h2>
<span class="guide-paper-ref">Use these once you know the basics</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="{BASE}/interleaving">
<span class="guide-question-marks">Mixed practice</span>
<h3>Interleaving</h3>
<p>Mix depth-study, period-study and thematic questions in one session. Trains you to identify which second-order concept a question targets &mdash; the skill that separates a top-band response from a mid-band one.</p>
</a>
<a class="guide-question-card" href="{BASE}/elaborative-interrogation">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; about every date and interpretation. Why did the Black Death cause the Peasants&rsquo; Revolt? Why do two historians interpret the same source differently? Turn memorised facts into explained significance.</p>
</a>
<a class="guide-question-card" href="{BASE}/knowledge-organisers">
<span class="guide-question-marks">Structured notes</span>
<h3>Knowledge Organisers</h3>
<p>One page per option: key dates, named figures, second-order judgements, and a thematic-study change tracker across all three eras. Redraw from memory. The base layer of solid exam preparation.</p>
</a>
<a class="guide-question-card" href="{BASE}/timed-practice">
<span class="guide-question-marks">Exam conditions</span>
<h3>Timed Practice</h3>
<p>Simulate the real thing. Questions rise from a 2-mark &lsquo;describe a feature&rsquo; recall all the way to a 16-mark essay &mdash; practising under time pressure builds the judgement about when to recall quickly and when to evaluate carefully.</p>
</a>
</div>
</div>

</div>"""
})

# ══════════════════════════════════════════════════════════════
# sort_order = 1 — RETRIEVAL PRACTICE
# ══════════════════════════════════════════════════════════════
pages.append({
    "subject_id": SUBJECT_ID,
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
<tr><td><strong>Agarwal et al. (2017)</strong></td><td>Low-stakes retrieval quizzes raised test scores by an average of one grade.</td><td>Short regular quizzing moves your real exam score.</td></tr>
<tr><td><strong>Smith et al. (2016)</strong></td><td>Students who practised retrieval scored higher even on questions testing information they didn&rsquo;t specifically retrieve.</td><td>Builds the skill of remembering itself, not just the facts.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Study a chunk of content</strong> &mdash; read through a lesson, watch a video, or cover a topic in class. Don&rsquo;t try to memorise. Just understand.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Close everything</strong> &mdash; book shut, tab closed, notes flipped over. The whole point is that you cannot see the material.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Write down everything you can remember</strong> &mdash; no looking back. This is called a &ldquo;brain dump.&rdquo; Write until you run out. It should feel uncomfortable.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Check against the source</strong> &mdash; open the lesson. Mark what you missed in a different colour. Don&rsquo;t just glance &mdash; properly compare.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Target the gaps</strong> &mdash; re-study only the parts you missed. Not the whole lesson again. Just the holes.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Retest tomorrow</strong> &mdash; hit the same topic again within 24 hours. The second attempt is where the learning locks in.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Exact dates, treaties and Acts of Parliament</div>
<p>After studying the Hundred Years War or the Elizabethan period, close the lesson and write every named event from memory with its precise date: the Statute of Labourers (1351), the Treaty of Br&eacute;tigny (1360), the Peasants&rsquo; Revolt (1381), the Armada (1588), the Poor Law (1601). Next to each, add the named individual most closely associated with it. Examiners award marks only for accurate factual recall, so a date one year out or a misspelled name can cost you. Precision matters far more than volume &mdash; ten facts you know cold beat thirty you half-know. Check back and highlight anything you misplaced by more than five years or misidentified the person behind.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Key terms and specialist vocabulary</div>
<p>Brain-dump specialist vocabulary completely from memory for one option. For Germany 1919&ndash;1939: <em>Anschluss</em>, <em>Enabling Act</em>, <em>Kristallnacht</em>, <em>Lebensraum</em>, the <em>Reichstag fire</em> and <em>Night of the Long Knives</em> with their dates and a one-sentence definition for each. For the thematic studies, terms like <em>chevauch&eacute;e</em> (Hundred Years War tactics), <em>recusancy</em> (Elizabethan religious non-conformity) and <em>perestroika</em> (Soviet reform under Gorbachev) carry marks in both recall questions and the SPaG band of extended responses. Spell them correctly in your dump. Wait three days and retest cold.</p>
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
<p>Build it in <strong>every week</strong>, from the start of your course through to your exams. Aim for 15&ndash;20 minutes per session, two or three times a week. The last two weeks before an exam is when retrieval practice becomes your main tool &mdash; swap passive reading for brain dumps and flashcards. On StudyVault, the Knowledge Check and Flashcard buttons in every lesson sidebar are retrieval practice in disguise &mdash; use them.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 25%;" title="Study: 5 min"></span>
<span style="background: #9a3412; width: 40%;" title="Brain dump: 8 min"></span>
<span style="background: #c2410c; width: 35%;" title="Check &amp; gaps: 7 min"></span>
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
    "subject_id": SUBJECT_ID,
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
<tr><td><strong>Kang (2016)</strong></td><td>Optimal gap &asymp; 10&ndash;20% of the time until the test. For a May exam, that means revisiting material every 3&ndash;6 weeks from the start of your course.</td><td>You can plan exactly when to revisit a topic.</td></tr>
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
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Chronologies and turning-point judgements</div>
<p>You study the Elizabethan Age on Monday: the Religious Settlement (1559), the Northern Earls&rsquo; revolt (1569), Mary Queen of Scots&rsquo; execution (1587), the Armada (1588), the Poor Law (1601). On Tuesday, do a quick brain dump of all five events in order with their dates. On Thursday, redo the dump and this time add a second-order judgement for each &mdash; which was most significant for Elizabethan stability? Why? The following Monday, attempt a timed 8-mark &lsquo;explain the significance of&rsquo; question cold. Each review takes under 10 minutes and the spacing means the chronology feels automatic by exam day while the significance judgement deepens with each pass.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Second-order concept frameworks across a depth study</div>
<p>After first covering Germany 1919&ndash;1939, log it on a revision tracker. Day 1 review: write from memory five causes of Hitler&rsquo;s rise to power (economic crisis, Weimar instability, Nazi propaganda, SA intimidation, elite miscalculation) with a date and named evidence for each. Day 7 review: attempt the same recall without notes, then rank the causes and write a two-sentence justification for your most important choice. Day 21 review: answer a timed &lsquo;explain why the Weimar Republic collapsed&rsquo; question. Revisiting the same events through a different second-order lens each time &mdash; cause, then significance, then change &mdash; builds the analytical flexibility the higher-mark questions demand.</p>
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
<p>This is the organising principle of your whole revision year &mdash; not a technique you pull out near the exam. From the first lesson of your course, log every topic you cover and schedule reviews at 1 day, 3 days, 7 days, 14 days, and 30 days. The StudyVault flashcard system does this automatically via the Leitner method &mdash; questions move between five boxes with intervals of 1, 2, 4, 7, and 14 days. When a card comes up, do it.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 20%;" title="Day 1"></span>
<span style="background: #9a3412; width: 20%;" title="Day 3"></span>
<span style="background: #c2410c; width: 20%;" title="Day 7"></span>
<span style="background: #ea580c; width: 20%;" title="Day 14"></span>
<span style="background: #fb923c; width: 20%;" title="Day 30"></span>
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
    "subject_id": SUBJECT_ID,
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
<p>Most students revise by blocking &mdash; an hour on the Elizabethan Age, an hour on Germany, an hour on Crime &amp; Punishment. It feels productive and the topic seems clear by the end. Interleaving is the opposite: you jump between topics inside a single session. It feels worse at the time, and you&rsquo;ll make more mistakes. But when the real exam arrives, you will be dramatically better at knowing <em>which</em> second-order concept a question is targeting &mdash; cause, consequence, significance, change &mdash; and that identification is often the hardest part of a History response.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Rohrer &amp; Taylor (2007)</strong></td><td>Students who interleaved topics scored 43% higher on delayed tests than blocked-practice students.</td><td>Same time spent &mdash; huge difference in exam performance.</td></tr>
<tr><td><strong>Birnbaum et al. (2013)</strong></td><td>Interleaved learners felt LESS confident during practice but performed BETTER in the test.</td><td>If revision feels too easy, interleave.</td></tr>
<tr><td><strong>Bjork &amp; Bjork (2011)</strong></td><td>Desirable difficulties &mdash; including interleaving &mdash; create durable long-term learning at the cost of short-term performance.</td><td>Short-term struggle is the price of long-term gain.</td></tr>
<tr><td><strong>Taylor &amp; Rohrer (2010)</strong></td><td>Benefit was largest when topics looked superficially similar &mdash; students learnt to DISTINGUISH them.</td><td>Most useful where students confuse related ideas &mdash; exactly the problem with second-order concepts.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Pick 3&ndash;5 related topics or question types</strong> &mdash; topics that share a paper, a second-order concept, or a question format. Similar enough that students confuse them.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Make a mixed problem set</strong> &mdash; 10&ndash;15 questions drawn from all the topics. Don&rsquo;t label which topic each question belongs to.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Attempt each question cold</strong> &mdash; the first step is identifying what&rsquo;s being asked. Is this a cause question, a significance question, or a change-and-continuity question? That identification is the skill you&rsquo;re training.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Mark after every question</strong> &mdash; note which concept or topic area each question targeted. Pay attention to mis-identifications &mdash; those are the highest-value gaps.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Rebuild a new mixed set tomorrow</strong> &mdash; same topics, different questions, different order. Over time, misclassifications drop.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Expect to feel worse than blocked practice</strong> &mdash; that&rsquo;s the right feeling. Your exam self will thank you.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Mixing depth-study and thematic-study question types</div>
<p>Mix questions from your British depth study, your period study and your thematic study in one 40-minute session. Write 12 questions on separate slips: four from each area, shuffled. Before each question, ask yourself: &ldquo;Is this a cause/consequence question, a significance question, a source utility question, or a change/continuity question?&rdquo; Students regularly confuse a 6-mark &lsquo;explain a cause&rsquo; question (which wants developed causation) with an 8-mark &lsquo;explain the significance of&rsquo; question (which wants a judgement about lasting impact). The interleaving drill trains that distinction directly, preventing the common error of writing a narrative response to a significance question.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Mixing content from across the three thematic eras</div>
<p>For a thematic study such as Crime &amp; Punishment or Warfare, mix questions from the medieval (c.500&ndash;1500), early modern (c.1500&ndash;1750) and modern (c.1750&ndash;present) eras in one session without labelling which era each question comes from. This trains you to recognise which era the evidence belongs to and whether it represents change or continuity &mdash; the exact discrimination the thematic essay demands. Students who revise each era in isolation often produce essays that list events chronologically instead of weighing change against continuity across all three periods. Interleaving prevents this by making era-to-era comparison the natural reflex.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Interleaving before you know the basics.</strong> You need to know each topic individually first. Use interleaving once you&rsquo;ve studied all your options &mdash; not as a first-pass strategy.</li>
<li><strong>Giving up because it feels hard.</strong> Difficulty during interleaved practice is the signal it&rsquo;s working. Persist.</li>
<li><strong>Mixing completely unrelated subjects.</strong> Interleaving works best when the topics are related enough to be confused. Mix History question types together &mdash; not History with Geography.</li>
<li><strong>Not checking mis-identifications.</strong> The mistake is the data. If you approached a &lsquo;why do interpretations differ?&rsquo; question as if it were a &lsquo;describe a feature&rsquo; question, that confusion is exactly what needs fixing before the exam.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Start interleaving once you have studied all your options at least once. In the final six weeks before the exam, replace most blocked revision with interleaved mixed sets. Particularly powerful the week before the exam when you want to simulate the unpredictable order in which questions appear &mdash; the exam will not group all the causation questions together, and neither should your revision.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 15%;" title="Choose topics"></span>
<span style="background: #9a3412; width: 55%;" title="Mixed problem set"></span>
<span style="background: #c2410c; width: 30%;" title="Mark &amp; review mis-IDs"></span>
</div>
<span class="guide-quick-ref-total">~40 minutes per interleaved session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Pick 3&ndash;5 related topics</li>
<li>Build mixed question set</li>
<li>Identify the concept first</li>
<li>Attempt the question</li>
<li>Mark every question</li>
<li>Rebuild tomorrow</li>
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
    "subject_id": SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "dual-coding",
    "title": "Dual Coding",
    "sort_order": 4,
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Visual learning</span>
<h1>Dual Coding</h1>
<p class="guide-used-in">Combine words and visuals to remember more with less effort.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Your brain processes verbal information and visual information through two separate channels. When both channels carry the same idea simultaneously &mdash; a diagram alongside an explanation &mdash; the memory trace is twice as strong as text alone. Dual coding is not about making pretty revision notes. It is about deliberately constructing visuals that mirror the verbal content, so both channels reinforce each other.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Paivio (1986)</strong></td><td>Dual-coded memories are more retrievable because they can be accessed via two independent pathways.</td><td>Forgetting one channel still leaves the other intact.</td></tr>
<tr><td><strong>Mayer &amp; Moreno (2003)</strong></td><td>Students who studied with text-plus-diagrams scored 89% higher on transfer tests than those who studied text alone.</td><td>Drawing diagrams yourself is more powerful than reading them.</td></tr>
<tr><td><strong>Ainsworth et al. (2011)</strong></td><td>Explaining content by drawing it produced the deepest understanding, even when students felt less confident drawing than writing.</td><td>The act of constructing the visual is the learning.</td></tr>
<tr><td><strong>Dunlosky et al. (2013)</strong></td><td>Dual coding rated moderate-to-high utility across subjects. Most effective when visuals are self-generated, not copied.</td><td>Draw your own &mdash; don&rsquo;t just copy a teacher&rsquo;s diagram.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Study the topic in text first</strong> &mdash; read the lesson or your notes until you understand the core idea.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Close the text</strong> &mdash; don&rsquo;t copy the diagram from the lesson. Build your own from scratch.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Choose the right visual type</strong> &mdash; timelines for chronological sequences, cause-and-consequence maps for causation, change/continuity diagrams for thematic studies, annotated site sketches for historic environment questions.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Add labels in your own words</strong> &mdash; the label is not decoration. It forces you to translate the concept into language you own.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Check against the source</strong> &mdash; compare your diagram to the lesson. Correct anything missing or wrong in a different colour.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Redraw from memory a week later</strong> &mdash; combine with spaced repetition. Redrawing is retrieval practice for visual memories.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Cause-and-consequence map for the Black Death</div>
<p>After studying the Black Death (1348&ndash;1349) and the Peasants&rsquo; Revolt (1381), close the lesson and draw a cause-and-consequence web from memory. At the centre: &ldquo;Black Death kills ~40% of England&rsquo;s population.&rdquo; Radiating outward: labour shortages (cause of peasant bargaining power), higher wages demanded, Statute of Labourers 1351 (government response), growing resentment, Poll Tax 1381, Revolt led by Wat Tyler and John Ball. Add arrows showing which events caused which. Label each arrow with the concept it illustrates (cause, consequence, significance). Check back. The visual structure prevents the most common error: listing events in order rather than tracing the causal chain. Redraw in one week without looking.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Change/continuity diagram for a thematic study</div>
<p>For Crime &amp; Punishment (or any thematic study), draw a three-column table from memory: Medieval (c.500&ndash;1500), Early Modern (c.1500&ndash;1750), Modern (c.1750&ndash;present). In each column add: one key crime type, one key punishment, one key law-enforcement method, one turning point. Then draw arrows between columns wherever something changed (change arrow) or stayed the same across eras (continuity line). For the historic environment element &mdash; Policing in Liverpool for Crime &amp; Punishment &mdash; sketch a rough site map annotated with what it tells us about the thematic story. Linking the site to the wider narrative is the step most students miss, and the visual connection makes it stick.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Copying rather than constructing.</strong> Tracing or re-drawing a teacher&rsquo;s diagram activates almost no memory encoding. Close the source and build from scratch.</li>
<li><strong>Over-decorating.</strong> Colour and aesthetic neatness are not the goal. A rough sketch with accurate labels beats a beautiful diagram with vague ones.</li>
<li><strong>Not combining with retrieval.</strong> A diagram drawn once is a note. A diagram redrawn from memory three times is a memory. Always close the original and reconstruct.</li>
<li><strong>Choosing the wrong visual type.</strong> A timeline for a concept that is really about competing interpretations adds confusion, not clarity. Choose the visual that mirrors the structure of the idea.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Use dual coding when you are first learning a topic, not as a last-minute revision strategy. It takes more time than re-reading but saves far more time later because the material is easier to retrieve. For History, the most valuable visuals to construct are: chronological timelines for each depth study with dates and significance annotations; cause-and-consequence maps for major turning points; change/continuity three-era diagrams for each thematic study; and a labelled sketch of each historic environment site linked to the wider thematic narrative.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 20%;" title="Study text"></span>
<span style="background: #9a3412; width: 50%;" title="Construct visual from memory"></span>
<span style="background: #c2410c; width: 30%;" title="Check &amp; redraw"></span>
</div>
<span class="guide-quick-ref-total">~25 minutes per diagram</span>
<h4>Best visual types</h4>
<ol class="guide-quick-ref-steps">
<li>Timeline &mdash; depth-study chronology</li>
<li>Cause-consequence map &mdash; turning points</li>
<li>Three-era table &mdash; thematic change</li>
<li>Spider &mdash; factors behind an event</li>
<li>Site sketch &mdash; historic environment</li>
<li>Two-column &mdash; contrasting interpretations</li>
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
    "subject_id": SUBJECT_ID,
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
<p>Facts in isolation are fragile. Facts connected by explanations survive. Elaborative interrogation is the habit of asking &ldquo;why is that true?&rdquo; and &ldquo;how does that work?&rdquo; about every fact you learn &mdash; and forcing yourself to answer. The answer doesn&rsquo;t need to be perfect. The act of trying to answer is what builds the mental connections that turn memorised dates and events into explained significance and causation. This is exactly what examiners reward in the 6-mark, 8-mark, 10-mark and 12-mark questions &mdash; not the facts themselves, but the reasoning that connects them.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Pressley et al. (1988)</strong></td><td>Asking &ldquo;why?&rdquo; during reading boosted recall by 40&ndash;70% compared to silent reading.</td><td>Works even when the answer is imperfect.</td></tr>
<tr><td><strong>Dunlosky et al. (2013)</strong></td><td>Rated &ldquo;moderate utility&rdquo; &mdash; robust across subjects and ages, especially when applied to new material that builds on existing knowledge.</td><td>Best for consolidating material you half-know.</td></tr>
<tr><td><strong>Smith &amp; Holliday (2006)</strong></td><td>Students who self-explained while studying scored significantly higher on transfer questions requiring application.</td><td>Builds the ability to USE the knowledge, not just recall it.</td></tr>
<tr><td><strong>Chi et al. (1994)</strong></td><td>Self-explanation was a stronger predictor of understanding than prior knowledge.</td><td>Even weaker students catch up by explaining to themselves.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Study a chunk of content</strong> &mdash; a lesson, a paragraph, a key date or event. Anything where facts are being introduced.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>After each fact, ask &ldquo;why?&rdquo;</strong> &mdash; why did this happen? Why was it significant? Why did the historian writing Source A reach this conclusion?</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Then ask &ldquo;how?&rdquo;</strong> &mdash; how does this connect to the wider period? How does it support or challenge the interpretation in the question? How would you use it in an 8-mark response?</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Try to answer out loud or in writing</strong> &mdash; even if your answer is wrong, the attempt activates deeper processing. Write your answer in the margin.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Check your answer against the source</strong> &mdash; does the lesson support your explanation? If not, update it. The correction matters more than the first guess.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Build chains</strong> &mdash; once you&rsquo;ve asked &ldquo;why?&rdquo; once, ask it again of your answer. Push until you hit a genuinely fundamental cause or consequence. This is where deep historical understanding forms.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Why two historians interpret the same event differently</div>
<p>Fact: the 10-mark &lsquo;why do interpretations differ?&rsquo; question is not asking you to describe how the interpretations differ &mdash; it asks you to explain why the authors reached different conclusions. Ask &ldquo;why might Historian A emphasise economic causes of Hitler&rsquo;s rise while Historian B emphasises propaganda?&rdquo; &mdash; because their access to evidence differed (B wrote after the Nuremberg Files were opened), their purpose differed (A was addressing a 1940s wartime audience), and their methodological frameworks differed. Ask &ldquo;how does the date an interpretation was written affect its reliability?&rdquo; &mdash; a historian writing in 1945 lacked access to Nazi Party membership records that post-1960s historians could consult. This three-step interrogation is the exact structure of a top-band interpretation answer.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Why source utility is about more than bias</div>
<p>Fact: a source that is &lsquo;biased&rsquo; is not automatically useless. Ask &ldquo;why might a biased source still be useful to a historian?&rdquo; &mdash; because its bias IS evidence of the attitudes of the person or organisation that produced it; a piece of Nazi propaganda is highly useful for studying what the regime wanted Germans to believe, even though it misrepresents events. Ask &ldquo;how does provenance combine with content to determine utility?&rdquo; &mdash; the origin tells you who produced it and why; the content tells you what it claims; your own contextual knowledge tells you how far the claim is supported by other evidence. Ask &ldquo;why do students lose marks on the 5-mark source question?&rdquo; &mdash; because they write &lsquo;it is biased so it is not useful&rsquo; and fail to use all three strands (content, provenance, context) together. That chain of three &ldquo;why?&rdquo; questions is the full mark scheme in reverse.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Accepting &ldquo;I don&rsquo;t know&rdquo;.</strong> Take a guess. Even a wrong guess activates the processing. Then check and correct.</li>
<li><strong>One &ldquo;why?&rdquo; and moving on.</strong> The real gains come from the third or fourth &ldquo;why?&rdquo;, when you hit the fundamental causes and the deepest analytical connections.</li>
<li><strong>Using second-order concepts as labels rather than lenses.</strong> Writing &ldquo;this is significant because it was important&rdquo; is not elaboration &mdash; it is circular. Push your &ldquo;why?&rdquo; until you explain the lasting impact on a named person, group or period.</li>
<li><strong>Skipping the check.</strong> Unchecked wrong answers reinforce misunderstanding. Always verify against the source.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Any time you are covering interpretations, source work or causation topics. Particularly powerful for the questions that carry the most marks: the 10-mark &lsquo;why do interpretations differ?&rsquo;, the 12-mark &lsquo;evaluate this interpretation&rsquo; and the 16-mark essays. Build it into every lesson revisit, not as a separate session. It adds around 50% to your reading time but makes everything else &mdash; retrieval, exam answers &mdash; significantly easier. The two most common examiner criticisms in History are &ldquo;students describe but do not explain&rdquo; and &ldquo;students can identify but not evaluate.&rdquo; Elaborative interrogation is the direct cure for both.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 20%;" title="Read fact"></span>
<span style="background: #9a3412; width: 45%;" title="Ask why/how, answer"></span>
<span style="background: #c2410c; width: 35%;" title="Check &amp; build chain"></span>
</div>
<span class="guide-quick-ref-total">Adds ~50% to reading time, transforms recall</span>
<h4>The chain</h4>
<ol class="guide-quick-ref-steps">
<li>Read the fact or date</li>
<li>Ask &ldquo;why did this happen?&rdquo;</li>
<li>Ask &ldquo;why does it matter?&rdquo;</li>
<li>Write your answer</li>
<li>Check against the source</li>
<li>Ask &ldquo;why?&rdquo; again of your answer</li>
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
    "subject_id": SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "knowledge-organisers",
    "title": "Knowledge Organisers",
    "sort_order": 6,
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Structured notes</span>
<h1>Knowledge Organisers</h1>
<p class="guide-used-in">One page per option &mdash; everything you need to know, nothing you don&rsquo;t.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>A knowledge organiser is a single page that captures all the essential facts, definitions, named individuals, key dates and second-order judgements for one option. The page itself is not the product &mdash; redrawing it from memory is. When you can reconstruct a complete knowledge organiser without looking, you have achieved the kind of well-organised memory that makes exam questions feel familiar rather than surprising.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Kirschner, Sweller &amp; Clark (2006)</strong></td><td>Structured, explicit knowledge organisation significantly outperforms unguided discovery for complex material.</td><td>Organised knowledge is recalled faster and more accurately.</td></tr>
<tr><td><strong>Sweller (1988) &mdash; Cognitive Load Theory</strong></td><td>Breaking complex content into manageable chunks prevents working memory from becoming overloaded.</td><td>One-page structure prevents the &ldquo;where do I start?&rdquo; freeze.</td></tr>
<tr><td><strong>Rosenshine (2012)</strong></td><td>Reviewing key information in small doses and checking for understanding produces the highest retention rates.</td><td>Brief, structured review beats long unstructured sessions.</td></tr>
<tr><td><strong>Willingham (2009)</strong></td><td>Prior knowledge is the single biggest predictor of how much new knowledge sticks. Well-organised schemas grow themselves.</td><td>Building strong knowledge organisers early accelerates all later learning.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Choose one option or topic</strong> &mdash; one depth study, one period, or one era of a thematic study. Not a whole paper at once &mdash; the page must fit on one side of A4.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Plan the sections</strong> &mdash; key dates and events (exact years), named individuals and their roles, key terms and definitions, second-order concept judgements (e.g. most significant cause, greatest point of change), and for thematic studies a change-across-eras tracker. These sections cover the structure of every History option.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Build the page using the lesson as source</strong> &mdash; write in your own words. If you cannot paraphrase it, you do not understand it yet.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Turn the page face-down and reconstruct it</strong> &mdash; blank paper, no notes. Fill in as much as you can. This converts the note-making activity into retrieval practice.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Compare and mark in red</strong> &mdash; every item you missed gets circled. Those circles are tomorrow&rsquo;s revision targets.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Repeat at spaced intervals</strong> &mdash; reconstruct the same organiser on day 3, day 7, day 14. Each attempt should take less time and produce fewer red circles.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Depth study knowledge organiser (Elizabethan Age or Germany 1919&ndash;1939)</div>
<p>Build a one-page organiser for your British or non-British depth study. Sections: (1) Chronology &mdash; 8&ndash;10 key events in date order, each with the exact year. For Germany: Weimar Republic founded (1919), Munich Putsch (1923), Wall Street Crash impact (1929), Hitler Chancellor (1933), Enabling Act (1933), Night of the Long Knives (1934), Anschluss (1938), Kristallnacht (1938). (2) Named figures and roles &mdash; for Germany: Hindenburg (President who appointed Hitler), Rohm (SA leader, Night of the Long Knives), Goebbels (propaganda). (3) Key terms &mdash; Lebensraum, Reichstag fire, Gestapo, NEP, perestroika (for USSR options). (4) Second-order judgement &mdash; &ldquo;Most significant cause of Hitler&rsquo;s rise: economic crisis &mdash; because without mass unemployment Nazi promises of jobs and order would have had no audience.&rdquo; Reconstruct on day 3 &mdash; the dates and specialist vocabulary are consistently the first sections students fail.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Thematic study knowledge organiser with three-era change tracker</div>
<p>Build a one-page organiser for your thematic study (Crime &amp; Punishment, Health &amp; Medicine, Warfare, or Entertainment &amp; Leisure). Sections: (1) Three-era change tracker &mdash; one row per era (Medieval, Early Modern, Modern), columns for: key crime/health issue/warfare method/leisure form, key response/treatment/weapon/venue, key turning point and date. (2) Named Acts, battles and individuals per era. (3) Historic environment link &mdash; for Crime &amp; Punishment: Policing in Liverpool &mdash; what the site shows about policing development, and how it connects to the modern era column. (4) Change vs continuity judgements &mdash; &ldquo;Greatest point of change in Health &amp; Medicine: Germ Theory 1861 (Pasteur) &mdash; because it replaced miasma theory and made targeted treatment scientifically possible for the first time.&rdquo; The historic environment link is the section most often missing in student organis ers, and it always carries marks.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Making it too long.</strong> If it doesn&rsquo;t fit on one A4 side, split it into two topics. Length signals you haven&rsquo;t condensed the content yet.</li>
<li><strong>Copying instead of paraphrasing.</strong> If you paste sentences from the lesson word-for-word, you are not processing &mdash; you are transcribing. Rephrase everything.</li>
<li><strong>Never reconstructing from memory.</strong> A knowledge organiser you don&rsquo;t rebuild from scratch is just a note. The reconstruction is the revision.</li>
<li><strong>Building all pages at once.</strong> Spreading organiser-building across the year &mdash; one page per lesson &mdash; works far better than building ten pages the week before the exam.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Build each organiser within a day of studying the lesson &mdash; while the material is fresh enough to paraphrase. Then use spaced reconstruction to keep the knowledge active. For History, the highest-value organisers to build are: one per depth study option (key dates, named figures, specialist vocabulary, top second-order judgement); one per period study unit (chronological anchor points, turning points, change vs continuity judgements); and one per thematic study era (key evidence per era, the change/continuity verdict, the historic environment site link). The thematic study organisers are particularly important because the 12-mark and 16-mark essays demand confident movement across all three eras simultaneously.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 30%;" title="Build the page"></span>
<span style="background: #9a3412; width: 40%;" title="Reconstruct from memory"></span>
<span style="background: #c2410c; width: 30%;" title="Mark &amp; repeat"></span>
</div>
<span class="guide-quick-ref-total">~30 min build + 10 min per reconstruction</span>
<h4>Five sections</h4>
<ol class="guide-quick-ref-steps">
<li>Key dates &amp; events (exact years)</li>
<li>Named figures &amp; roles</li>
<li>Key terms &amp; definitions</li>
<li>Second-order judgements</li>
<li>Thematic era change tracker</li>
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
    "subject_id": SUBJECT_ID,
    "guide_type": "revision-technique",
    "slug": "timed-practice",
    "title": "Timed Practice",
    "sort_order": 7,
    "content_html": """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Exam conditions</span>
<h1>Timed Practice</h1>
<p class="guide-used-in">Simulate the real exam &mdash; build the judgement no amount of revision can replace.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>Knowing the content is necessary but not sufficient. The History exam tests whether you can recall precise facts, analyse a source using your own contextual knowledge, evaluate competing interpretations, and build a structured analytical essay &mdash; all under time pressure and in sequence. The only way to build that combined skill is to practise it under the same conditions. Timed practice is the final layer of preparation that converts revision knowledge into exam performance.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Lyle &amp; Crawford (2011)</strong></td><td>Students who practised retrieval under timed conditions scored significantly higher than those who studied without time constraints.</td><td>The time pressure itself trains the memory and decision-making you need.</td></tr>
<tr><td><strong>Kornell &amp; Bjork (2007)</strong></td><td>Interleaved, timed retrieval practice was the condition most predictive of delayed exam performance.</td><td>Timed + interleaved is the most effective combination for exam prep.</td></tr>
<tr><td><strong>Roediger et al. (2011)</strong></td><td>Regular low-stakes testing significantly reduced exam anxiety alongside improving performance.</td><td>Timed practice reduces nerves as well as raising scores.</td></tr>
<tr><td><strong>Butler (2010)</strong></td><td>Students who practised applying knowledge in test conditions showed better transfer to novel questions than those who studied without testing.</td><td>Timed practice prepares you for questions you have never seen before.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Start with one question</strong> &mdash; choose a question type you find hard. Allocate time roughly by marks: 2 marks = 2 minutes; 4 marks = 4 minutes; 5 marks = 5&ndash;6 minutes; 6 marks = 6&ndash;7 minutes; 8 marks = 10 minutes (plan first); 10 marks = 12 minutes (plan first); 12 marks = 14 minutes; 16 marks = 18&ndash;20 minutes (2 minutes planning). Set a timer.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Attempt under strict conditions</strong> &mdash; no notes, no phone. Write the answer as a structured analytical response, not as bullet points. The 8-mark-and-above questions demand a planned structure with an argument, not a list.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Mark against a model answer</strong> &mdash; be honest. A point you wrote in a way the mark scheme would not credit does not count. The mark scheme for extended questions is banded &mdash; identify which band your answer sits in and what the next band requires.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Annotate why you missed marks</strong> &mdash; was it recall (didn&rsquo;t know the date or name)? Analysis (described events instead of explaining significance)? Source utility (judged bias without using content, provenance and context)? Interpretations (said how they differ, not why)? Different causes need different fixes.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Build up to a full paper</strong> &mdash; one question &rarr; one question type across topics &rarr; half a paper &rarr; full paper under exam conditions.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Debrief every paper</strong> &mdash; three minutes reviewing where marks were lost is worth more than an hour of extra revision on topics you already know.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>History Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; The 5-mark &lsquo;how useful is this source?&rsquo; question</div>
<p>Practise the source utility question under strict time: allow 5&ndash;6 minutes. Use a source you haven&rsquo;t seen before. Aim to cover all three strands: (1) Content &mdash; what does the source actually say or show that is useful? Quote or reference it precisely. (2) Provenance &mdash; who produced it, when, and why? How does the producer&rsquo;s purpose or position affect what they chose to include or omit? (3) Own contextual knowledge &mdash; what do you know from beyond the source that supports or limits its usefulness? The single most common error in this question is writing &ldquo;it is biased therefore it is limited.&rdquo; Practise under time until all three strands feel automatic &mdash; a source&rsquo;s bias is part of its utility, not a reason to dismiss it. If you cannot cover all three strands in 6 minutes, your organiser-level knowledge is the gap to fix.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; The 16-mark essay (period study or thematic change)</div>
<p>The 16-mark &lsquo;how far do you agree?&rsquo; essay is the highest-mark question on the paper. Allow 18&ndash;20 minutes total: 2 minutes planning, 16&ndash;18 minutes writing. In the 2-minute plan, decide your argument (agree, mostly agree, disagree, or conditional) and identify three paragraphs worth of evidence &mdash; two supporting, one challenging. For a thematic study essay, each paragraph must draw on a different era (Medieval, Early Modern, Modern) and weigh change against continuity rather than listing events in order. Common pitfalls to practise avoiding: (1) Writing in the first person (&ldquo;I think...&rdquo;) &mdash; write as a structured analytical argument. (2) Avoiding specialist vocabulary &mdash; terms like <em>chevauch&eacute;e</em>, <em>recusancy</em>, <em>Anschluss</em> or <em>NEP</em> earn SPaG marks and signal command of the period. (3) Describing events rather than using them as evidence for the argument. Mark your practice essays against the banded mark scheme before the exam; recognising a Level 3 response from a Level 4 response is the most efficient way to raise your final mark.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Doing timed practice too early.</strong> If you don&rsquo;t know the content yet, timed practice just practises failure. Retrieval, spaced repetition and knowledge organisers come first.</li>
<li><strong>Spending too long on low-mark questions.</strong> A 2-mark &lsquo;describe a feature&rsquo; question should not take more than 2 minutes. Every minute over budget is a minute stolen from the 16-mark essay where the real grade-boundary marks live.</li>
<li><strong>Marking too generously.</strong> A vague or half-formed answer is not a mark. Apply the mark scheme strictly &mdash; the exam will.</li>
<li><strong>Practising only the questions you find easy.</strong> Timed practice on familiar material is comfortable but not useful. Target the question types where you consistently lose marks: usually the source utility, the interpretations question, or the extended essay.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Begin single-question timed practice once you have covered each option. In the final six weeks before the exam, attempt at least one timed section per week. In the final two weeks, do at least one full timed paper. The mark-per-minute budget is roughly as follows: 2-mark questions = 2 minutes; 4-mark = 4 minutes; 5-mark source = 6 minutes; 6-mark explain = 7 minutes; 8-mark significance = 10 minutes (plan 2); 10-mark interpretations = 12 minutes (plan 2); 12-mark essay = 14 minutes (plan 2); 16-mark essay = 20 minutes (plan 2). The 8-mark-and-above questions demand written planning time &mdash; practise building the habit of planning under the clock. Use the StudyVault practice questions for structured low-stakes timed retrieval, then work up to past papers and mark-scheme marking for the higher-mark questions.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #7c2d12; width: 15%;" title="Setup &amp; plan"></span>
<span style="background: #9a3412; width: 60%;" title="Attempt under time"></span>
<span style="background: #c2410c; width: 25%;" title="Mark &amp; debrief"></span>
</div>
<span class="guide-quick-ref-total">~1 min per mark + 2 min plan (8+ marks) + 3 min debrief</span>
<h4>Build-up schedule</h4>
<ol class="guide-quick-ref-steps">
<li>One question, timed</li>
<li>One question type across topics</li>
<li>Half a paper, timed</li>
<li>Full paper, timed</li>
<li>Full paper, exam conditions</li>
<li>Debrief every attempt</li>
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
# UPSERT ALL PAGES
# ─────────────────────────────────────────────────────────────

print(f"\nUpserting {len(pages)} guide pages for History (Eduqas)...")

for page in pages:
    result = sb.table('guide_pages').upsert(
        page,
        on_conflict='subject_id,guide_type,slug'
    ).execute()
    print(f"  OK: sort_order={page['sort_order']} slug={page['slug']}")

print("\nDone. Verifying...")
rows = sb.table('guide_pages').select('slug,title,sort_order').eq(
    'subject_id', SUBJECT_ID
).eq('guide_type', 'revision-technique').order('sort_order').execute()

print(f"\n{'sort_order':<12} {'slug':<35} {'title'}")
print("-" * 75)
for row in rows.data:
    print(f"{row['sort_order']:<12} {row['slug']:<35} {row['title']}")

print(f"\nTotal rows: {len(rows.data)}/8")
