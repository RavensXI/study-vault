# -*- coding: utf-8 -*-
"""Journey 1: brand-new student, front door to dashboard."""
import sys, time
sys.path.insert(0, r"C:\Users\tshau\.claude\jobs\4059242c\tmp")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from journey import OUT, S, W, H, shot
from playwright.sync_api import sync_playwright

# each click re-renders the view, so pick ONE per pass and re-query every time
CLICK_ONE_BOARD = """() => {
  const rows = [...document.querySelectorAll('.brow')];
  for (const r of rows) {
    if (r.querySelector('.chip[aria-pressed="true"]')) continue;
    const c = r.querySelector('.chip:not(.off)') || r.querySelector('.chip');
    if (c) { c.click(); return true; }
  }
  return false;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context(viewport={"width": W, "height": H}).new_page()
    errs = []
    pg.on("console", lambda m: errs.append(m.text[:90]) if m.type == "error" else None)

    pg.goto(S + "/", wait_until="networkidle", timeout=60000); time.sleep(3.5)
    shot(pg, "j1_01_landing")
    pg.evaluate("() => go('picker')"); time.sleep(2.5)
    for s in ("history", "geog", "psych", "business"):
        pg.evaluate("(s)=>{const e=[...document.querySelectorAll('[data-slug]')].find(x=>x.dataset.slug===s&&x.offsetParent); if(e)e.click();}", s)
        time.sleep(0.5)
    time.sleep(1); shot(pg, "j1_03_picker-chosen")

    pg.evaluate("() => go('boards')"); time.sleep(2.5)
    for _ in range(20):
        if not pg.evaluate(CLICK_ONE_BOARD): break
        time.sleep(0.9)
    time.sleep(1.5); shot(pg, "j1_05_boards-chosen")
    print("boards stored:", pg.evaluate("() => JSON.parse(localStorage.getItem('sv-welcome')||'{}').boards"))

    pg.evaluate("() => go('topics')"); time.sleep(2.5)
    for q in range(14):
        chips = pg.evaluate("() => [...document.querySelectorAll('#tcard .chip')].filter(e=>e.offsetParent).length")
        if not chips: break
        label = pg.evaluate("() => ((document.querySelector('.tq')||{}).textContent||'').slice(0,30)")
        shot(pg, "j1_06_topic%02d" % (q + 1))
        # some questions need 2 or 4 picks — keep choosing until Next unlocks
        for k in range(4):
            pg.evaluate("(k) => { const c=[...document.querySelectorAll('#tcard .chip')].filter(e=>e.offsetParent); if(c[k]) c[k].click(); }", k)
            time.sleep(0.9)
            nx0 = pg.locator("#tnext")
            if nx0.count() and not nx0.is_disabled(): break
        nx = pg.locator("#tnext")
        if nx.count() and not nx.is_disabled():
            nx.click(); time.sleep(2.0)
        else:
            print("  stuck on:", label, "| next disabled"); break
        if "/classic" in pg.url or "/desk" in pg.url: break
    time.sleep(4); shot(pg, "j1_07_dashboard")
    print("ended at:", pg.url)
    print("console errors:", errs[:6])
    b.close()
