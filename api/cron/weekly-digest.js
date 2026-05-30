/**
 * Weekly admin digest — emails a summary of everything awaiting Tom's review:
 * pending subject requests, open bug reports, and Simplify/Explain QA failures.
 *
 * Scheduled via vercel.json `crons` to run daily; it only actually sends on
 * Mondays (UTC) so it works the same on Hobby and Pro plans (Hobby crons are
 * limited to ~once/day). A manual trigger with the admin password always sends,
 * for testing.
 *
 * Auth:
 *   - Vercel Cron: set CRON_SECRET in env; Vercel then sends
 *     `Authorization: Bearer <CRON_SECRET>` automatically.
 *   - Manual test: GET /api/cron/weekly-digest with header X-Admin-Password.
 *
 * Reuses api/_lib/notify.js (Resend). Env: RESEND_API_KEY, NOTIFY_TO/FROM.
 */

const { supabase } = require('../pipeline/_lib/supabase');
const { notifyAdmin, escHtml } = require('../_lib/notify');

const BASE = 'https://www.studyvault.co.uk';

function authorize(req) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers['authorization'] || '';
  if (secret && auth === 'Bearer ' + secret) return { ok: true, manual: false };
  const pw = req.headers['x-admin-password'];
  if (pw && process.env.ADMIN_PASSWORD && pw === process.env.ADMIN_PASSWORD) return { ok: true, manual: true };
  if (!secret) return { ok: true, manual: false }; // no secret configured — allow cron out of the box
  return { ok: false };
}

async function countRows(table, col, val, col2, val2) {
  let q = supabase.from(table).select('*', { count: 'exact', head: true }).eq(col, val);
  if (col2) q = q.eq(col2, val2);
  const { count } = await q;
  return count || 0;
}

async function recentRows(table, select, col, val, orderCol) {
  const { data } = await supabase.from(table).select(select).eq(col, val).order(orderCol, { ascending: false }).limit(5);
  return data || [];
}

function section(title, count, link, linkLabel, rowsHtml) {
  return (
    '<div style="margin:0 0 1.5rem">' +
      '<h3 style="margin:0 0 0.4rem;font-size:1rem;color:#2d2a26">' + escHtml(title) +
        ' <span style="color:' + (count > 0 ? '#b91c1c' : '#15803d') + '">(' + count + ')</span></h3>' +
      (rowsHtml || '<p style="margin:0 0 0.5rem;color:#8a8479;font-size:0.85rem">Nothing pending.</p>') +
      '<a href="' + link + '" style="font-size:0.82rem;color:#1d4ed8">' + escHtml(linkLabel) + ' &rarr;</a>' +
    '</div>'
  );
}

function fmtDate(iso) {
  if (!iso) return '';
  try { return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }); }
  catch (e) { return ''; }
}

function listHtml(items) {
  if (!items.length) return '';
  return '<ul style="margin:0 0 0.5rem;padding-left:1.1rem;color:#2d2a26;font-size:0.85rem">' +
    items.map(function (li) { return '<li style="margin:0.1rem 0">' + li + '</li>'; }).join('') + '</ul>';
}

module.exports = async (req, res) => {
  const a = authorize(req);
  if (!a.ok) return res.status(401).json({ error: 'Unauthorised' });

  // Weekly cadence: only send on Mondays unless manually triggered.
  const isMonday = new Date().getUTCDay() === 1;
  if (!a.manual && !isMonday) return res.status(200).json({ skipped: 'not Monday' });

  try {
    const reqCount = await countRows('subject_requests', 'status', 'pending');
    const bugCount = await countRows('bug_reports', 'status', 'open');
    const qaCount = await countRows('simplify_cache', 'qa_status', 'pending_review');
    const qaSimple = await countRows('simplify_cache', 'qa_status', 'pending_review', 'target_level', 'simple');
    const qaExplain = qaCount - qaSimple;

    const reqRows = await recentRows('subject_requests', 'subject_name, exam_board, created_at', 'status', 'pending', 'created_at');
    const bugRows = await recentRows('bug_reports', 'message, created_at', 'status', 'open', 'created_at');
    const qaRows = await recentRows('simplify_cache', 'target_level, subject_slug, updated_at, lessons(title)', 'qa_status', 'pending_review', 'updated_at');

    const total = reqCount + bugCount + qaCount;

    const reqList = listHtml(reqRows.map(function (r) {
      return escHtml(r.subject_name || 'Subject') + (r.exam_board ? ' (' + escHtml(r.exam_board) + ')' : '') +
        ' <span style="color:#8a8479">· ' + fmtDate(r.created_at) + '</span>';
    }));
    const bugList = listHtml(bugRows.map(function (b) {
      return escHtml((b.message || '').slice(0, 90)) + ' <span style="color:#8a8479">· ' + fmtDate(b.created_at) + '</span>';
    }));
    const qaList = listHtml(qaRows.map(function (q) {
      var t = (q.lessons && q.lessons.title) ? q.lessons.title : (q.subject_slug || 'lesson');
      var mode = q.target_level === 'explain' ? 'Explain' : 'Simplify';
      return '<strong>' + escHtml(mode) + '</strong> · ' + escHtml(t) + ' <span style="color:#8a8479">· ' + fmtDate(q.updated_at) + '</span>';
    }));

    const subject = total > 0
      ? 'StudyVault weekly digest — ' + total + ' item' + (total === 1 ? '' : 's') + ' to review'
      : 'StudyVault weekly digest — all clear';

    const html =
      '<div style="font-family:Inter,Arial,sans-serif;max-width:560px;margin:0 auto;color:#2d2a26">' +
        '<h2 style="font-size:1.25rem;margin:0 0 0.25rem">Weekly digest</h2>' +
        '<p style="color:#8a8479;font-size:0.85rem;margin:0 0 1.5rem">' +
          (total > 0 ? total + ' item' + (total === 1 ? '' : 's') + ' need your attention.' : 'Nothing needs review this week — all clear.') +
        '</p>' +
        section('Subject requests', reqCount, BASE + '/admin/requests', 'Open requests', reqList) +
        section('Bug reports', bugCount, BASE + '/admin/bugs', 'Open bugs', bugList) +
        section('Simplify / Explain QA', qaCount, BASE + '/admin/simplify-review',
          'Review queue', qaList ? (qaList + '<p style="margin:0 0 0.5rem;color:#8a8479;font-size:0.8rem">' +
            qaSimple + ' simplify · ' + qaExplain + ' explain</p>') : '') +
        '<hr style="border:none;border-top:1px solid #eee;margin:1.5rem 0 0.75rem">' +
        '<p style="color:#b3ada3;font-size:0.72rem;margin:0">Automated weekly summary · StudyVault admin</p>' +
      '</div>';

    const text = 'StudyVault weekly digest\n\n' +
      'Subject requests pending: ' + reqCount + ' (' + BASE + '/admin/requests)\n' +
      'Bug reports open: ' + bugCount + ' (' + BASE + '/admin/bugs)\n' +
      'Simplify/Explain QA to review: ' + qaCount + ' [' + qaSimple + ' simplify, ' + qaExplain + ' explain] (' + BASE + '/admin/simplify-review)\n';

    const result = await notifyAdmin({ subject, html, text });
    return res.status(200).json({ ok: true, total, counts: { reqCount, bugCount, qaCount }, email: result });
  } catch (e) {
    console.error('[weekly-digest]', e);
    return res.status(500).json({ error: String(e) });
  }
};
