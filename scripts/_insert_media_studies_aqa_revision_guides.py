"""Insert/update revision-technique guide pages for Media Studies (AQA 8572)."""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
from lib.supabase_client import get_client

SUBJECT_ID = "538bc758-a36f-442a-9d68-d58e664f5649"
SUBJECT_SLUG = "media-studies-aqa"
SUBJECT_NAME = "Media Studies"
GUIDE_TYPE = "revision-technique"
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "REVISION_TECHNIQUES")

# -------- Examples per technique (AQA Media Studies 8572) --------

EXAMPLES = {
    "retrieval-practice": (
        # Example 1 — Theorist brain dump (highest exam-value activity)
        "After studying Narrative Theory: Propp, Todorov and Audience Engagement (Media Language, L3), close the tab and write down Todorov’s five-stage equilibrium structure from memory — equilibrium, disruption, complication, climax, new equilibrium — with one sentence explaining what happens at each stage. Then, in a separate column, list as many of Propp’s eight character functions as you can recall alongside one example from a media product you know. Compare to the lesson, highlight the gaps in a different colour, and retest only the missed items the following day.",
        # Example 2 — Regulator acronym recall
        "After studying Regulation, Digital Disruption and the key UK regulators (Media Industries, L5), shut the tab and write down the name, the full acronym, and the remit of each of the five regulators covered: OFCOM, IPSO, BBFC, ASA and PEGI. Common error: students swap remits — for example attributing press regulation to OFCOM instead of IPSO. Check your list against the lesson and rewrite any swapped remits in red. Return to the same test tomorrow before moving on — accuracy on regulators is mark-affecting in extended responses."
    ),
    "spaced-repetition": (
        # Example 1 — Encoding/decoding model
        "On the day you study Audience Interpretation and Hall’s Reception Theory (Media Representations, L5), write a one-paragraph summary of Stuart Hall’s three audience reading positions — preferred, negotiated and oppositional — and note the social variables (age, class, gender, ethnicity) that shape them. Retest on day 1, day 3, day 7, day 14 and day 30, each time adding one worked example of a real media product and the reading position an audience group might take. Examiners reward the negotiated reading most often in extended answers because students routinely collapse Hall into a binary (accept or reject) and miss the middle ground entirely.",
        # Example 2 — Theorist pairings across units
        "When you reach Uses and Gratifications Theory — Active and Passive Audiences (Media Audiences, L1) — add it to a running theorist schedule that already contains Barthes (semiotics), Propp, Todorov (narrative), Hall (representation and reception), and Mulvey (male gaze). Assign each theorist a review date: the day you cover them, then day 3, day 7 and day 14. On each review, write the theorist’s name, their central argument in one sentence, and one applied example. By the time you reach the synoptic essay, every theorist should have been revisited at least four times — application under exam pressure only works when recall is automatic."
    ),
    "interleaving": (
        # Example 1 — Mix framework-area questions inside one session
        "Once you have covered all four framework areas — Media Language, Media Representations, Media Industries, and Media Audiences — build a mixed question set using one question from each unit. For example: (1) Explain how Todorov’s narrative theory applies to a news broadcast (Media Language); (2) Explain how Stuart Hall’s male gaze concept operates in a magazine advertisement (Media Representations); (3) Explain the difference between vertical and horizontal integration using a media conglomerate you have studied (Media Industries); (4) Explain one reason why Uses and Gratifications theory presents audiences as active rather than passive (Media Audiences). Attempt without labelling which framework area each question belongs to — identifying the framework IS the skill the synoptic question tests.",
        # Example 2 — Mix short-form question types
        "Build a mixed set alternating between 1-mark Identify questions and 4-mark Explain questions drawn from across all four units. For example: ‘Identify one technical code used in film trailers’ (1 mark) immediately followed by ‘Explain how audience categorisation by demographic group helps a media organisation target its advertising’ (4 marks). The shift in cognitive demand — from factual recall to explanation of meaning — mirrors exactly what happens inside a real exam paper, where mark allocations jump without warning. Students who only practise blocked by question type are poorly prepared for this rhythm."
    ),
    "dual-coding": (
        # Example 1 — Theorist comparison table
        "After covering the representation unit, draw a three-column comparison table — Theorist / Central Argument / Applied Example — for Hall (encoding/decoding, three reading positions), Mulvey (male gaze, scopophilia, objectification), Gerbner (cultivation theory, mainstreaming) and Bandura (social learning, modelling). Keep each cell to a single phrase or a drawn arrow, never a sentence. Draw a red arrow between Hall’s preferred reading and Gerbner’s dominant ideology to show the conceptual link. A week later, reproduce the table from memory on a blank page and compare. The act of drawing the connections — not just listing the theorists — is where exam-ready understanding forms.",
        # Example 2 — Ownership structure flowchart
        "For Ownership: Conglomerates, Mergers and Integration (Media Industries, L1), draw a two-level flowchart showing horizontal integration (arrows pointing inward to a single company from competing firms at the same level) and vertical integration (arrows pointing upward through production, distribution and exhibition). Label each arrow with one real-world example — for instance a streaming platform acquiring a production studio for vertical integration. Add a sticky note at the bottom: ‘synergy = 1 + 1 > 2’ as the one-word pay-off of integration. Redraw from memory three days later, adding any labels you missed."
    ),
    "elaborative-interrogation": (
        # Example 1 — Why does selection construct reality?
        "Take the concept from Selection, Combination and the Construction of Reality (Media Language, L2): ‘producers select, combine and exclude elements of media language to construct points of view.’ Ask: why does selection construct reality rather than simply report it? (Because every choice to include one image, word or camera angle necessarily excludes alternatives — so the product cannot be a neutral window on the world.) How does this connect to encoding in Stuart Hall’s model? (The producer’s selection is the encoding stage; the choices embed a preferred meaning before any audience sees the text.) Now ask why this matters for a representation question: how does selective framing produce a biased or stereotyped view of a social group? Build the chain until you can answer a 6-mark Explain with Example from this single starting fact.",
        # Example 2 — Why does convergence change industry power?
        "Take the fact from Convergence and the Cross-Platform Media Landscape (Media Industries, L3): ‘content, network and platform providers have converged.’ Ask: why has convergence happened? (Digital technology removed the technical barriers between previously separate industries — the same fibre network can deliver television, telephone and internet.) How does this shift power toward platform owners? (Whoever owns the delivery mechanism can prioritise their own content, bundle subscriptions, and harvest audience data — the ‘vertical stack.’) Push further: why does this make independent producers more vulnerable than before convergence? This chain of reasoning produces the analytical depth that separates a 6-mark Explain from an 8-mark Analyse answer."
    ),
    "knowledge-organisers": (
        # Example 1 — One organiser per framework area
        "Build a single-sided A4 organiser for the Media Representations unit. Divide it into four sections: (1) Key Vocabulary (re-presentation, mediation, stereotype, counter-type, misrepresentation, symbolic annihilation — one-line definitions only); (2) Named Theorists (Hall, Mulvey, Gerbner, Butler — name plus one-phrase argument); (3) Applied Examples (three generic product types where representation operates: a tabloid front page, a pop music video, a TV drama); (4) Common Misconceptions (all stereotypes are negative; Hall’s three readings are binary; Mulvey applies only to film). Draw a small two-arrow diagram in the top-right corner showing the encoding–decoding loop. Redraw from memory every Sunday for four weeks.",
        # Example 2 — Industries quick-reference page
        "For the Media Industries unit, build a one-page organiser with five sections: (1) Ownership patterns (conglomerate, vertical integration, horizontal integration — with one company name each); (2) Funding models (public service broadcasting, advertising revenue, subscription, freemium — with one UK example each); (3) Regulators (OFCOM, IPSO, BBFC, ASA, PEGI — remit in four words each); (4) Key concepts (synergy, convergence, globalisation — one sentence each); (5) Misconceptions box (‘OFCOM does NOT regulate the press — that is IPSO’; ‘the BBC is publicly funded, not government-controlled’). Carry this page to every revision session and redraw it in full once a week in the final month."
    ),
    "timed-practice": (
        # Example 1 — 8-mark Analyse question under time
        "Pull an 8-mark Analyse with Reference question, set a 10-minute timer, and write by hand. The exam rewards sustained analysis of one or two media products over surface-level mention of many. Before the timer starts, write one sentence naming the product and the framework area you will use. During the 10 minutes, develop two analytical points using the PEEL structure: Point, Evidence (a specific element from the product), Explanation of how meaning is constructed, Link to a named theory. After the timer, check: did you use framework terminology in every paragraph, or drift into describing the product’s plot? Mark harshly — description earns the bottom band.",
        # Example 2 — Full unseen-source analysis (first written paper skills)
        "Six weeks before exams, find a print media source — a front page, an advertisement, or a magazine cover — you have never studied before. Set a timer matching the actual allocation for the unseen question and analyse it using the media language framework: identify the technical, symbolic and verbal codes operating; explain the connotations of each; link to at least one named theory. Stop when the timer runs out even if unfinished. The marking bar for the unseen source is: students must analyse codes, not describe content. If your draft contains more description than analysis, rework one paragraph under a second timed session the same day."
    ),
    "theory-application-drills": (
        # Example 1 — Theorist + product + because-chain
        "After studying any lesson in the Media Representations unit, practise a Theory Application Drill: write the theorist’s name, state their central argument in one sentence, name a specific media product type, then write a ‘because… because…’ chain of at least three links explaining why the theory applies. For example: Hall’s reception theory argues that audiences decode media texts from three positions. A tabloid front page about immigration invites a preferred reading that migrants are a threat — because the producer has selected emotive language and images that encode anxiety — because this encoding reflects the outlet’s dominant ideology — because dominant ideology shapes which meanings are ‘common sense’ and which require effort to resist. Students who name the theory without this chain earn AO1 only; the chain is what earns AO2.",
        # Example 2 — Synoptic cross-area drill
        "For the highest-mark synoptic essay question, practise connecting at least two framework areas in a single drill. Choose a media product type (a social media influencer video, for example). Write: (1) one sentence naming the media language codes used; (2) one sentence explaining the representation constructed by those codes (who is presented, and how); (3) one sentence connecting that representation to the industrial context (who funds and distributes the product and what commercial interests shape the representation); (4) one sentence linking to audience theory (what reading positions are invited and why). Students who answer the synoptic question drawing on only one framework area cannot reach the top band. This drill makes the four-way connection automatic before exam day."
    ),
}

