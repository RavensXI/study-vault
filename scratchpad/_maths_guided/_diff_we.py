import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
pre=json.load(open('_pre_l06.json',encoding='utf-8'))
live=json.load(open('_live_l06.json',encoding='utf-8'))
print('PRE == LIVE worked_examples:', pre['worked_examples']==live['worked_examples'])
# show which differ
for i,(a,b) in enumerate(zip(pre['worked_examples'],live['worked_examples'])):
    print(i, 'same' if a==b else 'DIFF', '| pre q=',a.get('question'),'| live q=',b.get('question'))
print('lens', len(pre['worked_examples']), len(live['worked_examples']))
