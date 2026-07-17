import json, os, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
ID='e023770a-3bf9-43e4-9718-fc2da08eda49'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
req=urllib.request.Request(url, headers={'apikey':key,'Authorization':'Bearer '+key})
d=json.load(urllib.request.urlopen(req))
pd=d[0]['practice_data']
json.dump(pd, open('_maths_boards/_live_number-L01.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('top keys', list(pd.keys()))
print('bank tiers', list(pd['problem_bank'].keys()) if 'problem_bank' in pd else 'none')
