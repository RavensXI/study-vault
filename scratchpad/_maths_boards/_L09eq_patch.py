import os, json, urllib.request

LID = "038c2343-8acf-41e4-b02a-914268bc6572"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-eduqas_algebra-L09.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
pb = live["problem_bank"]
print("live tier sizes:", {t: len(pb[t]) for t in ("bronze","silver","gold")})
print("live has guided:", "guided" in live, " tier_guides:", "tier_guides" in live)
print("b0 input_type:", pb["bronze"][0]["input_type"], " sol:", pb["bronze"][0]["solutions"])
print("worked_examples preserved:", len(live.get("worked_examples") or []))
print("match written == live:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
