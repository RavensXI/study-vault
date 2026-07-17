import os, json, io, urllib.request
LID="112923c0-364e-4701-91d9-280e7859d6d3"
sk=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_graphs-L01.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":sk,"Authorization":f"Bearer {sk}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify round-trip
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":sk,"Authorization":f"Bearer {sk}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("round-trip match:", json.dumps(live,sort_keys=True)==json.dumps(pd,sort_keys=True))
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
