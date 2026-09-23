const fs = require('fs');
const path = require('path');
const { supabase } = require('./pipeline/_lib/supabase');

/**
 * What search engines read: the sitemaps and a plain-HTML subject directory.
 *
 *   /sitemap.xml              -> ?kind=index     sitemap index (pages + one sitemap per subject)
 *   /sitemaps/pages.xml       -> ?kind=sitemap&name=pages
 *   /sitemaps/{subject}.xml   -> ?kind=sitemap&name={subject}
 *   /subjects                 -> ?kind=subjects             every subject, as links
 *   /subjects/{subject}       -> ?kind=subjects&slug=...    its units and lessons, as links
 *   /lesson/..., /practice/..., /browse/...  -> ?kind=page&t=...   the page's own HTML shell with
 *        its real title, description, canonical and share tags written into <head>, so a
 *        crawler or a link preview that runs no JavaScript still sees what the page is.
 *        The loaders fill the page exactly as before.
 *
 * Free tier only: school_id NULL, subject live, lesson live. School content and anything
 * awaiting review never appears here. Guides are left out: they send a visitor with no saved
 * subjects back to the home page, so a crawler would only ever see the home page.
 */
const SITE = 'https://www.studyvault.co.uk';
const STATIC_PAGES = ['/welcome', '/subjects', '/about', '/faq', '/teach', '/copyright.html', '/privacy.html'];

function esc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function day(ts) { return ts ? String(ts).slice(0, 10) : null; }

async function all(build) {
  const out = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await build().range(from, from + 999);
    if (error) throw error;
    out.push(...data);
    if (data.length < 1000) return out;
  }
}

// Live free-tier subjects that have at least one live lesson.
async function subjects() {
  const [subs, units, live] = await Promise.all([
    all(() => supabase.from('subjects').select('id, slug, name, exam_board, settings')
      .is('school_id', null).eq('status', 'live').order('name').order('exam_board').order('id')),
    all(() => supabase.from('units').select('id, subject_id').order('id')),
    all(() => supabase.from('lessons').select('unit_id').eq('status', 'live').order('id'))
  ]);
  const subjectOf = new Map(units.map(u => [u.id, u.subject_id]));
  const withLessons = new Set(live.map(l => subjectOf.get(l.unit_id)));
  return subs.filter(s => withLessons.has(s.id));
}

// A subject's revision-technique guides (the hub first). Exam-technique guides were retired.
async function guides(subject) {
  const rows = await all(() => supabase.from('guide_pages').select('slug, title, sort_order')
    .eq('subject_id', subject.id).eq('guide_type', 'revision-technique').order('sort_order').order('slug'));
  if (!rows.some(r => r.slug === 'index')) return [];
  const hub = `/guide/${subject.slug}/revision-technique`;
  return [{ path: hub, title: 'Revision techniques' }]
    .concat(rows.filter(r => r.slug !== 'index').map(r => ({ path: hub + '/' + r.slug, title: r.title })));
}

// One subject's units, each with its live lessons in order. Units with none are dropped.
async function outline(subject) {
  const units = await all(() => supabase.from('units').select('id, slug, name, subtitle, sort_order')
    .eq('subject_id', subject.id).order('sort_order'));
  if (!units.length) return [];
  const lessons = await all(() => supabase.from('lessons').select('unit_id, lesson_number, title, updated_at')
    .in('unit_id', units.map(u => u.id)).eq('status', 'live').order('lesson_number'));
  const s = subject.settings || {};
  const practiceUnits = s.practice_units || [];
  return units.map(u => {
    const kind = (s.format === 'practice' || practiceUnits.indexOf(u.slug) >= 0) ? 'practice' : 'lesson';
    const ls = lessons.filter(l => l.unit_id === u.id).map(l => ({
      n: l.lesson_number, title: l.title, lastmod: day(l.updated_at),
      path: `/${kind}/${subject.slug}/${u.slug}/${l.lesson_number}`
    }));
    return { slug: u.slug, name: u.name, subtitle: u.subtitle, path: `/browse/${subject.slug}/${u.slug}`, lessons: ls };
  }).filter(u => u.lessons.length);
}

function newest(dates) { return dates.filter(Boolean).sort().pop() || null; }

