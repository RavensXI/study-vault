import os,json,io,urllib.request
ID='496a8347-7f03-47a6-9543-49cb82efe3af'
key=os.environ['SUPABASE_SERVICE_KEY']
pd=json.load(io.open('lesson_maths-eduqas_algebra-L08.json',encoding='utf-8'))
url='https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s'%ID
body=json.dumps({"practice_data":pd}).encode('utf-8')
req=urllib.request.Request(url,data=body,method='PATCH',headers={
 'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json',
 'Prefer':'return=minimal'})
resp=urllib.request.urlopen(req)
print('PATCH status',resp.status)
# verify readback
req2=urllib.request.Request(url+'&select=practice_data',headers={'apikey':key,'Authorization':'Bearer '+key})
back=json.load(urllib.request.urlopen(req2))[0]['practice_data']
print('readback has guided:', 'guided' in back, '| tier_guides:', 'tier_guides' in back)
print('bronze b0 sol:', back['problem_bank']['bronze'][0]['solutions'])
print('bronze b7 sol:', back['problem_bank']['bronze'][7]['solutions'])
print('opener svg present:', '<svg' in back['guided']['opener']['display'])
