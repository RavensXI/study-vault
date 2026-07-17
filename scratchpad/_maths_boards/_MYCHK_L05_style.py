import json
live = json.load(open("_MYCHK_L05_live.json", encoding="utf-8"))

EM = "—"
def walk(obj, path=""):
    if isinstance(obj, dict):
        for k,v in obj.items():
            # skip internal note fields for em-dash rule
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EM in obj and not path.endswith(".note"):
            print("EM DASH:", path, "->", obj[:80])

walk(live)
print("em-dash sweep done")

# check hints are plain text (no LaTeX backslash, no < >)
pb = live["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        h = p.get("hint","")
        if "\\(" in h or "<" in h:
            print(f"HINT not plain: {t}[{i}] -> {h}")
        # guided_steps answers numeric
        for j,s in enumerate(p.get("guided_steps",[])):
            if "answer" in s and not isinstance(s["answer"], (int,float)):
                print(f"NON-NUMERIC answer {t}[{i}].gs[{j}]: {s['answer']}")
print("hint/numeric sweep done")

# verify gold[3] display and solution
g3 = pb["gold"][3]
print("gold[3] display:", g3["display"])
print("gold[3] solutions:", g3["solutions"])
