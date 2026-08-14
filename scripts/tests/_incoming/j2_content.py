# -*- coding: utf-8 -*-
"""Journey 2: open real content as a student and photograph it."""
import sys, time, json
sys.path.insert(0, r"C:\Users\tshau\.claude\jobs\4059242c\tmp")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from journey import S, W, H, shot
from playwright.sync_api import sync_playwright

TARGETS = json.load(open(r"C:\Users\tshau\.claude\jobs\4059242c\tmp\targets.json"))
SHELF = ("localStorage.setItem('sv-welcome', JSON.stringify({picked:['maths','lang','lit','science',"
         "'history','geog','psych','business','rs','cs','spanish'],"
         "boards:{maths:'aqa',lang:'aqa',lit:'aqa',science:'aqa',history:'aqa',geog:'aqa',"
         "psych:'aqa',business:'aqa',rs:'aqa',cs:'ocr',spanish:'aqa'},topics:{},meta:{}}));")

PROBE = """() => {
  const bs = String.fromCharCode(92);
  const txt = document.body.innerText;
  return {title: ((document.querySelector('h1')||{}).textContent||'').slice(0,46),
          path: location.pathname,
          rawTex: txt.split(bs + '(').length - 1,
          textLen: txt.trim().length};
}"""

notes = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for t in TARGETS:
        url = "%s/%s/%s/%s/%s" % (S, t["kind"], t["subject"], t["unit"], t["n"])
        tag = "j2_%s_%s" % (t["subject"], t["unit"][:16])
        ctx = b.new_context(viewport={"width": W, "height": H}); ctx.add_init_script(SHELF)
        pg = ctx.new_page()
        errs, bad = [], []
        pg.on("console", lambda m: errs.append(m.text[:70]) if m.type == "error" else None)
        pg.on("response", lambda r: bad.append(r.url.split("/")[-1][:30]) if r.status >= 400 else None)
        try:
            pg.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            notes.append([tag, {"url": url, "FAIL": str(e)[:60]}]); ctx.close(); continue
        time.sleep(6)
        shot(pg, tag + "_a_top")
        pg.mouse.wheel(0, 2200); time.sleep(2.5)
        shot(pg, tag + "_b_mid")
        i = pg.evaluate(PROBE)
        i["url"] = url; i["404s"] = sorted(set(bad))[:3]; i["errors"] = errs[:2]
        notes.append([tag, i])
        flag = ""
        if i["path"] not in url: flag += " REDIRECTED"
        if i["rawTex"]: flag += " RAW-LATEX x%d" % i["rawTex"]
        if i["textLen"] < 400: flag += " THIN(%d)" % i["textLen"]
        print("%-42s %-44s%s" % (tag[3:], i["title"], flag))
        ctx.close()
    b.close()
json.dump(notes, open(r"C:\Users\tshau\.claude\jobs\4059242c\tmp\j2_notes.json", "w"), indent=1, default=str)
print("\nsaved notes")
