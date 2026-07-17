import json, os, urllib.request

ID = "47a41e5d-3d22-45fd-a1c0-b29405585d87"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
pd = row["practice_data"]
json.dump(pd, open("_CHK_L08_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "count", len(pb[t]))
