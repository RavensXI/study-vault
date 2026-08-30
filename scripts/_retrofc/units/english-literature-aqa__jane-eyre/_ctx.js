const fs = require('fs');
const RAW = fs.readFileSync('C:/Users/tshau/Documents/Study Vault/scripts/_retrofc/_texts/jane_eyre_gutenberg.txt', 'utf8');
const lines = RAW.split(/\r?\n/);
const chapters = [];
lines.forEach((l, i) => { const m = l.trim().match(/^CHAPTER ([IVXL]+)\b/); if (m) chapters.push({ roman: m[1], line: i, head: l.trim() }); });
function rom(r) { const v = { I: 1, V: 5, X: 10, L: 50 }; let t = 0; for (let i = 0; i < r.length; i++) { const a = v[r[i]], b = v[r[i + 1]]; t += (b && a < b) ? -a : a; } return t; }
chapters.forEach(c => c.n = rom(c.roman));
console.log('CHAPTERS:', chapters.length, 'last heads:', chapters.slice(-3).map(c => c.n + ':' + c.head).join(' | '));

function norm(s) { return s.replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/[\u2014\u2013]/g, '-').replace(/\s+/g, ' '); }
const bodies = chapters.map((c, i) => ({ n: c.n, text: norm(lines.slice(c.line, i + 1 < chapters.length ? chapters[i + 1].line : lines.length).join(' ')) }));

const NEEDLES = process.argv.slice(2);
for (const nd of NEEDLES) {
  const [needle, pre, post] = nd.split('||');
  const b4 = pre ? +pre : 220, af = post ? +post : 320;
  console.log('\n########## ' + needle + ' ##########');
  let found = 0;
  for (const b of bodies) {
    let idx = b.text.toLowerCase().indexOf(needle.toLowerCase());
    while (idx >= 0) {
      console.log(`--- CH ${b.n} ---\n...${b.text.slice(Math.max(0, idx - b4), idx + needle.length + af)}...`);
      found++;
      if (found > 6) break;
      idx = b.text.toLowerCase().indexOf(needle.toLowerCase(), idx + 1);
    }
    if (found > 6) break;
  }
  if (!found) console.log('NOT FOUND');
}
