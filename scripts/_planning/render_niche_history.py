"""Render scripts/_planning/niche_schools_history.html from dfe_niche_history.json.

Classifies every school that entered a niche subject in any available year, and
writes the class flags out to niche_school_classes.json so render_report.py can
stamp them onto Table 3 of remaining_builds_2025.html.

Self-contained page: no external stylesheet, font or script. The school tables
are painted from an embedded JSON block by a small inline script, so the file
stays around a megabyte instead of thirty.
"""

import html as H
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "dfe_niche_history.json"), encoding="utf-8"))
YEARS = D["years"]
LATEST = YEARS[-1]

CLASSES = ["NEW", "ESTABLISHED", "ALTERNATE", "INTERMITTENT", "ONE-OFF", "LAPSED"]
CLASS_RANK = {c: i for i, c in enumerate(CLASSES)}
APPROACH = {
    "NEW": "prospect",
    "ESTABLISHED": "department",
    "ALTERNATE": "timing",
    "INTERMITTENT": "timing",
    "ONE-OFF": "skip",
    "LAPSED": "skip",
}
CLASS_CSS = {
    "NEW": "tag-build",
    "ESTABLISHED": "tag-port",
    "ALTERNATE": "tag-warm",
    "INTERMITTENT": "tag-alias",
    "ONE-OFF": "tag-skip",
    "LAPSED": "tag-skip",
}


def e(x):
    return H.escape(str(x)) if x is not None else ""


def norm_subject(s):
    return re.sub(r"\s*/\s*", "/", re.sub(r"\s+", " ", str(s).strip())).lower()


# ---------------------------------------------------------------- classifying
def classify(present, comparable):
    """present: the comparable years in which the school had entries, in order.
    comparable: the years the row's series can actually be read across."""
    if not present:
        return "LAPSED"
    latest = comparable[-1]
    if latest not in present:
        # A single year, and not the latest, is a one-off. Two years or more
        # and then nothing is a department that closed.
        if len(present) == 1 and len(comparable) > 2:
            return "ONE-OFF"
        return "LAPSED"
    # in the latest year
    if len(comparable) > 2:
        since = comparable[-3:]              # 2022/23, 2023/24, 2024/25
        if all(y in present for y in since):
            return "ESTABLISHED"
        if present[0] in comparable[-2:]:
            return "NEW"
    else:
        if all(y in present for y in comparable):
            return "ESTABLISHED"
        return "NEW"
    # gaps between the first entry and now
    span = comparable[comparable.index(present[0]):]
    gap, worst = 0, 0
    for y in span:
        if y in present:
            worst = max(worst, gap)
            gap = 0
        else:
            gap += 1
    return "ALTERNATE" if worst <= 1 else "INTERMITTENT"


def prepare():
    subjects = []
    classes_out = {}
    for s in D["subjects"]:
        comp = s["comparable_years"]
        rows = []
        for sch in s["schools"]:
            ent = {y: int(sch["entries"].get(y, 0) or 0) for y in YEARS}
            present = [y for y in comp if ent.get(y, 0) > 0]
            if not present:
                continue                    # only appears outside the comparable window
            cls = classify(present, comp)
            rows.append({
                "urn": sch["urn"],
                "name": sch["name"],
                "type": sch["type"] or "",
                "n": [ent[y] for y in YEARS],
                "c": cls,
            })
        rows.sort(key=lambda r: (CLASS_RANK[r["c"]],
                                 -r["n"][len(YEARS) - 1],
                                 -sum(r["n"]), r["name"] or ""))

        counts = {c: 0 for c in CLASSES}
        for r in rows:
            counts[r["c"]] += 1

        # churn: schools kept, lost and gained between consecutive years
        sets = {y: {r["urn"] for r in rows if r["n"][YEARS.index(y)] > 0}
                for y in YEARS}
        churn = []
        for a, b in zip(comp, comp[1:]):
            prev, cur = sets[a], sets[b]
            kept = len(prev & cur)
            churn.append({
                "from": a, "to": b,
                "kept": kept,
                "lost": len(prev - cur),
                "gained": len(cur - prev),
                "retention": (kept / len(prev)) if prev else None,
            })

        first, last = comp[0], comp[-1]
        e0 = s["totals"][first]["entries"]
        e1 = s["totals"][last]["entries"]
        subjects.append({
            **{k: v for k, v in s.items() if k != "schools"},
            "rows": rows,
            "class_counts": counts,
            "churn": churn,
            "entries_change_pct": ((e1 - e0) / e0 * 100) if e0 else None,
            "schools_latest": s["totals"][LATEST]["schools"],
            "family_above_niche_line": s["totals"][LATEST]["entries"] > 3000
            and s["set"] == "table3",
        })
        classes_out[norm_subject(s["subject_discount_group"])] = {
            "mode": s["mode"],
            "comparable_years": comp,
            "taxonomy_break_2023_24": s["taxonomy_break_2023_24"],
            "schools": {r["urn"]: {"class": r["c"], "approach": APPROACH[r["c"]],
                                   "entries": r["n"]} for r in rows},
        }
    return subjects, classes_out


