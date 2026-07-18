import json, os, urllib.request
KEY=os.environ.get('SUPABASE_SERVICE_KEY')
ID="d42fee71-d641-4f20-90c6-8bde5e185595"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,practice_data,lesson_number,title,slug"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
row=data[0]
json.dump(row['practice_data'], open('_chk_8a0771_live.json','w',encoding='utf-8'), indent=2, ensure_ascii=False)
pd=row['practice_data']
print("title:", row['title'], "| slug:", row['slug'])
b0=pd['problem_bank']['bronze'][0]
print("bronze[0] display:", b0['display'][:80])
print("bronze[0] solutions:", b0['solutions'])
print("bronze counts:", {t:len(pd['problem_bank'][t]) for t in ['bronze','silver','gold']})
