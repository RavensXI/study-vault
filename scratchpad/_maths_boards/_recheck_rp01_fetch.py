import os, json, urllib.request
SID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{SID}&select=practice_data,slug,title,unit_id"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
pd = row["practice_data"]
with open("_recheck_rp01_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
