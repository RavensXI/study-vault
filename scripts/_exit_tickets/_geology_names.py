import json
import urllib.request

rows = json.load(open('_geology_rows.json', encoding='utf-8'))
want_sch = {r['loc']['SCH'] for r in rows}
want_la = {r['loc']['LA'] for r in rows}

req = urllib.request.Request(
    'https://api.education.gov.uk/statistics/v1/data-sets/1ae39901-b462-df76-b108-640a078d7944/meta?types=Locations',
    headers={'User-Agent': 'StudyVault-research'})
meta = json.load(urllib.request.urlopen(req, timeout=120))

names = {}
las = {}


def walk(opts, level=None):
    for o in opts:
        lvl = o.get('level', level)
        opt = o.get('option', o)
        oid = opt.get('id')
        if oid in want_sch:
            names[oid] = opt
        if oid in want_la:
            las[oid] = opt.get('label')
        if o.get('options'):
            walk(o['options'], lvl)


locs = meta.get('locations', [])
walk(locs)
print('resolved schools:', len(names), '| LAs:', len(las))

table = []
for r in rows:
    s = names.get(r['loc']['SCH'], {})
    table.append({
        'school': s.get('label', r['loc']['SCH']),
        'urn': s.get('urn', ''),
        'la': las.get(r['loc']['LA'], r['loc']['LA']),
        'entries': r['values'].get('TEpPJ'),
    })
table.sort(key=lambda x: -int(x['entries'] or 0))
for t in table:
    print(f"{t['entries']:>4}  {t['school']}  ({t['la']})  URN {t['urn']}")
json.dump(table, open('_geology_schools.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
