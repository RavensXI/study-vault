# -*- coding: utf-8 -*-
import json, io
base = json.load(io.open(r"_L04ocr_live.json", encoding="utf-8"))
new  = json.load(io.open(r"lesson_maths-ocr_algebra-L04.json", encoding="utf-8"))

problems = 0
errs = []

# preservation: displays/options/solutions unchanged
for tier in ("bronze","silver","gold"):
    for i,(a,c) in enumerate(zip(base["problem_bank"][tier], new["problem_bank"][tier])):
        if a["display"] != c["display"]:
            errs.append(f"{tier}[{i}] display changed")
        if a.get("solutions") != c.get("solutions"):
            errs.append(f"{tier}[{i}] solutions changed {a.get('solutions')}->{c.get('solutions')}")
        if a.get("options") != c.get("options"):
            errs.append(f"{tier}[{i}] options changed")

if base.get("related_videos") != new.get("related_videos"):
    errs.append("related_videos changed")
if base.get("topic_links") != new.get("topic_links"):
    errs.append("topic_links changed")
# worked_examples: only labels de-emdashed
for i,(a,c) in enumerate(zip(base["worked_examples"], new["worked_examples"])):
    if a["question"] != c["question"]:
        errs.append(f"worked_examples[{i}] question changed")

# every non-MC final guided box lands on solution; expects != solution
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(new["problem_bank"][tier]):
        if p.get("input_type") == "multiple_choice":
            for m in p.get("misconceptions",[]):
                if m.get("expect") is not None:
                    errs.append(f"{tier}[{i}] MC expect not null")
            continue
        problems += 1
        sol = p["solutions"][0]
        gs = p.get("guided_steps",[])
        boxes = [s for s in gs if s.get("answer") is not None]
        if not boxes:
            errs.append(f"{tier}[{i}] no boxes"); continue
        if boxes[-1]["answer"] != sol:
            errs.append(f"{tier}[{i}] last box {boxes[-1]['answer']} != sol {sol}")
        # phase present
        if not any(s.get("phase")=="substitute" for s in gs):
            errs.append(f"{tier}[{i}] no phase boundary")
        for m in p.get("misconceptions",[]):
            e = m.get("expect")
            if e is not None and abs(float(e)-float(sol))<1e-9:
                errs.append(f"{tier}[{i}] expect {e} == sol")

# teach walks land correctly (manual expected finals)
teach_final = {"bronze":11,"silver":-4,"gold":21}
for t,exp in teach_final.items():
    boxes=[s for s in new["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if boxes[-1]["answer"]!=exp:
        errs.append(f"teach {t} final {boxes[-1]['answer']} != {exp}")

print("single_value problems with walks:", problems)
if errs:
    print("ERRORS:")
    for e in errs: print("  -", e)
else:
    print("ALL CHECKS PASS")
