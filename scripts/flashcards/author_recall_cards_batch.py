"""Author list + explain flashcards for every live free-tier article lesson, on the Batch API
(Sonnet), then gate with Jev and load. Unity lessons never go through the API (subscription
agents do those). Lessons that already carry authored cards (the canary units) are skipped.

  python scripts/flashcards/author_recall_cards_batch.py submit     # builds + submits the batch (whole free tier)
  python scripts/flashcards/author_recall_cards_batch.py submit --subject latin-eduqas --status pending_review   # one new subject
  python scripts/flashcards/author_recall_cards_batch.py collect    # polls; writes _authored/fleet.json when ended
  python scripts/flashcards/gate_authored_cards.py scripts/flashcards/_authored/fleet.json
  python scripts/flashcards/author_recall_cards_batch.py load       # passing cards -> lessons.recall_cards

State in _authored/_fleet_state.json. Usage totted from the batch results.
"""
import io, json, os, re, sys, html, time, urllib.request
import anthropic

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "_authored")
# scope: the whole free tier (default, tag "fleet") or one subject (--subject S [--school-id X] [--status pending_review]); files are named by the tag
A = sys.argv[2:]
SUBJECT = A[A.index("--subject") + 1] if "--subject" in A else None
SCHOOL = A[A.index("--school-id") + 1] if "--school-id" in A else None
STATUS = A[A.index("--status") + 1] if "--status" in A else "live"
TAG = (("unity__" if SCHOOL else "") + SUBJECT) if SUBJECT else "fleet"
STATE = os.path.join(OUT, "_%s_state.json" % TAG)
MODEL = "claude-sonnet-5"
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(), headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=60).read()
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
def state():
    return json.load(io.open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
def save(st): io.open(STATE, "w", encoding="utf-8").write(json.dumps(st, indent=1))

RULES = io.open(os.path.join(HERE, "..", "..", "docs", "FLASHCARD_RULES.md"), encoding="utf-8").read()[:6000]
SYSTEM = """You write flashcards for StudyVault, a GCSE revision site. You will be given one lesson's text, its glossary and the flashcards it already has. Write up to 2 LIST cards and up to 2 EXPLAIN cards for it.

Hard rules:
- A card may only use facts stated in the lesson text. Add nothing from elsewhere.
- Never name an exam board (no AQA, Edexcel, Pearson, OCR, Eduqas, WJEC) and never mention the exam, examiners, marks or the specification.
- Plain words a 15-year-old uses. Context lives in the question: it must say exactly what is being asked without the student guessing.
- Do not repeat what the existing flashcards already ask.
- If the lesson's text marks some content as Higher tier only (it will be labelled [HIGHER] ... [/HIGHER]), build a card on it only if the whole card sits inside that content, and then set "tier": "higher".

LIST card: the front asks for a set the lesson explicitly gives, with the count stated, e.g. "Name the four reasons the lesson gives for ...". "items" is 3 to 6 short strings (1 to 8 words each) as a student could recall them. The set must be complete and closed in the lesson, not "some examples". "answer" is the items joined with " / ". If the lesson has no closed list, write fewer or no list cards.
EXPLAIN card: the front asks why or how about one mechanism or cause ("Why did ...?", "How does ... cause ...?"). "answer" is ONE sentence of at most 30 words that a marker would accept as the full explanation, drawn from the lesson.

Reply with JSON only, no prose, in this shape:
{"cards": [{"kind": "list", "front": "...", "items": ["...", "..."], "answer": "... / ..."}, {"kind": "explain", "front": "...", "answer": "..."}]}

The flashcard rules the site follows:
""" + RULES

def lesson_prompt(l):
    txt = re.sub(r'<div class="higher-only">(.*?)</div>', lambda m: " [HIGHER] " + strip(m.group(1)) + " [/HIGHER] ", l.get("content_html") or "", flags=re.S)
    txt = strip(txt)[:14000]
    gl = "; ".join("%s: %s" % (strip(g.get("term", "")), strip(g.get("definition", ""))) for g in (l.get("glossary_terms") or [])[:30])
    ex = "\n".join("- Q: %s | A: %s" % (strip(c.get("q") or c.get("question") or ""), strip(c.get("a") or c.get("answer") or "")) for c in (l.get("flashcard_questions") or []) if c)
    return "LESSON TITLE: %s\n\nLESSON TEXT:\n%s\n\nGLOSSARY:\n%s\n\nEXISTING FLASHCARDS (do not repeat these):\n%s\n\nWrite the cards now as JSON." % (l["title"], txt, gl or "(none)", ex or "(none)")

def PARAMS(l):
    # thinking off: with adaptive thinking on, Sonnet spends the output budget thinking and the JSON is cut short
    return {"model": MODEL, "max_tokens": 2000, "thinking": {"type": "disabled"}, "system": SYSTEM, "messages": [{"role": "user", "content": lesson_prompt(l)}]}

def resubmit():
    """the lessons whose first answer was cut off (stop_reason max_tokens): same prompt, thinking off"""
    cl = anthropic.Anthropic(); st = state()
    ids = set(json.load(io.open(os.path.join(OUT, "_%s_failed_ids.json" % TAG))))
    todo = [l for l in lessons_to_do() if l["id"] in ids]
    print("resubmitting", len(todo))
    reqs = [{"custom_id": l["id"], "params": PARAMS(l)} for l in todo]
    for k in range(0, len(reqs), 2000):
        b = cl.messages.batches.create(requests=reqs[k:k + 2000]); st.setdefault("batches", []).append(b.id); print("submitted", b.id, len(reqs[k:k + 2000]))
    save(st)

def lessons_to_do():
    rows = []
    off = 0
    while True:
        page = get("lessons?select=id,title,lesson_number,content_html,glossary_terms,flashcard_questions,recall_cards,units!inner(slug,subjects!inner(slug,school_id))&status=eq.%s&is_listening=eq.false&content_html=not.is.null&units.subjects.school_id=%s%s&order=id&limit=500&offset=%d" % (STATUS, ("eq." + SCHOOL) if SCHOOL else "is.null", ("&units.subjects.slug=eq." + SUBJECT) if SUBJECT else "", off))
        rows += page
        if len(page) < 500: break
        off += 500
    todo = [l for l in rows if len(l.get("content_html") or "") > 1500 and not any((c or {}).get("src") == "authored" for c in (l.get("recall_cards") or []))]
    return todo

def submit():
    cl = anthropic.Anthropic()
    todo = lessons_to_do()
    print("lessons to author:", len(todo))
    reqs = [{"custom_id": l["id"], "params": PARAMS(l)} for l in todo]
    meta = {l["id"]: {"title": l["title"], "lesson_number": l["lesson_number"], "subject": l["units"]["subjects"]["slug"], "unit": l["units"]["slug"]} for l in todo}
    st = state(); st["batches"] = []; st["meta"] = meta
    for k in range(0, len(reqs), 2000):
        b = cl.messages.batches.create(requests=reqs[k:k + 2000])
        st["batches"].append(b.id); print("submitted", b.id, len(reqs[k:k + 2000]), "requests")
    save(st)

def collect():
    cl = anthropic.Anthropic(); st = state()
    allres = {}; usage = {"in": 0, "out": 0}; errs = 0; pending = 0
    for bid in st.get("batches", []):
        b = cl.messages.batches.retrieve(bid)
        print(bid, b.processing_status, b.request_counts.model_dump())
        if b.processing_status != "ended": pending += 1; continue
        for r in cl.messages.batches.results(bid):
            if r.result.type != "succeeded": errs += 1; continue
            m = r.result.message; usage["in"] += m.usage.input_tokens; usage["out"] += m.usage.output_tokens
            text = "".join(blk.text for blk in m.content if blk.type == "text")
            mm = re.search(r"\{.*\}", text, re.S)
            try: allres[r.custom_id] = json.loads(mm.group(0)) if mm else {"cards": []}
            except Exception:
                errs += 1
                if r.custom_id not in allres: allres[r.custom_id] = {"cards": []}     # a later (resubmitted) answer wins
    if pending: print("still running:", pending, "batch(es)"); return
    out = []
    for lid, res in allres.items():
        meta = st["meta"].get(lid, {})
        cards = []
        for c in (res.get("cards") or [])[:4]:
            if not isinstance(c, dict) or c.get("kind") not in ("list", "explain") or not c.get("front") or not c.get("answer"): continue
            card = {"kind": c["kind"], "front": strip(c["front"]), "answer": strip(c["answer"]), "src": "authored"}
            if c["kind"] == "list": card["items"] = [strip(x) for x in (c.get("items") or []) if x][:6]
            if c.get("tier") == "higher": card["tier"] = "higher"
            cards.append(card)
        out.append({"lesson_id": lid, "lesson_number": meta.get("lesson_number"), "title": meta.get("title"), "subject": meta.get("subject"), "unit": meta.get("unit"), "cards": cards})
    io.open(os.path.join(OUT, TAG + ".json"), "w", encoding="utf-8").write(json.dumps(out, indent=1, ensure_ascii=False))
    cost = usage["in"] / 1e6 * 1.5 + usage["out"] / 1e6 * 7.5
    print("lessons", len(out), "cards", sum(len(x["cards"]) for x in out), "errors", errs, "| tokens in %d out %d | est. $%.2f (batch prices)" % (usage["in"], usage["out"], cost))
    st["usage"] = usage; st["est_usd"] = round(cost, 2); save(st)

def load():
    cards = json.load(io.open(os.path.join(OUT, TAG + ".gated.json"), encoding="utf-8"))
    by = {}; held = 0
    for c in cards:
        if c.get("gate") != "pass": held += 1; continue
        by.setdefault(c["lesson_id"], []).append({k: c[k] for k in ("kind", "front", "answer", "items", "tier", "src") if c.get(k) is not None})
    added = 0
    for i, (lid, new) in enumerate(by.items()):
        cur = get("lessons?select=recall_cards&id=eq." + lid)[0]["recall_cards"] or []
        keep = [c for c in cur if c.get("src") != "authored"]; fronts = {c["front"] for c in keep}
        merged = keep + [c for c in new if c["front"] not in fronts]
        patch("lessons?id=eq." + lid, {"recall_cards": merged}); added += len(merged) - len(keep)
        if i % 500 == 0: print("loaded", i, "lessons")
    print("authored cards loaded:", added, "| held back:", held, "| lessons:", len(by))

if __name__ == "__main__":
    {"submit": submit, "resubmit": resubmit, "collect": collect, "load": load}[sys.argv[1]]()
