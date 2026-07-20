import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
pd=json.load(open("lesson_L12.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
r=urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Prefer":"return=minimal"})
print("patch status", urllib.request.urlopen(r).status)
r2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
back=json.load(urllib.request.urlopen(r2))[0]["practice_data"]
c=0; found=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(back["problem_bank"][tier]):
        if "unit" in p: c+=1; found.append((tier,i,p["unit"],p.get("input_type")))
print("units live:",c,found)
print("identical:", json.dumps(back,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False))
