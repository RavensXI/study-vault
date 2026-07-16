import os, json, io, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
ID='4aa9afe1-7e47-4f0f-b7e6-da22be472716'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
req=urllib.request.Request(url, headers={'apikey':key,'Authorization':'Bearer '+key})
pd=json.load(urllib.request.urlopen(req))[0]['practice_data']
json.dump(pd, io.open("_live_after.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
local=json.load(io.open("lesson_graphs-L06.json",encoding="utf-8"))
print("round-trip identical:", pd==local)
