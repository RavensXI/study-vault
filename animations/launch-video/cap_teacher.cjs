const { browser, page, go } = require('./common.cjs');
const O = 'captures/final/';
(async () => {
  const b = await browser(); const p = await page(b, 1440, 900, 2);
  await go(p, 'http://127.0.0.1:8931/teacher/classes.html?fixture=rich');
  await p.waitForTimeout(3000);
  await p.screenshot({ path: O + 'teach-top.png' });
  await p.screenshot({ path: O + 'teach-full.png', fullPage: true });
  await p.getByText('Questions', { exact: true }).first().click(); await p.waitForTimeout(1500);
  await p.screenshot({ path: O + 'teach-questions.png' });
  await p.getByText('Markbook', { exact: true }).first().click(); await p.waitForTimeout(1500);
  await p.screenshot({ path: O + 'teach-markbook.png' });
  await b.close();
})();
