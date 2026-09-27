const { browser, page, go } = require('./common.cjs');
const O = 'captures/final/';
const which = process.argv[2];
const prep = async (p, url) => {
  await go(p, url);
  await p.evaluate(() => [...document.querySelectorAll('button')].filter(b => /Got it|let.s practi/i.test(b.innerText)).forEach(b => b.click()));
  await p.waitForTimeout(1200);
  await p.evaluate(() => document.getElementById('learn-back-practice-btn') && document.getElementById('learn-back-practice-btn').click());
  await p.waitForTimeout(1800);
  await p.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('[class*=tour],[class*=coach]').forEach(e => e.remove());
    [...document.querySelectorAll('div,section')].filter(e => /^Refer back to the method card/.test((e.innerText || '').trim()) && e.offsetHeight < 300).forEach(e => e.remove()); });
  await p.waitForTimeout(500);
  return p.evaluate(() => practiceState.currentIndex);
};
(async () => {
  const b = await browser(); const p = await page(b, 1440, 900, 2);
  if (which === 'es') {
    const i = await prep(p, 'https://www.studyvault.co.uk/practice/spanish-aqa/people-and-lifestyle/1');
    await p.screenshot({ path: O + 'es-0.png' });
    const n = await p.evaluate(i => window._problemBank.bronze[i].pairs.length, i);
    for (let L = 0; L < n; L++) {
      await p.evaluate(L => document.querySelector(`.vm-left[data-pair-id="${L}"]`).click(), L); await p.waitForTimeout(150);
      await p.screenshot({ path: O + `es-p${L}-sel.png` });
      await p.evaluate(L => document.querySelector(`.vm-right[data-pair-id="${L}"]`).click(), L);
      await p.waitForTimeout(200); await p.screenshot({ path: O + `es-p${L}-ok.png` });
      await p.waitForTimeout(450); await p.screenshot({ path: O + `es-p${L}-done.png` });
    }
    await p.waitForTimeout(900); await p.screenshot({ path: O + 'es-end.png' });
  }
  if (which === 'en') {
    const i = await prep(p, 'https://www.studyvault.co.uk/practice/english-language-aqa/paper-1-reading/1');
    await p.screenshot({ path: O + 'en-0.png' });
    const n = await p.evaluate(() => document.querySelectorAll('.tl-stmt').length);
    for (let r = 0; r < n; r++) {
      await p.evaluate(([i, r]) => { const q = window._problemBank.bronze[i]; const row = document.querySelectorAll('.tl-stmt')[r];
        const txt = row.querySelector('.stmt-text').innerText.trim(); const st = q.statements.find(s => s.text.trim() === txt);
        const btn = [...row.querySelectorAll('.tl-btn')].find(bt => (bt.title || '').toLowerCase() === String(st.correct).toLowerCase()); btn.click(); }, [i, r]);
      await p.waitForTimeout(150); await p.screenshot({ path: O + `en-r${r}.png` });
    }
    await p.evaluate(() => document.getElementById('problem-check-btn').click());
    for (let k = 0; k < 6; k++) { await p.waitForTimeout(180); await p.screenshot({ path: O + `en-after-${k}.png` }); }
  }
  await b.close();
})();
