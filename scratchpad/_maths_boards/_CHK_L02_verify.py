import json, re
from fractions import Fraction as F

pd=json.load(open("_CHK_L02_livefresh.json",encoding="utf-8"))["practice_data"]
errors=[]

# helper: parse a display like \frac{a}{b} OP \frac{c}{d} ... and mixed numbers, evaluate exactly
def frags(disp):
    # extract mixed numbers  N\frac{a}{b}
    return disp

# Manual fresh-solve of each problem's expected simplified value
def val(t):
    # returns Fraction from solutions list
    if len(t)==1: return F(t[0])
    return F(t[0],t[1])

# Fresh solve each by encoding the display arithmetic explicitly
solve={
 # gold
 ('gold',0): F(2,3)+F(3,4)-F(1,6),
 ('gold',1): F(5,2)*F(8,5),
 ('gold',2): F(13,4)-F(5,3),
 ('gold',3): F(3,8)/F(9,16),
 ('gold',4): F(5,6)*F(3,10)+F(1,4),
 # bronze
 ('bronze',0): F(1,4)+F(1,3),
 ('bronze',1): F(3,5)+F(1,5),
 ('bronze',2): F(5,6)-F(1,3),
 ('bronze',3): F(2,7)+F(3,7),
 ('bronze',4): F(1,2)*F(3,4),
 ('bronze',5): F(7,8)-F(1,8),
 ('bronze',6): F(2,5)*F(5,6),
 ('bronze',7): F(1,2)+F(1,6),
 # silver
 ('silver',0): F(2,3)+F(5,8),
 ('silver',1): F(3,4)-F(2,5),
 ('silver',2): F(3,5)*F(10,9),
 ('silver',3): F(4,5)/F(2,3),
 ('silver',4): F(4,3)+F(2,5),
 ('silver',5): F(5,6)/F(5,12),
 ('silver',6): F(7,10)-F(1,4),
}
for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        sol=val(p['solutions'])
        fresh=solve[(tier,i)]
        if sol!=fresh:
            errors.append(f"{tier}[{i}] SOLUTION MISMATCH: display={p['display']} stored={p['solutions']}({sol}) fresh={fresh}")
        # non-calc clean check
        if p.get('calculator')==False:
            # fraction input clean if denom small; single_value must be integer-ish
            if p['input_type']=='single_value' and fresh.denominator!=1:
                errors.append(f"{tier}[{i}] single_value non-integer {fresh}")

# recompute guided_steps final boxes land on solution
def check_walk(tier,i,p):
    steps=[s for s in p.get('guided_steps',[]) if 'answer' in s]
    # just report the numeric answers list for manual continuity; verify last box(es)
    return [s['answer'] for s in steps]

print("SOLUTION CHECK done, errors so far:",len(errors))
for e in errors: print("  ",e)

# Verify misconception expects by recomputing the described error
# We'll check the arithmetic of each expect against note where determinate.
misc_checks=[]
for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        for j,m in enumerate(p.get('misconceptions',[])):
            misc_checks.append((tier,i,j,m.get('pattern'),m.get('expect'),m.get('note')))
print("\nMISCONCEPTIONS (",len(misc_checks),"):")
for c in misc_checks:
    print("  ",c[0],c[1],c[2],c[3],"expect=",c[4])
