# -*- coding: utf-8 -*-
"""Sit the score-reading lessons as a student who cannot read music.

Captures each stage and measures the things that decide whether the lesson is
usable: how big the notation is actually rendered, whether it can be zoomed,
whether anything on it is annotated, and what the first question demands.
"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\sr"
import os
os.makedirs(OUT, exist_ok=True)
BASE = "http://127.0.0.1:8901"
INIT = """
localStorage.setItem('studyvault-auth', JSON.stringify({role:'admin', school_id:null, name:'Admin'}));
sessionStorage.setItem('studyvault-auth', JSON.stringify({role:'admin', school_id:null, name:'Admin'}));
localStorage.setItem('sv-reader-tour-v1','1');
localStorage.setItem('studyvault-cookie-consent','essential');
"""

MEASURE = """() => {
  const out = {imgs: [], lightbox: false, zoomable: false};
  document.querySelectorAll('img').forEach(im => {
    const r = im.getBoundingClientRect();
    if (r.width < 40) return;
    out.imgs.push({
      src: im.src.split('/').pop(),
      natural: im.naturalWidth + 'x' + im.naturalHeight,
      shown: Math.round(r.width) + 'x' + Math.round(r.height),
      scale: im.naturalWidth ? +(r.width / im.naturalWidth).toFixed(2) : null,
      clickable: !!(im.closest('a') || im.style.cursor === 'zoom-in' ||
                    im.classList.contains('lightbox-trigger') || im.closest('[data-lightbox]'))
    });
  });
  out.lightbox = !!document.querySelector('.lightbox, #lightbox, .sv-lightbox');
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for n in (1, 2, 3, 4):
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.add_init_script(INIT)
        errs = []
        pg.on("console", lambda m: errs.append(m.text[:110]) if m.type == "error" else None)
        pg.goto("%s/practice/music-aqa/score-reading/%d" % (BASE, n), wait_until="load")
        pg.wait_for_timeout(4500)

        print("=" * 84)
        title = pg.locator("h1").first.inner_text() if pg.locator("h1").count() else "?"
        print("L%d  %s" % (n, title[:70]))

        # 1. the method modal a student meets first
        modal = pg.locator("#method-modal-overlay.active").first
        if modal.count() and modal.is_visible():
            txt = modal.inner_text()
            print("\n  METHOD MODAL — %d chars, %d words" % (len(txt), len(txt.split())))
            print("  first 300: %s" % txt[:300].replace("\n", " "))
            pg.screenshot(path="%s\\L%d_1_method.png" % (OUT, n))
            for sel in ["#method-modal-close", 'button:has-text("Got it")']:
                loc = pg.locator(sel).first
                if loc.count() and loc.is_visible():
                    loc.click(); pg.wait_for_timeout(700); break
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)

        # 2. how is the notation actually presented?
        m = pg.evaluate(MEASURE)
        print("\n  NOTATION AS RENDERED:")
        for im in m["imgs"]:
            print("    %-24s natural %-11s shown %-11s scale %-5s clickable=%s"
                  % (im["src"][:24], im["natural"], im["shown"], im["scale"], im["clickable"]))
        pg.screenshot(path="%s\\L%d_2_worked.png" % (OUT, n))

        # 3. into the questions
        for label in ["Jump ahead to Practice", "Start practising", "Practise"]:
            loc = pg.locator('button:has-text("%s")' % label).first
            if loc.count() and loc.is_visible():
                loc.click(); pg.wait_for_timeout(2500); break
        q = pg.evaluate("""() => {
          const qEl = document.querySelector('.problem-question, .question-text, [class*=question]');
          const opts = [...document.querySelectorAll('.option-btn, [class*=option]')]
                        .map(o => o.innerText.trim()).filter(t => t && t.length < 120);
          return {q: qEl ? qEl.innerText.trim().slice(0,220) : null, opts: opts.slice(0,6)};
        }""")
        print("\n  FIRST QUESTION: %s" % (q["q"] or "(none found)"))
        for o in q["opts"]:
            print("     - %s" % o.replace("\n", " ")[:90])
        m2 = pg.evaluate(MEASURE)
        print("  notation visible while answering: %s"
              % ([i["shown"] for i in m2["imgs"]] or "NONE"))
        pg.screenshot(path="%s\\L%d_3_question.png" % (OUT, n))
        print("  console errors: %s" % (errs[:2] or "none"))
        print()
        pg.close()
    b.close()
print("screenshots ->", OUT)
