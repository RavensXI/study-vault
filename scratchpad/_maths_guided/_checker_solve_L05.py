# -*- coding: utf-8 -*-
import json, io
live = json.load(io.open('_checker_live_L05.json', encoding='utf-8'))[0]['practice_data']

# independent fresh solves keyed by display
def approx(a,b,tol=1e-6): return abs(a-b)<=tol
solve = {
 "Find 25% of 80": 20,
 "Find 10% of 350": 35,
 "Find 50% of 126": 63,
 "Find 15% of 240": 36,
 "Express 18 out of 60 as a percentage": 30,
 "Decrease 80 by 10%": 72,
 "Increase 150 by 20%": 180,
 "Find 5% of 640": 32,
 "Increase £350 by 15%": 402.5,
 "Decrease 480 by 35%": 312,
 "Express 45 as a percentage of 180": 25,
 "A phone costs £315 after a 10% discount. Find the original price.": 350,
 "A population grows from 250 to 310. What is the percentage increase?": 24,
 "VAT is 20%. A laptop costs £480 including VAT. Find the price before VAT.": 400,
 "A shirt is reduced by 30%. It now costs £28. Find the original price.": 40,
 "A house increases in value by 5% to £315 000. Find the original value.": 300000,
 "A car depreciates by 15% per year. It is now worth £14 450. What was it worth one year ago?": 17000,
 "A shop increases prices by 20% then has a 20% sale. An item now costs £48. Find the original price.": 50,
 "After a 12.5% pay cut, Priya earns £21 000. What was her original salary?": 24000,
 "A train fare goes up by 3% to £45.26. Find the original fare to the nearest penny.": 43.94,
}

print("=== SOLUTION CHECK ===")
fails=[]
for t in ['bronze','silver','gold']:
    for j,pr in enumerate(live['problem_bank'][t]):
        disp=pr['display']; stored=pr['solutions'][0]
        mine=solve.get(disp,'??')
        ok = (mine!='??' and approx(float(mine),float(stored)))
        calc=pr.get('calculator')
        # clean answer on non-calc: integer or .5 money
        clean = (stored==int(stored)) or (round(stored*100)==stored*100 and calc)
        flag='' if ok else '  <<< MISMATCH'
        if not ok: fails.append((t,j,disp,mine,stored))
        print(f"{t}[{j}] calc={calc} stored={stored} mine={mine} {flag}")

print("\nSOLUTION FAILS:", fails)

# ---- expect verification: recompute the wrong answer each misconception describes ----
print("\n=== EXPECT CHECK (report non-null expects; verify manually below) ===")
for t in ['bronze','silver','gold']:
    for j,pr in enumerate(live['problem_bank'][t]):
        for m in pr.get('misconceptions',[]):
            e=m.get('expect')
            print(f"{t}[{j}] pattern={m['pattern']:24s} expect={e}")
