"""Render the night's Jev results as one page: scripts/_jev/_results/report.html"""
import io, json, os, collections, statistics, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "_results")
def load(name):
    p = os.path.join(R, name)
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None
def e(s): return H.escape(str(s if s is not None else ""))
def pct(x): return "%d%%" % round(100 * x)

# ---- ledger: cost + latency
rows = []
for l in io.open(os.path.join(HERE, "_ledger.jsonl"), encoding="utf-8", errors="ignore"):
    try: rows.append(json.loads(l))
    except Exception: pass
by = collections.defaultdict(list); tok = collections.defaultdict(int)
for r in rows: by[r["tag"]].append(r["ms"]); tok[r["tag"]] += r["input_tokens"]
total_calls = len(rows); total_usd = sum(tok.values()) / 1e6 * 0.042
allms = sorted(r["ms"] for r in rows); p50 = allms[len(allms) // 2]; p95 = allms[int(len(allms) * 0.95)]

badges = load("badges.json"); badges2 = load("badges2.json"); fc = load("factcheck.json"); dupes = load("dupes.json"); qtype = load("qtype.json")
widgets = load("widgets.json"); safe = load("safeguard.json"); spec = load("speccov.json"); psych = load("speccov_psych.json"); hist = load("speccov_unity_history.json")
tier = load("tier.json"); onboard = load("onboard.json"); kc = load("kc_full.json"); kc6k = load("kc.json"); gaps = load("gap_spotcheck.json"); kcspot = load("kc_spotcheck.json"); desc = load("desc.json"); media = load("media.json")
flash = load("flashgrade.json"); search = load("search.json"); marking = load("marking.json")

def card(title, verdict, what, numbers, caveat, examples=None, build=None):
    cls = {"build": "v-build", "pipeline": "v-pipe", "no": "v-no", "maybe": "v-maybe"}[verdict[0]]
    h = '<section class="exp"><div class="exp-head"><h2>%s</h2><span class="verdict %s">%s</span></div>' % (e(title), cls, e(verdict[1]))
    h += '<p class="what">%s</p>' % what
    if numbers:
        h += '<table class="nums"><tbody>' + "".join('<tr><th>%s</th><td>%s</td></tr>' % (e(k), v) for k, v in numbers) + '</tbody></table>'
    if examples:
        h += '<div class="examples">' + "".join('<p>%s</p>' % x for x in examples) + '</div>'
    h += '<p class="caveat">%s</p>' % caveat
    if build: h += '<p class="build">%s</p>' % build
    return h + '</section>'

parts = []
# ---------------- STRONG: things to build
if flash:
    s = flash["summary"]
    parts.append(card("Typed-recall flashcards", ("build", "Build it"),
        "Today a student flips a card and taps whether they knew it. With Jev judging a typed recall against the card's answer, flashcards become a genuine test, and the retrieval-strength ratings stop depending on honesty.",
        [("Cards tested", s["n"]), ("Exact answers accepted", s["at_0.5"]["verbatim_accepted"]), ("Misspelt or word-dropped answers accepted", s["at_0.5"]["mangled_accepted"]), ("Wrong answers from the same lesson rejected", s["at_0.5"]["wrong_rejected"]), ("Half-answers accepted", s["at_0.5"]["partial_accepted"] + " (it reads them as partial, which is right)")],
        "The few wrong answers it accepted were not really wrong: a hand-warmer as an exothermic example, a description of hardwoods in place of the word. Each judgement costs about a fiftieth of a penny and comes back in under half a second, so it can run on every card, live.",
        [("<b>%s</b> · answer: %s · typed: <i>%s</i> · accepted at %s" % (e(x["q"]), e(x["answer"]), e(x["typed"]), pct(x["p"]))) for x in s["wrong_but_accepted"][:3]],
        "Where it goes: the flashcard modal gets a text box under the question; the completeness score drives the Leitner box instead of the honesty tap."))
if search:
    s = search["summary"]; sty = s["by_style"]
    parts.append(card("“What do you want to revise?”", ("build", "Build it"),
        "A student types a question, a topic, a misspelt word or half a memory, and lands on the right lesson. Two cheap calls: pick the subject, then pick the lesson from that subject's whole list (up to 255 options in one call). Tested on 120 queries an Opus agent wrote against real lessons, from exact to vague to misspelt.",
        [("Subject right (family level)", "%s of %d" % (s["subject_family"], s["queries"])), ("Lesson right, given the subject", pct(s["lesson_given_true_subject"]["top1_rate"]) + " top-1, " + pct(s["lesson_given_true_subject"]["top3_rate"]) + " top-3"), ("End to end", pct(s["lesson_end_to_end"]["top1_rate"]) + " top-1, " + pct(s["lesson_end_to_end"]["top3_rate"]) + " top-3"),
         ("By query style", ", ".join("%s %s" % (k, pct(v["rate"])) for k, v in sorted(sty.items())))],
        "Given the subject it is nearly perfect on every style, misspelt and vague included. The end-to-end figure is lower only because the first step, choosing among 90 board-specific subjects, cannot know whether the student sits AQA or Edexcel History; on the dashboard that is already known, so the first step collapses to the student's own subjects and the end-to-end figure becomes the per-subject one.",
        [("<i>%s</i> → wanted <b>%s</b> (confidence %s)" % (e(m["query"]), e(m["wanted"]), pct(m["conf"]))) for m in s["misses"][:4]],
        "Where it goes: a search box on the dashboard and inside a lesson; the same call powers “revise this” from a photo of a homework question once text is extracted."))
if widgets:
    w = widgets["wired"]; u = widgets["unwired"]
    parts.append(card("Widget matching for the 3-lesson band", ("pipeline", "Use it now"),
        "The queue of 48 clusters waiting for interactives needs each lesson paired with the right widget from the fleet of 91. Jev sees the lesson's title, description and headings and picks from the whole catalogue in one call.",
        [("Wired lessons re-matched", w["wired_checked"]), ("Picked the widget a human wired", pct(w["top1_rate"]) + " top-1, " + pct(w["top3_rate"]) + " top-3"), ("At high confidence", "%s of %d right" % (pct(w["by_confidence"]["high"]["rate"]), w["by_confidence"]["high"]["n"])), ("Unwired lessons scanned", u["unwired_checked"]), ("Confident new pairings found", u["confident_candidates"])],
        "The catalogue is text-only, so it cannot judge whether the widget's data deck fits (portable versus content-bound). That stays a human check, but on a list of 64 instead of 400.",
        [("%s → <b>%s</b> (%s)" % (e(c["key"]), e(c["widget"]), pct(c["conf"]))) for c in u["top_20"][:5]],
        "Where it goes: a match_existing_widgets pass that costs 13p for 400 lessons and hands Tom a ranked list."))
if safe:
    s = safe["summary"]; t5 = s["by_threshold"][1]
    parts.append(card("Safeguarding triage", ("build", "Build it, carefully"),
        "Students type answers a teacher will read, bug reports, and soon free-text requests. A calibrated flag that sends a disclosure to a safeguarding lead the same day, without drowning teachers in exam-stress false alarms. Tested on 50 hand-written messages: 12 disclosures, 12 ambiguous, 26 ordinary.",
        [("Disclosures caught", t5["concerning_caught"]), ("Ordinary messages flagged", t5["benign_flagged"]), ("Ambiguous messages flagged", t5["ambiguous_flagged"]), ("Routing", "every disclosure routed to the safeguarding lead; every ordinary answer to nobody")],
        "Fifty synthetic messages is a pilot, not a validation. It should run silently for a term on real traffic, with a human reading everything it flags, before anyone relies on it. It is a net, not a policy.",
        None, "Where it goes: the practice-answer save, the bug reporter, the teacher's “pupils to talk to” panel."))
if onboard:
    s = onboard["summary"]
    parts.append(card("Sign-up from a pasted description", ("build", "Build it"),
        "“i do triple science with aqa, edexcel maths, english lit and lang aqa, history aqa, french and rs” becomes the whole wizard: every subject family with its board, or not-taken, or board-unknown, in one call.",
        [("Messages", s["messages"]), ("Subject-and-board fields", s["labelled_fields"]), ("Right", pct(s["accuracy"])), ("At high confidence", "%s of %d right" % (pct(s["by_confidence"]["high"]["rate"]), s["by_confidence"]["high"]["n"]))],
        "It follows the words literally: “everything else is aqa i think” made it put Business on AQA, which is what the student said. Low-confidence fields should be asked, not assumed.",
        [("<i>%s</i> → %s" % (e(x["text"]), e(json.dumps(x["wrong"])))) for x in s["wrong_fields"][:2]],
        "Where it goes: one text box at the top of the wizard, above the tick boxes, and the class-code join page for a school's students."))
if dupes:
    s = dupes["summary"]
    parts.append(card("Duplicate and overlapping lessons", ("pipeline", "Use it now"),
        "The Unity retro-check found four Religious Studies lessons that duplicated a neighbour. Jev scored every pair of lessons within each RS unit for overlap, blind to which ones had been archived.",
        [("Lesson pairs scored", s["pairs"]), ("The four archived duplicates", "ranked 1st, 2nd, 3rd and 5th of %d" % s["pairs"]), ("Cost", "under a penny")],
        "The fourth-ranked pair (Families and Gender Roles / Families and Contemporary Family Issues) is a genuine near-duplicate the checkers did not flag, so the one “miss” is arguably a find.",
        [("%s ↔ %s · overlap %.2f of 2" % (e(t["A"]), e(t["B"]), t["overlap"])) for t in s["top"][:5]],
        "Where it goes: a fleet-wide pass over every unit (about 30,000 pairs, roughly £2) producing a short list for Tom."))
if spec:
    s = spec["summary"]; sq = s["sql_strings_random_check"]
    parts.append(card("Specification coverage matrix", ("pipeline", "Use it now"),
        "Every statement of a spec against every lesson of a subject: which lesson covers it, how confidently, and which statements nobody covers. Run on OCR Computer Science (236 statements, 25 lessons) as the test, because we knew where the gap was.",
        [("Statements covered by some lesson", "%d of %d" % (s["covered"], s["statements"])), ("Gaps flagged", s["gaps"]), ("The known 2.2.3 gap", "SQL, string handling and random numbers all mapped to the two lessons built on 18 Sep and nowhere else"),
         ("AQA Psychology (186 statements, 32 lessons)", "%d gaps: four are the maths-skills statements (standard form, significant figures, frequency tables, ratios) and one is Piaget in education" % psych["summary"]["gaps"] if psych else "not run")] + ([("Unity History (AQA 8145, four options)", "%d of %d statements covered, %d gaps" % (hist["summary"]["covered"], hist["summary"]["statements"], hist["summary"]["gaps"]))] if hist else []),
        "It judges coverage from what we give it, and this run gave it only the lesson body and glossary. An Opus reader then read every lesson behind every flagged gap, including practice questions, quizzes and neighbouring lessons: " + (("%s of the History gaps and %s of the Computer Science gaps are real; the rest are taught in a practice question, a quiz, or under another heading next door." % (gaps["summary"]["history_real_gaps"], gaps["summary"]["cs_real_gaps"])) if gaps else "") + " So the matrix is a short list, not a verdict, and the fix is the same one the quiz audit taught: hand the judge everything, not the body alone. Even so, the reader found a live Computer Science lesson (Networks, Topologies and Protocols) whose text stops mid-thought before the four-layer model it promises, which nobody had noticed.",
        ([("<b>Real gap, %s:</b> %s" % ("Unity History" if k == "history" else "OCR Computer Science", e(g["statement"]))) for k in ("history", "computer_science") for g in gaps[k] if g.get("verdict") == "real gap"] if gaps else [("<b>%s</b> %s" % (e(g["code"]), e(g["statement"]))) for g in s["gap_list"][:4]]),
        "Where it goes: a coverage page per subject in the admin area, re-run nightly; the same matrix tells the wizard which lessons belong to which option, and tells a teacher exactly what their class has not yet been taught."))
if media:
    s = media["summary"]
    parts.append(card("Related-media relevance", ("pipeline", "Use it now"),
        "Every related-media link judged against its lesson: is it on topic, is it a whole channel rather than a video, is it pitched above GCSE.",
        [("Items judged", s["items"]), ("Off-topic", pct(s["irrelevant_rate"])), ("Whole-channel or homepage links", pct(s["generic_rate"])), ("Above GCSE level", pct(s["advanced_rate"]))],
        "The off-topic hits look real: AQA Biology notes on an Edexcel lesson, “BBC Sounds” as a link, Mr Bruff fiction videos on a non-fiction lesson. The weekly link audit checks that videos play; this checks that they belong.",
        [("%s/%s/%s · <i>%s</i> · %s" % (e(x["subject"]), e(x["unit"]), x["n"], e(x["item"]), pct(x["p"]))) for x in s["least_relevant"][:4]],
        "Where it goes: a column in the Sunday audit; items under 40% go on the prune list with the dead links."))
if kc:
    s = kc["summary"]; f = s["flags"]
    nt = [r for r in kc["rows"] if r["taught"] < 0.4][:5]
    parts.append(card("Knowledge-check audit", ("pipeline", "Use it now, with the whole lesson"),
        "For each five-question quiz: does the lesson actually teach what the question asks, is the marked answer the best one, is any distractor also right. This one taught me the most about the tool.",
        [("Questions audited (article lessons, full text)", s["questions"]), ("Lesson does not teach it", f.get("not_taught", 0)), ("Marked answer doubtful", f.get("key_doubtful", 0)), ("A second option is also right", f.get("second_right_option", 0)), ("Flag rate", "%.1f%%" % (100 * s["flag_rate"]))],
        "The first run gave each call only the opening 6,000 characters of the lesson and flagged 8% of questions as untaught; an Opus reader then found most of those answers printed further down the page, and the rest were practice sets whose teaching lives outside the lesson text. Given the whole lesson the flag rate fell to half a percent, and the survivors are real: three copies of a placeholder question, a name the lesson never mentions, a term that appears only in the quiz. The lesson is the pattern's, not the model's: retrieve everything, then judge." + ("" if not kcspot else " Opus agreed with %s of the earlier not-taught flags and %s of the second-right-option flags." % (kcspot["summary"]["not_taught_precision"].split(" ")[0], kcspot["summary"]["also_right_precision"])),
        [("<b>%s</b> · %s/%s/%s · taught %s" % (e(r["q"]), e(r["subject"]), e(r["unit"]), r["n"], pct(r["taught"]))) for r in nt],
        "Where it goes: the same pass for every quiz on the site, about £1.50 with full text, feeding a short review list."))
if qtype:
    s = qtype["summary"]
    parts.append(card("Question-type labels", ("pipeline", "Use it now"),
        "The badge on each practice question (“8 marks — Explain”) was written by the content model; the fleet task to relabel the wrong ones has been waiting. Jev classified 1,500 questions from their text alone.",
        [("Agrees with the badge", pct(s["rate"])), ("Confident disagreements", s["confident_disagreements"]), ("Biggest disagreement", "%d questions badged as source or extract analysis that read as plain Explain questions, the closed-book relabel already known about" % s["top_disagreements"][0]["n"])],
        "Agreement is the wrong measure when the badges are what we are checking; the confident disagreements are the worklist, and each needs a glance rather than a rewrite.",
        None, "Where it goes: run over all 27,000 questions (about 70p), review the confident disagreements, done in an afternoon."))
if marking:
    s = marking["summary"]
    parts.append(card("Marking: bands, gates and a live checklist", ("build", "Build the gates and the checklist"),
        "Not feedback: that stays with the big model. Three things around it. Which band is this answer in? Is it off-topic, too short, or a scheme paste, so we do not spend a Bedrock call on it? And, point by point, has the student hit each creditable point yet, a checklist that could tick live while they type. Tested on 40 questions with four answers each, written and marked by an Opus examiner.",
        [("Answers", s["answers"]), ("Band exactly right", pct(s["band_exact"])), ("Band within one", pct(s["band_within_one"])), ("Orders two answers correctly", pct(s["pairwise_order_concordance"]) + " of pairs"), ("Off-topic answers caught", s["off_topic_gate"]["offtopic_caught"]), ("Good answers wrongly flagged", s["off_topic_gate"]["others_flagged"]),
         ("Point checklist", "precision %s, recall %s against the examiner's own list" % (pct(s["point_checklist"]["precision"]), pct(s["point_checklist"]["recall"])))],
        "It ranks answers better than it places them, which is what you would expect from a judge that cannot count marks. As a live checklist and a cheap gate it is ready; as the mark itself it is not, and it does not need to be.",
        None, "Where it goes: a ticking list beside the answer box; the gate in front of the AI marker; a “you are in the middle band, what is missing” nudge before submit."))
# ---------------- middling / no
if desc:
    s = desc["summary"]
    withtext = [r for r in desc["rows"] if r["subject"] and not any(k in r["subject"] for k in ("maths", "english-language", "french", "spanish", "german", "music"))]
    mism = sum(1 for r in withtext if r["matches"] < 0.5)
    parts.append(card("Lesson descriptions", ("maybe", "Useful, with a filter"),
        "Does the one-line description match the lesson, and does it promise something the lesson does not deliver?",
        [("Lessons checked", s["lessons"]), ("Mismatches on article lessons", "%d of %d" % (mism, len(withtext))), ("Promises the lesson does not keep", pct(s["promises_missing_rate"]))],
        "The raw mismatch rate was inflated by practice-first and listening lessons, whose content lives outside the lesson text I gave it. Filtered to article lessons it is a short, plausible worklist.", None, None))
if badges2:
    s = badges2["summary"]; s1 = badges["summary"] if badges else None
    parts.append(card("Badge versus mark-scheme totals", ("no", "Not this"),
        "The 899 mismatches Opus adjudicated on 18 Sep, re-judged by Jev with the parsed scheme total supplied.",
        [("Four-way agreement with Opus", pct(s["four_way_agreement"])), ("As a “needs a change” flag", "precision %s, recall %s" % (pct(s["needs_change"]["precision"]), pct(s["needs_change"]["recall"]))), ("First framing", pct(s1["agreement"]) + " agreement" if s1 else "")],
        "The task is arithmetic over a scheme (add the bands, spot the SPaG extra), and the model is documented as unable to count. It knew: three quarters of its answers came back with low confidence. Keep this with Opus.", None, None))
if fc:
    s = fc["summary"]
    parts.append(card("Fact-check triage without evidence", ("no", "Not this"),
        "700 corrections from the retro fact-check: could Jev tell the wrong sentence from the corrected one, blind?",
        [("Picked the corrected version", pct(s["pairwise"]["accuracy"])), ("At high confidence", "%s of %d, a tenth of the cases" % (pct(s["pairwise"]["by_confidence"]["high"]["rate"]), s["pairwise"]["by_confidence"]["high"]["n"])), ("Blind error score separates them", "AUC %.2f, barely" % s["blind"]["auc"])],
        "It is a judge, not an oracle: it has no store of facts about the Turnip Winter or the Christchurch magnitude. Where it was confident it was usually right, and it did catch invented mark-scheme claims. Given the spec text or a source as evidence it may do far better; that is the next experiment, not this one.", None, None))
if tier:
    s = tier["summary"]
    parts.append(card("Higher-tier tagging", ("no", "Not this"),
        "Science lessons wrap Higher-only content in a marker. Could Jev tell Higher chunks from shared ones, blind?",
        [("Chunks", s["chunks"]), ("Separation within a lesson", "AUC %.2f" % s["within_lesson_auc"]), ("Usable threshold", "none: nothing crosses 50% either way")],
        "Same reason as the fact-check: which content is Higher is a fact about the spec, not a judgement about the text. With the spec's tier table supplied it would be a different test.", None, None))

# ---------------- cost table
cost_rows = "".join('<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%.3f</td></tr>' % (e(t), len(v), sorted(v)[len(v) // 2], sorted(v)[int(len(v) * 0.95)], tok[t] / 1e6 * 0.042) for t, v in sorted(by.items(), key=lambda kv: -len(kv[1])))

page = """<title>Jev on StudyVault</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Inter:wght@400;500;600&display=swap">
<style>
:root{--bg:#faf8f5;--ink:#2d2a26;--muted:#6f685f;--rule:#e4ddd2;--card:#ffffff;--accent:#2f6b6b;--accent-ink:#1f4c4c;--good:#2f6b6b;--goodbg:#e6f0ef;--pipe:#5a5f8a;--pipebg:#e9e9f3;--no:#a24d2a;--nobg:#f6e7df;--maybe:#8a6d1f;--maybebg:#f5efdc}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1c1a17;--ink:#ece6dc;--muted:#a69e92;--rule:#3a352e;--card:#26231f;--accent:#7fc1bd;--accent-ink:#a9dbd7;--good:#7fc1bd;--goodbg:#233634;--pipe:#a9acd9;--pipebg:#2b2c3d;--no:#e0906d;--nobg:#3d2a21;--maybe:#d9b85a;--maybebg:#3a3323}}
:root[data-theme="dark"]{--bg:#1c1a17;--ink:#ece6dc;--muted:#a69e92;--rule:#3a352e;--card:#26231f;--accent:#7fc1bd;--accent-ink:#a9dbd7;--good:#7fc1bd;--goodbg:#233634;--pipe:#a9acd9;--pipebg:#2b2c3d;--no:#e0906d;--nobg:#3d2a21;--maybe:#d9b85a;--maybebg:#3a3323}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:15px;line-height:1.55;margin:0;padding-block:32px 72px;padding-inline:max(16px,calc((100% - 720px)/2))}
h1,h2,h3{font-family:"Source Serif 4",Georgia,serif;text-wrap:balance;margin:0}
h1{font-size:34px;font-weight:600;line-height:1.15}
.lede{color:var(--muted);margin:10px 0 0;max-width:62ch}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:26px 0 0}
.stat{background:var(--card);border:1px solid var(--rule);border-radius:16px;padding:14px 16px}
.stat b{display:block;font-family:"Source Serif 4",Georgia,serif;font-size:26px;font-weight:600;font-variant-numeric:tabular-nums}
.stat span{color:var(--muted);font-size:13px}
.verdicts{margin:34px 0 0;padding:18px 20px;background:var(--card);border:1px solid var(--rule);border-radius:16px}
.verdicts h2{font-size:18px;margin-bottom:8px}
.verdicts p{margin:6px 0;max-width:68ch}
.verdicts b{font-weight:600}
h2.sect{font-size:22px;font-weight:600;margin-top:44px;padding-top:20px;border-top:1px solid var(--rule)}
.exp{margin-top:26px;padding:18px 20px;background:var(--card);border:1px solid var(--rule);border-radius:16px}
.exp-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap}
.exp h2{font-size:19px;font-weight:600}
.verdict{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:4px;white-space:nowrap}
.v-build{color:var(--good);background:var(--goodbg)}.v-pipe{color:var(--pipe);background:var(--pipebg)}.v-no{color:var(--no);background:var(--nobg)}.v-maybe{color:var(--maybe);background:var(--maybebg)}
.what{margin:10px 0 0;max-width:68ch}
table.nums{border-collapse:collapse;width:100%;margin:12px 0 0;font-variant-numeric:tabular-nums}
table.nums th{text-align:left;font-weight:500;color:var(--muted);padding:6px 10px 6px 0;border-bottom:1px solid var(--rule);width:46%;vertical-align:top}
table.nums td{padding:6px 0;border-bottom:1px solid var(--rule);vertical-align:top}
.examples{margin:12px 0 0;padding:10px 14px;background:var(--bg);border-radius:10px;font-size:13.5px}
.examples p{margin:4px 0;color:var(--ink)}
.caveat{margin:12px 0 0;color:var(--muted);max-width:68ch}
.build{margin:10px 0 0;max-width:68ch;color:var(--accent-ink)}
.wrap{overflow-x:auto}
table.cost{border-collapse:collapse;width:100%;margin-top:14px;font-variant-numeric:tabular-nums;font-size:13.5px}
table.cost th,table.cost td{text-align:left;padding:6px 10px;border-bottom:1px solid var(--rule)}
table.cost th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
table.cost td:not(:first-child),table.cost th:not(:first-child){text-align:right}
p{max-width:68ch}
</style>
<h1>Jev on StudyVault</h1>
<p class="lede">Overnight, 19 September 2026. Jev is TypeSafe's decision model: state in, typed answers out, each with a probability. It writes nothing. Every experiment below ran on real StudyVault data, against a ground truth where one existed, on the key you set last night.</p>
<div class="stats">
<div class="stat"><b>@CALLS@</b><span>calls made</span></div>
<div class="stat"><b>$@USD@</b><span>spent of $3</span></div>
<div class="stat"><b>@P50@ ms</b><span>median answer</span></div>
<div class="stat"><b>@P95@ ms</b><span>slowest 5%</span></div>
<div class="stat"><b>@NEXP@</b><span>experiments</span></div>
</div>
<div class="verdicts">
<h2>The short version</h2>
<p>Your instinct holds, with one sharp boundary. Jev is a judge, not an oracle. Give it the evidence and a well-scoped question and it is right, calibrated and almost free at any scale we have. Ask it to know a fact or count marks and it fails, and it says so with low confidence.</p>
<p><b>Build for students:</b> typed-recall flashcards, a “what do you want to revise?” box, a live marking-point checklist and a cheap gate in front of the AI marker, sign-up from a pasted subject list, and a safeguarding net over anything a student types.</p>
<p><b>Use in the pipeline now:</b> widget matching for the 3-lesson band, duplicate-lesson detection fleet-wide, a specification coverage matrix per subject, related-media relevance in the Sunday audit, the knowledge-check audit, and the question-type relabel.</p>
<p><b>Not this:</b> fact-checking without evidence, Higher-tier tagging, badge-versus-scheme arithmetic. Each needs either facts it does not hold or counting it cannot do.</p>
</div>
<h2 class="sect">The experiments</h2>
@PARTS@
<h2 class="sect">What it cost</h2>
<p>Input tokens are the only charge. The whole night, including the two runs that failed and were re-run, came to a dollar and a bit.</p>
<div class="wrap"><table class="cost"><thead><tr><th>Experiment</th><th>Calls</th><th>Median ms</th><th>95th ms</th><th>$</th></tr></thead><tbody>@COST@</tbody></table></div>
<h2 class="sect">What I would build first</h2>
<p>Typed-recall flashcards. It is the smallest change with the largest effect on the thing the platform is for: the retrieval-strength ratings become real. Then the search box, because it removes the one moment a student has to know the site's structure. The pipeline uses can run this week without touching what students see.</p>
<p>Everything here is in <code>scripts/_jev/</code>: the harness, one script per experiment, the result files with every row, and this page's generator.</p>
""".replace("@CALLS@", "{:,}".format(total_calls)).replace("@USD@", "%.2f" % total_usd).replace("@P50@", str(p50)).replace("@P95@", str(p95)).replace("@NEXP@", str(len(parts))).replace("@PARTS@", "".join(parts)).replace("@COST@", cost_rows)
io.open(os.path.join(R, "report.html"), "w", encoding="utf-8").write(page)
print("report written; experiments:", len(parts), "calls:", total_calls, "usd: %.3f" % total_usd)
