import os, json, urllib.request
ID="5cfec765-3128-469b-9d6a-626f042d6161"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_ratio-proportion-L01.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify roundtrip
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("live keys:",list(back.keys()))
print("guided ok:", "guided" in back and "opener" in back["guided"])
print("tier_guides ok:", set(back.get("tier_guides",{}).keys())=={"bronze","silver","gold"})
print("bronze n:",len(back["problem_bank"]["bronze"]),"silver:",len(back["problem_bank"]["silver"]),"gold:",len(back["problem_bank"]["gold"]))
print("B8 display:", back["problem_bank"]["bronze"][7]["display"])
print("worked_examples preserved:", back.get("worked_examples")==pd.get("worked_examples"))
