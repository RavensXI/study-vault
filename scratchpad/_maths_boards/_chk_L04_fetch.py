import os, json, urllib.request
SID = "4feee23f-c960-4264-a828-cde0f9080d45"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{SID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
pd = row["practice_data"]
with open("_live_eduqas_algebra-L04.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("title:", row.get("title"), "| slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
