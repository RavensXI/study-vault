import os, json, urllib.request

ID = "da15f5f9-2162-4b08-b990-ac2efa64f13a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_L04ocr_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("OK keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
if isinstance(pb, dict):
    for t in ("bronze","silver","gold"):
        arr = pb.get(t)
        if isinstance(arr, list):
            print(t, len(arr))
