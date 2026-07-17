# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-ocr_geometry-L04.json", encoding="utf-8"))
errs = []

# --- independent solvers ---
def translate(p, v): return (p[0]+v[0], p[1]+v[1])
def reflect_x(p): return (p[0], -p[1])
def reflect_y(p): return (-p[0], p[1])
def reflect_yx(p): return (p[1], p[0])
def reflect_ynx(p): return (-p[1], -p[0])
def rot90acw(p): return (-p[1], p[0])
def rot90cw(p): return (p[1], -p[0])
def rot180(p): return (-p[0], -p[1])
def enlarge(p, sf, c=(0,0)): return (c[0]+sf*(p[0]-c[0]), c[1]+sf*(p[1]-c[1]))

# expected correct answers (index for MC = 0 means options[0]); verify options[0] matches solver
checks = {
 "bronze": [
   ("(7, 1)", translate((4,2),(3,-1))),
   ("(-2, 7)", translate((1,5),(-3,2))),
   ("(3, -2)", reflect_x((3,2))),
   ("(-5, -1)", reflect_y((5,-1))),
   ("(7, 2)", reflect_yx((2,7))),
   ("(0, 1)", rot90acw((1,0))),
   ("(6, 2)", enlarge((3,1),2)),
   ("(12, 6)", enlarge((4,2),3)),
 ],
 "silver": [
   ("(-1, -4)", reflect_ynx((4,1))),
   ("(-3, -1)", rot180((3,1))),
   ("(1, 2)", enlarge((2,4),0.5)),
   ("(9, 5)", enlarge((5,3),2,(1,1))),
   (3, ("sv", (5,7)[0]-(2,3)[0])),
   (45, ("sv", 5*3**2)),
   ("(4, 0)", rot90cw((0,4))),
 ],
 "gold": [
   ("(-3, -1)", enlarge((3,2),-2,(1,1))),
   ("180", ("mc0",)),
   (24, ("sv", 12*2)),
   ("(1, 0)", enlarge((4,6),-0.5,(2,2))),
   (5, ("sv", int((200//8)**0.5))),
 ],
}

def parse_pt(s):
    m = re.search(r'\(([-\d.]+),\s*([-\d.]+)\)', s)
    return (float(m.group(1)), float(m.group(2)))

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        exp = checks[tier][i]
        if p["input_type"]=="multiple_choice":
            # solution index 0 => options[0] is correct; compare with computed
            opt0 = p["options"][0]
            computed = exp[1]
            if isinstance(computed, tuple) and len(computed)==2 and not isinstance(computed[0],str):
                cp = parse_pt(opt0)
                if abs(cp[0]-computed[0])>1e-6 or abs(cp[1]-computed[1])>1e-6:
                    errs.append(f"{tier}[{i}] MC opt0 {opt0} != computed {computed}")
        else:
            sol = p["solutions"][0]
            computed = exp[1][1] if isinstance(exp,tuple) else exp
            if isinstance(exp, tuple):
                computed = exp[1]
            # exp is (sol_expected, ("sv",value))
            want = exp[1][1]
            if abs(sol-want)>1e-6:
                errs.append(f"{tier}[{i}] sv sol {sol} != computed {want}")

# --- verify guided_steps boxes land correctly (recompute each numerically stated) ---
# S4 boxes: 4,3,5 ; S5: 9,45,5 ; G2: 2,24,12 ; G4: 25,5,200
gs_expect = {
 ("silver",4): [4,3,5],
 ("silver",5): [9,45,5],
 ("gold",2): [2,24,12],
 ("gold",4): [25,5,200],
}
for (tier,i),vals in gs_expect.items():
    boxes = [s["answer"] for s in pb[tier][i]["guided_steps"] if "answer" in s]
    if boxes != vals:
        errs.append(f"{tier}[{i}] guided boxes {boxes} != {vals}")

# --- verify teach boxes ---
teach_expect = {"bronze":[5,1,3,-4], "silver":[3,-4,25,25], "gold":[4,3,-8,-7,-5,-8]}
for tier,vals in teach_expect.items():
    boxes=[s["answer"] for s in pd["guided"]["teach"][tier]["steps"] if "answer" in s]
    if boxes!=vals:
        errs.append(f"teach.{tier} boxes {boxes} != {vals}")

# opener boxes
op=[s["answer"] for s in pd["guided"]["opener"]["steps"] if "answer" in s]
if op!=[6,4,-2]:
    errs.append(f"opener boxes {op} != [6,4,-2]")

# --- verify expects reproduce a real error and match a distractor option (MC) ---
def check_mc_expect(tier,i,err_pt):
    p=pb[tier][i]; e=p["misconceptions"][0]["expect"]
    cp=parse_pt(p["options"][e])
    if abs(cp[0]-err_pt[0])>1e-6 or abs(cp[1]-err_pt[1])>1e-6:
        errs.append(f"{tier}[{i}] expect opt[{e}]={p['options'][e]} != error {err_pt}")
# bronze errors
check_mc_expect("bronze",0,(7,3))   # +1 instead of -1
check_mc_expect("bronze",1,(-2,3))  # subtract y
check_mc_expect("bronze",2,(-3,2))  # y-axis
check_mc_expect("bronze",3,(5,1))   # x-axis
check_mc_expect("bronze",4,(2,-7))  # sign not swap
check_mc_expect("bronze",5,(0,-1))  # cw rule
check_mc_expect("bronze",6,(5,3))   # add 2
check_mc_expect("bronze",7,(7,5))   # add 3
check_mc_expect("silver",0,(-4,-1)) # negate both
check_mc_expect("silver",1,(3,-1))  # negate y only
check_mc_expect("silver",2,(4,8))   # doubled
check_mc_expect("silver",3,(10,6))  # from origin
check_mc_expect("silver",6,(-4,0))  # acw rule
check_mc_expect("gold",0,(5,3))     # +2
check_mc_expect("gold",3,(3,4))     # +0.5
# sv expects
sv_exp={("silver",4):-3,("silver",5):15,("gold",2):48,("gold",4):25}
for (tier,i),ev in sv_exp.items():
    got=pb[tier][i]["misconceptions"][0]["expect"]
    if got!=ev: errs.append(f"{tier}[{i}] sv expect {got} != {ev}")

# --- SVG label/number crosscheck: every coord in svg text must be in problem text ---
for tier in ("silver","gold"):
    for i,p in enumerate(pb[tier]):
        d=p["display"]
        if "<svg" in d:
            texts=re.findall(r'>([^<]*\([-\d, ]+\)[^<]*)<', d)
            # collect coord tuples from svg text and from question text
            svg_part=d[:d.index("</svg>")]
            q_part=d[d.index("</svg>")+6:]
            svg_coords=set(re.findall(r'\(\s*-?\d+,\s*-?\d+\s*\)', svg_part))
            q_coords=set(re.findall(r'\(\s*-?\d+,\s*-?\d+\s*\)', q_part))
            norm=lambda s:re.sub(r'\s','',s)
            for c in svg_coords:
                if norm(c) not in {norm(x) for x in q_coords}:
                    # centre coords appear in q text too; allow if matches
                    errs.append(f"{tier}[{i}] svg coord {c} not in question text {q_coords}")

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: all problems, boxes, expects, and figure labels reproduce.")
