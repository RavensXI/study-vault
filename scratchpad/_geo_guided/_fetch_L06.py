import os, json, urllib.request

ID = "64b88a88-ec47-40c2-9478-1f7ba7572096"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_live_L06.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t) or []))
print("written", out, os.path.getsize(out))
