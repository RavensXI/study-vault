import os, json, urllib.request, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
print("LIVE related_videos:")
for v in pd["related_videos"]: print("  ",v["title"])
print("LIVE topic_links:", pd["topic_links"])
print("LIVE method_card title:", pd["method_card"]["title"])
print("has guided:", "guided" in pd, "has tier_guides:", "tier_guides" in pd)
# check saved file
saved=json.load(open("_live_L07.json",encoding="utf-8"))
print("SAVED file related_videos:")
for v in saved["related_videos"]: print("  ",v["title"])