# -------- Other-techniques sidebar link map --------

TECHNIQUE_ORDER = [
    ("retrieval-practice", "Retrieval Practice"),
    ("spaced-repetition", "Spaced Repetition"),
    ("interleaving", "Interleaving"),
    ("dual-coding", "Dual Coding"),
    ("elaborative-interrogation", "Elaborative Interrogation"),
    ("knowledge-organisers", "Knowledge Organisers"),
    ("timed-practice", "Timed Practice"),
    ("theory-application-drills", "Theory Application Drills"),
]

OPTIONAL_CARD = """<a class="guide-question-card" href="/guide/media-studies-aqa/revision-technique/theory-application-drills">
<span class="guide-question-marks">Theory application</span>
<h3>Theory Application Drills</h3>
<p>Practise linking a named theorist to a worked product example, then build a “because… because…” chain. Directly mirrors the synoptic essay format.</p>
</a>"""

THEORY_APPLICATION_HTML = """<main class="lesson-content">
<div class="lesson-header">
<span class="guide-marks-badge">Theory application</span>
<h1>Theory Application Drills</h1>
<p class="guide-used-in">Name the theory, pick a product, build the chain &mdash; that&rsquo;s what the high-mark questions reward.</p>
</div>

<div class="guide-section">
<h2>Why Media Studies Needs This</h2>
<p>Media Studies has a specific exam problem: students learn theories (Hall, Mulvey, Propp, Todorov, Blumler and Katz, Gerbner, Bandura, Jenkins) and then deploy them in two very different ways. The lower-band approach is to name the theorist and summarise their argument — this earns AO1 knowledge marks and then stops. The higher-band approach is to take the theory into a specific product, explain how the theory operates in that product, and chain the reasoning outward until the explanation is genuinely analytical. The gap between these two approaches is not about knowing more theory. It is about practising the application move itself until it is automatic.</p>
<h3>What the Exam Rewards</h3>
<table class="guide-levels">
<thead><tr><th>Response type</th><th>What it earns</th><th>What&rsquo;s missing</th></tr></thead>
<tbody>
<tr><td><strong>Theory summary only</strong></td><td>AO1 knowledge marks</td><td>No application &mdash; ceils the answer in the lower band</td></tr>
<tr><td><strong>Theory + product named</strong></td><td>AO1 + partial AO2</td><td>Application is asserted, not reasoned</td></tr>
<tr><td><strong>Theory + product + because-chain</strong></td><td>Full AO2 analysis marks</td><td>Nothing &mdash; this is the top-band move</td></tr>
<tr><td><strong>Cross-area theory links (synoptic)</strong></td><td>Top-band synoptic marks</td><td>Requires connecting two or more framework areas</td></tr>
</tbody>
</table>
</div>

<div class="guide-section">
<h2>Step-by-Step Method</h2>
<ol class="guide-steps">
<li class="guide-step"><span class="guide-step-number">1</span><div class="guide-step-body"><strong>Choose one theorist</strong> &mdash; pick any named theorist from your lessons. Write their name and their central argument in one sentence maximum.</div></li>
<li class="guide-step"><span class="guide-step-number">2</span><div class="guide-step-body"><strong>Pick a generic media product type</strong> &mdash; a broadsheet front page, a pop music video, a streaming teen drama, a social media campaign. Not a named Close Study Product &mdash; a category. The exam tests your ability to apply a theory, not recall a specific product.</div></li>
<li class="guide-step"><span class="guide-step-number">3</span><div class="guide-step-body"><strong>Write the application sentence</strong> &mdash; one sentence stating how the theory operates in that product type. Name a specific element: a camera angle, a headline choice, a casting decision, a funding model.</div></li>
<li class="guide-step"><span class="guide-step-number">4</span><div class="guide-step-body"><strong>Add the first &ldquo;because&rdquo;</strong> &mdash; why does that element support your application? This is your evidence-to-theory link. Write it as &ldquo;because [reason connecting the element to the theoretical concept].&rdquo;</div></li>
<li class="guide-step"><span class="guide-step-number">5</span><div class="guide-step-body"><strong>Add the second &ldquo;because&rdquo;</strong> &mdash; push one level deeper. Why is that first reason true? This is where the analytical chain forms. Two &ldquo;because&rdquo; links is the minimum for a developed AO2 paragraph.</div></li>
<li class="guide-step"><span class="guide-step-number">6</span><div class="guide-step-body"><strong>For synoptic practice, add a cross-area link</strong> &mdash; what does this theory application tell you about a different framework area? (e.g. a media language choice that reflects an industry funding model; an audience reading that challenges a representation.)</div></li>
</ol>
</div>

<div class="collapsible">
<button aria-expanded="false" class="collapsible-toggle"><span>Media Studies Examples</span><svg class="collapsible-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="collapsible-content"><div class="collapsible-inner">
<div class="guide-template">
<div class="guide-template-label">Example 1</div>
<p>After studying any lesson in the Media Representations unit, practise a Theory Application Drill: write the theorist&rsquo;s name, state their central argument in one sentence, name a specific media product type, then write a &ldquo;because&hellip; because&hellip;&rdquo; chain of at least three links explaining why the theory applies. For example: Hall&rsquo;s reception theory argues that audiences decode media texts from three positions. A tabloid front page about immigration invites a preferred reading that migrants are a threat &mdash; because the producer has selected emotive language and images that encode anxiety &mdash; because this encoding reflects the outlet&rsquo;s dominant ideology &mdash; because dominant ideology shapes which meanings are &ldquo;common sense&rdquo; and which require effort to resist. Students who name the theory without this chain earn AO1 only; the chain is what earns AO2.</p>
</div>
<div class="guide-template">
<div class="guide-template-label">Example 2</div>
<p>For the highest-mark synoptic essay question, practise connecting at least two framework areas in a single drill. Choose a media product type (a social media influencer video, for example). Write: (1) one sentence naming the media language codes used; (2) one sentence explaining the representation constructed by those codes (who is presented, and how); (3) one sentence connecting that representation to the industrial context (who funds and distributes the product and what commercial interests shape the representation); (4) one sentence linking to audience theory (what reading positions are invited and why). Students who answer the synoptic question drawing on only one framework area cannot reach the top band. This drill makes the four-way connection automatic before exam day.</p>
</div>
</div></div>
</div>

<div class="guide-section">
<h2>Common Pitfalls</h2>
<ul class="guide-mistakes">
<li><strong>Theory summary instead of application.</strong> &ldquo;Todorov said equilibrium disruption resolution&rdquo; is a summary. &ldquo;The opening two minutes of a typical streaming thriller establishes equilibrium through low-angle domestic framing &mdash; because that framing encodes ordinary safety &mdash; because it sets up the disruption as a violation of familiar space&rdquo; is an application.</li>
<li><strong>One &ldquo;because&rdquo; and stopping.</strong> A single link from theory to product produces a basic AO2 paragraph. Two or three &ldquo;because&rdquo; links produce the sustained analytical chain the mark scheme rewards at the top band.</li>
<li><strong>Applying the wrong theory to the question&rsquo;s framework area.</strong> If the question is tagged to Media Industries, applying Hall&rsquo;s representation theory without anchoring it to an industrial context loses marks. Always identify which framework area the question is testing before choosing your theory.</li>
<li><strong>Listing multiple theories in one answer.</strong> Higher-band answers pick the most appropriate theory and sustain it. Shopping-list answers (Hall, then Mulvey, then Bandura in successive sentences) produce breadth without depth and stall in the middle band.</li>
</ul>
</div>

<div class="guide-section">
<h2>When to Use This</h2>
<p>Start Theory Application Drills as soon as you have covered two or three theorists &mdash; typically midway through Year 10. Aim for one drill per theorist per week during the main revision period. In the final four weeks before exams, focus drills on synoptic four-area chains, since those are the highest-mark questions on both written papers. The Knowledge Check and Flashcard tools in each StudyVault lesson give you the raw recall; this technique turns that recall into exam-ready analysis.</p>
</div>
</main>

<aside class="lesson-sidebar">
<div class="sidebar-section guide-quick-ref">
<div class="sidebar-section-title">Quick Reference</div>
<div class="guide-quick-ref-bar">
<span style="background: #16a34a; width: 20%;" title="Name theorist"></span>
<span style="background: #22c55e; width: 35%;" title="Apply to product"></span>
<span style="background: #4ade80; width: 30%;" title="Build because-chain"></span>
<span style="background: #86efac; width: 15%;" title="Add cross-area link"></span>
</div>
<span class="guide-quick-ref-total">~15 minutes per drill</span>
<h4>The drill</h4>
<ol class="guide-quick-ref-steps">
<li>Name theorist &amp; argument</li>
<li>Pick a product type</li>
<li>Write application sentence</li>
<li>First &ldquo;because&rdquo;</li>
<li>Second &ldquo;because&rdquo;</li>
<li>Cross-area link (synoptic)</li>
</ol>
</div>
<div class="sidebar-section">
<div class="sidebar-section-title">Video</div>
<div class="guide-video-placeholder"><svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon fill="currentColor" points="10 8 16 12 10 16 10 8" stroke="none"/></svg><span>Video walkthrough coming soon</span></div>
</div>
<div class="sidebar-section sidebar-media">
<div class="sidebar-collapsible">
<button class="sidebar-collapsible-toggle" aria-expanded="false"><span>&#128218; Other Techniques</span><svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
<div class="sidebar-collapsible-content">{{OTHER_TECHNIQUES_LINKS}}</div>
</div>
</div>
</aside>"""

