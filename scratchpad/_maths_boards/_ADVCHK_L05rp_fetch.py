import os, json, urllib.request

ID = "93469b0d-2704-499c-a20b-587a84c2e214"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
with open("_ADVCHK_L05rp_live.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
pd = data[0]["practice_data"]
print("TITLE:", data[0].get("title"), "| slug:", data[0].get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb.get(t), list) else (pb.get(t,{}).get("problems") if isinstance(pb.get(t),dict) else None)
    print(t, "->", type(pb.get(t)))
