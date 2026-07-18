import json, io
pd=json.load(io.open('_live_canon_fresh.json',encoding='utf-8'))
# find all float-noise values across whole object
import re
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
    if isinstance(v, float):
        # detect noise: not clean at 4 decimals
        if abs(v - round(v,4)) > 1e-9:
            print(p, repr(v))
