import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="55a5af04-f88a-4be7-b4c0-7f89c607e266"
pd=json.load(io.open("lesson_maths-aqa_algebra-L03.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# round-trip verify
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
back=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("roundtrip guided present:", "guided" in back and "tier_guides" in back)
print("bronze[0] expects:", [m["expect"] for m in back["problem_bank"]["bronze"][0]["misconceptions"]])
