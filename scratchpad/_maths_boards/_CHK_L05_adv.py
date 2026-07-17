# -*- coding: utf-8 -*-
import json, math

ID = "93f6b9f1-7ae6-4f12-945b-a5b0c096dc09"
live = json.load(open("_CHK_L05_live.json", encoding="utf-8"))

predump = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
pre = None
for r in predump:
    if r.get("id") == ID:
        pre = r.get("practice_data")
        break
print("PRE-DUMP FOUND:", pre is not None)
if pre:
    for fld in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pre.get(fld), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {fld}: {'SAME' if a==b else 'CHANGED'}")
        if a != b:
            print("  PRE :", a[:500])
            print("  LIVE:", b[:500])

def approx(a, b, tol=0.05):
    return abs(a-b) <= tol

pb = live["problem_bank"]
issues = []

exp = {
 ("bronze",0):10, ("bronze",1):12, ("bronze",2):15, ("bronze",3):8,
 ("bronze",4):17, ("bronze",5):25, ("bronze",6):9, ("bronze",7):7,
 ("silver",0):9.6, ("silver",1):6.9, ("silver",2):44.4, ("silver",3):53.1,
 ("silver",4):4.7, ("silver",5):7.0, ("silver",6):5.9,
 ("gold",0):35.7, ("gold",1):8, ("gold",2):13, ("gold",3):12.1, ("gold",4):40,
}
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        e = exp[(tier,i)]
        if not approx(sol, e, 0.05):
            issues.append(f"{tier}[{i}] solution {sol} != computed {e}")
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                issues.append(f"{tier}[{i}].guided_steps[{j}] non-numeric answer {st['answer']!r}")

def chk(name, got, want, tol=0.02):
    if not approx(got, want, tol):
        issues.append(f"BOX {name}: recompute {want:.4f} vs stored {got}")

chk("gold.teach.b1", 0.19, round(1.5/8,2))
chk("gold.teach.theta", 10.6, round(math.degrees(math.atan(1.5/8)),1))
chk("gold.teach.check", 0.19, round(math.tan(math.radians(10.6)),2))
chk("gold.teach.hyp", 8.1, round(math.sqrt(1.5**2+8**2),1))
chk("silver.teach.ratio",0.75,round(9/12,2))
chk("silver.teach.theta",36.9,round(math.degrees(math.atan(0.75)),1))
chk("silver.teach.other",53.1,round(90-36.9,1))
chk("opener.b1",25,9+16)
chk("opener.b2",5,math.sqrt(25))

recompute = {
 "gold[0].tan": (0.7, round(math.tan(math.radians(35)),3)),
 "gold[0].d": (35.7, round(25/math.tan(math.radians(35)),1)),
 "gold[3].cos": (0.91, round(math.cos(math.radians(25)),2)),
 "gold[3].H": (12.1, round(11/math.cos(math.radians(25)),1)),
 "silver[0].sin": (0.64, round(math.sin(math.radians(40)),2)),
 "silver[0].O": (9.6, round(15*math.sin(math.radians(40)),1)),
 "silver[1].cos": (0.57, round(math.cos(math.radians(55)),2)),
 "silver[1].A": (6.9, round(12*math.cos(math.radians(55)),1)),
 "silver[2].asin": (44.4, round(math.degrees(math.asin(0.7)),1)),
 "silver[3].atan": (53.1, round(math.degrees(math.atan(8/6)),1)),
 "silver[4].sin": (0.94, round(math.sin(math.radians(70)),2)),
 "silver[4].h": (4.7, round(5*math.sin(math.radians(70)),1)),
 "silver[5].tan": (0.78, round(math.tan(math.radians(38)),2)),
 "silver[5].x": (7.0, round(9*math.tan(math.radians(38)),1)),
 "silver[6].hyp": (5.9, round(math.sqrt(3.5**2+4.8**2),1)),
}
for k,(stored,comp) in recompute.items():
    chk(k, stored, comp)

mis = {
 "gold[0]":(17.5, round(25*math.tan(math.radians(35)),1)),
 "gold[2]":(5, round(math.sqrt(3**2+4**2))),
 "gold[3]":(10.0, round(11*math.cos(math.radians(25)),1)),
 "gold[4]":(130, round(math.sqrt(50**2+120**2))),
 "bronze[1]":(13.9, round(math.sqrt(13**2+5**2),1)),
 "bronze[3]":(11.7, round(math.sqrt(10**2+6**2),1)),
 "silver[0]":(11.5, round(15*math.cos(math.radians(40)),1)),
 "silver[1]":(9.8, round(12*math.sin(math.radians(55)),1)),
 "silver[2]":(45.6, round(math.degrees(math.acos(0.7)),1)),
 "silver[3]":(36.9, round(math.degrees(math.atan(6/8)),1)),
 "silver[4]":(1.7, round(5*math.cos(math.radians(70)),1)),
 "silver[5]":(5.5, round(9*math.sin(math.radians(38)),1)),
 "silver[6]":(3.3, round(math.sqrt(4.8**2-3.5**2),1)),
}
for k,(stored,comp) in mis.items():
    if not approx(stored,comp,0.05):
        issues.append(f"EXPECT {k} stored {stored} vs computed {comp}")

def sweep(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            sweep(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): sweep(v,path+f"[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            issues.append(f"EMDASH at {path}: {o[:60]}")
sweep(live)

print("\n=== ISSUES ===")
print("NONE" if not issues else "")
for x in issues:
    print(" -", x)
