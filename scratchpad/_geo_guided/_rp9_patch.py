import os, io, json, urllib.request
ID = "2aeee60b-5e2f-4781-8455-e81739317bf9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HERE = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided"
pd = json.load(io.open(os.path.join(HERE, "lesson_L09.json"), encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH", r.status)

# verify
req2 = urllib.request.Request(url + "&select=practice_data",
                              headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
got = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("roundtrip identical:", got == pd)
