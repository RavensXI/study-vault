import os, json, urllib.request

LID = "a28fddf4-3ee1-48dc-b138-aa17facad15d"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_REVCHK_L01_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

s1 = pd["problem_bank"]["silver"][1]
print("DISPLAY:", s1["display"].split("<br>")[-1][:120])
print("SOLUTIONS:", s1["solutions"])
print("MISCONCEPTIONS:", json.dumps(s1["misconceptions"], ensure_ascii=False, indent=1))
