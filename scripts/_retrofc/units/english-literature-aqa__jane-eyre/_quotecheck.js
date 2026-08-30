const fs = require('fs');
const RAW = fs.readFileSync('C:/Users/tshau/Documents/Study Vault/scripts/_retrofc/_texts/jane_eyre_gutenberg.txt', 'utf8');

// Split into chapters
const lines = RAW.split(/\r?\n/);
const chapters = []; // {n, start}
lines.forEach((l, i) => {
  const m = l.trim().match(/^CHAPTER ([IVXL]+)$/);
  if (m) chapters.push({ roman: m[1], line: i });
});
function rom(r) { const v = { I: 1, V: 5, X: 10, L: 50, C: 100 }; let t = 0; for (let i = 0; i < r.length; i++) { const a = v[r[i]], b = v[r[i + 1]]; t += (b && a < b) ? -a : a; } return t; }
chapters.forEach(c => c.n = rom(c.roman));
console.log('chapters found:', chapters.length, chapters.slice(0, 3).map(c => c.n), '...', chapters.slice(-2).map(c => c.n));

// Build normalised full text with an index->chapter map
function norm(s) {
  return s
    .replace(/[\u2018\u2019\u02BC\u2032]/g, "'")
    .replace(/[\u201C\u201D\u2033]/g, '"')
    .replace(/[\u2014\u2013\u2012\u2010\u2212]/g, '-')
    .replace(/[\u00A0\u2007\u202F]/g, ' ')
    .replace(/\s+/g, ' ')
    .toLowerCase();
}
// chapter-wise normalised bodies
const bodies = [];
for (let i = 0; i < chapters.length; i++) {
  const start = chapters[i].line;
  const end = i + 1 < chapters.length ? chapters[i + 1].line : lines.length;
  bodies.push({ n: chapters[i].n, text: norm(lines.slice(start, end).join(' ')) });
}

// loosen: drop punctuation entirely for a second pass
function loose(s) { return s.replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim(); }

const Q = [
  ['A1', 'Do you think, because I am poor, obscure, plain, and little, I am soulless and heartless? You think wrong!', 23],
  ['A2', 'I have as much soul as you', 23],
  ['A3', 'full as much heart', 23],
  ['B', 'I am no bird; and no net ensnares me: I am a free human being with an independent will', 23],
  ['C1', 'I was a discord in Gateshead Hall', null],
  ['C2', 'I was like nobody there', null],
  ['D', 'Women are supposed to be very calm generally: but women feel just as men feel; they need exercise for their faculties, and a field for their efforts', 12],
  ['E1', 'You have no business to take our books', 1],
  ['E2', 'you are a dependent', 1],
  ['E3', 'you are a dependant', 1],
  ['F', 'Me, she had dispensed from joining the group', 1],
  ['G1', 'You are like a murderer', null],
  ['G2', 'you are like a slave-driver', null],
  ['G3', 'you are like the Roman emperors', null],
  ['H', 'I am glad you are no relation of mine: I will never call you aunt again as long as I live', 4],
  ['I', 'the strangest sense of freedom', 4],
  ['J', 'splendidly attired in velvet, silk, and furs', 7],
  ['K', 'you may indeed feed their vile bodies, but you little think how you starve their immortal souls', 7],
  ['L', 'dark face, with stern features and a heavy brow', 12],
  ['M', 'you have rather the look of another world', 13],
  ['N', 'a curious laugh; distinct, formal, mirthless', 11],
  ['N2', 'distinct, formal, mirthless', 11],
  ['O1', 'Do you think me handsome?', 14],
  ['O2', 'No, sir', 14],
  ['P', 'the great horse-chestnut at the bottom of the orchard had been struck by lightning in the night, and half of it split away', 23],
  ['Q1', 'grovelled, seemingly, on all fours', 26],
  ['Q2', 'it snatched and growled like some strange wild animal', 26],
  ['R', 'I care for myself. The more solitary, the more friendless, the more unsustained I am, the more I will respect myself', 27],
  ['S', 'Laws and principles are not for the times when there is no temptation: they are for such moments as this', 27],
  ['T', 'God and nature intended you for a missionary\u2019s wife', 34],
  ['U', 'If I join St. John, I abandon half myself', 34],
  ['V', 'iron shroud', 34],
  ['W', 'Jane! Jane! Jane!', 35],
  ['X', 'blackened ruin', 36],
  ['Y', 'caged eagle, whose gold-ringed eyes cruelty has extinguished', 37],
  ['Z', 'Reader, I married him', 38],
  ['AA1', 'I am my husband\u2019s life as fully as he is mine', 38],
  ['AA2', 'To be together is for us to be at once as free as in solitude, as gay as in company', 38],
  ['AB1', 'lark', null],
  ['AB2', 'eager bird', null],
  ['AC', 'quaker', null],
  ['AD', 'typhus', 9],
  ['AE1', 'demon', null],
  ['AE2', 'lunatic', null],
  ['AF', 'left hand', null],
  ['AG', 'I did what I had never done before', null],
];

for (const [id, qRaw, expect] of Q) {
  const q = norm(qRaw);
  const ql = loose(q);
  const exact = bodies.filter(b => b.text.includes(q)).map(b => b.n);
  const lo = bodies.filter(b => loose(b.text).includes(ql)).map(b => b.n);
  const hits = exact.length ? exact : lo;
  const kind = exact.length ? 'EXACT' : (lo.length ? 'LOOSE' : 'NONE ');
  let verdict = 'ok';
  if (!hits.length) verdict = '*** NOT FOUND ***';
  else if (expect && !hits.includes(expect)) verdict = `*** CH MISMATCH: claimed ${expect}, actual ${hits.join(',')} ***`;
  console.log(`${id}\t${kind}\tch=[${hits.slice(0, 8).join(',')}]${hits.length > 8 ? '+' : ''}\t${verdict}\t"${qRaw.slice(0, 62)}"`);
}
