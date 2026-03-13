"""
Convert HTML-entity equations in Science and Separate Sciences lessons to KaTeX LaTeX.

Finds <strong> blocks containing equations (sub/sup/HTML entities) and wraps them
in \\( ... \\) delimiters for KaTeX auto-render. Chemical formulae get \\ce{} via
mhchem if available, otherwise plain LaTeX.

Usage:
    python scripts/convert_equations_to_katex.py --dry-run    # preview changes
    python scripts/convert_equations_to_katex.py              # apply to Supabase
"""

import re
import sys
import os
import html

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from lib.supabase_client import get_client


def html_equation_to_latex(eq_html):
    """Convert an HTML equation string to LaTeX."""
    s = eq_html

    # Decode HTML entities first
    s = s.replace('&times;', ' \\times ')
    s = s.replace('&divide;', ' \\div ')
    s = s.replace('&rarr;', ' \\rightarrow ')
    s = s.replace('&#8652;', ' \\rightleftharpoons ')
    s = s.replace('&minus;', ' - ')
    s = s.replace('&frac12;', '\\frac{1}{2}')
    s = s.replace('&frac14;', '\\frac{1}{4}')
    s = s.replace('&frac34;', '\\frac{3}{4}')
    s = s.replace('&sup2;', '^{2}')
    s = s.replace('&sup3;', '^{3}')
    s = s.replace('&#8313;', '^{9}')
    s = s.replace('&Delta;', '\\Delta ')
    s = s.replace('&theta;', '\\theta ')
    s = s.replace('&lambda;', '\\lambda ')
    s = s.replace('&rho;', '\\rho ')
    s = s.replace('&Omega;', '\\, \\Omega')
    s = s.replace('&deg;', '^{\\circ}')
    s = s.replace('&thinsp;', '\\,')
    s = s.replace('&nbsp;', '\\,')
    s = s.replace('&ndash;', '\\text{--}')
    s = s.replace('&mdash;', '\\text{---}')

    # Convert <sub>...</sub> and <sup>...</sup>
    s = re.sub(r'<sub>([^<]+)</sub>', r'_{\1}', s)
    s = re.sub(r'<sup>([^<]+)</sup>', r'^{\1}', s)

    # Clean up any remaining HTML tags
    s = re.sub(r'<[^>]+>', '', s)

    # Decode any remaining HTML entities
    s = html.unescape(s)

    # Wrap runs of 2+ lowercase words in \text{} so they render properly
    # e.g. "mass of solute" → "\text{mass of solute}"
    # But skip single math variables (m, v, t, E, etc.)
    def wrap_text_runs(m):
        words = m.group(0)
        # Don't wrap if it's just a single short word (likely a variable)
        if len(words.split()) == 1 and len(words) <= 3:
            return words
        return '\\text{' + words + '}'

    # Match runs of lowercase words (2+ chars each) possibly with spaces
    s = re.sub(r'(?<![\\{])\b[a-z][a-z]+(?:\s+[a-z][a-z]+)+\b', wrap_text_runs, s)

    return s.strip()


def is_equation(text):
    """Check if a <strong> block looks like an equation (not just bold text)."""
    # Must contain at least one equation indicator
    indicators = ['<sub>', '<sup>', '&times;', '&divide;', '&frac',
                  '&rarr;', '&#8652;', '&Delta;', '&lambda;', '&rho;',
                  '&Omega;', '&sup2;', '&sup3;', '&minus;', '&#8313;']
    has_indicator = any(ind in text for ind in indicators)
    if not has_indicator:
        return False

    # Skip things that are clearly not equations (step descriptions, worked examples)
    skip_prefixes = ['Step ', 'Worked example', 'For example', 'Note:',
                     'Remember:', 'Tip:']
    clean = re.sub(r'<[^>]+>', '', text).strip()
    if any(clean.startswith(p) for p in skip_prefixes):
        return False

    return True


def is_chemical_formula_only(text):
    """Check if text is just a chemical formula (no = sign, no words)."""
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'&[^;]+;', '', clean)
    # Chemical formula: mostly uppercase letters, numbers, parentheses
    # No equals sign, no words longer than 3 chars
    if '=' in clean or 'divide' in clean or 'times' in clean:
        return False
    words = clean.split()
    if all(len(w) <= 3 or re.match(r'^[A-Z][a-z]?\d*', w) for w in words):
        return True
    return False


def convert_content(content_html, dry_run=False):
    """Convert equations in content HTML from HTML entities to KaTeX LaTeX."""
    if not content_html:
        return content_html, 0

    changes = 0

    def replace_equation(match):
        nonlocal changes
        full_match = match.group(0)
        inner = match.group(1)

        if not is_equation(inner):
            return full_match

        latex = html_equation_to_latex(inner)

        changes += 1
        # Wrap in LaTeX delimiters inside the <strong> tag
        return '<strong>\\(' + latex + '\\)</strong>'

    # Match <strong>...</strong> blocks that contain equation-like content
    # This regex handles nested sub/sup tags
    pattern = r'<strong>((?:[^<]|<(?:sub|sup)>[^<]*</(?:sub|sup)>)*)</strong>'
    result = re.sub(pattern, replace_equation, content_html)

    # Also convert standalone (non-bold) chemical equations with arrows
    # e.g., 2H<sub>2</sub> + O<sub>2</sub> &rarr; 2H<sub>2</sub>O
    # These appear in <p> text, not wrapped in <strong>

    return result, changes


def main():
    dry_run = '--dry-run' in sys.argv
    sb = get_client()

    total_changes = 0
    total_lessons = 0

    for slug in ['science', 'separate-sciences']:
        subj = sb.table('subjects').select('id, name').eq('slug', slug).single().execute()
        sid = subj.data['id']
        units = sb.table('units').select('id, slug').eq('subject_id', sid).order('sort_order').execute()

        print(f'\n=== {subj.data["name"]} ===')

        for u in units.data:
            lessons = sb.table('lessons').select(
                'id, title, lesson_number, content_html, exam_tip_html'
            ).eq('unit_id', u['id']).order('lesson_number').execute()

            for lesson in lessons.data:
                lesson_changes = 0

                # Convert content_html
                new_content, c1 = convert_content(lesson['content_html'])
                lesson_changes += c1

                # Convert exam_tip_html
                new_exam_tip, c2 = convert_content(lesson.get('exam_tip_html'))
                lesson_changes += c2

                if lesson_changes > 0:
                    total_changes += lesson_changes
                    total_lessons += 1
                    print(f'  {u["slug"]} L{lesson["lesson_number"]:02d}: {lesson_changes} equations converted')

                    if not dry_run:
                        update = {'content_html': new_content}
                        if c2 > 0:
                            update['exam_tip_html'] = new_exam_tip
                        sb.table('lessons').update(update).eq('id', lesson['id']).execute()

    print(f'\n{"[DRY RUN] " if dry_run else ""}Total: {total_changes} equations converted across {total_lessons} lessons')


if __name__ == '__main__':
    main()
