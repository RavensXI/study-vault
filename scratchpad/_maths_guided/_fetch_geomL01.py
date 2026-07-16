import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
lid = "65f2d938-335c-4d09-9917-f888f5a7c23e"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{lid}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
open("_CHK_geomL01_live.json","w",encoding="utf-8").write(json.dumps(data[0], ensure_ascii=False, indent=2))
print("slug:", data[0].get("slug"), "| title:", data[0].get("title"))
