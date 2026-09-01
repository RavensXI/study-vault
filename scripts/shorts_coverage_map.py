"""Shorts Coverage Map: one static HTML page, regenerated on demand.

    python scripts/shorts_coverage_map.py out.html

For every live free-tier subject: how many of its live ARTICLE lessons
have at least one short. Practice-first subjects (settings.format ==
"practice") and practice units inside mixed subjects
(settings.practice_units) have no article lessons and are listed as n/a.

Sources: the public shorts manifest (what the feed actually serves) and a
live Supabase census (service key). The page is a snapshot - the date in
the header is the only thing that tells you how old it is. Republish to
the SAME artifact URL so Tom's link keeps working:
https://claude.ai/code/artifact/4abdf0ca-2f48-4b11-ad49-bb91ab17dc3a
"""
import datetime
import html
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
MANIFEST = "https://www.studyvault.co.uk/data/_shorts_manifest.json"
H = {"apikey": K, "Authorization": "Bearer " + K}


def get(path):
    r = urllib.request.Request(U + "/rest/v1/" + path, headers=H)
    return json.loads(urllib.request.urlopen(r, timeout=120).read())


def paged(path, step=1000):
    out, off = [], 0
    while True:
        chunk = get(f"{path}&limit={step}&offset={off}")
        out += chunk
        if len(chunk) < step:
            return out
        off += step


def census():
    subs = [s for s in get("subjects?select=id,slug,name,settings,status,school_id&school_id=is.null")
            if s.get("status") == "live"]
    units = paged("units?select=id,slug,subject_id&id=not.is.null")
    lessons = paged("lessons?select=unit_id,lesson_number&status=eq.live")
    unit_by_id = {u["id"]: u for u in units}
    rows = {}
    for s in subs:
        st = s.get("settings") or {}
        rows[s["id"]] = {"slug": s["slug"], "name": s["name"],
                         "practice_first": st.get("format") == "practice",
                         "practice_units": set(st.get("practice_units") or []),
                         "article": set()}
    for l in lessons:
        u = unit_by_id.get(l["unit_id"])
        if not u or u["subject_id"] not in rows:
            continue
        r = rows[u["subject_id"]]
        if r["practice_first"] or u["slug"] in r["practice_units"]:
            continue
        r["article"].add((u["slug"], l["lesson_number"]))
    return sorted(rows.values(), key=lambda r: r["slug"])


def manifest():
    req = urllib.request.Request(MANIFEST, headers={"User-Agent": "Mozilla/5.0 (StudyVault QA)"})
    d = json.loads(urllib.request.urlopen(req, timeout=90).read())
    return d if isinstance(d, list) else d.get("items", [])


