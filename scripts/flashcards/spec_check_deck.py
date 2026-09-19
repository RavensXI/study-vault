"""Check every ACTIVE flashcard in a unit against the specification text (Jev): could a student
be examined on this, given the spec content? Reports the share within scope and lists the
outliers. Read-only.
  python scripts/flashcards/spec_check_deck.py <subject> <unit> <spec.md> <first line> <last line>
"""
import io, json, os, re, sys, html, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_jev"))
import jev
from jev import ask_many, answers, Noul
jev.BUDGET_USD = 12.0
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
def get(path): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
subject, unit, specf, a, b = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
spec = "\n".join(io.open(specf, encoding="utf-8").read().splitlines()[a - 1:b])
rows = get("lessons?select=id,title,lesson_number,flashcard_questions,recall_cards,units!inner(slug,subjects!inner(slug,school_id))&units.slug=eq.%s&units.subjects.slug=eq.%s&units.subjects.school_id=is.null&status=eq.live&order=lesson_number" % (unit, subject))
jobs = []
for l in rows:
    cards = [{"front": strip(c.get("q") or c.get("question")), "answer": strip(c.get("a") or c.get("answer") or ""), "kind": "recall"} for c in (l["flashcard_questions"] or []) if c and not c.get("off") and (c.get("q") or c.get("question"))]
    cards += [{"front": strip(c["front"]), "answer": strip(c.get("answer", "")), "kind": c.get("kind", "recall")} for c in (l["recall_cards"] or []) if c and not c.get("off") and c.get("front")]
    jobs.append({"lesson": l, "cards": cards})
def build(j):
    qs = {"k%d" % i: Noul(instructions="A student could be examined on what this flashcard tests, given the specification content: '%s' (answer: %s). Say no if the card asks for a detail the specification does not name and would not expect a student to recall." % (c["front"][:200], c["answer"][:120])) for i, c in enumerate(j["cards"])}
    return ({"specification_content": spec[:30000], "lesson_title": j["lesson"]["title"]}, qs)
res = ask_many(jobs, build, tag="speccheck", workers=6)
n = within = 0; out = []
for j, r, err in res:
    if not r: print("failed", j["lesson"]["lesson_number"], err); continue
    a = answers(r)
    for i, c in enumerate(j["cards"]):
        p = a.get("k%d" % i, {}).get("noul", 0.5); n += 1
        if p >= 0.5: within += 1
        else: out.append((p, j["lesson"]["lesson_number"], c["kind"], c["front"][:90], c["answer"][:60]))
out.sort()
print("%s / %s: %d active cards, %d within the spec (%d%%), %d outliers" % (subject, unit, n, within, round(100 * within / max(n, 1)), len(out)))
for p, ln, k, f, ans in out[:25]: print("  %.2f L%s [%s] %s -> %s" % (p, ln, k, f, ans))
