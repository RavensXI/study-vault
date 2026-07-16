import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
live=json.load(open("_live_L05.json",encoding="utf-8"))
ID="75d6eee2-25e6-4977-b549-e965ddd6c735"
entry=next(v for v in pre if v.get("id")==ID)
pw=entry["practice_data"]["worked_examples"]; lw=live["worked_examples"]
a=pw[2]; b=lw[2]
print("PRE :",json.dumps(a,ensure_ascii=False,indent=1))
print("LIVE:",json.dumps(b,ensure_ascii=False,indent=1))
