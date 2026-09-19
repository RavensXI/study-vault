"""Judged curation of a lesson's flashcards (Jev). For each lesson the deck is the curated
flashcard_questions plus recall_cards (generated term / definition / cloze and authored list /
explain). Jev reads the lesson and every card and scores each card on:
  central   - does it test a central idea of the lesson (0..2)
  redundant - is the same thing already tested by another card in the deck (0..1)
Code then keeps the best cards up to a cap, always at least one of each kind that exists,
dropping generated cards before authored ones and never touching the curated deck itself
(curated cards that score badly are only REPORTED, for a human look).

  python scripts/flashcards/curate_recall_cards.py --subject history-aqa --dry      # report what would go
  python scripts/flashcards/curate_recall_cards.py --subject history-aqa --apply    # writes recall_cards
  python scripts/flashcards/curate_recall_cards.py --all-free --apply [--school-id X]
Cap: 14 cards a lesson in total (curated + kept recall cards). Dropped recall cards are kept
in the row under "off": true so the decision is reversible and the card can come back.
"""
import io, json, os, re, sys, html, collections, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_jev"))
from jev import ask_many, answers, Score, Noul

CAP = 14
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
        if c and (c.get("q") or c.get("question")): cards.append({"id": "q%d" % i, "kind": "recall", "src": "curated", "front": strip(c.get("q") or c.get("question")), "answer": strip(c.get("a") or c.get("answer") or "")})
    for i, c in enumerate(l.get("recall_cards") or []):
        if c and c.get("front"): cards.append({"id": "r%d" % i, "kind": c.get("kind", "recall"), "src": c.get("src", "generated"), "front": strip(c["front"]), "answer": strip(c.get("answer", "")), "off": bool(c.get("off"))})
    return cards

def build(job):
    l, cards = job["lesson"], job["cards"]
    qs = {}
    for c in cards:
        qs["c_" + c["id"]] = Score(instructions="How central to this lesson is what card %s tests: '%s' (answer: %s)" % (c["id"], c["front"][:200], c["answer"][:120]),
                                   criteria=["a side detail a student could skip", "worth knowing", "a central idea or fact the lesson exists to teach"])
        qs["d_" + c["id"]] = Noul(instructions="Another card in the deck already tests the same fact or idea as card %s ('%s')" % (c["id"], c["front"][:160]))
    deck = "\n".join("%s [%s]: %s -> %s" % (c["id"], c["kind"], c["front"][:160], c["answer"][:100]) for c in cards)
    return ({"lesson_title": l["title"], "lesson_text": strip(l.get("content_html"))[:30000], "deck": deck}, qs)

def choose(cards, scores):
    """keep order: curated always; then authored, then generated, by score; cap total"""
    for c in cards:
        s = scores.get(c["id"], {})
        c["central"] = s.get("central", 1.0); c["redundant"] = s.get("redundant", 0.0)
        c["score"] = c["central"] - 1.2 * c["redundant"]
    curated = [c for c in cards if c["src"] == "curated"]
    rest = [c for c in cards if c["src"] != "curated"]
    rest.sort(key=lambda c: (-(c["src"] == "authored"), -c["score"]))
    room = max(0, CAP - len(curated))
    keep, kinds = [], set()
    # one of each kind first, then by score, never a card that is redundant and marginal
    for c in rest:
        if c["kind"] not in kinds and c["score"] > 0.2 and len(keep) < room: keep.append(c); kinds.add(c["kind"])
    for c in rest:
        if c in keep or len(keep) >= room: continue
        if c["score"] > 0.5: keep.append(c)
    return curated, keep, [c for c in rest if c not in keep]

def run(slug, school, apply):
    sch = ("eq." + school) if school else "is.null"
    rows = get("lessons?select=id,title,lesson_number,content_html,flashcard_questions,recall_cards,units!inner(slug,subjects!inner(slug,school_id))&units.subjects.slug=eq.%s&units.subjects.school_id=%s&status=eq.live&is_listening=eq.false&content_html=not.is.null&limit=2000" % (slug, sch))
    jobs = [{"lesson": l, "cards": [c for c in deck_of(l) if not c.get("off")]} for l in rows]
    jobs = [j for j in jobs if len(j["cards"]) > CAP - 2]          # nothing to trim otherwise
    res = ask_many(jobs, build, tag="curate", workers=6)
    dropped = 0; kept = 0; weak_curated = []
    for j, r, err in res:
        if not r: continue
        a = answers(r); sc = {}
        for k, v in a.items():
            cid = k[2:]; sc.setdefault(cid, {})
            if k.startswith("c_"): sc[cid]["central"] = v["score"]
            else: sc[cid]["redundant"] = v["noul"]
        curated, keep, drop = choose(j["cards"], sc)
        kept += len(keep); dropped += len(drop)
        weak_curated += [(j["lesson"]["units"]["slug"], j["lesson"]["lesson_number"], c["front"][:80], round(c["score"], 2)) for c in curated if c["score"] < 0.3]
        if not apply:
            if dropped <= 24:
                for c in drop: print("  DROP %s L%s [%s/%s] %.2f | %s" % (j["lesson"]["units"]["slug"], j["lesson"]["lesson_number"], c["kind"], c["src"], c["score"], c["front"][:90]))
            continue
        rc = j["lesson"].get("recall_cards") or []
        offs = {c["id"] for c in drop}
        for i, c in enumerate(rc):
            if not c: continue
            if ("r%d" % i) in offs: c["off"] = True
            elif ("r%d" % i) in {k["id"] for k in keep}: c.pop("off", None)
        patch("lessons?id=eq." + j["lesson"]["id"], {"recall_cards": rc})
    print("%-32s lessons judged %3d | recall cards kept %4d dropped %4d | weak curated cards %d%s" % (slug, len(res), kept, dropped, len(weak_curated), "" if apply else " (dry)"))
    return weak_curated

def main():
    a = sys.argv[1:]; apply = "--apply" in a
    school = a[a.index("--school-id") + 1] if "--school-id" in a else None
    subjects = [a[a.index("--subject") + 1]] if "--subject" in a else ([s["slug"] for s in get("subjects?select=slug&school_id=is.null&status=eq.live&order=slug")] if "--all-free" in a else [])
    if not subjects: print(__doc__); return
    weak = []
    for s in subjects: weak += run(s, school, apply)
    if weak:
        io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_authored", "weak_curated_cards.json"), "w", encoding="utf-8").write(json.dumps(weak, indent=1, ensure_ascii=False))
        print("weak curated cards listed for a human look:", len(weak))

if __name__ == "__main__":
    main()
