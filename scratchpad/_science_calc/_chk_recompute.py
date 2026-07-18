# -*- coding: utf-8 -*-
import json
pd = json.load(open("_chk_live_canonical.json", encoding="utf-8"))

def r(x, n):
    return round(x, n)

print("=== manual recompute of key answers/expects ===")
# gold[5] coefficient_error expect 30.0 : ignore coefficients
ae = 32/(32+74.5)*100
print("gold[5] ignore-coeff AE =", round(ae,4), "-> expect 30.0")

# gold[0] unit_error 80000
print("gold[0] unit slip (960/1.2)*100 =", (960/1.2)*100)
# gold[4] unit_error 84000
print("gold[4] unit slip (504/0.6)*100 =", (504/0.6)*100)
# silver[3] mole_ratio 160: no doubling
mfe = 0.0625*56
print("silver[3] no-double yield = (5.6/%.4f)*100 ="%mfe, (5.6/mfe)*100)
# bronze[1] inverse 115.2
print("bronze[1] 4.8*24 =", 4.8*24)
# bronze[5] inverse 133.33
print("bronze[5] (10/7.5)*100 =", round((10/7.5)*100,2))
# bronze[7] inverse 172.8
print("bronze[7] 7.2*24 =", 7.2*24)
# gold[1] wrong_route 56
print("gold[1] routeA AE = 56/(56+44)*100 =", 56/100*100)
# gold[2] mole_ratio 4.8
print("gold[2] no-ratio 0.2*24 =", 0.2*24)
# gold[3] mole_ratio 2.4
print("gold[3] no-ratio 0.1*24 =", 0.1*24)
# silver[1] mole_ratio 4.8
print("silver[1] no-ratio 0.2*24 =", 0.2*24)
# silver[4] coeff_error 56
print("silver[4] no-coeff AE = 56/(56+44)*100 =", 56/100*100)

print()
print("=== full solutions check ===")
# Verify each stored solution by recomputing
checks = {
 "gold[0]": (0.05*24, "theoretical 1.2 dm3=1200cm3; yield 960/1200*100", 80),
 "gold[1]": (56/74*100, "AE", 75.7),
 "gold[2]": (0.2*3*24, "vol CO2", 14.4),
 "gold[3]": (0.1*1.5*24, "vol O2", 3.6),
 "gold[4]": (504/600*100, "yield", 84),
 "gold[5]": (96/245*100, "AE", 39.2),
 "bronze[0]": (0.5*24, "vol", 12),
 "bronze[1]": (4.8/24, "moles", 0.2),
 "bronze[2]": (2*24, "vol", 48),
 "bronze[3]": (56/100*100, "AE", 56),
 "bronze[4]": (100, "AE one product", 100),
 "bronze[5]": (7.5/10*100, "yield", 75),
 "bronze[6]": (0.05*24, "vol", 1.2),
 "bronze[7]": (7.2/24, "moles", 0.3),
 "silver[0]": (0.05*24, "vol", 1.2),
 "silver[1]": (0.1*24, "vol", 2.4),
 "silver[2]": (0.025*24, "vol", 0.6),
 "silver[3]": (5.6/7*100, "yield", 80),
 "silver[4]": (112/244*100, "AE", 45.9),
 "silver[5]": (17/17*100, "AE", 100),
}
for k,(v,desc,stored) in checks.items():
    ok = abs(round(v,1)-stored)<0.05 or abs(v-stored)<0.05
    print(f"{k}: computed={round(v,4)} stored={stored} {'OK' if ok else '*** MISMATCH'} ({desc})")
