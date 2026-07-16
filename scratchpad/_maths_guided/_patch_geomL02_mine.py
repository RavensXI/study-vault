import os,json,io,urllib.request
ID="fe5f6191-4452-4313-934d-8e5d16ba1032"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_geometry-L02.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify
url2=url+"&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("verify B4 sols", back["problem_bank"]["bronze"][4]["solutions"])
print("verify has guided", "guided" in back, "tier_guides", "tier_guides" in back)
print("verify G0 msg tail", back["problem_bank"]["gold"][0]["misconceptions"][0]["message"][-20:])
