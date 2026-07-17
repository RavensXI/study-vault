import json, os, urllib.request

ID = "e16ccba1-6dc0-4321-835b-98ec18acce00"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_CHK_L07_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "count", len(pb[t]))

# find predump entry
for fn in ["_pre_dump_maths-ocr.json"]:
    try:
        predump = json.load(open(fn))
        print("predump type", type(predump))
        if isinstance(predump, dict):
            print("predump keys sample", list(predump.keys())[:5])
    except Exception as e:
        print("predump err", e)
