import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
pre=json.load(open('_pre_ratio_L01.json',encoding='utf-8'))
live=json.load(open('_live_ratio_L01.json',encoding='utf-8'))
print("=== PRE method_card ===")
print(json.dumps(pre['method_card'],ensure_ascii=False,indent=1))
print("=== LIVE method_card ===")
print(json.dumps(live['method_card'],ensure_ascii=False,indent=1))
print("\n=== worked_examples equal? ===", json.dumps(pre['worked_examples'],sort_keys=True)==json.dumps(live['worked_examples'],sort_keys=True))
print("PRE we count:",len(pre['worked_examples']),"LIVE we count:",len(live['worked_examples']))
for i,(a,b) in enumerate(zip(pre['worked_examples'],live['worked_examples'])):
    if json.dumps(a,sort_keys=True)!=json.dumps(b,sort_keys=True):
        print(f"we[{i}] PRE:",json.dumps(a,ensure_ascii=False))
        print(f"we[{i}] LIVE:",json.dumps(b,ensure_ascii=False))
