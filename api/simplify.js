/**
 * Simplify Language — generation endpoint
 *
 * Rewrites a single lesson paragraph into plainer English on demand, then
 * caches it. First viewer of a unique paragraph pays ~1s of Haiku; everyone
 * after reads the cache for free. An async Sonnet QA pass (api/simplify-qa.js)
 * blesses or rejects each cache row off the student's critical path.
 *
 * This is a READ-ONLY consumer of canonical content. It never touches
 * lessons.content_html or narration_manifest.
 *
 * POST /api/simplify
 * Body: { text, level?, lessonId?, paragraphIndex?, subjectSlug?, glossaryTerms? }
 *   - text          : the original paragraph text (plain)
 *   - level         : target level ('simple' for v1)
 *   - glossaryTerms : array of exact subject terms that must survive verbatim
 *
 * Response: { simplified, hash, status, useOriginal, needsQa }
 *   - useOriginal:true => the cached entry failed QA; render the original text
 *   - needsQa:true      => caller should fire POST /api/simplify-qa { hash }
 *
 * Rate limited per IP (anonymous free users can call this). Keys in env vars.
 * Mirrors api/ai-mark.js for the AI-call + rate-limit shape.
 */

const crypto = require('crypto');
const { supabase } = require('./pipeline/_lib/supabase');

// Leveling is a trivial task -> Haiku. "Explain it differently" reframes with
// an analogy (a reasoning task) -> Sonnet.
const SIMPLE_MODEL = 'claude-haiku-4-5-20251001';
const EXPLAIN_MODEL = 'claude-sonnet-4-6';
const MAX_TEXT_LEN = 4000; // a single paragraph; reject anything pathological

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  var body = req.body || {};
  var text = typeof body.text === 'string' ? body.text : '';
  var level = body.level === 'explain' ? 'explain' : 'simple';
  var lessonId = body.lessonId || null;
  var paragraphIndex = body.paragraphIndex || null;
  var subjectSlug = body.subjectSlug || null;
  var glossaryTerms = Array.isArray(body.glossaryTerms) ? body.glossaryTerms : [];

  if (!text.trim()) return res.status(400).json({ error: 'Missing text' });
  if (text.length > MAX_TEXT_LEN) return res.status(400).json({ error: 'Text too long' });

  // --- Rate limiting (per IP, in-memory, resets on redeploy) ---
  var ip = req.headers['x-forwarded-for'] || (req.connection && req.connection.remoteAddress) || 'unknown';
  var now = Date.now();
  var windowMs = 60 * 60 * 1000; // 1 hour
  if (!global._simplifyRates) global._simplifyRates = {};
  var rates = global._simplifyRates;
  rates[ip] = (rates[ip] || []).filter(function (ts) { return now - ts < windowMs; });
  var LIMIT = 120; // per hour — generous; cache hits don't count (returned before push)

  var hash = sha256(normalise(text)) ;

  // --- Lead-in guard ---
  // Paragraphs that introduce content which follows — list intros ending in a
  // colon, rhetorical questions ending in a question mark, or very short
  // fragments — must NOT be simplified. There is nothing to simplify, and the
  // model tends to "complete" them by inventing the list/answer that lives in
  // the paragraphs AFTER this one (which this per-paragraph call never sees).
  // Serve the original (already plain) and never spend a token on them.
  var trimmedText = text.trim();
  if (/[:?]\s*$/.test(trimmedText) || trimmedText.split(/\s+/).length <= 8) {
    return res.status(200).json({ simplified: null, hash: hash, status: 'skip', useOriginal: true, needsQa: false });
  }

  try {
    // --- Cache lookup ---
    var existing = await supabase
      .from('simplify_cache')
      .select('simplified_text, qa_status')
      .eq('original_hash', hash)
      .eq('target_level', level)
      .maybeSingle();

    if (existing.data) {
      var st = existing.data.qa_status;
      if (st === 'fail' || st === 'pending_review') {
        // Known-bad simplification — serve the canonical original instead.
        return res.status(200).json({ simplified: null, hash: hash, status: st, useOriginal: true, needsQa: false });
      }
      // pass or pending — serve the cached text. Cache hits are free (no
      // rate-limit charge, no model call).
      return res.status(200).json({
        simplified: existing.data.simplified_text,
        hash: hash,
        status: st,
        useOriginal: false,
        needsQa: st === 'pending'
      });
    }

    // --- Cache miss: this call costs a model token, so it's rate-limited ---
    if (rates[ip].length >= LIMIT) {
      return res.status(429).json({ error: 'Rate limit exceeded. Try again later.' });
    }
    rates[ip].push(now);

    // Only the subject terms that ACTUALLY appear in this paragraph are
    // constraints — the glossary is lesson-level, so most paragraphs contain
    // none of them. Passing the full list made the model (and QA) treat absent
    // terms as "missing" and fail faithful simplifications.
    var presentTerms = termsInText(glossaryTerms, text);
    var simplified = cleanOutput(await generate(text, presentTerms, level));
    if (!simplified) return res.status(502).json({ error: 'Empty simplification' });
    var genModel = level === 'explain' ? EXPLAIN_MODEL : SIMPLE_MODEL;

    // Insert as pending. Use upsert on the unique key to absorb the race where
    // two first-viewers hit a cold paragraph simultaneously.
    var upsert = await supabase
      .from('simplify_cache')
      .upsert({
        original_hash: hash,
        target_level: level,
        lesson_id: lessonId,
        paragraph_index: paragraphIndex,
        subject_slug: subjectSlug,
        original_text: text,
        simplified_text: simplified,
        qa_status: 'pending',
        gen_model: genModel,
        regen_count: 0
      }, { onConflict: 'original_hash,target_level' })
      .select('simplified_text, qa_status')
      .maybeSingle();

    // If the upsert raced and the winning row is already failed, respect it.
    if (upsert.data && (upsert.data.qa_status === 'fail' || upsert.data.qa_status === 'pending_review')) {
      return res.status(200).json({ simplified: null, hash: hash, status: upsert.data.qa_status, useOriginal: true, needsQa: false });
    }
    var served = (upsert.data && upsert.data.simplified_text) || simplified;

    return res.status(200).json({
      simplified: served,
      hash: hash,
      status: 'pending',
      useOriginal: false,
      needsQa: true
    });
  } catch (err) {
    console.error('Simplify error:', err.message);
    return res.status(502).json({ error: 'Simplification failed', detail: err.message });
  }
};

