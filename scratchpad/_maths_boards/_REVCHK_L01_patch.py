import os, json, urllib.request

LID = "a28fddf4-3ee1-48dc-b138-aa17facad15d"
key = os.environ["SUPABASE_SERVICE_KEY"]
ship = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_probability-statistics-L01.json"
with open(ship, encoding="utf-8") as f:
    pd = json.load(f)

url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": key, "Authorization": f"Bearer {key}"})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
mc = live["problem_bank"]["silver"][1]["misconceptions"][0]
print("LIVE expect:", mc["expect"])
print("LIVE msg has 2/15:", "12/90 = 2/15" in mc["message"])
print("LIVE msg has 1/15:", "1/15" in mc["message"])
