import json, re
pd = json.load(open("_CHK_ocrL01_live.json", encoding="utf-8"))
emdash_hits=[]
def scan(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k=="note":  # internal, exempt
                continue
            scan(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "—" in obj or "–" in obj:
            emdash_hits.append((path, obj))
scan(pd, "")
print("emdash/endash hits:", len(emdash_hits))
for p,s in emdash_hits: print(p, "::", s[:80])

# hints must be plain text (no LaTeX \( or HTML tags)
badhints=[]
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,pr in enumerate(pb[t]):
        h=pr.get("hint","")
        if "\(" in h or "<" in h:
            badhints.append(f"{t}[{i}] hint: {h}")
print("bad hints:", badhints)

# numeric-only answers
badans=[]
def chk(steps, base):
    for i,s in enumerate(steps):
        if "answer" in s and not isinstance(s["answer"], (int,float)):
            badans.append(f"{base}[{i}] answer={s['answer']!r}")
g=pd["guided"]
chk(g["opener"]["steps"],"opener")
for t in ["bronze","silver","gold"]:
    chk(g["teach"][t]["steps"],f"teach.{t}")
    for i,pr in enumerate(pb[t]):
        chk(pr.get("guided_steps",[]),f"{t}[{i}]")
print("non-numeric answers:", badans)

# tier guide word budget (<=115 words in steps)
for t in ["bronze","silver","gold"]:
    tg=pd["tier_guides"][t]
    wc=sum(len(re.sub(r'<[^>]+>','',s).split()) for s in tg["steps"])
    print(f"tier_guides.{t} steps words:", wc)