function urlset(entries) {
  return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    entries.map(e => `  <url><loc>${esc(SITE + e.path)}</loc>${e.lastmod ? `<lastmod>${e.lastmod}</lastmod>` : ''}</url>`).join('\n') +
    '\n</urlset>\n';
}

function subjectLabel(s) { return s.exam_board ? `${s.name} (${s.exam_board})` : s.name; }

function page({ title, description, path, body }) {
  return `<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  <link rel="canonical" href="${esc(SITE + path)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..800&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..500&family=Caveat:wght@400..700&family=Young+Serif&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/pages.css">
  <link rel="stylesheet" href="/css/scrollbar.css">
  <link rel="icon" type="image/png" sizes="192x192" href="/images/icon-192.png">
  <meta name="theme-color" content="#2d2a26">
</head>
<body>
<div class="top">
  <a class="brand" href="/">StudyVault<img class="brandlock" src="/assets/studyvault-lock-rust.svg" alt=""></a>
  <span class="sp"></span>
  <nav class="pnav" aria-label="Pages"><a href="/subjects"${path.indexOf('/subjects') === 0 ? ' aria-current="page"' : ''}>Subjects</a><a href="/about">About</a><a href="/faq">FAQ</a></nav>
  <a class="mine" href="/classic">My StudyVault &#8599;</a>
</div>
<div class="wrap">
  <main class="page dir">
${body}
  </main>
  <p class="legalrow"><a href="/about">About</a> &middot; <a href="/faq">FAQ</a> &middot; <a href="/copyright.html">Copyright &amp; IP</a> &middot; <a href="/privacy.html">Privacy</a> &middot; &copy; StudyVault</p>
</div>
</body>
</html>
`;
}

function directoryIndex(subs) {
  const groups = new Map();
  subs.forEach(s => { if (!groups.has(s.name)) groups.set(s.name, []); groups.get(s.name).push(s); });
  const items = [...groups.entries()].map(([name, list]) =>
    `      <li><strong>${esc(name)}</strong> &middot; ${list.map(s =>
      `<a href="/subjects/${esc(s.slug)}">${esc(s.exam_board || 'All boards')}</a>`).join(' &middot; ')}</li>`).join('\n');
  return page({
    title: 'GCSE subjects - StudyVault',
    description: `Free GCSE revision for ${groups.size} subjects across AQA, Edexcel, OCR and Eduqas: lessons, practice questions, flashcards and audio, built from each board's specification.`,
    path: '/subjects',
    body: `    <h1>GCSE subjects</h1>
    <p class="lede">Free revision lessons for every subject below, written to each exam board's specification. Pick your subject and your board.</p>
    <ul class="dir-subjects">
${items}
    </ul>`
  });
}

function directorySubject(subject, units, guideList) {
  const label = subjectLabel(subject);
  const count = units.reduce((n, u) => n + u.lessons.length, 0);
  const body = units.map(u => `    <h2><a href="${esc(u.path)}">${esc(u.name)}</a></h2>
${u.subtitle ? `    <p>${esc(u.subtitle)}</p>\n` : ''}    <ol>
${u.lessons.map(l => `      <li><a href="${esc(l.path)}">${esc(l.title)}</a></li>`).join('\n')}
    </ol>`).join('\n');
  return page({
    title: `GCSE ${label} revision - StudyVault`,
    description: `Free GCSE ${label} revision: ${count} lessons across ${units.length} units, written to the exam board specification.`,
    path: `/subjects/${subject.slug}`,
    body: `    <h1>GCSE ${esc(label)}</h1>
    <p class="lede">${count} free revision lessons in ${units.length} units. <a href="/browse/${esc(subject.slug)}">Open the course</a> or go straight to a lesson.</p>
${body}
${(guideList || []).length ? `    <h2><a href="${esc(guideList[0].path)}">How to revise ${esc(subject.name)}</a></h2>
    <ul>
${guideList.slice(1).map(g => `      <li><a href="${esc(g.path)}">${esc(g.title)}</a></li>`).join('\n')}
    </ul>
` : ''}    <p><a href="/subjects">All subjects</a></p>`
  });
}

// ---- Page shells with real <head> tags ------------------------------------------------------
// Same wording as the loaders' document.title (lesson-, practice- and browse-loader.js), so
// the title does not change when the page finishes loading.
function course(sub) { return 'GCSE ' + sub.name + (sub.exam_board ? ' ' + sub.exam_board : ''); }

