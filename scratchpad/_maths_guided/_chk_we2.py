import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_graphsL08_live.json",encoding="utf-8"))
pre=json.load(open("_CHK_graphsL08_predump.json",encoding="utf-8"))
for i,(a,b) in enumerate(zip(live["worked_examples"],pre["worked_examples"])):
    la=json.dumps(a,ensure_ascii=False); lb=json.dumps(b,ensure_ascii=False)
    if la!=lb:
        print(f"--- WE[{i}] ---")
        for sa,sb in zip(a["steps"],b["steps"]):
            if sa!=sb:
                print("  live label:",repr(sa.get("label")))
                print("  pre  label:",repr(sb.get("label")))
                if sa.get("content")!=sb.get("content"):
                    print("  live content:",sa.get("content"))
                    print("  pre  content:",sb.get("content"))
        if a.get("question")!=b.get("question"):
            print("  Q live:",a.get("question"))
            print("  Q pre :",b.get("question"))
