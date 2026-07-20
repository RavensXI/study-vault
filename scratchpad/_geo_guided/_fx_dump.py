import json, os
base=os.path.dirname(os.path.abspath(__file__))
pd=json.load(open(os.path.join(base,'_FX_L01_live.json'),encoding='utf-8'))
pb=pd['problem_bank']
def dump(tier, idx):
    p=pb[tier][idx]
    print('=== %s[%d] ==='%(tier,idx))
    print('display:', p.get('display'))
    print('input_type:', p.get('input_type'))
    print('options:', json.dumps(p.get('options'),ensure_ascii=False))
    print('solution:', json.dumps(p.get('solution'),ensure_ascii=False), 'solutions:', json.dumps(p.get('solutions'),ensure_ascii=False))
    print('chart:', json.dumps(p.get('chart'),ensure_ascii=False)[:1200])
    print('hint:', p.get('hint'))
    print('misconceptions:', json.dumps(p.get('misconceptions'),ensure_ascii=False,indent=1))
    print('guided_steps:', json.dumps(p.get('guided_steps'),ensure_ascii=False,indent=1))
    print()
for t,i in [('bronze',1),('silver',0),('silver',4),('bronze',7),('gold',2)]:
    dump(t,i)
