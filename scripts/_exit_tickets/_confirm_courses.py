# Course-confirmation crawler: for each school in a campaign CSV, fetch its
# website (homepage + likely curriculum/options pages, small budget per site)
# and look for the subject keyword. Output per school:
#   confirmed  - keyword found on a page (URL recorded)
#   unconfirmed - site reachable, keyword not found in the pages we tried
#                 (many schools bury options in PDFs - NOT evidence of dropping)
#   unreachable - site down / blocked
# Usage: python _confirm_courses.py Geology.csv "geology"
import csv
import html
import os
import re
import sys
import time
import urllib.parse
import urllib.request

BUSINESS = r'C:\Users\tshau\Documents\StudyVault Business\marketing\niche_target_schools'
UA = {'User-Agent': 'Mozilla/5.0 (StudyVault education research; studyvault.info@gmail.com)'}
PAGE_BUDGET = 6
LINK_HINTS = re.compile(r'curriculum|options|subject|gcse|ks4|key-?stage-?4|course|department|academic', re.I)

csv_name = sys.argv[1]
keywords = [k.strip().lower() for k in sys.argv[2].split(',')]


def fetch(url):
    time.sleep(0.5)   # politeness: up to 6 pages per school, thousands of schools on shared hosts
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            if 'html' not in (r.headers.get('Content-Type') or 'html'):
                return None, r.geturl()
            return r.read(400000).decode('utf-8', errors='replace'), r.geturl()
    except Exception:
        return None, url


def norm_site(w):
    w = (w or '').strip()
    if not w:
        return None
    if not w.startswith('http'):
        w = 'https://' + w
    return w


rows = list(csv.DictReader(open(os.path.join(BUSINESS, csv_name), encoding='utf-8-sig')))
print(f'{csv_name}: {len(rows)} schools, keywords {keywords}', flush=True)

for row in rows:
    site = norm_site(row.get('website'))
    row['course_check'] = 'unreachable'
    row['course_check_url'] = ''
    if not site:
        continue
    page, base = fetch(site)
    if page is None:
        continue
    row['course_check'] = 'unconfirmed'
    seen, queue = {base}, []
    for m in re.finditer(r'href=["\']([^"\'#]+)', page):
        u = urllib.parse.urljoin(base, html.unescape(m.group(1)))
        if u.startswith('http') and urllib.parse.urlparse(u).netloc == urllib.parse.urlparse(base).netloc \
           and LINK_HINTS.search(u) and u not in seen and not u.lower().endswith(('.pdf', '.doc', '.docx')):
            seen.add(u)
            queue.append(u)
    pages = [(base, page)] + [(u, fetch(u)[0]) for u in queue[:PAGE_BUDGET - 1]]
    for url, body in pages:
        if body and any(k in body.lower() for k in keywords):
            row['course_check'] = 'confirmed'
            row['course_check_url'] = url
            break
    print(f"  {row['course_check']:12s} {row['school'][:45]}", flush=True)

out = csv_name.replace('.csv', '_checked.csv')
with open(os.path.join(BUSINESS, out), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['course_check'])
    w.writeheader()
    w.writerows(rows)
c = sum(1 for r in rows if r['course_check'] == 'confirmed')
u = sum(1 for r in rows if r['course_check'] == 'unconfirmed')
x = sum(1 for r in rows if r['course_check'] == 'unreachable')
print(f'DONE {out}: {c} confirmed, {u} unconfirmed, {x} unreachable')
