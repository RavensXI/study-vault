import json, io
pd=json.load(io.open("_CHK_numL04_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
# find pre entry
entry=None
if isinstance(dump,dict):
    for k,v in dump.items():
        if isinstance(v,dict) and v.get("id")=="007f6c38-d280-4dd8-801d-5bb62c612eb2":
            entry=v; break
    if entry is None and "007f6c38-d280-4dd8-801d-5bb62c612eb2" in dump:
        entry=dump["007f6c38-d280-4dd8-801d-5bb62c612eb2"]
if entry is None and isinstance(dump,list):
    for v in dump:
        if v.get("id")=="007f6c38-d280-4dd8-801d-5bb62c612eb2":
            entry=v; break
print("entry found:", entry is not None)
if entry:
    print("entry keys:", list(entry.keys()))
    pre=entry.get("practice_data") or entry
    for f in ("related_videos","topic_links","worked_examples"):
        same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE:", json.dumps(pre.get(f),ensure_ascii=False)[:400])
            print("  NOW:", json.dumps(pd.get(f),ensure_ascii=False)[:400])
    # also list pre problem_bank solutions for cross-check
    print("\nPRE bank tiers:", {t:len(pre.get("problem_bank",{}).get(t,[])) for t in ("bronze","silver","gold")})
    print("NOW bank tiers:", {t:len(pd["problem_bank"][t]) for t in ("bronze","silver","gold")})
    for t in ("bronze","silver","gold"):
        pb=pre.get("problem_bank",{}).get(t,[])
        for i,p in enumerate(pb):
            nd=pd["problem_bank"][t][i]
            if p.get("display")!=nd.get("display") or p.get("solutions")!=nd.get("solutions"):
                print(f"  {t}[{i}] DISPLAY/SOL CHANGE")
                print(f"    pre disp: {p.get('display')} sol {p.get('solutions')}")
                print(f"    now disp: {nd.get('display')} sol {nd.get('solutions')}")
