"""Fix the 4 'read this specific chart' problems in Unit 2 that were left
as prose descriptions. Concept/calculation questions that just MENTION
chart names are not touched (they don't need a chart shown).

Targets:
  L01 Q11 (silver #3) — misleading truncated-y-axis bar chart
  L01 Q18 (gold #4)   — misleading pictogram with different-sized symbols
  L03 Q20 (gold #6)   — comparing two frequency polygons
  L04 Q19 (gold #5)   — histogram drawn with frequency on y instead of FD
"""
import os, requests, json, copy

URL = os.environ['SUPABASE_URL']; KEY = os.environ['SUPABASE_SERVICE_KEY']
H = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'}


def get_lesson(unit_slug, lesson_num):
    sid = requests.get(f"{URL}/rest/v1/subjects", headers=H, params={"slug": "eq.statistics-aqa", "school_id": "is.null", "select": "id"}).json()[0]['id']
    units = requests.get(f"{URL}/rest/v1/units", headers=H, params={"subject_id": f"eq.{sid}", "slug": f"eq.{unit_slug}", "select": "id"}).json()
    return requests.get(f"{URL}/rest/v1/lessons", headers=H, params={"unit_id": f"eq.{units[0]['id']}", "lesson_number": f"eq.{lesson_num}", "select": "id,practice_data,slug"}).json()[0]


def put_lesson(lid, practice_data):
    r = requests.patch(f"{URL}/rest/v1/lessons", headers=H, params={"id": f"eq.{lid}"}, json={"practice_data": practice_data})
    if r.status_code >= 300:
        raise RuntimeError(f"PATCH failed: {r.status_code} {r.text[:200]}")


def sync_json(slug, practice_data):
    path = f"scripts/_content_statistics-aqa/lessons/{slug}.json"
    with open(path, "r", encoding="utf-8-sig") as f: j = json.load(f)
    j['practice_data'] = practice_data
    with open(path, "w", encoding="utf-8") as f: json.dump(j, f, indent=2, ensure_ascii=False)


