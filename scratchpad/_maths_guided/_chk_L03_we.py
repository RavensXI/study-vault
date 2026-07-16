import json
live = json.load(open("_CHK_L03_live.json", encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID = "36364705-212f-4a63-a56c-839f1e986dc2"
entry = None
for e in (dump if isinstance(dump, list) else dump.values()):
    if isinstance(e, dict) and e.get("id") == ID:
        entry = e; break
pd = entry["practice_data"]
pre = pd["worked_examples"]
liv = live["worked_examples"]
print("count pre", len(pre), "live", len(liv))
for i,(a,b) in enumerate(zip(pre,liv)):
    for j,(sa,sb) in enumerate(zip(a["steps"], b["steps"])):
        # normalise em dash to colon-ish for comparison
        la, lb = sa.get("label",""), sb.get("label","")
        if la != lb:
            print(f"we[{i}].steps[{j}].label: PRE={la!r} LIVE={lb!r}")
        if sa.get("content") != sb.get("content"):
            print(f"we[{i}].steps[{j}].content DIFF: PRE={sa.get('content')!r} LIVE={sb.get('content')!r}")
    if a.get("question")!=b.get("question"):
        print(f"we[{i}].question DIFF: {a.get('question')!r} vs {b.get('question')!r}")
    if a.get("difficulty")!=b.get("difficulty"):
        print(f"we[{i}].difficulty DIFF")
print("done")
