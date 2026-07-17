# -*- coding: utf-8 -*-
import json,sys
io=sys.stdout
live=json.load(open("_chk_L06_live_v2.json",encoding="utf-8"))
pre=[e for e in json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8")) if e.get("id")=="0a7ff82d-058f-480c-86fe-63a16ac98dc5"][0]
ppd=pre.get("practice_data",pre)
pw=ppd["worked_examples"]; lw=live["worked_examples"]
def normlab(s): return s.replace(" — ",": ").replace("—",":")
diffs=[]
for i,(a,b) in enumerate(zip(pw,lw)):
    if a.get("question")!=b.get("question"): diffs.append(f"WE{i} question changed: {a.get('question')} -> {b.get('question')}")
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa.get("content")!=sb.get("content"): diffs.append(f"WE{i}.step{j} content changed:\n  {sa.get('content')}\n  {sb.get('content')}")
        la,lb=sa.get("label",""),sb.get("label","")
        if la!=lb:
            tag = "OK(em-dash->colon)" if normlab(la)==lb else "UNEXPECTED"
            diffs.append(f"WE{i}.step{j} label {tag}: '{la}' -> '{lb}'")
io.write("\n".join(diffs) if diffs else "identical\n")
io.write("\n")
