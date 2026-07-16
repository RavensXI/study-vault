import os, json, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
ID='d9ac5103-221b-441e-81f2-d95e77269ea3'
pd=json.load(open('lesson_graphs-L04.json',encoding='utf-8'))
body=json.dumps({"practice_data":pd}).encode('utf-8')
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}'
req=urllib.request.Request(url,data=body,method='PATCH',headers={
 'apikey':KEY,'Authorization':f'Bearer {KEY}','Content-Type':'application/json','Prefer':'return=minimal'})
r=urllib.request.urlopen(req)
print('PATCH status',r.status)
# verify readback
url2=f'{url}&select=practice_data'
req2=urllib.request.Request(url2,headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
back=json.load(urllib.request.urlopen(req2))[0]['practice_data']
print('readback equal:', back==pd)
