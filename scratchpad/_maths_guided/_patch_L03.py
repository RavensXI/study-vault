import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "c6b90b84-f603-4dea-8d46-f7205879bc89"
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"

pd = json.load(open("lesson_graphs-L03.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
vreq = urllib.request.Request(URL + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}", "Accept": "application/json"})
with urllib.request.urlopen(vreq) as r:
    got = json.load(r)[0]["practice_data"]
print("round-trip equal:", got == pd)
print("has guided:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("bronze[4] display:", got["problem_bank"]["bronze"][4]["display"])
print("silver[3] solutions:", got["problem_bank"]["silver"][3]["solutions"])
