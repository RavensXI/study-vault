# -*- coding: utf-8 -*-
import json,re
pd=json.load(open('_live_canonical.json',encoding='utf-8'))
issues=[]

# --- board neutrality on whole object ---
blob=json.dumps(pd,ensure_ascii=False)
for term in ['AQA','Edexcel','OCR','Eduqas','WJEC','equation sheet','formula sheet','memorise','must remember','on your sheet','given to you']:
    if re.search(term,blob,re.IGNORECASE):
        issues.append(f"BOARD/NEUTRALITY term found: '{term}'")
print("Board-neutrality: ", "clean" if not any('BOARD' in i for i in issues) else "FLAGS")

# --- em dash scan in student-facing strings (skip internal 'note') ---
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            walk(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if '—' in o: issues.append(f"EM DASH at {path}: {o[:60]}")
walk(pd)
print("Em-dash scan done")

# --- recompute every guided_steps / teach / opener box independently ---
# We just re-evaluate each 'pre' arithmetic expression where possible by trusting stated ops.
# Instead, hard-check known walks:
def box(arr): return [st for st in arr if 'answer' in st]

# helper to check a numeric list matches
def check(name, arr, expected):
    boxes=box(arr)
    got=[b['answer'] for b in boxes]
    if got!=expected:
        issues.append(f"{name} boxes {got} != expected {expected}")
    print(f"{name}: {got}  {'OK' if got==expected else 'MISMATCH exp '+str(expected)}")

G=pd['guided']
check('opener',G['opener']['steps'],[45,90])
check('teach.bronze',G['teach']['bronze']['steps'],[3600,35280,70560,2])
check('teach.silver',G['teach']['silver']['steps'],[25625,251125,352125,101000])
check('teach.gold',G['teach']['gold']['steps'],[200,1960,1470,490])

pb=pd['problem_bank']
check('bronze[0]',pb['bronze'][0]['guided_steps'],[2000,19600,2])
check('bronze[1]',pb['bronze'][1]['guided_steps'],[5000,49000,5])
check('bronze[2]',pb['bronze'][2]['guided_steps'],[0.001,1,9.8,0.001])
check('bronze[3]',pb['bronze'][3]['guided_steps'],[50000,490000,591000,490000])
check('bronze[4]',pb['bronze'][4]['guided_steps'],[10045,19.91,20])
check('silver[0]',pb['silver'][0]['guided_steps'],[41000,401800,502800,401800])
check('silver[1]',pb['silver'][1]['guided_steps'],[0.5,4.9,2.94,1.96])
check('silver[2]',pb['silver'][2]['guided_steps'],[0.00392,1000,3.92])
check('silver[3]',pb['silver'][3]['guided_steps'],[0.002,25000,50])
check('silver[4]',pb['silver'][4]['guided_steps'],[0.205,2.009,1.764,0.245])
check('gold[0]',pb['gold'][0]['guided_steps'],[11275000,110495000,110596000,101000])
check('gold[1]',pb['gold'][1]['guided_steps'],[5.125,50.225,29.4,20.825])
check('gold[2]',pb['gold'][2]['guided_steps'],[60,3,588000,588000])
check('gold[3]',pb['gold'][3]['guided_steps'],[8.16,79.968,49,1.632])

# --- completion boundary: >=1 before phase substitute, >=2 live boxes at/after ---
print("\n=== completion boundary ===")
for tier in ['bronze','silver','gold']:
    for i,prob in enumerate(pb[tier]):
        gs=prob.get('guided_steps')
        if not gs: continue
        boxes=[st for st in gs if 'answer' in st]
        # find first phase substitute among boxes
        bi=None
        for j,st in enumerate(boxes):
            if st.get('phase')=='substitute': bi=j;break
        before=bi
        after=len(boxes)-bi if bi is not None else 0
        ok = bi is not None and before>=1 and after>=2
        if not ok: issues.append(f"{tier}[{i}] boundary before={before} after={after}")
        print(f"{tier}[{i}] boxes={len(boxes)} boundary@{bi} before={before} after={after} {'OK' if ok else 'CHECK'}")

print("\nISSUES:")
for x in issues: print(" -",x)
if not issues: print(" none")
