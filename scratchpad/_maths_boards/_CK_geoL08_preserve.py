import json
live=json.load(open("_CK_geoL08_live.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
ID="3e214279-84c2-41dc-a639-94bda78e2da8"
row=[r for r in pre if r["id"]==ID]
print("found predump row:",len(row))
if not row:
    # match by title
    row=[r for r in pre if r.get("title")=="Vectors"]
    print("by title:",len(row),[r["id"] for r in row])
pp=row[0]["practice_data"]
print("pre keys:",sorted(pp.keys()))
print("live keys:",sorted(live.keys()))
import json as j
for f in ["related_videos","topic_links","worked_examples"]:
    same = j.dumps(pp.get(f),sort_keys=True,ensure_ascii=False)==j.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE:", j.dumps(pp.get(f),ensure_ascii=False)[:400])
        print("  LIVE:",j.dumps(live.get(f),ensure_ascii=False)[:400])
