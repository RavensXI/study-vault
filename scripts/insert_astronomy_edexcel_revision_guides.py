"""
Insert Astronomy revision technique guide pages into Supabase.
Subject slug: astronomy-edexcel
Subject ID: looked up dynamically by slug at runtime.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://baipckgywpnwapobwtsy.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

SLUG = 'astronomy-edexcel'

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
<p>Evidence-based strategies tailored to Astronomy. The written papers reward students who can recall equations precisely &mdash; parallax, distance modulus, Hubble&rsquo;s law, telescope magnification, Kepler&rsquo;s third law, redshift &mdash; apply them to unfamiliar observational scenarios, and build explained evaluations in extended responses. The most-missed points in past examiner reports are sidereal vs synodic period confusion, reversed HR diagram axes, and the three Big Bang evidence strands. These techniques are chosen to directly address those gaps.</p>
</div>
</div>
<div class="guide-hub">

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Foundation Techniques</h2>
<span class="guide-paper-ref">Start early &mdash; use these from day one</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="{BASE}/retrieval-practice">
<span class="guide-question-marks">Active recall</span>
<h3>Retrieval Practice</h3>
<p>Test yourself on equations, definitions and object classifications rather than re-reading. Brain dumps of the HR diagram axis labels, the Chandrasekhar limit, and the sidereal vs synodic distinction reveal exactly what you can&rsquo;t name &mdash; and lock in what you can.</p>
</a>
<a class="guide-question-card" href="{BASE}/spaced-repetition">
<span class="guide-question-marks">Distributed practice</span>
<h3>Spaced Repetition</h3>
<p>Revisit parallax calculations, stellar evolution paths, and eclipse geometry at 1, 3, 7, 14 and 30-day gaps. Works far better than cramming and stops the &lsquo;I knew this last week&rsquo; feeling on exam day.</p>
</a>
<a class="guide-question-card" href="{BASE}/dual-coding">
<span class="guide-question-marks">Visual learning</span>
<h3>Dual Coding</h3>
<p>Combine words and visuals. An HR diagram sketched from memory with correctly reversed temperature axis, an eclipse umbra/penumbra diagram, or a stellar evolution flowchart sticks far better than text alone.</p>
</a>
</div>
</div>

<div class="guide-paper" style="--paper-accent: #16a34a; --paper-light: #f0fdf4;">
<div class="guide-paper-header">
<h2>Stretch Techniques</h2>
<span class="guide-paper-ref">Use these once you know the basics</span>
</div>
<div class="guide-paper-questions">
<a class="guide-question-card" href="{BASE}/interleaving">
<span class="guide-question-marks">Mixed practice</span>
<h3>Interleaving</h3>
<p>Mix naked-eye observation, telescopic, and cosmology questions in one session. Trains you to identify which topic area a question targets &mdash; the exact skill the data-response papers test when an unfamiliar observational scenario appears.</p>
</a>
<a class="guide-question-card" href="{BASE}/elaborative-interrogation">
<span class="guide-question-marks">Deep thinking</span>
<h3>Elaborative Interrogation</h3>
<p>Ask &ldquo;why?&rdquo; and &ldquo;how?&rdquo; about every fact. Why does a higher-mass star leave the main sequence sooner? How does the redshift of galaxies constitute evidence for an expanding universe? Turn memorised equations into understood physics.</p>
</a>
<a class="guide-question-card" href="{BASE}/knowledge-organisers">
<span class="guide-question-marks">Structured notes</span>
<h3>Knowledge Organisers</h3>
<p>One page per topic area. Equations with correct symbols and units, HR diagram regions, stellar evolution tracks by mass, the three Big Bang evidence strands. Redraw from memory. The base layer of solid exam preparation.</p>
</a>
<a class="guide-question-card" href="{BASE}/timed-practice">
<span class="guide-question-marks">Exam conditions</span>
<h3>Timed Practice</h3>
<p>Simulate the real thing. The papers mix short calculation questions with data-response scenarios and extended explanations &mdash; practising under time pressure builds the judgement about when to calculate and when to describe.</p>
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
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; The key equations brain dump</div>
<p>After studying the measurement and distance lessons, close the lesson and write all six core equations from memory &mdash; parallax distance \\(d = 1/p\\) (d in parsecs, p in arcseconds); distance modulus \\(m - M = 5\\log(d) - 5\\); Hubble&rsquo;s law \\(v = H_0 d\\) (\\(H_0 \\approx 70\\) km s\\(^{-1}\\) Mpc\\(^{-1}\\)); telescope magnification \\(M = f_o / f_e\\); Kepler&rsquo;s third law \\(T^2 \\propto r^3\\); redshift \\(\\Delta\\lambda / \\lambda = v / c\\). For each, write the quantity each symbol represents and one worked example with units. Check back and highlight any symbol you mis-remembered. Examiner reports confirm that unit errors and symbol confusion account for a disproportionate share of lost calculation marks.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Sidereal vs synodic period</div>
<p>The sidereal vs synodic period distinction is the most-missed point across past examiner reports &mdash; brain dump it cold. Write: &ldquo;Sidereal period: time for a body to complete one orbit relative to the distant stars &mdash; the true orbital period. Synodic period: time between successive identical alignments relative to the Sun as seen from Earth &mdash; always longer for an outer planet, shorter for Mercury and Venus.&rdquo; Then write one numerical example for Mars: sidereal period 687 days, synodic period 780 days. Explain in one sentence why they differ. Check and correct any part you got wrong. Retest in three days cold.</p>
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
<p>Build it in <strong>every week</strong>, from the start of your course through to your exams. Aim for 15&ndash;20 minutes per session, two or three times a week. The last two weeks before an exam is when retrieval practice becomes your main tool &mdash; swap passive reading for equation brain dumps, HR diagram redraws, and stellar evolution flashcards. On StudyVault, the Knowledge Check and Flashcard buttons in every lesson sidebar are retrieval practice in disguise &mdash; use them.</p>
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
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Stellar evolution paths</div>
<p>You study stellar evolution on Monday: low-mass stars (like the Sun) leave the main sequence, expand to red giants, shed a planetary nebula, and leave a white dwarf cooling to a black dwarf. High-mass stars expand to red supergiants, then explode as supernovae, leaving either a neutron star or (above the Chandrasekhar limit of 1.4 M&#9737;) collapsing to a black hole. On Tuesday do a quick brain dump of both paths from memory. On Thursday redo the dump, this time adding one observable feature per stage &mdash; for example, &ldquo;red giant: luminosity high, temperature low &mdash; plots upper-right of HR diagram.&rdquo; The following Monday, answer a timed question cold using the Brackenfell Observing Society scenario: &ldquo;Member Priya Nair asks why the star Betelgeuse is both very bright and very red. Explain using its position on the HR diagram.&rdquo; Each review takes under 10 minutes and the spacing means the paths feel automatic by exam day.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Equatorial coordinate recall</div>
<p>After first covering the celestial sphere lessons, log the equatorial coordinate system on a revision tracker. Day 1 review: write from memory that right ascension (RA) is measured in hours (0h to 24h) eastward from the vernal equinox, and declination (Dec) is measured in degrees (\\(-90°\\) to \\(+90°\\)) from the celestial equator. Day 7 review: recall the same definitions and add a worked example &mdash; &ldquo;Sirius: RA 06h 45m, Dec \\(-16°43'\\) &mdash; visible from UK in winter evenings, transits south of zenith because its declination is negative.&rdquo; Day 21 review: answer a short question from the Caerwyn Observatory scenario. The RA-in-hours vs degrees confusion is a reliable mark-loser &mdash; spacing your review directly targets it.</p>
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
<p>Most students revise by blocking &mdash; an hour on the solar system, an hour on stars, an hour on cosmology. It feels productive and the topic seems clear by the end. Interleaving is the opposite: you jump between topics inside a single session. It feels worse at the time, and you&rsquo;ll make more mistakes. But when the real exam arrives, you will be dramatically better at knowing <em>which</em> idea a question is testing &mdash; and that is usually the hardest part of an unfamiliar observational scenario.</p>
<h3>Evidence Base</h3>
<table class="guide-levels">
<thead><tr><th>Study</th><th>Finding</th><th>Impact</th></tr></thead>
<tbody>
<tr><td><strong>Rohrer &amp; Taylor (2007)</strong></td><td>Students who interleaved topics scored 43% higher on delayed tests than blocked-practice students.</td><td>Same time spent &mdash; huge difference in exam performance.</td></tr>
<tr><td><strong>Birnbaum et al. (2013)</strong></td><td>Interleaved learners felt LESS confident during practice but performed BETTER in the test.</td><td>If revision feels too easy, interleave.</td></tr>
<tr><td><strong>Bjork &amp; Bjork (2011)</strong></td><td>Desirable difficulties &mdash; including interleaving &mdash; create durable long-term learning at the cost of short-term performance.</td><td>Short-term struggle is the price of long-term gain.</td></tr>
<tr><td><strong>Taylor &amp; Rohrer (2010)</strong></td><td>Benefit was largest when topics looked superficially similar &mdash; students learnt to DISTINGUISH them.</td><td>Most useful where students confuse related ideas.</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Pick 3&ndash;5 related topics</strong> &mdash; topics that share a paper, a theme, or a question type. Similar enough that students confuse them.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Make a mixed problem set</strong> &mdash; 10&ndash;15 questions drawn from all the topics. Don&rsquo;t label which topic each question belongs to.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Attempt each question cold</strong> &mdash; the first step is identifying what&rsquo;s being asked. That identification is the skill you&rsquo;re training.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Mark after every question</strong> &mdash; note which topic area each one was. Pay attention to mis-identifications &mdash; those are the highest-value gaps.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Rebuild a new mixed set tomorrow</strong> &mdash; same topics, different questions, different order. Over time, misclassifications drop.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Expect to feel worse than blocked practice</strong> &mdash; that&rsquo;s the right feeling. Your exam self will thank you.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Sidereal vs synodic vs orbital period topic mix</div>
<p>Mix questions covering sidereal period, synodic period, and Kepler&rsquo;s third law in one 40-minute session. Write 12 questions on separate slips: four from each area, shuffled. Before each question, ask yourself: &ldquo;Is this about the true orbital period, the observed repeat alignment, or the orbital radius relationship?&rdquo; Students frequently confuse the sidereal period (star-referenced, the true period) with the synodic period (Sun-referenced, what Earth observers actually measure) &mdash; the identification exercise in revision prevents losing marks on what examiners confirm is the most-missed distinction. After each attempt, record whether you identified the concept correctly before calculating.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Naked-eye vs telescopic observation topic mix</div>
<p>The course splits cleanly across 12 naked-eye lessons (constellation patterns, seasonal visibility, planets to the unaided eye, eclipse geometry) and 14 telescopic lessons (refractors, reflectors, eyepiece calculations, CCD imaging, radio telescopes). Mix questions from both halves &mdash; for example: &ldquo;Marina Vassilakis at Caerwyn Observatory uses a refractor with focal lengths \\(f_o = 1200\\) mm, \\(f_e = 25\\) mm. What magnification does she achieve?&rdquo; alongside &ldquo;Dr Halima Yousef observes that Orion is highest in the sky at midnight in January. Explain why, using the Earth&rsquo;s orbital position.&rdquo; The two question types demand different reasoning skills; interleaving forces you to switch between them rapidly, exactly as the exam paper does.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Interleaving before you know the basics.</strong> You need to know each topic individually first. Use interleaving once you&rsquo;ve studied both halves of the course &mdash; not as a first-pass strategy.</li>
<li><strong>Giving up because it feels hard.</strong> Difficulty during interleaved practice is the signal it&rsquo;s working. Persist.</li>
<li><strong>Mixing unrelated topics.</strong> Interleaving works best when the topics are related enough to be confused. Mix topics within the same conceptual area &mdash; distance measures, stellar classification, or period types &mdash; not random combinations.</li>
<li><strong>Not checking mis-identifications.</strong> The mistake is the data. If you mislabelled a question as being about &lsquo;telescope design&rsquo; when it was about &lsquo;eyepiece magnification&rsquo;, that confusion is exactly what needs fixing.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Start interleaving once you have studied all major topic areas at least once. In the final six weeks before the exam, replace most blocked revision with interleaved mixed sets. Particularly powerful the week before the exam when you want to simulate the varied order in which questions appear on the actual papers.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 15%;" title="Choose topics"></span>
<span style="background: #22c55e; width: 55%;" title="Mixed problem set"></span>
<span style="background: #4ade80; width: 30%;" title="Mark &amp; review mis-IDs"></span>
</div>
<span class="guide-quick-ref-total">~40 minutes per interleaved session</span>
<h4>Steps</h4>
<ol class="guide-quick-ref-steps">
<li>Pick 3&ndash;5 related topics</li>
<li>Build mixed question set</li>
<li>Identify the topic first</li>
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
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Choose the right visual type</strong> &mdash; timelines for sequences, two-column tables for comparisons, flowcharts for processes, annotated sketches for physical geometry.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Add labels in your own words</strong> &mdash; the label is not decoration. It forces you to translate the concept into language you own.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Check against the source</strong> &mdash; compare your diagram to the lesson. Correct anything missing or wrong in a different colour.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Redraw from memory a week later</strong> &mdash; combine with spaced repetition. Redrawing is retrieval practice for visual memories.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; The HR diagram from memory</div>
<p>After studying stellar classification, close the lesson and draw a blank HR diagram from scratch. The most-missed feature is the axis orientation: temperature increases to the <em>left</em> along the x-axis (reversed), and luminosity increases upward on the y-axis (in solar luminosities, \\(L/L_\\odot\\)). Populate from memory: the main sequence running from upper-left (hot, luminous O-type blue stars) to lower-right (cool, dim M-type red dwarfs); red giants and supergiants in the upper-right; white dwarfs in the lower-left. Mark the Sun&rsquo;s approximate position (spectral type G, \\(L = 1\\,L_\\odot\\)). Check back &mdash; most students place the Sun too high or put temperature increasing left-to-right. Correct any errors in red and redraw in one week.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Eclipse geometry umbra and penumbra</div>
<p>After studying eclipses, sketch the Sun&ndash;Moon&ndash;Earth geometry for both a total solar eclipse and a lunar eclipse on the same page from memory. Label the umbra (the region of total shadow, where the light source is completely blocked) and the penumbra (the region of partial shadow). Annotate why the Moon&rsquo;s distance variation matters &mdash; when the Moon is near apogee and appears smaller than the Sun&rsquo;s disc, the result is an annular eclipse rather than a total eclipse. Add a second sketch showing the tidal bulge: differential gravitational force across the Earth&rsquo;s diameter, greater on the near side, creating two bulges &mdash; the Moon-facing bulge from direct attraction, the far-side bulge from the Earth being pulled away more than the ocean. Check against the lesson and correct any geometry errors in red.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Copying rather than constructing.</strong> Tracing or re-drawing a teacher&rsquo;s diagram activates almost no memory encoding. Close the source and build from scratch.</li>
<li><strong>Over-decorating.</strong> Colour and aesthetic neatness are not the goal. A rough sketch with accurate labels beats a beautiful diagram with vague ones.</li>
<li><strong>Not combining with retrieval.</strong> A diagram drawn once is a note. A diagram redrawn from memory three times is a memory. Always close the original and reconstruct.</li>
<li><strong>Forgetting reversed axes on the HR diagram.</strong> This is the single most common dual-coding error in Astronomy &mdash; always check temperature increases to the left before marking your diagram complete.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Use dual coding when you are first learning a topic, not as a last-minute revision strategy. It takes more time than re-reading but saves far more time later because the material is easier to retrieve. For Astronomy, the highest-value visuals to construct are: the HR diagram with correctly reversed temperature axis and all four stellar populations labelled; the stellar evolution flowchart for low-mass and high-mass stars; the eclipse geometry diagram with umbra/penumbra; the equatorial coordinate sphere with RA and Dec marked; and the parallax geometry triangle with the 1 AU baseline and arcsecond angle labelled.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 20%;" title="Study text"></span>
<span style="background: #22c55e; width: 50%;" title="Construct visual from memory"></span>
<span style="background: #4ade80; width: 30%;" title="Check &amp; redraw"></span>
</div>
<span class="guide-quick-ref-total">~25 minutes per diagram</span>
<h4>Best visual types</h4>
<ol class="guide-quick-ref-steps">
<li>HR diagram &mdash; reversed temp axis</li>
<li>Stellar evolution flowchart</li>
<li>Eclipse umbra/penumbra sketch</li>
<li>Equatorial coordinate sphere</li>
<li>Parallax triangle with 1 AU baseline</li>
<li>Telescope ray diagram</li>
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
<p>Facts in isolation are fragile. Facts connected by explanations survive. Elaborative interrogation is the habit of asking &ldquo;why is that true?&rdquo; and &ldquo;how does that work?&rdquo; about every fact you learn &mdash; and forcing yourself to answer. The answer doesn&rsquo;t need to be perfect. The act of trying to answer is what builds the mental connections that turn memorised lists into understood physics. This is exactly what examiners reward in &lsquo;explain&rsquo; and &lsquo;evaluate&rsquo; questions.</p>
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
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Study a chunk of content</strong> &mdash; a lesson, a paragraph, a key fact. Anything where facts are being introduced.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>After each fact, ask &ldquo;why?&rdquo;</strong> &mdash; why is this true? Why does it work this way? Why does the examiner care about it?</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Then ask &ldquo;how?&rdquo;</strong> &mdash; how does this connect to the topic? How does it lead to what comes next? How would you explain it to someone else?</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Try to answer out loud or in writing</strong> &mdash; even if your answer is wrong, the attempt activates deeper processing. Write your answer in the margin.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Check your answer against the source</strong> &mdash; does the lesson support your explanation? If not, update it. The correction matters more than the first guess.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Build chains</strong> &mdash; once you&rsquo;ve asked &ldquo;why?&rdquo; once, ask it again of your answer. Push until you hit a genuinely fundamental fact. This is where deep understanding forms.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Why redshift constitutes evidence for an expanding universe</div>
<p>Fact: the spectral lines of distant galaxies are shifted toward longer (redder) wavelengths. Ask &ldquo;why does that happen?&rdquo; &mdash; because the galaxies are moving away from us; the Doppler effect stretches the wavelength of emitted light, and \\(\\Delta\\lambda / \\lambda = v/c\\). Ask &ldquo;how does the degree of shift relate to distance?&rdquo; &mdash; Hubble found that recession speed is proportional to distance: \\(v = H_0 d\\), with \\(H_0 \\approx 70\\) km s\\(^{-1}\\) Mpc\\(^{-1}\\). Ask &ldquo;why does this mean the universe is expanding rather than just that galaxies are moving through space?&rdquo; &mdash; because the relationship holds in every direction with no central point, which means space itself is stretching. That three-step chain is exactly the reasoning a 4-mark &lsquo;explain&rsquo; question on Big Bang evidence expects.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Why a high-mass star ends its life differently from a low-mass star</div>
<p>Fact: stars above approximately 8 solar masses end as supernovae rather than planetary nebulae. Ask &ldquo;why does mass determine the endpoint?&rdquo; &mdash; because higher mass means higher core temperature and pressure, which allows fusion to continue beyond helium to carbon, neon, oxygen, silicon, and eventually iron. Ask &ldquo;why does iron end fusion?&rdquo; &mdash; because iron has the highest binding energy per nucleon; fusing iron absorbs energy rather than releasing it, so the energy source driving the star switches off. Ask &ldquo;why does the core then collapse?&rdquo; &mdash; because without radiation pressure, gravity overwhelms the electron degeneracy pressure if the core exceeds the Chandrasekhar limit of 1.4 M&#9737;, producing a neutron star or black hole. That chain converts a memorised fact into an explained mechanism.</p>
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
<p>Any time you are covering conceptual material &mdash; not just recalling named items. Particularly powerful for the three Big Bang evidence strands (redshift, CMB at 2.7 K, quasar distribution), the mass-dependent stellar evolution tracks, and the eclipse geometry questions. Build it into every lesson revisit, not as a separate session. It adds around 50% to your reading time but makes everything else &mdash; retrieval, exam answers &mdash; significantly easier.</p>
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
<h4>The chain</h4>
<ol class="guide-quick-ref-steps">
<li>Read the fact</li>
<li>Ask &ldquo;why is this true?&rdquo;</li>
<li>Ask &ldquo;how does it work?&rdquo;</li>
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
<p class="guide-used-in">One page per topic &mdash; everything you need to know, nothing you don&rsquo;t.</p>
</div>

<div class="guide-section">
<h2>What the Research Says</h2>
<p>A knowledge organiser is a single page that captures all the essential facts, definitions, named lists and examples for one topic. The page itself is not the product &mdash; redrawing it from memory is. When you can reconstruct a complete knowledge organiser without looking, you have achieved the kind of well-organised memory that makes exam questions feel familiar rather than surprising.</p>
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
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Choose one topic</strong> &mdash; one lesson or one spec topic area. Not a whole unit at once &mdash; the page must fit on one side of A4.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Plan the sections</strong> &mdash; key terms and definitions, equations with symbol glossaries and units, named classifications (spectral types, stellar populations, telescope types), a worked numerical example, a mini diagram or sketch. These sections cover the structure of every Astronomy topic.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Build the page using the lesson as source</strong> &mdash; write in your own words. If you cannot paraphrase it, you do not understand it yet.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Turn the page face-down and reconstruct it</strong> &mdash; blank paper, no notes. Fill in as much as you can. This converts the note-making activity into retrieval practice.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Compare and mark in red</strong> &mdash; every item you missed gets circled. Those circles are tomorrow&rsquo;s revision targets.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Repeat at spaced intervals</strong> &mdash; reconstruct the same organiser on day 3, day 7, day 14. Each attempt should take less time and produce fewer red circles.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Equations and distance measures organiser</div>
<p>Build a one-page organiser covering the six key equations. Sections: (1) Parallax &mdash; \\(d\\,(\\text{pc}) = 1 / p\\,(\\text{arcsec})\\); baseline = 1 AU; only reliable within ~1000 pc. (2) Distance modulus &mdash; \\(m - M = 5\\log(d) - 5\\); \\(m\\) = apparent magnitude, \\(M\\) = absolute magnitude, \\(d\\) in parsecs. (3) Hubble&rsquo;s law &mdash; \\(v = H_0 d\\); \\(H_0 \\approx 70\\) km s\\(^{-1}\\) Mpc\\(^{-1}\\). (4) Telescope magnification &mdash; \\(M = f_o / f_e\\); \\(f_o\\) = objective focal length, \\(f_e\\) = eyepiece focal length. (5) Kepler&rsquo;s third law &mdash; \\(T^2 \\propto r^3\\) (same for all planets orbiting the same star). (6) Redshift &mdash; \\(\\Delta\\lambda / \\lambda = v / c\\). Include a worked example for each. Reconstruct on day 3 &mdash; the symbol-to-quantity mapping is the first thing students drop, and incorrect units lose marks even when the method is right.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; Big Bang evidence strands organiser</div>
<p>Build a one-page organiser for the three Big Bang evidence strands. Sections: (1) Galactic redshift &mdash; Hubble (1929) found all galaxies recede; recession speed proportional to distance (\\(v = H_0 d\\)); implies universe expanding from a common origin. (2) Cosmic Microwave Background (CMB) &mdash; uniform 2.7 K radiation across the entire sky; predicted as the cooled relic of the hot early universe; discovered by Penzias &amp; Wilson (1965). (3) Quasar distribution &mdash; quasars are only observed at high redshift (i.e. great distances, early universe); none nearby &mdash; evidence the universe was different in the past, inconsistent with a steady-state model. Add one counter-argument per strand (e.g. CMB: could have another source?) and a rebuttal. Reconstruct in one week. Students who can reproduce all three strands with their rebuttals are ready for any extended-response cosmology question.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Making it too long.</strong> If it doesn&rsquo;t fit on one A4 side, split it into two topics. Length signals you haven&rsquo;t condensed the content yet.</li>
<li><strong>Copying instead of paraphrasing.</strong> If you paste sentences from the lesson word-for-word, you are not processing &mdash; you are transcribing. Rephrase everything.</li>
<li><strong>Never reconstructing from memory.</strong> A knowledge organiser you don&rsquo;t rebuild from scratch is just a note. The reconstruction is the revision.</li>
<li><strong>Building all pages at once.</strong> Spreading organiser-building across the year &mdash; one page per lesson &mdash; works far better than building all 26 pages the week before the exam.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Build each organiser within a day of studying the lesson &mdash; while the material is fresh enough to paraphrase. Then use spaced reconstruction to keep the knowledge active. For Astronomy, the highest-value organisers to build are: the six core equations with symbol glossaries and units; the HR diagram with all four stellar populations; the stellar evolution flowchart for low-mass and high-mass paths; the three Big Bang evidence strands with rebuttals; and the sidereal vs synodic period comparison with worked numerical examples. These are the topics that appear most consistently in mark scheme breakdowns.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 30%;" title="Build the page"></span>
<span style="background: #22c55e; width: 40%;" title="Reconstruct from memory"></span>
<span style="background: #4ade80; width: 30%;" title="Mark &amp; repeat"></span>
</div>
<span class="guide-quick-ref-total">~30 min build + 10 min per reconstruction</span>
<h4>Five sections</h4>
<ol class="guide-quick-ref-steps">
<li>Key terms &amp; definitions</li>
<li>Equations with symbol glossary</li>
<li>Named classifications</li>
<li>Worked numerical example</li>
<li>Mini diagram or sketch</li>
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
<p>Knowing the content is necessary but not sufficient. The exam tests whether you can recall equations, apply them to unfamiliar data, and communicate explanations clearly under time pressure &mdash; all at once. The only way to build that combined skill is to practise it under the same conditions. Timed practice is the final layer of preparation that converts revision knowledge into exam performance.</p>
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
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Start with one question</strong> &mdash; choose a question type you find hard. Allocate time: roughly 1 minute per mark. Set a timer.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Attempt under strict conditions</strong> &mdash; no notes, no phone. Show all working for calculations, even if you are not confident in the answer.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Mark against a model answer</strong> &mdash; be honest. A correct numerical answer with no working shown will not receive full marks. Check that units and significant figures are present.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Annotate why you missed marks</strong> &mdash; was it recall (forgot the equation)? Substitution (wrong value in the right formula)? Communication (right idea, wrong units)? Different causes need different fixes.</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Build up to a full paper</strong> &mdash; one question &rarr; one topic section &rarr; half a paper &rarr; full paper under exam conditions.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>Debrief every paper</strong> &mdash; three minutes reviewing where marks were lost is worth more than an hour of extra revision on topics you already know.</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Astronomy Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1 &mdash; Timed calculation question</div>
<p>Practise calculation questions cold under timed conditions. Allow 4 minutes for a 4-mark calculation: &ldquo;The Brackenfell Observing Society measures the parallax of a nearby star as 0.042 arcseconds. Calculate the distance to the star in parsecs and in light-years. Show your working.&rdquo; Work through: \\(d = 1/p = 1/0.042 \\approx 23.8\\) pc; convert to light-years (1 pc = 3.26 ly) giving \\(23.8 \\times 3.26 \\approx 77.6\\) ly. If you overran 4 minutes, that is the bottleneck to fix. If you forgot the conversion factor, that is a retrieval gap &mdash; add it to your spaced repetition schedule. The examiner&rsquo;s mark scheme awards one mark for the correct equation, one for correct substitution, one for the numerical answer in parsecs, and one for the light-year conversion &mdash; losing any one of these four independent marks is the most common calculation failure pattern.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2 &mdash; The extended explanation question</div>
<p>Extended questions of 5&ndash;6 marks require structured explanation, not just recall. Practise with: &ldquo;Dr Halima Yousef observes the spectrum of a distant galaxy and notes that all spectral lines are shifted toward longer wavelengths. Explain what this tells us about the galaxy and what it implies about the large-scale structure of the universe.&rdquo; Plan for 1&ndash;2 minutes before writing: (1) define redshift using \\(\\Delta\\lambda / \\lambda = v/c\\); (2) state the galaxy is receding; (3) link to Hubble&rsquo;s law &mdash; recession speed proportional to distance; (4) state this is observed in all directions; (5) conclude the universe is expanding from a common origin &mdash; the Big Bang. Mark your answer: the top mark band requires the equation, Hubble&rsquo;s law, and the expanding-universe inference, not just &ldquo;the galaxy is moving away.&rdquo; Build the habit of planning before writing under time pressure.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Doing timed practice too early.</strong> If you don&rsquo;t know the content yet, timed practice just practises failure. Retrieval, spaced repetition and knowledge organisers come first.</li>
<li><strong>Skipping units and significant figures.</strong> In calculation questions, correct numerical answers without correct units frequently drop marks. Practise writing units alongside every number from the start.</li>
<li><strong>Marking too generously.</strong> A vague or half-formed answer is not a mark. Apply the mark scheme strictly &mdash; the exam will.</li>
<li><strong>Practising only the questions you find easy.</strong> Timed practice on familiar material is comfortable but not useful. Target the question types where you consistently lose marks &mdash; for most students, these are calculation chains and extended cosmology explanations.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Begin single-question timed practice once you have covered each topic area. In the final six weeks before the exam, attempt at least one timed section per week. In the final two weeks, do at least one full timed paper. Allocate roughly 1 minute per mark. Extended explanation questions (5&ndash;6 marks) need 1&ndash;2 minutes of planning before you write &mdash; practise building that planning habit under time pressure. Use the StudyVault practice questions for structured low-stakes timed retrieval, then work up to past papers for the higher-mark questions.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 15%;" title="Setup"></span>
<span style="background: #22c55e; width: 60%;" title="Attempt under time"></span>
<span style="background: #4ade80; width: 25%;" title="Mark &amp; debrief"></span>
</div>
<span class="guide-quick-ref-total">~1 minute per mark + 3 min debrief</span>
<h4>Build-up schedule</h4>
<ol class="guide-quick-ref-steps">
<li>One question, timed</li>
<li>One topic section, timed</li>
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

print(f"\nUpserting {len(pages)} guide pages for Astronomy...")

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
