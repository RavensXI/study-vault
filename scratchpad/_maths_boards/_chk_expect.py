import math, json
pd = json.load(open("_chk_live_numberL01.json", encoding="utf-8"))
# Reproduce each expect by committing the described error
E = {
 ("gold",0): {"no_fraction_bracket": 18 + 6/2**2 + 5*3,       # bar ignored: 18 + 6/4 + 15
              "index_error": 24/2 + 15},                       # 2^2 read as 2
 ("gold",1): {"square_separately": (2**2+3**2) - 4*(7-5),      # 13-8
              "subtract_before_multiply": (25-4)*2},           # (25-4)x2
 ("gold",2): {"index_error": (3*3 - 7)/(2*5)},                 # 3^3 as 9
 ("gold",3): {"sign_error": -9 + 4*(-2),                       # (-3)^2=-9
              "sign_error_product": 9 + 8},                    # 4x-2=+8
 ("gold",4): {"index_error": 7 + 6*3 - 8,                      # 2^3=6
              "add_before_multiply": (7+8)*3 - 8},             # add 7+2^3 then x3
 ("bronze",0): {"left_to_right": (6+4)*3},
 ("bronze",1): {"left_to_right": (20-8)/2},
 ("bronze",2): {"left_to_right": (3+5)*2},
 ("bronze",3): {"add_first": 24/(6+2)},
 ("bronze",4): {"wrong_order": 10-(3+7)},
 ("bronze",5): {"left_to_right": (2*5+4)*3},                   # 2x5=10,+4=14,x3
 ("bronze",6): {"right_first": 18/(3*2)},
 ("bronze",7): {"left_to_right": (14-8)/2},
 ("silver",0): {"no_bracket": 3+5*4},
 ("silver",1): {"index_error": (4*2)+3*5,                      # 4^2=8
                "add_before_multiply": (16+3)*5},
 ("silver",2): {"no_bracket": 50-(4+6**2)},                    # 4+6^2=40
 ("silver",3): {"multiply_before_divide": 36/(6*3),
                "no_bracket": (36/2+4)*3},                     # 36/2=18,+4=22,x3
 ("silver",4): {"index_first": 2*(9-4**2)},                    # 9-16=-7
 ("silver",5): {"index_error": 100/(5*2)},                     # 5^2=10
 ("silver",6): {"add_before_multiply": (7+2)*5},
}
bad=[]
for (t,i),errs in E.items():
    for m in pd["problem_bank"][t][i]["misconceptions"]:
        pat=m["pattern"]; exp=m["expect"]
        if pat not in errs:
            bad.append(f"{t}[{i}] pattern {pat} not modelled"); continue
        got=errs[pat]
        if abs(got-exp) > 1e-9:
            bad.append(f"{t}[{i}] {pat}: my {got} != expect {exp}")
print("EXPECT mismatches:", len(bad))
for b in bad: print(" -",b)

# Verify walk box continuity: each bank problem's box answers must be internally consistent
# (already validated final=solution). Spot-check the check-step values for a few:
print("check-step spot checks:")
for (t,i),cs in [(("gold",4),7+8-24),(("bronze",4),14-7+3),(("silver",2),-50+100),(("gold",0),21-15)]:
    print(f"  {t}[{i}] check computes:", cs)
