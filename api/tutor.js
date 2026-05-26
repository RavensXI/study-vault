/**
 * Socratic Lesson Tutor API
 *
 * A standalone, lesson-grounded tutor chat. Students ask about anything in the
 * lesson; the tutor coaches them Socratically — guiding questions and
 * progressive hints — rather than handing over answers.
 *
 * POST /api/tutor
 * Body: {
 *   lessonTitle: string,
 *   lessonText:  string,   // plain text of the lesson content (grounding)
 *   messages:    [{ role: 'user'|'assistant', content: string }, ...]
 * }
 * Returns: { reply, model }
 *
 * Model: Haiku (cheap, multi-turn) — matches the /api/ai-mark quick tier.
 * Prompt caching: the system prompt + lesson content are stable across a
 * conversation, so they're sent as cached system blocks; only the rolling
 * messages vary. Keeps multi-turn chats cheap.
 *
 * Rate limited per IP. ANTHROPIC_API_KEY from env.
 */

const MODEL = 'claude-haiku-4-5-20251001';
const MAX_LESSON_CHARS = 9000;   // cap grounding context (~2.2k tokens)
const MAX_TURNS = 12;            // keep the last N messages
const MAX_MSG_CHARS = 1500;      // cap a single student message

const SYSTEM_PROMPT = `You are a friendly, encouraging GCSE tutor (for a UK student aged 15-16) helping with ONE specific lesson. Your goal is to get the student past whatever is blocking them and then back to their studying — NOT to keep them chatting. A good session is short and ends with the student confident enough to carry on without you.

Follow this arc:

1. DIAGNOSE first. Work out the ONE thing they're actually stuck on or missing. Ask a focused question or two to pinpoint it rather than guessing — don't launch into explaining before you understand the gap.

2. COACH them across it, Socratically. Nudge with a guiding question or a small hint so they reach the understanding themselves. Escalate to a bigger hint only if they're still stuck. Never write their practice or exam answer for them.

3. WRAP UP as soon as the gap is filled — when they explain it back correctly or clearly get it. Do NOT keep the conversation going. To wrap up:
   - Briefly affirm what they now understand ("You've got it — X happened because of Y, not Z.").
   - Give ONE quick, concrete revision technique to lock it in, suited to this material — e.g. "close the page and write that cause-and-consequence chain from memory", "make a flashcard: front 'why did X happen?', back your reason", "in ten minutes, explain it out loud without looking", or sketch a quick timeline/diagram.
   - Send them on their way: nudge them to try the practice question or move on, and say they can come back if they hit another wall.
   - Then STOP. Do NOT end with a further question that pulls them back into the chat.

Do not pad the conversation, fish for more engagement, or invent new things to discuss. Once they've understood, let them go.

Staying grounded:
- Base everything on the LESSON CONTENT provided below. If they ask about something outside this lesson, help briefly if it's general knowledge, then steer back. If the lesson doesn't cover something, say so honestly rather than inventing facts.

Style:
- British English. Warm, clear, concise — usually 2-4 sentences, one question at a time. No markdown headings or bullet-point dumps; talk like a patient teacher.
- If a student seems upset or mentions something worrying, be kind and suggest they talk to their teacher or a trusted adult.`;


module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // Only serve calls from our own site — a casual-abuse deterrent (a determined
  // scripter can spoof Origin, so the per-IP rate limit below is the real
  // backstop). Browsers always send Origin on POST. Allows production, any
  // Vercel preview deployment, and localhost.
  const origin = req.headers.origin || '';
  const okOrigin =
    /^https:\/\/(www\.)?studyvault\.co\.uk$/.test(origin) ||
    /^https:\/\/[a-z0-9-]+\.vercel\.app$/.test(origin) ||
    /^http:\/\/localhost(:\d+)?$/.test(origin);
  if (!okOrigin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { lessonTitle, lessonText, messages } = req.body || {};

  if (!Array.isArray(messages) || messages.length === 0) {
    return res.status(400).json({ error: 'Missing messages' });
  }

  // Sanitise + clamp the conversation: keep the last MAX_TURNS, valid roles only.
  const cleanMessages = messages
    .filter(m => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string' && m.content.trim())
    .slice(-MAX_TURNS)
    .map(m => ({ role: m.role, content: m.content.slice(0, MAX_MSG_CHARS) }));

  if (!cleanMessages.length || cleanMessages[cleanMessages.length - 1].role !== 'user') {
    return res.status(400).json({ error: 'Conversation must end with a student message' });
  }

  // Rate limit (in-memory, per IP, resets on redeploy)
  const ip = req.headers['x-forwarded-for'] || req.connection?.remoteAddress || 'unknown';
  const now = Date.now();
  const windowMs = 60 * 60 * 1000;
  if (!global._tutorRates) global._tutorRates = {};
  const rates = global._tutorRates;
  rates[ip] = (rates[ip] || []).filter(ts => now - ts < windowMs);
  if (rates[ip].length >= 80) {
    return res.status(429).json({ error: "You've asked the tutor a lot in the last hour — take a short break and try again soon." });
  }
  rates[ip].push(now);

  const lessonContext = 'LESSON: ' + (lessonTitle || 'Untitled') + '\n\n'
    + 'LESSON CONTENT (the only material this lesson covers):\n'
    + String(lessonText || '').slice(0, MAX_LESSON_CHARS);

  try {
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
        model: MODEL,
        max_tokens: 400,
        temperature: 0.5,
        // System = stable instructions + lesson content. cache_control on the
        // lesson block caches the whole prefix (system prompt + lesson) across
        // the conversation's turns; only `messages` varies request to request.
        system: [
          { type: 'text', text: SYSTEM_PROMPT },
          { type: 'text', text: lessonContext, cache_control: { type: 'ephemeral' } },
        ],
        messages: cleanMessages,
      }),
    });

    if (!resp.ok) {
      const detail = await resp.text();
      console.error('Tutor API error:', resp.status, detail);
      return res.status(502).json({ error: 'Tutor unavailable', detail: detail.slice(0, 200) });
    }

    const data = await resp.json();
    const reply = (data.content || []).map(b => b.text || '').join('').trim();
    return res.status(200).json({ reply, model: MODEL });
  } catch (err) {
    console.error('Tutor error:', err.message);
    return res.status(502).json({ error: 'Tutor failed', detail: err.message });
  }
};
