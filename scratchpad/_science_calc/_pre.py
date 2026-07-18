import json
live=json.load(open('_live_L03.json'))
try:
    pre=json.load(open('_pre_dump_all.json'))
except Exception as ex:
    print("no predump:",ex); pre=None
if pre is not None:
    # find canonical id entry
    cid="a20c4a08-3698-4cb8-9f8c-b8978c3f9060"
    entry=None
    if isinstance(pre,dict):
        entry=pre.get(cid)
        if entry is None:
            for k,v in pre.items():
                if isinstance(v,dict) and v.get('id')==cid: entry=v;break
    print("predump type",type(pre), "keys sample", list(pre.keys())[:3] if isinstance(pre,dict) else len(pre))
    print("entry found:", entry is not None)
    if entry is not None:
        pd = entry.get('practice_data', entry)
        for f in ['related_videos','topic_links','worked_examples','exam_context']:
            print(f, "identical:", json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False))
# unit/accept present
for tier,probs in live['problem_bank'].items():
    if not isinstance(probs,list): continue
    for pi,p in enumerate(probs):
        print(f"{tier}[{pi}] unit={p.get('unit')} accept={p.get('accept','-')} higher_only={p.get('higher_only','-')}")
