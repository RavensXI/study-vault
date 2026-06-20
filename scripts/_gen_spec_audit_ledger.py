"""Render the spec-currency audit ledger (docs/SPEC_CURRENCY_AUDIT_2027.md)
from scripts/_spec_audit_results.json (verdicts with built_status joined).
Usage: python scripts/_gen_spec_audit_ledger.py <run-date YYYY-MM-DD>"""
import sys, json, io, re
from collections import Counter

run_date = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
arr = json.load(io.open('scripts/_spec_audit_results.json', encoding='utf-8'))
st = Counter(r.get('status', '?') for r in arr)
bs = Counter(r.get('built_status', '?') for r in arr)
BUILT = ('free', 'both', 'school')
SUNSET_RX = re.compile(r'withdraw|sunset|final assessment|teach-out|forward flag|do not build', re.I)


def line(r):
    tags = f"{r.get('status')}/{r.get('built_status','?')}"
    return f"`{tags}` **{r.get('name','?')}** — {r.get('board','?')} `{r.get('spec_code','?')}` (conf {r.get('confidence','?')})"


def detail(r):
    out = [f"- {line(r)}"]
    if r.get('withdrawal_end_date'):
        out.append(f"  - **End date:** {r['withdrawal_end_date']}")
    if r.get('amendment_summary'):
        out.append(f"  - **What changed:** {r['amendment_summary'][:500]}")
    out.append(f"  - **Action:** {(r.get('action','') or '')[:480]}")
    if r.get('evidence_urls'):
        out.append(f"  - Evidence: {' · '.join(r['evidence_urls'][:3])}")
    return '\n'.join(out)


L = []
L.append('# Spec-Currency Audit — 2027 Cohort (all subjects, all boards)')
L.append('')
L.append(f'**Run:** {run_date} · **Scope:** {len(arr)} qualifications = every catalogued spec '
         '(specs/index.json, all boards) unioned with everything we ship. '
         f'Build status: {dict(bs)}.')
L.append('')
L.append(f'**Result:** {st.get("GREEN",0)} GREEN · {st.get("AMBER",0)} AMBER · {st.get("RED",0)} RED.')
L.append('')
L.append('Method: per-qualification research agent (Ofqual register operational/cert end dates + board '
         'amendment pages), every RED/withdrawal adversarially re-verified. For built specs RED/AMBER = act now; '
         'for not-built specs the verdict is a BUILD-READINESS signal (RED = do not build / superseded). '
         'Re-run: `_gen_spec_audit_worklist.py --scope full` → workflow `spec-currency-audit-2027` → this script.')
L.append('')
L.append('> **Systemic note — Wales reform.** WJEC `3xxxQS`/`3xxxCS` legacy GCSEs (Curriculum for Wales / '
         '"Made-for-Wales") are being withdrawn: final full assessment Summer 2026, Jan-2027 resit only, no '
         'Summer 2027 series. Our "Eduqas / WJEC" aliased subjects are fine for **England (Eduqas, Cxxx)** but the '
         '**Wales (WJEC, 3xxx)** arm is dead for 2027 — relevant only if we serve Welsh students.')
L.append('')

# 1. Built + RED/AMBER (act now)
act = [r for r in arr if r.get('built_status') in BUILT and r.get('status') in ('RED', 'AMBER')]
act.sort(key=lambda r: (r.get('status') != 'RED', r.get('name', '')))
L.append(f'## 1. Built content needing action ({len(act)})')
L.append('')
L.append('Subjects we ship that are RED or AMBER — real 2027-cohort exposure.')
for r in act:
    L.append('')
    L.append(detail(r))
L.append('')

# 2. Sunsetting watch (fine for 2027, dying soon) — real end date with final/withdraw language
REAL_SUNSET = re.compile(r'final|withdraw|last exam|202[89]', re.I)
sun = [r for r in arr if r.get('built_status') in BUILT and r.get('status') != 'RED'
       and (r.get('withdrawal_end_date') or '').strip()
       and REAL_SUNSET.search(r.get('withdrawal_end_date', ''))]
sun = [r for r in sun if r not in act]
L.append(f'## 2. Sunsetting watch — built, fine for 2027 but withdrawing soon ({len(sun)})')
L.append('')
for r in sun:
    L.append(detail(r))
    L.append('')

# 3. Don't-build (not-built RED)
nb_red = [r for r in arr if r.get('built_status') == 'not-built' and r.get('status') == 'RED']
nb_red.sort(key=lambda r: r.get('board', ''))
L.append(f'## 3. Do NOT build — not-built specs that are withdrawn/superseded ({len(nb_red)})')
L.append('')
for r in nb_red:
    L.append(f"- `{r.get('board')}` **{r.get('name','?')}** `{r.get('spec_code','?')}` — {(r.get('action','') or '')[:200]}")
L.append('')

# 4. Build-ready AMBER (not-built, build to new version)
nb_amber = [r for r in arr if r.get('built_status') == 'not-built' and r.get('status') == 'AMBER']
L.append(f'## 4. Build with care — not-built AMBER (build to the current version) ({len(nb_amber)})')
L.append('')
for r in nb_amber:
    L.append(f"- `{r.get('board')}` **{r.get('name','?')}** `{r.get('spec_code','?')}` — {(r.get('action','') or '')[:200]}")
L.append('')

# 5. GREEN summary
greens = [r for r in arr if r.get('status') == 'GREEN']
L.append(f'## 5. GREEN — current & offered for 2027 ({len(greens)})')
L.append('')
L.append(f'{sum(1 for r in greens if r.get("built_status") in BUILT)} built (no action) · '
         f'{sum(1 for r in greens if r.get("built_status")=="not-built")} not-built (build-ready).')
L.append('')
L.append('<details><summary>Full GREEN list</summary>')
L.append('')
for r in sorted(greens, key=lambda r: (r.get('built_status', ''), r.get('name', ''))):
    L.append(f"- `{r.get('built_status')}` {r.get('name','?')} — {r.get('board','?')} `{r.get('spec_code','?')}`")
L.append('')
L.append('</details>')
L.append('')

io.open('docs/SPEC_CURRENCY_AUDIT_2027.md', 'w', encoding='utf-8').write('\n'.join(L))
print(f"wrote docs/SPEC_CURRENCY_AUDIT_2027.md | {dict(st)} | act-now={len(act)} sunset={len(sun)} dont-build={len(nb_red)}")
