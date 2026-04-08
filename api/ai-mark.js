/**
 * AI Marking API Route
 *
 * Routes to different models based on marking tier:
 *   - "quick" → Anthropic Haiku 4.5 — for inference, technique ID, connotation checks,
 *               and standard practice questions (≤8 marks)
 *   - "exam"  → Anthropic Sonnet 4.6 — for extended responses (12+ marks) with
 *               level descriptors requiring nuanced judgement
 *   - "auto"  → Automatically selects based on `marks` field:
 *               ≤8 marks → quick, >8 marks → exam
 *
 * POST /api/ai-mark
 * Body: { tier, marks, system, prompt }
 *
 * If tier is omitted or "auto", the `marks` field determines routing.
 * If both tier and marks are omitted, defaults to "quick".
 *
 * Rate limited per student session. API keys stored in env vars.
 * Supports Groq as optional fallback for quick tier (set GROQ_API_KEY).
 */

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const { tier: requestedTier, marks, system, prompt } = req.body || {};

  if (!prompt) {
    return res.status(400).json({ error: 'Missing prompt' });
  }

  // Determine tier: explicit > auto (from marks) > default quick
  let tier;
  if (requestedTier === 'quick' || requestedTier === 'exam') {
    tier = requestedTier;
  } else if (typeof marks === 'number') {
    tier = marks > 8 ? 'exam' : 'quick';
  } else {
    tier = 'quick';
  }

  // Rate limiting (simple in-memory, per IP, resets on redeploy)
  const ip = req.headers['x-forwarded-for'] || req.connection?.remoteAddress || 'unknown';
  const now = Date.now();
  const windowMs = 60 * 60 * 1000; // 1 hour
  if (!global._aiMarkRates) global._aiMarkRates = {};
  const rates = global._aiMarkRates;
  if (!rates[ip]) rates[ip] = { quick: [], exam: [] };

  // Clean old entries
  ['quick', 'exam'].forEach(t => {
    rates[ip][t] = (rates[ip][t] || []).filter(ts => now - ts < windowMs);
  });

  const limits = { quick: 60, exam: 20 }; // per hour
  if (rates[ip][tier]?.length >= (limits[tier] || 60)) {
    return res.status(429).json({ error: 'Rate limit exceeded. Try again later.' });
  }
  rates[ip][tier].push(now);

  try {
    let result;
    let model;

    if (tier === 'exam') {
      result = await callAnthropic(system, prompt, 'claude-sonnet-4-6', 800);
      model = 'claude-sonnet-4-6';
    } else {
      // Quick tier: try Groq first (cheaper), fall back to Haiku
      if (process.env.GROQ_API_KEY) {
        try {
          result = await callGroq(system, prompt);
          model = 'groq/gpt-oss-120b';
        } catch (groqErr) {
          // Groq failed — fall back to Haiku
          result = await callAnthropic(system, prompt, 'claude-haiku-4-5-20251001', 400);
          model = 'claude-haiku-4-5-20251001';
        }
      } else {
        result = await callAnthropic(system, prompt, 'claude-haiku-4-5-20251001', 400);
        model = 'claude-haiku-4-5-20251001';
      }
    }

    return res.status(200).json({ result, model, tier });
  } catch (err) {
    console.error('AI marking error:', err.message);
    return res.status(502).json({ error: 'AI marking failed', detail: err.message });
  }
};


async function callGroq(system, prompt) {
  const key = process.env.GROQ_API_KEY;
  if (!key) throw new Error('GROQ_API_KEY not configured');

  const resp = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + key,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'openai/gpt-oss-120b',
      messages: [
        { role: 'system', content: system || 'You are a GCSE examiner. Mark the student response.' },
        { role: 'user', content: prompt },
      ],
      temperature: 0.3,
      max_tokens: 400,
    }),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error('Groq API error: ' + resp.status + ' ' + err);
  }

  const data = await resp.json();
  return data.choices[0].message.content;
}


async function callAnthropic(system, prompt, model, maxTokens) {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) throw new Error('ANTHROPIC_API_KEY not configured');

  const resp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: model,
      max_tokens: maxTokens || 600,
      system: system || 'You are a GCSE examiner. Mark the student response against the provided mark scheme.',
      messages: [
        { role: 'user', content: prompt },
      ],
    }),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error('Anthropic API error: ' + resp.status + ' ' + err);
  }

  const data = await resp.json();
  return data.content[0].text;
}
