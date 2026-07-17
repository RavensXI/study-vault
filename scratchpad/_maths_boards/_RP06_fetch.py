import json, os, urllib.request

ID = "ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_RP06_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("top-level keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs = pb.get(t) or pd.get(t)
    if isinstance(probs, list):
        print(t, "->", len(probs), "problems")
