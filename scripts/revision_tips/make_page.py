"""Review page for the revision-tip canary: old tip vs new tip for every box, with Jev's checks."""
import html, os, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "_canary", "revision-tips-canary.html")
TYPE_NAME = {"rank": "Rank", "what_if": "What if", "odd_one_out": "Odd one out", "weak_link": "Weak link", "predict": "Predict",
             "argue": "Argue", "apply": "Apply", "connect": "Connect", "sketch": "Sketch", "exam_question": "Write the question",
             "explain_simply": "Explain simply", "recall_test": "Recall"}
GENERIC = {"key fact": "Cover this box and try to recall every detail from memory.",
           "section": "(the subject's generic line for a dropdown section)", "diagram": "(the subject's generic line for a diagram)",
           "timeline": "Draw this timeline from memory on a blank page, then check your gaps."}
e = html.escape


def status(a):
    if not a.get("new"): return "fail", "Missing"
    if not a.get("pass"): return "fail", "Failed: " + (a.get("why") or "")
    c = (a.get("checks") or {}).get("clear", 1)
    if c < 0.5: return "look", "Passed, worth a look (clarity %.2f)" % c
    return "ok", "Passed"


def make(results):
    units = collections.OrderedDict()
    for key, v in results.items():
        s, u, l = key.split("/")
        units.setdefault((s, u), []).append((l, v))
    allA = [a for v in results.values() for a in v.get("anchors", [])]
    st = collections.Counter(status(a)[0] for a in allA)
    types = collections.Counter(TYPE_NAME.get(a.get("type"), "?") for a in allA if a.get("new"))
    old_recall = sum(1 for a in allA if (a.get("old") or GENERIC.get(a["kind"], "")).lower().startswith(("cover", "close", "test yourself", "write from memory")))

    body = []
    for (s, u), lessons in units.items():
        body.append('<section class="unit"><h2>%s <span>%s</span></h2>' % (e(u.replace("-", " ").capitalize()), e(s)))
        for l, v in sorted(lessons):
            body.append('<article class="lesson"><h3>%s · %s</h3>' % (e(l), e(v.get("title", ""))))
            for a in v.get("anchors", []):
                k, label = status(a)
                old = a.get("old") or GENERIC.get(a["kind"], "")
                ch = a.get("checks") or {}
                checks = " · ".join("%s %.2f" % (n, ch[n]) for n in ("doable", "thinking", "new_fact", "clear") if n in ch)
                body.append(
                    '<div class="tip %s"><div class="meta"><span class="kind">%s</span><span class="type">%s</span>'
                    '<span class="tech">%s</span><span class="st">%s</span></div>'
                    '<p class="new">%s</p><p class="old"><b>Now:</b> %s</p>'
                    '<details><summary>The box and Jev\'s checks</summary><p class="box">%s</p><p class="checks">%s%s</p></details></div>'
                    % (k, e(a["kind"]), e(TYPE_NAME.get(a.get("type"), "?")), e((a.get("technique") or "no link").replace("-", " ")),
                       e(label), e(a.get("new") or "(none)"), e(old), e(a["text"][:900]), e(checks),
                       " · rewritten once" if a.get("rewritten") else ""))
            body.append("</article>")
        body.append("</section>")

    page = """<title>Revision Tips Canary</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#faf8f5;--card:#fff;--ink:#2d2a26;--mut:#6f6a62;--line:#e8e3da;--ok:#2f6b3f;--look:#8a5a12;--fail:#a3322a;--accent:#3d5a73;--soft:#f3efe8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1b1a18;--card:#242220;--ink:#ece8e2;--mut:#a39d93;--line:#38342f;--ok:#8fd19e;--look:#e6b45c;--fail:#ef8f86;--accent:#9cb9d1;--soft:#2c2a27;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1b1a18;--card:#242220;--ink:#ece8e2;--mut:#a39d93;--line:#38342f;--ok:#8fd19e;--look:#e6b45c;--fail:#ef8f86;--accent:#9cb9d1;--soft:#2c2a27;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:400 15px/1.55 Inter,system-ui,sans-serif;margin:0}
.wrap{max-width:900px;margin:0 auto;padding-inline:16px;padding-block:28px 60px}
h1{font:600 1.9rem/1.2 "Source Serif 4",Georgia,serif;margin:0 0 6px;text-wrap:balance}
.lede{color:var(--mut);margin:0 0 18px;max-width:65ch}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 26px}
.stats div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.stats b{display:block;font:600 1.4rem/1.2 Inter;font-variant-numeric:tabular-nums}.stats span{color:var(--mut);font-size:.85rem}
.unit{margin:0 0 30px}.unit h2{font:600 1.3rem "Source Serif 4",Georgia,serif;margin:0 0 10px}.unit h2 span{font:500 .8rem Inter;color:var(--mut);margin-left:6px}
.lesson{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin:0 0 12px}
.lesson h3{font:600 1rem/1.35 Inter;margin:0 0 10px}
.tip{border-top:1px solid var(--line);padding:10px 0}.tip:first-of-type{border-top:0}
.meta{display:flex;flex-wrap:wrap;gap:6px 12px;font:500 .74rem Inter;letter-spacing:.03em;text-transform:uppercase;color:var(--mut)}
.meta .type{color:var(--accent)}.tip.ok .st{color:var(--ok)}.tip.look .st{color:var(--look)}.tip.fail .st{color:var(--fail)}
.new{font:400 1.02rem/1.5 "Source Serif 4",Georgia,serif;margin:6px 0 4px}
.old{color:var(--mut);font-size:.86rem;margin:0}
details{margin-top:6px}summary{cursor:pointer;color:var(--mut);font-size:.82rem}
.box{background:var(--soft);border-radius:10px;padding:8px 10px;font-size:.86rem;margin:6px 0}.checks{font-size:.8rem;color:var(--mut);font-variant-numeric:tabular-nums;margin:0}
.rules{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 18px;margin-top:30px}
.rules h2{font:600 1.2rem "Source Serif 4",Georgia,serif;margin:0 0 8px}.rules li{margin:4px 0}
</style>
<div class="wrap">
<h1>Revision tips: canary</h1>
<p class="lede">New lightbulb tasks for 10 units, first 4 lessons each, written by Opus from what each box says and checked by Jev. The grey line under each is what pupils see now. Nothing is live.</p>
<div class="stats"><div><b>%d</b><span>boxes</span></div><div><b>%d</b><span>passed</span></div><div><b>%d</b><span>worth a look</span></div><div><b>%d</b><span>failed</span></div><div><b>%d</b><span>current tips that are cover/recall</span></div></div>
<p class="lede">Task types used: %s</p>
%s
<div class="rules"><h2>Proposed rule for new builds (docs/CONTENT_PROMPT.md)</h2><ul>
<li>Each tip is about its own box: it names the real people, terms or figures in it.</li>
<li>The pupil does something with the idea: rank, what if, weak link, predict, argue, apply, connect, sketch, write the question, explain simply. Pen and paper, 2 to 5 minutes.</li>
<li>No two boxes in a lesson share a type. Closed-book recall only where exact recall is the point, at most once a lesson.</li>
<li>No new facts, no answer given away, no exam advice. One task, under 180 characters.</li>
<li>Every tip passes Jev's checks (doable, thinking, no new fact, clear) before the lesson is saved.</li>
</ul></div>
</div>""" % (len(allA), st["ok"] + st["look"], st["look"], st["fail"], old_recall,
             e(", ".join("%s %d" % (t, n) for t, n in types.most_common())), "\n".join(body))
    open(PAGE, "w", encoding="utf-8").write(page)
    print("page:", PAGE)
