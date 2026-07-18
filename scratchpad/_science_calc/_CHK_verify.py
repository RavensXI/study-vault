import json, math, re
pd=json.load(open('_chk_live.json'))
pb=pd['problem_bank']
issues=[]

def within(v, target, acc):
    return abs(v-target)<= (acc if acc is not None else 0.005)

# board-neutrality scan across all student-facing strings
blob=json.dumps(pd)
for bad in ['AQA','Edexcel','OCR','Eduqas','WJEC','equation sheet','must memorise','on your sheet','memorize']:
    if bad.lower() in blob.lower():
        # find context
        idx=blob.lower().find(bad.lower())
        issues.append(f"BOARD/SHEET term '{bad}': ...{blob[idx-40:idx+40]}...")

# em dash scan
if '—' in blob:
    issues.append("EM DASH present somewhere")

# per-problem numeric check of expects outside accept window & solution
def check_expect(tier,i,prob):
    sol=prob.get('solutions',[None])[0]
    acc=prob.get('accept')
    for m in prob.get('misconceptions',[]):
        e=m.get('expect')
        if e is None: continue
        # dead if inside accept window of solution
        if isinstance(sol,(int,float)) and within(e,sol,acc):
            issues.append(f"{tier}[{i}] DEAD expect {e} inside accept window of sol {sol} (accept {acc}) pattern={m['pattern']}")

for tier in ['bronze','silver','gold']:
    for i,prob in enumerate(pb[tier]):
        check_expect(tier,i,prob)

print("ISSUES:",len(issues))
for x in issues: print(" -",x)
