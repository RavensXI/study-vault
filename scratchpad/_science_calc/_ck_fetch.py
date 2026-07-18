import os, json, urllib.request, io
KEY=os.environ['SUPABASE_SERVICE_KEY']
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data"
    r=urllib.request.Request(url,headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
    return json.load(urllib.request.urlopen(r))[0]['practice_data']
pd=get("91158ba8-389c-4771-9735-326785654ccb")
with io.open('_ck_canonical_live.json','w',encoding='utf-8') as f:
    json.dump(pd,f,indent=1,ensure_ascii=False)
print("keys",list(pd.keys()))
pb=pd.get('problem_bank',{})
for t in ('bronze','silver','gold'):
    print(t,len(pb.get(t,[])))
