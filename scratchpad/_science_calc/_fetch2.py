import json, os, urllib.request
KEY=os.environ.get('SUPABASE_SERVICE_KEY')
ID="d42fee71-d641-4f20-90c6-8bde5e185595"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,practice_data,lesson_number,title,slug"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
try:
    data=json.load(urllib.request.urlopen(req))
except urllib.error.HTTPError as e:
    print("ERR", e.code, e.read().decode()[:500]); raise
row=data[0]
json.dump(row['practice_data'], open('_live_canonical.json','w'), indent=2)
print("title:", row['title'], "| slug:", row['slug'], "| n:", row['lesson_number'])
pd=row['practice_data']
print("keys:", list(pd.keys()))
pb=pd.get('problem_bank',{})
for t in ['bronze','silver','gold']:
    print(t, len(pb.get(t,[])))
