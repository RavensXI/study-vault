# Build the niche-subject target-school campaign list.
# Source 1: DfE EES "Subject school level exam data" (KS4 2024/25) - per-school
#           GCSE entries by subject.
# Source 2: GIAS all-establishments CSV - postal address, website, head, by URN.
# Output: per-subject CSVs + combined CSV + summary, in the business folder.
import csv
import io
import json
import os
import sys
import urllib.request

DATASET = '1ae39901-b462-df76-b108-640a078d7944'
API = f'https://api.education.gov.uk/statistics/v1/data-sets/{DATASET}'
HDRS = {'User-Agent': 'StudyVault-research', 'Content-Type': 'application/json'}
OUT_DIR = r'C:\Users\tshau\Documents\StudyVault Business\marketing\niche_target_schools'
TMP = os.environ.get('CLAUDE_JOB_DIR', '.') + r'\tmp'

SUBJECTS = {
    'jyqAM': 'Geology',
    'NoPDC': 'Astronomy',
    '7ZMXo': 'Statistics',
    'iP46X': 'Classical Civilisation',
    'Q90wb': 'Ancient History',
    'k7Phs': 'Electronics (Physics)',
    'zKgFQ': 'Electronic-Electrical Engineering',
    'B3b7J': 'Economics',
    'EhuqF': 'Psychology',
    'wU9bx': 'Sociology',
    'SQaVx': 'Media Studies',
    'D9JQe': 'Music Technology',
    'bRntT': 'Music',
}
GRADE_TOTAL = 'mgN9K'
QUAL_GCSE = 'AHDJG'


def api_get(path):
    r = urllib.request.Request(API + path, headers=HDRS)
    return json.load(urllib.request.urlopen(r, timeout=180))


def api_query(subject_id, page):
    body = {
        'criteria': {'and': [
            {'filters': {'in': [subject_id]}},
            {'filters': {'in': [GRADE_TOTAL]}},
            {'filters': {'in': [QUAL_GCSE]}},
        ]},
        'indicators': ['TEpPJ'],
        'page': page, 'pageSize': 200,
    }
    r = urllib.request.Request(API + '/query', data=json.dumps(body).encode(),
                               method='POST', headers=HDRS)
    return json.load(urllib.request.urlopen(r, timeout=180))


print('1) location metadata...')
meta = api_get('/meta?types=Locations')
sch, las = {}, {}


def walk(opts):
    for o in opts:
        opt = o.get('option', o)
        oid = opt.get('id')
        if opt.get('urn'):
            sch[oid] = opt
        elif oid and opt.get('label'):
            las.setdefault(oid, opt['label'])
        if o.get('options'):
            walk(o['options'])


walk(meta.get('locations', []))
print('   schools in meta:', len(sch), '| other locations:', len(las))

print('2) querying', len(SUBJECTS), 'subjects...')
rows = []
for sid, label in SUBJECTS.items():
    first = api_query(sid, 1)
    pages = first.get('paging', {}).get('totalPages', 1)
    results = list(first.get('results', []))
    for p in range(2, min(pages, 40) + 1):
        results += api_query(sid, p).get('results', [])
    for r in results:
        s = sch.get(r['locations'].get('SCH'), {})
        raw = r['values'].get('TEpPJ')
        try:
            entries = int(raw)
        except (TypeError, ValueError):
            entries = 'suppressed (small cohort)'   # 'c' etc - school still teaches it
        rows.append({
            'subject': label,
            'entries': entries,
            'school': s.get('label', ''),
            'urn': s.get('urn', ''),
            'la': las.get(r['locations'].get('LA'), ''),
        })
    print(f'   {label}: {len(results)} schools')

print('3) GIAS addresses...')
import datetime
gias_rows = {}
for back in range(0, 7):
    d = (datetime.date.today() - datetime.timedelta(days=back)).strftime('%Y%m%d')
    url = f'https://ea-edubase-api-prod.azurewebsites.net/edubase/downloads/public/edubasealldata{d}.csv'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'StudyVault-research'})
        data = urllib.request.urlopen(req, timeout=300).read()
        print('   GIAS file:', d, len(data) // 1048576, 'MB')
        text = data.decode('cp1252', errors='replace')
        rdr = csv.DictReader(io.StringIO(text))
        for g in rdr:
            gias_rows[g.get('URN', '')] = {
                'street': g.get('Street', ''), 'locality': g.get('Locality', ''),
                'town': g.get('Town', ''), 'postcode': g.get('Postcode', ''),
                'website': g.get('SchoolWebsite', ''), 'phone': g.get('TelephoneNum', ''),
                'head': ' '.join(x for x in [g.get('HeadTitle (name)', '') or g.get('HeadTitle', ''),
                                             g.get('HeadFirstName', ''), g.get('HeadLastName', '')] if x).strip(),
                'status': g.get('EstablishmentStatus (name)', ''),
            }
        break
    except Exception as e:
        print('   ', d, 'failed:', str(e)[:80])
if not gias_rows:
    print('GIAS unavailable - writing list without addresses')

print('4) writing output...')
os.makedirs(OUT_DIR, exist_ok=True)
cols = ['subject', 'entries', 'school', 'urn', 'la', 'street', 'locality',
        'town', 'postcode', 'head', 'phone', 'website', 'status']
for row in rows:
    row.update(gias_rows.get(str(row['urn']), {}))
rows.sort(key=lambda r: (r['subject'], -(r['entries'] if isinstance(r['entries'], int) else -1)))

with open(os.path.join(OUT_DIR, 'ALL_SUBJECTS_combined.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
    w.writeheader()
    w.writerows(rows)
for label in set(SUBJECTS.values()):
    sub = [r for r in rows if r['subject'] == label]
    fn = label.replace(' ', '_').replace('/', '-') + '.csv'
    with open(os.path.join(OUT_DIR, fn), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(sub)

print()
print('SUMMARY (schools / total entries):')
for label in sorted(set(SUBJECTS.values())):
    sub = [r for r in rows if r['subject'] == label]
    tot = sum(r['entries'] for r in sub if isinstance(r['entries'], int))
    supp = sum(1 for r in sub if not isinstance(r['entries'], int))
    print(f'  {label:35s} {len(sub):5d} schools  {tot:7d} entries  ({supp} suppressed)')
print()
print('written to', OUT_DIR)