// --- Helpers ---

function normalise(s) {
  // Whitespace-insensitive so trivial markup/spacing differences share a cache
  // row, but otherwise faithful to the source text.
  return String(s).replace(/\s+/g, ' ').trim();
}

// Subject terms that actually occur in this paragraph (case-insensitive). The
// glossary is lesson-level, so a given paragraph usually contains none.
function termsInText(terms, text) {
  var lc = (text || '').toLowerCase();
  return (terms || []).filter(function (t) {
    return t && lc.indexOf(String(t).toLowerCase()) >= 0;
  });
}

// The model occasionally emits markdown (a leading "# heading", **bold**). We
// render output as plain text, so strip those artefacts.
function cleanOutput(s) {
  return String(s || '')
    .replace(/^\s*#{1,6}\s+/gm, '')
    .replace(/\*\*/g, '')
    .trim();
}

function sha256(s) {
  return crypto.createHash('sha256').update(s, 'utf8').digest('hex');
}

// Leveling: same facts, plainer wording. `presentTerms` are subject terms that
// actually occur in this paragraph (already filtered), so the rule only fires
// when there's something to preserve.
function buildSimpleSystemPrompt(presentTerms) {
  var termRule = presentTerms.length
    ? '1. This paragraph contains these exact subject terms: ' + presentTerms.join(', ') + '. Keep each of them unchanged — simplify the sentence around them, never replace them with easier words and never define them away.'
    : '1. Keep any specialist subject term that appears unchanged — simplify the sentence around it, never swap it for an easier word.';
  return [
    'You rewrite GCSE revision text into plainer English for students with a lower reading age or who are learning English as an additional language.',
    '',
    'Rules you must never break:',
    termRule,
    '2. Never change any number, date, name, place, or quotation. Never change a fact.',
    '3. Never add a new point and never remove a point. Same information, simpler wording. If the text is an introduction, a rhetorical question, or ends with a colon pointing to a list or section, rewrite ONLY the words you are given — do not answer the question and do not fill in or list the items it introduces. That content is in other paragraphs you cannot see.',
    '4. Use shorter sentences and everyday words. Break long sentences into two if it helps. Keep roughly the same overall length.',
    '5. Keep a neutral, factual tone. Do not address the student ("you"), do not add encouragement, do not add commentary.',
    '6. Output ONLY the rewritten text as plain prose. No markdown, no headings, no preamble, no notes, no quotation marks around it.'
  ].join('\n');
}

// Re-teaching: explain the same idea a different way, with an everyday analogy.
function buildExplainSystemPrompt(presentTerms) {
  var termRule = presentTerms.length
    ? '3. Keep using these subject terms from the paragraph (do not avoid them — the student is examined on them): ' + presentTerms.join(', ') + '.'
    : '3. Where the paragraph uses a specialist subject term, keep using it — do not avoid it, the student is examined on it.';
  return [
    'You are a GCSE teacher re-explaining a tricky paragraph to a student who did not follow the textbook version. Explain the SAME idea a different way, using an everyday analogy or concrete example to make it click.',
    '',
    'Rules you must never break:',
    '1. The analogy must be accurate — it must not imply anything false about the real concept. A misleading analogy is worse than none.',
    '2. Do not contradict or change any fact, number, date, name, or quotation from the original. If the paragraph is an introduction or a rhetorical question that points to content which follows, explain only the idea actually stated — do not answer the question or fill in the list it introduces (that content is in other paragraphs you cannot see).',
    termRule,
    '4. Keep it short — 2 to 4 sentences. Lead with the analogy or plain-language framing, then connect it back to the lesson idea.',
    '5. A warm, plain teacher voice is fine; you may address the student ("imagine you…"). Do not add unrelated facts or padding.',
    '6. Output ONLY the explanation as plain prose. No markdown, no preamble, no notes, no quotation marks around it.'
  ].join('\n');
}

async function generate(text, glossaryTerms, level) {
  if (level === 'explain') {
    return callAnthropic(buildExplainSystemPrompt(glossaryTerms), text, EXPLAIN_MODEL, 600, 0.6);
  }
  return callAnthropic(buildSimpleSystemPrompt(glossaryTerms), text, SIMPLE_MODEL, 700, 0.2);
}

async function callAnthropic(system, prompt, model, maxTokens, temperature) {
  var key = process.env.ANTHROPIC_API_KEY;
  if (!key) throw new Error('ANTHROPIC_API_KEY not configured');

  var resp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model,
      max_tokens: maxTokens || 600,
      temperature: typeof temperature === 'number' ? temperature : 0.2,
      system: system,
      messages: [{ role: 'user', content: prompt }]
    })
  });

  if (!resp.ok) {
    var err = await resp.text();
    throw new Error('Anthropic API error: ' + resp.status + ' ' + err);
  }
  var data = await resp.json();
  return data.content[0].text;
}
