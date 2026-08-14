# -*- coding: utf-8 -*-
"""Journey 3: actually USE a practice drill — dismiss the modal, answer one
wrong, read the feedback, open the walkthrough. Today's bugs all lived past the
first click."""
import sys, time, json
sys.path.insert(0, r"C:\Users\tshau\.claude\jobs\4059242c\tmp")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from journey import S, W, H, shot
from playwright.sync_api import sync_playwright

DRILLS = [("maths-aqa", "number", 1), ("maths-aqa", "algebra", 1),
          ("english-language-aqa", "paper-1-reading", 1),
          ("spanish-aqa", "people-and-lifestyle", 1),
          ("geography-aqa", "geographical-skills", 1)]
SHELF = ("localStorage.setItem('sv-welcome', JSON.stringify({picked:['maths','lang','geog','spanish'],"
         "boards:{maths:'aqa',lang:'aqa',geog:'aqa',spanish:'aqa'},topics:{},meta:{}}));")

notes = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for sub, unit, n in DRILLS:
        url = "%s/practice/%s/%s/%s" % (S, sub, unit, n)
        tag = "j3_%s_%s" % (sub, unit[:14])
        ctx = b.new_context(viewport={"width": W, "height": H}); ctx.add_init_script(SHELF)
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text[:70]) if m.type == "error" else None)
        try:
            pg.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            notes.append([tag, {"FAIL": str(e)[:70]}]); ctx.close(); continue
        time.sleep(5)
        # dismiss the method modal so the page is visible
        for lbl in ("Got it, let's practise!", "Got it", "Start Practice"):
            try:
                el = pg.locator('button:has-text("%s")' % lbl).first
                if el.count() and el.is_visible(): el.click(); break
            except Exception: pass
        time.sleep(1.5)
        try: pg.evaluate("() => switchMode('practice')")
        except Exception: pass
        time.sleep(3)
        shot(pg, tag + "_a_question")
        # answer wrong: pick a non-answer option, or type nonsense
        kind = pg.evaluate("""() => {
          if (document.querySelector('.mc-option')) return 'mc';
          if (document.querySelector('#problem-input-a')) return 'text';
          return 'other';
        }""")
        if kind == "mc":
            pg.evaluate("""() => { const ps=window.practiceState, b=window._problemBank;
              const p=b[ps.currentTier][ps.currentIndex];
              const sol=p.solutions[0];
              const bs=[...document.querySelectorAll('.mc-option')];
              (bs.find(x=>+x.dataset.idx!==sol)||bs[0]).click(); }""")
        elif kind == "text":
            pg.fill("#problem-input-a", "0")
        time.sleep(0.8)
        try: pg.evaluate("() => checkAnswer()")
        except Exception: pass
        time.sleep(2.5)
        shot(pg, tag + "_b_feedback")
        fb = pg.evaluate("() => ((document.getElementById('problem-feedback-content')||{}).innerText||'').slice(0,180)")
        notes.append([tag, {"inputKind": kind, "feedback": fb.replace("\n", " | "), "errors": errs[:2]}])
        print("%-34s [%s] %s" % (tag[3:], kind, fb.replace("\n", " | ")[:110]))
        ctx.close()
    b.close()
json.dump(notes, open(r"C:\Users\tshau\.claude\jobs\4059242c\tmp\j3_notes.json","w"), indent=1, default=str)
