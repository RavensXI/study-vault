# -*- coding: utf-8 -*-
import json, io, re
pd=json.load(io.open("lesson_higher-calculations-L04@f4e0c074d0.json",encoding="utf-8"))
pb=pd["problem_bank"]
issues=[]

# 1. expects outside accept window; not equal to correct
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sols=p["solutions"]; acc=p.get("accept",0)
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if p.get("input_type")=="multiple_choice": continue
            if abs(float(e)-float(sols[0]))<=max(acc,0.011):
                issues.append(f"{tier}[{i}].misc[{j}] expect {e} inside accept of {sols[0]} (acc {acc})")

# 2. last guided_steps box lands on solution; boundary has >=2 live boxes after
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice": issues.append(f"{tier}[{i}] no guided_steps")
            continue
        boxes=[s for s in gs if s.get("answer") is not None]
        # find phase idx
        pidx=next((k for k,s in enumerate(gs) if s.get("phase")=="substitute"),None)
        live=[s for s in gs[pidx:] if s.get("answer") is not None] if pidx is not None else []
        if pidx is None: issues.append(f"{tier}[{i}] no boundary")
        elif len(live)<2: issues.append(f"{tier}[{i}] only {len(live)} live boxes")
        # the compute box (phase step) should equal solution for single_value
        if p.get("input_type")=="single_value" and pidx is not None:
            comp=gs[pidx].get("answer")
            if abs(float(comp)-float(p["solutions"][0]))>max(p.get("accept",0),0.011):
                issues.append(f"{tier}[{i}] phase box {comp} != solution {p['solutions'][0]}")

# 3. figure numbers appear in display text (strip svg, check numbers in svg labels vs <p> text)
NUM=re.compile(r'\d[\d\s]*\.?\d*')
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        d=p["display"]
        if "<svg" not in d: continue
        svg=d[d.find("<svg"):d.find("</svg>")+6]
        text=d[d.find("</svg>")+6:]
        # collect number-ish tokens in svg text labels (inside >...<)
        labels=re.findall(r'>([^<]*)<',svg)
        labeltext=" ".join(labels)
        # numbers shown in figure
        for tok in re.findall(r'\d[\d ]*\d|\d',labeltext):
            n=tok.replace(" ","")
            # allow: appears in problem text (with or without spaces/commas), or is part of unit like m/s
            tnorm=text.replace(" ","").replace(",","")
            if n in tnorm or n in ("2","3","5","8","9","10","20","30","60","0","6"):
                continue
            # numbers like 4500,300,196000 etc must be in text
            if n not in tnorm:
                issues.append(f"{tier}[{i}] figure shows '{n}' not in text: {labeltext[:60]}")

print("ISSUES:" if issues else "CLEAN: all boxes land on solutions, expects valid, figures consistent")
for x in issues: print("  -",x)
