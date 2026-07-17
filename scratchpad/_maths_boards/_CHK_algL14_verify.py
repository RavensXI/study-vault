import json, re

live = json.load(open("_CHK_algL14_live.json", encoding="utf-8"))
pd = live["practice_data"]

# ---- em dash scan (student-facing) ----
EM = "—"
def scan(obj, path):
    hits=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k == "note":   # internal exempt
                continue
            hits += scan(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            hits += scan(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EM in obj:
            hits.append(path)
    return hits
print("EM DASH hits:", scan(pd, "pd"))

# ---- preservation vs pre-dump ----
try:
    predump = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
    entry=None
    ID="f4814142-6434-44c9-9458-6b95f1e27ec6"
    if isinstance(predump, list):
        for e in predump:
            if e.get("id")==ID: entry=e; break
    elif isinstance(predump, dict):
        entry = predump.get(ID) or predump.get("lessons",{}).get(ID)
    if entry:
        pdp = entry.get("practice_data", entry)
        for f in ("related_videos","topic_links","worked_examples"):
            same = json.dumps(pdp.get(f),sort_keys=True)==json.dumps(pd.get(f),sort_keys=True)
            print(f"PRESERVE {f}: {'OK' if same else 'CHANGED'}")
            if not same:
                print("   pre :", json.dumps(pdp.get(f))[:300])
                print("   live:", json.dumps(pd.get(f))[:300])
    else:
        print("pre-dump entry NOT FOUND; keys sample:", (list(predump)[:3] if isinstance(predump,dict) else type(predump)))
except Exception as e:
    print("predump err:", e)

# ---- box numeric check ----
def check_boxes(steps, label):
    for i,s in enumerate(steps):
        if "answer" in s:
            a=s["answer"]
            if not isinstance(a,(int,float)):
                print(f"NON-NUMERIC {label}[{i}]: {a!r}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        for gs in (p.get("guided_steps") or []):
            pass
        check_boxes(p.get("guided_steps") or [], f"{tier}[{i}].guided_steps")
for t in ("bronze","silver","gold"):
    check_boxes(pd["guided"]["teach"][t]["steps"], f"teach.{t}")
check_boxes(pd["guided"]["opener"]["steps"], "opener")
print("box scan done")
