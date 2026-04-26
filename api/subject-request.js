const { supabase } = require('./pipeline/_lib/supabase');

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

  return res.json({ ok: true });
};
