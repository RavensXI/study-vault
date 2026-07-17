import json
live=json.load(open('_live_graphs-L07.json',encoding='utf-8'))['practice_data']
json.dump(live, open('_live_graphs-L07_pd.json','w',encoding='utf-8'), ensure_ascii=False)
# em dash scan
import re
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if '—' in o: print("EM DASH:",path,"::",o[:80])
        if '&' in o and any(e in o for e in ['&rsquo;','&amp;','&nbsp;','&mdash;']): print("ENTITY:",path,"::",o[:80])
for _ in walk(live): pass
print("scan done")
