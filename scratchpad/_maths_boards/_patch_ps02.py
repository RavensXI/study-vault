import os, json, io, urllib.request
ID="ec35471d-bdb2-419a-9f86-1b8b85d6d5a7"
sk=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-aqa_probability-statistics-L02.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":sk,"Authorization":"Bearer "+sk,"Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify readback
u2="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req2=urllib.request.Request(u2,headers={"apikey":sk,"Authorization":"Bearer "+sk})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback keys:", list(back.keys()))
print("guided present:", "guided" in back, "| tier_guides present:", "tier_guides" in back)
print("gold[1] has svg:", "<svg" in back["problem_bank"]["gold"][1]["display"])
print("bronze[0] expect:", back["problem_bank"]["bronze"][0]["misconceptions"][0]["expect"])
