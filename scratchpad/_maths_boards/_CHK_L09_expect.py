# Reproduce scaled_lhs_only & rhs_not_subtracted expects by committing the error
# silver[0]: 3x+2y=16 ; x+y=7 ; scale eq2 x2 LHS only -> 2x+2y=7 ; subtract from eq1
x=(16-7)/(3-2); y=(7-2*x)/2   # back-sub into WRONG scaled eq 2x+2y=7
print("silver[0] scaled_lhs_only:", [x,y], "expect [9,-5.5]")
# silver[1]: 2x+3y=19 ; x+y=8 ; ->2x+2y=8 ; subtract eliminates x
y=(19-8)/(3-2); x=(8-2*y)/2
print("silver[1] scaled_lhs_only:", [x,y], "expect [-7,11]")
# gold[2]: 4x+3y=23 ; 2x+y=9 ; x3 LHS only ->6x+3y=9 ; subtract eq1 eliminates y
x=(9-23)/(6-4); y=(23-4*x)/3  # back-sub into eq1 (original)
print("gold[2] scaled_lhs_only:", [x,y], "expect [-7,17]")
# rhs_not_subtracted bronze[6]: 5x+y=17 ; 3x+y=11 ; subtract LHS but ADD rhs
x=(17+11)/(5-3); y=11-3*x
print("bronze[6] rhs_not_subtracted:", [x,y], "expect [14,-31]")
# rhs_wrong_operation bronze[0]: x+y=10 ; x-y=4 ; add LHS (2x) but SUBTRACT rhs
x=(10-4)/2; y=10-x
print("bronze[0] rhs_wrong_operation:", [x,y], "expect [3,7]")

# figure/chart sweep
import json
live=json.load(open("_CHK_L09eduqas_live.json",encoding="utf-8"))
has_svg=has_chart=0
for tier in ["bronze","silver","gold"]:
    for p in live["problem_bank"][tier]:
        if "chart" in p: has_chart+=1
        if "<svg" in p.get("display",""): has_svg+=1
print("\nfigures present: svg=%d chart=%d (linear simultaneous eqns = textual, none expected)"%(has_svg,has_chart))
