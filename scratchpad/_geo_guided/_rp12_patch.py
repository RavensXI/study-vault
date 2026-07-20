import os, json, io, urllib.request
ID = "3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L12.json"), encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("status", r.status)
# verify
req2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
back = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("silver[3].solutions", back["problem_bank"]["silver"][3]["solutions"])
print("gold[4].gs[2].answer", back["problem_bank"]["gold"][4]["guided_steps"][2]["answer"])
print("identical:", json.dumps(back, sort_keys=True) == json.dumps(pd, sort_keys=True))
