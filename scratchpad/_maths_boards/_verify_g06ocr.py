# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_maths-ocr_graphs-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# canonical solver from display
def solve(disp, sols):
    # returns True if stored sols look right by independent reasoning table
    return True

# 1. distinct within tier
for t in ("bronze","silver","gold"):
    seen = {}
    for i,p in enumerate(pb[t]):
        k = tuple(p["solutions"])
        if k in seen:
            errs.append(f"{t}[{i}] duplicate solution {k} (also {t}[{seen[k]}])")
        seen[k]=i

# 2. independent fresh-solve of each display (hard-coded reasoning)
expected = {
 "bronze":[0,1,-1,360,180,90,270,3],
 "silver":[30,60,150,0,120,240,300],
 "gold":[210,5,-3,4,45],
}
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        if p["solutions"] != [expected[t][i]]:
            errs.append(f"{t}[{i}] stored {p['solutions']} != fresh {expected[t][i]} | {p['display']}")

# 3. guided_steps last box lands on solution; expects != solution
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        sol = p["solutions"][0]
        gs = p.get("guided_steps",[])
        boxes = [s for s in gs if s.get("answer") is not None]
        if boxes and boxes[-1]["answer"] != sol:
            errs.append(f"{t}[{i}] last box {boxes[-1]['answer']} != solution {sol}")
        for j,mc in enumerate(p.get("misconceptions",[])):
            e = mc.get("expect")
            if e is not None and e == sol:
                errs.append(f"{t}[{i}].misc[{j}] expect==solution {e}")

# 4. chart points satisfy the stated curve
def chk_chart(p, path, fn, xmax):
    ch = p.get("chart")
    if not ch: return
    dsets = ch["data"]["datasets"]
    curve = dsets[0]["data"]
    for pt in curve:
        want = round(fn(math.radians(pt["x"])),4)
        if want == 0: want = 0.0
        if abs(pt["y"] - want) > 0.001:
            errs.append(f"{path} chart point x={pt['x']} y={pt['y']} != {want}")
    # x axis max
    if ch["options"]["scales"]["x"]["max"] != xmax:
        errs.append(f"{path} chart xmax != {xmax}")

chk_chart(pb["bronze"][7], "bronze[7]", math.sin, 360)   # crossings
chk_chart(pb["silver"][5], "silver[5]", math.cos, 360)   # cos -0.5
chk_chart(pb["gold"][0], "gold[0]", math.sin, 360)       # sin -0.5
chk_chart(pb["gold"][3], "gold[3]", math.sin, 720)       # count 0.3

# 5. kline values correct
def chk_kline(p, path, kval):
    ch=p["chart"]; dl=[d for d in ch["data"]["datasets"] if d.get("borderDash")]
    if not dl: errs.append(f"{path} missing dashed kline"); return
    ys={pt["y"] for pt in dl[0]["data"]}
    if ys != {kval}: errs.append(f"{path} kline y {ys} != {kval}")
chk_kline(pb["silver"][5],"silver[5]",-0.5)
chk_kline(pb["gold"][0],"gold[0]",-0.5)
chk_kline(pb["gold"][3],"gold[3]",0.3)

# 6. teach walks land correctly (spot list)
teach = pd["guided"]["teach"]
teach_expect = {"bronze":0, "silver":-0.5, "gold":0}  # last box answers
for t,exp in teach_expect.items():
    boxes=[s for s in teach[t]["steps"] if s.get("answer") is not None]
    if boxes[-1]["answer"]!=exp:
        errs.append(f"teach.{t} last box {boxes[-1]['answer']} != {exp}")
    if len(boxes)<4:
        errs.append(f"teach.{t} only {len(boxes)} boxes")

# opener boxes
op=[s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if [b["answer"] for b in op]!=[5,35,30]:
    errs.append(f"opener answers {[b['answer'] for b in op]} != [5,35,30]")

# em-dash scan
def scan(o,pth):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,pth+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,pth+f"[{i}]")
    elif isinstance(o,str) and "—" in o:
        errs.append("EM DASH at "+pth)
scan(pd,"pd")

print("ERRORS:" if errs else "ALL CHECKS PASS")
for e in errs: print("  -",e)
print("counts:", {t:len(pb[t]) for t in ('bronze','silver','gold')})