def other_links_for(current_slug):
    parts = []
    for slug, name in TECHNIQUE_ORDER:
        if slug == current_slug:
            continue
        parts.append(
            f'<a href="/guide/{SUBJECT_SLUG}/revision-technique/{slug}" class="sidebar-media-item"><strong>{name}</strong></a>'
        )
    return "\n".join(parts)

HUB_INTRO = (
    "Evidence-based revision strategies from cognitive science, tailored to GCSE Media Studies. "
    "Each technique is backed by peer-reviewed research and shown in action with Media Studies examples "
    "drawn from the four framework areas: Media Language, Representations, Industries and Audiences."
)

def load_template(filename):
    path = os.path.join(TEMPLATE_DIR, filename)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()

def fill_technique(filename, slug):
    html = load_template(filename)
    ex1, ex2 = EXAMPLES[slug]
    html = html.replace("{{SUBJECT_NAME}}", SUBJECT_NAME)
    html = html.replace("{{SUBJECT_SLUG}}", SUBJECT_SLUG)
    html = html.replace("{{SUBJECT_EXAMPLE_1}}", ex1)
    html = html.replace("{{SUBJECT_EXAMPLE_2}}", ex2)
    html = html.replace("{{OTHER_TECHNIQUES_LINKS}}", other_links_for(slug))
    return html

