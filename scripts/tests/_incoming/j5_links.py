# -*- coding: utf-8 -*-
"""Journey 5: every internal link a student is OFFERED on a lesson page —
header, sidebar, footer — followed and checked. A dead link only exists if the
site actually shows it, which is why this reads links off the page rather than
guessing URLs (my invented /guide/.../exam-technique/index proved nothing)."""
import sys, time, json
sys.path.insert(0, r"C:\Users\tshau\.claude\jobs\4059242c\tmp")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from journey import S, W, H
from playwright.sync_api import sync_playwright

LESSONS = [
 ("history-aqa",          "/lesson/history-aqa/germany-democracy-dictatorship/1"),
 ("psychology-aqa",       "/lesson/psychology-aqa/memory/1"),
 ("business-aqa",         "/lesson/business-aqa/business-real-world/1"),
 ("science-aqa",          "/lesson/science-aqa/biology-paper-1/1"),
 ("geography-aqa",        "/lesson/geography-aqa/paper-1/1"),
 ("religious-studies-aqa","/lesson/religious-studies-aqa/christianity-beliefs/1"),
 ("computer-science",     "/lesson/computer-science/computer-systems/1"),
 ("english-literature-aqa","/lesson/english-literature-aqa/macbeth/1"),
]
SHELF = ("localStorage.setItem('studyvault-free-prefs', JSON.stringify({subjects:["
         "{slug:'history-aqa'},{slug:'psychology-aqa'},{slug:'business-aqa'},{slug:'science-aqa'},"
         "{slug:'geography-aqa'},{slug:'religious-studies-aqa'},{slug:'computer-science'},"
         "{slug:'english-literature-aqa'}]}));")

dead = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for name, path in LESSONS:
        ctx = b.new_context(viewport={"width": W, "height": H}); ctx.add_init_script(SHELF)
        pg = ctx.new_page()
        try:
            pg.goto(S + path, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print("%-24s LESSON FAILED TO LOAD" % name); ctx.close(); continue
        time.sleep(6)
        links = pg.evaluate("""() => [...document.querySelectorAll('a[href]')]
            .filter(a => a.offsetParent)
            .map(a => ({text: a.textContent.trim().slice(0,26), href: a.getAttribute('href')}))
            .filter(l => l.href && l.href[0] === '/' )""")
        seen, bad = set(), []
        for l in links:
            if l["href"] in seen: continue
            seen.add(l["href"])
            r = pg.request.get(S + l["href"])
            status = r.status
            # a 200 that lands on a "not found" screen still counts as dead
            body = ""
            if status < 400:
                try: body = r.text()[:4000]
                except Exception: body = ""
            if status >= 400:
                bad.append((l["text"], l["href"], status))
        print("%-24s %2d links checked, %d hard-dead" % (name, len(seen), len(bad)))
        for t, h, s in bad: print("      DEAD %-3s %-26s %s" % (s, t, h))
        dead.append([name, len(seen), bad])
        ctx.close()
    b.close()
json.dump(dead, open(r"C:\Users\tshau\.claude\jobs\4059242c\tmp\j5_links.json","w"), indent=1, default=str)
