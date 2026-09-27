const { browser, page, go } = require('./common.cjs');
const O = 'captures/final/';
const answers = JSON.parse(process.argv[2] || '[]');
(async () => {
  const b = await browser(); const p = await page(b, 1440, 900, 2);
  await go(p, 'https://www.studyvault.co.uk/practice/maths-aqa/number/5');
  await p.evaluate(() => document.getElementById('learn-back-practice-btn').click());
  await p.waitForTimeout(1800);
  await p.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('[class*=tour],[class*=coach]').forEach(e => e.remove()); });
  await p.waitForTimeout(500);
  await p.screenshot({ path: O + 'maths-0.png' });
  let f = 0;
  for (let s = 0; s < answers.length; s++) {
    const inp = p.locator('input[type=text]:visible, input[type=number]:visible, input:not([type]):visible').last();
    await inp.focus();
    const a = String(answers[s]);
    for (let k = 0; k < a.length; k++) { await p.keyboard.type(a[k]); await p.waitForTimeout(60); await p.screenshot({ path: O + `maths-s${s}-t${k}.png` }); }
    await p.keyboard.press('Enter');
    for (let k = 0; k < 6; k++) { await p.waitForTimeout(160); await p.screenshot({ path: O + `maths-s${s}-a${k}.png` }); }
    await p.waitForTimeout(600);
    console.log('STEP', s, (await p.evaluate(() => (document.querySelector('.content-view:not(.hidden-left)')||document.body).innerText)).replace(/\s+/g, ' ').slice(0, 400));
  }
  await p.screenshot({ path: O + 'maths-end.png' });
  await b.close();
})();
