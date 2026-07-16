import json
live=json.load(open('_live_geometry-L07.json',encoding='utf-8'))
pre=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
LID="aee11210-c33f-4e61-a25e-1ef101e95ab3"
entry=None
def find(o):
    global entry
    if isinstance(o,dict):
        if o.get('id')==LID: entry=o
        for v in o.values(): find(v)
    elif isinstance(o,list):
        for v in o: find(v)
find(pre)
pd_pre=entry['practice_data']
if isinstance(pd_pre,str): pd_pre=json.loads(pd_pre)
print("PRE top keys:", sorted(pd_pre.keys()))
print("LIVE top keys:", sorted(live.keys()))
# compare problem displays/solutions
for tier in ['bronze','silver','gold']:
    pb_pre=pd_pre.get('problem_bank',{}).get(tier,[])
    pb_live=live['problem_bank'][tier]
    print(f"--- {tier}: pre {len(pb_pre)} live {len(pb_live)}")
    for i,(a,b) in enumerate(zip(pb_pre,pb_live)):
        if a.get('display')!=b.get('display'):
            print(f"  [{i}] DISPLAY CHANGED\n     pre : {a.get('display')}\n     live: {b.get('display')}")
        if a.get('solutions')!=b.get('solutions'):
            print(f"  [{i}] SOL CHANGED pre {a.get('solutions')} live {b.get('solutions')}")
# method_card pre vs live word count
import re
mc=live['method_card']['content']
words=len(re.sub('<[^>]+>',' ',mc).split())
print("method_card content words:", words)
