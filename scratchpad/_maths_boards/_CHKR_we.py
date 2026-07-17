import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="fc1f101a-9d1b-4eab-8bf8-8159f78caea2"
live=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
pre=[v for v in json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8")) if v.get("id")==ID][0]["practice_data"]
print("PRE worked_examples:")
print(json.dumps(pre.get("worked_examples"),ensure_ascii=False,indent=1))
print("\nLIVE worked_examples:")
print(json.dumps(live.get("worked_examples"),ensure_ascii=False,indent=1))
# also check related_videos and topic_links raw
print("\nrelated_videos live:",json.dumps(live.get("related_videos"),ensure_ascii=False))
print("topic_links live:",json.dumps(live.get("topic_links"),ensure_ascii=False))
