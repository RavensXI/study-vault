import json
live=json.load(open("_CHK_L05_live.json",encoding="utf-8"))
pre=json.load(open("_CHK_L05_predump.json",encoding="utf-8"))
lw=live["worked_examples"]; pw=pre["worked_examples"]
def norm(o): # strip em dash / arrow differences
    s=json.dumps(o,ensure_ascii=False,sort_keys=True)
    return s.replace("—",":").replace(" : "," : ")
for i,(a,b) in enumerate(zip(pw,lw)):
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa!=sb:
            print(f"we[{i}].steps[{j}] label PRE={sa.get('label')!r} NOW={sb.get('label')!r} | content same? {sa.get('content')==sb.get('content')}")
    if a["question"]!=b["question"]:
        print(f"we[{i}] question PRE={a['question']!r} NOW={b['question']!r}")
print("counts pre/live", len(pw), len(lw))
