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

const GEN_MODEL = 'claude-haiku-4-5-20251001';
const MAX_TEXT_LEN = 4000; // a single paragraph; reject anything pathological

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  var body = req.body || {};
  var text = typeof body.text === 'string' ? body.text : '';
  var level = body.level === 'simple' ? 'simple' : 'simple'; // v1: single level
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

    var simplified = await generate(text, glossaryTerms);
    simplified = (simplified || '').trim();
    if (!simplified) return res.status(502).json({ error: 'Empty simplification' });

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
        gen_model: GEN_MODEL,
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

function sha256(s) {
  return crypto.createHash('sha256').update(s, 'utf8').digest('hex');
}

function buildSystemPrompt(glossaryTerms) {
  var termLine = glossaryTerms.length
    ? glossaryTerms.join(', ')
    : '(none for this lesson)';
  return [
    'You rewrite GCSE revision text into plainer English for students with a lower reading age or who are learning English as an additional language.',
    '',
    'Rules you must never break:',
    '1. Keep every one of these exact subject terms unchanged — simplify the sentence around them, never replace them with easier words and never define them away: ' + termLine + '.',
    '2. Never change any number, date, name, place, or quotation. Never change a fact.',
    '3. Never add a new point and never remove a point. Same information, simpler wording.',
    '4. Use shorter sentences and everyday words. Break long sentences into two if it helps. Keep roughly the same overall length.',
    '5. Keep a neutral, factual tone. Do not address the student ("you"), do not add encouragement, do not add commentary.',
    '6. Output ONLY the rewritten text. No preamble, no notes, no quotation marks around it.'
  ].join('\n');
}

async function generate(text, glossaryTerms) {
  return callAnthropic(buildSystemPrompt(glossaryTerms), text, GEN_MODEL, 700, 0.2);
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