def fill_hub():
    html = load_template("hub.html")
    html = html.replace("{{SUBJECT_SLUG}}", SUBJECT_SLUG)
    html = html.replace("{{SUBJECT_NAME}}", SUBJECT_NAME)
    html = html.replace("{{HUB_INTRO}}", HUB_INTRO)
    html = html.replace("{{OPTIONAL_SUBJECT_SPECIFIC_CARD}}", OPTIONAL_CARD)
    return html

def fill_theory_application():
    html = THEORY_APPLICATION_HTML
    html = html.replace("{{OTHER_TECHNIQUES_LINKS}}", other_links_for("theory-application-drills"))
    return html

pages = [
    {"slug": "index",                    "title": "Revision Techniques",         "content_html": fill_hub(),                                                     "sort_order": 0},
    {"slug": "retrieval-practice",       "title": "Retrieval Practice",          "content_html": fill_technique("retrieval-practice.html",       "retrieval-practice"),       "sort_order": 1},
    {"slug": "spaced-repetition",        "title": "Spaced Repetition",           "content_html": fill_technique("spaced-repetition.html",        "spaced-repetition"),        "sort_order": 2},
    {"slug": "interleaving",             "title": "Interleaving",                "content_html": fill_technique("interleaving.html",             "interleaving"),             "sort_order": 3},
    {"slug": "dual-coding",              "title": "Dual Coding",                 "content_html": fill_technique("dual-coding.html",              "dual-coding"),              "sort_order": 4},
    {"slug": "elaborative-interrogation","title": "Elaborative Interrogation",   "content_html": fill_technique("elaborative-interrogation.html","elaborative-interrogation"),"sort_order": 5},
    {"slug": "knowledge-organisers",     "title": "Knowledge Organisers",        "content_html": fill_technique("knowledge-organisers.html",     "knowledge-organisers"),     "sort_order": 6},
    {"slug": "timed-practice",           "title": "Timed Practice",              "content_html": fill_technique("timed-practice.html",           "timed-practice"),           "sort_order": 7},
    {"slug": "theory-application-drills","title": "Theory Application Drills",   "content_html": fill_theory_application(),                                       "sort_order": 8},
]

