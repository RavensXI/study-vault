import os,json,io,urllib.request
ID="f4814142-6434-44c9-9458-6b95f1e27ec6"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-aqa_algebra-L14.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
# verify
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live G5 sol:", live["problem_bank"]["gold"][3]["solutions"])
print("live gold[3] display:", live["problem_bank"]["gold"][3]["display"][:60])
