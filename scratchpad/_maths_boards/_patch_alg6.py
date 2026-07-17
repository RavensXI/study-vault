import os, json, urllib.request

LID = "7104a3b3-00b8-40c8-a875-0f55043cc6b8"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-aqa_algebra-L06.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
url2 = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live top keys:", sorted(live.keys()))
print("guided present:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze sols:", [p["solutions"][0] for p in live["problem_bank"]["bronze"]])
print("worked_examples preserved:", len(live.get("worked_examples", [])))
