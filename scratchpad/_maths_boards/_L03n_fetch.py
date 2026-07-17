import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "9e521b4c-a8d3-47d8-ac6b-1ce35dabf977"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_L03n_live.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    arr = pb.get(t) or pd.get(t)
    if isinstance(arr, list):
        print(t, "n=", len(arr))
