import os, json, urllib.request
ID="bc2b18ec-48ee-4af7-b9f4-875e7ef56db0"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
row=data[0]
pd=row["practice_data"]
open("_live_L02_v2.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("title:", row.get("title"))
print("slug:", row.get("slug"))
print("related_videos[0]:", pd["related_videos"][0]["title"])
print("topic_links:", pd["topic_links"])
print("bronze[0] display:", pd["problem_bank"]["bronze"][0]["display"])
print("keys:", list(pd.keys()))
