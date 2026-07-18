import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
CID='5473906a-ccfa-43f0-8230-5b9171181f19'
prepd=next(r for r in pre if r.get('id')==CID)['pd']
live=json.load(open('_live_L05.json',encoding='utf-8'))['canonical']

for f in ['related_videos','topic_links','exam_context','worked_examples']:
    same = json.dumps(prepd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")

# bank display/solutions/accept/unit preserved?
for tier in ['bronze','silver','gold']:
    for i,(a,b) in enumerate(zip(prepd['problem_bank'][tier], live['problem_bank'][tier])):
        for k in ['display','solutions','accept','unit','input_type','calculator','higher_only','options']:
            if a.get(k)!=b.get(k):
                print(f"  {tier}[{i}].{k}: PRE={a.get(k)!r} LIVE={b.get(k)!r}")
print("bank core fields compared")
