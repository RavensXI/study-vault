# -*- coding: utf-8 -*-
import os, json, io, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
ID='ee087e5f-7971-4f5d-b6e0-2fe13585d6f4'
pd=json.load(io.open("lesson_number-L03.json",encoding="utf-8"))
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}'
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method='PATCH',headers={
 'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json','Prefer':'return=minimal'})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify round-trip
req2=urllib.request.Request(url+'&select=practice_data',headers={'apikey':key,'Authorization':'Bearer '+key})
back=json.load(urllib.request.urlopen(req2))[0]['practice_data']
print("roundtrip keys:",sorted(back.keys()))
print("has guided:", 'guided' in back, "| tier_guides:", 'tier_guides' in back)
print("bronze_description present:", bool(back['problem_bank'].get('bronze_description')))
print("gold[0] has guided_steps:", bool(back['problem_bank']['gold'][0].get('guided_steps')))
print("equal to file:", back==pd)
