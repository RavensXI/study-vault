import json, os, urllib.request, io
KEY=os.environ['SUPABASE_SERVICE_KEY']
def get(url):
    req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':'Bearer '+KEY})
    return json.load(urllib.request.urlopen(req))
cid='25f5e5e1-21c7-451c-ab9c-81872507edf1'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=id,slug,title,practice_data'
data=get(url)
row=data[0]
with io.open('_chk95_canonical.json','w',encoding='utf-8') as f:
    json.dump(row['practice_data'], f, indent=2, ensure_ascii=False)
pd=row['practice_data']
pb=pd.get('problem_bank',{})
out=['slug: '+str(row['slug'])+' title: '+str(row['title'])]
for t in ('bronze','silver','gold'):
    out.append(t+' '+str(len(pb.get(t,[]))))
out.append('top keys: '+str(list(pd.keys())))
with io.open('_chk95_summary.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
print('\n'.join(out))
