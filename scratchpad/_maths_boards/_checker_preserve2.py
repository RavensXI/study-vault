import json
ID="063c867c-7ba6-4879-9747-c3546382aaf2"
pre=json.load(open('_pre_dump_maths-aqa.json',encoding='utf-8'))
entry=[v for v in pre if v.get('id')==ID][0]
ppd=entry['practice_data']
live=json.load(open('_live_graphs-L07.json',encoding='utf-8'))['practice_data']
for f in ['related_videos','topic_links','worked_examples']:
    a=json.dumps(ppd.get(f),ensure_ascii=False,sort_keys=True)
    b=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
    print(f, "SAME" if a==b else "DIFF")
    if a!=b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])
print("pre keys:", sorted(ppd.keys()))
print("live keys:", sorted(live.keys()))
