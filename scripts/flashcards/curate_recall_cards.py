"""Judged curation of a lesson's whole flashcard deck (Jev). The deck is the curated
flashcard_questions (12-15 plain question cards on most lessons) plus recall_cards (generated
term / definition / cloze and authored list / explain), so 20-26 cards before curation. Jev
reads the lesson and every card and answers, per card:
  central    - does it test a central idea of the lesson (Score 0..2)
  scope      - would a GCSE examiner expect it recalled from memory, or is it context (Noul)
  duplicate  - which other card, if any, tests the same fact or idea (Choice: none | card id)
Hard rule first: a list card asking for more than LIST_MAX items (or more than it holds) goes off.
Every card in the row is a candidate on every run, switched-off ones included, so the pass is
re-runnable and a deck that loses cards backfills from the pool.
Code then: merges duplicate pairs into groups and keeps one card a group (the more central
card; a typed kind over a plain question at equal centrality); keeps at least one card of
each kind present; fills the deck up to CAP by centrality with no kind taking more than
KIND_MAX slots. Dropped cards stay in the row under "off": true (both decks skip them), so
every decision is reversible and a card can come back.

  python scripts/flashcards/curate_recall_cards.py --subject history-aqa --dry      # record what would go
  python scripts/flashcards/curate_recall_cards.py --subject history-aqa --apply    # writes both columns
  python scripts/flashcards/curate_recall_cards.py --all-free --apply
  python scripts/flashcards/curate_recall_cards.py --school-id X --apply            # every subject of a school
Records: _authored/curation_<slug>[_dry].json
"""
import io, json, os, re, sys, html, collections, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_jev"))
import jev
from jev import ask_many, answers, Score, Choice, Noul
jev.BUDGET_USD = 12.0        # topped up 19 Sep; the fleet pass is about $2

CAP = 14; KIND_MAX = 7; DUP_P = 0.6; SCOPE_P = 0.35; LIST_MAX = 6
NUM = {"three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
def list_count(front):
    m = re.search(r"\b(three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\b", front.lower())
    return 0 if not m else (NUM.get(m.group(1)) or int(m.group(1)))
TYPED = {"definition", "cloze", "list", "explain", "term"}
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(), headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=60).read()
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()

def deck_of(l):
    cards = []
    for i, c in enumerate(l.get("flashcard_questions") or []):
        if c and (c.get("q") or c.get("question")): cards.append({"id": "q%d" % i, "kind": "recall", "src": "curated", "front": strip(c.get("q") or c.get("question")), "answer": strip(c.get("a") or c.get("answer") or ""), "off": bool(c.get("off"))})
    for i, c in enumerate(l.get("recall_cards") or []):
        if c and c.get("front"): cards.append({"id": "r%d" % i, "kind": c.get("kind", "recall"), "src": c.get("src", "generated"), "front": strip(c["front"]), "answer": strip(c.get("answer", "")), "off": bool(c.get("off")), "items": c.get("items") or []})
    return cards

def build(job):
    l, cards = job["lesson"], job["cards"]
    qs = {}
    for c in cards:
        qs["c_" + c["id"]] = Score(instructions="How central to this lesson is what card %s tests: '%s' (answer: %s)" % (c["id"], c["front"][:200], c["answer"][:120]),
                                   criteria=["a side detail a student could skip", "worth knowing", "a central idea or fact the lesson exists to teach"])
        qs["s_" + c["id"]] = Noul(instructions="A GCSE examiner would expect a student to recall what card %s asks from memory in the exam: '%s' (answer: %s). Not if it is context the lesson gives so the story makes sense: an exact day-and-month date, a minor name, a precise figure, or a list longer than a student would ever be asked." % (c["id"], c["front"][:200], c["answer"][:120]))
        crit = {"none": "no other card in the deck tests the same fact or idea"}
        for o in cards:
            if o["id"] != c["id"]: crit[o["id"]] = None
        qs["d_" + c["id"]] = Choice(instructions="Which other card in the deck tests the SAME fact or idea as card %s ('%s'), so that a student who can answer one can answer the other? Pick none if no card does." % (c["id"], c["front"][:160]), criteria=crit)
    deck = "\n".join("%s [%s]: %s -> %s" % (c["id"], c["kind"], c["front"][:160], c["answer"][:100]) for c in cards)
    return ({"lesson_title": l["title"], "lesson_text": strip(l.get("content_html"))[:30000], "deck": deck}, qs)

