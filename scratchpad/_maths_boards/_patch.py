import os, json, urllib.request
ID="89062264-f404-4e8e-8959-06c7a9fd0b7a"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_geometry-L01.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
# verify
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live gold[1] solutions:",back["problem_bank"]["gold"][1]["solutions"])
print("live has tier_guides:", "tier_guides" in back, "| has guided:", "guided" in back)
print("live opener boxes:",[s.get("answer") for s in back["guided"]["opener"]["steps"] if s.get("answer") is not None])
print("svg count in live:", json.dumps(back).count("<svg"))
