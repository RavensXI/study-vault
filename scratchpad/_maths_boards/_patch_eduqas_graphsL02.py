import os, json, io, urllib.request

ID = "8cd3697d-8a79-488d-87f0-7e8f6a40ddbb"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L02.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
rurl = f"{url}&select=practice_data"
rreq = urllib.request.Request(rurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(rreq) as r:
    live = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("gold0 svg live:", "<svg" in live["problem_bank"]["gold"][0]["display"])
print("bronze0 has guided_steps:", bool(live["problem_bank"]["bronze"][0].get("guided_steps")))
