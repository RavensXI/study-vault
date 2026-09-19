"""Jev gate for authored list / explain cards before anyone reads them.

For each card, with the lesson text as evidence: every list item must be stated in the
lesson; an explain answer must be supported by the lesson and answer its own question; the
card must not name a board or talk about the exam (regex). Writes <file>.gated.json with a
verdict per card and prints a summary. Nothing touches the database.

  python scripts/flashcards/gate_authored_cards.py scripts/flashcards/_authored/history-aqa__britain-health-people.json
"""
import io, json, os, re, sys, html, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_jev"))
from jev import ask_many, answers, Noul, Score

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
def get(path):
    req = urllib.request.Request(U + "/rest/v1/" + path, headers={"apikey": K, "Authorization": "Bearer " + K})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
BAN = re.compile(r"\b(AQA|Edexcel|Pearson|OCR|Eduqas|WJEC|examiners?|the exam|mark scheme|marks?|the spec|specification)\b", re.I)

def main():
    src = sys.argv[1]
    data = json.load(io.open(src, encoding="utf-8"))
    ids = [l["lesson_id"] for l in data]
    text = {}
    for k in range(0, len(ids), 30):
        for row in get("lessons?select=id,content_html&id=in.(" + ",".join(ids[k:k + 30]) + ")"):
            text[row["id"]] = strip(row["content_html"])[:40000]
    jobs = []
    for l in data:
        for i, c in enumerate(l.get("cards") or []):
            jobs.append({"lesson": l, "i": i, "card": c, "text": text.get(l["lesson_id"], "")})
    def build(j):
        c = j["card"]
        qs = {"answerable": Noul(instructions="A student who had read this lesson text could answer the card's question, and the card's model answer is supported by the lesson text"),
              "clear": Score(instructions="How clearly the question tells the student what is being asked, without needing to guess", criteria=["ambiguous", "clear enough", "unmistakable"])}
        if c.get("kind") == "list":
            for n, it in enumerate(c.get("items") or []):
                qs["item%d" % n] = Noul(instructions="This item is stated in the lesson text as one of the things the question asks for: " + it)
            qs["closed"] = Noul(instructions="The lesson text presents exactly this set of items as the complete list, not a longer or open-ended one")
        else:
            qs["why"] = Noul(instructions="The model answer explains a cause or mechanism (why or how), not just a description")
        return ({"lesson_text": j["text"], "card_question": c.get("front"), "card_answer": c.get("answer"), "card_items": c.get("items")}, qs)
    res = ask_many(jobs, build, tag="authored_gate", workers=6)
    out = []; ok = 0
    for j, r, err in res:
        c = dict(j["card"]); c["lesson_number"] = j["lesson"]["lesson_number"]; c["title"] = j["lesson"]["title"]; c["lesson_id"] = j["lesson"]["lesson_id"]
        if not r: c["gate"] = "error"; out.append(c); continue
        a = answers(r)
        c["p_answerable"] = a["answerable"]["noul"]; c["clarity"] = a["clear"]["score"]
        probs = []
        if c.get("kind") == "list":
            c["item_p"] = [a["item%d" % n]["noul"] for n in range(len(c.get("items") or []))]
            c["p_closed"] = a["closed"]["noul"]
            if min(c["item_p"] or [0]) < 0.6: probs.append("an item is not in the lesson")
            if c["p_closed"] < 0.5: probs.append("the set is not closed in the lesson")
            if not (3 <= len(c.get("items") or []) <= 6): probs.append("item count")
        else:
            c["p_why"] = a["why"]["noul"]
            if c["p_why"] < 0.5: probs.append("answer describes rather than explains")
            if len((c.get("answer") or "").split()) > 34: probs.append("answer too long")
        if c["p_answerable"] < 0.6: probs.append("not answerable from the lesson")
        if c["clarity"] < 0.8: probs.append("question unclear")
        if BAN.search((c.get("front") or "") + " " + (c.get("answer") or "")): probs.append("names a board or the exam")
        c["gate"] = "pass" if not probs else "hold"; c["problems"] = probs
        ok += c["gate"] == "pass"; out.append(c)
    dst = src.replace(".json", ".gated.json")
    io.open(dst, "w", encoding="utf-8").write(json.dumps(out, indent=1, ensure_ascii=False))
    print("cards", len(out), "pass", ok, "hold", len(out) - ok)
    for c in out:
        if c["gate"] != "pass": print("  HOLD L%s %s | %s | %s" % (c["lesson_number"], c["kind"], c["front"][:70], ", ".join(c.get("problems") or [c["gate"]])))

if __name__ == "__main__":
    main()
