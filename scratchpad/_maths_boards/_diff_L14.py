import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="da768b8a-d62b-4701-8423-7988dc8325a7"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
entry=[r for r in pre if r.get("id")==ID][0]["practice_data"]
live=json.load(open("_live_L14.json",encoding="utf-8"))
print("=== PRE worked_examples ===")
print(json.dumps(entry.get("worked_examples"),ensure_ascii=False,indent=1))
print("\n=== PRE method_card ===")
print(json.dumps(entry.get("method_card"),ensure_ascii=False,indent=1))
