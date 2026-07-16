import json,io,sys,difflib
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="4aa9afe1-7e47-4f0f-b7e6-da22be472716"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
pre_pd=[x for x in pre if x["id"]==ID][0]["practice_data"]
live=json.load(open("_L06_fresh.json",encoding="utf-8"))
a=json.dumps(pre_pd["worked_examples"],ensure_ascii=False,indent=1)
b=json.dumps(live["worked_examples"],ensure_ascii=False,indent=1)
for l in difflib.unified_diff(a.splitlines(),b.splitlines(),lineterm="",fromfile="PRE",tofile="LIVE"):
    print(l)
