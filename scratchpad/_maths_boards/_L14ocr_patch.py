import os, json, io, urllib.request

ID = "da768b8a-d62b-4701-8423-7988dc8325a7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/lesson_maths-ocr_algebra-L14.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
url2 = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live bronze[6] display:", live["problem_bank"]["bronze"][6]["display"])
print("live bronze[7] sol:", live["problem_bank"]["bronze"][7]["solutions"])
print("live gold[2] guided_steps boxes:", sum(1 for s in live["problem_bank"]["gold"][2]["guided_steps"] if s.get("answer") is not None))
