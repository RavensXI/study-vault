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
 *
 * NOTE ON GROQ: despite the name below, Groq is NOT a fallback — when
 * GROQ_API_KEY is set it is tried FIRST on the quick tier and Anthropic
 * catches its failures. Groq is US-served and cannot be pinned to its EU
 * region without an Enterprise plan, so unset GROQ_API_KEY to keep pupil work
 * inside Europe. Anthropic calls route via api/_lib/claude.js.
 */

const { callClaude } = require('./_lib/claude');

// Extended responses (>8 marks) need judgement, not fact-spotting, and Haiku
// is measurably too generous there — in the bake-off it gave 5/6 to invented
// quotations and 2/4 to a conservation-of-energy error. Keep this tier on the
// largest model the account can actually reach; api/_lib/claude.js maps it.
const EXAM_MODEL = 'claude-sonnet-5';

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  // Only serve calls from our own site (same pattern as api/tutor.js) — a
  // casual-abuse deterrent; the per-IP rate limit below is the backstop.
  const origin = req.headers.origin || '';
  const okOrigin =
    /^https:\/\/(www\.)?studyvault\.co\.uk$/.test(origin) ||
    /^https:\/\/[a-z0-9-]+\.vercel\.app$/.test(origin) ||
    /^http:\/\/localhost(:\d+)?$/.test(origin);
  if (!okOrigin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { tier: requestedTier, marks, system, prompt, free_tier } = req.body || {};

  if (!prompt) {
    return res.status(400).json({ error: 'Missing prompt' });
  }

  // Length caps — legit marking prompts (passage + question + mark scheme +
  // student answer) sit well under these; anything bigger is abuse.
  if (typeof prompt !== 'string' || prompt.length > 24000) {
    return res.status(400).json({ error: 'Prompt too long' });
  }
  if (system && (typeof system !== 'string' || system.length > 8000)) {
    return res.status(400).json({ error: 'System prompt too long' });
  }

  // Determine tier: explicit > auto (from marks) > default quick
  // Free tier users always get Haiku (quick) regardless of marks
  let tier;
  if (free_tier) {
    tier = 'quick';
  } else if (requestedTier === 'quick' || requestedTier === 'exam') {
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
      // 2000, not 800. The bake-off (scripts/model-eval/) found Sonnet hit an
      // 800-token ceiling on HALF its calls even on short answers — it scored
      // 69% truncated against 98% untruncated, so the old budget was measuring
      // the cap rather than the model. A 16- or 30-mark essay needs the room.
      result = await callAnthropic(system, prompt, EXAM_MODEL, 2000);
      model = EXAM_MODEL;
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
  const data = await callClaude({
    model: model,
    max_tokens: maxTokens || 600,
    system: system || 'You are a GCSE examiner. Mark the student response against the provided mark scheme.',
    messages: [
      { role: 'user', content: prompt },
    ],
  });
  return data.content[0].text;
}
