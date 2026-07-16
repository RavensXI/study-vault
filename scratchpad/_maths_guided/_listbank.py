import json
pre=json.load(open('_pre_ratio_L01.json',encoding='utf-8'))
live=json.load(open('_live_ratio_L01.json',encoding='utf-8'))
for src,name in [(pre,'PRE'),(live,'LIVE')]:
    print("="*8,name)
    for tier in ['bronze','silver','gold']:
        print(f"-- {tier} ({len(src['problem_bank'][tier])})")
        for i,p in enumerate(src['problem_bank'][tier]):
            print(f"  [{i}] {p.get('input_type'):15} sol={p.get('solutions')} :: {p.get('display')}")
