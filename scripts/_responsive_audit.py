# -*- coding: utf-8 -*-
"""Responsive audit of every student-facing page type at common viewports.

Loads each page in Playwright Chromium at phone / tablet / laptop / desktop sizes,
measures horizontal overflow, elements poking past the viewport, sub-11px text and
small tap targets, and saves a screenshot per page x viewport.

    python scripts/_responsive_audit.py [--base http://127.0.0.1:8904] [--out DIR] [--only picker,lesson]

Output: <out>/report.md + <out>/<page>__<viewport>.png
"""
import argparse, json, os, sys, time
from playwright.sync_api import sync_playwright

PAGES = {
    'welcome-landing': '/welcome',
    'welcome-picker':  '/welcome?view=picker',
    'welcome-year':    '/welcome?view=year',
    'welcome-boards':  '/welcome?view=boards&picked=maths,lang,lit,science,history,music&boards=maths:edexcel,science:aqa',
    'welcome-tier':    '/welcome?view=tier&picked=maths,lang,lit,science,history&boards=maths:edexcel,science:aqa,history:aqa,lang:aqa,lit:aqa',
    'welcome-topics':  '/welcome?view=topics&picked=maths,lang,lit,science,history&boards=history:aqa,lit:aqa',
    'welcome-save':    '/welcome?view=save&picked=maths,lang,lit,science&boards=maths:edexcel',
    'classic':         '/classic?picked=maths,lang,lit,science,history,music&boards=maths:edexcel,history:aqa,music:aqa',
    'desk':            '/desk?picked=maths,lang,lit,science,history,music&boards=maths:edexcel,history:aqa,music:aqa',
    'browse-subject':  '/browse/history-aqa',
    'browse-unit':     '/browse/history-aqa/germany-democracy-dictatorship',
    'browse-boards':   '/browse/history',
    'lesson-article':  '/lesson/history-aqa/germany-democracy-dictatorship/1',
    'lesson-listening':'/lesson/music-edexcel/aos3-stage-and-screen/3',
    'practice-maths':  '/practice/maths-edexcel/number/1',
    'practice-lang':   '/practice/french-aqa/people-and-lifestyle/1',
    'practice-sci':    '/practice/science-aqa/physics-calculations/1',
    'guide-hub':       '/guide/history-aqa/exam-technique',
    'exams':           '/exams',
    'revise':          '/revise',
    'faq':             '/faq',
    'about':           '/about',
    'shorts':          '/shorts',
    'join':            '/join',
}
VIEWPORTS = {
    'phone-s':  dict(viewport={'width':360,'height':740},  device_scale_factor=3, is_mobile=True,  has_touch=True),
    'iphone':   dict(viewport={'width':390,'height':844},  device_scale_factor=3, is_mobile=True,  has_touch=True),
    'phone-l':  dict(viewport={'width':430,'height':932},  device_scale_factor=3, is_mobile=True,  has_touch=True),
    'tablet-p': dict(viewport={'width':768,'height':1024}, device_scale_factor=2, is_mobile=True,  has_touch=True),
    'tablet-l': dict(viewport={'width':1024,'height':768}, device_scale_factor=2, is_mobile=True,  has_touch=True),
    'laptop':   dict(viewport={'width':1366,'height':768}, device_scale_factor=1),
    'desktop':  dict(viewport={'width':1920,'height':1080},device_scale_factor=1),
}
METRICS_JS = r"""
() => {
  const iw = innerWidth, de = document.documentElement;
  const sw = Math.max(de.scrollWidth, document.body ? document.body.scrollWidth : 0);
  const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const offenders = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (!(r.width > 0) || r.right <= iw + 2) continue;
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed' || cs.visibility === 'hidden' || cs.display === 'none' || cs.opacity === '0') continue;
    offenders.push({ sel: name(el), right: Math.round(r.right), w: Math.round(r.width) });
    if (offenders.length >= 8) break;
  }
  let small = 0; const tiny = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = walker.nextNode())) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el) continue; const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 11) { small++; if (tiny.length < 5) tiny.push(name(el) + ':' + fs.toFixed(1)); }
  }
  let tap = 0; const tapEls = [];
  for (const el of document.querySelectorAll('a,button,[role=button],input:not([type=hidden]),select')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (r.height < 30 || r.width < 30) { tap++; if (tapEls.length < 5) tapEls.push(name(el) + ':' + Math.round(r.width) + 'x' + Math.round(r.height)); }
  }
  return { iw, sw, overflow: sw - iw, zoom: getComputedStyle(document.body).zoom, offenders, small, tiny, tap, tapEls, h: de.scrollHeight };
}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8904')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(__file__), '_responsive_audit'))
    ap.add_argument('--only', default='')
    ap.add_argument('--vp', default='')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    pages = {k: v for k, v in PAGES.items() if not a.only or any(s in k for s in a.only.split(','))}
    vps = {k: v for k, v in VIEWPORTS.items() if not a.vp or k in a.vp.split(',')}
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vpn, vp in vps.items():
          for name, path in pages.items():
            # a fresh context per page: a context reused across pages served stale stylesheets
            ctx = browser.new_context(**vp)
            # a student who has set up: the planner, dashboards and lesson chrome need picks to render
            ctx.add_init_script("""try{ if(!localStorage.getItem('sv-welcome')){ localStorage.setItem('sv-welcome', JSON.stringify({picked:['maths','lang','lit','science','history','music'],boards:{maths:'edexcel',lang:'aqa',lit:'aqa',science:'aqa',history:'aqa',music:'aqa'},topics:{},meta:{}})); localStorage.setItem('studyvault-exam-year','2027'); localStorage.setItem('sv-welcome-decision','1'); } }catch(e){}""")
            pg = ctx.new_page()
            if True:
                url = a.base + path + ('&' if '?' in path else '?') + 'v=' + str(int(time.time()))
                try:
                    pg.goto(url, wait_until='load', timeout=45000)
                    pg.wait_for_timeout(2500)
                    m = pg.evaluate(METRICS_JS)
                    shot = os.path.join(a.out, f'{name}__{vpn}.png')
                    pg.screenshot(path=shot, full_page=True, clip=None)
                except Exception as e:
                    m = {'error': str(e)[:120]}
                m.update(page=name, vp=vpn)
                rows.append(m)
                sys.stdout.write(f"{name:18} {vpn:9} overflow={m.get('overflow','?'):>5} small={m.get('small','?'):>3} tap={m.get('tap','?'):>3} {m.get('error','')}\n"); sys.stdout.flush()
            ctx.close()
        browser.close()
    with open(os.path.join(a.out, 'report.json'), 'w', encoding='utf-8') as f: json.dump(rows, f, indent=1)
    lines = ['| page | viewport | overflow px | offenders | sub-11px text | small taps |', '|---|---|---|---|---|---|']
    for r in rows:
        if 'error' in r: lines.append(f"| {r['page']} | {r['vp']} | ERROR | {r['error']} | | |"); continue
        off = '; '.join(f"{o['sel']} ({o['right']})" for o in r['offenders'][:3])
        lines.append(f"| {r['page']} | {r['vp']} | {r['overflow']} | {off} | {r['small']} {' '.join(r['tiny'][:2])} | {r['tap']} {' '.join(r['tapEls'][:2])} |")
    with open(os.path.join(a.out, 'report.md'), 'w', encoding='utf-8') as f: f.write('\n'.join(lines))
    print('wrote', os.path.join(a.out, 'report.md'))

if __name__ == '__main__':
    main()
