import json
live=json.load(open('_live_L03.json'))
raw=open('_pre_dump_all.json','r',encoding='utf-8',errors='replace').read()
pre=json.loads(raw)
cid="a20c4a08-3698-4cb8-9f8c-b8978c3f9060"
entry=[v for v in pre if v.get('id')==cid][0]
pd=entry['pd']
print("pre pd keys:",list(pd.keys()))
for f in ['related_videos','topic_links','worked_examples','exam_context','method_card']:
    a=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f,"identical:",a==b)
for tier in ['bronze','silver','gold']:
    pp=pd['problem_bank'][tier]; lp=live['problem_bank'][tier]
    print(tier,"n_pre",len(pp),"n_live",len(lp),
          "sols_same",[x['solutions'] for x in pp]==[x['solutions'] for x in lp],
          "disp_same",[x['display'] for x in pp]==[x['display'] for x in lp],
          "units_same",[x.get('unit') for x in pp]==[x.get('unit') for x in lp],
          "accept_same",[x.get('accept') for x in pp]==[x.get('accept') for x in lp])
