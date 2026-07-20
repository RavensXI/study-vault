import json
pre=json.load(open('_z_L09_pre.json',encoding='utf-8'))['pd']
live=json.load(open('_CHK_L09_live.json',encoding='utf-8'))
for tier in ['bronze','silver','gold']:
    a=pre['problem_bank'][tier]; b=live['problem_bank'][tier]
    print(f"== {tier}: pre {len(a)} live {len(b)}")
    for i in range(max(len(a),len(b))):
        pa=a[i] if i<len(a) else {}
        pb=b[i] if i<len(b) else {}
        for f in ['display','solutions','options','image','chart','ruler','input_type','calculator']:
            if pa.get(f)!=pb.get(f):
                print(f"  {tier}[{i}].{f}\n    PRE : {json.dumps(pa.get(f),ensure_ascii=False)}\n    LIVE: {json.dumps(pb.get(f),ensure_ascii=False)}")
for f in ['related_videos','topic_links','worked_examples']:
    print(f, 'SAME' if pre.get(f)==live.get(f) else 'CHANGED')
    if pre.get(f)!=live.get(f):
        print('  PRE ',json.dumps(pre.get(f),ensure_ascii=False)[:600])
        print('  LIVE',json.dumps(live.get(f),ensure_ascii=False)[:600])
print('method_card pre:',json.dumps(pre.get('method_card'),ensure_ascii=False)[:800])
print('pre top keys',list(pre.keys()))
print('pre tier_guides?',bool(pre.get('tier_guides')))
