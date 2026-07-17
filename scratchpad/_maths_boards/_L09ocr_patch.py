import os, json, io, urllib.request

ID = "ee2766ef-5043-457b-b6b3-4e38d5ed9d0e"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_algebra-L09.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(vreq) as r:
    live = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze:", len(live["problem_bank"]["bronze"]), "silver:", len(live["problem_bank"]["silver"]), "gold:", len(live["problem_bank"]["gold"]))
print("input types:", set(p["input_type"] for t in ("bronze","silver","gold") for p in live["problem_bank"][t]))
print("round-trip equal:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
