const { browser, page, go } = require('./common.cjs');
const S = 'https://www.studyvault.co.uk';
(async () => {
  const b = await browser();
  let p = await page(b, 1440, 900);
  await go(p, S + '/practice/maths-aqa/number/2'); await p.screenshot({ path: 'captures/explore/practice-maths.png' });
  await go(p, S + '/practice/spanish-aqa/people-and-lifestyle/1'); await p.screenshot({ path: 'captures/explore/practice-spanish.png' });
  await go(p, S + '/practice/english-language-aqa/paper-1-reading/2'); await p.screenshot({ path: 'captures/explore/practice-englang.png' });
  await go(p, S + '/lesson/history-aqa/conflict-tension-first-world-war/13'); 
  const strip = await p.$('.sv-embed-strip'); if (strip) { await strip.scrollIntoViewIfNeeded(); await p.waitForTimeout(800); }
  await p.screenshot({ path: 'captures/explore/widget-strip.png' });
  await go(p, S + '/browse/history-aqa'); await p.screenshot({ path: 'captures/explore/browse.png' });
  await go(p, S + '/lesson/history-aqa/conflict-tension-inter-war/7');
  await p.screenshot({ path: 'captures/explore/lesson-clean.png' });
  const fl = await p.$('text=Flashcards'); if (fl) { await fl.click(); await p.waitForTimeout(2000); await p.screenshot({ path: 'captures/explore/flashcards.png' }); }
  await b.close();
})();
