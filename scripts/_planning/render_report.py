"""Render scripts/_planning/remaining_builds_2025.html from remaining_builds.json.

Self-contained page: no external stylesheet, font or script.
"""

import html as H
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "remaining_builds.json"), encoding="utf-8"))
T = D["totals"]
CM = D["cost_model"]
SRC = D["dfe_source"]
CC = D["crosscheck"]
CQ = D["crosscheck_summary"]
PREV = {}
_prev = os.path.join(HERE, "_remaining_builds_prev_2026shares.json")
if os.path.exists(_prev):
    _p = json.load(open(_prev, encoding="utf-8"))
    PREV = {r["spec_code"]: (i, r["est_students"])
            for i, r in enumerate(_p["table1_remaining"], 1)}

TAG_LABEL = {"build": "BUILD", "port": "PORT", "alias": "ALIAS", "skip": "SKIP",
             "general": "note"}
TIER_LABEL = {"S": "Top tier (400k+)", "A": "High uptake (100–400k)",
              "B": "Medium (30–100k)", "C": "Lower (10–30k)", "N": "Niche (<10k)"}


def e(x):
    return H.escape(str(x)) if x is not None else ""


def n(x):
    return "—" if x is None else f"{x:,}"


def pct(x):
    return "—" if x is None else f"{100 * x:.1f}%"


def trend(r):
    """2026 board-level share and the change in percentage points. Direction of
    travel only - no calculation on this page uses the 2026 series."""
    a, b = r.get("board_share_2025_boardlevel"), r.get("board_share_2026_boardlevel")
    if a is None or b is None:
        return '<span class="note">&mdash;</span>'
    d = r.get("board_delta_pp")
    if d is None:
        d = 100 * (b - a)
    cls = "up" if d > 0.25 else ("down" if d < -0.25 else "")
    arrow = "&#9650;" if d > 0.25 else ("&#9660;" if d < -0.25 else "&ndash;")
    return (f'{100*a:.1f}% &rarr; {100*b:.1f}%<br>'
            f'<span class="{cls}">{arrow} {d:+.1f} pp</span>'
            f'<br><span class="note">whole board, both series</span>')


