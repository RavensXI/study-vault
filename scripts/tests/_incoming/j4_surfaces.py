# -*- coding: utf-8 -*-
"""Journey 4: the surfaces not yet looked at — browse, guides, exams, revise,
shorts, and the desk dashboard."""
import sys, time, json
sys.path.insert(0, r"C:\Users\tshau\.claude\jobs\4059242c\tmp")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from journey import S, W, H, shot
from playwright.sync_api import sync_playwright

SHELF = ("localStorage.setItem('sv-welcome', JSON.stringify({picked:['maths','lang','lit','science',"
         "'history','geog','psych','business'],boards:{maths:'aqa',lang:'aqa',lit:'aqa',science:'aqa',"
         "history:'aqa',geog:'aqa',psych:'aqa',business:'aqa'},"
         "topics:{history:{'0':'germany-democracy-dictatorship'}},meta:{}}));"
         "localStorage.setItem('studyvault-free-prefs', JSON.stringify({subjects:["
         "{slug:'history-aqa',baseSlug:'history'},{slug:'psychology-aqa',baseSlug:'psych'}]}));")

PAGES = [
 ("browse-history",  "/browse/history-aqa"),
 ("browse-unit",     "/browse/history-aqa/germany-democracy-dictatorship"),
 ("browse-maths",    "/browse/maths-aqa"),
 ("browse-science",  "/browse/science-aqa"),
 ("guide-revision",  "/guide/history-aqa/revision-technique/index"),
 ("guide-exam",      "/guide/history-aqa/exam-technique/index"),
 ("guide-englit",    "/guide/english-literature-aqa/exam-technique/nineteenth-century-extract"),
 ("exams",           "/exams"),
 ("revise",          "/revise"),
 ("shorts",          "/shorts"),
 ("desk",            "/desk"),
 ("classic",         "/classic"),
]

notes = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for tag, path in PAGES:
        ctx = b.new_context(viewport={"width": W, "height": H}); ctx.add_init_script(SHELF)
        pg = ctx.new_page()
        errs, bad = [], []
        pg.on("console", lambda m: errs.append(m.text[:70]) if m.type == "error" else None)
        pg.on("response", lambda r: bad.append(r.url.split("/")[-1][:28]) if r.status >= 400 else None)
        try:
            pg.goto(S + path, wait_until="networkidle", timeout=60000)
        except Exception as e:
            notes.append([tag, {"path": path, "FAIL": str(e)[:60]}]); print("%-16s LOAD FAILED" % tag); ctx.close(); continue
        time.sleep(5)
        shot(pg, "j4_" + tag)
        i = pg.evaluate("""() => ({landed: location.pathname,
            h1: ((document.querySelector('h1')||{}).textContent||'').slice(0,44),
            textLen: document.body.innerText.trim().length})""")
        i["path"] = path; i["404s"] = sorted(set(bad))[:3]; i["errors"] = errs[:2]
        notes.append([tag, i])
        flag = ""
        if i["landed"].rstrip("/") != path.rstrip("/"): flag = " -> REDIRECTED to " + i["landed"]
        if i["textLen"] < 300: flag += " THIN(%d)" % i["textLen"]
        if i["404s"]: flag += " 404:%s" % i["404s"]
        print("%-16s %-46s%s" % (tag, i["h1"], flag))
        ctx.close()
    b.close()
json.dump(notes, open(r"C:\Users\tshau\.claude\jobs\4059242c\tmp\j4_notes.json","w"), indent=1, default=str)