def build():
    rows, items = census(), manifest()
    per_subject, covered = {}, {}
    for i in items:
        per_subject[i["subject"]] = per_subject.get(i["subject"], 0) + 1
        covered.setdefault(i["subject"], set()).add((i["unit"], i["lesson_number"]))
    total_art = total_cov = full = zero = 0
    trs = []
    for r in rows:
        if r["practice_first"] or not r["article"]:
            trs.append(f'<tr class="na"><td>{html.escape(r["slug"])}</td><td class="num">&mdash;</td>'
                       f'<td class="num">{per_subject.get(r["slug"], 0) or "&mdash;"}</td>'
                       f'<td colspan=2 class="mut">practice-first / no live article lessons</td></tr>')
            continue
        n_art = len(r["article"])
        n_cov = len(r["article"] & covered.get(r["slug"], set()))
        n_sh = per_subject.get(r["slug"], 0)
        pct = round(100 * n_cov / n_art)
        total_art += n_art
        total_cov += n_cov
        cls = "zero" if n_sh == 0 else ("full" if n_cov == n_art else "part")
        full += cls == "full"
        zero += cls == "zero"
        trs.append(f'<tr class="{cls}"><td>{html.escape(r["slug"])}</td><td class="num">{n_art}</td>'
                   f'<td class="num">{n_sh}</td><td class="num">{pct}%</td>'
                   f'<td><div class="bar"><i style="width:{pct}%"></i></div></td></tr>')
    today = datetime.date.today().strftime("%-d %b %Y") if os.name != "nt" else \
        datetime.date.today().strftime("%d %b %Y").lstrip("0")
    return f"""<title>Shorts Coverage Map</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@400;600&display=swap">
<style>
  body{{background:#faf8f5;color:#2d2a26;font-family:Inter,system-ui,sans-serif;margin:0;padding:1.2rem 1rem 3rem;line-height:1.45}}
  .wrap{{max-width:760px;margin:0 auto}}
  h1{{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:1.5rem;margin:.4rem 0 .3rem}}
  p.intro{{color:#5b564e;font-size:.9rem;margin:0 0 1.2rem;max-width:64ch}}
  .stamp{{display:inline-block;background:#fff;border:1px solid #e8e3db;border-radius:8px;padding:.3rem .6rem;font-size:.8rem;color:#5b564e;margin:0 0 .8rem}}
  .stamp b{{color:#2d2a26}}
  .pills{{display:flex;gap:.8rem;flex-wrap:wrap;margin:1rem 0 1.4rem}}
  .pill{{background:#fff;border:1px solid #e8e3db;border-radius:12px;padding:.6rem .95rem;flex:1 1 140px}}
  .pill b{{display:block;font-size:1.2rem;font-variant-numeric:tabular-nums}}
  .pill span{{font-size:.75rem;color:#5b564e}}
  .tablewrap{{overflow-x:auto}}
  table{{border-collapse:collapse;font-size:.8rem;width:100%}}
  td,th{{border-bottom:1px solid #eee8df;padding:.28rem .5rem;text-align:left;white-space:nowrap}}
  th{{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#8d8880;position:sticky;top:0;background:#faf8f5}}
  .num{{text-align:right;font-variant-numeric:tabular-nums}}
  .mut{{color:#8d8880}}
  tr.zero td:first-child{{color:#9a3a25;font-weight:600}}
  tr.full td:first-child{{color:#3f6f52}}
  .bar{{width:110px;height:7px;background:#eee8df;border-radius:4px;overflow:hidden}}
  .bar i{{display:block;height:100%;background:#4f7d63}}
  tr.zero .bar i{{background:#c96f57}}
  .key{{font-size:.75rem;color:#5b564e;margin:.4rem 0 1rem}}
  footer{{margin-top:2rem;color:#8d8880;font-size:.74rem}}
</style>
<div class="wrap">
<h1>Shorts Coverage Map</h1>
<div class="stamp">Snapshot taken <b>{today}</b>. This page does not update itself: ask for a refresh and it is regenerated from the live feed and database.</div>
<p class="intro">Every live free-tier subject: how many of its live article lessons have at least one short. Sorted by slug so board arms sit together. Practice-first subjects and practice units have no article lessons and correctly get no shorts.</p>
<div class="pills">
  <div class="pill"><b>{len(items):,}</b><span>shorts banked</span></div>
  <div class="pill"><b>{total_cov:,} / {total_art:,}</b><span>article lessons with &ge;1 short</span></div>
  <div class="pill"><b>{full}</b><span>subjects fully covered</span></div>
  <div class="pill"><b style="color:#9a3a25">{zero}</b><span>subjects with ZERO shorts</span></div>
</div>
<p class="key"><b style="color:#9a3a25">Red</b> = no shorts at all &middot; <b style="color:#3f6f52">green</b> = every article lesson covered &middot; bar = % of live article lessons with a short.</p>
<div class="tablewrap"><table>
<tr><th>Subject</th><th class="num">Article lessons</th><th class="num">Shorts</th><th class="num">Lesson coverage</th><th></th></tr>
{chr(10).join(trs)}
</table></div>
<footer>StudyVault &middot; generated {today} from the shorts manifest + live Supabase census &middot; shorts are generated per lesson, per board &mdash; no cross-board reuse</footer>
</div>
"""


if __name__ == "__main__":
    out = sys.argv[1]
    page = build()
    open(out, "w", encoding="utf-8").write(page)
    print("wrote", out, len(page), "bytes")
