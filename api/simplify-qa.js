/**
 * Simplify Language — asynchronous QA endpoint
 *
 * Runs a Sonnet faithfulness check on a cached simplification, off the
 * student's critical path. Client-triggered right after the first viewer
 * renders (Vercel kills unawaited promises, so QA can't piggyback on the gen
 * response). Self-healing: any later viewer who receives needsQa:true re-fires
 * this, so an entry never stays un-QA'd just because the first viewer left.
 *
 * Checks: numbers / dates / names / quotations preserved, required subject
 * terms intact, no points added or removed, and genuinely simpler.
 *   pass               -> qa_status='pass' (blessed, served to all)
 *   fail (1st time)    -> regenerate once with Haiku, re-QA
 *   fail (after regen) -> qa_status='pending_review' (admin queue; original served)
 *
 * POST /api/simplify-qa
 * Body: { hash, level? }
 * Response: { status, regenerated }
 */

const { supabase } = require('./pipeline/_lib/supabase');

const QA_MODEL = 'claude-sonnet-4-6';
const GEN_MODEL = 'claude-haiku-4-5-20251001';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  var body = req.body || {};
  var hash = typeof body.hash === 'string' ? body.hash : '';
  var level = body.level === 'simple' ? 'simple' : 'simple';
  if (!hash) return res.status(400).json({ error: 'Missing hash' });

  // Light per-IP throttle so QA can't be weaponised into a Sonnet bill.
  var ip = req.headers['x-forwarded-for'] || (req.connection && req.connection.remoteAddress) || 'unknown';
  var now = Date.now();
  if (!global._simplifyQaRates) global._simplifyQaRates = {};
  var rates = global._simplifyQaRates;
  rates[ip] = (rates[ip] || []).filter(function (ts) { return now - ts < 60 * 60 * 1000; });
  if (rates[ip].length >= 200) return res.status(429).json({ error: 'Rate limit exceeded' });
  rates[ip].push(now);

  try {
    var row = await supabase
      .from('simplify_cache')
      .select('id, lesson_id, original_text, simplified_text, qa_status, regen_count')
      .eq('original_hash', hash)
      .eq('target_level', level)
      .maybeSingle();

    if (!row.data) return res.status(404).json({ error: 'Cache row not found' });

    // Idempotent: already resolved => no Sonnet spend.
    if (row.data.qa_status === 'pass' || row.data.qa_status === 'pending_review') {
      return res.status(200).json({ status: row.data.qa_status, regenerated: false });
    }

    // Lean QA context: glossary + title only, not the whole lesson.
    var glossaryTerms = [];
    var lessonTitle = '';
    if (row.data.lesson_id) {
      var lesson = await supabase
        .from('lessons')
        .select('title, glossary_terms')
        .eq('id', row.data.lesson_id)
        .maybeSingle();
      if (lesson.data) {
        lessonTitle = lesson.data.title || '';
        glossaryTerms = (lesson.data.glossary_terms || []).map(function (g) {
          return g && g.term ? g.term : '';
        }).filter(Boolean);
      }
    }

    var original = row.data.original_text;
    var simplified = row.data.simplified_text;
    var regenerated = false;

    // First QA pass
    var verdict = await runQa(lessonTitle, glossaryTerms, original, simplified);

    // Fail + not yet regenerated -> regenerate once and re-check
    if (!verdict.pass && (row.data.regen_count || 0) < 1) {
      var regen = (await generate(original, glossaryTerms) || '').trim();
      regenerated = true;
      if (regen) {
        simplified = regen;
        verdict = await runQa(lessonTitle, glossaryTerms, original, simplified);
      }
    }

    var update = {
      qa_model: QA_MODEL,
      qa_notes: (verdict.reason || '') + (verdict.issues && verdict.issues.length ? ' | ' + verdict.issues.join('; ') : '')
    };
    if (regenerated) {
      update.simplified_text = simplified;
      update.gen_model = GEN_MODEL;
      update.regen_count = (row.data.regen_count || 0) + 1;
    }
    update.qa_status = verdict.pass ? 'pass' : 'pending_review';

    await supabase.from('simplify_cache').update(update).eq('id', row.data.id);

    return res.status(200).json({ status: update.qa_status, regenerated: regenerated });
  } catch (err) {
    console.error('Simplify QA error:', err.message);
    return res.status(502).json({ error: 'QA failed', detail: err.message });
  }
};

// --- QA ---

async function runQa(lessonTitle, glossaryTerms, original, simplified) {
  var system = [
    'You are a faithfulness checker for simplified GCSE revision text.',
    'You are given a lesson title, the required subject terms, the ORIGINAL paragraph, and a SIMPLIFIED rewrite.',
    'Decide whether the simplified version is safe to show students.',
    '',
    'It passes only if ALL of these hold:',
    '- Every number, date, name, place and quotation in the original is preserved exactly.',
    '- Every required subject term is still present.',
    '- No new claim has been added and no existing point has been dropped.',
    '- It reads more simply than the original (shorter sentences / commoner words).',
    '',
    'Reply with ONLY a JSON object, no other text:',
    '{"pass": true|false, "reason": "<one short sentence>", "issues": ["<specific problem>", ...]}'
  ].join('\n');

  var user = [
    'LESSON TITLE: ' + (lessonTitle || '(unknown)'),
    'REQUIRED SUBJECT TERMS: ' + (glossaryTerms.length ? glossaryTerms.join(', ') : '(none)'),
    '',
    'ORIGINAL:',
    original,
    '',
    'SIMPLIFIED:',
    simplified
  ].join('\n');

  var raw = await callAnthropic(system, user, QA_MODEL, 400, 0);
  return parseVerdict(raw);
}

function parseVerdict(raw) {
  try {
    var match = String(raw).match(/\{[\s\S]*\}/);
    var obj = JSON.parse(match ? match[0] : raw);
    return {
      pass: obj.pass === true,
      reason: typeof obj.reason === 'string' ? obj.reason : '',
      issues: Array.isArray(obj.issues) ? obj.issues : []
    };
  } catch (e) {
    // Unparseable verdict => treat as fail so a human looks at it.
    return { pass: false, reason: 'QA response could not be parsed', issues: [] };
  }
}

// --- Generation (regen path) — mirrors api/simplify.js ---

function buildGenSystemPrompt(glossaryTerms) {
  var termLine = glossaryTerms.length ? glossaryTerms.join(', ') : '(none for this lesson)';
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
  return callAnthropic(buildGenSystemPrompt(glossaryTerms), text, GEN_MODEL, 700, 0.2);
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
