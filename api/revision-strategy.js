/**
 * AI Revision Strategy API Route
 *
 * Takes a student's exam timetable and returns personalised revision advice.
 * Uses Haiku 4.5 for fast, cheap responses.
 *
 * POST /api/revision-strategy
 * Body: { exams: [{subject, paper, date, session}, ...] }
 */

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const { exams } = req.body || {};

  if (!exams || !Array.isArray(exams) || exams.length === 0) {
    return res.status(400).json({ error: 'Missing exams array' });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'API key not configured' });
  }

  // Build the timetable summary for the prompt
  const today = new Date().toISOString().split('T')[0];
  const timetableLines = exams.map(e => {
    const d = new Date(e.date + 'T00:00:00');
    const days = Math.ceil((d - new Date(today + 'T00:00:00')) / 86400000);
    const dayLabel = days <= 0 ? 'TODAY' : days === 1 ? 'TOMORROW' : `in ${days} days`;
    return `${e.date} (${e.session.toUpperCase()}) — ${e.subject}: ${e.paper} [${dayLabel}]`;
  }).join('\n');

  const systemPrompt = `You are a friendly, encouraging GCSE revision coach. A Year 11 student has shared their exam timetable with you. Today is ${today}.

Give them a clear, personalised revision strategy. Be specific and practical — reference their actual subjects and dates.

Structure your response EXACTLY like this, using these headings with markdown:

## Priority Right Now
What they should focus on this week based on which exam is closest. Be specific about the subject and topic areas.

## Your Revision Schedule
A week-by-week or phase-by-phase plan working through their exams in date order. For each phase, name the subject(s) to focus on and roughly how many days they have. Identify natural revision windows (gaps between exams).

## Smart Tips for Your Timetable
3-4 specific observations about their timetable — things like:
- Subjects that are close together (so they need to prep both early)
- Long gaps they can use for deeper revision
- Days with multiple exams where they should prepare in advance
- Their last exam (so they know when they're done!)

## You've Got This
A short encouraging sign-off (2-3 sentences max). Be warm but not cheesy.

Keep the whole response under 500 words. Use bullet points. Don't use generic advice — make every point reference their specific subjects and dates.`;

  const userPrompt = `Here is my exam timetable:\n\n${timetableLines}\n\nPlease give me a personalised revision strategy.`;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1024,
        system: systemPrompt,
        messages: [{ role: 'user', content: userPrompt }]
      })
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Anthropic API error:', err);
      return res.status(502).json({ error: 'AI service error' });
    }

    const data = await response.json();
    const text = data.content?.[0]?.text || '';

    return res.status(200).json({ strategy: text });
  } catch (err) {
    console.error('Revision strategy error:', err);
    return res.status(500).json({ error: 'Internal error' });
  }
};
