import json
live = json.load(open("_CHKR_L05_live.json", encoding="utf-8"))
pd = json.load(open("_CHKR_L05_pd.json", encoding="utf-8"))

# 1. Em dash sweep in student-facing strings (exclude 'note' keys)
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note":  # internal exempt
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            print("DASH:", path, "->", repr(o))

print("== em/en dash sweep (excluding note) ==")
walk(live)
print("== done ==")

# 2. Preservation: compare preserved fields
print("\n== preservation vs pre-dump ==")
for f in ["related_videos","topic_links","worked_examples"]:
    a=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "SAME" if a==b else "CHANGED")

# 3. problem_bank display/solutions diff (were problems altered?)
print("\n== problem_bank display+solutions diff ==")
for tier in ["bronze","silver","gold"]:
    old=pd["problem_bank"].get(tier,[])
    new=live["problem_bank"].get(tier,[])
    print(f"-- {tier}: old {len(old)} new {len(new)}")
    for i in range(max(len(old),len(new))):
        od = old[i]["display"] if i<len(old) else None
        nd = new[i]["display"] if i<len(new) else None
        os_ = old[i].get("solutions") if i<len(old) else None
        ns = new[i].get("solutions") if i<len(new) else None
        if od!=nd:
            print(f"  [{i}] DISPLAY old={od!r}\n         new={nd!r}")
        if os_!=ns:
            print(f"  [{i}] SOLUTIONS old={os_} new={ns}")
