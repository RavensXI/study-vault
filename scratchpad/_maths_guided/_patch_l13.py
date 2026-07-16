import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "a33d3e1a-9399-4ea4-9132-b391a705d6a7"
pd = json.load(io.open("lesson_algebra-L13.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read back to confirm
req2 = urllib.request.Request(url + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in got)
print("has tier_guides:", "tier_guides" in got)
print("bronze[6] display:", got["problem_bank"]["bronze"][6]["display"][:40])
print("silver[5] display:", got["problem_bank"]["silver"][5]["display"][:40])
print("silver[4] hint:", got["problem_bank"]["silver"][4]["hint"])
print("gold_description:", got["problem_bank"]["gold_description"])
print("roundtrip identical:", json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True))
