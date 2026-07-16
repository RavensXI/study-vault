import json
pre=json.load(open('_pre_l06.json',encoding='utf-8'))
live=json.load(open('_live_l06.json',encoding='utf-8'))
for f in ['related_videos','topic_links','worked_examples']:
    same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, 'UNCHANGED' if same else 'CHANGED')
# Also check problem displays/solutions preserved vs pre (numbers)
print('--- pre problem_bank tiers ---')
for tier in ['bronze','silver','gold']:
    pb=pre['problem_bank'][tier]
    print(tier, len(pb))
    for i,p in enumerate(pb):
        print(' ',i,repr(p['display']),p['solutions'], p.get('input_type'))
