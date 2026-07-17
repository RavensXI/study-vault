import os, json, urllib.request

LID = "1422954b-1171-49c2-a0c0-d5a1feb0da0d"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_algL08ocr_live.json", "w", encoding="utf-8") as f:
    json.dump(row, f, indent=1, ensure_ascii=False)
print("slug:", row.get("slug"), "| title:", row.get("title"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    arr = pb.get(t, [])
    print(f"\n=== {t}: {len(arr)} problems ===")
    for i, p in enumerate(arr):
        print(f"  [{i}] disp={p.get('display')!r}")
        print(f"      sol={p.get('solutions')} it={p.get('input_type')} calc={p.get('calculator')}")
