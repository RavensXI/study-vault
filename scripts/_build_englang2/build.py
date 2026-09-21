"""Edexcel English Language 2.0 (1EN2) — practice-format build.

1EN2 re-pairs the four skill blocks of 1EN0, which we already hold:
    1EN0 P1 fiction reading + imaginative writing | P2 non-fiction reading + transactional writing
    1EN2 P1 19th-c NON-FICTION reading (AO4 evaluate) + TRANSACTIONAL writing
         P2 contemporary fiction + literary non-fiction (AO3 compare) + IMAGINATIVE writing
So the two WRITING units port from 1EN0 with their exam framing rewritten, and the two
READING units are fresh: the text periods move and the assessment objective moves with them.

  python scripts/_build_englang2/build.py plan       # the lesson list, no writes
  python scripts/_build_englang2/build.py activate   # subject + units + 50 lesson rows
  python scripts/_build_englang2/build.py port       # the 24 writing lessons, no API
  python scripts/_build_englang2/build.py submit s1  # batch a stage for the 26 reading lessons
  python scripts/_build_englang2/build.py collect s1 # poll + save that stage
  python scripts/_build_englang2/build.py assemble   # merge stages -> practice_data -> Supabase
  python scripts/_build_englang2/build.py status

Stages: s1 passages, s2 method card + exam context + worked examples, s3 bronze, s4 silver+gold.
Lessons land at pending_review for Tom; the subject row is live (free-tier rule).
"""
import io, json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out")
os.makedirs(OUT, exist_ok=True)
STATE = os.path.join(OUT, "_state.json")
# The house rule is the strongest model for anything a student reads: pipeline_api_generate.py
# and pipeline_api_guides.py are both Opus, and Sonnet appears only on classification, media
# matching and cleanup. The first run of this build used Sonnet by inheriting it from the
# flashcard script; Tom caught it (21 Sep 2026) and the reading units were rebuilt on Opus.
MODEL = "claude-opus-4-6"
SLUG = "english-language-2-edexcel"
SRC = "english-language-edexcel"

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(p):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, headers=H), timeout=180).read())
def post(p, body, prefer="return=representation"):
    r = urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, data=json.dumps(body).encode(),
        headers=dict(H, Prefer=prefer), method="POST"), timeout=120).read()
    return json.loads(r) if r else None
