/**
 * Content reads for the admin pages (24 Sep 2026; two-factor 29 Sep 2026).
 *
 * The content tables are private to each school, and unpublished lessons are private to staff
 * (supabase/migrations/20260924210000_school_content_private.sql). js/content-reads.js sends an
 * admin page's content reads here with the admin's Bearer token; the read runs with the service
 * key only when that token belongs to a platform_admin who passed the two-factor step
 * (requireTeacher treats a password-only platform_admin as a teacher, so this answers 403).
 *
 * GET /api/staff/rest?p=<table>?<PostgREST query>     headers: Authorization: Bearer <token>
 * Read-only, and only the five content tables. Teachers never need this: they read with their
 * own sign-in, which the school rules already allow.
 */
const { requireTeacher } = require('../pipeline/_lib/auth');

const TABLES = /^(lessons|units|subjects|guide_pages|lesson_overrides)(\?|$)/;
const PASS_HEADERS = ['accept', 'prefer', 'range', 'range-unit'];

module.exports = async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    return res.status(405).json({ error: 'Read-only' });
  }
  const auth = await requireTeacher(req, res);
  if (!auth) return;
  if (auth.profile.role !== 'platform_admin') {
    return res.status(403).json({ error: 'Admin only' });
  }

  const p = String(req.query.p || '');
  if (!TABLES.test(p) || p.indexOf('..') !== -1) {
    return res.status(400).json({ error: 'Not a content table' });
  }

  const headers = {
    apikey: process.env.SUPABASE_SERVICE_KEY,
    Authorization: 'Bearer ' + process.env.SUPABASE_SERVICE_KEY
  };
  PASS_HEADERS.forEach(function (h) { if (req.headers[h]) headers[h] = req.headers[h]; });

  let upstream;
  try {
    upstream = await fetch(process.env.SUPABASE_URL + '/rest/v1/' + p, { method: req.method, headers });
  } catch (e) {
    return res.status(502).json({ error: 'Database unreachable' });
  }
  const body = await upstream.text();
  ['content-type', 'content-range', 'preference-applied'].forEach(function (h) {
    const v = upstream.headers.get(h);
    if (v) res.setHeader(h, v);
  });
  res.setHeader('Cache-Control', 'no-store');
  return res.status(upstream.status).send(body);
};
