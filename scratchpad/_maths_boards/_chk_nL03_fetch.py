import os, json, urllib.request

ID = "9e521b4c-a8d3-47d8-ac6b-1ce35dabf977"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_chk_nL03_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "count:", len(pb[t]))
