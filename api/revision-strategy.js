/**
 * AI Revision Strategy API Route
 *
 * Takes a student's exam timetable and returns:
 *   - strategy: markdown overview text
 *   - daily_plan: { "2026-04-15": [{subject, focus}], ... }
 *
 * Uses Haiku 4.5 for fast, cheap responses.
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

  // Find date range: today → last exam
  const examDates = exams.map(e => e.date).sort();
  const lastExamDate = examDates[examDates.length - 1];

  // Build list of all dates from today to last exam
  const allDates = [];
  const d = new Date(today + 'T00:00:00');
  const end = new Date(lastExamDate + 'T00:00:00');
  while (d <= end) {
    allDates.push(d.toISOString().split('T')[0]);
    d.setDate(d.getDate() + 1);
  }

  // Build exam date lookup
  const examsByDate = {};
  exams.forEach(e => {
    if (!examsByDate[e.date]) examsByDate[e.date] = [];
    examsByDate[e.date].push(e);
  });

  const timetableLines = exams.map(e => {
    const dt = new Date(e.date + 'T00:00:00');
    const days = Math.ceil((dt - new Date(today + 'T00:00:00')) / 86400000);
    const dayLabel = days <= 0 ? 'TODAY' : days === 1 ? 'TOMORROW' : `in ${days} days`;
    return `${e.date} (${e.session.toUpperCase()}) — ${e.subject}: ${e.paper} [${dayLabel}]`;
  }).join('\n');

  const subjects = [...new Set(exams.map(e => e.subject))];

  const systemPrompt = `You are a GCSE revision coach. Today is ${today}. A student has these exams:

${timetableLines}

You must return a JSON object with exactly two keys:

1. "strategy" — A short markdown overview (under 300 words) with these sections:
   ## Priority Right Now
   What to focus on this week.
   ## Smart Tips
   3-4 bullet points about their specific timetable (clusters, gaps, interleaving opportunities).
   ## You've Got This
   2 sentences of encouragement.

2. "daily_plan" — An object mapping EVERY date from ${today} to ${lastExamDate} (inclusive) to an array of revision tasks. Each task is: {"subject": "Subject Name", "focus": "Specific topic or activity"}.

Rules for the daily plan:
- On EXAM DAYS: include a task like {"subject": "English Literature", "focus": "EXAM — Paper 1 (AM)"}
- The day BEFORE an exam: prioritise that subject
- Use INTERLEAVING: mix 2-3 subjects per day, don't just block one subject all week
- Weight subjects by PROXIMITY: subjects with exams soon get more daily slots
- SUNDAYS MUST BE REST DAYS: only include {"subject": "Rest", "focus": "Rest day"}. No revision on Sundays, no exceptions.
- Weekdays and Saturdays should have 2-3 tasks each (not more)
- The "focus" field must be SHORT — just the subject area or topic, max 5 words. Examples: "Energy equations", "Moles & Mr", "Act 1 quotes", "Listening practice", "Punnett squares". Do NOT write instructions like "Practise..." or "Revise..." — just name the topic.
- For subjects with multiple papers, distinguish P1 and P2 content areas
- The student's subjects are: ${subjects.join(', ')}

Return ONLY valid JSON, no markdown fences, no explanation outside the JSON.`;

  const userPrompt = `Generate my day-by-day revision plan as JSON.`;

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
        max_tokens: 8192,
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

    // Strip markdown code fences if present
    text = text.replace(/^```json?\s*\n?/, '').replace(/\n?```\s*$/, '');

    let result;
    try {
      result = JSON.parse(text);
    } catch (parseErr) {
      console.error('Failed to parse AI response as JSON:', text.substring(0, 500));
      // Fallback: return the raw text as strategy with no daily plan
      return res.status(200).json({ strategy: text, daily_plan: {} });
    }

    return res.status(200).json({
      strategy: result.strategy || '',
      daily_plan: result.daily_plan || {}
    });
  } catch (err) {
    console.error('Revision strategy error:', err);
    return res.status(500).json({ error: 'Internal error' });
  }
};
