import os, json, urllib.request

LID = "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_VER_live_pd.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=2, ensure_ascii=False)
print("title:", row.get("title"))
print("slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
