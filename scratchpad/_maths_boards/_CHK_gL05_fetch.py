import os, json, urllib.request

LID = "2d827ad4-80ab-4327-81f8-a2e5cec4f50a"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,slug,title,unit_id"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))[0]
with open("_CHK_gL05_live.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("title:", data.get("title"), "slug:", data.get("slug"))
pd = data["practice_data"]
print("top keys:", list(pd.keys()))
