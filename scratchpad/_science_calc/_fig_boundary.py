import json,re
d=json.load(open('_live_81a530c1.json',encoding='utf-8'))
pb=d['problem_bank']
issues=[]

# Completion boundary rule: >=1 box before first phase:substitute, >=2 boxes at/after
def boundary(tier):
    for i,p in enumerate(pb[tier]):
        gs=p.get('guided_steps',[])
        boxes=[(j,s) for j,s in enumerate(gs) if 'answer' in s]
        first_ph=None
        for j,s in enumerate(gs):
            if s.get('phase')=='substitute':
                first_ph=j; break
        if first_ph is None:
            issues.append(f"{tier}[{i}] no phase:substitute boundary"); continue
        before=[j for j,s in boxes if j<first_ph]
        after=[j for j,s in boxes if j>=first_ph]
        if len(before)<1: issues.append(f"{tier}[{i}] <1 box before boundary")
        if len(after)<2: issues.append(f"{tier}[{i}] <2 live boxes after boundary ({len(after)})")

for t in ['bronze','silver','gold']: boundary(t)

# SVG figure numbers must appear in problem display
def figs(tier):
    for i,p in enumerate(pb[tier]):
        q=p.get('question','')
        disp=p['display']
        if '<svg' not in q: 
            issues.append(f"{tier}[{i}] no svg figure"); continue
        # extract text labels in svg
        texts=re.findall(r'>([^<>]*?)</text>',q)
        aria=re.findall(r'aria-label=\"([^\"]*)\"',q)
        # numeric tokens in labels
        labelnums=set()
        for t2 in texts:
            for n in re.findall(r'\d+\.?\d*',t2):
                labelnums.add(n)
        dispnums=set(re.findall(r'\d+\.?\d*',disp))
        # each label number should be traceable in display (allowing 0.10 vs 0.1)
        for ln in labelnums:
            variants={ln, ln.rstrip('0').rstrip('.') if '.' in ln else ln, ln+'0'}
            if not (variants & dispnums) and ln not in ('2',) :
                # check normalized
                found=False
                for dn in dispnums:
                    try:
                        if abs(float(dn)-float(ln))<1e-9: found=True;break
                    except: pass
                if not found:
                    issues.append(f"{tier}[{i}] svg label '{ln}' not in display: {disp[:60]}")

for t in ['bronze','silver','gold']: figs(t)

# equation_hint preserved on bronze/silver bank problems (bank recall toggle)
for t in ['bronze','silver']:
    for i,p in enumerate(pb[t]):
        if 'equation_hint' not in p:
            issues.append(f"{t}[{i}] missing equation_hint")

print("FIG/BOUNDARY ISSUES:" if issues else "FIG+BOUNDARY CLEAN")
for x in issues: print(" -",x)
