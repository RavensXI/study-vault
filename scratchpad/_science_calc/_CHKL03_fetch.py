import json, os, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
cid="6d1c06c8-5e4e-43e5-a65c-7b2041612fb5"
url=f"{BASE}?id=eq.{cid}&select=id,slug,unit_id,practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
json.dump(data[0], open("_L03_canon_live.json","w"), indent=1)
pd=data[0]["practice_data"]
print("slug:", data[0]["slug"])
print("pd keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    print(t, len(pb.get(t,[])))
