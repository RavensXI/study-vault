import json
pre = json.load(open("_pre_L12.json",encoding="utf-8"))
live = json.load(open("_live_L12.json",encoding="utf-8"))
a=json.dumps(pre["worked_examples"],sort_keys=True,ensure_ascii=False)
b=json.dumps(live["worked_examples"],sort_keys=True,ensure_ascii=False)
print("sorted equal?",a==b)
# unsorted
au=json.dumps(pre["worked_examples"],ensure_ascii=False)
bu=json.dumps(live["worked_examples"],ensure_ascii=False)
print("unsorted equal?",au==bu)
