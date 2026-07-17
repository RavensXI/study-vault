import json, re

live = json.load(open("_CHK_rp03_live.json", encoding="utf-8"))["practice_data"]
ID = "689bc7ff-0d4c-4f20-a83c-9476935f2ac9"

pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# find entry
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id")==ID:
            entry = r; break
elif isinstance(pre, dict):
    entry = pre.get(ID)
    if entry is None and "practice_data" in pre:
        entry = pre
print("pre entry found:", entry is not None)
if entry:
    ppd = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(ppd.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"{f}: {'SAME' if a==b else 'DIFFERENT'}")
        if a!=b:
            print("   PRE :", a[:400])
            print("   LIVE:", b[:400])
    print("pre keys:", sorted(ppd.keys()))
    print("live keys:", sorted(live.keys()))

# ---- style scan: em dashes in student-facing strings ----
print("\n=== em dash scan ===")
emcount = 0
def scan(obj, path):
    global emcount
    if isinstance(obj, str):
        if "note" in path.split("."):
            return
        if "—" in obj:
            emcount += 1
            print("EM DASH at", path, ":", obj[:80])
    elif isinstance(obj, dict):
        for k,v in obj.items():
            scan(v, path+"."+k)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan(v, f"{path}[{i}]")
scan(live, "root")
print("em dashes:", emcount)

# ---- HTML entities in plain-text-ish fields ----
print("\n=== html entity scan (student text) ===")
entcount=0
def scan2(obj, path):
    global entcount
    if isinstance(obj, str):
        for ent in ["&rsquo;","&amp;","&lt;","&gt;","&quot;","&nbsp;","&mdash;","&ndash;"]:
            if ent in obj:
                entcount+=1; print("ENTITY", ent, "at", path)
    elif isinstance(obj, dict):
        for k,v in obj.items(): scan2(v,path+"."+k)
    elif isinstance(obj, list):
        for i,v in enumerate(obj): scan2(v,f"{path}[{i}]")
scan2(live,"root")
print("entities:", entcount)

# ---- tier_guides word budget (<=115 per card steps) ----
print("\n=== tier guide word budgets ===")
import re as _re
for tier, g in live["tier_guides"].items():
    words = sum(len(_re.sub(r'<[^>]+>',' ',s).split()) for s in g["steps"])
    print(f"{tier}: {words} words (limit 115)")

# ---- numeric box check ----
print("\n=== non-numeric box scan ===")
def check_numeric(steps, label):
    for i,s in enumerate(steps):
        if "answer" in s and not isinstance(s["answer"], (int,float)):
            print("NON-NUMERIC", label, i, s["answer"])
for t,g in live["guided"]["teach"].items():
    check_numeric(g["steps"], "teach."+t)
check_numeric(live["guided"]["opener"]["steps"], "opener")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        check_numeric(p.get("guided_steps",[]), f"{tier}[{i}]")
print("done")
