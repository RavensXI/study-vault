import json, os, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data"
    req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
    return json.load(urllib.request.urlopen(req))[0]['practice_data']
c=get('72ac6bb2-a0ff-4955-98f0-7ead3e2b7423')
o=get('7cb0647a-2614-4a1b-ae2f-4598bfa47c96')
json.dump(c,open('_live_canonical.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
json.dump(o,open('_live_other.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
print("byte identical:", json.dumps(c,sort_keys=True,ensure_ascii=False)==json.dumps(o,sort_keys=True,ensure_ascii=False))
print("top keys:", sorted(c.keys()))
