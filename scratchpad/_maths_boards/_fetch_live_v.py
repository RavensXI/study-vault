import os, json, urllib.request
ID="04953988-ada8-4eb2-bbd4-401fb67247ff"
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd, open("_ocrL11_live2.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("refetched. guided:",bool(pd.get("guided")),"tier_guides:",bool(pd.get("tier_guides")))
print("bronze[0] hint:",repr(pd["problem_bank"]["bronze"][0].get("hint"))[:60])
