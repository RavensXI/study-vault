import os, json, urllib.request

ID = "89689a46-7251-4c2a-900e-5fdc240dafd3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
with open("_chk_gL01_live.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"), "slug:", data[0].get("slug"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
