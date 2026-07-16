import json
live=json.load(open('_maths_guided/_chk_L04_de190166.json',encoding='utf-8'))
pre=[x for x in json.load(open('_maths_guided/_pre_fanout_dump.json',encoding='utf-8')) if x['id']=='de190166-58bb-4edb-927f-1f2f3f3d8eb3'][0]['practice_data']

# method_card compare
print('method_card pre==live:', json.dumps(pre['method_card'],sort_keys=True)==json.dumps(live['method_card'],sort_keys=True))
print('pre mc title:',pre['method_card']['title'])
print('live mc title:',live['method_card']['title'])

# dup solutions within tier
for t in ['bronze','silver']:
    sols=[p['solutions'][0] for p in live['problem_bank'][t]]
    print(t,'solutions',sols,'dups' if len(set(sols))!=len(sols) else 'all-distinct')
# gold correct option letters
for j,p in enumerate(live['problem_bank']['gold']):
    opts=p['options']
    print('gold',j,'distinct-opts' if len(set(opts))==len(opts) else 'DUP-OPTS', 'sol',p['solutions'])

# tier_guides example answers verify
tg=live['tier_guides']
print('bronze tg example ans step:', tg['bronze']['example']['steps'][-1]['content'])
print('silver tg example ans step:', tg['silver']['example']['steps'][-1]['content'])
print('gold tg example ans step:', tg['gold']['example']['steps'][-1]['content'])
