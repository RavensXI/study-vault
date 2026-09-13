"""Record the tour clips (Tom, 13 Sep 2026): the dashboard set and the lesson set.

One short muted clip per dashboard feature, recorded on the demo students so
every state is on show (revisit slot, quick check, rest day, docking books...).
Re-run after any dashboard change so the tour never drifts from the real thing:

    python scripts/dashboard_tour/record.py                # dashboard clips, both sizes
    python scripts/dashboard_tour/record.py --set lesson   # lesson clips (assets/tour/lesson/)
    python scripts/dashboard_tour/record.py --only revisit --size desktop

Needs a dev server for the checkout on 127.0.0.1:8907 (python _dev_server_8907.py)
and ffmpeg on PATH. Writes assets/tour/<id>-<size>.mp4 (+ .webm), then
assets/tour/manifest.json (ids, sizes, durations) which js/dash-tour.js reads.
The clip copy (title + description) lives in js/dash-tour.js, next to the ids.
"""
import argparse, json, os, shutil, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'assets', 'tour')
LESSON = '/lesson/business-aqa/business-real-world/1'     # the lesson the lesson tour is filmed on: narration, podcast, video, six questions
H = 'http://127.0.0.1:8907'
HEIGHTS = {'books': 1000, 'rings': 1000}     # desktop clips where the topics panel opens under the shelf
SIZES = {
    'desktop': dict(viewport={'width': 1200, 'height': 780}, scale=1),
    'phone': dict(viewport={'width': 390, 'height': 760}, scale=2),
}

# a drawn pointer + a soft ring round the thing being shown; injected into every page
INIT = r"""
(() => {
  const CSS = `
    .tour-cursor{position:fixed;z-index:99999;width:22px;height:22px;margin:-3px 0 0 -3px;pointer-events:none;
      background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M4 2l16 9-7 1.5L9.5 21z' fill='%23fff' stroke='%23000' stroke-width='1.6' stroke-linejoin='round'/></svg>") no-repeat;
      transition:transform .08s;opacity:0}
    .tour-cursor.on{opacity:1}.tour-cursor.down{transform:scale(.82)}
    .tour-ring{position:fixed;z-index:99998;pointer-events:none;border:3px solid #c06325;border-radius:10px;
      box-shadow:0 0 0 6px rgba(192,99,37,.18);animation:tourpulse 1.4s ease-in-out infinite;transition:all .35s ease}
    @keyframes tourpulse{50%{box-shadow:0 0 0 12px rgba(192,99,37,.08)}}
    *{caret-color:transparent}`;
  let cur = null, ring = null, styled = false;
  function ensure() {
    if (!document.documentElement) return false;
    if (!styled) { const st = document.createElement('style'); st.textContent = CSS; document.documentElement.appendChild(st); styled = true; }
    if (!cur) { cur = document.createElement('div'); cur.className = 'tour-cursor'; document.documentElement.appendChild(cur); }
    return true;
  }
  addEventListener('mousemove', e => { if (!ensure()) return; cur.style.left = e.clientX + 'px'; cur.style.top = e.clientY + 'px'; cur.classList.add('on'); }, true);
  addEventListener('mousedown', () => { if (cur) cur.classList.add('down'); }, true);
  addEventListener('mouseup', () => { if (cur) cur.classList.remove('down'); }, true);
  let target = null, tpad = 6;
  function place() {
    if (!ring || !target) return;
    const gone = !document.contains(target) || target.hidden || getComputedStyle(target).display === 'none' || getComputedStyle(target).visibility === 'hidden';
    const r = target.getBoundingClientRect();
    if (gone || (!r.width && !r.height)) { ring.style.opacity = '0'; return; }
    ring.style.opacity = '1';
    ring.style.left = (r.left - tpad) + 'px'; ring.style.top = (r.top - tpad) + 'px';
    ring.style.width = (r.width + tpad * 2) + 'px'; ring.style.height = (r.height + tpad * 2) + 'px';
  }
  (function tick() { place(); requestAnimationFrame(tick); })();
  window.__ring = (sel, pad) => {
    if (!ensure()) return false;
    const el = typeof sel === 'string' ? document.querySelector(sel) : sel;
    if (!el) { if (ring) ring.remove(); ring = null; target = null; return false; }
    target = el; tpad = pad == null ? 6 : pad;
    if (!ring) { ring = document.createElement('div'); ring.className = 'tour-ring'; ring.style.transition = 'opacity .2s'; document.documentElement.appendChild(ring); }
    place();
    return true;
  };
  window.__unring = () => { if (ring) ring.remove(); ring = null; target = null; };
  /* keep every one-time hint out of the picture */
  try {
    localStorage.setItem('sv-dash-tour-v1', '1'); localStorage.setItem('sv-reader-tour-v1', '1'); localStorage.setItem('sv-lesson-tour-v2', '1');
    localStorage.setItem('sv-lesson-tutorial-done', '1'); localStorage.setItem('sv-flashcard-tutorial-done', '1');
  } catch (e) {}
})();
"""


