import json
ID="7e5e6d1a-aa08-4fbf-8094-760926f7e56c"
pre=json.load(open('_pre_dump_maths-eduqas.json',encoding='utf-8'))
row=[r for r in pre if r.get('id')==ID]
print("found in predump:", len(row))
p=row[0]['practice_data'] if row else {}
live=json.load(open('_CHK_algL01_live.json',encoding='utf-8'))['practice_data']
print("pre keys:", sorted(p.keys()))
print("live keys:", sorted(live.keys()))
for f in ['related_videos','topic_links','worked_examples','method_card']:
    same = json.dumps(p.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if same else "CHANGED")
# problem bank displays/options/solutions preservation
def bank(pd):
    out={}
    pb=pd.get('problem_bank',{})
    for t in ['bronze','silver','gold']:
        out[t]=[(x.get('display'),tuple(x.get('options',[])),tuple(x.get('solutions',[]))) for x in pb.get(t,[])]
    return out
pb_pre=bank(p); pb_live=bank(live)
for t in ['bronze','silver','gold']:
    print("bank",t,"len pre/live",len(pb_pre.get(t,[])),len(pb_live.get(t,[])))
    for i,(a,b) in enumerate(zip(pb_pre.get(t,[]),pb_live.get(t,[]))):
        if a!=b:
            print("  DIFF",t,i)
            print("   pre :",a)
            print("   live:",b)
