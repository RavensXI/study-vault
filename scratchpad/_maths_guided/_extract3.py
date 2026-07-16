import json
ID="4aa9afe1-7e47-4f0f-b7e6-da22be472716"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
p=[x for x in pre if x["id"]==ID][0]
pd=p["practice_data"]
print("title:",p["title"])
print("pre practice_data keys:",list(pd.keys()))
open("_pre_L06.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
# preservation-relevant fields
for f in ["related_videos","topic_links","worked_examples"]:
    print("---",f,"---")
    print(json.dumps(pd.get(f),ensure_ascii=False)[:400])