# ---------------------------------------------------------------- css / markup
CSS = """
*{box-sizing:border-box}
body{margin:0;background:#faf8f5;color:#2d2a26;
 font:15px/1.55 "Inter","Segoe UI",system-ui,-apple-system,sans-serif;}
.wrap{max-width:1360px;margin:0 auto;padding:2.5rem 1.5rem 5rem}
h1,h2,h3{font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
 font-weight:700;letter-spacing:-.01em;margin:0}
h1{font-size:2rem}
h2{font-size:1.35rem;margin:3rem 0 .35rem}
h3{font-size:1.02rem;margin:1.8rem 0 .5rem}
.sub{color:#7a736a;font-size:.85rem;margin:.4rem 0 0}
.lede{color:#5c554d;font-size:.95rem;margin:.6rem 0 0;max-width:76ch}
.hint{color:#7a736a;font-size:.82rem;margin:.35rem 0 1rem;max-width:92ch}
.cards{display:flex;flex-wrap:wrap;gap:.75rem;margin:1.75rem 0 .5rem}
.card{background:#fff;border-radius:16px;padding:.95rem 1.25rem;min-width:150px;
 box-shadow:0 1px 4px rgba(0,0,0,.05)}
.card .num{font-family:"Source Serif 4",Georgia,serif;font-size:1.6rem;font-weight:700;line-height:1}
.card .lbl{font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:#7a736a;margin-top:.35rem}
.card .fine{font-size:.72rem;color:#9a938a;margin-top:.2rem}
.panel{background:#fff;border-radius:16px;box-shadow:0 1px 4px rgba(0,0,0,.05);
 padding:1.1rem 1.35rem;margin:1rem 0}
.tw{overflow-x:auto;background:#fff;border-radius:16px;box-shadow:0 1px 4px rgba(0,0,0,.05)}
table{width:100%;border-collapse:collapse;font-size:.82rem}
th{text-align:left;background:#f6f3ee;padding:.6rem .8rem;border-bottom:1px solid #ece7de;
 font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:#7a736a;font-weight:600;
 white-space:nowrap;vertical-align:bottom}
td{padding:.5rem .8rem;border-bottom:1px solid #f4f1ea;vertical-align:top}
tr:last-child td{border-bottom:none}
tbody tr:hover td{background:#fcfbf8}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.rank{color:#9a938a;font-variant-numeric:tabular-nums}
td.zero{color:#c8c1b7}
td.nc{color:#c8c1b7;font-style:italic}
.mono{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;font-size:.76rem}
.strong{font-weight:600}
.note{color:#5c554d;font-size:.78rem;line-height:1.45}
.tag{display:inline-block;font-size:.62rem;font-weight:700;letter-spacing:.05em;
 padding:2px 6px;border-radius:4px;white-space:nowrap}
.tag-build{background:#dcecdf;color:#28502f}
.tag-port{background:#e2e6f2;color:#33406b}
.tag-alias{background:#f0e6f4;color:#5b3568}
.tag-skip{background:#eeeae4;color:#6d655b}
.tag-warm{background:#fbeccd;color:#7a5300}
.flag{display:inline-block;font-size:.62rem;font-weight:700;letter-spacing:.04em;
 padding:2px 6px;border-radius:4px;background:#fbeccd;color:#7a5300}
.ok{display:inline-block;font-size:.62rem;font-weight:700;letter-spacing:.04em;
 padding:2px 6px;border-radius:4px;background:#e4ece3;color:#2f5136}
.up{color:#8a5a00;font-weight:600}
.down{color:#3d6b8a;font-weight:600}
details{background:#fff;border-radius:16px;box-shadow:0 1px 4px rgba(0,0,0,.05);
 padding:.85rem 1.2rem;margin:.6rem 0}
summary{cursor:pointer;font-weight:600;font-size:.9rem;list-style:none}
summary::-webkit-details-marker{display:none}
summary:before{content:"\\25b8 ";color:#9a938a}
details[open] summary:before{content:"\\25be "}
.slug{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:baseline;
 font-weight:400;font-size:.78rem;color:#7a736a;margin-top:.35rem}
.slug b{color:#2d2a26;font-variant-numeric:tabular-nums}
.yrs{font-variant-numeric:tabular-nums;color:#5c554d;font-size:.78rem}
.mini{width:auto;font-size:.76rem;margin-top:.9rem}
.mini th,.mini td{padding:.35rem .7rem}
.mini{background:#faf8f5;border-radius:10px}
.stw{overflow-x:auto;margin-top:.9rem;border-top:1px solid #f0ece4}
ul.plain{font-size:.86rem;color:#5c554d;line-height:1.6;max-width:88ch}
a{color:#33406b}
footer{margin-top:3.5rem;font-size:.78rem;color:#9a938a}
.toolbar{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin:1.2rem 0 .4rem}
.toolbar input{font:inherit;font-size:.86rem;padding:.5rem .8rem;border:1px solid #e4ded4;
 border-radius:10px;background:#fff;min-width:320px;color:#2d2a26}
.toolbar button{font:inherit;font-size:.78rem;padding:.5rem .9rem;border:1px solid #e4ded4;
 border-radius:10px;background:#fff;color:#5c554d;cursor:pointer}
.toolbar button:hover{background:#f6f3ee}
#hits{margin:.4rem 0 0}
@media(max-width:720px){h1{font-size:1.5rem}.toolbar input{min-width:0;width:100%}}
"""

