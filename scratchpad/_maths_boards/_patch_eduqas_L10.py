import os, json, urllib.request
SK=os.environ["SUPABASE_SERVICE_KEY"]
ID="27ec4539-cb68-4e60-ad0d-fa0828706d80"
pd=json.load(open("lesson_maths-eduqas_algebra-L10.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":SK,"Authorization":f"Bearer {SK}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify readback
u2=f"{url}&select=practice_data"
rq=urllib.request.Request(u2,headers={"apikey":SK,"Authorization":f"Bearer {SK}"})
back=json.load(urllib.request.urlopen(rq))[0]["practice_data"]
print("readback matches:", json.dumps(back,sort_keys=True)==json.dumps(pd,sort_keys=True))
print("gold[0] has svg:", "<svg" in back["problem_bank"]["gold"][0]["display"])
print("bank sizes:", {t:len(back["problem_bank"][t]) for t in ("bronze","silver","gold")})
