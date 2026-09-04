"""Build the diagram canary review page. Usage: canary_report.py <canary_dir> <out.html>
Reads lessons.json, briefs.json, results.json, gate*.json (later files override earlier verdicts),
insert_log.json (optional) and every out/L{n}*.jpg. Thumbnails are embedded at 640px."""
import base64, glob, html, io, json, os, re, sys
from PIL import Image
D, OUT = sys.argv[1], sys.argv[2]
data = json.load(open(os.path.join(D, "lessons.json"), encoding="utf-8"))
briefs = {b["lesson_number"]: b for b in json.load(open(os.path.join(D, "briefs.json"), encoding="utf-8"))}
results = json.load(open(os.path.join(D, "results.json"), encoding="utf-8"))
gate = {}
for gp in sorted(glob.glob(os.path.join(D, "gate*.json"))):
    for k, v in json.load(open(gp, encoding="utf-8")).items():
        gate.setdefault(k, []).append(dict(v, pass_=os.path.basename(gp)))
ins = json.load(open(os.path.join(D, "insert_log.json"), encoding="utf-8")) if os.path.exists(os.path.join(D, "insert_log.json")) else {}
RATE = 30.0  # GBP per 1M output tokens (Foundry, measured 4 Sep)

def thumb(path, w=640):
    im = Image.open(path).convert("RGB"); im.thumbnail((w, w)); b = io.BytesIO(); im.save(b, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def chip(v):
    return {"accept": '<span class="chip ok">Accepted</span>', "reject": '<span class="chip bad">Rejected</span>'}.get(v, f'<span class="chip warn">{html.escape(v)}</span>')

cards = []; n_img = 0; n_acc = 0; forms = {}
for l in data["lessons"]:
    n = l["lesson_number"]; key = f"L{n}"; b = briefs.get(n, {}); form = b.get("visual_form", "none")
    forms[form] = forms.get(form, 0) + 1
    if form == "none":
        cards.append(f'<section class="lesson"><header><span class="num">L{n}</span><h3>{html.escape(l["title"])}</h3><span class="chip mute">No visual</span></header><p class="why">{html.escape(b.get("rationale",""))}</p></section>')
        continue
    attempts = sorted(glob.glob(os.path.join(D, "out", f"{key}_a*.jpg")), key=lambda p: int(re.search(r"_a(\d+)", p).group(1)))
    final = os.path.join(D, "out", f"{key}.jpg")
    seq = attempts + ([final] if os.path.exists(final) else [])
    n_img += len(seq)
    verdicts = gate.get(key, [])
    final_v = verdicts[-1]["verdict"] if verdicts else "not gated"
    if final_v == "accept": n_acc += 1
    figs = []
    for i, p in enumerate(seq):
        v = verdicts[i] if i < len(verdicts) else None
        cap = (chip(v["verdict"]) + f'<p>{html.escape(v.get("note") or "; ".join(v.get("issues", [])) or "")}</p>' if v else '<span class="chip warn">Not gated</span>')
        flags = "".join(f'<p class="flag">For Tom: {html.escape(f)}</p>' for f in (v or {}).get("flag_for_tom", []))
        figs.append(f'<figure><img src="{thumb(p)}" alt="{html.escape(b.get("alt",""))}" loading="lazy"><figcaption><b>Attempt {i+1}</b>{cap}{flags}</figcaption></figure>')
    status = ins.get(key, "")
    cards.append(f'''<section class="lesson"><header><span class="num">L{n}</span><h3>{html.escape(l["title"])}</h3><span class="chip mute">{html.escape(form)}</span>{chip(final_v)}</header>
<p class="why">{html.escape(b.get("rationale",""))} <span class="anchor">Placed after: {html.escape(b.get("anchor_heading",""))}</span></p>
<div class="attempts">{"".join(figs)}</div>
<p class="cap"><b>Caption:</b> {html.escape(b.get("caption",""))}{(" · <b>Live:</b> " + html.escape(status)) if status else ""}</p></section>''')

toks = n_img * 1372
summary = f'''<div class="pills">
<div class="pill"><b>{len(data["lessons"])}</b><span>lessons</span></div>
<div class="pill"><b>{sum(1 for b in briefs.values() if b["visual_form"] != "none")}</b><span>briefed for a visual</span></div>
<div class="pill"><b>{n_acc}</b><span>accepted by the gate</span></div>
<div class="pill"><b>{n_img}</b><span>images generated (incl. retries)</span></div>
<div class="pill"><b>£{toks*RATE/1e6:.2f}</b><span>spent at £30 per million tokens</span></div>
<div class="pill"><b>{(toks*RATE/1e6/max(n_acc,1))*100:.0f}p</b><span>per accepted image</span></div>
</div>'''
page = f'''<title>Diagram Canary: {html.escape(data["unit"]["name"])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
:root{{--bg:#faf8f5;--ink:#2d2a26;--mute:#5b564e;--rule:#e8e3db;--card:#fff;--ok-bg:#eaf2ec;--ok:#3f6f52;--warn-bg:#fdf6e3;--warn:#8a6d1a;--bad-bg:#fbeee9;--bad:#9a3a25;--radius:16px}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1c1a17;--ink:#ece7df;--mute:#a8a094;--rule:#3a3631;--card:#262320;--ok-bg:#20302a;--ok:#9fcfae;--warn-bg:#33301e;--warn:#e0c26a;--bad-bg:#3a2521;--bad:#f0a08e}}}}
:root[data-theme="dark"]{{--bg:#1c1a17;--ink:#ece7df;--mute:#a8a094;--rule:#3a3631;--card:#262320;--ok-bg:#20302a;--ok:#9fcfae;--warn-bg:#33301e;--warn:#e0c26a;--bad-bg:#3a2521;--bad:#f0a08e}}
body{{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;margin:0;padding:1.4rem 1rem 4rem;line-height:1.45}}
.wrap{{max-width:1100px;margin:0 auto}}
h1{{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:1.7rem;margin:.3rem 0 .4rem;text-wrap:balance}}
h3{{font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:1.05rem;margin:0;flex:1;text-wrap:balance}}
p.lede{{color:var(--mute);max-width:70ch;margin:0 0 1.2rem;font-size:.95rem}}
.pills{{display:flex;gap:.7rem;flex-wrap:wrap;margin:0 0 1.6rem}}
.pill{{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:.6rem .95rem;flex:1 1 130px}}
.pill b{{display:block;font-size:1.2rem;font-variant-numeric:tabular-nums}}.pill span{{font-size:.74rem;color:var(--mute)}}
.lesson{{background:var(--card);border:1px solid var(--rule);border-radius:var(--radius);padding:1rem 1.1rem;margin:0 0 1.2rem}}
.lesson header{{display:flex;align-items:center;gap:.7rem;flex-wrap:wrap}}
.num{{font-size:.72rem;font-weight:600;color:var(--mute);letter-spacing:.06em}}
.why{{color:var(--mute);font-size:.86rem;margin:.4rem 0 .7rem}}.anchor{{display:block;font-size:.78rem}}
.attempts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.8rem}}
figure{{margin:0;border:1px solid var(--rule);border-radius:12px;overflow:hidden;background:var(--bg)}}
figure img{{display:block;width:100%;height:auto}}
figcaption{{padding:.5rem .7rem .7rem;font-size:.8rem}}figcaption b{{display:block;margin-bottom:.25rem}}
figcaption p{{margin:.3rem 0 0;color:var(--mute)}}.flag{{color:var(--warn)}}
.cap{{font-size:.84rem;margin:.7rem 0 0}}
.chip{{font-size:.7rem;font-weight:600;padding:.12rem .55rem;border-radius:6px;white-space:nowrap}}
.chip.ok{{background:var(--ok-bg);color:var(--ok)}}.chip.warn{{background:var(--warn-bg);color:var(--warn)}}.chip.bad{{background:var(--bad-bg);color:var(--bad)}}.chip.mute{{background:var(--rule);color:var(--mute)}}
</style>
<div class="wrap">
<h1>Diagram Canary: {html.escape(data["unit"]["name"])}</h1>
<p class="lede">One unit end to end: a brief agent chose a visual form per lesson from the lesson text, GPT-Image-2 (medium, 1536×1024) drew it on Foundry, a Claude vision gate checked every label, figure and word, rejects went back with the gate's note, and accepted figures were inserted after the section they illustrate. Every attempt is shown so the misses are as visible as the hits.</p>
{summary}
{"".join(cards)}
</div>'''
open(OUT, "w", encoding="utf-8").write(page)
print(OUT, len(page)//1024, "KB; accepted", n_acc, "images", n_img, "forms", forms)
