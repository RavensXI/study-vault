"""Insert/update revision-technique guide pages for Information Technology (OCR J836 — it-ocr).

Subject: IT in the Digital World (R050 — external exam only, 8 lessons).
NEA units R060 and R070 removed 2026-05-09; all examples reference the 8
remaining lessons only. No optional 8th technique — Walk the Process was
anchored to the NEA spreadsheet/AR units which no longer exist.

8 rows total: 1 hub (sort_order 0) + 7 canonical techniques (sort_order 1..7).
"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
from lib.supabase_client import get_client

SUBJECT_ID = "ccb8b884-4c48-41cc-a356-fe95e60b396d"
SUBJECT_SLUG = "it-ocr"
SUBJECT_NAME = "Information Technology"
GUIDE_TYPE = "revision-technique"
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "REVISION_TECHNIQUES")

# -------- Examples per technique (IT in the Digital World — 8 lessons only) --------

EXAMPLES = {
    "retrieval-practice": (
        # Example 1 — Cyber-security threat lists (Lesson 5)
        "After studying <strong>Cyber-security: Threats &amp; Impacts</strong> (L5), close the lesson and brain-dump "
        "every named threat: Denial of Service, the seven malware types (adware, botnet, ransomware, spyware, "
        "Trojan horse, virus, worm), and all six social engineering methods (baiting, phishing, pretexting, "
        "quid pro quo, scareware, shoulder surfing). Then write one sentence on HOW each threat works. "
        "Check against the lesson, mark what you missed in red, and retest the gaps the next day. "
        "This is the densest content block in the whole qualification — build the recall first, then the definitions.",

        # Example 2 — Validation vs verification tools (Lesson 3)
        "After covering <strong>Information, Data Types &amp; Validation</strong> (L3), shut the tab and list "
        "every validation tool OCR names (data type check, format check, input mask, length check, limited choice "
        "/ drop-down list / radio buttons / tick list, lookup, presence check, range check) plus the two "
        "verification tools (double entry, manual checking). For each one, write a one-line description of what "
        "it checks and whether it is validation or verification. This distinction is a classic 2-mark question "
        "&mdash; brain-dumping both lists together forces you to notice the difference, not just memorise words."
    ),
    "spaced-repetition": (
        # Example 1 — IoE four pillars (Lesson 8)
        "The day you study <strong>The Internet of Everything</strong> (L8), write out the four pillars "
        "(people, process, data, things) and one real-world example for each (e.g. a paramedic with a tablet "
        "= people; the ambulance dispatch workflow = process; the patient&rsquo;s biometric readings = data; "
        "the heart-rate monitor = things). Retest at 24 hours, 3 days, 7 days, and 14 days &mdash; each time, "
        "add a different application area (smart home, manufacturing, transport) to the same card. "
        "The spec says students should &lsquo;keep up to date with emerging technologies&rsquo; &mdash; spacing "
        "the IoE review while adding examples is the best way to stop this topic feeling abstract on exam day.",

        # Example 2 — Five Acts of legislation (Lesson 6)
        "When you cover <strong>Prevention Measures &amp; IT Legislation</strong> (L6), write one flashcard per Act "
        "(Computer Misuse, Copyright Designs and Patents, Data Protection, Freedom of Information, "
        "Health and Safety at Work) &mdash; each card has the Act name on the front and its PURPOSE plus "
        "one implication for organisations on the back. Review at day 1, day 3, day 7, and day 14. "
        "The spec explicitly excludes detailed knowledge of the legislation &mdash; so the card should never "
        "contain section numbers or legal wording. Space the PURPOSE, not the small print."
    ),
    "interleaving": (
        # Example 1 — Validation vs verification vs test data (Lessons 3 and 4)
        "Once you have covered <strong>Information, Data Types &amp; Validation</strong> (L3) and "
        "<strong>Data Collection, Storage &amp; Testing</strong> (L4), build a mixed question set "
        "that pulls validation, verification and test-data questions together without labelling which is which. "
        "A sample set: &lsquo;A user types their password twice &mdash; what technique is this?&rsquo;, "
        "&lsquo;A field rejects the entry 150 when the valid range is 0&ndash;100 &mdash; which test data "
        "type caught this?&rsquo;, &lsquo;A drop-down list stops a user entering text in a numeric field "
        "&mdash; what validation tool is this?&rsquo;. Marking the topic at the top of each question defeats "
        "the point &mdash; your brain must first identify the concept, then apply it. "
        "This is exactly what the R050 scenario questions demand.",

        # Example 2 — HCI interaction methods vs digital communication channels (Lessons 2 and 7)
        "After covering <strong>Human Computer Interface (HCI) in Everyday Life</strong> (L2) and "
        "<strong>Digital Communications &amp; Distribution</strong> (L7), mix questions from both lessons: "
        "&lsquo;A smart speaker responds to the user&rsquo;s command &mdash; what interaction method is this?&rsquo;, "
        "&lsquo;A business sends a monthly update to staff via email &mdash; which distribution channel?&rsquo;, "
        "&lsquo;Which connectivity type does a smartwatch use to sync with a phone over short range?&rsquo;. "
        "These two lessons share the theme of how people interact with technology &mdash; interleaving them "
        "trains you to identify whether a question is about INPUT (HCI) or OUTPUT (communications), "
        "which is the classification the exam exploits in Section B scenarios."
    ),
    "dual-coding": (
        # Example 1 — HCI application areas hub-and-spoke (Lesson 2)
        "After <strong>Human Computer Interface (HCI) in Everyday Life</strong> (L2), draw a hub-and-spoke "
        "diagram by hand: &lsquo;HCI&rsquo; in the centre circle, six spokes for banking, embedded systems, "
        "entertainment, fitness, home appliances, and retail. On each spoke, write two words for the device "
        "type and two words for the interaction method (e.g. &lsquo;fitness &mdash; wearable &mdash; "
        "touch/voice&rsquo;). Keep labels to 2&ndash;4 words. A week later, redraw the diagram from memory "
        "on a blank page. Any missing spoke is a gap. This technique works especially well for HCI because "
        "the content is about visual interfaces &mdash; encoding it visually reinforces the topic itself.",

        # Example 2 — Cyber-security threat map with impact column (Lessons 5 and 6)
        "Draw a three-column table by hand for <strong>Cyber-security: Threats &amp; Impacts</strong> (L5) "
        "and <strong>Prevention Measures &amp; IT Legislation</strong> (L6). Column 1: threat category "
        "(DoS / hacking / malware / social engineering). Column 2: one sub-type per row with a two-word "
        "definition. Column 3: the matched prevention measure. Keep each cell to four words. "
        "Draw a thick dividing line between physical prevention measures (left box) and logical prevention "
        "measures (right box) at the bottom of the table. A week later, redraw from memory &mdash; any "
        "missing cell is a revision target. Linking threat to countermeasure visually trains the "
        "&lsquo;which prevention measure would mitigate this threat?&rsquo; question type."
    ),
    "elaborative-interrogation": (
        # Example 1 — Why does HCI differ across contexts? (Lesson 2)
        "From <strong>Human Computer Interface (HCI) in Everyday Life</strong> (L2), take the fact that "
        "a banking ATM uses a keypad and limited-choice screen buttons. Ask: why? "
        "(Security &mdash; physical buttons confirm intent and reduce accidental taps; "
        "a keypad is harder for shoulder surfers to read than a touchscreen grid.) "
        "How does that differ from a fitness tracker HCI? "
        "(Tiny screen, gesture-based, no keyboard &mdash; designed for one-handed glances during exercise.) "
        "Why does hardware constrain the software choice? "
        "(Processing power and display size limit which OS and input method can run.) "
        "Push the chain to three &lsquo;why&rsquo;s and you have built the evaluative answer "
        "the exam expects for a &lsquo;Discuss the suitability of&rsquo; question.",

        # Example 2 — Why validate AND verify? (Lesson 3)
        "Take the fact from <strong>Information, Data Types &amp; Validation</strong> (L3) that data entry "
        "systems use both validation and verification. Ask: why isn&rsquo;t validation alone enough? "
        "(A date of birth could pass a format check and a range check but still be wrong if the clerk "
        "typed the year incorrectly.) How does double-entry verification catch that? "
        "(The second entry is compared character-by-character; a mismatch triggers a warning.) "
        "Why does the spec separate them as distinct tools? "
        "(They target different failure modes: validation catches unreasonable data, verification catches "
        "transcription errors.) Reasoning through this chain means you can write a correct &lsquo;Explain&rsquo; "
        "answer without memorising the difference &mdash; you understand it."
    ),
    "knowledge-organisers": (
        # Example 1 — Cyber-security one-pager (Lessons 5 and 6)
        "Make a single A4 page for the cyber-security section covering both "
        "<strong>Cyber-security: Threats &amp; Impacts</strong> (L5) and "
        "<strong>Prevention Measures &amp; IT Legislation</strong> (L6). "
        "Divide the page into four sections: "
        "(1) Threats &mdash; three columns for DoS/hacking, malware, social engineering with one-word "
        "definitions per sub-type; "
        "(2) Impacts &mdash; a 6-box grid (data destruction, data manipulation, data modification, "
        "data theft in transit/at rest, denial of service, identity theft) with one-line consequences; "
        "(3) Prevention Measures &mdash; two columns for physical vs logical, each with bullet terms only; "
        "(4) Legislation &mdash; five rows, one per Act, showing name and purpose only (no section numbers). "
        "The misconception box at the bottom: &lsquo;hacking and malware are SEPARATE threats &mdash; "
        "a hacker may USE malware, but they are not the same thing.&rsquo; Redraw from memory every Sunday.",

        # Example 2 — IoE applications grid (Lesson 8)
        "Make a one-page organiser for <strong>The Internet of Everything</strong> (L8). "
        "Top section: a 2&times;2 box for the four pillars (people, process, data, things) with one example "
        "in each cell. Middle section: a 7-row application grid (energy management, health, manufacturing, "
        "military/emergency services, smart devices, transport, security) &mdash; each row gets a 2-word "
        "&lsquo;how IoE helps&rsquo; label. "
        "Bottom section: a small Venn diagram showing IoT (things only) inside IoE (all four pillars) "
        "&mdash; this single visual kills the IoT/IoE misconception. "
        "A common 4-mark exam question is &lsquo;Name the four pillars of IoE and give one example of each&rsquo; "
        "&mdash; this organiser gives you the exact structure to answer it in four minutes."
    ),
    "timed-practice": (
        # Example 1 — The 8-mark hand-sketch question (R050 Section B)
        "Pull a past or specimen R050 Section B scenario and find the 8-mark &lsquo;Create a design "
        "document&rsquo; question (e.g. &lsquo;Sketch a mind map to plan a website for a small "
        "business&rsquo;). Set a timer for 10 minutes and draw it by hand &mdash; labels required. "
        "The assessment guidance is explicit: marks reward labelling, completeness and a visible link "
        "to the scenario. After the timer, check: did you use the business context from the scenario "
        "in at least three labels? Did every branch have a label (not just a box)? "
        "Marks are lost by students who draw a generic mind map with no scenario content. "
        "One timed attempt per week from 10 weeks out, each on a different design tool "
        "(mind map, flowchart, visualisation diagram, wireframe) from "
        "<strong>Design Tools for IT Solutions</strong> (L1) until all four feel automatic.",

        # Example 2 — Full R050 paper under exam conditions (1 hr 30 min, 70 marks)
        "Six weeks before your exam, simulate the full R050 paper: 1 hour 30 minutes, 70 marks, "
        "handwritten, no notes, phone in another room. "
        "Section A is 15 marks of closed response, MCQ and short-answer &mdash; target 15 minutes "
        "and attempt every item. "
        "Section B is 55 marks of one continuous scenario &mdash; read the scenario first, "
        "highlight the business type, the named technology constraints and the stated user needs "
        "BEFORE writing answer 1. "
        "Check your pacing after: the 9-mark extended response (levels of response) needs at "
        "least 12 minutes &mdash; if you spent 8 minutes on a 3-mark Explain in Section B, you ran over. "
        "Mark Section A with the scheme and Section B using the levels descriptors. "
        "Note where you lost marks: was it missing command-word depth "
        "(explain without &lsquo;because / therefore&rsquo;) or missing scenario application?"
    ),
}

# -------- Other-techniques sidebar link map --------

TECHNIQUE_ORDER = [
    ("retrieval-practice",        "Retrieval Practice"),
    ("spaced-repetition",         "Spaced Repetition"),
    ("interleaving",              "Interleaving"),
    ("dual-coding",               "Dual Coding"),
    ("elaborative-interrogation", "Elaborative Interrogation"),
    ("knowledge-organisers",      "Knowledge Organisers"),
    ("timed-practice",            "Timed Practice"),
]

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
    "Evidence-based revision strategies from cognitive science, tailored to Information Technology. "
    "Each technique is backed by peer-reviewed research and shown in action with a real example "
    "from IT in the Digital World."
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
    html = html.replace("{{OPTIONAL_SUBJECT_SPECIFIC_CARD}}", "")
    return html

pages = [
    {"slug": "index",                     "title": "Revision Techniques",       "content_html": fill_hub(),                                               "sort_order": 0},
    {"slug": "retrieval-practice",        "title": "Retrieval Practice",        "content_html": fill_technique("retrieval-practice.html",        "retrieval-practice"),        "sort_order": 1},
    {"slug": "spaced-repetition",         "title": "Spaced Repetition",         "content_html": fill_technique("spaced-repetition.html",         "spaced-repetition"),         "sort_order": 2},
    {"slug": "interleaving",              "title": "Interleaving",              "content_html": fill_technique("interleaving.html",              "interleaving"),              "sort_order": 3},
    {"slug": "dual-coding",               "title": "Dual Coding",               "content_html": fill_technique("dual-coding.html",               "dual-coding"),               "sort_order": 4},
    {"slug": "elaborative-interrogation", "title": "Elaborative Interrogation", "content_html": fill_technique("elaborative-interrogation.html", "elaborative-interrogation"), "sort_order": 5},
    {"slug": "knowledge-organisers",      "title": "Knowledge Organisers",      "content_html": fill_technique("knowledge-organisers.html",      "knowledge-organisers"),      "sort_order": 6},
    {"slug": "timed-practice",            "title": "Timed Practice",            "content_html": fill_technique("timed-practice.html",            "timed-practice"),            "sort_order": 7},
]

# --- Pre-flight: check no {{PLACEHOLDER}} left ---
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
for p in pages:
    leaks = PLACEHOLDER_RE.findall(p["content_html"])
    if leaks:
        print(f"ABORT - placeholder leak in {p['slug']}: {leaks}")
        sys.exit(1)
print("Pre-flight OK - no placeholder leaks in any of the 8 pages.")

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
        print(f"  updated  {p['slug']:<32} (sort_order={p['sort_order']})")
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
        print(f"  inserted {p['slug']:<32} (sort_order={p['sort_order']})")

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
    print(f"  [{r['sort_order']}] {r['slug']:<32} {r['title']:<30} len={len(r['content_html'] or ''):>5}  {status}")

# --- Rationale: no optional 8th technique ---
# Walk the Process was anchored to NEA units (R060 spreadsheets, R070 AR)
# which were removed 2026-05-09. Neither "Tracing Through Data" nor
# "Mapping Threats and Mitigations" adds real value over the canonical 7
# for a single 8-lesson exam unit. The spec's densest content is already
# well served by Retrieval Practice, Spaced Repetition, and Knowledge
# Organisers. Adding an 8th would be padding, not signal.