JS = """
const DATA = JSON.parse(document.getElementById('d').textContent);
const YEARS = DATA.years;
const CSS = DATA.css;
const esc = s => (s==null?'':String(s)).replace(/[&<>"]/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function cells(n, comp){
  let tds = '';
  YEARS.forEach((y,i) => {
    const off = comp.indexOf(y) < 0;
    const v = n[i];
    tds += `<td class="num${off?' nc':(v?'':' zero')}">${off?'n/c':(v?v.toLocaleString():'&mdash;')}</td>`;
  });
  return tds;
}

function rowHtml(r, comp){
  const [urn, n, c] = r, s = DATA.schools[urn] || ['', ''];
  return `<tr><td class="strong">${esc(s[0])}</td>`
       + `<td class="mono">${esc(urn)}</td>`
       + `<td class="note">${esc(s[1])}</td>`
       + cells(n, comp)
       + `<td><span class="tag ${CSS[c]}">${c}</span></td>`
       + `<td class="note">${DATA.approach[c]}</td></tr>`;
}

function paint(key){
  const box = document.getElementById('t-'+key);
  if(!box || box.dataset.done) return;
  const s = DATA.subjects.find(x => x.key === key);
  const head = '<tr><th>School or college</th><th>URN</th><th>Type</th>'
    + YEARS.map(y => `<th class="num">${y}</th>`).join('')
    + '<th>Class</th><th>Approach</th></tr>';
  box.innerHTML = '<div class="tw"><table><thead>' + head + '</thead><tbody>'
    + s.rows.map(r => rowHtml(r, s.comparable_years)).join('')
    + '</tbody></table></div>';
  box.dataset.done = '1';
}

document.querySelectorAll('details[data-key]').forEach(d => {
  d.addEventListener('toggle', () => { if(d.open) paint(d.dataset.key); });
});
document.getElementById('expand').addEventListener('click', () => {
  document.querySelectorAll('details[data-key]').forEach(d => {
    d.open = true; paint(d.dataset.key);
  });
});
document.getElementById('collapse').addEventListener('click', () => {
  document.querySelectorAll('details[data-key]').forEach(d => { d.open = false; });
});

const box = document.getElementById('hits');
document.getElementById('q').addEventListener('input', ev => {
  const q = ev.target.value.trim().toLowerCase();
  if(q.length < 3){ box.innerHTML = ''; return; }
  const hit = new Set();
  Object.keys(DATA.schools).forEach(u => {
    if(String(u).includes(q) || (DATA.schools[u][0]||'').toLowerCase().includes(q))
      hit.add(u);
  });
  const out = [];
  DATA.subjects.forEach(s => s.rows.forEach(r => {
    if(hit.has(r[0])) out.push({s, r});
  }));
  if(!out.length){ box.innerHTML = '<p class="hint">No school matches.</p>'; return; }
  out.sort((a,b) => (DATA.schools[a.r[0]][0]||'').localeCompare(DATA.schools[b.r[0]][0]||''));
  const head = '<tr><th>School or college</th><th>URN</th><th>Subject</th>'
    + YEARS.map(y => `<th class="num">${y}</th>`).join('')
    + '<th>Class</th></tr>';
  box.innerHTML = '<p class="hint">' + out.length + ' matching school-subject '
    + 'rows.</p><div class="tw"><table><thead>' + head + '</thead><tbody>'
    + out.slice(0,400).map(({s,r}) =>
        `<tr><td class="strong">${esc(DATA.schools[r[0]][0])}</td>`
        + `<td class="mono">${esc(r[0])}</td>`
        + `<td>${esc(s.subject_discount_group)}</td>`
        + cells(r[1], s.comparable_years)
        + `<td><span class="tag ${CSS[r[2]]}">${r[2]}</span></td></tr>`).join('')
    + '</tbody></table></div>'
    + (out.length > 400 ? '<p class="hint">First 400 shown.</p>' : '');
});
"""


