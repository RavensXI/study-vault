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
const SIMPLE_MODEL = 'claude-haiku-4-5-20251001';
const EXPLAIN_MODEL = 'claude-sonnet-4-6';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // Only serve calls from our own site (same pattern as api/tutor.js).
  var origin = req.headers.origin || '';
  var okOrigin =
    /^https:\/\/(www\.)?studyvault\.co\.uk$/.test(origin) ||
    /^https:\/\/[a-z0-9-]+\.vercel\.app$/.test(origin) ||
    /^http:\/\/localhost(:\d+)?$/.test(origin);
  if (!okOrigin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  var body = req.body || {};
  var hash = typeof body.hash === 'string' ? body.hash : '';
  var level = body.level === 'explain' ? 'explain' : 'simple';
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
      .select('id, lesson_id, target_level, original_text, simplified_text, qa_status, regen_count')
      .eq('original_hash', hash)
      .eq('target_level', level)
      .maybeSingle();

    if (!row.data) return res.status(404).json({ error: 'Cache row not found' });

    // Trust the stored level for prompt selection, not the client.
    var rowLevel = row.data.target_level === 'explain' ? 'explain' : 'simple';

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

    // Only terms that actually occur in this paragraph are constraints (the
    // glossary is lesson-level). Without this filter, faithful simplifications
    // of paragraphs that don't mention a glossary term were wrongly failed.
    var presentTerms = termsInText(glossaryTerms, original);

    // First QA pass
    var verdict = await runQa(rowLevel, lessonTitle, presentTerms, original, simplified);

    // Fail + not yet regenerated -> regenerate once and re-check
    if (!verdict.pass && (row.data.regen_count || 0) < 1) {
      var regen = cleanOutput(await generate(original, presentTerms, rowLevel));
      regenerated = true;
      if (regen) {
        simplified = regen;
        verdict = await runQa(rowLevel, lessonTitle, presentTerms, original, simplified);
      }
    }

    var update = {
      qa_model: QA_MODEL,
      qa_notes: (verdict.reason || '') + (verdict.issues && verdict.issues.length ? ' | ' + verdict.issues.join('; ') : '')
    };
    if (regenerated) {
      update.simplified_text = simplified;
      update.gen_model = rowLevel === 'explain' ? EXPLAIN_MODEL : SIMPLE_MODEL;
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

function simpleQaSystem() {
  return [
    'You are a faithfulness checker for simplified GCSE revision text.',
    'You are given a lesson title, a list of subject terms that appear in this paragraph (may be empty), the ORIGINAL paragraph, and a SIMPLIFIED rewrite.',
    'Decide whether the simplified version is safe to show students.',
    '',
    'It passes only if ALL of these hold:',
    '- Every number, date, name, place and quotation in the original is preserved exactly.',
    '- Each listed subject term that appears in the ORIGINAL is still present in the simplified version (not swapped for an easier word). If the term list is empty, skip this check entirely — do NOT require any term.',
    '- No new claim has been added and no existing point has been dropped.',
    '- It reads more simply than the original (shorter sentences / commoner words).',
    '',
    'Reply with ONLY a JSON object, no other text:',
    '{"pass": true|false, "reason": "<one short sentence>", "issues": ["<specific problem>", ...]}'
  ].join('\n');
}

function explainQaSystem() {
  return [
    'You are checking an alternative "explain it differently" rewrite of a GCSE revision paragraph. The rewrite is meant to re-teach the SAME idea a different way, usually with an everyday analogy.',
    'You are given a lesson title, the required subject terms, the ORIGINAL paragraph, and the ALTERNATIVE explanation.',
    'Decide whether the alternative is safe to show students.',
    '',
    'It passes only if ALL of these hold:',
    '- The analogy / reframing is ACCURATE — it does not imply anything false or misleading about the real concept. This is the most important check.',
    '- It does not contradict or change any fact, number, date, name or quotation in the original.',
    '- It actually explains the same idea as the original (not a different topic).',
    '- It is genuinely a clearer / more intuitive explanation, not just a reworded copy.',
    '',
    'Reply with ONLY a JSON object, no other text:',
    '{"pass": true|false, "reason": "<one short sentence>", "issues": ["<specific problem>", ...]}'
  ].join('\n');
}

async function runQa(level, lessonTitle, presentTerms, original, simplified) {
  var system = level === 'explain' ? explainQaSystem() : simpleQaSystem();
  var altLabel = level === 'explain' ? 'ALTERNATIVE EXPLANATION:' : 'SIMPLIFIED:';
  var user = [
    'LESSON TITLE: ' + (lessonTitle || '(unknown)'),
    'SUBJECT TERMS IN THIS PARAGRAPH: ' + (presentTerms.length ? presentTerms.join(', ') : '(none — skip the term check)'),
    '',
    'ORIGINAL:',
    original,
    '',
    altLabel,
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

// Subject terms that actually occur in this paragraph (case-insensitive).
function termsInText(terms, text) {
  var lc = (text || '').toLowerCase();
  return (terms || []).filter(function (t) {
    return t && lc.indexOf(String(t).toLowerCase()) >= 0;
  });
}

// Strip markdown the model sometimes emits; output is rendered as plain text.
function cleanOutput(s) {
  return String(s || '')
    .replace(/^\s*#{1,6}\s+/gm, '')
    .replace(/\*\*/g, '')
    .trim();
}

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

async function generate(text, presentTerms, level) {
  if (level === 'explain') {
    return callAnthropic(buildExplainSystemPrompt(presentTerms), text, EXPLAIN_MODEL, 600, 0.6);
  }
  return callAnthropic(buildSimpleSystemPrompt(presentTerms), text, SIMPLE_MODEL, 700, 0.2);
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
