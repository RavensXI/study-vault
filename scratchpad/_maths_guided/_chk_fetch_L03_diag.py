import os, json, urllib.request

ID = "d168ac22-370f-4c9f-a647-85febc0e8213"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_CHK_L03_NOW.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("top keys:", list(pd.keys()))
