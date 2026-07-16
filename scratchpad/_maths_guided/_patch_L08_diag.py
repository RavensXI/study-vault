import os,json,urllib.request
ID="33559430-93a0-4565-971b-65b8fc2cc53d"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_graphs-L08_diagrams.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH",r.status)
# verify live
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
lv=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
pb=lv["problem_bank"]
nsvg=sum(str(p.get("display","")).count("<svg") for t in pb if isinstance(pb[t],list) for p in pb[t])
nchart=sum(1 for t in pb if isinstance(pb[t],list) for p in pb[t] if "chart" in p)
print("live svg:",nsvg,"live chart:",nchart)
