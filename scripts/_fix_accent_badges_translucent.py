"""One-off: convert solid accent_badge hex values to translucent <accent>33 form.

Per memory rule feedback_accent_badge_must_be_translucent — the unit pill
background should be the accent colour at ~20% opacity, NOT a solid darker hex.
The overnight activation scripts produced solid darker badges; this fixes them
across all 4 subjects built last night.

Usage:
    python scripts/_fix_accent_badges_translucent.py            # dry-run
    python scripts/_fix_accent_badges_translucent.py --apply    # update Supabase
"""
import argparse, sys
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

SLUGS = [
    'electronics-eduqas',
    'geology-eduqas',
    'design-technology-eduqas',
    'computer-science-eduqas',
    'cambridge-nationals-enterprise-and-marketing',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    sb = get_client()
    n_total = n_changed = 0
    for slug in SLUGS:
        sub = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').execute().data
        if not sub:
            print(f'  SKIP {slug}: not found')
            continue
        units = sb.table('units').select('id, slug, accent, accent_badge').eq('subject_id', sub[0]['id']).order('sort_order').execute().data
        print(f'\n{slug}: {len(units)} units')
        for u in units:
            n_total += 1
            current = u['accent_badge'] or ''
            already_translucent = len(current) == 9 and current.lower().endswith('33')
            if already_translucent:
                print(f"  [skip ] {u['slug']:45s} already translucent {current}")
                continue
            new_badge = u['accent'] + '33'
            print(f"  [{'APPLY' if args.apply else 'dry  '}] {u['slug']:45s} {current} -> {new_badge}")
            if args.apply:
                sb.table('units').update({'accent_badge': new_badge}).eq('id', u['id']).execute()
            n_changed += 1
    print(f'\nTotal: {n_changed}/{n_total} units {"updated" if args.apply else "would be updated"}')


if __name__ == '__main__':
    main()
