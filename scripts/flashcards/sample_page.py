"""Render the gated authored cards as one page for Tom's look: scripts/flashcards/_authored/sample.html"""
import io, json, os, html as H, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_authored")
SETS = [("AQA History: Britain, Health and the People", "history-aqa__britain-health-people.gated.json"), ("AQA Combined Science: Biology Paper 1", "science-aqa__biology-paper-1.gated.json")]
def e(s): return H.escape(str(s if s is not None else ""))
parts = []; tot = collections.Counter()
for name, f in SETS:
    cards = json.load(io.open(os.path.join(D, f), encoding="utf-8"))
    by = collections.OrderedDict()
    for c in sorted(cards, key=lambda x: (x["lesson_number"], x["kind"])): by.setdefault((c["lesson_number"], c["title"]), []).append(c)
    tot["cards"] += len(cards); tot["pass"] += sum(1 for c in cards if c["gate"] == "pass"); tot["list"] += sum(1 for c in cards if c["kind"] == "list"); tot["explain"] += sum(1 for c in cards if c["kind"] == "explain")
    h = '<h2 class="sect">%s</h2>' % e(name)
    for (n, title), cs in by.items():
        h += '<section class="lesson"><h3>Lesson %d · %s</h3>' % (n, e(title))
        for c in cs:
            held = c["gate"] != "pass"
            h += '<div class="card%s"><div class="head"><span class="kind">%s</span>%s</div>' % (" held" if held else "", "Name them all" if c["kind"] == "list" else "Explain", ('<span class="hold">held: %s</span>' % e(", ".join(c.get("problems") or []))) if held else "")
            h += '<p class="front">%s</p>' % e(c["front"])
            if c["kind"] == "list":
                h += '<ol class="items">' + "".join('<li>%s<span class="p">%s</span></li>' % (e(it), ("%d%%" % round(100 * p)) if p is not None else "") for it, p in zip(c.get("items") or [], (c.get("item_p") or []) + [None] * 8)) + '</ol>'
            else:
                h += '<p class="answer">%s</p>' % e(c["answer"])
            h += '</div>'
        h += '</section>'
    parts.append(h)
page = """<title>List and Explain Cards</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Inter:wght@400;500;600&display=swap">
<style>
:root{--bg:#faf8f5;--ink:#2d2a26;--muted:#6f685f;--rule:#e4ddd2;--card:#fff;--accent:#2f6b6b;--hold:#a24d2a;--holdbg:#f6e7df}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1c1a17;--ink:#ece6dc;--muted:#a69e92;--rule:#3a352e;--card:#26231f;--accent:#7fc1bd;--hold:#e0906d;--holdbg:#3d2a21}}
:root[data-theme="dark"]{--bg:#1c1a17;--ink:#ece6dc;--muted:#a69e92;--rule:#3a352e;--card:#26231f;--accent:#7fc1bd;--hold:#e0906d;--holdbg:#3d2a21}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:15px;line-height:1.5;margin:0;padding-block:32px 72px;padding-inline:max(16px,calc((100% - 720px)/2))}
h1,h2,h3{font-family:"Source Serif 4",Georgia,serif;text-wrap:balance;margin:0}
h1{font-size:32px;font-weight:600}.lede{color:var(--muted);margin:10px 0 0;max-width:62ch}
.stats{display:flex;gap:18px;flex-wrap:wrap;margin:22px 0 0;color:var(--muted);font-size:14px}.stats b{color:var(--ink);font-variant-numeric:tabular-nums}
h2.sect{font-size:22px;font-weight:600;margin-top:40px;padding-top:18px;border-top:1px solid var(--rule)}
.lesson{margin-top:22px}.lesson h3{font-size:16px;font-weight:600;color:var(--muted);margin-bottom:8px}
.card{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:12px 16px;margin:8px 0}
.card.held{background:var(--holdbg)}
.head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.hold{color:var(--hold);text-transform:none;letter-spacing:0}
.front{font-family:"Source Serif 4",Georgia,serif;font-size:17px;font-weight:600;margin:6px 0 4px}
.answer{margin:0;color:var(--ink)}.items{margin:2px 0 0;padding-left:22px}.items li{margin:2px 0}.items .p{color:var(--muted);font-size:12px;margin-left:8px;font-variant-numeric:tabular-nums}
</style>
<h1>List and Explain Cards</h1>
<p class="lede">The canary: two units authored on the subscription, two list cards and two explain cards per lesson, every card checked by Jev against its own lesson. Small grey percentages are the judge's confidence that each list item is stated in the lesson. Held cards are the ones I would not ship as written.</p>
<div class="stats"><span><b>@C@</b> cards</span><span><b>@L@</b> list</span><span><b>@E@</b> explain</span><span><b>@P@</b> pass the gate</span><span><b>@H@</b> held</span></div>
@PARTS@
""".replace("@C@", str(tot["cards"])).replace("@L@", str(tot["list"])).replace("@E@", str(tot["explain"])).replace("@P@", str(tot["pass"])).replace("@H@", str(tot["cards"] - tot["pass"])).replace("@PARTS@", "".join(parts))
io.open(os.path.join(D, "sample.html"), "w", encoding="utf-8").write(page); print("written", tot)