class Clip:
    def __init__(self, pg, size):
        self.pg, self.size, self.phone = pg, size, size == 'phone'
        self.t_start = None

    # ---- helpers ----
    def go(self, path, wait=4500):
        self.pg.goto(H + path); self.pg.wait_for_timeout(wait)
        self.pg.evaluate("document.querySelectorAll('.sv-tour-block,.sv-tour').forEach(e=>e.remove())")

    def demo(self, who='amira', extra=None):
        """seed the demo student, then apply any extra localStorage before the real load"""
        self.pg.goto(H + '/classic?demo=' + who); self.pg.wait_for_timeout(2500)
        for _ in range(20):   # the seed redirects to /classic once written; wait for that
            if self.pg.evaluate("!!localStorage.getItem('sv-user') && !location.search"): break
            self.pg.wait_for_timeout(300)
        if extra:
            self.pg.evaluate("(x)=>{for(const k in x) localStorage.setItem(k, JSON.stringify(x[k]))}", extra)

    def start(self):
        self.t_start = time.time()
        self.pg.wait_for_timeout(600)

    def box(self, sel):
        el = self.pg.locator(sel).first
        try:
            el.scroll_into_view_if_needed(timeout=3000); self.pg.wait_for_timeout(200)
            return el.bounding_box()
        except Exception:
            return None

    def move_to(self, sel, dx=0.5, dy=0.5, steps=22):
        b = self.box(sel)
        if not b: return None
        x, y = b['x'] + b['width'] * dx, b['y'] + b['height'] * dy
        self.pg.mouse.move(x, y, steps=steps); self.pg.wait_for_timeout(250)
        return x, y

    def click(self, sel, dx=0.5, dy=0.5, hold=140, keep=False):
        p = self.move_to(sel, dx, dy)
        if not p: return
        self.pg.mouse.down(); self.pg.wait_for_timeout(hold); self.pg.mouse.up()
        if not keep: self.unring()      # the ring never outlives the screen it was drawn on

    def ring(self, sel, pad=6, nth=0):
        self.pg.evaluate("([s,p,n])=>__ring(document.querySelectorAll(s)[n]||null,p)", [sel, pad, nth])

    def unring(self):
        try: self.pg.evaluate("__unring()")
        except Exception: pass      # the click navigated; the ring went with the old page

    def pause(self, ms):
        self.pg.wait_for_timeout(ms)


