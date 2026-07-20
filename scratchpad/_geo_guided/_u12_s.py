import json,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
pd=json.load(open("_u12_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        print(tier,i,"| input_type:",p.get("input_type"),"| ruler:",p.get("ruler"),"| solutions:",json.dumps(p.get("solutions"),ensure_ascii=False)[:250])
