import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_graphs_l01.json",encoding="utf-8"))
pre=json.load(open("_pre_pd.json",encoding="utf-8"))
a=json.dumps(pre["worked_examples"],sort_keys=True,ensure_ascii=False)
b=json.dumps(live["worked_examples"],sort_keys=True,ensure_ascii=False)
print("worked_examples identical:", a==b)
if a!=b:
    # find per-example diffs
    for i,(o,n) in enumerate(zip(pre["worked_examples"],live["worked_examples"])):
        if json.dumps(o,sort_keys=True,ensure_ascii=False)!=json.dumps(n,sort_keys=True,ensure_ascii=False):
            print(f"WE[{i}] PRE:",json.dumps(o,ensure_ascii=False))
            print(f"WE[{i}] LIVE:",json.dumps(n,ensure_ascii=False))
print("\nmethod_card PRE steps count:",len(pre["method_card"]["steps"]),"words:",len(pre["method_card"]["content"].split()))
print("method_card LIVE steps count:",len(live["method_card"]["steps"]),"words:",len(live["method_card"]["content"].split()))
