import json
LID="65e7a745-9820-431a-8b99-d96cd7514bf3"
live=json.load(open('_live_ps_L03.json',encoding='utf-8'))[0]['practice_data']
pre=json.load(open('_pre_dump_maths-ocr.json',encoding='utf-8'))
entry=None
for r in pre:
    if r.get('id')==LID:
        entry=r; break
print("found:", entry is not None, "| title:", entry.get('title') if entry else None)
pd=entry['practice_data']
print("pre keys:", sorted(pd.keys()))
print("live keys:", sorted(live.keys()))
# Preservation-critical fields
for f in ['related_videos','topic_links','worked_examples']:
    a=pd.get(f,'<<absent>>'); b=live.get(f,'<<absent>>')
    same = json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)
    print(f"\n[{f}] identical={same}")
    if not same:
        print("  PRE :", json.dumps(a,ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(b,ensure_ascii=False)[:400])
# count pre problems per tier
prpb=pd.get('problem_bank',{})
for t in ['bronze','silver','gold']:
    pc=len(prpb.get(t,[])); lc=len(live['problem_bank'].get(t,[]))
    print(f"problems {t}: pre={pc} live={lc}")
