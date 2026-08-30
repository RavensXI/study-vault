# -*- coding: utf-8 -*-
"""Render the retro fact-check tracker page from _state.json.

    python scripts/_retrofc/build_tracker.py [out.html]

The state file is the source of truth. Update it (statuses, findings,
batches), re-run this, republish the artifact to the SAME url.
Status vocabulary: unchecked | in-progress | checked | partial |
gate-built | exempt-practice.
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
state = json.load(io.open(os.path.join(HERE, '_state.json'), encoding='utf-8'))

LABEL = {'unchecked': 'Unchecked', 'in-progress': 'In progress',
         'checked': 'Checked \u2713', 'partial': 'Partially checked',
         'gate-built': 'Gate-built \u2713', 'exempt-practice': 'Practice-verified \u2713'}
CLS = {'unchecked': 'u', 'in-progress': 'p', 'checked': 'g',
       'partial': 'p', 'gate-built': 'g', 'exempt-practice': 'g'}
PRIO_NAME = {1: 'Priority 1 \u00b7 English Literature', 2: 'Priority 2 \u00b7 Sciences',
             3: 'Priority 3 \u00b7 History', 4: 'Priority 4 \u00b7 Geography',
             5: 'Priority 5 \u00b7 RS, Geology, Astronomy', 6: 'Priority 6 \u00b7 Business, CS, PE, Sociology, D&T',
             7: 'Priority 7 \u00b7 Niche and vocational', 8: 'Priority 8 \u00b7 Sunsetting',
             9: 'Already gated at build'}

subs = state['subjects']
done_l = sum(s['lessons'] for s in subs if s['status'] in ('checked', 'gate-built'))
part_l = sum(s['lessons'] for s in subs if s['status'] == 'partial')
todo_l = sum(s['lessons'] for s in subs if s['status'] in ('unchecked', 'in-progress'))
tot_l = done_l + part_l + todo_l
findings = sum(b.get('findings') or 0 for b in state['batches'])
fixed = sum(b.get('fixed') or 0 for b in state['batches'])
pct = round(100.0 * done_l / tot_l) if tot_l else 0

rows, cur = [], None
for s in subs:
    if s['priority'] != cur:
        cur = s['priority']
        rows.append('<tr class="grp"><td colspan="5">%s</td></tr>' % PRIO_NAME.get(cur, 'Priority %d' % cur))
    f = '' if s['findings'] is None else str(s['findings'])
    fx = '' if s['fixed'] is None else str(s['fixed'])
    extra = (' \u00b7 ' + s['checked_on']) if s['checked_on'] else ''
    note = ('<div class="note">%s</div>' % s['note']) if s['note'] else ''
    rows.append('<tr><td>%s%s</td><td class="num">%d</td>'
                '<td><span class="st %s">%s%s</span></td>'
                '<td class="num">%s</td><td class="num">%s</td></tr>'
                % (s['slug'], note, s['lessons'], CLS[s['status']],
                   LABEL[s['status']], extra, f, fx))

log = '\n'.join('<tr><td>%s</td><td>%s</td><td class="num">%s</td><td class="num">%s</td></tr>'
                % (b['date'], b['what'], b.get('findings', ''), b.get('fixed', ''))
                for b in reversed(state['batches']))

page = """<title>Retro Fact-Check Tracker</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@400;600&display=swap">
<style>
  body{background:#faf8f5;color:#2d2a26;font-family:Inter,system-ui,sans-serif;margin:0;padding:1.2rem 1rem 3rem;line-height:1.45}
  .wrap{max-width:780px;margin:0 auto}
  h1{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:1.5rem;margin:.4rem 0 .3rem}
  p.intro{color:#5b564e;font-size:.9rem;margin:0 0 1rem;max-width:66ch}
  h2{font-size:.95rem;font-weight:700;margin:1.8rem 0 .5rem}
  .pills{display:flex;gap:.7rem;flex-wrap:wrap;margin:1rem 0}
  .pill{background:#fff;border:1px solid #e8e3db;border-radius:12px;padding:.6rem .95rem;flex:1 1 130px}
  .pill b{display:block;font-size:1.2rem;font-variant-numeric:tabular-nums}
  .pill span{font-size:.74rem;color:#5b564e}
  .bar{height:10px;background:#eee8df;border-radius:6px;overflow:hidden;margin:.4rem 0 1.2rem}
  .bar i{display:block;height:100%%;background:#4f7d63;width:%(pct)d%%}
  .barnote{font-size:.78rem;color:#5b564e;margin:-0.9rem 0 1rem}
  .tablewrap{overflow-x:auto}
  table{border-collapse:collapse;font-size:.8rem;width:100%%}
  td,th{border-bottom:1px solid #eee8df;padding:.3rem .5rem;text-align:left;vertical-align:top}
  th{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#8d8880}
  .num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
  tr.grp td{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:#8d8880;padding-top:.9rem;border-bottom:none}
  .st{font-size:.72rem;font-weight:600;padding:.1rem .5rem;border-radius:8px;white-space:nowrap}
  .st.u{background:#fbeee9;color:#9a3a25}
  .st.p{background:#fdf6e3;color:#8a6d1a}
  .st.g{background:#eaf2ec;color:#3f6f52}
  .note{font-size:.72rem;color:#8d8880;font-weight:400;white-space:normal;max-width:38ch}
  footer{margin-top:2rem;color:#8d8880;font-size:.74rem}
</style>
<div class="wrap">
<h1>Retro Fact-Check Tracker</h1>
<p class="intro">Fact-checking every lesson built before the mandatory gate (~May 2026). Historic finding rate: 11&ndash;15%% of lessons carry something mark-affecting. This page re-renders from <code>scripts/_retrofc/_state.json</code> after every batch &mdash; same link throughout.</p>
<div class="pills">
  <div class="pill"><b>%(done)s</b><span>lessons checked or gate-built</span></div>
  <div class="pill"><b>%(part)s</b><span>lessons in partially-checked subjects</span></div>
  <div class="pill"><b style="color:#9a3a25">%(todo)s</b><span>lessons still to check</span></div>
  <div class="pill"><b>%(findings)d / %(fixed)d</b><span>findings / fixed so far</span></div>
</div>
<div class="bar"><i></i></div>
<p class="barnote">%(pct)d%% of the corpus fully covered (practice-first subjects are separately machine-verified and excluded from the bar).</p>

<h2>Subjects</h2>
<div class="tablewrap"><table>
<tr><th>Subject</th><th class="num">Live lessons</th><th>Status</th><th class="num">Findings</th><th class="num">Fixed</th></tr>
%(rows)s
</table></div>

<h2>Batch log</h2>
<div class="tablewrap"><table>
<tr><th>Date</th><th>Batch</th><th class="num">Findings</th><th class="num">Fixed</th></tr>
%(log)s
</table></div>

<footer>StudyVault \u00b7 updated %(updated)s \u00b7 state: scripts/_retrofc/_state.json</footer>
</div>""" % {'pct': pct, 'done': format(done_l, ','), 'part': format(part_l, ','),
             'todo': format(todo_l, ','), 'findings': findings, 'fixed': fixed,
             'rows': '\n'.join(rows), 'log': log, 'updated': state['updated']}

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'tracker.html')
io.open(out, 'w', encoding='utf-8').write(page)
print('wrote', out)
