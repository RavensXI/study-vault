import os, json, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.42fe9f9d-e989-46b1-afef-c70754f8e4d3&select=practice_data"
r=urllib.request.Request(url, headers={'apikey':key,'Authorization':'Bearer '+key})
d=json.load(urllib.request.urlopen(r))
pd=d[0]['practice_data']
base=os.path.dirname(os.path.abspath(__file__))
open(os.path.join(base,'_FX_L01_live.json'),'w',encoding='utf-8').write(json.dumps(pd,ensure_ascii=False,indent=1))
print('ok', len(json.dumps(pd)))
