import json,io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
pd=json.load(open('_CHKgeoL07_live.json',encoding='utf-8'))
issues=[]
EMDASH='—'

def scan_em(s,path):
    if isinstance(s,str) and EMDASH in s:
        issues.append(f"EMDASH {path}: {s!r}")

# problem bank: last numeric guided box must equal solution for single_value
pb=pd['problem_bank']
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        path=f"{tier}[{i}]"
        it=p.get('input_type')
        sol=p.get('solutions')
        scan_em(p.get('display',''),path+'.display')
        scan_em(p.get('hint',''),path+'.hint')
        gs=p.get('guided_steps')
        if it=='single_value' and gs:
            boxes=[s for s in gs if 'answer' in s]
            last=boxes[-1]['answer'] if boxes else None
            # find the phase:substitute box and the box that lands the solution
            landed=[b['answer'] for b in boxes]
            if sol and sol[0] not in landed:
                issues.append(f"{path}: solution {sol[0]} not hit by any box {landed}")
            # boundary check
            phs=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
            if not phs:
                issues.append(f"{path}: no phase:substitute boundary")
            else:
                bidx=phs[0]
                before_boxes=[s for s in gs[:bidx] if 'answer' in s]
                atafter_boxes=[s for s in gs[bidx:] if 'answer' in s]
                if len(before_boxes)<1: issues.append(f"{path}: <1 box before boundary")
                if len(atafter_boxes)<2: issues.append(f"{path}: <2 boxes at/after boundary ({len(atafter_boxes)})")
        for mc in p.get('misconceptions',[]):
            scan_em(mc.get('message',''),path+'.mc.message')
            ex=mc.get('expect')
            if not (ex is None or isinstance(ex,(int,float))):
                issues.append(f"{path}: expect not number/null: {ex!r}")

# teach + opener boxes em-dash + say scan
g=pd['guided']
for tier,walk in g['teach'].items():
    scan_em(walk.get('display',''),f"teach.{tier}.display")
    for j,s in enumerate(walk['steps']):
        scan_em(s.get('pre',''),f"teach.{tier}[{j}].pre")
        scan_em(s.get('say',''),f"teach.{tier}[{j}].say")
        scan_em(s.get('done',''),f"teach.{tier}[{j}].done")
op=g['opener']
scan_em(op.get('display',''),'opener.display')
for j,s in enumerate(op['steps']):
    for k in ('pre','say','done'): scan_em(s.get(k,''),f"opener[{j}].{k}")

# tier_guides em-dash + budget
for tier,tg in pd['tier_guides'].items():
    for j,st in enumerate(tg['steps']): scan_em(st,f"tier_guides.{tier}.steps[{j}]")
    wc=sum(len(re.sub('<[^>]+>','',s).split()) for s in tg['steps'])
    if wc>115: issues.append(f"tier_guides.{tier}: {wc} words >115")

print("ISSUES:" if issues else "NO AUTOMATED ISSUES")
for x in issues: print(" -",x)