def choose(cards, sc):
    for c in cards:
        s = sc.get(c["id"], {}); c["central"] = s.get("central", 1.0); c["dup"] = s.get("dup"); c["dup_p"] = s.get("dup_p", 0.0); c["scope"] = s.get("scope", 1.0)
    # best first: centrality, a typed kind ahead of a plain question at equal centrality, curated ahead of generated
    order = sorted(cards, key=lambda c: (-(c["central"] + (0.3 if c["kind"] in TYPED else 0)), c["src"] != "curated"))
    names = {c["id"]: (c["dup"] if c["dup_p"] >= DUP_P else None) for c in cards}
    keep, per_kind, later = [], collections.Counter(), []
    def twin(c):
        """a kept card that this card duplicates (pairwise, never a chain)"""
        for k in keep:
            if names[c["id"]] == k["id"] or names[k["id"]] == c["id"]: return k
    for c in order:
        if c["kind"] == "list" and (len(c["items"]) > LIST_MAX or list_count(c["front"]) > max(len(c["items"]), LIST_MAX)): c["why"] = "too long a list"; continue
        if c["scope"] < SCOPE_P: c["why"] = "beyond what the exam asks"; continue
        t = twin(c)
        if t: c["why"] = "same as " + t["id"]; continue
        if c["central"] < 0.7: c["why"] = "side detail"; continue
        if len(keep) >= CAP: c["why"] = "deck full"; continue
        if per_kind[c["kind"]] >= KIND_MAX: later.append(c); continue
        keep.append(c); per_kind[c["kind"]] += 1
    for c in later:                                       # a kind past its share only fills a short deck
        if len(keep) < CAP and not twin(c): keep.append(c)
        else: c["why"] = "enough %s cards" % c["kind"]
    keep.sort(key=lambda c: (c["id"][0] != "q", int(c["id"][1:])))
    drop = [c for c in cards if c not in keep]
    return keep, drop

def run(slug, school, apply):
    sch = ("eq." + school) if school else "is.null"
    rows = get("lessons?select=id,title,lesson_number,content_html,flashcard_questions,recall_cards,units!inner(slug,subjects!inner(slug,school_id))&units.subjects.slug=eq.%s&units.subjects.school_id=%s&status=eq.live&is_listening=eq.false&content_html=not.is.null&limit=2000" % (slug, sch))
    jobs = [{"lesson": l, "cards": deck_of(l)} for l in rows]          # every card, switched-off ones included: the pass is re-runnable
    jobs = [j for j in jobs if len(j["cards"]) > 0]
    res = ask_many(jobs, build, tag="curate", workers=6)
    record = []; dropped = kept = 0; fails = 0
    for j, r, err in res:
        if not r: fails += 1; continue
        a = answers(r); sc = {}
        for k, v in a.items():
            cid = k[2:]; sc.setdefault(cid, {})
            if k.startswith("c_"): sc[cid]["central"] = v["score"]
            elif k.startswith("s_"): sc[cid]["scope"] = v["noul"]
            else:
                ch = v.get("choice"); sc[cid]["dup"] = None if ch == "none" else ch
                sc[cid]["dup_p"] = (v.get("probabilities") or {}).get(ch, v.get("confidence", 0.0)) or 0.0
        keep, drop = choose(j["cards"], sc)
        kept += len(keep); dropped += len(drop)
        record.append({"id": j["lesson"]["id"], "unit": j["lesson"]["units"]["slug"], "n": j["lesson"]["lesson_number"], "title": j["lesson"]["title"], "deck": len(j["cards"]), "after": len(keep),
                       "keep": [{"id": c["id"], "kind": c["kind"], "src": c["src"], "front": c["front"], "answer": c["answer"], "central": round(c["central"], 2)} for c in keep],
                       "drop": [{"id": c["id"], "kind": c["kind"], "src": c["src"], "front": c["front"], "answer": c["answer"], "central": round(c["central"], 2), "scope": round(c["scope"], 2), "why": c["why"]} for c in drop]})
        if not apply: continue
        offs = {c["id"] for c in drop}; ons = {c["id"] for c in keep}
        fq = j["lesson"].get("flashcard_questions") or []; rc = j["lesson"].get("recall_cards") or []
        for pre, arr in (("q", fq), ("r", rc)):
            for i, c in enumerate(arr):
                if not c: continue
                cid = "%s%d" % (pre, i)
                if cid in offs: c["off"] = True
                elif cid in ons: c.pop("off", None)
        patch("lessons?id=eq." + j["lesson"]["id"], {"flashcard_questions": fq, "recall_cards": rc})
    io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_authored", "curation_%s%s%s.json" % (("unity__" if school else ""), slug, "" if apply else "_dry")), "w", encoding="utf-8").write(json.dumps(record, indent=1, ensure_ascii=False))
    sizes = sorted(len(x["keep"]) for x in record)
    print("%-36s lessons %3d (judged %3d, failed %d) | kept %5d dropped %5d | deck after: median %s max %s%s" % (slug, len(rows), len(record), fails, kept, dropped, sizes[len(sizes) // 2] if sizes else "-", sizes[-1] if sizes else "-", "" if apply else " (dry)"), flush=True)
    return record

def main():
    a = sys.argv[1:]; apply = "--apply" in a
    school = a[a.index("--school-id") + 1] if "--school-id" in a else None
    if "--subject" in a: subjects = [a[a.index("--subject") + 1]]
    elif "--all-free" in a: subjects = [s["slug"] for s in get("subjects?select=slug&school_id=is.null&status=eq.live&order=slug")]
    elif school: subjects = [s["slug"] for s in get("subjects?select=slug&school_id=eq.%s&status=eq.live&order=slug" % school)]
    else: print(__doc__); return
    for s in subjects: run(s, school, apply)
    print("jev spent so far: $%.2f" % jev.spent()[0])

if __name__ == "__main__":
    main()
