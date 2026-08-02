"""
Surgical removal of OCR spec-code leakage from Cambridge National content.
MECHANICAL, high-confidence fixes only:
  1. Unit subtitles: strip the 'RNNN externally assessed unit: ' prefix.
  2. content_html/exam_tip_html/conclusion_html: strip bare parenthetical spec
     codes like ' (1.1.1)' / ' (2.1)' — pure digits+dots only, so real
     measurements like '(5.71 Ω)', '(7.3 lb)', '(BMI 18.5-24.9)' are untouched.

Does NOT touch ECE R44/R129 (genuine car-seat standards) or any measurement.
Prose R-code references (e.g. 'OCR R038 requires...') are left for an agent pass.

Usage: python scripts/_fix_cn_codes.py [--commit]
"""
import sys, re, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

SLUGS = ['cambridge-nationals-child-development', 'cambridge-nationals-creative-imedia',
         'cambridge-nationals-engineering-design', 'cambridge-nationals-engineering-manufacture',
         'cambridge-nationals-engineering-programmable-systems', 'cambridge-nationals-sport-science']

SUBTITLE_PREFIX = re.compile(r'^R\d{3}\s+externally assessed unit:\s*', re.I)
# bare parenthetical spec code: '(1.1)', '(1.1.1)', '(2.1)' — pure numeric/dots only
PAREN_CODE = re.compile(r'\s*\((\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\)')


def fix_subtitle(s):
    if not s:
        return s, False
    new = SUBTITLE_PREFIX.sub('', s)
    if new != s:
        new = new[:1].upper() + new[1:]
        return new, True
    return s, False


def fix_body(html):
    if not html:
        return html, 0
    new, n = PAREN_CODE.subn('', html)
    return new, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--commit', action='store_true')
    args = ap.parse_args()
    sb = get_client()

    sub_fixed = body_fixed = 0
    for slug in SLUGS:
        sid = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').single().execute().data['id']
        units = sb.table('units').select('id,slug,subtitle').eq('subject_id', sid).order('sort_order').execute().data
        for u in units:
            new_sub, changed = fix_subtitle(u.get('subtitle'))
            if changed:
                sub_fixed += 1
                print(f"[SUBTITLE] {slug}/{u['slug']}")
                print(f"   - {u['subtitle'][:80]}")
                print(f"   + {new_sub[:80]}")
                if args.commit:
                    sb.table('units').update({'subtitle': new_sub}).eq('id', u['id']).execute()
            ls = sb.table('lessons').select('id,lesson_number,content_html,exam_tip_html,conclusion_html').eq('unit_id', u['id']).order('lesson_number').execute().data
            for l in ls:
                upd = {}
                tot = 0
                for fld in ('content_html', 'exam_tip_html', 'conclusion_html'):
                    nv, n = fix_body(l.get(fld))
                    if n:
                        upd[fld] = nv
                        tot += n
                if tot:
                    body_fixed += 1
                    print(f"[PAREN-CODES x{tot}] {slug}/{u['slug']} L{l['lesson_number']:02d}")
                    if args.commit:
                        sb.table('lessons').update(upd).eq('id', l['id']).execute()
    print(f"\n{'COMMITTED' if args.commit else 'DRY-RUN'}: {sub_fixed} subtitles, {body_fixed} lessons with paren-codes stripped")


if __name__ == '__main__':
    main()
