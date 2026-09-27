const { chromium } = require('playwright');
const INIT = `try{['sv-lesson-tour-v2','sv-lesson-tutorial-done','sv-reader-tour-v1','sv-highlight-tutorial-done','sv-dash-tour-v1','sv-flashcard-tutorial-done','sv_collapsible_hint'].forEach(function(k){localStorage.setItem(k,'1')});localStorage.setItem('studyvault-cookie-consent','declined');}catch(e){}`;
async function browser() { return chromium.launch({ channel: 'chrome' }); }
async function page(b, w, h, dsf) {
  const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dsf || 1, isMobile: w < 600, hasTouch: w < 600 });
  await c.addInitScript(INIT);
  const p = await c.newPage();
  p.on('pageerror', e => console.log('  pageerror', String(e).slice(0, 120)));
  return p;
}
async function go(p, u) { try { await p.goto(u, { waitUntil: 'networkidle', timeout: 60000 }); } catch (e) { console.log('  goto', e.message.slice(0, 80)); } await p.waitForTimeout(2500); }
module.exports = { browser, page, go, INIT };
