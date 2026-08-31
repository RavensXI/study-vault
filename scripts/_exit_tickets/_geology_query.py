import json
import sys
import urllib.request

DATASET = '1ae39901-b462-df76-b108-640a078d7944'
SUBJECT = sys.argv[1] if len(sys.argv) > 1 else 'jyqAM'   # Geology

def query(page):
    body = {
        "criteria": {"and": [
            {"filters": {"in": [SUBJECT]}},
            {"filters": {"in": ["mgN9K"]}},   # Total exam entries
            {"filters": {"in": ["AHDJG"]}},   # GCSE (9-1) Full Course
        ]},
        "indicators": ["TEpPJ"],
        "page": page, "pageSize": 200,
    }
    req = urllib.request.Request(
        f'https://api.education.gov.uk/statistics/v1/data-sets/{DATASET}/query',
        data=json.dumps(body).encode(), method='POST',
        headers={'Content-Type': 'application/json', 'User-Agent': 'StudyVault-research'})
    return json.load(urllib.request.urlopen(req, timeout=120))

try:
    first = query(1)
except urllib.error.HTTPError as e:
    print('HTTP', e.code, e.read()[:600])
    sys.exit(1)

print('paging:', first.get('paging'))
rows = list(first.get('results', []))
pages = first.get('paging', {}).get('totalPages', 1)
for p in range(2, min(pages, 20) + 1):
    rows += query(p).get('results', [])

print('sample row:', json.dumps(rows[0], indent=1)[:600] if rows else 'NONE')
out = []
for r in rows:
    loc = r.get('locations', {})
    out.append({'loc': loc, 'values': r.get('values', {})})
json.dump(out, open('_geology_rows.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('rows saved:', len(out))
