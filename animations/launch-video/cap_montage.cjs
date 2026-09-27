const { browser, page, go } = require('./common.cjs');
const list = require('./montage.json');
(async () => {
  const b = await browser(); const p = await page(b, 390, 844, 3);
  for (const [sub, unit, n] of list) {
    await go(p, `https://www.studyvault.co.uk/lesson/${sub}/${unit}/${n}`);
    await p.evaluate(() => document.querySelectorAll('[class*=countdown] .close, .exam-countdown-close').forEach(e => e.click()));
    await p.screenshot({ path: `captures/final/mont-${sub}.png` });
  }
  await b.close();
})();
