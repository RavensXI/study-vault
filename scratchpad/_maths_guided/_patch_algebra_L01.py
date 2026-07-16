import os, json, io, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
ID='2603a7c5-7660-4a4c-943d-78f2a112009e'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}'
pd=json.load(io.open('lesson_algebra-L01.json',encoding='utf-8'))
body=json.dumps({'practice_data':pd}).encode('utf-8')
req=urllib.request.Request(url, data=body, method='PATCH', headers={
    'apikey':KEY,'Authorization':f'Bearer {KEY}',
    'Content-Type':'application/json','Prefer':'return=minimal'})
resp=urllib.request.urlopen(req)
print('PATCH status', resp.status)
# verify
req2=urllib.request.Request(url+'&select=practice_data', headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
back=json.load(urllib.request.urlopen(req2))[0]['practice_data']
print('roundtrip keys:', list(back.keys()))
print('silver[6] display:', back['problem_bank']['silver'][6]['display'])
print('has guided.opener:', bool(back.get('guided',{}).get('opener')))
print('has tier_guides:', bool(back.get('tier_guides')))
