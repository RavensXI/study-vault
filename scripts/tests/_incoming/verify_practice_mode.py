# -*- coding: utf-8 -*-
"""Answer a real question in practice mode: player present, card readable,
buttons reachable. This is the state a student is actually in most of the time."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"
BASE = "http://127.0.0.1:8901"
INIT = """
localStorage.setItem('studyvault-auth', JSON.stringify({role:'admin', school_id:null, name:'Admin'}));
sessionStorage.setItem('studyvault-auth', JSON.stringify({role:'admin', school_id:null, name:'Admin'}));
localStorage.setItem('sv-reader-tour-v1','1');
localStorage.setItem('studyvault-cookie-consent','essential');
"""
PAGES = [
    ("music-aos1-L1", "/practice/music-aqa/western-classical-1650-1910/1"),
    ("music-skills-L1", "/practice/music-aqa/listening-skills/1"),
    ("geog-skills-L1", "/practice/geography-aqa/geographical-skills/1"),
]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for name, path in PAGES:
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.add_init_script(INIT)
        errs = []
        pg.on("console", lambda m: errs.append(m.text[:120]) if m.type == "error" else None)
        pg.goto(BASE + path, wait_until="load")
        pg.wait_for_timeout(4200)
        for sel in ['button:has-text("Got it")']:
            try:
                loc = pg.locator(sel).first
                if loc.count() and loc.is_visible():
                    loc.click(); pg.wait_for_timeout(600)
            except Exception:
                pass
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
        # into practice
        for label in ["Jump ahead to Practice", "Start practising", "Practise"]:
            try:
                loc = pg.locator('button:has-text("%s")' % label).first
                if loc.count() and loc.is_visible():
                    loc.click(); pg.wait_for_timeout(2600); break
            except Exception:
                pass
        st = pg.evaluate("""() => {
          const g = document.querySelector('.guided-card-head');
          const players = document.querySelectorAll('.sv-ap-inline');
          const wired = document.querySelectorAll('.sv-ap-inline[data-api-init]');
          const vis = [...players].filter(x => x.offsetParent !== null).length;
          return {guidedOver: g ? g.scrollHeight - g.clientHeight : null,
                  hasMore: g ? g.classList.contains('has-more') : null,
                  players: players.length, wired: wired.length, visible: vis,
                  native: document.querySelectorAll('audio[controls]').length};
        }""")
        print("== %-16s %s" % (name, st))
        # try answering: click the first option then submit
        try:
            opt = pg.locator(".option-btn, .mcq-option, [class*=option]").first
            if opt.count() and opt.is_visible():
                opt.click(); pg.wait_for_timeout(700)
        except Exception:
            pass
        pg.screenshot(path="%s\\pm_%s.png" % (OUT, name))
        print("   errors:", errs[:3] or "none")
        pg.close()
    b.close()
