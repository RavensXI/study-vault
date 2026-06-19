"""Generate the spec-currency audit work-list: every LIVE free-tier subject
(school_id NULL) with its board + spec code + build date. Feeds the
spec-currency-audit-2027 workflow (.claude/workflows/). Re-run before each
annual sweep so the ledger reflects the current catalogue.

Usage: python scripts/_gen_spec_audit_worklist.py
Writes: scripts/_spec_audit_worklist.json
"""
import sys, json, io
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client


def main():
    sb = get_client()
    rows = (sb.table('subjects').select('slug,name,exam_board,spec_code,created_at')
            .is_('school_id', 'null').eq('status', 'live').order('name').execute().data)
    work = [{
        'slug': r['slug'],
        'name': r['name'],
        'board': (r.get('exam_board') or '').strip(),
        'spec_code': (r.get('spec_code') or '').strip(),
        'built': (r.get('created_at') or '')[:10],
    } for r in rows]
    io.open('scripts/_spec_audit_worklist.json', 'w', encoding='utf-8').write(
        json.dumps(work, ensure_ascii=False, indent=1))
    missing = [w['slug'] for w in work if not w['spec_code']]
    print(f"wrote scripts/_spec_audit_worklist.json: {len(work)} live free-tier subjects")
    if missing:
        print(f"  WARN: {len(missing)} missing spec_code: {missing}")


if __name__ == '__main__':
    main()
