const { browser, page, go } = require('./common.cjs');
const O = 'captures/final/';
(async () => {
  const b = await browser(); const p = await page(b, 1440, 900, 2);
  await go(p, 'https://www.studyvault.co.uk/lesson/history-aqa/conflict-tension-inter-war/7');
  // open practice questions via the sidebar tile
  await p.evaluate(() => { const m = document.querySelector('.pq-modal'); if (m) m.hidden = false; });
  await p.waitForTimeout(1500);
  for (let k = 0; k < 20; k++) {
    const t = await p.evaluate(() => document.getElementById('practice-text').innerText);
    if (/Lytton Report/.test(t) && /identify two findings/i.test(t)) break;
    await p.evaluate(() => document.getElementById('practice-new').click()); await p.waitForTimeout(400);
  }

  await p.waitForTimeout(600);
  await p.screenshot({ path: O + 'ai-0.png' });
  const ans = "The report found that Japan's military action on 18–19 September 1931 was not legitimate self-defence, so the invasion of Manchuria could not be justified by the Mukden Incident. It also found that Manchukuo was not the result of a genuine independence movement but 'an instrument of Japanese policy' — in other words, a puppet state.";
  const steps = 12;
  for (let i = 1; i <= steps; i++) { await p.fill('#practice-answer', ans.slice(0, Math.round(ans.length * i / steps))); await p.waitForTimeout(80); await p.screenshot({ path: O + `ai-type-${String(i).padStart(2, '0')}.png` }); }
  await p.evaluate(() => document.getElementById('practice-ai-mark').click());
  const t0 = Date.now();
  for (let k = 0; k < 60; k++) {
    await p.waitForTimeout(500);
    const done = await p.evaluate(() => { const f = document.getElementById('practice-ai-feedback'); return f && !f.hidden && (document.getElementById('practice-ai-feedback-body').innerText || '').length > 40; });
    if (k % 2 === 0) await p.screenshot({ path: O + `ai-wait-${String(k).padStart(2, '0')}.png` });
    if (done) break;
  }
  console.log('marked in', (Date.now() - t0) / 1000, 's');
  await p.waitForTimeout(1500);
  await p.evaluate(() => document.getElementById('practice-ai-feedback').scrollIntoView({ block: 'center' }));
  await p.waitForTimeout(600);
  await p.screenshot({ path: O + 'ai-result.png' });
  console.log((await p.evaluate(() => document.getElementById('practice-ai-feedback-body').innerText)).slice(0, 600));
  await b.close();
})();