# =====================================================================
# Fix 1: L01 tally-charts-tabulation-and-pictograms — Silver #3 + Gold #4
# =====================================================================
def fix_L01():
    L = get_lesson("representing-data", 1)
    pd = copy.deepcopy(L['practice_data'])

    # Silver #3 — misleading truncated bar chart
    p = pd['problem_bank']['silver'][2]
    p['display'] = (
        '<p>A reporter shows the bar chart below and claims Group B scored '
        'twice as many points as Group A. Read the chart carefully — what is the correct response?</p>'
    )
    p['chart'] = {
        "type": "bar",
        "data": {
            "labels": ["Group A", "Group B"],
            "datasets": [{
                "label": "Score",
                "data": [80, 100],
                "backgroundColor": ["#2563eb", "#7c3aed"],
                "borderColor": ["#1e40af", "#6d28d9"],
                "borderWidth": 1
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {"display": False},
                "title": {"display": True, "text": "Reporter's bar chart (y-axis starts at 50)"}
            },
            "scales": {
                "y": {"min": 50, "max": 110, "title": {"display": True, "text": "Score"}},
                "x": {"title": {"display": False}}
            }
        }
    }

    # Gold #4 — misleading pictogram with different-sized symbols
    # 4 train routes, each row uses a symbol that grows with the count (visually misleading).
    p = pd['problem_bank']['gold'][3]
    # SVG: 4 rows, each with a single circle whose RADIUS scales with the passenger count.
    # This is exactly the misleading practice the question asks the student to spot.
    counts = [(80, "Route 1"), (160, "Route 2"), (240, "Route 3"), (320, "Route 4")]
    svg_rows = ['<svg class="pictogram" viewBox="0 0 460 220" width="100%" xmlns="http://www.w3.org/2000/svg">']
    for i, (count, name) in enumerate(counts):
        y = 25 + i * 50
        r = 10 + (count / 320) * 28  # radius scales 10..38px
        svg_rows.append(f'<text x="80" y="{y+4}" text-anchor="end" font-family="Inter,sans-serif" font-size="13">{name}</text>')
        svg_rows.append(f'<circle cx="120" cy="{y}" r="{r:g}" fill="#7c3aed"/>')
        svg_rows.append(f'<text x="200" y="{y+4}" font-family="Inter,sans-serif" font-size="12" fill="#555">= {count} passengers</text>')
    svg_rows.append('</svg>')
    pictogram_svg = ''.join(svg_rows)
    p['display'] = (
        '<p>The pictogram below shows the number of passengers on four train routes. '
        'A single symbol is used per row, but the symbols are drawn at different sizes proportional to the number of passengers. '
        f'Which statement best describes why this is a misleading representation?</p>{pictogram_svg}'
    )

    put_lesson(L['id'], pd)
    sync_json(L['slug'], pd)
    print(f"  [OK] L01 ({L['slug']}): Silver #3 + Gold #4 charts embedded")


# =====================================================================
# Fix 2: L03 frequency-polygons — Gold #6 (compare two polygons)
# =====================================================================
def fix_L03():
    L = get_lesson("representing-data", 3)
    pd = copy.deepcopy(L['practice_data'])
    p = pd['problem_bank']['gold'][5]
    p['display'] = (
        '<p>The frequency polygons below show the test scores of two groups. '
        'A student claims that because Group A\'s polygon is always above Group B\'s, '
        'Group A must have a higher mean score. Which response correctly evaluates the claim?</p>'
    )
    p['chart'] = {
        "type": "line",
        "data": {
            "labels": ["5", "15", "25", "35", "45", "55"],
            "datasets": [
                {"label": "Group A", "data": [4, 10, 18, 16, 8, 4], "borderColor": "#2563eb", "backgroundColor": "rgba(37,99,235,0.1)", "tension": 0, "fill": False},
                {"label": "Group B", "data": [2, 6, 10, 8, 4, 2], "borderColor": "#7c3aed", "backgroundColor": "rgba(124,58,237,0.1)", "tension": 0, "fill": False}
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {"display": True, "text": "Test scores — two groups"},
                "legend": {"display": True}
            },
            "scales": {
                "x": {"title": {"display": True, "text": "Score (class midpoint)"}},
                "y": {"title": {"display": True, "text": "Frequency"}, "beginAtZero": True}
            }
        }
    }
    put_lesson(L['id'], pd)
    sync_json(L['slug'], pd)
    print(f"  [OK] L03 ({L['slug']}): Gold #6 chart embedded")


# =====================================================================
# Fix 3: L04 histograms — Gold #5 (wrong-y-axis histogram)
# =====================================================================
def fix_L04():
    L = get_lesson("representing-data", 4)
    pd = copy.deepcopy(L['practice_data'])
    p = pd['problem_bank']['gold'][4]
    # Classes of unequal width: 0–5, 5–10, 10–20, 20–40 with frequencies 10, 12, 16, 8.
    # Drawn (incorrectly) with FREQUENCY on the y-axis rather than frequency density.
    # The 10–20 bar appears equally tall as 5–10, and the 20–40 bar looks low, even though
    # density would tell a different story.
    p['display'] = (
        '<p>A student has drawn the histogram below for the classes 0–5, 5–10, 10–20, 20–40 '
        'with frequencies 10, 12, 16, 8 — but they have used <strong>frequency</strong> on the y-axis '
        'instead of <strong>frequency density</strong>. Both bars for 10–20 and 20–40 are drawn the same width as the others. '
        'Which response correctly identifies what is wrong?</p>'
    )
    p['chart'] = {
        "type": "bar",
        "data": {
            "labels": ["0–5", "5–10", "10–20", "20–40"],
            "datasets": [{
                "label": "Frequency",
                "data": [10, 12, 16, 8],
                "backgroundColor": "#0d9488",
                "borderColor": "#0f766e",
                "borderWidth": 1,
                "barPercentage": 1.0,
                "categoryPercentage": 1.0
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {"display": False},
                "title": {"display": True, "text": "Student's histogram (wrong y-axis)"}
            },
            "scales": {
                "x": {"title": {"display": True, "text": "Class (note: bars have equal width but classes don't!)"}},
                "y": {"title": {"display": True, "text": "Frequency (incorrect — should be frequency density)"}, "beginAtZero": True}
            }
        }
    }
    put_lesson(L['id'], pd)
    sync_json(L['slug'], pd)
    print(f"  [OK] L04 ({L['slug']}): Gold #5 chart embedded")


if __name__ == "__main__":
    fix_L01()
    fix_L03()
    fix_L04()
    print("\nDone — 4 prose-described charts now properly embedded.")
