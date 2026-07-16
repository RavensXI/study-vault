import json
live = json.load(open("_CHK_L10_live.json", encoding="utf-8"))

emdash_hits=[]
nonnum_boxes=[]

def walk(obj, path, in_note=False):
    if isinstance(obj, dict):
        for k,v in obj.items():
            note = in_note or (k=="note")
            if isinstance(v,str) and "—" in v and not note:
                emdash_hits.append(f"{path}.{k}")
            # numeric box answer check
            if k=="answer":
                if not isinstance(v,(int,float)):
                    nonnum_boxes.append(f"{path}.answer = {v!r}")
            walk(v, f"{path}.{k}", note)
    elif isinstance(obj, list):
        for i,x in enumerate(obj):
            walk(x, f"{path}[{i}]", in_note)

walk(live, "root")
print("EM DASH hits (student-facing):", emdash_hits or "NONE")
print("Non-numeric answer boxes:", nonnum_boxes or "NONE")

# hints plain text (no LaTeX \( or < tags) on problem-level hint
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(live["problem_bank"][tier]):
        h=p.get("hint","")
        if "\(" in h or "<" in h:
            print(f"hint LaTeX/html {tier}[{i}]: {h}")