def trend_mark(pct):
    if pct is None:
        return '<span class="note">&mdash;</span>'
    if pct > 2:
        return f'<span class="up">&#9650; {pct:+.0f}%</span>'
    if pct < -2:
        return f'<span class="down">&#9660; {pct:+.0f}%</span>'
    return f'<span class="note">&ndash; {pct:+.0f}%</span>'


def summary_block(s):
    comp = s["comparable_years"]
    head = ("<tr><th></th>" + "".join(f'<th class="num">{e(y)}</th>' for y in YEARS)
            + "</tr>")
    def line(label, get):
        cells = ""
        for y in YEARS:
            if y in comp:
                cells += f'<td class="num">{get(y):,}</td>'
            else:
                cells += '<td class="num nc">n/c</td>'
        return f"<tr><td>{label}</td>{cells}</tr>"
    body = (line("England entries", lambda y: s["totals"][y]["entries"])
            + line("Schools entering", lambda y: s["totals"][y]["schools"]))
    tbl = (f'<table class="mini"><thead>{head}</thead><tbody>{body}</tbody></table>')

    ch = ("<tr><th>Year on year</th><th class='num'>Kept</th>"
          "<th class='num'>Lost</th><th class='num'>Gained</th>"
          "<th class='num'>Retention</th></tr>")
    cb = ""
    for c in s["churn"]:
        ret = "&mdash;" if c["retention"] is None else f'{100 * c["retention"]:.0f}%'
        cb += (f'<tr><td>{e(c["from"])} &rarr; {e(c["to"])}</td>'
               f'<td class="num">{c["kept"]:,}</td>'
               f'<td class="num">{c["lost"]:,}</td>'
               f'<td class="num">{c["gained"]:,}</td>'
               f'<td class="num">{ret}</td></tr>')
    churn = f'<table class="mini"><thead>{ch}</thead><tbody>{cb}</tbody></table>'
    return (f'<div style="display:flex;gap:1.5rem;flex-wrap:wrap">{tbl}{churn}</div>')


