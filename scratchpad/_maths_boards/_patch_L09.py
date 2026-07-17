import os, json, urllib.request
ID="5ff3e1eb-2284-4096-af06-4bcb6754b0e1"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_algebra-L09.json", encoding="utf-8"))
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":"Bearer "+key,
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status", r.status)
# verify readback
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":key,"Authorization":"Bearer "+key})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback keys:", sorted(back.keys()))
print("has guided:", "guided" in back, "tier_guides:", "tier_guides" in back)
print("bronze sols:", [p["solutions"] for p in back["problem_bank"]["bronze"]])
print("all xy_pair:", all(p.get("input_type")=="xy_pair" for t in ("bronze","silver","gold") for p in back["problem_bank"][t]))
