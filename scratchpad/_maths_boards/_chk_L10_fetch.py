import os, json, urllib.request
ID="0c881c07-49bb-49cd-8c89-41b971335061"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_CHK_L10_live.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("OK bytes", len(json.dumps(pd)))
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
