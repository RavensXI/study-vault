import json,os,urllib.request
pd=json.load(open('_chk689_live.json',encoding='utf-8'))

print("=== COMPLETION BOUNDARIES (need >=1 box before, >=2 live boxes at/after phase) ===")
def boundary(steps,label):
    boxes=[j for j,s in enumerate(steps) if 'answer' in s]
    ph=[j for j,s in enumerate(steps) if s.get('phase')=='substitute']
    if not ph:
        # opener/teach walks don't need phase; only bank guided_steps do
        return
    p=ph[0]
    before=[b for b in boxes if b<p]
    after=[b for b in boxes if b>=p]
    if len(before)<1 or len(after)<2:
        print(f"  BOUNDARY ISSUE {label}: before={len(before)} after={len(after)}")
for t in ['bronze','silver','gold']:
    for i,pr in enumerate(pd['problem_bank'][t]):
        boundary(pr.get('guided_steps',[]),f'{t}[{i}]')
print("boundary scan done (issues above)")

print("\n=== PRESERVATION vs pre-dump ===")
try:
    pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
    # find canonical row
    cid='4ef45adc-b491-4025-9906-f541fa8a7a8f'
    row=None
    if isinstance(pre,dict):
        row=pre.get(cid)
        if row is None:
            for k,v in pre.items():
                if isinstance(v,dict) and v.get('id')==cid: row=v;break
    elif isinstance(pre,list):
        for v in pre:
            if v.get('id')==cid: row=v;break
    if row is None:
        print("  canonical id not found in pre-dump; keys sample:", list(pre)[:3] if isinstance(pre,dict) else 'list')
    else:
        ppd=row.get('practice_data',row)
        for f in ['worked_examples','related_videos','topic_links','exam_context','method_card']:
            same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
            print(f"  {f}: {'UNCHANGED' if same else 'CHANGED'}")
        # bank displays/solutions
        for t in ['bronze','silver','gold']:
            pb=ppd.get('problem_bank',{}).get(t,[])
            nb=pd['problem_bank'][t]
            for i in range(min(len(pb),len(nb))):
                if pb[i].get('solutions')!=nb[i].get('solutions'):
                    print(f"  SOLUTION CHANGED {t}[{i}]: {pb[i].get('solutions')} -> {nb[i].get('solutions')}")
                if pb[i].get('display')!=nb[i].get('display'):
                    print(f"  DISPLAY CHANGED {t}[{i}]")
            if len(pb)!=len(nb): print(f"  BANK SIZE {t}: {len(pb)} -> {len(nb)}")
except FileNotFoundError:
    print("  no _pre_dump_all.json found")