# --- Pre-flight: check no {{PLACEHOLDER}} left ---
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
for p in pages:
    leaks = PLACEHOLDER_RE.findall(p["content_html"])
    if leaks:
        print(f"ABORT - placeholder leak in {p['slug']}: {leaks}")
        sys.exit(1)
print("Pre-flight OK - no placeholder leaks in any of the 9 pages.")

sb = get_client()

inserted, updated = 0, 0
for p in pages:
    existing = (
        sb.table("guide_pages")
        .select("id")
        .eq("subject_id", SUBJECT_ID)
        .eq("guide_type", GUIDE_TYPE)
        .eq("slug", p["slug"])
        .execute()
        .data
    )
    if existing:
        sb.table("guide_pages").update({
            "title": p["title"],
            "content_html": p["content_html"],
            "sort_order": p["sort_order"],
        }).eq("id", existing[0]["id"]).execute()
        updated += 1
        print(f"  updated  {p['slug']}  (sort_order={p['sort_order']})")
    else:
        sb.table("guide_pages").insert({
            "subject_id": SUBJECT_ID,
            "guide_type": GUIDE_TYPE,
            "slug": p["slug"],
            "title": p["title"],
            "content_html": p["content_html"],
            "sort_order": p["sort_order"],
        }).execute()
        inserted += 1
        print(f"  inserted {p['slug']}  (sort_order={p['sort_order']})")

print(f"\nDone. inserted={inserted}, updated={updated}, total={inserted+updated}")

# --- Verify: query back and confirm content has no placeholder leaks ---
print("\nVerification query...")
rows = (
    sb.table("guide_pages")
    .select("slug,title,sort_order,content_html")
    .eq("subject_id", SUBJECT_ID)
    .eq("guide_type", GUIDE_TYPE)
    .order("sort_order")
    .execute()
    .data
)
print(f"  rows returned: {len(rows)}")
for r in rows:
    leaks = PLACEHOLDER_RE.findall(r["content_html"] or "")
    status = "OK" if not leaks else f"LEAK: {leaks}"
    print(f"  [{r['sort_order']}] {r['slug']:<30} {r['title']:<30} len={len(r['content_html'] or ''):>5}  {status}")
