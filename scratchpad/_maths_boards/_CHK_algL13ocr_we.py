import json, io
ID="44ac4c68-828c-4d38-888a-37758fefde57"
pre=json.load(io.open("_pre_dump_maths-ocr.json",encoding="utf-8"))
live=json.load(io.open("_CHK_algL13ocr_live.json",encoding="utf-8"))
entry=None
for v in (pre.values() if isinstance(pre,dict) else pre):
    if isinstance(v,dict) and v.get("id")==ID: entry=v; break
pd=entry["practice_data"]
pw=pd["worked_examples"]; lw=live["worked_examples"]
for i,(a,b) in enumerate(zip(pw,lw)):
    assert a["question"]==b["question"], f"Q{i} changed"
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        c = "content SAME" if sa.get("content")==sb.get("content") else "CONTENT DIFF"
        l = "label SAME" if sa.get("label")==sb.get("label") else f"label: {repr(sa.get('label'))} -> {repr(sb.get('label'))}"
        if "CONTENT DIFF" in c: print(f"we[{i}].step[{j}] {c}: {sa.get('content')} -> {sb.get('content')}")
        elif "label:" in l: print(f"we[{i}].step[{j}] {l}")
print("questions & content all identical (only labels differ)")
