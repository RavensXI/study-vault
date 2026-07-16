import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="aee11210-c33f-4e61-a25e-1ef101e95ab3"
pd=json.load(io.open("lesson_geometry-L07_diagrams.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
