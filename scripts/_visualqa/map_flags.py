"""Map each visual-walk flag to the stored problem it came from.

The walk numbers screens in the order a student meets them, which does not line up
reliably with the stored order once a tier resets, so matching is by content: the
judge's one-line description quotes or paraphrases the stem, and the problem in that
lesson sharing the most distinctive words with it is the one on screen.
"""
import io, json, re, sys
from collections import Counter

HERE = __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0]
rows = json.load(io.open(HERE + "/englang2_data.json", encoding="utf-8"))
flags = json.load(io.open(HERE + "/flags.json", encoding="utf-8"))
STOP = set("""the a an and or of to in for on with by from as at is are was were be this that these those it its
their they them not no but if then so which who what when where how why all any each only question asks student
students shown visible screen text passage answer options option click select there only but has have will would
should about into one two three four five words word shows shown asks asked""".split())


def toks(s):
    return [w for w in re.findall(r"[a-z][a-z'-]{2,}", (s or "").lower()) if w not in STOP]


def flat(q):
    parts = [q.get("question") or ""]
    for k in ("original", "quote", "brief", "context"):
        if isinstance(q.get(k), str): parts.append(q[k])
    for s in q.get("statements") or []:
        if isinstance(s, dict): parts.append(s.get("text") or "")
    for c in q.get("chips") or []:
        if isinstance(c, dict): parts.append(c.get("text") or "")
    for t in q.get("tokens") or []:
        if isinstance(t, dict): parts.append(t.get("text") or "")
    for o in q.get("options") or []:
        if isinstance(o, str): parts.append(o)
    for c in q.get("claims") or []:
        if isinstance(c, str): parts.append(c)
    return " ".join(parts)


by_lesson = {}
for r in rows:
    by_lesson["%s/%s" % (r["units"]["slug"], r["lesson_number"])] = r

out = []
for f in flags:
    r = by_lesson.get("%s/%d" % (f["unit"], f["n"]))
    best, score = None, -1
    want = Counter(toks(f["what"]))
    for tier, qs in (r["practice_data"].get("problem_bank") or {}).items():
        for i, q in enumerate(qs):
            have = set(toks(flat(q)))
            s = sum(n for w, n in want.items() if w in have)
            if s > score:
                best, score = (tier, i, q), s
    tier, i, q = best
    out.append(dict(f, tier=tier, i=i, type=q.get("input_type"), stem=(q.get("question") or "")[:200],
                    passage_id=q.get("passage_id"), score=score, lesson_id=r["id"]))
io.open(HERE + "/flags_mapped.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
for o in out:
    print("%-13s %-20s %-6s %-2d %-18s s=%-2d %s" % (o["fault"], "%s/%d" % (o["unit"], o["n"]), o["tier"], o["i"],
                                                   o["type"], o["score"], o["stem"][:70].replace("\n", " ")))