const SHELLS = {};
async function shell(file, req) {
  if (SHELLS[file]) return SHELLS[file];
  try { SHELLS[file] = fs.readFileSync(path.join(process.cwd(), file), 'utf8'); }
  catch (e) {
    const r = await fetch(`https://${req.headers.host}/${file}`);
    if (!r.ok) throw new Error('shell ' + file + ' ' + r.status);
    SHELLS[file] = await r.text();
  }
  return SHELLS[file];
}

const SUBJECT_COLS = 'slug, name, exam_board, school_id, status';

async function headFor(t, q) {
  const s = String(q.s || ''), u = String(q.u || ''), n = parseInt(q.n, 10);
  if (t === 'lesson' || t === 'practice') {
    if (!s || !u || !n) return null;
    const { data } = await supabase.from('lessons')
      .select(`title, description, hero_image_url, status, is_listening, ${t === 'lesson' ? 'content_html, ' : ''}units!inner(slug, name, subjects!inner(${SUBJECT_COLS}))`)
      .eq('lesson_number', n).eq('status', 'live').eq('units.slug', u)
      .eq('units.subjects.slug', s).is('units.subjects.school_id', null).eq('units.subjects.status', 'live')
      .limit(1);
    const l = data && data[0];
    if (!l) return null;
    const sub = l.units.subjects;
    const path = `/${t}/${s}/${u}/${n}`;
    const description = l.description || `${l.title}: a free ${course(sub)} revision ${t === 'practice' ? 'practice set' : 'lesson'} on ${l.units.name}.`;
    return {
      title: `${l.title} - ${course(sub)} - StudyVault`, description, image: l.hero_image_url, path,
      ld: [learningResource(l.title, description, sub, path, l.hero_image_url),
           breadcrumbs([[course(sub), `/subjects/${s}`], [l.units.name, `/browse/${s}/${u}`], [l.title, path]])],
      // the lesson's own text, for crawlers and link previews that run no JavaScript. Listening
      // lessons are a player and a card deck, not prose, so they carry none.
      body: (t === 'lesson' && !l.is_listening && l.content_html) ? `<h1>${esc(l.title)}</h1>\n${l.content_html}` : null
    };
  }
  if (t === 'browse') {
    if (!s) return null;
    const { data: subs } = await supabase.from('subjects').select(`id, ${SUBJECT_COLS}`)
      .eq('slug', s).is('school_id', null).eq('status', 'live').limit(1);
    const sub = subs && subs[0];
    if (!sub) return null;
    if (!u) return {
      title: `${course(sub)} revision - StudyVault`,
      description: `Free ${course(sub)} revision: every unit and lesson, written to the exam board specification.`,
      path: `/browse/${s}`,
      ld: [breadcrumbs([[course(sub), `/browse/${s}`]])]
    };
    const { data: units } = await supabase.from('units').select('name, subtitle, image_url')
      .eq('subject_id', sub.id).eq('slug', u).limit(1);
    const unit = units && units[0];
    if (!unit) return null;
    return {
      title: `${unit.name} - ${course(sub)} - StudyVault`,
      description: unit.subtitle || `${unit.name}: free ${course(sub)} revision lessons.`,
      image: unit.image_url, path: `/browse/${s}/${u}`,
      ld: [breadcrumbs([[course(sub), `/browse/${s}`], [unit.name, `/browse/${s}/${u}`]])]
    };
  }
  if (t === 'guide') {
    const type = String(q.type || ''), slug = String(q.slug || '') || 'index';
    if (!s || type !== 'revision-technique') return null;           // exam-technique guides were retired
    const { data: subs } = await supabase.from('subjects').select(`id, ${SUBJECT_COLS}`)
      .eq('slug', s).is('school_id', null).eq('status', 'live').limit(1);
    const sub = subs && subs[0];
    if (!sub) return null;
    const { data: pages } = await supabase.from('guide_pages').select('title, content_html')
      .eq('subject_id', sub.id).eq('guide_type', type).eq('slug', slug).limit(1);
    const g = pages && pages[0];
    if (!g) return null;
    const hubPath = `/guide/${s}/${type}`;
    const path = slug === 'index' ? hubPath : `${hubPath}/${slug}`;
    const name = slug === 'index' ? 'Revision techniques' : g.title;
    const firstPara = (String(g.content_html || '').match(/<p[^>]*>([\s\S]*?)<\/p>/i) || [])[1] || '';
    const plain = firstPara.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&[a-z]+;/g, ' ').replace(/\s+/g, ' ').trim();
    const description = (plain.length > 40 ? plain : `${name}: how to revise ${course(sub)} using methods the research supports.`).slice(0, 200);
    const crumbs = [[course(sub), `/subjects/${s}`], ['Revision techniques', hubPath]];
    if (slug !== 'index') crumbs.push([g.title, path]);
    return {
      title: `${name} - ${course(sub)} - StudyVault`, description, path,
      ld: [learningResource(name, description, sub, path, null), breadcrumbs(crumbs)],
      body: `<h1>${esc(name)}</h1>\n${guideLinks(g.content_html || '', s)}`
    };
  }
  return null;
}

