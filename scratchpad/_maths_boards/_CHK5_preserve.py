import json
ID="acf8619c-92bc-4778-b29c-dd0cb973f59c"
dump=json.load(open('_pre_dump_maths-ocr.json',encoding='utf-8'))
pre=None
for r in dump:
    if r['id']==ID:
        pre=r['practice_data']; break
print("found pre:", pre is not None, "title:", [r['title'] for r in dump if r['id']==ID])
live=json.load(open('_CHK5_live.json',encoding='utf-8'))
pre=pre or {}
# preservation-critical fields
for f in ['related_videos','topic_links','worked_examples']:
    a=json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if a==b else "CHANGED")
    if a!=b:
        print("  PRE :",a[:400])
        print("  LIVE:",b[:400])
print("pre keys:",sorted(pre.keys()))
print("live keys:",sorted(live.keys()))
# check displays/solutions preserved for problems
def probs(pd):
    out={}
    pb=pd.get('problem_bank',{})
    for t in ['bronze','silver','gold']:
        for i,p in enumerate(pb.get(t,[])):
            out[f"{t}[{i}]"]=(p.get('display'),tuple(p.get('solutions') or []),p.get('input_type'))
    return out
pp=probs(pre); lp=probs(live)
print("--- problem display/solution changes ---")
for k in sorted(set(pp)|set(lp)):
    if pp.get(k)!=lp.get(k):
        print(k)
        print("  PRE :",pp.get(k))
        print("  LIVE:",lp.get(k))
