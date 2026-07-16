import json,io
live=json.load(io.open('_live_geometry_L06.json',encoding='utf-8'))[0]['practice_data']
pre=json.load(io.open('_pre_fanout_dump.json',encoding='utf-8'))
row=[r for r in pre if r['id']=='4e2bb5ad-e75a-48be-951a-0e8b8db75296'][0]
pd=row['practice_data']
print("PRE keys:", sorted(pd.keys()))
print("LIVE keys:", sorted(live.keys()))
for f in ['related_videos','topic_links','worked_examples']:
    same = pd.get(f)==live.get(f)
    print(f, "PRESERVED:" , same)
    if not same:
        print("  PRE:", json.dumps(pd.get(f),ensure_ascii=False)[:300])
        print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:300])
# check pre problem displays/solutions vs live to see if numbers changed
def bank(pd): return pd.get('problem_bank',{})
for tier in ['bronze','silver','gold']:
    pb=bank(pd).get(tier,[]); lb=bank(live).get(tier,[])
    print(f"--- {tier}: pre {len(pb)} live {len(lb)}")
    for i,(a,b) in enumerate(zip(pb,lb)):
        if a.get('display')!=b.get('display') or a.get('solutions')!=b.get('solutions') or a.get('input_type')!=b.get('input_type'):
            print(f"  [{i}] DISPLAY/SOL CHANGED")
            print("     pre disp:",a.get('display'),"sol",a.get('solutions'))
            print("     liv disp:",b.get('display'),"sol",b.get('solutions'))
