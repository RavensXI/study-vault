import json, re

live = json.load(open("_chk_live_numL01.json", encoding="utf-8"))

# 1. em dash + entity scan on student-facing strings
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            # skip internal note fields
            if k == "note":
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash = []
entities = []
for path, s in walk(live):
    if "—" in s:
        emdash.append((path, s))
    if re.search(r"&[a-zA-Z]+;|&#\d+;", s):
        entities.append((path, s))
print("EM DASHES:", len(emdash))
for p, s in emdash: print("  ", p, "::", s[:80])
print("ENTITIES:", len(entities))
for p, s in entities: print("  ", p, "::", s[:80])

# 2. numeric-only box answers
badbox = []
for tier in ["bronze","silver","gold"]:
    for i, prob in enumerate(live["problem_bank"][tier]):
        for j, st in enumerate(prob.get("guided_steps", [])):
            if "answer" in st and not isinstance(st["answer"], (int, float)):
                badbox.append((tier, i, j, st["answer"]))
print("NON-NUMERIC BOXES:", badbox)

# 3. tier guide word budget (<=115 words in steps)
for tier in ["bronze","silver","gold"]:
    tg = live["tier_guides"][tier]
    words = sum(len(re.sub(r"<[^>]+>","",s).split()) for s in tg["steps"])
    print(f"tier_guide {tier} steps words: {words}")

# preservation compare
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
print("PRE type:", type(pre))
if isinstance(pre, dict):
    print("PRE keys sample:", list(pre.keys())[:5])
