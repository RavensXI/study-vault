import os, json, urllib.request
ID="04953988-ada8-4eb2-bbd4-401fb67247ff"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-ocr_algebra-L11_diagrams.json",encoding="utf-8"))
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":key,"Authorization":"Bearer "+key,
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
# verify round trip
url2=url+"&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":key,"Authorization":"Bearer "+key})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("keys live:",sorted(live.keys()))
print("has tier_guides:",bool(live.get("tier_guides")),"has guided:",bool(live.get("guided")))
print("bronze count:",len(live["problem_bank"]["bronze"]),
      "svg figs:",sum(1 for t in("bronze","silver","gold") for p in live["problem_bank"][t] if "<svg" in p["display"]))
print("bronze[2] display:",live["problem_bank"]["bronze"][2]["display"])
print("gold[3] display:",live["problem_bank"]["gold"][3]["display"])
print("worked_examples preserved count:",len(live.get("worked_examples") or []))
