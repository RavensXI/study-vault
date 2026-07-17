import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

d = json.load(open('_live_L04.json', encoding='utf-8'))[0]['practice_data']

EMDASH = '—'
HORBAR = '―'

def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'note':
                continue
            yield from walk(v, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + '[' + str(i) + ']')
    elif isinstance(o, str):
        yield path, o

emdash = []
mojibake = []
MOJI = ['Ã', 'â', 'Â°', 'âˆ']
for p, s in walk(d):
    if EMDASH in s or HORBAR in s:
        emdash.append((p, s))
    for tok in MOJI:
        if tok in s:
            mojibake.append((p, s))
            break

print('EM DASH count:', len(emdash))
for p, s in emdash:
    print('  ', p, '::', s)
print('MOJIBAKE count:', len(mojibake))
for p, s in mojibake[:10]:
    print('  ', p, '::', s[:90])

# also check for HTML entities in plain-text message/hint fields
import re
ent = []
for p, s in walk(d):
    if re.search(r'&[a-zA-Z]+;|&#\d+;', s):
        ent.append((p, s))
print('HTML ENTITY count:', len(ent))
for p, s in ent[:10]:
    print('  ', p, '::', s[:90])
