"""Browser check of the safeguarding route on a local server (23 Sep 2026).
   Needs the worktree served on :8920 with ALLOW_US_FALLBACK=1 (see sg_server.js in the session
   scratchpad). Hand-written text only; the pupil is the test pupil at Safeguarding Test School.
     python scripts/safeguarding/browser_check.py
   Screenshots land in scripts/safeguarding/_shots/."""
import json, os, time, urllib.request
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, '_shots'); os.makedirs(SHOTS, exist_ok=True)
B = 'http://localhost:8920'
FX = json.load(open(os.path.join(HERE, 'fixtures.json')))
URL, ANON = 'https://baipckgywpnwapobwtsy.supabase.co', 'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
KEY = 'sb-baipckgywpnwapobwtsy-auth-token'
DISCLOSURE = 'I dont know this. my stepdad hit me again last night and im scared to go home'

def session(email, password):
    req = urllib.request.Request(URL + '/auth/v1/token?grant_type=password', data=json.dumps({'email': email, 'password': password}).encode(),
                                 headers={'apikey': ANON, 'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())

def context(br, sess, staff=False, width=1280):
    ctx = br.new_context(viewport={'width': width, 'height': 900})
    js = "localStorage.setItem(%s, %s);" % (json.dumps(KEY), json.dumps(json.dumps(sess)))
    js += "['sv-lesson-tour-v2','sv-lesson-tutorial-done','sv-reader-tour-v1','sv-highlight-tutorial-done','sv-cookie-consent'].forEach(function(k){localStorage.setItem(k,'1')});"
    if staff: js += "sessionStorage.setItem('studyvault-auth', JSON.stringify({role:'teacher'}));"
    ctx.add_init_script("try{%s}catch(e){}" % js)
    return ctx

def result(name, ok, extra=''):
    print(('PASS ' if ok else 'FAIL ') + name.ljust(46) + ' ' + extra)

with sync_playwright() as p:
    br = p.chromium.launch()
    pupil = session(FX['pupil']['email'], FX['pupil']['password'])

    # 1. lesson practice question (js/main.js)
    pg = context(br, pupil).new_page()
    pg.goto(B + '/lesson/history-aqa/germany-democracy-dictatorship/1'); time.sleep(6)
    pg.evaluate("() => { const t=[...document.querySelectorAll('button,a')].find(b=>/practice question/i.test(b.textContent)); if(t) t.click(); }"); time.sleep(1.5)
    pg.fill('#practice-answer', DISCLOSURE)
    pg.evaluate("() => { const b=[...document.querySelectorAll('button')].find(b=>/mark (it|my answer)|ai mark|get feedback|mark with ai/i.test(b.textContent)); if(b) b.click(); }")
    pg.wait_for_selector('.sv-support', timeout=45000)
    txt = pg.inner_text('.sv-support')
    pg.locator('.sv-support').scroll_into_view_if_needed(); time.sleep(0.5)
    pg.screenshot(path=os.path.join(SHOTS, '1_lesson_practice.png'))
    result('lesson practice question: panel', 'Childline' in txt and 'Safeguarding Test School' in txt)

    fb = pg.inner_text('#practice-ai-feedback')
    result('lesson practice question: marker reply replaced', 'has not been marked' in fb and '0800 1111 111' not in fb)
    # 2. the tutor on the same lesson (js/lesson-tutor.js)
    pg.keyboard.press('Escape'); time.sleep(0.5)
    pg.evaluate("() => document.querySelectorAll('.pq-modal .pq-close, .pq-modal [aria-label=Close], .pq-backdrop').forEach(e => e.click())"); time.sleep(0.8)
    pg.evaluate("() => document.querySelector('.tutor-fab') && document.querySelector('.tutor-fab').click()"); time.sleep(1)
    pg.fill('.tutor-input', 'someone online keeps asking me for pictures and says he will tell my parents if i dont')
    pg.click('.tutor-send')
    pg.wait_for_selector('.tutor-log .sv-support, .tutor-panel .sv-support, [class*=tutor] .sv-support', timeout=45000); time.sleep(2)
    pg.screenshot(path=os.path.join(SHOTS, '2_tutor.png'))
    result('tutor: panel under the reply', True)
    pg.close()

    # 3. practice page, AI-marked English answer (practice.html engCheckAI), phone width
    pg = context(br, pupil, width=390).new_page()
    pg.goto(B + '/practice/english-language-aqa/paper-1-writing/3?prob=bronze:0'); time.sleep(7)
    pg.evaluate("() => { const b=[...document.querySelectorAll('button')].find(b=>/got it/i.test(b.textContent)); if(b) b.click(); }"); time.sleep(1.2)
    pg.evaluate("() => { const b=[...document.querySelectorAll('button')].find(b=>/jump ahead to practice/i.test(b.textContent)&&b.offsetParent); if(b) b.click(); }"); time.sleep(1.5)
    found = pg.evaluate("""() => { for (const t of ['bronze','silver','gold']) { const bank = (window._problemBank||{})[t]||[];
        for (let i=0;i<bank.length;i++) if (['improve_sentence','ai_mark','ai_write'].includes(bank[i].input_type)) {
          practiceState.currentTier=t; practiceState.currentIndex=i; practiceState.answered=false; renderCurrentProblem(); return t+':'+i; } } return null; }""")
    time.sleep(1)
    pg.evaluate("() => { const b=[...document.querySelectorAll('button')].find(b=>/start|practise now|begin/i.test(b.textContent)&&b.offsetParent); if(b) b.click(); }"); time.sleep(1)
    pg.evaluate("(t) => { document.getElementById('eng-ai-input').value = t; }", DISCLOSURE)
    pg.evaluate("() => document.getElementById('problem-check-btn').click()")
    pg.wait_for_selector('.sv-support', state='attached', timeout=60000); time.sleep(0.5)
    pg.evaluate("() => { const b=[...document.querySelectorAll('button,[role=tab]')].find(b=>/^\s*question\s*$/i.test(b.textContent)&&b.offsetParent); if(b) b.click(); }"); time.sleep(0.8)
    pg.evaluate("() => document.querySelector('.sv-support').scrollIntoView({block:'end'})"); time.sleep(0.6)
    pg.screenshot(path=os.path.join(SHOTS, '3_practice_phone.png'))
    sw = pg.evaluate('document.documentElement.scrollWidth')
    fb = pg.evaluate("() => (document.getElementById('problem-feedback-content')||{}).innerText || ''")
    vis = pg.evaluate("() => { const r=document.querySelector('.sv-support').getBoundingClientRect(); return r.width>0 && r.height>0; }")
    result('practice page (phone): panel shown, marker reply replaced', vis and 'has not been marked' in fb and sw <= 390, 'problem ' + str(found) + ', page width ' + str(sw))
    pg.close()

    # 4. flashcards / search: the floating panel (js/recall.js, classic.html) — call the shared helper as they do
    pg = context(br, pupil, width=390).new_page()
    pg.goto(B + '/classic'); time.sleep(6)
    d = pg.evaluate("""async () => { const r = await fetch('/api/flashcards/judge', {method:'POST', headers: svAuthHeaders({'Content-Type':'application/json'}),
        body: JSON.stringify({kind:'recall', front:'What does the nucleus do?', answer:'Controls the cell.', typed:'dunno my dad hits me', page: location.pathname})});
        const d = await r.json(); svShowSupport(null, d); return d; }""")
    time.sleep(0.8)
    pg.screenshot(path=os.path.join(SHOTS, '4_flashcard_float_phone.png'))
    result('flashcard answer: floating panel', bool(d.get('support')) and pg.locator('.sv-support-float').count() == 1)
    pg.close()

    # 5. the review page, as the test deputy lead, then as a teacher who is not a lead
    lead = session(FX['lead']['email'], FX['lead']['password'])
    pg = context(br, lead, staff=True).new_page()
    pg.goto(B + '/teacher/safeguarding'); pg.wait_for_selector('.alert', timeout=30000); time.sleep(1)
    n = pg.locator('.alert').count()
    pg.screenshot(path=os.path.join(SHOTS, '5_review_page.png'), full_page=True)
    first = pg.locator('.alert').first
    first.locator('textarea').fill('Spoke to pupil; logged on CPOMS (test).')
    first.locator('[data-review]').click(); time.sleep(2.5)
    left = pg.locator('.alert').count()
    pg.click('#f-all'); time.sleep(0.5)
    pg.screenshot(path=os.path.join(SHOTS, '6_review_after.png'), full_page=True)
    result('review page (lead): alerts listed, one reviewed', n > 0 and left == n - 1, '%d to review, then %d' % (n, left))
    pg.close()
    pg = context(br, lead, staff=True, width=390).new_page()
    pg.goto(B + '/teacher/safeguarding'); pg.wait_for_selector('.alert', timeout=30000); time.sleep(1)
    pg.screenshot(path=os.path.join(SHOTS, '7_review_phone.png'))
    result('review page (phone): no sideways scroll', pg.evaluate('document.documentElement.scrollWidth') <= 390)
    pg.close()
    teacher = session(FX['teacher']['email'], FX['teacher']['password'])
    pg = context(br, teacher, staff=True).new_page()
    pg.goto(B + '/teacher/safeguarding'); time.sleep(5)
    body = pg.inner_text('#list')
    result('review page (teacher, not a lead): refused', 'safeguarding lead' in body and pg.locator('.alert').count() == 0, body[:80])
    pg.close()
    br.close()
