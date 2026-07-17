import os, json, urllib.request

ID = "769be867-fe49-4cf1-b45f-1308b21e81dd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))[0]
with open("_chk_number_L05_live.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("slug:", data.get("slug"), "title:", data.get("title"))
pd = data["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    if t in pb:
        print(t, "problems:", len(pb[t]) if isinstance(pb[t], list) else "n/a")
