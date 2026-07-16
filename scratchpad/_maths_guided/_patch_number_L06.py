import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "f6f5708d-edf9-42e6-81d8-49c3cf282310"
pd = json.load(io.open("lesson_number-L06.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read back and confirm
r2url = f"{url}&select=practice_data"
req2 = urllib.request.Request(r2url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("live keys:", list(live.keys()))
print("silver[6] display:", live["problem_bank"]["silver"][6]["display"], live["problem_bank"]["silver"][6]["solutions"])
print("silver[4] display:", live["problem_bank"]["silver"][4]["display"], live["problem_bank"]["silver"][4]["solutions"])
print("has guided:", "guided" in live, "| has tier_guides:", "tier_guides" in live)
print("bronze_description:", live["problem_bank"].get("bronze_description"))
