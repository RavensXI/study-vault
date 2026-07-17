import json, re
pd = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]

emdash = "—"
issues=[]

def walk(obj, path):
    if isinstance(obj, str):
        if emdash in obj:
            issues.append(("EMDASH", path, obj))
    elif isinstance(obj, dict):
        for k,v in obj.items():
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")

walk(pd, "pd")
print("EM DASH hits:", len([x for x in issues if x[0]=="EMDASH"]))
for x in issues:
    print(x)

# hints: check for LaTeX or HTML in hint fields (bank problems)
print("\n--- HINT field scan (should be plain text, no \\( or < )")
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][t]):
        h = p.get("hint","")
        if "\\(" in h or "<" in h or emdash in h:
            print(f"  {t}[{i}] hint suspicious: {h!r}")

# guided_steps box hints: plain text
print("\n--- guided_steps box hint scan for LaTeX/HTML")
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][t]):
        for j,s in enumerate(p.get("guided_steps",[])):
            h=s.get("hint","")
            if "\\(" in h or "<" in h:
                print(f"  {t}[{i}].gs[{j}] hint: {h!r}")
            # box answer numeric?
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                print(f"  {t}[{i}].gs[{j}] NON-NUMERIC answer: {s['answer']!r}")

# tier_guides word count
print("\n--- tier_guides step word counts (<=115)")
for tier,tg in pd["tier_guides"].items():
    words = sum(len(re.sub('<[^>]+>','',s).split()) for s in tg["steps"])
    print(f"  {tier}: {words} words")
