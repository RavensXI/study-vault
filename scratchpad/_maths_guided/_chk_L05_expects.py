import json
from decimal import Decimal
live=json.load(open("_CHK_L05_live.json",encoding="utf-8"))
r2=lambda x: round(x+1e-12,2)
# expects committed error, keyed by (tier,index,pattern) -> computed wrong answer
checks={
 ("gold",0,"subtract_5_percent"): 315000-0.05*315000,
 ("gold",1,"add_15_percent"): 14450+0.15*14450,
 ("gold",2,"cancel_out"): 48,
 ("gold",2,"one_multiplier"): 48/0.8,
 ("gold",3,"add_12.5_percent"): 21000+0.125*21000,
 ("gold",4,"subtract_3_percent"): r2(45.26-0.03*45.26),
 ("bronze",0,"wrong_conversion"): 0.25,
 ("bronze",0,"divide_not_multiply"): 80/0.25,
 ("bronze",1,"decimal_error"): 3.5,
 ("bronze",2,"doubled"): 126*2,
 ("bronze",3,"percent_as_multiplier"): 1.5*240,
 ("bronze",3,"wrong_decimal"): 0.015*240,
 ("bronze",5,"increase_not_decrease"): 80*1.1,
 ("bronze",5,"subtract_percent"): 80-10,
 ("bronze",6,"find_percent_only"): 30,
 ("bronze",6,"decrease_not_increase"): 150*0.8,
 ("bronze",7,"ten_percent"): 64,
 ("silver",0,"add_percentage"): 350+15,
 ("silver",1,"increase_not_decrease"): 480*1.35,
 ("silver",2,"upside_down"): 180/45*100,
 ("silver",3,"add_10_percent"): 315+0.10*315,
 ("silver",4,"divide_by_new"): r2(60/310*100),
 ("silver",4,"no_multiply_100"): r2(60/250),
 ("silver",5,"subtract_20_percent"): 480-0.20*480,
 ("silver",6,"add_30_percent"): r2(28+0.30*28),
}
pb=live["problem_bank"]
bad=[]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        for m in p.get("misconceptions",[]):
            key=(t,i,m["pattern"])
            exp=m["expect"]
            if exp is None: continue
            if key in checks:
                comp=checks[key]
                ok=abs(float(exp)-float(comp))<1e-6
                if not ok: bad.append((key,exp,comp))
            else:
                bad.append((key,exp,"NO-CHECK-DEFINED"))
if bad:
    for b in bad: print("MISMATCH",b)
else:
    print("ALL EXPECTS REPRODUCE")
# also list any expect present that we didn't model
