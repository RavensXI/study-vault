# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
ID="1422954b-1171-49c2-a0c0-d5a1feb0da0d"
live=json.load(io.open("_CHK_algL08ocr_live.json",encoding="utf-8"))
pre_all=json.load(io.open("_pre_dump_maths-ocr.json",encoding="utf-8"))
pre=[e for e in pre_all if e.get("id")==ID][0]["practice_data"]
pw=pre["worked_examples"]; lw=live["worked_examples"]
for i,(a,b) in enumerate(zip(pw,lw)):
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa!=sb:
            print(f"we[{i}].steps[{j}] label pre={sa.get('label')!r} live={sb.get('label')!r} content_same={sa.get('content')==sb.get('content')}")
    if a.get("question")!=b.get("question"):
        print(f"we[{i}] question changed pre={a.get('question')!r} live={b.get('question')!r}")
    if a.get("difficulty")!=b.get("difficulty"):
        print(f"we[{i}] difficulty pre={a.get('difficulty')} live={b.get('difficulty')}")
print("done")
