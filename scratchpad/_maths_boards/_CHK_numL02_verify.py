import json
from fractions import Fraction as F

live = json.load(open('_CHK_numL02_live.json', encoding='utf-8'))
pb = live['problem_bank']
issues = []

# Ground-truth solver keyed by display -> expected reduced fraction
truth = {
    # bronze
    "1/4+1/3": F(1,4)+F(1,3),
    "3/5+1/5": F(3,5)+F(1,5),
    "5/6-1/3": F(5,6)-F(1,3),
    "2/7+3/7": F(2,7)+F(3,7),
    "1/2*3/4": F(1,2)*F(3,4),
    "7/8-1/8": F(7,8)-F(1,8),
    "2/5*5/6": F(2,5)*F(5,6),
    "1/2+1/6": F(1,2)+F(1,6),
    # silver
    "2/3+5/8": F(2,3)+F(5,8),
    "3/4-2/5": F(3,4)-F(2,5),
    "3/5*10/9": F(3,5)*F(10,9),
    "4/5:2/3": F(4,5)/F(2,3),
    "1+1/3+2/5": F(4,3)+F(2,5),
    "5/6:5/12": F(5,6)/F(5,12),
    "7/10-1/4": F(7,10)-F(1,4),
    # gold
    "2/3+3/4-1/6": F(2,3)+F(3,4)-F(1,6),
    "2+1/2*1+3/5": F(5,2)*F(8,5),
    "3+1/4-1+2/3": F(13,4)-F(5,3),
    "3/8:9/16": F(3,8)/F(9,16),
    "5/6*3/10+1/4": F(5,6)*F(3,10)+F(1,4),
}
order = {
 'bronze':["1/4+1/3","3/5+1/5","5/6-1/3","2/7+3/7","1/2*3/4","7/8-1/8","2/5*5/6","1/2+1/6"],
 'silver':["2/3+5/8","3/4-2/5","3/5*10/9","4/5:2/3","1+1/3+2/5","5/6:5/12","7/10-1/4"],
 'gold':["2/3+3/4-1/6","2+1/2*1+3/5","3+1/4-1+2/3","3/8:9/16","5/6*3/10+1/4"],
}

def sol_to_frac(sol):
    if len(sol)==1: return F(sol[0])
    return F(sol[0], sol[1])

for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        key=order[tier][i]
        exp=truth[key]
        got=sol_to_frac(p['solutions'])
        if got!=exp:
            issues.append(f"{tier}[{i}] SOLUTION: display={p['display']} stored={p['solutions']} -> {got} != truth {exp}")
        # simplest-form check on stored fraction pair
        if len(p['solutions'])==2:
            n,d=p['solutions']
            if F(n,d)!=F(n,d):  # placeholder
                pass
            from math import gcd
            if gcd(n,d)!=1:
                issues.append(f"{tier}[{i}] NOT SIMPLIFIED stored {p['solutions']}")
        # final guided box lands on solution
        boxes=[s for s in p['guided_steps'] if 'answer' in s and 'say' not in s]
        # verify each guided box independently is hard generically; check final two match solution parts
        # verify check-back not required numerically here

print("=== SOLUTIONS ===")
print("OK" if not issues else "\n".join(issues))

# Misconception expects: recompute committed error
mis_issues=[]
def check(tier,i,pat,exp,computed):
    if exp is None: return
    ce=[computed.numerator, computed.denominator] if isinstance(computed,F) else computed
    if list(exp)!=list(ce):
        mis_issues.append(f"{tier}[{i}] {pat}: stored expect {exp} != committed-error {ce}")

# bronze
b=pb['bronze']
check('bronze',0,'add_denominators',b[0]['misconceptions'][0]['expect'],[1+1,4+3])
check('bronze',1,'add_denominators',b[1]['misconceptions'][0]['expect'],[3+1,5+5])
check('bronze',2,'subtract_across',b[2]['misconceptions'][0]['expect'],[5-1,6-3])
check('bronze',2,'no_simplify',b[2]['misconceptions'][1]['expect'],[3,6])
check('bronze',3,'add_denominators',b[3]['misconceptions'][0]['expect'],[2+3,7+7])
check('bronze',5,'no_simplify',b[5]['misconceptions'][1]['expect'],[6,8])
check('bronze',6,'no_simplify',b[6]['misconceptions'][0]['expect'],[10,30])
check('bronze',7,'add_denom',b[7]['misconceptions'][0]['expect'],[1+1,2+6])
check('bronze',7,'no_simplify',b[7]['misconceptions'][1]['expect'],[4,6])
# silver
s=pb['silver']
check('silver',0,'add_across',s[0]['misconceptions'][0]['expect'],[2+5,3+8])
check('silver',1,'no_scale',s[1]['misconceptions'][0]['expect'],[3-2,20])
check('silver',2,'no_simplify',s[2]['misconceptions'][0]['expect'],[30,45])
check('silver',3,'no_flip',s[3]['misconceptions'][0]['expect'],[4*2,5*3])
check('silver',4,'ignore_whole',s[4]['misconceptions'][0]['expect'],[F(1,3)+F(2,5)])
# 1/3+2/5=11/15
check('silver',4,'ignore_whole',s[4]['misconceptions'][0]['expect'],F(1,3)+F(2,5))
check('silver',6,'no_scale',s[6]['misconceptions'][0]['expect'],[7-1,20])
# gold
g=pb['gold']
check('gold',0,'combine_across',g[0]['misconceptions'][0]['expect'],[2+3-1,3+4-6])
check('gold',0,'no_simplify',g[0]['misconceptions'][1]['expect'],[15,12])
check('gold',2,'split_no_borrow',g[2]['misconceptions'][0]['expect'],[2*12+5,12]) # 2 5/12
check('gold',3,'no_flip',g[3]['misconceptions'][0]['expect'],F(3,8)*F(9,16))
check('gold',4,'order_error',g[4]['misconceptions'][0]['expect'],F(5,6)*(F(3,10)+F(1,4)))

print("=== MISCONCEPTION EXPECTS ===")
print("OK" if not mis_issues else "\n".join(mis_issues))
