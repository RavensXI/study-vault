import os, json, urllib.request

ID = "0334612d-1b10-4495-8d37-21ef41d3a925"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
with open("_CHK_gL04_live.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("slug:", data[0].get("slug"), "title:", data[0].get("title"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    if isinstance(pb.get(t), list):
        print(t, "problems:", len(pb[t]))
