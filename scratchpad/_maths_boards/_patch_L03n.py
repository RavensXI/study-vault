import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "9e521b4c-a8d3-47d8-ac6b-1ce35dabf977"
pd = json.load(io.open("lesson_maths-eduqas_number-L03.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# read back and confirm key fields landed
url2 = f"{url}&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("has guided:", "guided" in live, "| has tier_guides:", "tier_guides" in live)
print("silver sols:", [p["solutions"][0] for p in live["problem_bank"]["silver"]])
print("gold[1] display ok:", "square number" in live["problem_bank"]["gold"][1]["display"])
