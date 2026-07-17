import os, json, urllib.request

ID = "2e75898f-577a-42bd-b94e-f1435e89ace3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_ADVCHK_L05_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb and isinstance(pb[t], list):
        print(t, "count", len(pb[t]))
