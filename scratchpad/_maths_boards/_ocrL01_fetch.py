import os, json, io, urllib.request

LID = "d8a78aa2-a642-4dcd-9cb0-1aa5990761e7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, io.open("_ocrL01_live.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ["bronze", "silver", "gold"]:
    arr = pb.get(t, [])
    print(f"\n=== {t} ({len(arr)}) ===")
    for i, p in enumerate(arr):
        print(f"[{i}] input={p.get('input_type')} calc={p.get('calculator')}")
        print("    display:", p.get("display"))
        print("    solutions:", p.get("solutions"))
        if p.get("options"): print("    options:", p.get("options"))
