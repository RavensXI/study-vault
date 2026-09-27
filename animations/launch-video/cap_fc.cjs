const { browser, page, go } = require('./common.cjs');
const S = 'https://www.studyvault.co.uk', O = 'captures/final/';
(async () => {
  const b = await browser(); const p = await page(b, 390, 844, 3);
  await go(p, S + '/lesson/history-aqa/conflict-tension-inter-war/7?open=cards'); await p.waitForTimeout(2500);
  let front = '';
  for (let k = 0; k < 16; k++) {
    front = (await p.evaluate(() => document.getElementById('fc-front-text').innerText)).trim();
    if (front === 'Lytton Report') break;
    await p.click('text=Skip'); await p.waitForTimeout(900);
  }
  console.log('front:', front);
  const ans = "the League's report that said Japan's invasion of Manchuria wasn't justified";
  const steps = 10;
  await p.click('#fc-typed-in');
  for (let i = 0; i <= steps; i++) {
    const n = Math.round(ans.length * i / steps);
    await p.fill('#fc-typed-in', ans.slice(0, n));
    await p.waitForTimeout(120);
    await p.screenshot({ path: O + `fc-type-${String(i).padStart(2, '0')}.png` });
  }
  await p.click('#fc-check');
  for (let i = 0; i < 12; i++) { await p.waitForTimeout(250); await p.screenshot({ path: O + `fc-after-${String(i).padStart(2, '0')}.png` }); }
  await p.waitForTimeout(1500); await p.screenshot({ path: O + 'fc-verdict.png' });
  console.log(await p.evaluate(() => (document.getElementById('fc-verdict-head') || {}).innerText + ' | ' + (document.getElementById('fc-verdict-line') || {}).innerText));
  await b.close();
})();
