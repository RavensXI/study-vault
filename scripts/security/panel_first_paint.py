"""
Lesson side panel on first open (24 Sep 2026): the progress box must exist, sit at the top of
the panel, show the final count, and never show the old "N of N complete" state on the way.

  python scripts/security/panel_first_paint.py [BASE]     default http://127.0.0.1:8911

Runs each lesson with the server-rendered text (as on the live site) and, locally, also
without it (?nossr), on desktop and phone width. Samples the panel every 20 ms for 5 s.
"""
import sys
import time

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8911"
LOCAL = "127.0.0.1" in BASE
SKIP = "try{['sv-lesson-tour-v2','sv-reader-tour-v1','sv-cookie-consent'].forEach(k=>localStorage.setItem(k,'1'))}catch(e){}"
LESSONS = ["/lesson/history-aqa/conflict-tension-inter-war/7", "/lesson/science-aqa/chemistry-paper-2/7",
           "/lesson/geography-aqa/paper-1/3", "/lesson/music-edexcel/aos3-stage-and-screen/3"]
PROBE = """() => {
  const sec = document.querySelector('.sidebar-progress-section');
  const s = sec && sec.querySelector('.lesson-progress-summary');
  const sb = document.querySelector('.lesson-sidebar') || {dataset: {}};
  const panel = document.querySelector('.lesson-sidebar > .sv-panel');
  return JSON.stringify({ summary: s ? s.textContent.trim() : null, wrapped: !!sb.dataset.panelWrap,
    topOfPanel: !!(panel && sec && panel.firstElementChild === sec), inFinishCard: !!(sec && sec.closest('.sv-card--finish')),
    listening: document.body.classList.contains('sv-listening-mode') });
}"""
fails = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for vp in ({"width": 1440, "height": 900}, {"width": 390, "height": 844}):
        for path in LESSONS:
            for ssr in ([True, False] if LOCAL else [True]):
                ctx = b.new_context(viewport=vp); ctx.add_init_script(SKIP); pg = ctx.new_page()
                errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:90]))
                url = BASE + path + ("" if ssr else "?nossr=1")
                t0 = time.time(); pg.goto(url, wait_until="commit"); seen = []
                while time.time() - t0 < 5:
                    try:
                        st = pg.evaluate(PROBE)
                        if not seen or seen[-1] != st: seen.append(st)
                    except Exception:
                        pass
                    time.sleep(0.02)
                import json
                last = json.loads(seen[-1]) if seen else {}
                states = [json.loads(s) for s in seen]
                old_state = any(s["summary"] and s["summary"].endswith("complete") for s in states)
                ok_place = last.get("topOfPanel") or last.get("inFinishCard") or (vp["width"] < 961 and last.get("summary"))
                ok = bool(last.get("summary")) and bool(ok_place) and not old_state and not errs
                fails += not ok
                print(("PASS " if ok else "FAIL ") + f'{vp["width"]:>4} {"ssr  " if ssr else "nossr"} {path.split("/lesson/")[1]:45} '
                      f'final={last.get("summary")} top={last.get("topOfPanel")} finish={last.get("inFinishCard")} '
                      f'old-state-seen={old_state} errors={errs[:1]}', flush=True)
                ctx.close()
    b.close()
print("\nall passed" if not fails else f"\n{fails} FAILED")
sys.exit(1 if fails else 0)
