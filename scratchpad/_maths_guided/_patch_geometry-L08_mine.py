import os, json, io, urllib.request
ID="0b095025-37bb-49e4-94da-6f898ad6f3e7"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_geometry-L08.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
