import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre = json.load(open("_pre_L12.json",encoding="utf-8"))
live = json.load(open("_live_L12.json",encoding="utf-8"))
pw=pre["worked_examples"]; lw=live["worked_examples"]
for i in range(4):
    a=pw[i]; b=lw[i]
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if json.dumps(sa,ensure_ascii=False)!=json.dumps(sb,ensure_ascii=False):
            print(f"we[{i}].steps[{j}]")
            print("  PRE :",repr(sa.get("content")))
            print("  LIVE:",repr(sb.get("content")))
