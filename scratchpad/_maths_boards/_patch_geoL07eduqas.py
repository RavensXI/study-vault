import os, json, io, urllib.request
LID="f3574e2a-651d-42a7-af75-8ee52eeb48d8"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_geometry-L07.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%LID
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":KEY,"Authorization":"Bearer "+KEY,
  "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify round-trip
url2=url+"&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
got=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
pb=got["problem_bank"]
print("live now: bronze",len(pb["bronze"]),"silver",len(pb["silver"]),"gold",len(pb["gold"]),
      "| guided?",("guided" in got),"| tier_guides?",("tier_guides" in got),
      "| svg count", json.dumps(got).count("<svg"))
print("gold[0] sol",pb["gold"][0]["solutions"],"| silver[3] sol",pb["silver"][3]["solutions"])
