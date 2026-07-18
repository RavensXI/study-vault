import json, io
pd=json.load(io.open('_live_canon_fresh.json',encoding='utf-8'))
def walk(o, path=''):
    if isinstance(o, dict):
        for k,v in o.items():
            yield from walk(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')
    else:
        yield path, o
for p,v in walk(pd):
    if isinstance(v, float) and len(repr(v)) > 8:
        print(p, repr(v))
