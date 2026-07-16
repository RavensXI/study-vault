import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
pre=json.load(open('_pre_l06.json',encoding='utf-8'))
live=json.load(open('_live_l06.json',encoding='utf-8'))
for i,(a,b) in enumerate(zip(pre['worked_examples'],live['worked_examples'])):
    if a!=b:
        print('=== item',i,'===')
        print('PRE :',json.dumps(a,ensure_ascii=False))
        print('LIVE:',json.dumps(b,ensure_ascii=False))
