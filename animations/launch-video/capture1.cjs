const { browser, page, go } = require('./common.cjs');
const S = 'https://www.studyvault.co.uk', O = 'captures/final/';
(async () => {
  const b = await browser();
  // desktop home, subjects, lesson
  let p = await page(b, 1440, 900, 2);
  await go(p, S + '/welcome'); await p.screenshot({ path: O + 'home-d.png' });
  await go(p, S + '/subjects'); await p.screenshot({ path: O + 'subjects-d.png' }); await p.screenshot({ path: O + 'subjects-d-full.png', fullPage: true });
  await go(p, S + '/lesson/history-aqa/conflict-tension-inter-war/7'); await p.screenshot({ path: O + 'lesson-d-top.png' });
  await p.evaluate(() => window.scrollTo(0, 560)); await p.waitForTimeout(800); await p.screenshot({ path: O + 'lesson-d-mid.png' });
  const pod = await p.$('text=Lesson Podcast'); if (pod) { await pod.click(); await p.waitForTimeout(1200); await p.screenshot({ path: O + 'lesson-d-podcast.png' }); }
  await p.context().close();
  // phone lesson + dashboard
  p = await page(b, 390, 844, 3);
  await go(p, S + '/lesson/history-aqa/conflict-tension-inter-war/7'); await p.screenshot({ path: O + 'lesson-p-top.png' });
  await go(p, S + '/classic?demo=amira'); await p.screenshot({ path: O + 'dash-p.png' });
  await go(p, S + '/welcome'); await p.screenshot({ path: O + 'home-p.png' });
  await p.context().close();
  await b.close();
})();
