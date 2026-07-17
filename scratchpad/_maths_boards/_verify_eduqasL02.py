# -*- coding: utf-8 -*-
def rnd(x, n): return round(x, n)
checks = []
checks.append(("bronze0", 0.25*60, 15))
checks.append(("bronze1", 0.10*340, 34))
checks.append(("bronze2", 200*1.15, 230))
checks.append(("bronze3", 80*0.8, 64))
checks.append(("bronze4", 35*0.9, 31.50))
checks.append(("bronze5", 0.35*100, 35))
checks.append(("bronze6", 18/60*100, 30))
checks.append(("bronze7", 0.40*250, 100))
checks.append(("silver0_simpleint", 8000*0.05*3, 1200))
checks.append(("silver0_cmpd_distr", 8000*1.05**3-8000, 1261.00))
checks.append(("silver1", 50000*1.02, 51000))
checks.append(("silver2", 16000*0.9**2, 12960))
checks.append(("silver3", 45/180*100, 25))
checks.append(("silver4", 30000/150000*100, 20))
checks.append(("silver5", 6000*1.04**3, 6749.69))
checks.append(("silver6", 85*1.2, 102))
checks.append(("gold0", 60/1.25, 48))
checks.append(("gold1", 350/0.70, 500))
v=2000; yrs=0
while v<=2500:
    v*=1.06; yrs+=1
checks.append(("gold2_years", yrs, 4))
checks.append(("gold3", 12000/1.05**2, 10884.35))
checks.append(("gold4", 80000*0.97**5, 68589))
print("%-22s %15s %12s %s" % ("id","computed","stored","match?"))
for name, comp, stored in checks:
    c = rnd(comp, 2)
    m = abs(c - stored) < 0.02 or abs(round(comp)-stored) < 0.5
    print("%-22s %15s %12s %s" % (name, c, stored, "OK" if m else "*** MISMATCH ***"))
print()
print("silver5 exact 6000*1.04^3 =", 6000*1.04**3)
print("gold4 exact 80000*0.97^5 =", 80000*0.97**5, " 0.97^5 =", 0.97**5)
