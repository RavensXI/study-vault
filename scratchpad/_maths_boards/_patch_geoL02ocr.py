import os, json, urllib.request
ID = "7134e062-5209-4de5-894e-c315dc3ee9d0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-ocr_geometry-L02.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
req2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("guided present:", "guided" in got)
print("tier_guides present:", "tier_guides" in got)
print("bronze[0] has svg:", "<svg" in got["problem_bank"]["bronze"][0]["display"])
print("bronze[0] guided_steps:", len(got["problem_bank"]["bronze"][0]["guided_steps"]))
print("round-trip equal:", got == pd)