# ---------------- the clips ----------------
def clip_plan(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.card.plan'); c.move_to('.card.plan ol li:nth-child(2)'); c.pause(1600)
    c.ring('.starttile' if not c.phone else '.starttile', 4); c.move_to('.starttile'); c.pause(1800)
    c.unring(); c.pause(400)

def clip_revisit(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.card.plan ol li:first-child', 3); c.pause(1200)
    c.click('.card.plan ol li:first-child'); c.pause(1800)
    # answer the first question, whichever option is right
    if c.pg.locator('.wu-opt').count():
        c.click('.wu-opt >> nth=0'); c.pause(1600)
        nxt = c.pg.locator('.wu-card button:has-text("Next"), .wu-card button:has-text("next")').first
        if nxt.count(): c.click('.wu-card button:has-text("Next")'); c.pause(1400)
    c.pause(800)

def clip_quickcheck(c):
    c.demo('amira')
    # a lesson the student rated confident and has not read: the quick check opens on arrival
    c.pg.evaluate("""(()=>{const w=JSON.parse(localStorage.getItem('sv-welcome')||'{}'); w.rag=w.rag||{}; w.rag['history-aqa/conflict-tension-inter-war']='g'; localStorage.setItem('sv-welcome',JSON.stringify(w));
      const d=JSON.parse(localStorage.getItem('sv-lessons-done')||'{}'); d['history-aqa/conflict-tension-inter-war']=[]; localStorage.setItem('sv-lessons-done',JSON.stringify(d));
      const k=JSON.parse(localStorage.getItem('sv-kc-log')||'{}'); Object.keys(k).forEach(x=>{ if(x.indexOf('history-aqa/conflict-tension-inter-war/')===0) delete k[x]; }); localStorage.setItem('sv-kc-log',JSON.stringify(k)); })()""")
    c.go('/lesson/history-aqa/conflict-tension-inter-war/1', 7000); c.start()
    c.pause(600)
    if c.pg.locator('.sv-to-stages').count():
        c.ring('.sv-to-stages', 8); c.move_to('.sv-to-stages'); c.pause(2000); c.unring()
        c.ring('.sv-to-foot', 4); c.move_to('.sv-to-skip'); c.pause(1600); c.unring()
    c.pause(600)

def clip_books(c):
    c.demo('amira'); c.go('/classic'); c.start()
    sel = '.bk >> nth=3'
    c.ring('.bk', 4, nth=3); c.pause(900)
    c.click(sel); c.pause(2200)
    c.ring('.sdetail', 4); c.move_to('.sdetail .top'); c.pause(1400); c.unring()
    if c.pg.locator('.ublock').count():
        c.ring('.units', 3); c.pause(900)
        c.click('.ublock >> nth=1'); c.pause(1500)
        c.ring('.lessons', 4); c.pause(1600); c.unring()
    c.pause(500)

def clip_rings(c):
    c.demo('amira'); c.go('/classic')
    c.pg.locator('.bk').nth(3).click(force=True); c.pause(2000)
    c.start()
    for i, cls in enumerate(['g', 'a', 'r']):
        sel = '.ublock.band-' + cls
        if c.pg.locator(sel).count():
            c.ring(sel, 3); c.move_to(sel); c.pause(1500)
    c.unring(); c.pause(500)

def clip_week(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.card.week', 3); c.pause(900)
    c.click('.card.week'); c.pause(600)
    c.ring('.card.week', 3); c.pause(1400)
    c.ring('.card.week .weeksaid', 4); c.pause(1800); c.unring()
    c.pause(600)

def clip_flashcards(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('#fcdoor', 3); c.pause(900)
    c.click('#fcdoor'); c.pause(1800)
    c.click('.bigcard'); c.pause(2000)
    if c.pg.locator('.fcbtns .fb.ok').count():
        c.ring('.fcbtns', 4); c.pause(900)
        c.click('.fcbtns .fb.ok'); c.pause(1500)
    c.pause(500)

def clip_podcast(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.podbar', 5); c.pause(900)
    c.pg.evaluate("player.muted=true")
    c.click('#podplay', keep=True); c.pause(2800)
    if not c.phone: c.click('#podnext', keep=True); c.pause(2200)   # the skip button is off the phone bar (lock screen has it)
    c.unring(); c.pause(400)

def clip_timer(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.svtimer', 5); c.pause(900)
    c.click('.svtimer', keep=True); c.pause(1200)
    c.click('.svtimer-pop button[data-min="25"]', keep=True); c.pause(2600); c.unring(); c.pause(400)

def clip_restday(c):
    c.demo('amira', {'sv-plan-prefs': {'rest': [time.localtime().tm_wday + 1 if time.localtime().tm_wday < 6 else 0], 'hols': []}})
    c.go('/classic'); c.start()
    c.ring('.card.plan ol li:nth-child(2)', 3); c.move_to('.card.plan ol li:nth-child(2) small'); c.pause(2600); c.unring(); c.pause(500)

def clip_planner(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.card.exam', 3); c.pause(900)
    c.click('.card.exam'); c.pause(2200)
    try: c.pg.wait_for_load_state()
    except Exception: pass
    if c.pg.locator('.plsheet').count() and not c.phone:
        c.move_to('.plsheet .plday >> nth=9'); c.pause(1800)
    elif c.phone: c.pause(1600)
    c.pause(500)

def clip_reading(c):
    c.demo('amira'); c.go('/classic'); c.start()
    c.ring('.svset', 5); c.pause(900)
    c.click('.svset'); c.pause(1200)
    c.ring('.svset-pop .row:first-of-type', 3); c.pause(600)
    c.click('.svset-pop .sw'); c.pause(2200)
    c.click('.svset-pop .sw'); c.pause(1200)
    c.click('.svset-pop [data-font="atkinson"]'); c.pause(1600)
    c.click('.svset-pop [data-font="default"]'); c.pause(600)

# ---------------- the lesson clips ----------------
def lesson_open(c):
    """a signed-in demo student on the tour lesson, page settled, no hints"""
    c.demo('amira'); c.go(LESSON, 7500)
    c.pg.evaluate("document.querySelectorAll('.sv-tour-block,.sv-tour,.sv-tour-card,.sv-tourclips').forEach(e=>e.remove()); document.body.classList.remove('sv-tourclips-open')")
    c.pg.evaluate("window.scrollTo(0,0)"); c.pause(400)

def panel(c):
    """the side panel is a drawer on phones: open it before pointing at anything in it"""
    if c.phone: c.click('.mobile-menu-btn', keep=True); c.pause(900)

def scroll_to(c, sel, offset=120):
    c.pg.evaluate("([s,o])=>{const e=document.querySelector(s); if(e){ const y=e.getBoundingClientRect().top+scrollY-o; window.scrollTo({top:Math.max(0,y),behavior:'smooth'}); }}", [sel, offset]); c.pause(900)

def lclip_read(c):
    lesson_open(c); scroll_to(c, '.a11y-toolbar', 90); c.start()
    c.ring('.a11y-toolbar', 5); c.pause(1000)
    c.click('.a11y-reading-toggle', keep=True); c.pause(900); c.unring()
    c.ring('.a11y-reading-pop', 5); c.pause(800)
    c.click('.a11y-reading-pop .a11y-rd-fonts button >> nth=1', keep=True); c.pause(1800)
    c.click('.a11y-reading-pop .a11y-font-size-group .a11y-font-up', keep=True); c.pause(1500)
    c.click('.a11y-reading-pop .a11y-font-size-group .a11y-font-down', keep=True); c.pause(500)
    c.click('.a11y-reading-pop .a11y-rd-fonts button >> nth=0', keep=True); c.pause(500); c.unring()
    c.pg.keyboard.press('Escape'); c.pause(500)

def lclip_listen(c):
    lesson_open(c); scroll_to(c, '.audio-player-wrapper', 140); c.start()
    c.pg.evaluate("document.querySelectorAll('audio').forEach(a=>a.muted=true)")
    c.ring('.audio-player-wrapper', 5); c.pause(900)
    c.click('.narration-play', keep=True); c.pause(3200)
    tab = c.pg.locator('.audio-tab[data-mode="podcast"]')
    if tab.count() and tab.first.is_visible():
        c.click('.audio-tab[data-mode="podcast"]', keep=True); c.pause(2200)
    c.unring(); c.pause(400)

def lclip_text(c):
    lesson_open(c); scroll_to(c, '.term', 200); c.start()
    c.ring('.term', 3); c.move_to('.term'); c.pause(1000)
    if c.pg.locator('.term-popup').count(): c.ring('.term-popup', 4); c.pause(1600)
    c.unring(); c.pg.mouse.move(600, 200); c.pause(500)
    scroll_to(c, '.key-fact', 160); c.ring('.key-fact', 4); c.pause(1500)
    c.click('.revision-tip-btn', keep=True); c.pause(700)
    if c.pg.locator('.revision-tip-popup.is-open').count(): c.ring('.revision-tip-popup.is-open', 4); c.pause(2000)
    c.unring(); c.pg.keyboard.press('Escape'); c.pause(400)

def lclip_stuck(c):
    lesson_open(c); scroll_to(c, '.sv-chunk', 160); c.start()
    c.ring('.sv-chunk', 6, nth=1); c.pause(900)
    c.click('.sv-chunk >> nth=1'); c.pause(900)
    if c.pg.locator('.sv-bubbles').count():
        c.ring('.sv-bubbles', 6); c.pause(600)
        for i in range(3):
            if c.pg.locator('.sv-bubble').count() > i: c.move_to('.sv-bubble >> nth=%d' % i); c.pause(900)
        c.pause(600); c.unring()
    c.pg.keyboard.press('Escape'); c.pause(500)

def lclip_quiz(c):
    lesson_open(c); scroll_to(c, '.sidebar-knowledge-check', 200); c.start(); panel(c)
    c.ring('#knowledge-check-btn', 4); c.pause(900)
    c.click('#knowledge-check-btn'); c.pause(1200)
    # the right answer, whichever position it was shuffled to
    pos = c.pg.evaluate("""(()=>{ const q=window.knowledgeCheck&&window.knowledgeCheck[0]; if(!q||!q.options) return 0;
      const d=document.createElement('div'); d.innerHTML=q.options[q.correct]; const t=d.textContent.trim();
      const i=[...document.querySelectorAll('#kc-options .kc-option')].findIndex(b=>b.textContent.trim()===t); return i<0?0:i; })()""")
    if c.pg.locator('#kc-options .kc-option').count():
        c.click('#kc-options .kc-option >> nth=%d' % pos, keep=True); c.pause(700)
        c.click('#kc-check', keep=True); c.pause(2200)
        c.ring('#kc-body', 4); c.pause(1200); c.unring()
    c.pause(500)

def lclip_flashcards(c):
    lesson_open(c); scroll_to(c, '.sidebar-flashcard-section', 200); c.start(); panel(c)
    c.ring('#sidebar-flashcard-btn', 4); c.pause(900)
    c.click('#sidebar-flashcard-btn'); c.pause(1500)
    if c.pg.locator('.fc-modal-overlay.active').count():
        c.click('.fc-modal-overlay .fc-card, .fc-modal-overlay .fc-card-container', keep=True); c.pause(1800)
        if c.pg.locator('.fc-answer-btn--right').count():
            c.ring('.fc-modal-overlay .fc-answer-btn--right', 4); c.pause(700)
            c.click('.fc-answer-btn--right'); c.pause(1500)
    c.pause(400)

def lclip_practice(c):
    lesson_open(c); scroll_to(c, '.tile-practice', 260); c.start(); panel(c)
    c.ring('.tile-practice', 4); c.pause(900)
    c.click('.sv-practice-btn'); c.pause(1500)
    if c.pg.locator('.pq-modal').count():
        c.click('#practice-answer', keep=True); c.pause(300)
        c.pg.keyboard.type('A business exists to make a profit by selling goods or services that customers want. It also creates jobs and provides things people need, like food shops or bus services.', delay=18)
        c.pause(600)
        c.ring('#practice-ai-mark', 4); c.pause(600)
        c.click('#practice-ai-mark', keep=True)
        for _ in range(40):
            if c.pg.evaluate("(()=>{const f=document.getElementById('practice-ai-feedback'); return f&&!f.hidden})()"): break
            c.pause(500)
        c.unring(); c.pause(400)
        if c.pg.locator('#practice-ai-feedback:not([hidden])').count():
            c.pg.evaluate("document.getElementById('practice-ai-feedback').scrollIntoView({block:'center',behavior:'smooth'})"); c.pause(800)
            c.ring('#practice-ai-feedback', 4); c.pause(3000); c.unring()
    c.pause(400)

def lclip_tutor(c):
    lesson_open(c); scroll_to(c, '.tile-tutor', 260); c.start(); panel(c)
    c.ring('.tile-tutor', 4); c.pause(900)
    c.click('.tile-tutor .sv-tool-btn'); c.pause(1200)
    if c.pg.locator('.tutor-panel.open').count():
        c.ring('.tutor-panel', 4); c.pause(600)
        c.click('#tutor-input', keep=True); c.pause(300)
        c.pg.keyboard.type('What is the difference between a good and a service?', delay=22); c.pause(500)
        c.pg.keyboard.press('Enter')
        for _ in range(40):
            if c.pg.evaluate("(()=>{const p=document.querySelector('.tutor-panel'); return p&&/service/i.test(p.textContent)&&p.querySelectorAll('[class*=msg],[class*=reply],[class*=bubble],p').length>1})()"): break
            c.pause(500)
        c.pause(3000); c.unring()
    c.pause(400)

def lclip_media(c):
    lesson_open(c); scroll_to(c, '#sidebar-video-section', 200); c.start(); panel(c)
    c.ring('#sidebar-video-section', 4); c.move_to('#sidebar-video-section'); c.pause(1800); c.unring()
    c.ring('.sidebar-media', 4); c.pause(800)
    c.click('.rm-launcher'); c.pause(1500)
    if c.pg.locator('.rm-modal').count(): c.pause(2000)
    c.pg.keyboard.press('Escape'); c.pause(400)

def lclip_focus(c):
    lesson_open(c); scroll_to(c, '.a11y-toolbar', 90); c.start()
    c.ring('.a11y-focus-toggle', 4); c.pause(900)
    c.click('.a11y-focus-toggle', keep=True); c.pause(800); c.unring()
    for i in (1, 2, 3):
        c.pg.evaluate("(i)=>{const e=document.querySelectorAll('.sv-chunk')[i]; if(e) e.scrollIntoView({block:'center',behavior:'smooth'})}", i); c.pause(600)
        c.move_to('.sv-chunk >> nth=%d' % i); c.pause(1500)
    scroll_to(c, '.a11y-toolbar', 90)
    c.click('.a11y-focus-toggle'); c.pause(500)

def lclip_progress(c):
    lesson_open(c); scroll_to(c, '.sidebar-progress-section', 200); c.start(); panel(c)
    c.ring('.sidebar-progress-section', 4); c.move_to('.sidebar-progress-section'); c.pause(2600); c.unring()
    if c.phone: c.click('.sidebar-panel-close-btn'); c.pause(600)
    c.pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); c.pause(900)
    c.ring('#nav-next-lesson', 4); c.move_to('#nav-next-lesson'); c.pause(2000); c.unring(); c.pause(300)

LESSON_CLIPS = [
    ('read', lclip_read), ('listen', lclip_listen), ('text', lclip_text), ('stuck', lclip_stuck), ('quiz', lclip_quiz),
    ('flashcards', lclip_flashcards), ('practice', lclip_practice), ('tutor', lclip_tutor), ('media', lclip_media),
    ('focus', lclip_focus), ('progress', lclip_progress),
]

CLIPS = [
    ('plan', clip_plan), ('revisit', clip_revisit), ('quickcheck', clip_quickcheck), ('books', clip_books),
    ('rings', clip_rings), ('week', clip_week), ('flashcards', clip_flashcards), ('podcast', clip_podcast),
    ('timer', clip_timer), ('restday', clip_restday), ('planner', clip_planner), ('reading', clip_reading),
]


def encode(src, dst_base, trim, phone):
    """webm from Playwright -> mp4 (h264, plays everywhere) + a webm copy; trimmed to the action"""
    scale = 'scale=trunc(iw/2)*2:trunc(ih/2)*2'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{trim:.2f}', '-i', src, '-an',
                    '-vf', scale, '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    dst_base + '.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{trim:.2f}', '-i', src, '-an',
                    '-vf', scale, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', '-row-mt', '1', dst_base + '.webm'], check=True)
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', dst_base + '.mp4'], capture_output=True, text=True)
    return float(out.stdout.strip() or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', nargs='*'); ap.add_argument('--size', choices=list(SIZES), nargs='*')
    ap.add_argument('--set', choices=['dashboard', 'lesson'], default='dashboard')
    a = ap.parse_args()
    global OUT
    clips = CLIPS if a.set == 'dashboard' else LESSON_CLIPS
    if a.set == 'lesson': OUT = os.path.join(OUT, 'lesson')
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, '_raw'); os.makedirs(tmp, exist_ok=True)
    mpath = os.path.join(OUT, 'manifest.json')
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        for cid, fn in clips:
            if a.only and cid not in a.only: continue
            for size, cfg in SIZES.items():
                if a.size and size not in a.size: continue
                phone = size == 'phone'
                vp = dict(cfg['viewport'])
                if not phone and a.set == 'dashboard' and cid in HEIGHTS: vp['height'] = HEIGHTS[cid]
                vs = dict(vp)   # the screencast is in CSS px; a larger frame just leaves the page in one corner
                ctx = browser.new_context(viewport=vp, device_scale_factor=cfg['scale'], is_mobile=phone, has_touch=phone,
                                          record_video_dir=tmp, record_video_size=vs)
                t0 = time.time()
                pg = ctx.new_page(); pg.add_init_script(INIT)
                c = Clip(pg, size)
                try:
                    fn(c)
                except Exception as e:
                    print('FAILED', cid, size, str(e)[:160])
                path = pg.video.path()
                ctx.close()
                trim = max(0.0, (c.t_start or t0) - t0 - 0.25)
                base = os.path.join(OUT, f'{cid}-{size}')
                dur = encode(path, base, trim, phone)
                os.remove(path)
                web = '/assets/tour/' + ('lesson/' if a.set == 'lesson' else '')
                manifest.setdefault(cid, {})[size] = {'mp4': f'{web}{cid}-{size}.mp4', 'webm': f'{web}{cid}-{size}.webm', 'duration': round(dur, 1)}
                print(f'{cid:11s} {size:8s} {dur:5.1f}s  {os.path.getsize(base + ".mp4") // 1024:5d} KB mp4')
        browser.close()
    json.dump(manifest, open(mpath, 'w'), indent=1)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
