# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout.reconfigure(encoding='utf-8')

pd = json.load(open('_live_pd.json', encoding='utf-8'))
s = json.dumps(pd, ensure_ascii=False)

EM = '—'   # em dash
EN = '–'   # en dash
MINUS = '−'
TIMES = '×'
print('U+2014 em dash count :', s.count(EM))
print('U+2013 en dash count :', s.count(EN))
print('U+2212 minus count   :', s.count(MINUS))
print('U+00d7 times count   :', s.count(TIMES))
print('ASCII hyphen "-" count:', s.count('-'))

# show em dash contexts if any
i = 0
while True:
    k = s.find(EM, i)
    if k < 0: break
    print('EM@', repr(s[k-45:k+45]))
    i = k+1

# Preservation check vs pre-dump
print('\n=== PRESERVATION ===')
try:
    pre = json.load(open('_pre_fanout_dump.json', encoding='utf-8'))
except Exception as e:
    pre = None
    print('pre-dump load error:', e)

if pre is not None:
    lid = '1d039d5e-b358-4864-b935-b3334ba965a0'  # placeholder
    lid = '1d039d5e-b358-4864-b935-b3334ba90000'
    # Actually find real entry by id
    target = '1d039d5e-b358-4864-b935-b3334ba9'
    entry = None
    def walk(o):
        found=[]
        if isinstance(o, dict):
            for kk,vv in o.items():
                if isinstance(vv,str) and vv.startswith('1d039d5e'):
                    found.append(('val',kk,vv))
                found += walk(vv)
            if any(str(o.get(k,'')).startswith('1d039d5e') for k in ('id','lesson_id')):
                found.append(('entry', o.get('id') or o.get('lesson_id'), o))
        elif isinstance(o, list):
            for it in o: found += walk(it)
        return found
    hits = walk(pre)
    entries = [h for h in hits if h[0]=='entry']
    print('pre-dump top type:', type(pre).__name__, 'entries matching id:', len(entries))
    if entries:
        row = entries[0][2]
        prepd = row.get('practice_data', row)
        for fld in ('related_videos','topic_links','worked_examples'):
            a = json.dumps(prepd.get(fld), ensure_ascii=False, sort_keys=True)
            b = json.dumps(pd.get(fld), ensure_ascii=False, sort_keys=True)
            print(f'  {fld}: {"UNCHANGED" if a==b else "CHANGED"}  (pre {len(a)} chars / live {len(b)} chars)')
