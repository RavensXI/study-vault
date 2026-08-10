/**
 * AI Revision Strategy API Route
 *
 * The AI generates revision TOPICS per subject (the what).
 * The client code schedules them into days (the when).
 *
 * Returns:
 *   - strategy: markdown overview text
 *   - topics: { "English Literature": ["Macbeth key quotes", "19th Century Novel themes", ...], ... }
 *
 * POST /api/revision-strategy
 * Body: { exams: [{subject, paper, date, session}, ...], today: "2026-04-14" }
 */

const { callClaude, useBedrock } = require('./_lib/claude');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  // Only serve calls from our own site (same pattern as api/tutor.js).
  const origin = req.headers.origin || '';
  const okOrigin =
    /^https:\/\/(www\.)?studyvault\.co\.uk$/.test(origin) ||
    /^https:\/\/[a-z0-9-]+\.vercel\.app$/.test(origin) ||
    /^http:\/\/localhost(:\d+)?$/.test(origin);
  if (!okOrigin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { exams, today: clientToday } = req.body || {};

  if (!exams || !Array.isArray(exams) || exams.length === 0) {
    return res.status(400).json({ error: 'Missing exams array' });
  }
  if (exams.length > 60) {
    return res.status(400).json({ error: 'Too many exams' });
  }

  // Rate limit (in-memory, per IP, resets on redeploy) — a student generates a
  // plan a handful of times; this endpoint calls Sonnet so keep it tight.
  const ip = String(req.headers['x-forwarded-for'] || req.connection?.remoteAddress || 'unknown').split(',')[0].trim();
  const now = Date.now();
  const windowMs = 60 * 60 * 1000;
  if (!global._revStrategyRates) global._revStrategyRates = {};
  const rates = global._revStrategyRates;
  rates[ip] = (rates[ip] || []).filter(ts => now - ts < windowMs);
  if (rates[ip].length >= 10) {
    return res.status(429).json({ error: 'Rate limit exceeded. Try again later.' });
  }
  rates[ip].push(now);

  // Either credential set is fine: Bedrock (AWS_*) or the direct API key.
  if (!useBedrock() && !process.env.ANTHROPIC_API_KEY) {
    return res.status(500).json({ error: 'API key not configured' });
  }

  const today = clientToday || new Date().toISOString().split('T')[0];

  const timetableLines = exams.map(e => {
    const date = String(e.date || '').slice(0, 10);
    const session = String(e.session || '').slice(0, 10);
    const subject = String(e.subject || '').slice(0, 80);
    const paper = String(e.paper || '').slice(0, 120);
    const d = new Date(date + 'T00:00:00');
    const days = Math.ceil((d - new Date(today + 'T00:00:00')) / 86400000);
    const dayLabel = days <= 0 ? 'TODAY' : days === 1 ? 'TOMORROW' : `in ${days} days`;
    return `${date} (${session.toUpperCase()}) — ${subject}: ${paper} [${dayLabel}]`;
  }).join('\n');

  const subjects = [...new Set(exams.map(e => String(e.subject || '').slice(0, 80)))];

  // Count how many revision days each subject roughly needs
  const subjectPapers = {};
  exams.forEach(e => {
    const subject = String(e.subject || '').slice(0, 80);
    if (!subjectPapers[subject]) subjectPapers[subject] = 0;
    subjectPapers[subject]++;
  });

  const systemPrompt = `You are a GCSE revision coach. Today is ${today}. A student has these exams:

${timetableLines}

Return a JSON object with exactly two keys:

1. "strategy" — A short markdown overview (under 250 words) with these sections:
   ## Priority Right Now
   What to focus on this week (reference specific subjects and dates).
   ## Smart Tips
   3-4 bullet points about their specific timetable.
   ## You've Got This
   2 sentences of encouragement.

2. "topics" — An object where each key is a subject name (exactly as listed above) and each value is an array of revision topic strings. These are the specific topics/areas the student should cover for that subject.

Rules for topics:
- Each topic must be SHORT: 2-4 words max. Just the topic name. Examples: "Macbeth key quotes", "Cell division", "Algebra basics", "Listening practice"
- For subjects with 2 papers: provide topics for BOTH papers, roughly in curriculum order
- Number of topics per subject: roughly ${Object.entries(subjectPapers).map(([s, n]) => `${s}: ${n * 8} topics`).join(', ')}
- Topics should cover the full breadth of the specification — don't just list 3 topics, give enough to fill multiple revision sessions
- Do NOT include scheduling instructions — just list the topics

Return ONLY valid JSON. No markdown fences, no explanation.`;

  const userPrompt = `Generate my revision topic lists as JSON.`;

  try {
    const data = await callClaude({
      model: 'claude-sonnet-4-6',
      max_tokens: 4096,
      system: systemPrompt,
      messages: [{ role: 'user', content: userPrompt }]
    });

    // Every text block, not content[0] — a thinking-enabled model puts a
    // thinking block first and content[0].text is undefined.
    let text = (data.content || []).map(b => b.text || '').join('').trim();
    text = text.replace(/^```json?\s*\n?/, '').replace(/\n?```\s*$/, '');

    let result;
    try {
      result = JSON.parse(text);
    } catch (parseErr) {
      console.error('Failed to parse AI response:', text.substring(0, 500));
      return res.status(200).json({ strategy: text, topics: {} });
    }

    return res.status(200).json({
      strategy: result.strategy || '',
      topics: result.topics || {}
    });
  } catch (err) {
    console.error('Revision strategy error:', err);
    return res.status(500).json({ error: 'Internal error' });
  }
};
