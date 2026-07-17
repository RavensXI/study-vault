import math
def r2(v): return round(v,2)
cases=[
 ("teach.silver +", (-2+math.sqrt(20))/2, 1.24),
 ("teach.silver -", (-2-math.sqrt(20))/2, -3.24),
 ("s0 +28/2", (-4+math.sqrt(28))/2, 0.65),
 ("s0 -28/2", (-4-math.sqrt(28))/2, -4.65),
 ("s1 +20/2", (6+math.sqrt(20))/2, 5.24),
 ("s1 -20/2", (6-math.sqrt(20))/2, 0.76),
 ("s4 +41/4", (-3+math.sqrt(41))/4, 0.85),
 ("s4 -41/4", (-3-math.sqrt(41))/4, -2.35),
 ("s5 +17/2", (-5+math.sqrt(17))/2, -0.44),
 ("s5 -17/2", (-5-math.sqrt(17))/2, -4.56),
 ("sqrt28", math.sqrt(28), 5.29),
 ("sqrt20", math.sqrt(20), 4.47),
 ("sqrt41", math.sqrt(41), 6.40),
 ("sqrt17", math.sqrt(17), 4.12),
]
bad=0
for n,v,exp in cases:
    ok = abs(r2(v)-exp)<0.011
    if not ok: bad+=1
    print(f"{n:16} {v:.4f} -> {r2(v):.2f}  expect {exp}  {'OK' if ok else 'MISMATCH'}")
print("BAD:",bad)
