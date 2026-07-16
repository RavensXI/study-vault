import os, json, urllib.request
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.1d039d5e-b358-4864-b935-b3334ba99d20&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,open("_live_L04_refetch.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
# print solutions for all problems
for tier in ["gold","bronze","silver"]:
    for j,p in enumerate(pd["problem_bank"][tier]):
        print(tier,j,"disp:",p["display"][:55])
        print("      sols:",p["solutions"])
