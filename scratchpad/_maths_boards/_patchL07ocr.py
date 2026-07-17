import json, os, urllib.request

ID = "e16ccba1-6dc0-4321-835b-98ec18acce00"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-ocr_number-L07.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
url2 = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
got = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got)
print("bronze[0] has guided_steps:", bool(got["problem_bank"]["bronze"][0].get("guided_steps")))
print("opener has svg:", "<svg" in got["guided"]["opener"]["display"])
print("round-trip equal:", got == pd)
