import os, json, urllib.request

ID = "7134e062-5209-4de5-894e-c315dc3ee9d0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,slug,title,unit_id,practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
with open("_CHK_gL02ocr_live.json", "w", encoding="utf-8") as f:
    json.dump(row, f, ensure_ascii=False, indent=1)
pd = row["practice_data"]
print("slug:", row["slug"], "title:", row["title"])
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t)
    if isinstance(probs, list):
        print(f"  {t}: {len(probs)} problems")
