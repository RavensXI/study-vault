import json, io
live=json.load(io.open("_CHK_algL12ocr_live.json","r",encoding="utf-8"))
issues=[]

# Verify arithmetic 'check' boxes independently (the substituted evaluations)
checks=[
 # (label, computed, stored)
 ("teach.gold check 2(2^2)+2-6", 2*(2**2)+2-6, 4),
 ("teach.bronze check 4^2-8*4+15", 4**2-8*4+15, -1),
 ("teach.silver check 3^2+2*3-8", 3**2+2*3-8, 7),
 ("opener 7-2", 7-2, 5),
 ("opener 4-2", 4-2, 2),
 ("opener 4-6", 4-6, -2),
 ("gold[3] check 3^2-9", 3**2-9, 0),
 ("bronze[4] total 5+5", 5+5, 10),
 ("bronze[6] check 4^2-3*4-4", 4**2-3*4-4, 0),
 ("silver[2] check (-2)^2-3*(-2)-10", (-2)**2-3*(-2)-10, 0),
 ("silver[5] check 7^2", 7**2, 49),
]
for lbl,comp,stored in checks:
    ok = comp==stored
    print(f"{'OK ' if ok else 'BAD'} {lbl} = {comp} (stored {stored})")
    if not ok: issues.append(f"{lbl}: computed {comp} != stored {stored}")

# single_value misconception expects: recompute the described error
print("\n-- single_value expects --")
# gold[3]: expect 7 = count of x^2-9<=0 alone (-3..3); expect 5 = include x=-1 (x>=-1 & -3..3 -> -1..3? no: x>=-1 gives -1,0,1,2,3 =5)
print("gold[3] e7:", len([i for i in range(-3,4)]), "e5:", len([i for i in range(-3,4) if i>=-1]))
# bronze[4]: expect12 = >=25 (x<=-5 or x>=5) integers -10..10; expect5 = one side
print("bronze[4] e12:", len([i for i in range(-10,11) if i*i>=25]), "e5(one side):", len([i for i in range(6,11)]))
# bronze[6]: expect4 = strict <0 (-1,4 excluded); expect5 = drop -1 endpoint
print("bronze[6] e4:", len([i for i in range(-1,5) if -1<i<4]), "e5:", len([i for i in range(0,5)]))
# silver[2]: expect6 strict; expect7 off-by-one
print("silver[2] e6:", len([i for i in range(-2,6) if -2<i<5]), "e7(drop one end):", len([i for i in range(-1,6)]))
# silver[5]: expect8 include zero; expect6 stop at 6
print("silver[5] e8:", len([i for i in range(0,8)]), "e6:", len([i for i in range(1,7)]))
# silver[6]: expect5 wrong sign, expect -5 other root -> just labels

print("\nISSUES:", issues if issues else "NONE")
