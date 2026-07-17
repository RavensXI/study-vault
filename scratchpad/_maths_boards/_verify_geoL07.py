# -*- coding: utf-8 -*-
import json, io, re, sys
sys.stdout.reconfigure(encoding="utf-8")
pd=json.load(io.open("lesson_maths-aqa_geometry-L07.json",encoding="utf-8"))
prob=[]
def txt(d):
    d=re.sub(r"<svg.*?</svg>","[SVG]",d,flags=re.S)
    d=re.sub(r"<[^>]+>","",d)
    return d.strip()
def svg_of(d):
    m=re.search(r"<svg.*?</svg>",d,flags=re.S)
    return m.group(0) if m else ""
def nums(s):
    return re.findall(r"-?\d+\.?\d*",s)

pb=pd["problem_bank"]
issues=[]
# fresh solves (independent), keyed by (tier,i)
expect_sol={
 ("bronze",0):62,("bronze",1):96,("bronze",2):90,("bronze",3):108,("bronze",4):35,
 ("bronze",5):0,("bronze",6):75,("bronze",7):58,
 ("silver",0):35,("silver",1):64,("silver",2):50,("silver",3):12,("silver",4):220,
 ("silver",5):104,("silver",6):85,
 ("gold",0):65,("gold",1):100,("gold",2):70,("gold",3):62,("gold",4):125,
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        key=(tier,i)
        sol=p["solutions"]
        if key in expect_sol and sol[0]!=expect_sol[key]:
            issues.append(f"{tier}[{i}] stored sol {sol} != fresh {expect_sol[key]}")
        # guided_steps final answer must equal solution (single_value)
        gs=p.get("guided_steps")
        if gs:
            boxes=[s["answer"] for s in gs if s.get("answer") is not None]
            # find the box whose value == solution and appears at/after phase
            if p.get("input_type")=="single_value":
                if sol[0] not in boxes:
                    issues.append(f"{tier}[{i}] solution {sol[0]} never appears as a guided box: {boxes}")
            # phase boundary live boxes
            sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
            if not sub:
                issues.append(f"{tier}[{i}] no phase boundary")
            else:
                live=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None)
                if live<2: issues.append(f"{tier}[{i}] only {live} live boxes after boundary")
        # figure numbers appear in problem text (label vs numbers)
        d=p["display"]; svg=svg_of(d); body=txt(d)
        svgn=set(nums(re.sub(r'viewBox="[^"]*"|max-width:280px|font-size="\d+"|stroke-width="[^"]*"|r="[^"]*"|cx="[^"]*"|cy="[^"]*"|x1="[^"]*"|y1="[^"]*"|x2="[^"]*"|y2="[^"]*"|x="[^"]*"|y="[^"]*"|A0 0|60a5fa|0.16|1.3|1.5|1.6|2.1','',svg)))
        # crude: pull only text-node numbers
        textnodes=re.findall(r">([^<]*)</text>",svg)
        labelnums=set()
        for tn in textnodes:
            for n in nums(tn): labelnums.add(n)
        bodynums=set(nums(body))
        # every numeric label (excluding pure letters) should be justified by body OR be a known derived answer
        allowed=bodynums | {str(expect_sol.get(key,"")), str(sol[0])}
        for ln in labelnums:
            if ln not in bodynums:
                issues.append(f"{tier}[{i}] figure label '{ln}' not in problem text: {body[:70]!r}")
        # misconception expects
        for m in p.get("misconceptions",[]):
            if "expect" not in m: issues.append(f"{tier}[{i}] misc missing expect")

# opener/teach box internal check: each 'pre' that states an arithmetic 'a op b =' must equal answer
def check_walk(steps,label):
    for j,s in enumerate(steps):
        if s.get("answer") is None: continue
        pre=s.get("pre","")
        prez=pre.replace("−","-")
        # only check strict two-operand expressions (skip 3+ term check sums)
        tail=prez.split("=")[0]
        if len(re.findall(r"-?\d+",tail))!=2:
            continue
        m=re.search(r"(-?\d+)\s*([+\-×÷x])\s*(-?\d+)\s*=\s*$",prez)
        if m:
            a,op,b=int(m.group(1)),m.group(2),int(m.group(3))
            val={"+":a+b,"-":a-b,"×":a*b,"x":a*b,"÷":a//b if b and a%b==0 else (a/b if b else None)}[op]
            if val!=s["answer"]:
                issues.append(f"{label}[{j}] '{pre.strip()}' computes {val} != box {s['answer']}")

check_walk(pd["guided"]["opener"]["steps"],"opener")
for t in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][t]["steps"],f"teach.{t}")
    for i,p in enumerate(pb[t]):
        if p.get("guided_steps"): check_walk(p["guided_steps"],f"{t}[{i}].gs")

print("ISSUES:",len(issues))
for x in issues: print("  -",x)
if not issues: print("ALL CLEAN")
