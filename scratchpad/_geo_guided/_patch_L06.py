import os, io, json, urllib.request

ID = "64b88a88-ec47-40c2-9478-1f7ba7572096"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L06.json"), encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify
req2 = urllib.request.Request(url + "&select=practice_data",
                              headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
got = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("keys:", sorted(got.keys()))
print("guided present:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("descriptions:", all(got["problem_bank"].get(t + "_description") for t in ("bronze", "silver", "gold")))
print("identical to file:", json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True))
n = sum(1 for t in ("bronze", "silver", "gold") for p in got["problem_bank"][t] if p.get("guided_steps"))
print("problems with guided_steps:", n)
print("charts:", sum(1 for t in ("bronze", "silver", "gold") for p in got["problem_bank"][t] if p.get("chart")))
