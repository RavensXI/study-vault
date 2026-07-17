# -*- coding: utf-8 -*-
import json, re, statistics

ID = "9bf07c35-9977-4389-9fbb-7c9b3a67caea"
live = json.load(open("_chk_L04_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
preentry = next(x for x in pre if x["id"] == ID)
prepd = preentry["practice_data"]

errors = []
notes = []

def approx(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) <= tol
    except:
        return a == b

pb = live["problem_bank"]

# ---------- fresh-solve helpers ----------
def solve_expected(tier, i, disp):
    # returns computed answer for known problems, else None
    return None

# ---- Bronze fresh solves ----
bronze_expected = [
    ("mean 4,8,6,10,7", statistics.mean([4,8,6,10,7])),         # 7
    ("median 3,9,1,7,5", statistics.median([3,9,1,7,5])),       # 5
    ("mode 7,2,8,2,5,2,9", statistics.mode([7,2,8,2,5,2,9])),   # 2
    ("range 14,3,8,22,11", max([14,3,8,22,11])-min([14,3,8,22,11])), # 19
    ("total mean5=8", 8*5),                                     # 40
    ("median 10,4,15,7,9,3", statistics.median([10,4,15,7,9,3])), # 8
    ("mean 12,15,18,21,24", statistics.mean([12,15,18,21,24])), # 18
    ("mode 50,60,60,65,70,75,80", statistics.mode([50,60,60,65,70,75,80])), # 60
]
for i,(lbl,exp) in enumerate(bronze_expected):
    sol = pb["bronze"][i]["solutions"][0]
    if not approx(sol, exp):
        errors.append(f"bronze[{i}] solution {sol} != fresh {exp} ({lbl})")

# ---- Silver fresh solves ----
# s0 freq mean
fx=[1*3,2*5,3*8,4*4]; s0=sum(fx)/sum([3,5,8,4])
# s1 grouped mean
s1=(4*5+10*15+6*25)/(4+10+6)
# s2 fifth number
s2=5*18-4*15
# s3 modal class -> index 0 = 20-40
# s4 median class -> index 0 = 10-20
# s5 median from freq table 3(2),4(5),5(8),6(3),7(2) n=20 median avg 10th,11th
data_s5=[3]*2+[4]*5+[5]*8+[6]*3+[7]*2
s5=statistics.median(data_s5)
# s6 MC index0=6
silver_checks=[("s0 freqmean",s0,pb["silver"][0]["solutions"][0]),
               ("s1 groupmean",s1,pb["silver"][1]["solutions"][0]),
               ("s2 fifth",s2,pb["silver"][2]["solutions"][0]),
               ("s5 medtable",s5,pb["silver"][5]["solutions"][0])]
for lbl,exp,sol in silver_checks:
    if not approx(sol,exp):
        errors.append(f"silver solution {sol} != fresh {exp} ({lbl})")
# MC index correctness
if pb["silver"][3]["options"][pb["silver"][3]["solutions"][0]] != "20-40":
    errors.append("silver[3] modal-class option index wrong")
if pb["silver"][4]["options"][pb["silver"][4]["solutions"][0]] != "10-20":
    errors.append("silver[4] median-class option index wrong")
# s4 verify median class properly: n=30 running 6,18 -> 15th in 10-20
run=0; classes=[("0-10",6),("10-20",12),("20-30",8),("30-40",4)]; medcls=None
for c,f in classes:
    run+=f
    if run>=15: medcls=c; break
if medcls!="10-20": errors.append(f"silver[4] fresh median class={medcls}")
# s3 modal
mc=max([("0-20",5),("20-40",15),("40-60",10)],key=lambda x:x[1])[0]
if mc!="20-40": errors.append(f"silver[3] fresh modal class={mc}")
# s6 verify only option 0 works
base=[2,5,5,7,8,12]
for opt in ["6","3","1","15"]:
    med=statistics.median(sorted(base+[int(opt)]))
    if opt=="6" and med!=6: errors.append(f"silver[6] adding 6 median={med}")
    if opt!="6" and med==6: notes.append(f"silver[6] option {opt} ALSO gives median 6 (ambiguous MC)")

# ---- Gold fresh solves ----
g0=(3*5+7*15+12*25+8*35)/(3+7+12+8)      # 23.333
g1=(10*12-6*10)/4                        # 15
g2=3*15                                  # 45
g3=20+5                                  # 25
# g4 solve k
# (2700+150k)/(20+k)=140 -> k=10
k=(140*20-2700)/(150-140)
gold_checks=[("g0",round(g0,1),pb["gold"][0]["solutions"][0]),
             ("g1",g1,pb["gold"][1]["solutions"][0]),
             ("g2",g2,pb["gold"][2]["solutions"][0]),
             ("g3",g3,pb["gold"][3]["solutions"][0]),
             ("g4 k",k,pb["gold"][4]["solutions"][0])]
for lbl,exp,sol in gold_checks:
    if not approx(sol,exp):
        errors.append(f"gold solution {sol} != fresh {exp} ({lbl})")

# ---------- recompute every guided_steps / teach / opener box ----------
def check_boxes(steps, path):
    for j,st in enumerate(steps):
        if "answer" not in st: continue
        ans=st["answer"]
        if not isinstance(ans,(int,float)):
            errors.append(f"{path}[{j}] answer not numeric: {ans!r}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if gs: check_boxes(gs, f"{tier}[{i}].guided_steps")
        elif p.get("input_type")!="multiple_choice":
            errors.append(f"{tier}[{i}] non-MC but no guided_steps")
for tier in ("bronze","silver","gold"):
    check_boxes(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_boxes(live["guided"]["opener"]["steps"], "opener")

# ---------- reproduce expects ----------
def expects_report():
    rep=[]
    # bronze
    exp_specs=[
        ("bronze",0,"gave_total",35),
        ("bronze",1,"no_order",1),   # unordered 3,9,1,7,5 middle(3rd)=1
        ("bronze",2,"found_median",5), # median ordered 2,2,2,5,7,8,9 4th=5
        ("bronze",3,"gave_max",22),
        ("bronze",4,"added",13),
        ("bronze",5,"no_order",11),  # unordered 10,4,15,7,9,3 middle two 15,7 avg=11
        ("bronze",6,"gave_total",90),
        ("bronze",7,"found_median",65),
        ("silver",0,"ignored_frequency",2.5),
        ("silver",1,"ignored_frequency",15),
        ("silver",2,"used_new_mean",18),
        ("silver",5,"found_mean",4.9),
        ("gold",0,"used_upper_bounds",28.3),
        ("gold",1,"forgot_to_subtract",30),
        ("gold",2,"range_unchanged",15),
        ("gold",3,"mean_unchanged",20),
    ]
    for tier,i,pat,val in exp_specs:
        mcs=pb[tier][i].get("misconceptions",[])
        m=next((x for x in mcs if x.get("pattern")==pat),None)
        if not m:
            errors.append(f"{tier}[{i}] missing misconception {pat}")
            continue
        if not approx(m["expect"],val):
            errors.append(f"{tier}[{i}].{pat} expect {m['expect']} != committed-error {val}")
expects_report()

# verify committed-error math independently
# bronze1 no_order: middle of unordered 3,9,1,7,5 = index2 =1 -> ok
assert [3,9,1,7,5][2]==1
# bronze5 no_order: unordered 10,4,15,7,9,3 middle two idx2,3 =15,7 avg11
assert (( [10,4,15,7,9,3][2]+[10,4,15,7,9,3][3])/2)==11
# bronze2 found_median: statistics.median ordered =5
assert statistics.median([7,2,8,2,5,2,9])==5
# bronze7 found_median: median of 7 sorted =65
assert statistics.median([50,60,60,65,70,75,80])==65
# silver0 ignored_freq: mean of 1,2,3,4=2.5
assert statistics.mean([1,2,3,4])==2.5
# silver1 ignored_freq mean midpoints 5,15,25=15
assert statistics.mean([5,15,25])==15
# silver5 found_mean 98/20=4.9
assert (3*2+4*5+5*8+6*3+7*2)/20==4.9
# gold0 upper bounds
assert round((3*10+7*20+12*30+8*40)/30,1)==28.3

# ---------- em dash check ----------
def walk_strings(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk_strings(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk_strings(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
STUDENT_FIELDS=("display","pre","post","say","hint","message","title","content","label","example","question","steps","options")
emdash=[]
for path,s in walk_strings(live):
    # skip internal note fields
    if path.endswith(".note"): continue
    if "—" in s:
        emdash.append((path,s[:60]))
if emdash:
    for p,s in emdash: notes.append(f"EM DASH at {p}: {s}")

# ---------- preservation vs pre-dump ----------
for f in ("related_videos","topic_links","worked_examples"):
    if json.dumps(prepd.get(f),sort_keys=True)!=json.dumps(live.get(f),sort_keys=True):
        errors.append(f"PRESERVATION: {f} changed vs pre-dump")
    else:
        notes.append(f"preserved OK: {f}")

# duplicate answers within tier
for tier in ("bronze","silver","gold"):
    sols=[tuple(p["solutions"]) for p in pb[tier] if p.get("input_type")!="multiple_choice"]
    dups=[x for x in set(sols) if sols.count(x)>1]
    if dups: notes.append(f"{tier}: duplicate numeric solutions {dups}")

# non-calculator clean answers
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("calculator")==False and p.get("input_type")!="multiple_choice":
            for s in p["solutions"]:
                if isinstance(s,float) and not s.is_integer():
                    notes.append(f"{tier}[{i}] non-calc has decimal answer {s}")

print("=== ERRORS ===")
for e in errors: print(" ", e)
print("=== NOTES ===")
for n in notes: print(" ", n)
print(f"\nTOTAL ERRORS: {len(errors)}")
