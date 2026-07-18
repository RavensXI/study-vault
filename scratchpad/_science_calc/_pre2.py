import json
live=json.load(open('_live_L03.json'))
raw=open('_pre_dump_all.json','r',encoding='utf-8',errors='replace').read()
pre=json.loads(raw)
cid="a20c4a08-3698-4cb8-9f8c-b8978c3f9060"
entry=None
if isinstance(pre,list):
    for v in pre:
        if v.get('id')==cid: entry=v;break
elif isinstance(pre,dict):
    entry=pre.get(cid)
    if entry is None:
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get('id')==cid or k==cid): entry=v;break
print("found",entry is not None, "container", type(pre))
if entry:
    pd=entry.get('practice_data',entry)
    for f in ['related_videos','topic_links','worked_examples','exam_context','method_card']:
        a=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "identical:", a==b)
    # count bank problems & solutions preserved
    for tier in ['bronze','silver','gold']:
        pp=pd['problem_bank'][tier]; lp=live['problem_bank'][tier]
        print(tier, "n_pre",len(pp),"n_live",len(lp),
              "sols_same", [x['solutions'] for x in pp]==[x['solutions'] for x in lp],
              "displays_same",[x['display'] for x in pp]==[x['display'] for x in lp])
