const { supabase } = require('./pipeline/_lib/supabase');
const { notifyAdmin, escHtml } = require('./_lib/notify');

const ALLOWED_BOARDS = ['AQA', 'Edexcel', 'OCR', 'Eduqas', 'WJEC', 'NCFE', 'Other', ''];

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = req.body || {};
  const subject_name = String(body.subject_name || '').trim().slice(0, 120);
  const topic = String(body.topic || '').trim().slice(0, 200);
  const exam_board = String(body.exam_board || '').trim().slice(0, 20);
  const email = String(body.email || '').trim().slice(0, 200);
  const notes = String(body.notes || '').trim().slice(0, 500);

  if (!subject_name) {
    return res.status(400).json({ error: 'Subject name is required' });
  }
  if (exam_board && !ALLOWED_BOARDS.includes(exam_board)) {
    return res.status(400).json({ error: 'Invalid exam board' });
  }
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // Light per-IP rate limit: max 5 requests per IP in last hour.
  // Service-key only — never reveal the count to the client.
  const ipHeader = (req.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || req.socket?.remoteAddress
    || '';
  const userAgent = String(req.headers['user-agent'] || '').slice(0, 300);

  const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString();
  if (ipHeader) {
    const { count } = await supabase
      .from('subject_requests')
      .select('id', { count: 'exact', head: true })
      .gt('created_at', oneHourAgo)
      .ilike('user_agent', '%' + ipHeader + '%');
    if ((count || 0) >= 5) {
      return res.status(429).json({ error: 'Too many requests, try again later' });
    }
  }

  const { error } = await supabase.from('subject_requests').insert({
    subject_name,
    topic: topic || null,
    exam_board: exam_board || null,
    email: email || null,
    notes: notes || null,
    user_agent: ipHeader ? `${ipHeader} | ${userAgent}` : userAgent || null,
  });

  if (error) {
    console.error('subject_request insert failed', error);
    return res.status(500).json({ error: 'Could not save request' });
  }

  // Fire-and-forget admin email — don't block the response if the email
  // service is down or the API key is missing.
  notifyAdmin({
    subject: `[StudyVault Request] ${subject_name}${exam_board ? ' (' + exam_board + ')' : ''}`,
    text:
      `New subject request on StudyVault\n\n` +
      `Subject: ${subject_name}\n` +
      `Topic: ${topic || '(not specified)'}\n` +
      `Exam board: ${exam_board || '(not specified)'}\n` +
      `Requester email: ${email || '(not provided)'}\n` +
      `Notes: ${notes || '(none)'}\n\n` +
      `Triage at: https://www.studyvault.co.uk/admin/requests`,
    html:
      `<h2 style="font-family:sans-serif;margin:0 0 0.5em">New subject request</h2>` +
      `<table style="font-family:sans-serif;font-size:0.95em;border-collapse:collapse;margin-top:0.5em">` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Subject</td><td><strong>${escHtml(subject_name)}</strong></td></tr>` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Topic</td><td>${escHtml(topic || '(not specified)')}</td></tr>` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Exam board</td><td>${escHtml(exam_board || '(not specified)')}</td></tr>` +
      `<tr><td style="padding:4px 12px 4px 0;color:#666">Requester</td><td>${escHtml(email || '(not provided)')}</td></tr>` +
      (notes ? `<tr><td style="padding:4px 12px 4px 0;color:#666;vertical-align:top">Notes</td><td>${escHtml(notes)}</td></tr>` : '') +
      `</table>` +
      `<p style="margin-top:1.5em;font-family:sans-serif"><a href="https://www.studyvault.co.uk/admin/requests" style="background:#2d2a26;color:#fff;padding:0.6em 1.2em;text-decoration:none;border-radius:6px;font-weight:600">Open admin triage &rarr;</a></p>`,
  }).catch((e) => console.error('[subject-request] notify error:', e));

  return res.json({ ok: true });
};
