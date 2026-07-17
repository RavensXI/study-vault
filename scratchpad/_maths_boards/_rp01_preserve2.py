# -*- coding: utf-8 -*-
import json, io
pre_all = json.load(io.open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
ID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
# pre_dump structure: find entry for this id
pre = None
if isinstance(pre_all, dict):
    if ID in pre_all: pre = pre_all[ID]
    elif "ratio-proportion-L01" in pre_all: pre = pre_all["ratio-proportion-L01"]
    else:
        for k,v in pre_all.items():
            if isinstance(v,dict) and v.get("id")==ID: pre=v.get("practice_data",v); break
elif isinstance(pre_all, list):
    for v in pre_all:
        if v.get("id")==ID: pre=v.get("practice_data"); break
if pre and "practice_data" in pre: pre = pre["practice_data"]
print("pre found:", pre is not None)
new = json.load(io.open("lesson_maths-eduqas_ratio-proportion-L01.json", encoding="utf-8"))
if pre:
    # related_videos & topic_links unchanged
    print("related_videos same:", pre.get("related_videos")==new.get("related_videos"))
    print("topic_links same:", pre.get("topic_links")==new.get("topic_links"))
    # worked_examples: only labels changed (em dash->colon), content/questions same
    pw, nw = pre.get("worked_examples",[]), new.get("worked_examples",[])
    print("worked_examples count same:", len(pw)==len(nw))
    ok=True
    for a,b in zip(pw,nw):
        if a.get("question")!=b.get("question") or a.get("difficulty")!=b.get("difficulty"): ok=False
        for sa,sb in zip(a.get("steps",[]),b.get("steps",[])):
            if sa.get("content")!=sb.get("content"): ok=False
    print("worked_examples questions+content preserved:", ok)
    # displays/options/solutions preserved for every problem
    dok=True
    for tier in ("bronze","silver","gold"):
        for pa,pb in zip(pre["problem_bank"][tier], new["problem_bank"][tier]):
            if pa.get("display")!=pb.get("display"): dok=False
            if pa.get("options")!=pb.get("options"): dok=False
            if pa.get("solutions")!=pb.get("solutions"): dok=False
            if pa.get("input_type")!=pb.get("input_type"): dok=False
    print("all displays/options/solutions/input_type preserved:", dok)
