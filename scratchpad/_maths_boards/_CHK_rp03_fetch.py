import os, json, urllib.request

ID = "689bc7ff-0d4c-4f20-a83c-9476935f2ac9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
with open("_CHK_rp03_live.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"))
print("slug:", data[0].get("slug"))
print("keys:", list(data[0]["practice_data"].keys()))
