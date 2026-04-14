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

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const { exams, today: clientToday } = req.body || {};

  if (!exams || !Array.isArray(exams) || exams.length === 0) {
    return res.status(400).json({ error: 'Missing exams array' });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'API key not configured' });
  }

  const today = clientToday || new Date().toISOString().split('T')[0];

  const timetableLines = exams.map(e => {
    const d = new Date(e.date + 'T00:00:00');
    const days = Math.ceil((d - new Date(today + 'T00:00:00')) / 86400000);
    const dayLabel = days <= 0 ? 'TODAY' : days === 1 ? 'TOMORROW' : `in ${days} days`;
    return `${e.date} (${e.session.toUpperCase()}) — ${e.subject}: ${e.paper} [${dayLabel}]`;
  }).join('\n');

  const subjects = [...new Set(exams.map(e => e.subject))];

  // Count how many revision days each subject roughly needs
  const subjectPapers = {};
  exams.forEach(e => {
    if (!subjectPapers[e.subject]) subjectPapers[e.subject] = 0;
    subjectPapers[e.subject]++;
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
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 4096,
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
    let text = (data.content?.[0]?.text || '').trim();
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
