"""Render the spec-currency audit ledger (docs/SPEC_CURRENCY_AUDIT_2027.md)
from scripts/_spec_audit_results.json (the workflow's verdict array).
Usage: python scripts/_gen_spec_audit_ledger.py <run-date YYYY-MM-DD>"""
import sys, json, io
from collections import Counter

run_date = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
arr = json.load(io.open('scripts/_spec_audit_results.json', encoding='utf-8'))
st = Counter(r.get('status', '?') for r in arr)
order = {'RED': 0, 'AMBER': 1, 'GREEN': 2, 'ERROR': 3}
arr.sort(key=lambda r: (order.get(r.get('status'), 9), r.get('name', '')))

L = []
L.append('# Spec-Currency Audit — 2027 Cohort')
L.append('')
L.append(f'**Run:** {run_date} · **Scope:** {len(arr)} live free-tier subjects (school_id NULL). '
         'Unity bespoke out of scope (owner-controlled, low spec-volatility).')
L.append('')
L.append(f'**Result:** {st.get("GREEN",0)} GREEN · {st.get("AMBER",0)} AMBER · {st.get("RED",0)} RED'
         + (f' · {st.get("ERROR",0)} ERROR' if st.get('ERROR') else ''))
L.append('')
L.append('Method: one research agent per subject checked the Ofqual Register of Regulated Qualifications '
         '(operational/certification end dates = authoritative withdrawal signal) plus the board\'s own '
         'specification/updates pages. Every RED/withdrawal verdict was adversarially re-verified before it '
         'was allowed to stand (a refuted withdrawal downgrades to AMBER for human confirm, never silently to GREEN). '
         'Calibration: GCSEs cannot be reformed mid-course, so RED = withdrawal affecting the 2027 series, not a future reform.')
L.append('')
L.append('Re-run annually: `python scripts/_gen_spec_audit_worklist.py` then run the `spec-currency-audit-2027` '
         'workflow, then `python scripts/_gen_spec_audit_ledger.py <date>`.')
L.append('')

def block(tag, title, blurb):
    rows = [r for r in arr if r.get('status') == tag]
    if not rows:
        return
    L.append(f'## {title} ({len(rows)})')
    if blurb:
        L.append('')
        L.append(blurb)
    for r in rows:
        L.append('')
        L.append(f'### {r.get("name","?")} — {r.get("board","?")} `{r.get("spec_code","?")}`')
        L.append(f'- **slug:** `{r.get("slug","?")}` · **offered 2027:** {r.get("still_offered_2027")} '
                 f'· **confidence:** {r.get("confidence","?")}'
                 + (f' · **end date:** {r.get("withdrawal_end_date")}' if r.get('withdrawal_end_date') else ''))
        if r.get('amendment_summary'):
            L.append(f'- **What changed:** {r["amendment_summary"]}')
        if r.get('verify'):
            v = r['verify']
            L.append(f'- **Adversarial verify:** confirmed_withdrawn={v.get("confirmed_withdrawn")}, '
                     f'still_offered_2027={v.get("still_offered_2027")} — {(v.get("reasoning","") or "")[:300]}')
        L.append(f'- **Action:** {r.get("action","")}')
        if r.get('evidence_urls'):
            L.append(f'- **Evidence:** {" · ".join(r["evidence_urls"][:4])}')
    L.append('')

block('RED', 'RED — withdrawn / not offered for 2027 (decision needed)',
      'These qualifications do not have a normal summer-2027 exam series. Decide per subject: pull from the picker, '
      'mark legacy, or rebuild against the replacement spec.')
block('AMBER', 'AMBER — offered for 2027 but a change needs a content review',
      'Offered for 2027, but a material spec/assessment change lands on the 2027 cohort or a withdrawal is coming for a later cohort. '
      'Targeted content pass, not a rebuild. Priority-order by exam-entry size.')
block('ERROR', 'ERROR — audit could not complete', 'Re-run these individually.')

# GREEN summary table
greens = [r for r in arr if r.get('status') == 'GREEN']
low = [r for r in greens if r.get('confidence') == 'low']
L.append(f'## GREEN — current & offered for 2027 ({len(greens)})')
L.append('')
if low:
    L.append(f'**{len(low)} low-confidence GREEN(s)** — sources were hard to reach, glance before relying:')
    for r in low:
        L.append(f'- {r.get("name")} ({r.get("board")} `{r.get("spec_code")}`) — {(r.get("action","") or "")[:140]}')
    L.append('')
L.append('<details><summary>Full GREEN list</summary>')
L.append('')
for r in sorted(greens, key=lambda r: r.get('name', '')):
    L.append(f'- {r.get("name")} — {r.get("board")} `{r.get("spec_code")}` ({r.get("slug")})')
L.append('')
L.append('</details>')
L.append('')

io.open('docs/SPEC_CURRENCY_AUDIT_2027.md', 'w', encoding='utf-8').write('\n'.join(L))
print(f'wrote docs/SPEC_CURRENCY_AUDIT_2027.md ({st.get("GREEN",0)}G / {st.get("AMBER",0)}A / {st.get("RED",0)}R)')
