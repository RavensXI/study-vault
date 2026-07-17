import json, os, urllib.request

ID = "4fd08300-e0fe-44c5-93cd-76b6d900c72d"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_CHKR_L05_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "count", len(pb[t]))
# pre-dump
predump = json.load(open("_pre_dump_maths-ocr.json"))
print("predump type", type(predump))
