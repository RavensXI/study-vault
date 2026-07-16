import os, json, urllib.request
ID="4e2bb5ad-e75a-48be-951a-0e8b8db75296"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_geometry-L06.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify live
gurl=f"{url}&select=practice_data"
greq=urllib.request.Request(gurl, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(greq))[0]["practice_data"]
disp=live["problem_bank"]["silver"][0]["display"]
print("live has P1 arc:", "M96.7 141.0 A16 16 0 0 0 84.9 125.6" in disp)
print("live still has old P2 75-arc:", "M143.3 141.0" in disp)
print("live 75 text x=102.5:", 'x="102.5"' in disp)
