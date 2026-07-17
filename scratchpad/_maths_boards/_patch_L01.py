import json, os, io, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
ID='e023770a-3bf9-43e4-9718-fc2da08eda49'
pd=json.load(io.open("_maths_boards/lesson_number-L01.json",encoding="utf-8"))
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}'
body=json.dumps({"practice_data":pd}).encode('utf-8')
req=urllib.request.Request(url,data=body,method='PATCH',headers={
 'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json','Prefer':'return=minimal'})
r=urllib.request.urlopen(req)
print('PATCH status',r.status)
# verify round trip
req2=urllib.request.Request(url+'&select=practice_data',headers={'apikey':key,'Authorization':'Bearer '+key})
live=json.load(urllib.request.urlopen(req2))[0]['practice_data']
print('tiers',list(live['problem_bank'].keys()))
print('has guided',bool(live.get('guided')),'has tier_guides',bool(live.get('tier_guides')))
print('bronze[5] display',live['problem_bank']['bronze'][5]['display'])
print('worked_examples',len(live.get('worked_examples',[])))