def subject_panel(s):
    counts = s["class_counts"]
    chips = " ".join(
        f'<span class="tag {CLASS_CSS[c]}">{c} {counts[c]}</span>'
        for c in CLASSES if counts[c])
    notes = []
    if s["set"] == "extended":
        notes.append('<span class="tag tag-alias">EXTENDED</span> above the '
                     '3,000 line, named in the brief')
    if s["taxonomy_break_2023_24"]:
        notes.append('<span class="flag">TAXONOMY BREAK</span> DfE re-coded this '
                     'group in 2023/24, so only the last two years compare')
    if s["mode"] == "vocational":
        notes.append("all Level 1/2 awarding routes rolled together")
    if s["family_above_niche_line"]:
        notes.append("the whole family is above 3,000 entries &mdash; Table 3 "
                     f"counted only the {e(s['qualification'])} slice")
    note = ('<p class="hint" style="margin:.6rem 0 0">' + " &middot; ".join(notes)
            + "</p>") if notes else ""

    yrs = " ".join(
        f'{e(y)}&nbsp;'
        + (f'<b>{s["totals"][y]["entries"]:,}</b>' if y in s["comparable_years"]
           else '<span class="nc">n/c</span>')
        for y in YEARS)
    return (
        f'<details data-key="{e(s["key"])}">'
        f'<summary>{e(s["subject_discount_group"])}'
        f'<span class="slug">'
        f'<span>{e(s["qualification"])}</span>'
        f'<span class="yrs">Entries &nbsp;{yrs}</span>'
        f'<span>{trend_mark(s["entries_change_pct"])}</span>'
        f'<span><b>{s["schools_latest"]:,}</b> schools in {LATEST}</span>'
        f'<span>{chips}</span></span></summary>'
        f'{note}{summary_block(s)}'
        f'<div class="stw" id="t-{e(s["key"])}"></div>'
        f'</details>')


