"""Repair half-disc rendering in pictogram SVGs across statistics-aqa.

The Unit 2 regen agent generated half-discs with a path like:
   <path d="M132,105 a10,10 0 0,1 0,-20 Z" fill="..."/>

This arcs upward from the row baseline, putting the half-disc centred 10px
ABOVE the row (visually as a 'moon' floating above the circle). On some rows
the X is also wrong (placed at the right edge of the penultimate circle
instead of the last one).

Fix: for each broken path, group circles by row (same cy), determine the
row's spacing and last cx, then rewrite the path as a right-half-disc
at the next slot, vertically aligned with the row:
   <path d="M{new_cx},{cy-r} A {r},{r} 0 0,1 {new_cx},{cy+r} Z" fill="..."/>
"""
import os, re, json, sys, requests
from collections import defaultdict

URL = os.environ['SUPABASE_URL']; KEY = os.environ['SUPABASE_SERVICE_KEY']
H = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'}

CIRCLE_RE = re.compile(r'<circle\s+cx="([\d.]+)"\s+cy="([\d.]+)"\s+r="([\d.]+)"\s+fill="([^"]+)"\s*/>')
# Match the broken half-disc pattern (with optional intervening `m{dx},{dy}`).
BROKEN_PATH_RE = re.compile(
    r'<path\s+d="M([\d.]+),([\d.]+)(?:\s+m-?[\d.]+,-?[\d.]+)?\s+a([\d.]+),([\d.]+)\s+0\s+0,1\s+0,-([\d.]+)\s+Z"\s+fill="([^"]+)"\s*/>'
)
# Match the broken QUARTER-disc pattern (two chained arcs).
# Example: M160,65 m-9,0 a9,9 0 0 1 0,-18 a9,9 0 0 1 4.5,7.8 Z
BROKEN_QUARTER_RE = re.compile(
    r'<path\s+d="M([\d.]+),([\d.]+)(?:\s+m-?[\d.]+,-?[\d.]+)?\s+a([\d.]+),([\d.]+)\s+0\s+0\s*,?\s*1\s+0,-[\d.]+\s+a[\d.]+,[\d.]+\s+0\s+0\s*,?\s*1\s+[\d.]+,[\d.]+\s+Z"\s+fill="([^"]+)"\s*/>'
)


def fix_svg(svg):
    """Rewrite broken half-disc paths in a single SVG block."""
    # Index circles by row (cy). Some SVGs have multiple rows of circles.
    circles = [(float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4))
               for m in CIRCLE_RE.finditer(svg)]
    if not circles:
        return svg, 0

    rows = defaultdict(list)
    for cx, cy, r, fill in circles:
        rows[round(cy)].append((cx, r, fill))
    for cy in rows:
        rows[cy].sort()  # sort by cx

    changes = 0

    def find_row(m_y, r):
        candidate_rows = sorted(rows.keys(), key=lambda cy: abs(cy - m_y))
        if not candidate_rows:
            return None
        row_cy = candidate_rows[0]
        if abs(row_cy - m_y) > r * 1.5:
            return None
        return row_cy

    def next_slot(row_cy, r):
        row_circles = rows[row_cy]
        last_cx = row_circles[-1][0]
        if len(row_circles) >= 2:
            spacing = row_circles[-1][0] - row_circles[-2][0]
        else:
            spacing = r * 2 + 4
        return last_cx + spacing

    def rewrite_half(match):
        nonlocal changes
        m_y = float(match.group(2))
        r = float(match.group(3))
        fill = match.group(6)
        row_cy = find_row(m_y, r)
        if row_cy is None: return match.group(0)
        new_cx = next_slot(row_cy, r)
        top_y = row_cy - r; bot_y = row_cy + r
        changes += 1
        return (f'<path d="M{new_cx:g},{top_y:g} A{r:g},{r:g} 0 0,1 {new_cx:g},{bot_y:g} Z" '
                f'fill="{fill}"/>')

    def rewrite_quarter(match):
        nonlocal changes
        m_y = float(match.group(2))
        r = float(match.group(3))
        fill = match.group(5)
        row_cy = find_row(m_y, r)
        if row_cy is None: return match.group(0)
        new_cx = next_slot(row_cy, r)
        # Top-right quarter-disc, centred at (new_cx, row_cy):
        # from (new_cx, row_cy-r) arc clockwise to (new_cx+r, row_cy), then line back to centre.
        top_y = row_cy - r
        right_x = new_cx + r
        changes += 1
        return (f'<path d="M{new_cx:g},{row_cy:g} L{new_cx:g},{top_y:g} '
                f'A{r:g},{r:g} 0 0,1 {right_x:g},{row_cy:g} Z" '
                f'fill="{fill}"/>')

    # Quarter pattern first (more specific — two arcs)
    new_svg = BROKEN_QUARTER_RE.sub(rewrite_quarter, svg)
    new_svg = BROKEN_PATH_RE.sub(rewrite_half, new_svg)
    return new_svg, changes


def fix_practice_data(pd):
    """Walk problem_bank + worked_examples, fix any embedded SVGs."""
    total = 0
    for tier in ('bronze', 'silver', 'gold'):
        for p in pd.get('problem_bank', {}).get(tier, []) or []:
            disp = p.get('display') or ''
            if '<svg' not in disp:
                continue
            new_disp, n = fix_svg(disp)
            if n:
                p['display'] = new_disp
                total += n
    for we in pd.get('worked_examples', []) or []:
        q = we.get('question') or ''
        new_q, n = fix_svg(q)
        if n:
            we['question'] = new_q
            total += n
        for step in we.get('steps', []) or []:
            content = step.get('content') or ''
            new_c, n = fix_svg(content)
            if n:
                step['content'] = new_c
                total += n
    return total


def main():
    sid = requests.get(f"{URL}/rest/v1/subjects", headers=H, params={"slug": "eq.statistics-aqa", "school_id": "is.null", "select": "id"}).json()[0]['id']
    units = requests.get(f"{URL}/rest/v1/units", headers=H, params={"subject_id": f"eq.{sid}", "select": "id,slug"}).json()
    unit_ids = [u['id'] for u in units]
    lessons = requests.get(f"{URL}/rest/v1/lessons", headers=H, params={"unit_id": f"in.({','.join(unit_ids)})", "select": "id,slug,practice_data"}).json()
    total_changes = 0
    lessons_changed = 0
    for L in lessons:
        pd = L.get('practice_data')
        if not pd:
            continue
        n = fix_practice_data(pd)
        if n:
            lessons_changed += 1
            total_changes += n
            r = requests.patch(f"{URL}/rest/v1/lessons", headers=H, params={"id": f"eq.{L['id']}"}, json={"practice_data": pd})
            status = "OK" if r.status_code < 300 else f"FAIL {r.status_code}"
            print(f"  [{status}] {L['slug']:60s}  {n} half-disc fixes")
    print(f"\nLessons changed: {lessons_changed}.  Total half-disc fixes: {total_changes}.")


if __name__ == "__main__":
    main()
