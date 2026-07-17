import os, json, urllib.request
ID="b749e688-9faa-49ba-ae68-08f8abdc7496"
sk=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_algebra-L02.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":sk,"Authorization":"Bearer "+sk,"Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify
u2="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
q=urllib.request.Request(u2,headers={"apikey":sk,"Authorization":"Bearer "+sk})
live=json.load(urllib.request.urlopen(q))[0]["practice_data"]
print("live has keys:",sorted(live.keys()))
print("guided present:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[0] hint:", live["problem_bank"]["bronze"][0].get("hint"))
print("gold[3] guided_steps len:", len(live["problem_bank"]["gold"][3].get("guided_steps",[])))
print("worked_examples preserved:", len(live.get("worked_examples",[])))
