import os, io, json, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
rid="9733399d-1134-4649-8166-74c5b738c4a3"
req=urllib.request.Request(f"{BASE}?id=eq.{rid}&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
pd=json.loads(urllib.request.urlopen(req).read())[0]['practice_data']
io.open("_val_raw.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
io.open("_val_wrapped.json","w",encoding="utf-8").write(json.dumps({"practice_data":pd},indent=2,ensure_ascii=False))
print("written")
