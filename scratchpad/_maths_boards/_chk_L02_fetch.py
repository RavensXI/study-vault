import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "cbc91397-a67c-472a-b0da-308aa9da1653"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,slug,title,practice_data"
req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
with open("_CHK_L02_live.json","w",encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
row = data[0]
print("title:", row["title"], "| slug:", row["slug"])
pd = row["practice_data"]
print("keys:", list(pd.keys()))
