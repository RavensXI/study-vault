import json
live = json.load(open("_CHK_L13_live.json", encoding="utf-8"))
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID = "a33d3e1a-9399-4ea4-9132-b391a705d6a7"
entry = [r for r in pre if r.get("id")==ID][0]
pre_we = entry["practice_data"]["worked_examples"]
live_we = live["worked_examples"]

# normalize by replacing em dash with colon in pre labels
def norm(o):
    if isinstance(o, dict): return {k:norm(v) for k,v in o.items()}
    if isinstance(o, list): return [norm(v) for v in o]
    if isinstance(o, str): return o.replace(" — ", ": ").replace("—", ":")
    return o

print("after em-dash-normalising pre labels, worked_examples SAME:",
      json.dumps(norm(pre_we), sort_keys=True) == json.dumps(live_we, sort_keys=True))

# show every differing label
for i,(a,b) in enumerate(zip(pre_we, live_we)):
    for j,(sa,sb) in enumerate(zip(a["steps"], b["steps"])):
        if sa["label"] != sb["label"]:
            print(f"  we[{i}].steps[{j}].label: {sa['label']!r} -> {sb['label']!r}")
        if sa.get("content") != sb.get("content"):
            print(f"  we[{i}].steps[{j}].content DIFF: {sa.get('content')!r} -> {sb.get('content')!r}")
    if a["question"]!=b["question"]:
        print(f"  we[{i}].question DIFF")
