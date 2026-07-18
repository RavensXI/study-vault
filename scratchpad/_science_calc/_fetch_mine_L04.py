import os, json, urllib.request
SB="https://baipckgywpnwapobwtsy.supabase.co"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
cid="e6963758-b327-488c-87b4-177b336f29e9"
url=f"{SB}/rest/v1/lessons?id=eq.{cid}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_mine_L04_canonical.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])))
