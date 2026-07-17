import os, json, urllib.request
ID="32acb3ec-b5ac-410b-984c-d9008683af8e"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-eduqas_algebra-L06.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status",r.status)
# verify
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(g) as r:
    live=json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("live bronze sols:", [p["solutions"][0] for p in live["problem_bank"]["bronze"]])
print("match:", live==pd)
