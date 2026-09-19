"""Opus vs Sonnet canary, side by side per lesson: scripts/flashcards/_authored/compare.html"""
import io, json, os, html as H, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_authored")
UNITS = [("AQA History: Britain, Health and the People", "history-aqa__britain-health-people"), ("AQA Combined Science: Biology Paper 1", "science-aqa__biology-paper-1")]
def e(s): return H.escape(str(s if s is not None else ""))
def load(f): return json.load(io.open(os.path.join(D, f), encoding="utf-8"))
def card_html(c):
    held = c["gate"] != "pass"
    h = '<div class="card%s"><div class="head"><span class="kind">%s</span>%s</div><p class="front">%s</p>' % (" held" if held else "", "Name them all" if c["kind"] == "list" else "Explain", ('<span class="hold">held: %s</span>' % e(", ".join(c.get("problems") or []))) if held else "", e(c["front"]))
    if c["kind"] == "list":
        h += '<ol class="items">' + "".join('<li>%s<span class="p">%s</span></li>' % (e(it), ("%d%%" % round(100 * p)) if p is not None else "") for it, p in zip(c.get("items") or [], (c.get("item_p") or []) + [None] * 8)) + '</ol>'
    else:
        h += '<p class="answer">%s</p>' % e(c["answer"])
    return h + '</div>'
parts = []; stats = {"opus": collections.Counter(), "sonnet": collections.Counter()}
for name, slug in UNITS:
    opus = load(slug + ".gated.json"); son = load("sonnet__" + slug + ".gated.json")
    for m, cs in (("opus", opus), ("sonnet", son)):
        stats[m]["cards"] += len(cs); stats[m]["pass"] += sum(1 for c in cs if c["gate"] == "pass")
        stats[m]["explain_words"] += sum(len((c.get("answer") or "").split()) for c in cs if c["kind"] == "explain"); stats[m]["explain_n"] += sum(1 for c in cs if c["kind"] == "explain")
        stats[m]["item_conf"] += sum(sum(c.get("item_p") or []) for c in cs if c["kind"] == "list"); stats[m]["items"] += sum(len(c.get("item_p") or []) for c in cs if c["kind"] == "list")
    lessons = sorted({(c["lesson_number"], c["title"]) for c in opus + son})
    h = '<h2 class="sect">%s</h2>' % e(name)
    for n, title in lessons:
        h += '<section class="lesson"><h3>Lesson %d · %s</h3><div class="cols"><div class="col"><h4>Opus</h4>%s</div><div class="col"><h4>Sonnet</h4>%s</div></div></section>' % (
            n, e(title), "".join(card_html(c) for c in sorted(opus, key=lambda x: x["kind"]) if c["lesson_number"] == n), "".join(card_html(c) for c in sorted(son, key=lambda x: x["kind"]) if c["lesson_number"] == n))
    parts.append(h)
def row(m):
    s = stats[m]; return "<tr><td>%s</td><td>%d</td><td>%d</td><td>%.1f</td><td>%d%%</td></tr>" % (m.capitalize(), s["cards"], s["cards"] - s["pass"], s["explain_words"] / max(s["explain_n"], 1), round(100 * s["item_conf"] / max(s["items"], 1)))
page = """<title>Opus and Sonnet Cards</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Inter:wght@400;500;600&display=swap">
<style>
:root{--bg:#faf8f5;--ink:#2d2a26;--muted:#6f685f;--rule:#e4ddd2;--card:#fff;--hold:#a24d2a;--holdbg:#f6e7df}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1c1a17;--ink:#ece6dc;--muted:#a69e92;--rule:#3a352e;--card:#26231f;--hold:#e0906d;--holdbg:#3d2a21}}
:root[data-theme="dark"]{--bg:#1c1a17;--ink:#ece6dc;--muted:#a69e92;--rule:#3a352e;--card:#26231f;--hold:#e0906d;--holdbg:#3d2a21}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:14.5px;line-height:1.5;margin:0;padding-block:32px 72px;padding-inline:max(16px,calc((100% - 1040px)/2))}
h1,h2,h3,h4{font-family:"Source Serif 4",Georgia,serif;text-wrap:balance;margin:0}
h1{font-size:32px;font-weight:600}.lede{color:var(--muted);margin:10px 0 0;max-width:68ch}
table{border-collapse:collapse;margin-top:18px;font-variant-numeric:tabular-nums}th,td{text-align:left;padding:6px 14px 6px 0;border-bottom:1px solid var(--rule)}th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
h2.sect{font-size:22px;font-weight:600;margin-top:40px;padding-top:18px;border-top:1px solid var(--rule)}
.lesson{margin-top:22px}.lesson h3{font-size:16px;font-weight:600;color:var(--muted);margin-bottom:8px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:700px){.cols{grid-template-columns:1fr}}
.col h4{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.card{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:10px 14px;margin:6px 0}.card.held{background:var(--holdbg)}
.head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.hold{color:var(--hold);text-transform:none;letter-spacing:0}
.front{font-family:"Source Serif 4",Georgia,serif;font-size:16px;font-weight:600;margin:5px 0 4px}
.answer{margin:0}.items{margin:2px 0 0;padding-left:22px}.items li{margin:2px 0}.items .p{color:var(--muted);font-size:12px;margin-left:8px}
</style>
<h1>Opus and Sonnet Cards</h1>
<p class="lede">The same brief, the same two units, written twice: once by Opus (the first canary, already on the preview) and once by Sonnet. Every card checked by Jev against its lesson. The question is whether Sonnet is good enough for the fleet run at two thirds of the price.</p>
<table><thead><tr><th>Model</th><th>Cards</th><th>Held by the gate</th><th>Words per explain answer</th><th>List items the judge is sure are in the lesson</th></tr></thead><tbody>@ROWS@</tbody></table>
@PARTS@
""".replace("@ROWS@", row("opus") + row("sonnet")).replace("@PARTS@", "".join(parts))
io.open(os.path.join(D, "compare.html"), "w", encoding="utf-8").write(page); print("written", dict(stats["opus"]), dict(stats["sonnet"]))
