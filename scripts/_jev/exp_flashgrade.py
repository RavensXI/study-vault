"""E20 - Typed-recall flashcards. Today a student flips a card and taps "got it" or "not yet".
If Jev can judge whether a typed recall matches the card's answer, cards become a real test.
Ground truth built from the data itself: for each card, the RIGHT recall is the card's own
answer (and a lightly mangled version of it: lower-cased, a word dropped, a typo), the WRONG
recall is the answer of a different card from the same lesson (a hard negative on the same
topic), and a NEAR-MISS is the answer to a card from the same unit's neighbouring lesson."""
import io, json, os, sys, re, random, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, sb_all, sb_get, Noul, Score
random.seed(21)
light = sb_all("lessons?select=id,units!inner(subjects!inner(school_id))&status=eq.live&is_listening=eq.false&units.subjects.school_id=is.null")
random.shuffle(light); ids = [r["id"] for r in light[:300]]
rows = []
for k in range(0, len(ids), 40):
    rows += sb_get("lessons?select=id,title,lesson_number,flashcard_questions,units!inner(slug,subjects!inner(slug))&id=in.(" + ",".join(ids[k:k + 40]) + ")")
def mangle(a):
    w = a.split()
    if len(w) > 4 and random.random() < 0.5: w.pop(random.randrange(len(w)))
    s = " ".join(w).lower()
    if len(s) > 12 and random.random() < 0.6:
        i = random.randrange(2, len(s) - 2); s = s[:i] + s[i + 1] + s[i] + s[i + 2:]
    return s
items = []
for r in rows:
    cards = [c for c in (r.get("flashcard_questions") or []) if c.get("q") and c.get("a") and 3 <= len(c["a"].split()) <= 40]
    if len(cards) < 3: continue
    for c in random.sample(cards, min(3, len(cards))):
        others = [o for o in cards if o is not c]
        wrong = random.choice(others)
        base = {"subject": r["units"]["subjects"]["slug"], "unit": r["units"]["slug"], "n": r["lesson_number"], "q": c["q"], "answer": c["a"]}
        items.append({**base, "typed": c["a"], "truth": "right_verbatim"})
        items.append({**base, "typed": mangle(c["a"]), "truth": "right_mangled"})
        items.append({**base, "typed": wrong["a"], "truth": "wrong_same_lesson"})
        if random.random() < 0.5:
            items.append({**base, "typed": " ".join(c["a"].split()[:max(2, len(c["a"].split()) // 3)]), "truth": "partial"})
random.shuffle(items); items = items[:1200]
print("cards", len(items), collections.Counter(i["truth"] for i in items))
def build(it):
    return ({"flashcard_question": it["q"], "model_answer": it["answer"], "student_typed_recall": it["typed"]},
            {"correct": Noul(instructions="The student's typed recall gives the same fact as the model answer; different wording, spelling mistakes and missing minor words are fine"),
             "completeness": Score(instructions="How much of the model answer the recall covers", criteria=["none of it", "part of it", "all of it"])})
res = ask_many(items, build, tag="flashgrade", workers=8)
out = []
for it, r, err in res:
    if not r: continue
    a = answers(r); out.append({**it, "p": a["correct"]["noul"], "cov": a["completeness"]["score"]})
def rate(label, th, above=True):
    xs = [o for o in out if o["truth"] == label]
    return "%d/%d" % (sum(1 for o in xs if (o["p"] >= th) == above), len(xs))
summary = {"n": len(out), "at_0.5": {"verbatim_accepted": rate("right_verbatim", 0.5), "mangled_accepted": rate("right_mangled", 0.5), "wrong_rejected": rate("wrong_same_lesson", 0.5, False), "partial_accepted": rate("partial", 0.5)},
           "at_0.7": {"verbatim_accepted": rate("right_verbatim", 0.7), "mangled_accepted": rate("right_mangled", 0.7), "wrong_rejected": rate("wrong_same_lesson", 0.7, False), "partial_accepted": rate("partial", 0.7)},
           "mean_p": {k: round(sum(o["p"] for o in out if o["truth"] == k) / max(1, sum(1 for o in out if o["truth"] == k)), 3) for k in ("right_verbatim", "right_mangled", "wrong_same_lesson", "partial")},
           "mean_completeness": {k: round(sum(o["cov"] for o in out if o["truth"] == k) / max(1, sum(1 for o in out if o["truth"] == k)), 2) for k in ("right_verbatim", "right_mangled", "wrong_same_lesson", "partial")},
           "wrong_but_accepted": [{"q": o["q"][:80], "answer": o["answer"][:70], "typed": o["typed"][:70], "p": o["p"]} for o in out if o["truth"] == "wrong_same_lesson" and o["p"] >= 0.7][:8]}
print(json.dumps(summary, indent=1, ensure_ascii=False)); save("flashgrade.json", {"summary": summary, "rows": out})
