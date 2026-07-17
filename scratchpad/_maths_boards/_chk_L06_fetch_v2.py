import json, os, urllib.request

ID = "0a7ff82d-058f-480c-86fe-63a16ac98dc5"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
json.dump(row["practice_data"], open("_chk_L06_live_v2.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "problems:", len(pb[t]))
