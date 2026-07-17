import json
live=json.load(open('_CHK5_live.json',encoding='utf-8'))
pb=live['problem_bank']

def check(name, ds, fn, tol=1e-3):
    bad=0
    for pt in ds:
        exp=fn(pt['x'])
        if abs(exp-pt['y'])>tol:
            bad+=1
            print(f"  MISMATCH {name} x={pt['x']} stored y={pt['y']} expected {exp:.4f}")
    print(f"{name}: {len(ds)} pts, {bad} mismatches")

# gold[1] chart: y = x^3 - 9x
check("gold[1] y=x^3-9x", pb['gold'][1]['chart']['data']['datasets'][0]['data'], lambda x:x**3-9*x)
# bronze[5] chart: reciprocal, appears y=6/x (two branches)
for i,d in enumerate(pb['bronze'][5]['chart']['data']['datasets']):
    check(f"bronze[5] branch{i} y=6/x", d['data'], lambda x:6.0/x)
# silver[4] chart: y = 0.5^x
check("silver[4] y=0.5^x", pb['silver'][4]['chart']['data']['datasets'][0]['data'], lambda x:0.5**x)
