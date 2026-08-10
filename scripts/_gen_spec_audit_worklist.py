"""Generate the spec-currency audit work-list.

Scopes:
  --scope free   (default) live free-tier subjects only (annual maintenance check)
  --scope full   EVERY catalogued spec (specs/index.json, all boards) UNIONED with
                 everything we actually ship (any school_id) — the full build-universe
                 map: built + unbuilt, all subjects, all boards.

Each item: {slug, name, board, spec_code, built (date or ''), built_status}
built_status in: free | school | both | not-built

Feeds the spec-currency-audit-2027 workflow. Re-run before each annual sweep.
Usage: python scripts/_gen_spec_audit_worklist.py [--scope free|full]
"""
import sys, json, io, re, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client


# Live rows sometimes store component/unit codes rather than the qualification
# code the catalogue uses. Without these aliases the token join fails and the
# qualification appears twice in the audit — once researched via the live-row
# fallthrough, once wrongly as "not-built" from the catalogue side (seen in
# the 2027 audit: Unity Music and Sport Science).
ALIASES = {
    'C660U': 'C660QS',   # Unity Music: Eduqas component prefix vs qual code
    'R180': 'J828',      # Unity Sport Science: exam unit vs Cambridge National
}


def tokens(code):
    toks = set(t for t in re.split(r'[\s/,;]+', (code or '').upper()) if t)
    toks |= {ALIASES[t] for t in toks if t in ALIASES}
    return toks


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scope', choices=['free', 'full'], default='free')
    args = ap.parse_args(); sb = get_client()

    live = (sb.table('subjects').select('slug,name,exam_board,spec_code,school_id,created_at')
            .eq('status', 'live').order('name').execute().data)

    if args.scope == 'free':
        work = [{
            'slug': r['slug'], 'name': r['name'], 'board': (r.get('exam_board') or '').strip(),
            'spec_code': (r.get('spec_code') or '').strip(), 'built': (r.get('created_at') or '')[:10],
            'built_status': 'free',
        } for r in live if r.get('school_id') is None]
        _write(work); return

    # --- full scope: specs/index.json universe UNION everything we ship ---
    specs = json.load(io.open('specs/index.json', encoding='utf-8'))
    # index live subjects by spec-code token for build-status matching
    work = []
    matched_live = set()
    for s in specs:
        code = (s.get('spec_code') or '').strip()
        ctoks = tokens(code)
        builders = [r for r in live if ctoks & tokens(r.get('spec_code'))]
        if builders:
            schools = {('free' if b.get('school_id') is None else 'school') for b in builders}
            status = 'both' if len(schools) > 1 else next(iter(schools))
            built = min((b.get('created_at') or '')[:10] for b in builders if b.get('created_at')) or ''
            for b in builders:
                matched_live.add(b['slug'])
        else:
            status, built = 'not-built', ''
        work.append({
            'slug': s.get('slug') or code, 'name': s.get('subject') or '?',
            'board': s.get('board') or '?', 'spec_code': code, 'built': built, 'built_status': status,
        })
    # append live subjects whose spec didn't match any index spec (e.g. NCFE, BTEC, some L1/2)
    for r in live:
        if r['slug'] in matched_live:
            continue
        work.append({
            'slug': r['slug'], 'name': r['name'], 'board': (r.get('exam_board') or '').strip(),
            'spec_code': (r.get('spec_code') or '').strip(), 'built': (r.get('created_at') or '')[:10],
            'built_status': ('free' if r.get('school_id') is None else 'school'),
        })
    _write(work)


def _write(work):
    io.open('scripts/_spec_audit_worklist.json', 'w', encoding='utf-8').write(json.dumps(work, ensure_ascii=False, indent=1))
    from collections import Counter
    bs = Counter(w['built_status'] for w in work)
    miss = [w['slug'] for w in work if not w['spec_code']]
    print(f"wrote scripts/_spec_audit_worklist.json: {len(work)} qualifications | build status {dict(bs)}")
    if miss:
        print(f"  WARN: {len(miss)} missing spec_code: {miss[:10]}")


if __name__ == '__main__':
    main()
