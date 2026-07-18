import json, io
d=json.load(open('_live_fetch.json',encoding='utf-8'))['cc2d2229-8dc3-496f-abf9-5e3f9b2d14ec']
io.open('_live_canonical.json','w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False))
print('wrote', len(json.dumps(d)))
