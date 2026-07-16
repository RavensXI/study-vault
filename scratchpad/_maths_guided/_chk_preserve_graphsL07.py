import json, io
pd=json.load(io.open("_CHK_graphsL07_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
# find entry
entry=None
if isinstance(dump,dict):
    if ID in dump: entry=dump[ID]
    else:
        for k,v in dump.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v; break
elif isinstance(dump,list):
    for v in dump:
        if v.get("id")==ID: entry=v; break
print("entry found:", entry is not None)
if entry:
    pre=entry.get("practice_data") if "practice_data" in entry else entry
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'SAME' if a==b else 'CHANGED'}")
    # bank display texts + solutions preserved? (problems may be edited, list them)
    for tier in ["bronze","silver","gold"]:
        pb_pre=pre.get("problem_bank",{}).get(tier,[])
        pb_now=pd.get("problem_bank",{}).get(tier,[])
        print(f"--- {tier}: pre {len(pb_pre)} now {len(pb_now)}")
        for i in range(max(len(pb_pre),len(pb_now))):
            dpre=pb_pre[i]["display"] if i<len(pb_pre) else "MISSING"
            dnow=pb_now[i]["display"] if i<len(pb_now) else "MISSING"
            spre=pb_pre[i].get("solutions") if i<len(pb_pre) else None
            snow=pb_now[i].get("solutions") if i<len(pb_now) else None
            flag="" if (dpre==dnow and spre==snow) else "  <== CHANGED"
            if flag:
                print(f"  [{i}] sol {spre}->{snow}{flag}")
                print(f"      pre: {dpre}")
                print(f"      now: {dnow}")