def main():
    subjects, classes_out = prepare()

    json.dump({"generated": time.strftime("%Y-%m-%d %H:%M"),
               "years": YEARS,
               "approach": APPROACH,
               "subjects": classes_out},
              open(os.path.join(HERE, "niche_school_classes.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=1)

    tot_rows = sum(len(s["rows"]) for s in subjects)
    tot_new = sum(s["class_counts"]["NEW"] for s in subjects)
    tot_est = sum(s["class_counts"]["ESTABLISHED"] for s in subjects)
    tot_lapsed = sum(s["class_counts"]["LAPSED"] + s["class_counts"]["ONE-OFF"]
                     for s in subjects)
    uniq = len({r["urn"] for s in subjects for r in s["rows"]})

    # School names and types repeat across subjects, so they live once in a
    # URN-keyed lookup and the rows carry only the URN. That is the difference
    # between a 3.5 Mb page and a 1.5 Mb one.
    lookup = {}
    for s in subjects:
        for r in s["rows"]:
            lookup.setdefault(r["urn"], [r["name"], r["type"]])
    payload = {
        "years": YEARS,
        "approach": APPROACH,
        "css": CLASS_CSS,
        "schools": lookup,
        "subjects": [{"key": s["key"],
                      "subject_discount_group": s["subject_discount_group"],
                      "comparable_years": s["comparable_years"],
                      "rows": [[r["urn"], r["n"], r["c"]] for r in s["rows"]]}
                     for s in subjects],
    }

    panels = "".join(subject_panel(s) for s in subjects)
    src = D["source"]
    ees = src["ees"]
    api_set = ees["api_data_sets"][0] if ees["api_data_sets"] else {}

    page = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Niche subjects — every school, every year</title>
<style>{CSS}</style></head>
<body><div class="wrap">

<h1>Niche subjects: every school, every available year</h1>
<p class="sub">England, key stage 4 &middot; {" &middot; ".join(YEARS)} &middot;
generated {e(D["generated"])} from DfE data, read-only</p>

<p class="lede">Table 3 of the To-Build page lists the small subjects and the ten
largest centres in each. This page is the whole list, and it adds time. For every
subject with 3,000 or fewer England entries in {LATEST} &mdash; plus the languages
named alongside them that sit just over the line &mdash; it takes every school that
entered a pupil in any year the data covers, lines the years up side by side, and
says what kind of centre it is.</p>

<p class="lede">The classes are simple. <span class="tag tag-build">NEW</span>
means the school's first entries fall in {YEARS[-2]} or {LATEST} &mdash; a course
that has just started, whose teacher is still building the resources and has
nothing on the shelf. That is the warmest prospect on the page.
<span class="tag tag-port">ESTABLISHED</span> means entries in every year from
2022/23 onwards: a real department, harder to displace but worth more when it
lands. <span class="tag tag-warm">ALTERNATE</span> means the entries skip a year
at a time, which is the ordinary shape of a small cohort taught every other year,
not a school losing interest &mdash; the approach is to check where they are in the
cycle. <span class="tag tag-alias">INTERMITTENT</span> is the same idea with a
longer gap. <span class="tag tag-skip">LAPSED</span> means entries earlier but
none in {LATEST}, and <span class="tag tag-skip">ONE-OFF</span> means a single
year that is not the latest. Both are cold.</p>

<h3>What the numbers cannot tell you</h3>
<ul class="plain">
<li><strong>England only.</strong> The source counts pupils at the end of key
stage 4 in English schools and colleges. Wales, Scotland and Northern Ireland are
absent, so a WJEC-heavy subject looks smaller here than it is.</li>
<li><strong>Independent schools are in.</strong> The performance tables cover
independent centres that enter pupils, and for Classical Greek, Latin, Ancient
History and Hebrew they dominate. The Type column says which is which, and an
independent school buys very differently from a state one.</li>
<li><strong>Two exam years are missing and cannot be recovered.</strong> Summer
2020 and summer 2021 were centre-assessed and teacher-assessed; no exams were sat
and DfE published no performance tables. 2018/19 exists but the download service
no longer serves it. So the deepest series available anywhere is four years, and
a school that taught a subject through the pandemic and stopped in 2022 is
invisible.</li>
<li><strong>A single latest-year appearance is ambiguous.</strong> One entry in
{LATEST} and nothing before reads as NEW, but it is equally consistent with a
departing teacher's last cohort, a private candidate sitting at a nearby centre,
or a single pupil entered for a heritage language they already speak. For the
heritage languages that last case is the common one, which is why Polish, Chinese
and Portuguese show thousands of schools and almost no departments.</li>
<li><strong>Alternate-year cohorts are real.</strong> A school with eight takers
often runs the option every other year. Do not read a one-year gap as a loss.</li>
<li><strong>The vocational groups were re-coded in 2023/24.</strong> DfE folded
BTEC First, WJEC Level 1/2, AQA Technical Award and most VRQ rows into a single
"Level 1/Level 2 vocational qualification" bucket, and re-cut several subject
discount groups at the same time. Rows where that shows are marked
<span class="flag">TAXONOMY BREAK</span> and only their last two years are
compared. Every vocational row also rolls all Level 1/2 awarding routes together,
because a school switching from a BTEC to a Cambridge National is still teaching
the subject.</li>
<li><strong>Entries are not pupils on roll.</strong> They are exam entries counted
at the end of KS4, so a school entering the same pupil for two routes appears
twice in the family total.</li>
</ul>

<div class="cards">
 <div class="card"><div class="num">{len(subjects)}</div>
  <div class="lbl">Subjects</div><div class="fine">27 from Table 3, 7 extended</div></div>
 <div class="card"><div class="num">{uniq:,}</div>
  <div class="lbl">Distinct schools</div><div class="fine">across all subjects</div></div>
 <div class="card"><div class="num">{tot_rows:,}</div>
  <div class="lbl">School&ndash;subject rows</div><div class="fine">every year, not a top ten</div></div>
 <div class="card"><div class="num">{tot_new:,}</div>
  <div class="lbl">NEW</div><div class="fine">first entries {YEARS[-2]} or {LATEST}</div></div>
 <div class="card"><div class="num">{tot_est:,}</div>
  <div class="lbl">ESTABLISHED</div><div class="fine">every year since 2022/23</div></div>
 <div class="card"><div class="num">{tot_lapsed:,}</div>
  <div class="lbl">Lapsed or one-off</div><div class="fine">nothing in {LATEST}</div></div>
</div>

<div class="toolbar">
 <input id="q" type="search" placeholder="Find a school by name or URN, across every subject">
 <button id="expand" type="button">Expand all</button>
 <button id="collapse" type="button">Collapse all</button>
</div>
<div id="hits"></div>

<h2>Subject by subject</h2>
<p class="hint">Ordered by {LATEST} entries. Each panel opens to every school that
entered the subject in any comparable year, NEW first, then ESTABLISHED by latest
entries. "n/c" marks a year the row cannot be compared across.</p>
{panels}

<h2>Where the data comes from</h2>
<p class="hint">Two DfE sources, both read-only, recorded in full in
<span class="mono">scripts/_planning/dfe_datasets.json</span>.</p>
<div class="panel">
<p class="note"><strong>Explore Education Statistics.</strong> The publication
&ldquo;Key stage 4 performance&rdquo; ({e(ees["publication_id"])}) carries a
school-level subject data set for {LATEST} only, as API data set
<span class="mono">{e(api_set.get("id", "—"))}</span>
&mdash; the one this repo already queries for
<span class="mono">dfe_subject_entries_2025.json</span>. The 2023/24 release
carries the same table as a plain CSV data-set file with no API data set. The
2022/23, 2021/22, 2020/21 and 2019/20 releases carry no school-level subject file
at all, so the EES API on its own cannot give a multi-year series.</p>
<p class="note"><strong>School performance tables download service.</strong>
Publishes the same underlying table &mdash; KS4 underlying data, entries and
grades &mdash; for 2021/22 to {LATEST} under one schema, as
<span class="mono">england_ks4underlying_entriesandgrades_2.xlsx</span>. That is
the series used here. As a check, every one of the {len(subjects)} subject totals
this page computes for {LATEST} from the performance tables matches the figure
the EES API returns, to the entry.</p>
</div>

<footer>Sources: DfE Explore Education Statistics API
(<a href="https://explore-education-statistics.service.gov.uk/find-statistics/key-stage-4-performance">key stage 4 performance</a>)
and the DfE school performance tables download service
(<a href="https://www.compare-school-performance.service.gov.uk/download-data">download data</a>).
Row filter: grade &ldquo;Total number entered&rdquo;. Built by
<span class="mono">scripts/_planning/fetch_dfe_history.py</span> and
<span class="mono">scripts/_planning/render_niche_history.py</span>.</footer>
</div>
<script type="application/json" id="d">{json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>{JS}</script>
</body></html>
"""
    out = os.path.join(HERE, "niche_schools_history.html")
    open(out, "w", encoding="utf-8").write(page)
    print(f"wrote {out} ({len(page):,} bytes)")
    print(f"  {len(subjects)} subjects, {tot_rows:,} school rows, "
          f"{uniq:,} distinct schools")
    print(f"  NEW {tot_new:,} · ESTABLISHED {tot_est:,} · "
          f"lapsed/one-off {tot_lapsed:,}")


if __name__ == "__main__":
    main()
