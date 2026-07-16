import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="4aa9afe1-7e47-4f0f-b7e6-da22be472716"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
pre_pd=[x for x in pre if x["id"]==ID][0]["practice_data"]
live=json.load(open("_L06_fresh.json",encoding="utf-8"))
for tier,idx in [("silver",1),("silver",3),("bronze",5)]:
    print(f"=== {tier}[{idx}] ===")
    print(" PRE display :",pre_pd["problem_bank"][tier][idx]["display"])
    print(" PRE sols    :",pre_pd["problem_bank"][tier][idx]["solutions"])
    print(" LIVE display:",live["problem_bank"][tier][idx]["display"])
    print(" LIVE sols   :",live["problem_bank"][tier][idx]["solutions"])
    print(" LIVE mc msg :",[m["message"] for m in live["problem_bank"][tier][idx].get("misconceptions",[])])
