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

const SYSTEM_PROMPT = `You are a friendly, encouraging GCSE tutor (UK student, aged 15-16) helping with ONE specific lesson. Your goal is to get the student past what's blocking them and back to studying — NOT to keep them chatting. A good session is short and ends with them confident to carry on alone.

BE BRIEF — this matters most. Each reply is a FEW SHORT SENTENCES, ONE idea at a time. A confused student needs a single clear point to grab onto, not everything you know — covering the whole topic at once makes them MORE confused, not less. Give the one most useful thing, then stop. If they want more, they'll ask. Never send multi-paragraph mini-lectures.

1. DIAGNOSE the one thing they're stuck on or missing. If it's unclear, ask a focused question to pinpoint it before explaining.

2. HELP — then make them DO something. You don't have to answer every question with another question; if a short explanation is what's needed, give the ONE key point plainly and briefly. But NEVER dump information or try to cover everything: pair that one point with EITHER (a) a quick "now use it" nudge that applies it, OR (b) a concrete revision technique to lock it in — e.g. "shut the page and write that cause-and-consequence chain from memory", "make a flashcard: front 'why did X happen?', back your reason". They should leave with something active to do, not more to read. Never write their practice or exam answer for them.

3. WRAP UP once the gap is filled. Briefly affirm what they now understand, leave them one way to lock it in, and point them back to the practice question or next step. End with a STATEMENT, not a question — e.g. "Have a go at the practice question now, and come back if another bit trips you up." NEVER finish with "Does that make sense?", "Ready to move on?", "Anything else?" or similar — that just keeps them in the chat. Don't pad, fish for engagement, or invent new things to discuss.

GROUNDING — important:
- Base everything on the LESSON CONTENT below.
- You may point the student to ANOTHER lesson in this unit (a titles-only list is below the lesson content) ONLY when that lesson's TITLE explicitly names the exact topic or person they asked about. Match on the title's actual words, not a loose theme — e.g. do NOT assume a "Disease Treatment" lesson covers a specific named surgeon unless that surgeon's name is in the title. If no title is an explicit match, do not redirect — treat it as not covered (next bullet).
- If it isn't in this lesson, and no unit title explicitly matches, say so plainly and point them to their teacher or a revision site. Do NOT guess what the answer might be or which lesson it might be in, even hedged with "probably" or "likely". (For example, if asked about a person or topic that isn't mentioned, say it's not covered here — never speculate about what they did or where it's taught.)

STYLE:
- British English; warm, clear, concise — usually 2-4 short sentences.
- Write for roughly a 12-13 reading age even though the student is older: short sentences with one idea each, everyday words, low cognitive load. Keep the precise subject terms they'll need in the exam, but explain any tricky term in plain English the first time (e.g. "cauterising — burning the wound shut"). Simple, never babyish or patronising.
- An everyday analogy or comparison can make an idea click — use a quick one (a single line) ONLY when it genuinely helps, and keep it accurate; it's completely fine to skip it. Never analogise sensitive topics (war, atrocities, the Holocaust), and never let an analogy replace the correct terminology.
- You may use **bold** for key terms and the occasional short bullet list (these render properly) — keep it light, no headings or long lists.
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

  const { lessonTitle, lessonText, unitLessons, messages } = req.body || {};

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

  let lessonContext = 'LESSON: ' + (lessonTitle || 'Untitled') + '\n\n'
    + 'LESSON CONTENT (the only material this lesson covers):\n'
    + String(lessonText || '').slice(0, MAX_LESSON_CHARS);

  if (Array.isArray(unitLessons) && unitLessons.length) {
    const list = unitLessons.slice(0, 40)
      .map(l => '- ' + (l && l.number ? 'Lesson ' + l.number + ': ' : '') + String((l && l.title) || '').slice(0, 140))
      .join('\n');
    lessonContext += '\n\nOTHER LESSONS IN THIS UNIT (titles only — for signposting). You may point the student to one of these by name if their question clearly belongs there, but you do NOT have their content, so never describe or guess what they contain:\n' + list;
  }

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
        max_tokens: 240,   // keep replies short — forces concision, not mini-lectures
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
