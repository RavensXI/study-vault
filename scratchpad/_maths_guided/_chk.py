import json
live=json.load(open('_live_L03.json',encoding='utf-8'))
dump=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
e=[x for x in dump if x.get('id')=='d168ac22-370f-4c9f-a647-85febc0e8213'][0]
pd=e['practice_data']
for f in ['related_videos','topic_links','worked_examples','method_card']:
    same = pd.get(f)==live.get(f)
    print(f, 'EQUAL' if same else 'DIFFERENT')
    if not same:
        print('  PRE :', json.dumps(pd.get(f))[:500])
        print('  LIVE:', json.dumps(live.get(f))[:500])
for tier in ['bronze','silver','gold']:
    pre=pd['problem_bank'][tier]; lv=live['problem_bank'][tier]
    print(tier,'count pre',len(pre),'live',len(lv))
    for i,(a,b) in enumerate(zip(pre,lv)):
        for k in ['display','solutions','input_type','calculator']:
            if a.get(k)!=b.get(k):
                print('  %s[%d].%s: PRE=%r LIVE=%r'%(tier,i,k,a.get(k),b.get(k)))
