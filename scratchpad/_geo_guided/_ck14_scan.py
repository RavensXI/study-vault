# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_ck14_live.json"
pd = json.load(open(P, encoding='utf-8'))["practice_data"]
pb = pd["problem_bank"]
S = json.dumps(pd, ensure_ascii=False)

print("== em dashes ==", S.count("—"), "en dash:", S.count("–"))
print("== check:wrong ==", S.count('"check"'))
print("== html entities ==", re.findall(r"&[a-z]+;", S)[:10])

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "[%d]" % i)
    else:
        yield path, o

for p, v in walk(pd):
    if isinstance(v, str) and "—" in v:
        print("EMDASH", p, v[:80])
    if p.endswith(".check"):
        print("CHECK KEY", p, v)

print("\n== per problem ==")
for t in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[t]):
        tag = "%s[%d]" % (t, i)
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if "answer" in s]
        # boundary
        bidx = [j for j, s in enumerate(gs) if s.get("phase") == "substitute"]
        pre = len([s for s in gs[:bidx[0]] if "answer" in s]) if bidx else None
        post = len([s for s in gs[bidx[0]:] if "answer" in s]) if bidx else None
        nonnum = [(j, s.get("answer")) for j, s in enumerate(gs) if "answer" in s and not isinstance(s.get("answer"), (int, float))]
        sol = p.get("solutions")
        last = boxes[-1].get("answer") if boxes else None
        print("%-10s it=%-16s unit=%-4s sol=%-8s boxes=%d pre=%s post=%s lastbox=%s%s" % (
            tag, p.get("input_type"), p.get("unit", "-"), sol, len(boxes), pre, post, last,
            "  NONNUM:%s" % nonnum if nonnum else ""))
        if not bidx:
            print("    !! NO phase:substitute")
        # misconceptions
        for m in p.get("misconceptions", []):
            keys = sorted(m.keys())
            print("     misc %s expect=%r" % (keys, m.get("expect")))
        # hint plaintext
        h = p.get("hint", "")
        if re.search(r"[<>\\$]", h): print("    !! hint markup:", h)
        # options em dash / units
        for oi, o in enumerate(p.get("options", []) or []):
            if "—" in o: print("    !! option emdash", oi)

print("\n== tier guides word counts ==")
for t in ("bronze", "silver", "gold"):
    tg = pd["tier_guides"][t]
    w = sum(len(s.split()) for s in tg["steps"])
    print(t, "steps=", len(tg["steps"]), "words=", w, "| title:", tg["title"])

print("\n== method_card words ==", len(re.sub("<[^>]+>", " ", pd["method_card"]["content"]).split()),
      "steps=", len(pd["method_card"]["steps"]))

print("\n== board-neutral scan ==")
for b in ["AQA", "Edexcel", "OCR", "Eduqas", "WJEC", "mark", "marks"]:
    hits = [p for p, v in walk(pd) if isinstance(v, str) and re.search(r"\b%s\b" % b, v)]
    if hits: print(b, hits[:6])
