import json,sys
sys.stdout.reconfigure(encoding='utf-8')
pre=json.load(open('_CHK_L03_pre.json',encoding='utf-8'))['pd']
live=json.load(open('_CHK_L03_live.json',encoding='utf-8'))
print('PRE top keys',sorted(pre.keys()))
print('LIVE top keys',sorted(live.keys()))
for k in ['related_videos','topic_links','worked_examples']:
    print(k,'identical:',pre.get(k)==live.get(k))
print('method_card PRE:',json.dumps(pre.get('method_card'),ensure_ascii=False)[:1500])
print('method_card LIVE:',json.dumps(live.get('method_card'),ensure_ascii=False)[:1500])
for t in ['bronze','silver','gold']:
    P=pre['problem_bank'][t]; L=live['problem_bank'][t]
    print('===',t,len(P),len(L))
    for i,(a,b) in enumerate(zip(P,L)):
        if a.get('display')!=b.get('display'):
            print(f' {t}[{i}] DISPLAY CHANGED\n   PRE : {a.get("display")}\n   LIVE: {b.get("display")}')
        if a.get('solutions')!=b.get('solutions'):
            print(f' {t}[{i}] SOLUTIONS {a.get("solutions")} -> {b.get("solutions")}')
        if a.get('options')!=b.get('options'):
            print(f' {t}[{i}] OPTIONS\n   PRE : {a.get("options")}\n   LIVE: {b.get("options")}')
        if json.dumps(a.get('chart'),sort_keys=True)!=json.dumps(b.get('chart'),sort_keys=True):
            print(f' {t}[{i}] CHART CHANGED')
            print('   PRE :',json.dumps(a.get('chart'),ensure_ascii=False)[:600])
            print('   LIVE:',json.dumps(b.get('chart'),ensure_ascii=False)[:600])
        for k in ('image','ruler','input_type','calculator'):
            if a.get(k)!=b.get(k): print(f' {t}[{i}] {k}: {a.get(k)} -> {b.get(k)}')
        pk=set(a.keys())-set(b.keys())
        if pk: print(f' {t}[{i}] DROPPED KEYS',pk)
        print(f'   {t}[{i}] pre-misc:',json.dumps(a.get('misconceptions'),ensure_ascii=False)[:300])
