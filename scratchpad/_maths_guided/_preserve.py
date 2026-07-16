import json
dump=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
LID="4e2bb5ad-e75a-48be-951a-0e8b8db75296"
# find entry
def find(o):
    if isinstance(o,dict):
        if o.get('id')==LID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
e=find(dump)
if e is None:
    print("structure keys:", list(dump.keys()) if isinstance(dump,dict) else type(dump))
    # maybe keyed by id
    if isinstance(dump,dict) and LID in dump:
        e={'practice_data':dump[LID]}
        print("found by key")
else:
    print("found by id scan")
pre=e.get('practice_data') if 'practice_data' in e else e
live=json.load(open('_live_L06.json',encoding='utf-8'))
for f in ['related_videos','topic_links','worked_examples']:
    print(f, "SAME" if pre.get(f)==live.get(f) else "DIFF")
    if pre.get(f)!=live.get(f):
        print("  PRE:",json.dumps(pre.get(f))[:300])
        print("  LIVE:",json.dumps(live.get(f))[:300])
# also check problem displays/solutions changed
print("\n-- bank display/solution diffs (pre vs live) --")
for tier in ['bronze','silver','gold']:
    pb=pre.get('problem_bank',{}).get(tier,[])
    lb=live.get('problem_bank',{}).get(tier,[])
    for i in range(max(len(pb),len(lb))):
        pd=pb[i] if i<len(pb) else {}
        ld=lb[i] if i<len(lb) else {}
        if pd.get('display')!=ld.get('display') or pd.get('solutions')!=ld.get('solutions'):
            print(f"{tier}[{i}] display/sol changed")
            print("  PRE:", pd.get('display'), pd.get('solutions'))
            print("  LIVE:", ld.get('display'), ld.get('solutions'))
