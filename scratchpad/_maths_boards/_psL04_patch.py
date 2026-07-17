import os, json, io, urllib.request
ID="54d6fba0-9730-427b-917f-ca3487dc16e9"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_probability-statistics-L04.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify roundtrip
u2=f"{url}&select=practice_data"
req2=urllib.request.Request(u2,headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("roundtrip keys:",sorted(back.keys()))
print("has guided:", "guided" in back, "| tier_guides:", "tier_guides" in back)
print("bronze/silver/gold:", len(back["problem_bank"]["bronze"]),len(back["problem_bank"]["silver"]),len(back["problem_bank"]["gold"]))
print("svg in silver[0]:", "<svg" in back["problem_bank"]["silver"][0]["display"])
