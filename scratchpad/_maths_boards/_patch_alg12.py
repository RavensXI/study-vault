import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="971cfba0-badb-4c6b-b0f8-e9d33d450b8c"
pd=json.load(io.open("lesson_maths-ocr_algebra-L12.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req); print("PATCH status", r.status)
# readback
g=urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
back=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("readback == local:", json.dumps(back,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False))
print("keys:", sorted(back.keys()))
