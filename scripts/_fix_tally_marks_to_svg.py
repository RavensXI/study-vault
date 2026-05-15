"""Convert text-based tally marks (||||, |||| ||) to inline SVG with proper
4-verticals-plus-diagonal-strikethrough rendering on each 5-group.

The Unit 2 regen agent rendered tally marks as plain pipe characters in
the Tally column of tally-chart tables. That's not how tally marks are
written in real life (the 5th mark is a diagonal strikethrough across the
prior four) and not how GCSE papers print them. Replacing with SVG.
"""
import os, re, json, requests
from html import unescape

URL = os.environ['SUPABASE_URL']; KEY = os.environ['SUPABASE_SERVICE_KEY']
H = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'}

# Cells that look like text tallies: only pipes and spaces, at least 1 pipe
TALLY_TEXT_RE = re.compile(r'^\s*[\|\s]+\s*$')

LINE_HEIGHT = 18
PADDING_Y = 2
STROKE_X = 4       # horizontal spacing between vertical strokes
STROKE_W = 1.6
GROUP_GAP = 8
EDGE_PAD = 3


def tally_svg(n):
    """Return inline SVG rendering of a tally count for n >= 0."""
    if n <= 0:
        return ''
    groups = n // 5
    rem = n % 5
    parts = []
    x = EDGE_PAD
    for _ in range(groups):
        # 4 vertical lines per 5-group
        for i in range(4):
            xi = x + i * STROKE_X
            parts.append(f'<line x1="{xi}" y1="{PADDING_Y}" x2="{xi}" y2="{PADDING_Y + LINE_HEIGHT}" stroke="currentColor" stroke-width="{STROKE_W}" stroke-linecap="round"/>')
        # diagonal strikethrough across the 4 (top-right -> bottom-left)
        x_left = x - 2
        x_right = x + 3 * STROKE_X + 2
        y_top = PADDING_Y + 2
        y_bot = PADDING_Y + LINE_HEIGHT - 2
        parts.append(f'<line x1="{x_right}" y1="{y_top}" x2="{x_left}" y2="{y_bot}" stroke="currentColor" stroke-width="{STROKE_W}" stroke-linecap="round"/>')
        x += 3 * STROKE_X + GROUP_GAP + 4  # advance past the 4 verticals + gap to next group
    # Remainder loose vertical lines
    for i in range(rem):
        xi = x + i * STROKE_X
        parts.append(f'<line x1="{xi}" y1="{PADDING_Y}" x2="{xi}" y2="{PADDING_Y + LINE_HEIGHT}" stroke="currentColor" stroke-width="{STROKE_W}" stroke-linecap="round"/>')
    if rem:
        x += (rem - 1) * STROKE_X
    total_w = x + EDGE_PAD
    total_h = LINE_HEIGHT + PADDING_Y * 2
    return (f'<svg class="tally" viewBox="0 0 {total_w} {total_h}" '
            f'width="{total_w}" height="{total_h}" '
            f'xmlns="http://www.w3.org/2000/svg" aria-label="tally of {n}">'
            + ''.join(parts) + '</svg>')


def count_pipes(text):
    """Count tally marks (pipes) in a string, ignoring whitespace."""
    return text.count('|')


# Replace tally cells in a tally-chart table. We only touch the 2nd column.
TR_RE = re.compile(r'<tr\b[^>]*>(.*?)</tr>', re.IGNORECASE | re.DOTALL)
TD_RE = re.compile(r'<td\b[^>]*>(.*?)</td>', re.IGNORECASE | re.DOTALL)


def fix_tally_chart(html):
    """Find tally-chart tables and rewrite the 2nd <td> in each data row.

    Truth-source priority:
      1. Frequency number in the 3rd <td> (if numeric). Tally SVG matches that.
      2. Pipe count from the 2nd <td>. Used when the frequency is '?' (the
         student answers by counting marks).
    """
    changes = 0
    def fix_row(tr_match):
        nonlocal changes
        tr = tr_match.group(0)
        cells = list(TD_RE.finditer(tr))
        if len(cells) < 2:
            return tr
        tally_cell = cells[1]
        inner = tally_cell.group(1).strip()
        # Detect either text-tally or existing SVG-tally
        has_text_tally = TALLY_TEXT_RE.match(unescape(inner).strip())
        existing_svg_count_m = re.search(r'aria-label="tally of (\d+)"', inner)
        if not has_text_tally and not existing_svg_count_m:
            return tr
        # Determine the target count
        n = None
        if len(cells) >= 3:
            freq_inner = unescape(cells[2].group(1).strip())
            freq_text = re.sub(r'<[^>]+>', '', freq_inner).strip()
            try:
                n = int(freq_text)
            except (ValueError, TypeError):
                n = None
        if n is None:
            # No frequency truth — fall back to pipe count or existing SVG count
            if has_text_tally:
                n = count_pipes(unescape(inner))
            elif existing_svg_count_m:
                n = int(existing_svg_count_m.group(1))
        if not n or n <= 0:
            return tr
        # Skip rewrite if cell already has the right SVG count
        if existing_svg_count_m and int(existing_svg_count_m.group(1)) == n:
            return tr
        svg = tally_svg(n)
        new_td = tr[:tally_cell.start()] + f'<td>{svg}</td>' + tr[tally_cell.end():]
        changes += 1
        return new_td
    new_html = TR_RE.sub(fix_row, html)
    return new_html, changes


def fix_practice_data(pd):
    total = 0
    for tier in ('bronze', 'silver', 'gold'):
        for p in pd.get('problem_bank', {}).get(tier, []) or []:
            disp = p.get('display') or ''
            if 'tally-chart' not in disp:
                continue
            new_disp, n = fix_tally_chart(disp)
            if n:
                p['display'] = new_disp
                total += n
    for we in pd.get('worked_examples', []) or []:
        q = we.get('question') or ''
        if 'tally-chart' in q:
            new_q, n = fix_tally_chart(q)
            if n:
                we['question'] = new_q
                total += n
        for step in we.get('steps', []) or []:
            c = step.get('content') or ''
            if 'tally-chart' in c:
                new_c, n = fix_tally_chart(c)
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
            print(f"  [{status}] {L['slug']:60s}  {n} tally rows -> SVG")
    print(f"\nLessons changed: {lessons_changed}.  Total tally rows converted: {total_changes}.")


if __name__ == "__main__":
    main()
