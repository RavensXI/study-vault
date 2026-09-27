const { browser, page, go } = require('./common.cjs');
const O = 'captures/final/';
(async () => {
  const b = await browser(); const p = await page(b, 1440, 900, 2);
  await go(p, 'https://www.studyvault.co.uk/lesson/history-aqa/conflict-tension-first-world-war/13');
  await p.evaluate(() => { const s = document.querySelector('.sv-embed-strip'); s.scrollIntoView({ block: 'center' }); });
  await p.waitForTimeout(800); await p.screenshot({ path: O + 'wd-strip.png' });
  await p.evaluate(() => { const s = document.querySelector('.sv-embed-strip'); const b = s.querySelector('button,a'); b.click(); });
  await p.waitForTimeout(3000); await p.screenshot({ path: O + 'wd-open.png' });
  const clickT = async t => { const l = p.getByText(t, { exact: false }).last(); await l.click({ timeout: 5000 }).catch(e => console.log('click fail', t, e.message.slice(0, 60))); };
  const q = await p.evaluate(() => document.body.innerText.match(/Where does this leave (\w+)/)[1]);
  console.log('round side:', q);
  await clickT(q === 'Germany' ? 'Closer to losing' : 'Closer to winning'); await p.waitForTimeout(500); await p.screenshot({ path: O + 'wd-a1.png' });
  const fact = await p.evaluate(() => { const o = [...document.querySelectorAll('button.t-opt')].slice(3); const pick = o.find(x => /had to|before/i.test(x.innerText)) || o.find(x => !/^The (tonnage|ground)/.test(x.innerText)) || o[0]; pick.click(); return pick.innerText; });
  console.log('fact:', fact);
  await p.waitForTimeout(500); await p.screenshot({ path: O + 'wd-a2.png' });
  await p.evaluate(() => document.querySelector('button.t-go').click());
  for (let k = 0; k < 6; k++) { await p.waitForTimeout(200); await p.screenshot({ path: O + 'wd-after-' + k + '.png' }); }
  await p.waitForTimeout(1200); await p.screenshot({ path: O + 'wd-result.png' });
  const info = await p.evaluate(() => { const f = document.querySelector('iframe'); return f ? f.src : [...document.querySelectorAll('[class*=widget],[class*=embed]')].map(e => e.className).slice(0, 10).join(' | '); });
  console.log(info);
  await b.close();
})();
