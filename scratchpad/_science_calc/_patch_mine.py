import json, urllib.request, os
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ids=["08e03207-3ecf-4964-81dc-a8b94002b3e2","599f6b2c-9f8e-4321-b8b0-7e6036ce1450","9d4bd9f1-eed4-4293-bc3e-1d92c305d7ac","30f59090-f7ba-45e5-a2e4-47efa34fd2bd","37227c2b-ee4d-4132-8dc6-39dda152d21a","6134dce2-77b2-4bb5-8e24-7ec8a0e7f5b2","a19bb97b-86bd-46fd-8623-a309449c8166"]
pd=json.load(open("lesson_physics-calculations-L01@32fbb0cae2.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode()
base="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq."
hdr={"apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"}
for i in ids:
    req=urllib.request.Request(base+i,data=body,headers=hdr,method="PATCH")
    r=urllib.request.urlopen(req)
    print(i,r.status)
print("PATCHED",len(ids))
