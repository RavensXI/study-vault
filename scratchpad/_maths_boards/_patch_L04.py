import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="6a2afcf8-1c03-4b07-b228-3999deb3d402"
pd=json.load(io.open("lesson_maths-ocr_number-L04.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify readback
url2=url+"&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("silver solutions:", [p["solutions"] for p in live["problem_bank"]["silver"]])
print("bronze n/silver n/gold n:", len(live["problem_bank"]["bronze"]),len(live["problem_bank"]["silver"]),len(live["problem_bank"]["gold"]))
