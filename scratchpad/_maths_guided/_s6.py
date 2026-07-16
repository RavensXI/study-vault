import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_live_graphsL01.json"))
p=pd["problem_bank"]["silver"][6]
print(json.dumps(p,ensure_ascii=False,indent=1))
