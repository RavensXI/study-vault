import os, json, urllib.request

ID = "74d5f6d6-9036-4da3-adf3-d7e2c86fc6b4"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
with open("_live_psL03.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, ensure_ascii=False, indent=2)
print("title:", data[0].get("title"))
print("slug:", data[0].get("slug"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