/* Guide pages link to each other as "retrieval-practice.html" or "../revision-technique/x.html"
   (the loader rewrites them in the browser); the server copy gets the real addresses. Links to
   the retired exam-technique guides lose their link and keep their words. */
function guideLinks(html, s) {
  return String(html).replace(/<a\b([^>]*?)href="([^"]+)"([^>]*)>([\s\S]*?)<\/a>/gi, (m, pre, href, post, inner) => {
    if (/^(https?:|\/|#|mailto:)/i.test(href) || !/\.html$/i.test(href)) return m;
    if (/exam-technique\//.test(href)) return inner;
    const slug = href.replace(/^.*\//, '').replace(/\.html$/i, '');
    const to = `/guide/${s}/revision-technique` + (slug === 'index' ? '' : '/' + slug);
    return `<a${pre}href="${to}"${post}>${inner}</a>`;
  });
}

/* Structured data (schema.org): what the page is, and where it sits. */
function learningResource(name, description, sub, path, image) {
  const o = {
    '@context': 'https://schema.org', '@type': 'LearningResource', name, description,
    url: SITE + path, inLanguage: 'en-GB', isAccessibleForFree: true,
    educationalLevel: 'GCSE', learningResourceType: 'revision notes',
    about: { '@type': 'Thing', name: 'GCSE ' + sub.name },
    audience: { '@type': 'EducationalAudience', educationalRole: 'student' },
    provider: { '@type': 'Organization', name: 'StudyVault', url: SITE }
  };
  if (sub.exam_board) o.educationalAlignment = { '@type': 'AlignmentObject', alignmentType: 'educationalSubject', targetName: course(sub) };
  if (image) o.image = image;
  return o;
}
function breadcrumbs(items) {
  return { '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: items.map(([name, path], i) => ({ '@type': 'ListItem', position: i + 1, name, item: SITE + path })) };
}
function jsonLd(o) { return JSON.stringify(o).replace(/</g, '\\u003c'); }

/* A school pupil and a free-tier pupil can share an address (Unity's Triple Science and the
   free AQA Triple Science are both /lesson/separate-sciences/...). The server cannot tell which
   is visiting, so the text written into the page is the free-tier lesson; this runs before
   anything is drawn and hides it for a school session (or a staff preview, ?sid=), so a school
   pupil never glimpses the wrong lesson. The loader then fills the page as it always has. */
const SSR_GUARD = `<style>.sv-ssr-hide .sv-ssr{display:none!important}.sv-ssr-hide #guide-loading{display:block!important}</style>
  <script>try{if(sessionStorage.getItem('studyvault-school')||localStorage.getItem('sv-school')||/[?&]sid=/.test(location.search))document.documentElement.classList.add('sv-ssr-hide')}catch(e){}</script>`;

function withHead(html, h) {
  if (!h) return html;
  const tags = `<title>${esc(h.title)}</title>
  <meta name="description" content="${esc(h.description)}">
  <link rel="canonical" href="${esc(SITE + h.path)}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="StudyVault">
  <meta property="og:title" content="${esc(h.title.replace(/ - StudyVault$/, ''))}">
  <meta property="og:description" content="${esc(h.description)}">
  <meta property="og:url" content="${esc(SITE + h.path)}">${h.image ? `
  <meta property="og:image" content="${esc(h.image)}">
  <meta name="twitter:card" content="summary_large_image">` : ''}${(h.ld || []).map(o => `
  <script type="application/ld+json">${jsonLd(o)}</script>`).join('')}${h.body ? '\n  ' + SSR_GUARD : ''}`;
  let out = html.replace(/<title>[^<]*<\/title>/, () => tags);
  if (h.body) {
    // lesson: into the notes container, which the loader overwrites with the same lesson
    out = out.replace('<article class="study-notes" id="study-notes"></article>',
      () => `<article class="study-notes" id="study-notes"><div class="sv-ssr">${h.body}</div></article>`);
    // guide: into the guide container, shown straight away in place of the spinner
    out = out.replace('<div id="guide-content" style="display: none;"></div>',
      () => `<div id="guide-content"><div class="sv-ssr">${h.body}</div></div>`);
    if (out.indexOf('<div id="guide-content"><div class="sv-ssr">') >= 0)
      out = out.replace('<div id="guide-loading">', '<div id="guide-loading" style="display:none">');
  }
  return out;
}

const SHELL_FILE = { lesson: 'lesson.html', practice: 'practice.html', browse: 'browse.html', guide: 'guide.html' };

async function servePage(req, res) {
  const t = String(req.query.t || '');
  const html = await shell(SHELL_FILE[t], req);
  let h = null;
  try { h = await headFor(t, req.query); } catch (e) { h = null; }   // a lookup failure never blocks the page
  let out = html;
  try { out = withHead(html, h); } catch (e) { out = html; }          // nor does a fault in writing it in
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=86400');
  return res.status(200).send(out);
}

module.exports = async function handler(req, res) {
  if (req.query.kind === 'page' && SHELL_FILE[req.query.t]) {
    try { return await servePage(req, res); }
    catch (e) { res.setHeader('Cache-Control', 'no-store'); return res.status(500).send('Error'); }
  }
  const kind = String(req.query.kind || '');
  const name = String(req.query.name || req.query.slug || '').replace(/\.xml$/, '');
  try {
    const subs = await subjects();
    const bySlug = new Map(subs.map(s => [s.slug, s]));
    res.setHeader('Cache-Control', 'public, s-maxage=21600, stale-while-revalidate=86400');

    if (kind === 'index') {
      res.setHeader('Content-Type', 'application/xml; charset=utf-8');
      return res.status(200).send('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ['pages', ...subs.map(s => s.slug)].map(n => `  <sitemap><loc>${SITE}/sitemaps/${esc(n)}.xml</loc></sitemap>`).join('\n') +
        '\n</sitemapindex>\n');
    }

    if (kind === 'sitemap') {
      let entries;
      if (name === 'pages') {
        entries = [...STATIC_PAGES, ...subs.map(s => `/subjects/${s.slug}`)].map(path => ({ path }));
      } else if (bySlug.has(name)) {
        const units = await outline(bySlug.get(name));
        entries = [{ path: `/browse/${name}`, lastmod: newest(units.flatMap(u => u.lessons.map(l => l.lastmod))) }];
        units.forEach(u => {
          entries.push({ path: u.path, lastmod: newest(u.lessons.map(l => l.lastmod)) });
          u.lessons.forEach(l => entries.push({ path: l.path, lastmod: l.lastmod }));
        });
        (await guides(bySlug.get(name))).forEach(g => entries.push({ path: g.path }));
      } else {
        return res.status(404).send('Not found');
      }
      res.setHeader('Content-Type', 'application/xml; charset=utf-8');
      return res.status(200).send(urlset(entries));
    }

    if (kind === 'subjects') {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      if (!name) return res.status(200).send(directoryIndex(subs));
      if (!bySlug.has(name)) return res.status(404).send(page({ title: 'Subject not found - StudyVault', description: 'This subject is not on StudyVault.', path: '/subjects',
        body: '    <h1>Subject not found</h1>\n    <p class="lede">That subject is not here. <a href="/subjects">See every subject</a>.</p>' }));
      const subject = bySlug.get(name);
      return res.status(200).send(directorySubject(subject, await outline(subject), await guides(subject)));
    }

    return res.status(400).send('Unknown kind');
  } catch (e) {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(500).send('Error');
  }
};