def patch(p, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()
def state():
    return json.load(io.open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
def save_state(s):
    io.open(STATE, "w", encoding="utf-8").write(json.dumps(s, indent=1))

# ----------------------------------------------------------------- the plan
PAPER1 = {"name": "Paper 1: Non-Fiction Texts", "time": "1 hour 55 minutes", "marks": "80 marks (50% of the qualification)"}
PAPER2 = {"name": "Paper 2: Contemporary Texts", "time": "1 hour 55 minutes", "marks": "80 marks (50% of the qualification)"}

UNITS = [
  {"slug": "paper-1-reading", "name": "Paper 1: 19th-Century Non-Fiction Reading", "sort": 1, "kind": "reading",
   "paper": PAPER1, "ao": "AO1 (find and interpret), AO2 (analyse language and structure) and AO4 (evaluate a text critically)",
   "texts": "unseen 19th-century non-fiction: letters, diaries, speeches, journalism, travel writing, reports and pamphlets",
   "section": "Section A: six questions, three on each of two thematically linked unseen 19th-century non-fiction extracts",
   "lessons": [
     "Reading 19th-Century Non-Fiction: Forms and Conventions",
     "Locating Explicit and Implicit Information",
     "Analysing Language in 19th-Century Prose",
     "Structure and Organisation in Non-Fiction",
     "Tone, Register and the 19th-Century Voice",
     "Purpose, Audience and Context",
     "Using Subject Terminology Precisely",
     "Summarising a 19th-Century Extract",
     "Drawing Inferences from Period Detail",
     "Evaluating a Writer's Methods",
     "Evaluating How Far You Agree",
     "Handling Unfamiliar Vocabulary",
     "Paper 1 Reading - Exam Practice"]},
  {"slug": "paper-1-writing", "name": "Paper 1: Transactional Writing", "sort": 2, "kind": "port",
   "paper": PAPER1, "from_unit": "paper-2-writing",
   "section": "Section B: one extended transactional writing task from a choice of two, assessing AO5 and AO6, with 16 of the 80 marks for spelling, punctuation and grammar"},
  {"slug": "paper-2-reading", "name": "Paper 2: Contemporary Reading", "sort": 3, "kind": "reading",
   "paper": PAPER2, "ao": "AO1 (find and interpret), AO2 (analyse language and structure) and AO3 (compare writers' ideas and perspectives across two texts)",
   "texts": "unseen 20th- and 21st-century prose fiction and literary non-fiction: novels, short stories, memoir, travel writing and reportage",
   "section": "Section A: two questions on the first unseen text, two on the second, then two on both texts together",
   "lessons": [
     "Contemporary Fiction and Literary Non-Fiction",
     "Identifying Information Across Two Texts",
     "Analysing Language in Contemporary Prose",
     "Structural Features and Narrative Shape",
     "Characterisation and Voice",
     "Memoir, Travel Writing and Reportage",
     "Perspective and Viewpoint",
     "Making Inferences in Contemporary Texts",
     "Comparing Writers' Ideas",
     "Comparing Writers' Methods",
     "Building a Comparison Answer",
     "Subject Terminology for Comparison",
     "Paper 2 Reading - Exam Practice"]},
  {"slug": "paper-2-writing", "name": "Paper 2: Imaginative Writing", "sort": 4, "kind": "port",
   "paper": PAPER2, "from_unit": "paper-1-writing",
   "section": "Section B: one extended imaginative writing task from a choice of two, assessing AO5 and AO6, with 16 of the 80 marks for spelling, punctuation and grammar"},
]
READING = [u for u in UNITS if u["kind"] == "reading"]

def reading_lessons():
    out = []
    for u in READING:
        for i, t in enumerate(u["lessons"], 1):
            out.append({"key": u["slug"] + "/" + str(i), "unit": u, "n": i, "title": t})
    return out

def cmd_plan():
    total = 0
    for u in UNITS:
        n = len(u["lessons"]) if u["kind"] == "reading" else 12
        total += n
        print("\n%-16s %-44s %2d lessons  (%s)" % (u["slug"], u["name"], n, u["kind"]))
        if u["kind"] == "reading":
            for i, t in enumerate(u["lessons"], 1):
                print("   %2d %s" % (i, t))
        else:
            print("      ported from %s/%s with the exam framing rewritten" % (SRC, u["from_unit"]))
    print("\n%d lessons: %d fresh, 24 ported." % (total, len(reading_lessons())))

# ------------------------------------------------------------- activation
QUOTES = None
def cmd_activate():
    src = get("subjects?select=*&slug=eq.%s&school_id=is.null" % SRC)[0]
    have = get("subjects?select=id&slug=eq.%s&school_id=is.null" % SLUG)
    if have:
        sid = have[0]["id"]; print("subject exists", sid)
    else:
        settings = dict(src["settings"] or {})
        settings["practice_units"] = [u["slug"] for u in UNITS]
        row = {"slug": SLUG, "name": "English Language 2.0", "exam_board": "Edexcel", "spec_code": "1EN2",
               "status": "live", "is_active": True, "sort_order": src.get("sort_order") or 0,
               "color": src.get("color"), "settings": settings, "school_id": None}
        sid = post("subjects", row)[0]["id"]; print("subject created", sid)
    srcunits = {u["slug"]: u for u in get("units?select=*,subjects!inner(slug)&subjects.slug=eq.%s&order=sort_order" % SRC)}
    for u in UNITS:
        ex = get("units?select=id&subject_id=eq.%s&slug=eq.%s" % (sid, u["slug"]))
        if ex:
            uid = ex[0]["id"]
        else:
            s = srcunits.get(u["from_unit"] if u["kind"] == "port" else u["slug"], {})
            n = len(u["lessons"]) if u["kind"] == "reading" else 12
            uid = post("units", {"subject_id": sid, "slug": u["slug"], "name": u["name"], "sort_order": u["sort"],
                                 "lesson_count": n, "accent": s.get("accent"), "accent_light": s.get("accent_light"),
                                 "accent_badge": s.get("accent_badge"), "body_class": s.get("body_class"),
                                 "image_url": s.get("image_url"), "subtitle": s.get("subtitle")})[0]["id"]
            print("unit created", u["slug"])
        u["id"] = uid
        titles = u["lessons"] if u["kind"] == "reading" else [l["title"] for l in get(
            "lessons?select=title,lesson_number,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s&units.slug=eq.%s&status=eq.live&order=lesson_number" % (SRC, u["from_unit"]))]
        for i, t in enumerate(titles, 1):
            if get("lessons?select=id&unit_id=eq.%s&lesson_number=eq.%d" % (uid, i)):
                continue
            post("lessons", {"unit_id": uid, "lesson_number": i, "title": t,
                             "slug": re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-"), "status": "pending_review"},
                 prefer="return=minimal")
        print("  %-16s %2d lesson rows" % (u["slug"], len(titles)))
    st = state(); st["subject_id"] = sid; save_state(st)

# ------------------------------------------------------------------- port
PAPER_RE = re.compile(r"Paper\s*([12])", re.I)
def reframe(obj, from_paper, to_paper):
    """Swap every Paper 1/Paper 2 reference and rewrite the named paper title."""
    if isinstance(obj, dict): return {k: reframe(v, from_paper, to_paper) for k, v in obj.items()}
    if isinstance(obj, list): return [reframe(v, from_paper, to_paper) for v in obj]
    if not isinstance(obj, str): return obj
    s = obj
    s = s.replace("Paper 1: Fiction and Imaginative Writing", to_paper["name"])
    s = s.replace("Paper 2: Non-Fiction and Transactional Writing", to_paper["name"])
    s = s.replace("Paper 1: Imaginative Writing", to_paper["name"])
    s = s.replace("Paper 2: Transactional Writing", to_paper["name"])
    s = PAPER_RE.sub(lambda m: "Paper " + ("1" if to_paper is PAPER1 else "2"), s)
    return s

def cmd_port():
    sid = state()["subject_id"]
    moved = 0
    for u in UNITS:
        if u["kind"] != "port": continue
        src_rows = get("lessons?select=lesson_number,title,description,practice_data,units!inner(slug,subjects!inner(slug))"
                       "&units.subjects.slug=eq.%s&units.slug=eq.%s&status=eq.live&order=lesson_number" % (SRC, u["from_unit"]))
        uid = get("units?select=id&subject_id=eq.%s&slug=eq.%s" % (sid, u["slug"]))[0]["id"]
        from_paper = PAPER2 if u["from_unit"].startswith("paper-2") else PAPER1
        for r in src_rows:
            pd = reframe(r["practice_data"], from_paper, u["paper"])
            pd["exam_context"] = {"paper": u["paper"]["name"], "time": "45 minutes for Section B",
                                  "marks": "40 marks (24 content and organisation, 16 spelling, punctuation and grammar)",
                                  "frequency": "Section B on every " + u["paper"]["name"].split(":")[0]}
            if isinstance(pd.get("topic_links"), dict):
                for kk in ("prerequisites", "next"):
                    for link in (pd["topic_links"].get(kk) or []):
                        if isinstance(link, dict) and link.get("slug"):
                            link["slug"] = u["slug"] + "/" + str(link["slug"]).rsplit("/", 1)[-1]
            tgt = get("lessons?select=id&unit_id=eq.%s&lesson_number=eq.%d" % (uid, r["lesson_number"]))
            if not tgt: continue
            patch("lessons?id=eq." + tgt[0]["id"], {"practice_data": pd, "description": r["description"], "status": "pending_review"})
            moved += 1
        print("ported %-16s %2d lessons" % (u["slug"], len(src_rows)))
    print("ported lessons:", moved)

# ------------------------------------------------------------------ batch
SYSTEM = """You write practice-format GCSE English Language lessons for StudyVault. The qualification is
Pearson Edexcel English Language 2.0. Students are 15 to 16 years old.

Hard rules:
- Everything you write is ORIGINAL. Never reproduce or imitate a real past paper question, a mark scheme, or
  any published text. Passages are written by you, in period, and are your own work.
- Never name an exam board, a specification, a paper code or an assessment objective code in anything a
  student reads. Talk about "this paper", "the reading section", "evaluating", "comparing".
- Plain words a 15-year-old uses. British English.
- Reply with JSON only. No prose, no markdown fence."""

def stage_prompt(stage, L, prior):
    u = L["unit"]
    head = ("LESSON: %s\nUNIT: %s\nPAPER: %s, %s, %s\nWHAT THE READING SECTION ASKS: %s\nSKILLS ASSESSED: %s\nTEXTS: %s\n"
            % (L["title"], u["name"], u["paper"]["name"], u["paper"]["time"], u["paper"]["marks"],
               u["section"], u["ao"], u["texts"]))
    if stage == "s1":
        return head + """
Write THREE original extracts for this lesson, one per difficulty tier, that the lesson's questions will work on.
Each must be a genuine piece of the kind of text named above, not a description of one, and must be rich enough
to ask language, structure and inference questions about.
  bronze 120-170 words, accessible   silver 170-220 words   gold 200-260 words, more demanding
Give each a label a student would see, naming the form and a plausible source, e.g. "Source A - Letter to a
Manchester newspaper, 1847". Invent the sources; they are yours.
JSON: {"passages":[{"id":"bronze","label":"...","text":"..."},{"id":"silver",...},{"id":"gold",...}]}"""
    if stage == "s2":
        return head + "\nTHE THREE EXTRACTS:\n" + json.dumps(prior.get("passages"), ensure_ascii=False)[:6000] + """

Write the teaching frame for this lesson.
- method_card: title (the lesson title), content (2-3 sentences of HTML in <p> tags, strategy not content:
  how a student approaches this task), steps (4-6 imperative steps).
- exam_context: {"paper": the paper name given above, "time": realistic minutes for this kind of question,
  "marks": realistic marks, "frequency": where it appears}
- worked_examples: exactly three, one per tier, each {"difficulty":"Bronze"|"Silver"|"Gold","question":"...",
  "steps":[{"label":"Step 1","content":"..."}, ...]} with 3-4 steps. Work on the matching extract above and
  frame illustratively ("Look at the phrase...", "Consider how..."), never "Read this extract now".
  The LAST step of each worked example also carries "isAnswer": true.
JSON: {"method_card":{...},"exam_context":{...},"worked_examples":[...]}"""
    ptxt = json.dumps(prior.get("passages"), ensure_ascii=False)[:6000]
    if stage == "s3":
        return head + "\nTHE THREE EXTRACTS:\n" + ptxt + """

Write EIGHT bronze-tier problems: the accessible end, one step each, building confidence.
Every problem is an object with "question", "input_type", "passage_id":"bronze", and the fields its type needs:
  multiple_choice   "options":[4 strings, no A./B. prefixes], "solutions":[index], "wrong":{"0":"why that is wrong",...}
  traffic_light     "statements":[{"text":"...","correct":"category","explain":"..."}], 4-6 statements
  highlight_evidence "instruction":"...", "answers":["exact phrase from the extract", ...], "explain":"..."
  connotation_picker "word":"...", "options":[3-4 strings], "solutions":[index], "explain":"..."
  evidence_match    "pairs":[{"left":"claim","right":"quotation from the extract","explain":"..."}]
  misleading_summary "summaries":[{"text":"...","correct":true|false,"explain":"..."}]
Use at least four different input types. Every quotation must appear verbatim in the bronze extract.
JSON: {"bronze":[...8 problems...]}"""
    return head + "\nTHE THREE EXTRACTS:\n" + ptxt + """

Write the harder two tiers.
- "silver": SIX problems on the silver extract ("passage_id":"silver"), two steps of thinking each.
- "gold": FIVE problems on the gold extract ("passage_id":"gold"), the hardest, and at least two of them
  "input_type":"ai_mark" with "marks": 4-8, "instruction" and "mark_scheme_points":[3-5 short strings a
  marker would credit]. Reward insight, not format: naming a word without quotation marks is valid evidence.
Non-ai_mark problems repeat the bronze field contract EXACTLY - never abbreviate it:
  multiple_choice   "question", "options":[4 strings, no A./B. prefixes], "solutions":[index of the right one],
                    "wrong":{"0":"why that one is wrong", ...}. The key is "solutions" and it is a LIST holding
                    the INDEX. Never "answer", never "correct_answer", never the option's text.
  traffic_light     "statements":[{"text","correct","explain"}]
  highlight_evidence "instruction", "answers":[exact phrases], "explain"
  connotation_picker "word", "options", "solutions":[index], "explain"
  evidence_match    "pairs":[{"left","right","explain"}]
  misleading_summary "summaries":[{"text","correct","explain"}]
Every quotation must appear verbatim in the matching extract.
JSON: {"silver":[...6...],"gold":[...5...]}"""

MAXTOK = {"s1": 3000, "s2": 4000, "s3": 6000, "s4": 6000}

def cmd_submit(stage):
    import anthropic
    cl = anthropic.Anthropic()
    st = state(); done = st.setdefault("stages", {})
    prior = {}
    for s in ("s1", "s2", "s3"):
        f = os.path.join(OUT, s + ".json")
        if os.path.exists(f):
            for k, v in json.load(io.open(f, encoding="utf-8")).items(): prior.setdefault(k, {}).update(v) if isinstance(v, dict) else None
    p1 = json.load(io.open(os.path.join(OUT, "s1.json"), encoding="utf-8")) if os.path.exists(os.path.join(OUT, "s1.json")) else {}
    reqs = []
    for L in reading_lessons():
        pr = p1.get(L["key"], {})
        reqs.append({"custom_id": L["key"].replace("/", "__"),
                     "params": {"model": MODEL, "max_tokens": MAXTOK[stage], "thinking": {"type": "disabled"},
                                "system": SYSTEM, "messages": [{"role": "user", "content": stage_prompt(stage, L, pr)}]}})
    b = cl.messages.batches.create(requests=reqs)
    done[stage] = b.id; save_state(st)
    print("submitted %s: %s (%d requests)" % (stage, b.id, len(reqs)))

def cmd_collect(stage):
    import anthropic
    cl = anthropic.Anthropic()
    st = state(); bid = st["stages"][stage]
    b = cl.messages.batches.retrieve(bid)
    print(stage, b.processing_status, b.request_counts.model_dump())
    if b.processing_status != "ended":
        return False
    out = {}; usage = {"in": 0, "out": 0}; bad = 0
    for r in cl.messages.batches.results(bid):
        if r.result.type != "succeeded": bad += 1; continue
        m = r.result.message; usage["in"] += m.usage.input_tokens; usage["out"] += m.usage.output_tokens
        text = "".join(x.text for x in m.content if x.type == "text")
        mm = re.search(r"\{.*\}", text, re.S)
        try: out[r.custom_id.replace("__", "/")] = json.loads(mm.group(0))
        except Exception: bad += 1
    io.open(os.path.join(OUT, stage + ".json"), "w", encoding="utf-8").write(json.dumps(out, indent=1, ensure_ascii=False))
    # INDICATIVE ONLY - the Anthropic console is authoritative. The list prices in
    # pipeline_api_generate.py are stale: this figure over-read the real spend 3x on the
    # 1EN2 Opus run (Tom checked the balance, 21 Sep 2026).
    rin, rout = (7.5, 37.5) if "opus" in MODEL else (1.5, 7.5)
    cost = usage["in"] / 1e6 * rin + usage["out"] / 1e6 * rout
    st.setdefault("usage", {})[stage] = dict(usage, usd=round(cost, 2)); save_state(st)
    print("%s: %d lessons, %d unusable | in %d out %d | $%.2f (batch)" % (stage, len(out), bad, usage["in"], usage["out"], cost))
    return True

# --------------------------------------------------------------- assemble
def normalise(q):
    """Both models drift from the field contract in the same small ways: Opus writes "type"
    for "input_type" and adds a "tier" key, Sonnet writes "answer"/"correct_answer" instead of
    "solutions", and both attach their reasoning under steps/thinking. Map it all back rather
    than re-running the batch (Tom, 21 Sep 2026)."""
    if not q.get("input_type") and q.get("type"):
        q["input_type"] = q.pop("type")
    q.pop("type", None); q.pop("tier", None)
    if not q.get("question"):
        q["question"] = q.pop("instruction", None) or q.get("question") or "Answer using the extract."
    if q.get("input_type") == "multiple_choice" and not isinstance(q.get("solutions"), list):
        ans = q.pop("correct_answer", None) or q.pop("answer", None)
        opts = q.get("options") or []
        idx = ans if isinstance(ans, int) and 0 <= ans < len(opts) else None
        if idx is None and isinstance(ans, str):
            for i, o in enumerate(opts):
                if str(o).strip().lower() == ans.strip().lower(): idx = i; break
        if idx is not None: q["solutions"] = [idx]
    q.pop("correct_answer", None); q.pop("answer", None)
    for kk in ("steps", "thinking", "steps_of_thinking", "thinking_steps"):
        if kk in q:
            st = q.pop(kk)
            if isinstance(st, list) and st and not q.get("explain"):
                q["explain"] = " ".join(str(x) for x in st)
    # Now the per-type contract the RENDERER actually reads (practice.html render*()).
    # The pipeline doc lists the type names but not their fields, so both models invented
    # plausible ones. These are taken from the live 1EN0 rows (Tom, 21 Sep 2026).
    t = q.get("input_type")
    if t == "highlight_evidence":
        if q.get("answers") and not q.get("answer_text"):
            a = q.pop("answers"); q["answer_text"] = a[0] if isinstance(a, list) and a else a
        q.pop("answers", None)
        if q.get("explain") and not q.get("explanation"): q["explanation"] = q.pop("explain")
        q.pop("explain", None)
    elif t == "misleading_summary":
        if q.get("summaries") and not q.get("summaryParts"):
            parts = []
            for x in q.pop("summaries"):
                part = {"text": x.get("text", ""), "wrong": not x.get("correct", False)}
                if x.get("explain"): part["explain"] = x["explain"]
                parts.append(part)
            q["summaryParts"] = parts
        q.pop("summaries", None)
        # 1EN0 also has a second, older shape: statements[] with a "misleading" flag.
        # renderMS() only reads summaryParts, so those rows render nothing (they are still
        # like that on the live 1EN0 lessons - reported to Tom 21 Sep 2026).
        if not q.get("summaryParts") and q.get("statements"):
            parts = []
            for x in q.pop("statements"):
                part = {"text": x.get("text", ""), "wrong": bool(x.get("misleading") or x.get("wrong"))}
                if x.get("explain"): part["explain"] = x["explain"]
                parts.append(part)
            q["summaryParts"] = parts
        q.pop("statements", None) if q.get("summaryParts") else None
    elif t == "traffic_light":
        # renderTL() builds its legend from the statement categories and calls .charAt on them,
        # so a boolean "correct" throws and the problem renders nothing.
        for st in (q.get("statements") or []):
            if isinstance(st.get("correct"), bool):
                st["correct"] = "supported by the text" if st["correct"] else "not supported"
            elif st.get("correct") is not None and not isinstance(st["correct"], str):
                st["correct"] = str(st["correct"])
    elif t == "connotation_picker":
        if not q.get("chips"):
            opts = q.pop("options", None) or []
            sol = set(q.pop("solutions", None) or [])
            if opts: q["chips"] = [{"text": o, "correct": i in sol} for i, o in enumerate(opts)]
        q.pop("word", None); q.pop("options", None); q.pop("solutions", None)
    elif t == "evidence_match":
        if q.get("pairs") and not q.get("claims"):
            pairs = q.pop("pairs")
            claims, quotes = [], []
            for pr in pairs:
                left = pr.get("left") or pr.get("claim") or ""
                if left not in claims: claims.append(left)
                quotes.append({"text": pr.get("right") or pr.get("quote") or "", "correctClaim": claims.index(left)})
            q["claims"] = claims; q["quotes"] = quotes
        q.pop("pairs", None)
    elif t == "multiple_choice":
        if q.get("wrong") and not q.get("misconceptions"):
            w = q.pop("wrong")
            if isinstance(w, dict):
                q["misconceptions"] = [{"id": "distractor-%s" % k, "expect": int(k), "message": v}
                                       for k, v in w.items() if str(k).isdigit()]
        q.pop("wrong", None)
    elif t == "ai_mark":
        q.pop("instruction", None)
    return q


def cmd_assemble():
    sid = state()["subject_id"]
    S = {s: json.load(io.open(os.path.join(OUT, s + ".json"), encoding="utf-8")) for s in ("s1", "s2", "s3", "s4")
         if os.path.exists(os.path.join(OUT, s + ".json"))}
    loaded = skipped = 0
    for L in reading_lessons():
        k = L["key"]
        if not all(k in S.get(s, {}) for s in ("s1", "s2", "s3", "s4")):
            skipped += 1; continue
        u = L["unit"]; n = L["n"]; titles = u["lessons"]
        pd = {"passages": S["s1"][k]["passages"],
              "method_card": S["s2"][k]["method_card"],
              "exam_context": S["s2"][k]["exam_context"],
              "worked_examples": S["s2"][k]["worked_examples"],
              "problem_bank": {"bronze": [normalise(x) for x in S["s3"][k]["bronze"]],
                               "silver": [normalise(x) for x in S["s4"][k]["silver"]],
                               "gold": [normalise(x) for x in S["s4"][k]["gold"]]},
              "topic_links": {"prerequisites": ([{"slug": "%s/%d" % (u["slug"], n - 1), "title": titles[n - 2]}] if n > 1 else []),
                              "next": ([{"slug": "%s/%d" % (u["slug"], n + 1), "title": titles[n]}] if n < len(titles) else [])}}
        # ai_mark problems point at a named prompt (the 1EN0 convention) and carry the
        # marker's checklist as "context"; without the key the QA gate flags ai-no-prompt.
        skill = "compare" if u["slug"].startswith("paper-2") else "evaluate"
        ai = [p for tier in pd["problem_bank"].values() for p in tier if p.get("input_type") == "ai_mark"]
        for p in ai:
            p["ai_prompt_key"] = skill
            if p.get("mark_scheme_points") and not p.get("context"):
                p["context"] = "A good response covers: " + "; ".join(str(x) for x in p.pop("mark_scheme_points"))
            p.pop("mark_scheme_points", None)
            if not p.get("question"):
                p["question"] = p.pop("instruction", "Answer in full sentences.")
            p.pop("instruction", None)
        if ai:
            focus = ("compares how the two writers present their ideas and perspectives"
                     if skill == "compare" else "evaluates how successfully the writer achieves their purpose")
            pd["ai_marking_prompts"] = {skill: (
                "You are a GCSE English Language tutor. The student " + focus + ".\n\n"
                "- Mastering (excellent): precise references, explains how the writer's choices work on a reader, sustained and even-handed.\n"
                "- Secure (good): clear points with evidence and some explanation of effect.\n"
                "- Developing (needs_work): identifies features but explains effect thinly, or leans on one text.\n"
                "- Emerging (not_valid): retells the text without addressing the question.\n\n"
                "Naming a word or phrase without quotation marks is valid evidence. Do not require a set structure or "
                "named terminology. Be encouraging. Give the mark out of the marks available and one sentence on what "
                "would raise it.")}
        uid = get("units?select=id&subject_id=eq.%s&slug=eq.%s" % (sid, u["slug"]))[0]["id"]
        row = get("lessons?select=id&unit_id=eq.%s&lesson_number=eq.%d" % (uid, n))
        if not row: skipped += 1; continue
        patch("lessons?id=eq." + row[0]["id"], {"practice_data": pd, "status": "pending_review",
              "description": (pd["method_card"].get("content") or "")[:220].replace("<p>", "").replace("</p>", "").strip()[:200]})
        loaded += 1
    print("assembled %d reading lessons | waiting on stages: %d" % (loaded, skipped))

def cmd_status():
    st = state()
    print(json.dumps({k: v for k, v in st.items() if k != "meta"}, indent=1)[:1200])
    for s in ("s1", "s2", "s3", "s4"):
        f = os.path.join(OUT, s + ".json")
        print("  %s: %s" % (s, len(json.load(io.open(f, encoding="utf-8"))) if os.path.exists(f) else "-"))
    tot = sum(v.get("usd", 0) for v in (st.get("usage") or {}).values())
    print("  spend so far: $%.2f" % tot)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    cmd = a[0]
    if cmd == "plan": cmd_plan()
    elif cmd == "activate": cmd_activate()
    elif cmd == "port": cmd_port()
    elif cmd == "submit": cmd_submit(a[1])
    elif cmd == "collect": cmd_collect(a[1])
    elif cmd == "assemble": cmd_assemble()
    elif cmd == "status": cmd_status()
    else: print(__doc__)
