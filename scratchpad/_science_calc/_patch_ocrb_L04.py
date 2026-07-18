import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
pd = json.load(io.open("lesson_chemistry-calculations-L04@6f3d09988e.json", encoding="utf-8"))
ids = ["1563a319-bb93-438e-9b64-e079bd7e410a","ea8d64f3-4cf2-4568-afe6-d4d41d065f55"]
body = json.dumps({"practice_data": pd}).encode("utf-8")
for i in ids:
    url = BASE + "?id=eq.%s" % i
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer "+KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    r = urllib.request.urlopen(req)
    print(i, r.status)
