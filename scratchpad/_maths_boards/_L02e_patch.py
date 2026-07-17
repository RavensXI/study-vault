import os, json, urllib.request
ID = "09c2b39e-ac37-4058-8de3-22b163764aa7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-eduqas_number-L02.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)
# verify round-trip
req2 = urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live keys:", sorted(live.keys()))
print("bronze count:", len(live["problem_bank"]["bronze"]), "has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("opener svg present:", "<svg" in live["guided"]["opener"]["steps"][0]["say"])
