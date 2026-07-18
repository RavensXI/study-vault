import os, json, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
IDS=["5145c094-e59a-4b76-b50f-368197215ca4"]
pd=json.load(open("lesson_higher-calculations-L05@f4fdd10261.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
for ID in IDS:
    url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}'
    req=urllib.request.Request(url, data=body, method="PATCH", headers={
        'apikey':KEY,'Authorization':f'Bearer {KEY}',
        'Content-Type':'application/json','Prefer':'return=minimal'})
    r=urllib.request.urlopen(req)
    print("PATCH", ID, r.status)
# verify propagation: re-fetch each and compare byte-identical
canon=json.dumps(pd,sort_keys=True)
for ID in IDS:
    url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
    req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
    got=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    print("MATCH", ID, json.dumps(got,sort_keys=True)==canon)
