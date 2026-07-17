import sympy as sp
x,y=sp.symbols('x y')
def sub_eq(a,b,c,known,val):  # solve a*x+b*y=c for the other var given one var
    e=a*x+b*y-c
    e=e.subs(known,val)
    other = y if known==x else x
    return float(sp.solve(e,other)[0])

checks=[]
# bronze0 rhs_wrong_operation expect [3,7]: RHS subtracted 10-4=6 -> 2x=6 x=3; then y from x+y=10 -> y=7
checks.append(("bronze0",[3, sub_eq(1,1,10,x,3)],[3,7]))
# bronze1 rhs_not_subtracted expect [14,-9]: LHS 2x-x=x, RHS 9+5=14 -> x=14; y from x+y=5 -> -9
checks.append(("bronze1",[14, sub_eq(1,1,5,x,14)],[14,-9]))
# bronze2 rhs_not_subtracted expect [-3,10]: 2y=13+7=20 y=10; x from x+y=7 -> -3
checks.append(("bronze2",[sub_eq(1,1,7,y,10),10],[-3,10]))
# bronze3 rhs_not_subtracted expect [10,-4]: 2x=14+6=20 x=10; y from x+y=6 -> -4
checks.append(("bronze3",[10, sub_eq(1,1,6,x,10)],[10,-4]))
# bronze4 substitute_sign_slip expect [5,-1]: x=5, y=-1 (reversed sub in x-y=4: y=x-4=1 correct; reversed -> -1)
checks.append(("bronze4",[5,-1],[5,-1]))
# bronze5 rhs_not_subtracted expect [12,-5]: 2x=17+7=24 x=12; y from x+y=7 -> -5
checks.append(("bronze5",[12, sub_eq(1,1,7,x,12)],[12,-5]))
# bronze6 substitute_sign_slip expect [3,16]: x=3; 2x+y=10 -> 6+y=10, err 10+6=16
checks.append(("bronze6",[3,16],[3,16]))
# bronze7 substitute_sign_slip expect [3,-6]: x=3, y sign flip -> -6
checks.append(("bronze7",[3,-6],[3,-6]))
# silver0 substitute_sign_slip expect [3,-5]
checks.append(("silver0",[3,-5],[3,-5]))
# silver1 scaled_lhs_only expect [-7,23]: 6x+3y=9 (rhs not scaled), minus 4x+3y=23 -> 2x=9-23=-14 x=-7; y from 2x+y=9 -> 23
checks.append(("silver1",[-7, sub_eq(2,1,9,x,-7)],[-7,23]))
# silver2 substitute_sign_slip expect [11,3]: y=3; 2x+9=13 err 13+9=22 x=11
checks.append(("silver2",[11,3],[11,3]))
# silver3 substitute_sign_slip expect [3,10]: x=3; y=3x-1 err +1 -> 10
checks.append(("silver3",[3,10],[3,10]))
# silver4 substitute_sign_slip expect [5,-3]
checks.append(("silver4",[5,-3],[5,-3]))
# gold1 substitute_sign_slip expect [2,18]: x=2; 7x+2y=22 ->14+2y=22 err 22+14=36 y=18
checks.append(("gold1",[2,18],[2,18]))
# gold2 rhs_wrong_operation expect [3,12]: 15-6=9 3x=9 x=3; y from x+y=15 ->12
checks.append(("gold2",[sub_eq(1,1,15,x,3),12],[3,12]))
# gold3 substitute_sign_slip expect [2,5]: x=2; 3x+2y=4 ->6+2y=4 err 4+6=10 y=5
checks.append(("gold3",[2,5],[2,5]))

bad=0
for name,model,stored in checks:
    m=[round(float(v),6) for v in model]
    ok = all(abs(a-b)<1e-9 for a,b in zip(m,stored))
    if not ok: bad+=1
    print(f"{name}: modeled={m} stored_expect={stored} {'OK' if ok else '*** MISMATCH ***'}")
print("BAD EXPECTS:",bad)