def tag(t):
    return f'<span class="tag tag-{e(t)}">{e(TAG_LABEL.get(t, t))}</span>'


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
.bar{display:flex;height:26px;border-radius:8px;overflow:hidden;margin:.6rem 0 .5rem}
.bar span{display:block}
.b-built{background:#3f6f4a}.b-rem{background:#c9a227}.b-park{background:#ddd7cd}
.key{display:flex;gap:1.25rem;flex-wrap:wrap;font-size:.78rem;color:#5c554d}
.key i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:.35rem;vertical-align:-1px}
.tw{overflow-x:auto;background:#fff;border-radius:16px;box-shadow:0 1px 4px rgba(0,0,0,.05)}
table{width:100%;border-collapse:collapse;font-size:.82rem}
table.t1{min-width:1240px}
table.t1 td:nth-child(4),table.t1 th:nth-child(4){min-width:150px}
table.t1 td:nth-child(7),table.t1 th:nth-child(7){min-width:215px}
table.t1 td:nth-child(9),table.t1 th:nth-child(9){min-width:120px}
table.t1 td:nth-child(11),table.t1 th:nth-child(11){min-width:330px}
table.t2{min-width:1000px}
table.t2 td:nth-child(6),table.t2 th:nth-child(6){min-width:420px}
th{text-align:left;background:#f6f3ee;padding:.6rem .8rem;border-bottom:1px solid #ece7de;
 font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:#7a736a;font-weight:600;
 white-space:nowrap;vertical-align:bottom}
td{padding:.6rem .8rem;border-bottom:1px solid #f4f1ea;vertical-align:top}
tr:last-child td{border-bottom:none}
tbody tr:hover td{background:#fcfbf8}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.rank{color:#9a938a;font-variant-numeric:tabular-nums}
.mono{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;font-size:.76rem}
.strong{font-weight:600}
.note{color:#5c554d;font-size:.78rem;line-height:1.45;max-width:52ch}
.tag{display:inline-block;font-size:.62rem;font-weight:700;letter-spacing:.05em;
 padding:2px 6px;border-radius:4px}
.tag-build{background:#dcecdf;color:#28502f}
.tag-port{background:#e2e6f2;color:#33406b}
.tag-alias{background:#f0e6f4;color:#5b3568}
.tag-skip{background:#eeeae4;color:#6d655b}
.tag-general{background:#f3efe8;color:#6d655b}
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
summary:before{content:"▸ ";color:#9a938a}
details[open] summary:before{content:"▾ "}
.schools{margin:.5rem 0 0;padding:0;list-style:none;
 columns:2;column-gap:2rem;font-size:.78rem}
.schools li{break-inside:avoid;padding:.16rem 0;color:#5c554d}
.schools .n{font-variant-numeric:tabular-nums;color:#2d2a26;font-weight:600}
.schools .urn{color:#9a938a;font-family:ui-monospace,Consolas,monospace;font-size:.7rem}
ul.plain{font-size:.86rem;color:#5c554d;line-height:1.6;max-width:88ch}
a{color:#33406b}
footer{margin-top:3.5rem;font-size:.78rem;color:#9a938a}
@media(max-width:720px){.schools{columns:1}h1{font-size:1.5rem}}
"""


def bar(built, rem, park):
    tot = built + rem + park or 1
    return (f'<div class="bar">'
            f'<span class="b-built" style="width:{100*built/tot:.2f}%"></span>'
            f'<span class="b-rem" style="width:{100*rem/tot:.2f}%"></span>'
            f'<span class="b-park" style="width:{100*park/tot:.2f}%"></span></div>')


# ---------------------------------------------------------------- table 1
def table1():
    head = ("<tr><th>#</th><th>Spec</th><th>Board</th><th>Subject</th>"
            "<th class='num'>England entries<br>2024/25</th>"
            "<th class='num'>Schools<br>entering</th>"
            "<th>Share of the subject, 2025<br>(route-adjusted; source)</th>"
            "<th class='num'>Board share<br>2025 &rarr; 2026</th>"
            "<th class='num'>Est.<br>students</th>"
            "<th class='num'>Likely<br>lessons</th>"
            "<th class='num'>Est.<br>cost</th>"
            "<th>Note from BUILD_NOTES</th></tr>")
    body = []
    for i, r in enumerate(D["table1_remaining"], 1):
        if r["board_share_known"]:
            # Keep Table 1 compact: the full entry breakdown behind each share
            # is in the "Board shares on file" table further down.
            src = re.sub(r"\s*\(.*", "", r["board_share_source"] or "")
            share = (f'{pct(r["board_share"])} '
                     f'<span class="ok">PUBLISHED</span><br>'
                     f'<span class="note">{e(src)}'
                     + (f'<br>Route weight {r["route_weight"]:.1%} of that board '
                        f'&mdash; {e(r["route_weight_source"])}'
                        if r.get("route_weight") else '') + '</span>')
        elif r["est_students"] is None:
            share = '<span class="flag">NO DfE MATCH</span>'
        elif r["board"] == "WJEC":
            share = '<span class="flag">WALES ONLY</span>'
        else:
            share = (f'{pct(r["board_share"])} '
                     f'<span class="flag">SHARE UNKNOWN</span><br>'
                     f'<span class="note">{e(r["est_basis"])}</span>')
        body.append(
            f'<tr><td class="rank">{i}</td>'
            f'<td class="mono">{e(r["spec_code"])}<br>{tag(r["tag"])}</td>'
            f'<td>{e(r["board"])}</td>'
            f'<td class="strong">{e(r["subject"])}</td>'
            f'<td class="num">{n(r["entries"])}</td>'
            f'<td class="num">{n(r["schools_entering"])}</td>'
            f'<td>{share}</td>'
            f'<td class="num">{trend(r)}</td>'
            f'<td class="num strong">{n(r["est_students"])}</td>'
            f'<td class="num">{r["likely_lessons"]}<br>'
            f'<span class="note">{e(r["lesson_reference"][:44])}</span></td>'
            f'<td class="num">&pound;{r["est_cost_gbp"]:,.2f}</td>'
            f'<td class="note">{e(r["note"] or r["general_note"] or "—")}</td></tr>')
    return ('<div class="tw"><table class="t1"><thead>' + head +
            '</thead><tbody>' + "".join(body) + '</tbody></table></div>')


# ---------------------------------------------------------------- table 2
def table2():
    head = ("<tr><th>Spec</th><th>Tag</th><th>Board</th><th>Subject</th>"
            "<th class='num'>Subject entries<br>England 2024/25</th>"
            "<th>Why it is not ranked as a build</th></tr>")
    body = []
    for r in D["table2_skipped"]:
        body.append(
            f'<tr><td class="mono">{e(r["spec_code"])}</td>'
            f'<td>{tag(r["tag"])}</td>'
            f'<td>{e(r["board"])}</td>'
            f'<td class="strong">{e(r["subject"])}</td>'
            f'<td class="num">{n(r["entries"])}</td>'
            f'<td class="note">{e(r["note"] or r["general_note"] or "—")}</td></tr>')
    t = ('<div class="tw"><table class="t2"><thead>' + head +
         '</thead><tbody>' + "".join(body) + '</tbody></table></div>')

    ports = [r for r in D["table1_remaining"] if r["tag"] == "port"]
    ph = ("<tr><th>Spec</th><th>Board</th><th>Subject</th>"
          "<th class='num'>Est. students</th><th class='num'>Lessons</th>"
          "<th class='num'>Est. cost</th><th>Reuse note</th></tr>")
    pb = []
    for r in ports:
        pb.append(f'<tr><td class="mono">{e(r["spec_code"])}</td>'
                  f'<td>{e(r["board"])}</td><td class="strong">{e(r["subject"])}</td>'
                  f'<td class="num">{n(r["est_students"])}</td>'
                  f'<td class="num">{r["likely_lessons"]}</td>'
                  f'<td class="num">&pound;{r["est_cost_gbp"]:,.2f}</td>'
                  f'<td class="note">{e((r["note"] or "")[:260])}</td></tr>')
    p = (f'<h3>PORT-tagged specs — ranked in Table 1, priced at '
         f'{CM["port_factor"]:.0%} of a fresh build</h3>'
         f'<p class="hint">A PORT is a new Supabase row with heavy reuse from an '
         f'existing build. It still reaches real students, so it belongs in the '
         f'ranking; it is listed again here so the reuse decision is visible in '
         f'one place.</p>'
         f'<div class="tw"><table><thead>{ph}</thead><tbody>{"".join(pb)}</tbody></table></div>')
    return t + p


# ---------------------------------------------------------------- table 3
def table3():
    out = []
    for r in D["table3_niche"]:
        schools = "".join(
            f'<li><span class="n">{s["entries"]}</span> &nbsp;{e(s["name"])} '
            f'<span class="urn">URN {e(s["urn"])}</span></li>'
            for s in r["top_schools"])
        out.append(
            f'<details><summary>{e(r["subject_discount_group"])} '
            f'&nbsp;·&nbsp; {r["entries"]:,} entries &nbsp;·&nbsp; '
            f'{r["schools_entering"]} schools &nbsp;·&nbsp; '
            f'<span class="note">{e(r["qualification"])}</span></summary>'
            f'<ul class="schools">{schools}</ul></details>')
    return "".join(out)


# ---------------------------------------------------------------- tier section
def tiers():
    head = ("<tr><th>Family</th><th>Tier letter on the page</th>"
            "<th>Letter the data gives</th><th class='num'>England entries</th>"
            "<th class='num'>Schools</th><th>Qualification counted</th>"
            "<th>Reading</th></tr>")
    body = []
    order = "SABCN"
    for t in D["tier_conflicts"]:
        moved = "up" if order.index(t["actual"]) < order.index(t["stated"]) else "down"
        word = ("bigger than the letter says" if moved == "up"
                else "smaller than the letter says")
        origin = ("explicit in ENTRY_TIER" if t["in_entry_tier_map"]
                  else "fell through to the C default")
        body.append(
            f'<tr><td class="strong">{e(t["family"])}</td>'
            f'<td>{e(t["stated"])} — {e(TIER_LABEL[t["stated"]])}<br>'
            f'<span class="note">{origin}</span></td>'
            f'<td class="{moved}">{e(t["actual"])} — {e(TIER_LABEL[t["actual"]])}</td>'
            f'<td class="num">{t["entries"]:,}</td>'
            f'<td class="num">{t["schools"]:,}</td>'
            f'<td class="note">{e(t["qualification"])}</td>'
            f'<td class="note">{word}</td></tr>')
    return f'<div class="tw"><table><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


# ---------------------------------------------------------------- coverage
def coverage_table():
    head = ("<tr><th>Subject family</th><th class='num'>England entries</th>"
            "<th class='num'>Schools</th><th class='num'>% covered</th>"
            "<th class='num'>Entries covered</th><th class='num'>Entries still open</th>"
            "<th>Boards built</th><th>Boards remaining</th><th>Boards parked</th>"
            "<th>Share basis</th></tr>")
    body = []
    for c in D["coverage_by_family"]:
        basis = ('<span class="ok">PUBLISHED</span>' if c["share_basis"] == "published"
                 else '<span class="flag">EQUAL SPLIT</span>')
        body.append(
            f'<tr><td class="strong">{e(c["family"])}</td>'
            f'<td class="num">{c["entries"]:,}</td>'
            f'<td class="num">{c["schools"]:,}</td>'
            f'<td class="num">{c["pct_built"]:.1f}%</td>'
            f'<td class="num">{c["entries_built"]:,}</td>'
            f'<td class="num">{c["entries_remaining"]:,}</td>'
            f'<td class="note">{e(", ".join(c["boards_built"]) or "—")}</td>'
            f'<td class="note">{e(", ".join(c["boards_remaining"]) or "—")}</td>'
            f'<td class="note">{e(", ".join(c["boards_parked"]) or "—")}</td>'
            f'<td>{basis}</td></tr>')
    return f'<div class="tw"><table><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def board_share_sources():
    rows = []
    for fam, sh in sorted(D["board_share_db"].get("shares", {}).items()):
        b25 = sh.get("boards", {})
        b26 = sh.get("boards_2026", {})
        d = sh.get("delta_pp", {})
        cells = []
        for b in sorted(b25, key=lambda k: -b25.get(k, 0)):
            if not b25.get(b):
                continue
            dd = d.get(b)
            move = (f' <span class="{"up" if dd > 0.25 else ("down" if dd < -0.25 else "")}">'
                    f'{dd:+.1f}</span>' if dd is not None else '')
            cells.append(f'{b} <strong>{100*b25[b]:.1f}%</strong>'
                         + (f' &rarr; {100*b26[b]:.1f}%{move}' if b in b26 else ''))
        ent = sh.get("board_entries_2025", {})
        ent_s = ", ".join(f"{b} {v:,}" for b, v in
                          sorted(ent.items(), key=lambda kv: -kv[1]) if v)
        rows.append(f'<tr><td class="strong">{e(fam)}</td>'
                    f'<td class="note">{" &nbsp;·&nbsp; ".join(cells)}</td>'
                    f'<td class="num">{n(sh.get("board_total_2025"))}</td>'
                    f'<td class="note">{e(ent_s) or "&mdash;"}</td>'
                    f'<td class="note">{e(sh["source_label"][:150])}<br>'
                    f'<span class="mono">{e(sh.get("source_url", ""))}</span></td></tr>')
    if not rows:
        return "<p class='hint'>No published board shares are on file.</p>"
    return ('<div class="tw"><table class="t2"><thead><tr><th>Family</th>'
            '<th>Share 2025 &rarr; 2026 (pp change)</th>'
            '<th class="num">Board sum<br>2025</th><th>2025 entries by board</th>'
            f'<th>Source</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def crosscheck_table():
    head = ("<tr><th>Family</th><th class='num'>DfE England<br>2024/25</th>"
            "<th class='num'>Board sum<br>June 2025</th>"
            "<th class='num'>Residual</th><th class='num'>Residual %</th>"
            "<th class='num'>Ratio<br>2025</th><th class='num'>Ratio<br>2026</th>"
            "<th>Reading</th></tr>")
    resit = set(CQ.get("resit_heavy", []))
    body = []
    for c in CC:
        dev25 = abs(c["ratio_2025"] - 1)
        dev26 = abs((c["ratio_2026"] or 1) - 1)
        if c["family"] in resit:
            why = ("post-16 resits: the boards count every entry, the DfE counts "
                   "only pupils at the end of KS4")
        elif abs(c["residual"]) < 400:
            why = "small subject; the residual is a few hundred candidates"
        elif dev25 <= 0.05:
            why = "matches"
        else:
            why = "board totals include non-England and post-16 entries"
        better = ('<span class="ok">2025 CLOSER</span>' if dev25 < dev26 - 0.002
                  else ('<span class="flag">2026 CLOSER</span>'
                        if dev26 < dev25 - 0.002 else ''))
        cls = "" if dev25 <= 0.05 else ("up" if c["residual"] > 0 else "down")
        body.append(
            f'<tr><td class="strong">{e(c["family"])}</td>'
            f'<td class="num">{c["dfe_entries"]:,}</td>'
            f'<td class="num">{c["board_sum_2025"]:,}</td>'
            f'<td class="num">{c["residual"]:+,}</td>'
            f'<td class="num {cls}">{c["residual_pct"]:+.1f}%</td>'
            f'<td class="num">{c["ratio_2025"]:.3f}</td>'
            f'<td class="num">{(c["ratio_2026"] or 0):.3f} {better}</td>'
            f'<td class="note">{why}</td></tr>')
    return ('<div class="tw"><table class="t2"><thead>' + head +
            '</thead><tbody>' + "".join(body) + '</tbody></table></div>')


def realignment_table():
    """What moved when the shares were realigned onto the 2025 cohort and the
    even route splits were replaced with measured ones."""
    if not PREV:
        return ""
    rows = []
    for i, r in enumerate(D["table1_remaining"], 1):
        prev = PREV.get(r["spec_code"])
        if not prev:
            continue
        move = prev[0] - i
        d = r["est_students"] - prev[1]
        if abs(move) < 1 and abs(d) < 500:
            continue
        cls = "up" if move > 0 else ("down" if move < 0 else "")
        rw = (f'route weight now {r["route_weight"]:.1%}, measured'
              if r.get("route_weight") else 'board share moved between series')
        rows.append(f'<tr><td class="mono">{e(r["spec_code"])}</td>'
                    f'<td class="strong">{e(r["subject"])}</td>'
                    f'<td>{e(r["board"])}</td>'
                    f'<td class="num">{prev[0]}</td><td class="num">{i}</td>'
                    f'<td class="num {cls}">{move:+d}</td>'
                    f'<td class="num">{prev[1]:,}</td>'
                    f'<td class="num strong">{r["est_students"]:,}</td>'
                    f'<td class="num {cls}">{d:+,}</td>'
                    f'<td class="note">{rw}</td></tr>')
    if not rows:
        return "<p class='hint'>No row changed rank.</p>"
    return ('<div class="tw"><table><thead><tr><th>Spec</th><th>Subject</th>'
            '<th>Board</th><th class="num">Rank before</th><th class="num">Rank now</th>'
            '<th class="num">Move</th><th class="num">Est. before</th>'
            '<th class="num">Est. now</th><th class="num">Change</th>'
            f'<th>Why</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def index_gaps_table():
    gaps = D.get("index_gaps", [])
    if not gaps:
        return ""
    body = []
    for g in gaps:
        body.append(f'<tr><td class="mono">{e(g["spec_code"])}</td>'
                    f'<td>{e(g["board"])}</td>'
                    f'<td class="strong">{e(g["subject"])}</td>'
                    f'<td class="num">{n(g.get("entries_2025"))}</td>'
                    f'<td class="num">{n(g.get("entries_2026"))}</td>'
                    f'<td class="note">{e(g["note"])}</td></tr>')
    return ('<div class="tw"><table class="t2"><thead><tr><th>Spec</th><th>Board</th>'
            '<th>Subject</th><th class="num">Entries<br>June 2025</th>'
            '<th class="num">Entries<br>June 2026</th>'
            f'<th>Why it matters</th></tr></thead><tbody>{"".join(body)}</tbody>'
            '</table></div>')


def main():
    built = T["england_entries_reached_built"]
    rem = T["england_entries_reached_remaining"]
    park = T["england_entries_parked"]
    scope = T["england_entries_in_scope"]

    page = f"""<!doctype html><html lang="en-GB"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remaining GCSE Builds</title>
<style>{CSS}</style>
</head><body>
<div class="wrap">
<h1>Remaining GCSE builds — rescoped on hard numbers</h1>
<p class="sub">Generated {e(D["generated"])} · branch <span class="mono">platform</span> ·
entry data: DfE Explore Education Statistics, {e(SRC["publication"])},
dataset &ldquo;{e(SRC["dataset"])}&rdquo; (<span class="mono">{e(SRC["dataset_id"])}</span>),
England, {e(SRC["time_period"])} &middot; board shares: the four boards' own
<strong>June 2025</strong> results statistics &mdash; the same exam series</p>
<p class="lede">Every unbuilt specification in <span class="mono">specs/index.json</span>,
scored against the real number of pupils who sat that subject in England last year.
The build/skip/alias/port decisions are the ones already recorded in
<span class="mono">admin/build-status.html</span>; this page adds the size of the prize
and the price of the work. Nothing here was written to the database.</p>

<div class="cards">
 <div class="card"><div class="num">{T["specs_total"]}</div><div class="lbl">Specs in the index</div>
   <div class="fine">{T["specs_excluded_portfolio"]} portfolio specs excluded</div></div>
 <div class="card"><div class="num">{T["specs_in_scope"]}</div><div class="lbl">In scope</div>
   <div class="fine">written-exam specs</div></div>
 <div class="card"><div class="num">{T["specs_built"]}</div><div class="lbl">Built</div>
   <div class="fine">{100*T["specs_built"]/T["specs_in_scope"]:.0f}% of in-scope specs</div></div>
 <div class="card"><div class="num">{T["buildable_remaining"]}</div><div class="lbl">Remaining, buildable</div>
   <div class="fine">ranked in Table 1</div></div>
 <div class="card"><div class="num">{T["skipped_or_aliased"]}</div><div class="lbl">Skipped or aliased</div>
   <div class="fine">not ranked — Table 2</div></div>
 <div class="card"><div class="num">&pound;{T["total_cost_remaining_gbp"]:,.0f}</div>
   <div class="lbl">To build everything left</div>
   <div class="fine">{T["total_lessons_remaining"]:,} lessons</div></div>
</div>

<h2>England GCSE entries reached</h2>
<p class="hint">Counted per subject family so no pupil is counted twice. For each
subject, the England entry total is split across the boards that offer it —
by published share where one exists, otherwise evenly across the
England-accessible boards, and then evenly across a board's routes unless the
build note records the split. Wales-only WJEC specs are excluded from the
denominator: they are not available to centres in England.</p>
<div class="panel">
{bar(built, rem, park)}
<div class="key">
 <span><i class="b-built"></i>Covered by a built spec — <strong>{built:,}</strong> entries
 ({100*built/scope:.1f}%)</span>
 <span><i class="b-rem"></i>Still open, buildable — <strong>{rem:,}</strong>
 ({100*rem/scope:.1f}%)</span>
 <span><i class="b-park"></i>Parked (skip/alias) — <strong>{park:,}</strong>
 ({100*park/scope:.1f}%)</span>
</div>
<p class="hint" style="margin-bottom:0">Total England entries across the subjects the
catalogue addresses: <strong>{scope:,}</strong>.</p>
</div>

<h2>Table 1 — remaining buildable specs, ranked by students reached</h2>
<p class="hint">Ranked on estimated students: England entries for the subject
&times; that spec's share of the subject. Where a board runs two routes, its
share is divided by the measured route weight, so the route-adjusted figure in
column seven can be smaller than the whole-board share in column eight. A green <span class="ok">PUBLISHED</span>
mark means the board share comes from a real source; an amber
<span class="flag">SHARE UNKNOWN</span> mark means no published board split was
found and the row uses an equal split, which is a placeholder, not a measurement.
Cost model: &pound;{CM["api_per_lesson_gbp"]:.3f}/lesson generation +
&pound;{CM["narration_per_lesson_gbp"]:.2f}/lesson narration +
&pound;{CM["factcheck_per_subject_gbp"]:.0f} fact-check per spec; PORT rows at
{CM["port_factor"]:.0%}.</p>
{table1()}

<h2>What the cohort realignment changed</h2>
<p class="hint">The first cut of this page joined June 2026 board shares to
2024/25 (summer 2025) DfE entries &mdash; two different cohorts &mdash; and split a
board's routes evenly for want of a figure. Both are now fixed: shares come from
the June 2025 releases, and every route split is measured. These rows moved.</p>
{realignment_table()}

<h2>Table 2 — skipped, aliased and port-tagged items</h2>
<p class="hint">SKIP and ALIAS rows are deliberately not ranked as builds. An
ALIAS costs nothing: one Supabase row serves both boards through slugMap. Most
SKIP rows are Wales-regulated WJEC specs that England centres cannot enter.</p>
{table2()}

<h2>Table 3 — niche subjects (≤ {D["niche_threshold"] if "niche_threshold" in D else 3000:,} entries): the schools that enter them</h2>
<p class="hint">The sales target list. These subjects are small enough that the
schools entering them are individually addressable, and small enough that no big
revision platform serves them. Each row opens to the ten largest centres by entries.</p>
{table3()}

<h2>Cross-check: DfE subject total against the June 2025 board sum</h2>
<p class="hint">Two independent counts of the same exam series. They cannot match
exactly &mdash; the DfE counts pupils at the end of KS4 in England, the boards count
every entry they took &mdash; but a large residual would mean a mis-mapped subject.
Across {CQ["quality"]["all_2025"]["families"]} families the median absolute
deviation is <strong>{CQ["quality"]["all_2025"]["median_abs_dev"]:.1%}</strong> on
2025 shares against {CQ["quality"]["all_2026"]["median_abs_dev"]:.1%} on the 2026
shares this page used before, and
{CQ["quality"]["all_2025"]["within_5pct"]} families sit within 5% against
{CQ["quality"]["all_2026"]["within_5pct"]}. Weighting by entries and setting aside
the three resit-heavy subjects, the deviation is
<strong>{CQ["quality"]["ex_resit_2025"]["entries_weighted_abs_dev"]:.2%}</strong>
against {CQ["quality"]["ex_resit_2026"]["entries_weighted_abs_dev"]:.2%}. The
realignment improves the fit on every measure.</p>
{crosscheck_table()}

<h2>Specifications missing from specs/index.json</h2>
<p class="hint">Found by the cross-check. These specifications appear in a board's
own results release but not in our spec index, so the To-Build page cannot see
them. They are counted in the share denominators here &mdash; leaving them out
inflated every other board &mdash; but they are not ranked in Table 1, because
Table 1 reproduces the page's logic. Both are real, unbuilt content gaps.</p>
{index_gaps_table()}

<h2>What changed against the tier letters</h2>
<p class="hint">The ENTRY_TIER map in <span class="mono">admin/build-status.html</span>
carries rough JCQ-2024 bands: S = 400k+, A = 100–400k, B = 30–100k, C = 10–30k,
N = &lt;10k. {len(D["tier_conflicts"])} families land in a different band once the
2024/25 England figures are applied. Families with no letter of their own fall
through to a C default, which is why so many vocational families read as C.</p>
{tiers()}

<h2>Coverage, family by family</h2>
{coverage_table()}

<h2>Board shares on file</h2>
{board_share_sources()}

<h2>Data caveats</h2>
<ul class="plain">
<li><strong>Cohort alignment.</strong> The entry totals are DfE 2024/25, which
is the summer 2025 exam series. The board shares are taken from the four boards'
own <strong>June 2025</strong> results statistics, so shares and totals describe
one cohort. June 2026 appears only as a direction-of-travel column and is never
used in a calculation. This matters: between the two series AQA French fell from
76.4% to 56.8% and AQA Spanish from 77.8% to 56.7% as the reformed MFL
specifications came in, so 2026 shares would have badly mis-stated the 2025
cohort. Every family on this page now carries a 2025 share except NCFE Music
Technology, which no GCSE results release covers, and the Pearson BTEC Tech
Award, whose 100% share is true by construction rather than derived.</li>
<li><strong>England only.</strong> The DfE dataset covers
{e(SRC["coverage"])}. Wales, Scotland and Northern Ireland are absent, so every
WJEC figure on this page is zero by construction rather than by measurement.</li>
<li><strong>DfE counts subjects, not boards.</strong> The dataset has no awarding
organisation column, so every per-board number here is the subject total multiplied
by a share. The shares themselves are <em>derived, not published</em>: no board or
regulator publishes a share, so each board's own published entry count is divided by
the sum across the England-accessible boards. Ofqual's entries release was checked
and carries England subject totals only, with no awarding-organisation split.</li>
<li><strong>Route splits are now measured, not assumed.</strong> Where a board runs
two routes, the split comes from that board's own June 2025 per-specification
entries. Twenty-four route weights are on file. The corrections are large: OCR
History B is 86.9% of OCR History, not half; OCR Geography B is 77.3%; Eduqas
Geography B is 62.9%; Pearson Geography B is 61.7%. AQA Combined Science Synergy
turns out to be 1.4% of AQA, not the &ldquo;under 10%&rdquo; the build note
estimates, and AQA Religious Studies Spec B is 9.4%.</li>
<li><strong>Discount groups are legacy labels.</strong> DfE files GCSE Citizenship
Studies under &ldquo;Community Development&rdquo;, GCSE PE under &ldquo;Sports
Studies&rdquo;, GCSE Drama under &ldquo;Speech &amp; Drama&rdquo; and GCSE Food
Preparation and Nutrition under &ldquo;Food Technology&rdquo;. Those mappings are
declared in <span class="mono">DFE_MAP</span> in
<span class="mono">scripts/_planning/remaining_builds.py</span>.</li>
<li><strong>Cambridge Nationals and Level 1/2 awards are in the data</strong> —
the dataset does carry the qualification types
&ldquo;OCR Level 1 / 2 Cambridge National Certificate&rdquo;, &ldquo;Level 1 / Level 2
vocational qualification&rdquo;, &ldquo;BTEC Technical Award L1/2&rdquo; and
&ldquo;VRQ Level 2&rdquo;. But those buckets are also legacy discount groups, so a
single bucket can hold more than one qualification title, and the boards inside a
bucket cannot be separated. Treat vocational entry counts as the size of the
territory, not of a single award.</li>
<li><strong>The subject mapping was cross-validated.</strong> Every DfE discount
group used here was checked against the four boards' own June 2026 entry totals.
On the aligned 2025 figures History reads 289,332 against a board sum of 290,336
(ratio 1.003), Geography 287,748 against 289,914 (1.008), Drama 48,301 against
48,923 (1.013), English Literature 605,318 against 610,807 (1.009). The full
residual table is above.</li>
<li><strong>The build note on OCR Geography B is confirmed and then some.</strong>
It says OCR B has higher uptake than OCR A. OCR's own June 2025 figures give B
19,293 entries against A 5,674 &mdash; B is 77.3% of OCR Geography, and the same
pattern is far stronger in History, where OCR B (SHP) takes 17,477 against OCR A's
2,635. We built the smaller route on both.</li>
<li><strong>Independent schools are included</strong> in the school list, which
matters most for Latin, Classical Greek, Ancient History and Classical Civilisation
— the niche subjects whose top-ten school lists are dominated by them.</li>
<li><strong>Short courses are excluded.</strong> The GCSE short-course qualification
type is not in the query, so AQA 8061 and OCR J125 add no entries of their own.</li>
<li><strong>Costs are settled spend, not meter readings.</strong> Per-lesson figures
come from two builds reconciled against the Anthropic Console: Psychology AQA+OCR
(69 lessons, $32.99) and the OCR poetry rebuild of 6 Sep 2026 (45 lessons,
&pound;13.38 plus ~&pound;5 narration). The driver's internal cost meter reads
1.4–1.8&times; high and is not used here. Costs cover generation, narration and the
fact-check pass only — not podcasts, explainer videos, hero images or Tom's review
time.</li>
<li><strong>Lesson counts are estimates.</strong> Where a build note states its own
size that number is used; otherwise the same board's existing route, then the median
of built sibling boards, then a tier default.</li>
</ul>

<footer>Sources: DfE Explore Education Statistics API,
{e(SRC["url"])} · dataset {e(SRC["dataset_id"])} ·
grade filter &ldquo;{e(SRC["grade_filter"])}&rdquo;, indicator
&ldquo;{e(SRC["indicator"])}&rdquo;. Build decisions from
admin/build-status.html. Built-spec state read from Supabase, read-only.</footer>
</div>
</body></html>
"""
    out = os.path.join(HERE, "remaining_builds_2025.html")
    open(out, "w", encoding="utf-8").write(page)
    print(f"wrote {out} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
