"""Insert/update revision-technique guide pages for AQA Psychology (8182)."""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
from lib.supabase_client import get_client

SUBJECT_ID = "fd19191e-255b-448e-82f1-b0cb15d80561"
SUBJECT_SLUG = "psychology-aqa"
SUBJECT_NAME = "Psychology"
GUIDE_TYPE = "revision-technique"
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "REVISION_TECHNIQUES")

# -------- Examples per technique (AQA Psychology 8182) --------

EXAMPLES = {
    "retrieval-practice": (
        # Example 1 — Core study brain dump
        "After studying Conformity and Asch's Study (Social Influence, L1), close the tab and write down the aim, procedure, key findings and conclusions of Asch's line-judgement study from memory. Include the headline figures: 75% of participants conformed at least once on the unambiguous trials, and the average conformity rate across critical trials was around 33%. Then list the three variables Asch later manipulated (group size, unanimity, task difficulty) and what each did to the conformity rate. Compare to the lesson, highlight the gaps in a different colour, and retest only the missed items the next day. Examiners reward students who quote precise figures rather than vague language like \"most people conformed.\"",
        # Example 2 — Multi-store model recall
        "After studying The Multi-Store Model of Memory (Memory, L2), shut the tab and sketch the Atkinson and Shiffrin diagram from memory: sensory register, short-term memory, long-term memory, plus the arrows for attention, rehearsal and retrieval. Annotate each store with its three properties — capacity, duration and coding. Then write out the supporting evidence (Murdock's serial position curve, the case of HM/Clive Wearing, the duration studies). The diagram and the supporting evidence together carry the marks on a six-mark Describe and Evaluate question. Retest tomorrow before moving on; recall accuracy on the diagram is the foundation for every evaluation point that follows."
    ),
    "spaced-repetition": (
        # Example 1 — Core studies running schedule
        "On the day you cover each core study — Asch, Milgram, Piliavin, Murdock, Bartlett, Bruner and Minturn, Gilchrist and Nesberg, Piaget, McGarrigle and Donaldson, Hughes, Von Frisch — add it to a running schedule with review dates at day 1, day 3, day 7, day 14 and day 30. On each review, write the aim, procedure, findings and one strength and one weakness in four short bullets. By exam day each of the named studies should have been revisited at least four times. Students who try to learn all studies in the final fortnight reliably confuse the procedures of Asch and Milgram or attribute Murdock's serial position finding to Bartlett — spacing prevents these mark-affecting mix-ups.",
        # Example 2 — Theories across units
        "When you reach Piaget's Theory of Cognitive Development (Development, L2), add it to a theorist review log that already contains the multi-store model (Memory), Gibson's direct theory and Gregory's constructivist theory (Perception), and the social learning explanation of obedience (Social Influence). Schedule each theorist for review at day 1, day 3, day 7 and day 14. On every review, write the theorist's name, the core claim in one sentence, one piece of supporting evidence, and one criticism. Theory comparison questions (\"compare Gibson and Gregory\") are predictable on the exam; the only way to handle them under pressure is to have the comparison already rehearsed."
    ),
    "interleaving": (
        # Example 1 — Mixed-topic question set
        "Once you have covered all eight topics, build a mixed question set that pulls one question from each: (1) Describe the procedure of Asch's study (Social Influence); (2) Explain one strength and one weakness of the multi-store model (Memory); (3) Outline Piaget's stage of concrete operations (Development); (4) Explain one ethical issue in psychological research (Research Methods); (5) Describe the function of the autonomic nervous system in fight-or-flight (Brain and Neuropsychology); (6) Explain Gregory's constructivist theory of perception (Perception); (7) Describe two characteristics of clinical depression (Psychological Problems); (8) Explain one difference between human and animal communication (Language, Thought and Communication). Attempt without referring to your notes. Identifying which topic each question belongs to is half the skill the exam tests.",
        # Example 2 — Mix short-form and extended response
        "Build a mixed set alternating between 2-mark Define questions and 6-mark Describe-and-Evaluate questions drawn from across all units. For example: \"Define the term internal validity\" (2 marks) immediately followed by \"Describe and evaluate Milgram's study of obedience\" (6 marks). The shift in cognitive demand — from a tight technical definition to a sustained eight-line answer — mirrors exactly what happens inside a real exam paper. Students who only practise blocked by question length are poorly prepared for this rhythm and run out of time on the longer questions because they over-write the early definitions."
    ),
    "dual-coding": (
        # Example 1 — Multi-store model with arrows
        "After covering the Memory unit, draw the multi-store model as a labelled diagram across an A4 page: three boxes (sensory register, STM, LTM) with arrows for attention (sensory → STM), rehearsal (STM → LTM) and retrieval (LTM → STM). Inside each box write capacity, duration and coding in three short cells. To the side of the diagram, draw Murdock's serial position curve as a small inverted U with two peaks (primacy on the left, recency on the right) and a dip in the middle. Connect the recency peak to the STM box with a red arrow and the primacy peak to the LTM box with a green arrow. Redraw from memory three days later — the act of drawing the connections, not the act of reading them, builds the exam-ready understanding.",
        # Example 2 — Bystander decision flowchart
        "For Bystander Behaviour and Piliavin's Study (Social Influence, L3), draw Latané and Darley's five-stage decision tree as a vertical flowchart: Notice → Interpret as emergency → Take responsibility → Know how to help → Decide to help. Beside each stage write the single factor that can break it: notice (distraction), interpret (pluralistic ignorance), responsibility (diffusion), competence (lack of skill), decide (cost-benefit). Then overlay arrows from Piliavin's findings — the drunk vs ill victim manipulation breaks the cost-benefit stage; the bystander count manipulation breaks the diffusion stage. Redraw the whole flowchart from memory the following week. This single diagram answers every 6-mark question on bystander behaviour."
    ),
    "elaborative-interrogation": (
        # Example 1 — Why does the central executive matter?
        "Take the concept from The Multi-Store Model of Memory (Memory, L2): \"information must be rehearsed in STM before it transfers to LTM.\" Ask: why does rehearsal matter? (Because without it, STM information decays within 18-30 seconds, as Peterson and Peterson's trigram study demonstrated.) Why does that decay happen? (Because STM uses acoustic coding and has a limited capacity of 7±2 items — rehearsal is the only way to keep an item active in the loop.) Why is this finding a problem for the multi-store model? (Because patients like KF with damaged STM can still form new long-term memories — showing that the strict rehearsal-then-storage sequence cannot be the whole story.) Build the chain until you can answer a 6-mark Evaluate question from this single starting fact.",
        # Example 2 — Why is obedience higher in uniform?
        "Take the fact from Obedience: Milgram and the Authoritarian Personality (Social Influence, L2): \"obedience rose when the experimenter wore a lab coat.\" Ask: why does a uniform increase obedience? (Because it signals legitimate authority — participants infer expertise and institutional backing from the visual cue alone.) Why does perceived legitimacy override personal ethics? (Because in Milgram's agentic state theory, the participant shifts responsibility for the outcome onto the authority figure — they are acting as the agent of the experimenter, not as an autonomous moral agent.) Why does this matter outside the laboratory? (Because the same mechanism explains compliance with police in everyday life and with military commands in atrocity contexts — Hofling's nurse study and the My Lai massacre both fit the same agentic-state model.) The chain produces the analytical depth that separates a six-mark Evaluate from a four-mark Describe."
    ),
    "knowledge-organisers": (
        # Example 1 — One organiser per topic
        "Build a single-sided A4 organiser for the Memory topic. Divide it into four sections: (1) Key terms (encoding, capacity, duration, episodic, semantic, procedural, retrieval failure, interference, displacement — one-line definitions only); (2) Theories and models (Multi-store model — Atkinson and Shiffrin; Reconstructive memory — Bartlett; Serial position effect — Murdock); (3) Core studies (Murdock's 1962 free-recall study — aim, procedure, findings in three short cells; Bartlett's War of the Ghosts — likewise); (4) Common misconceptions (long-term memory is not infinite; rehearsal is necessary but not sufficient for LTM; reconstructive memory does not mean memory is always wrong). Redraw the organiser from memory every Sunday for four weeks before the exam.",
        # Example 2 — Research Methods quick-reference page
        "For the Research Methods unit, build a one-page organiser with five sections: (1) Hypotheses (null, alternative, directional, non-directional — one sentence each with an example); (2) Variables (IV, DV, control, extraneous, confounding — one-line definitions); (3) Sampling methods (random, opportunity, stratified, volunteer — strengths and weaknesses in two-word labels); (4) Experimental designs (independent groups, repeated measures, matched pairs — one strength and one weakness each); (5) Ethics box (informed consent, deception, right to withdraw, protection from harm, confidentiality, debriefing — six BPS principles named). Research Methods questions appear on every paper and reward precise terminology; this page is the single highest-leverage document in the whole revision file."
    ),
    "timed-practice": (
        # Example 1 — 6-mark Describe and Evaluate under time
        "Pull a 6-mark Describe and Evaluate question — for example, \"Describe and evaluate one study of obedience\" — set a 7-minute timer, and write by hand. The exam rewards balanced description (the aim, procedure and findings) plus genuine evaluation (one strength and one limitation, each with a reason). Before the timer starts, write one sentence naming the study (Milgram, 1963) and the topic. During the 7 minutes, allocate roughly 3 minutes to description and 4 minutes to evaluation. After the timer, check: did you give the headline figure (65% delivered 450 volts)? Did your evaluation include a methodological point (low ecological validity, sample bias) AND an ethical point (deception, lack of right to withdraw)? Description-only answers ceiling at three marks.",
        # Example 2 — Full 9-mark extended response under exam conditions
        "Six weeks before exams, attempt a full 9-mark question — for example, \"Discuss two explanations for clinical depression\" — under exact exam conditions: 12 minutes, by hand, no notes. The 9-mark band requires depth on two named explanations (e.g. cognitive theory — Beck's negative triad — and biological — low serotonin), AT LEAST one strength and one weakness for each, and a brief comparative judgement at the end. Stop when the timer runs out even if unfinished. Mark harshly: if you only covered one explanation in depth, the answer ceilings at 5-6 marks. If you covered both but with no evaluation, the same. The bar for top band is two explanations, two strengths, two weaknesses, and a comparison — practise hitting all five elements inside 12 minutes."
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
    "Evidence-based revision strategies from cognitive science, tailored to GCSE Psychology. "
    "Each technique is backed by peer-reviewed research and shown in action with Psychology examples "
    "drawn from the eight topics: Memory, Perception, Development, Research Methods, Social Influence, "
    "Language Thought and Communication, Brain and Neuropsychology, and Psychological Problems."
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
    {"slug": "index",                    "title": "Revision Techniques",         "content_html": fill_hub(),                                                     "sort_order": 0},
    {"slug": "retrieval-practice",       "title": "Retrieval Practice",          "content_html": fill_technique("retrieval-practice.html",       "retrieval-practice"),       "sort_order": 1},
    {"slug": "spaced-repetition",        "title": "Spaced Repetition",           "content_html": fill_technique("spaced-repetition.html",        "spaced-repetition"),        "sort_order": 2},
    {"slug": "interleaving",             "title": "Interleaving",                "content_html": fill_technique("interleaving.html",             "interleaving"),             "sort_order": 3},
    {"slug": "dual-coding",              "title": "Dual Coding",                 "content_html": fill_technique("dual-coding.html",              "dual-coding"),              "sort_order": 4},
    {"slug": "elaborative-interrogation","title": "Elaborative Interrogation",   "content_html": fill_technique("elaborative-interrogation.html","elaborative-interrogation"),"sort_order": 5},
    {"slug": "knowledge-organisers",     "title": "Knowledge Organisers",        "content_html": fill_technique("knowledge-organisers.html",     "knowledge-organisers"),     "sort_order": 6},
    {"slug": "timed-practice",           "title": "Timed Practice",              "content_html": fill_technique("timed-practice.html",           "timed-practice"),           "sort_order": 7},
]

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
for p in pages:
    leaks = PLACEHOLDER_RE.findall(p["content_html"])
    if leaks:
        print(f"ABORT - placeholder leak in {p['slug']}: {leaks}")
        sys.exit(1)
print(f"Pre-flight OK - no placeholder leaks in any of the {len(pages)} pages.")

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
