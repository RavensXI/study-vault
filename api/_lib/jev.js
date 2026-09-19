/**
 * Jev (TypeSafe System One): a decision model. State in, typed answers out with a
 * probability each. It writes nothing, so it is safe to put in front of a student.
 * $0.042 per million input tokens, output free; a flashcard judgement is ~400 tokens.
 *
 *   const { ask } = require('./_lib/jev');
 *   const r = await ask({ state, questions: { ok: noul('...'), how: score('...', ['none','part','all']) } });
 *   r.answers.ok.noul            // 0..1
 *   r.answers.how.score          // 0..criteria.length-1, fractional
 */
const ENDPOINT = 'https://api.typesafe.ai/v1/systemone';
const MODEL = process.env.JEV_MODEL || 'jev-latest';

function key() {
  return process.env.JEV_API_KEY || process.env.TYPESAFE_API_KEY || '';
}
function noul(instructions) { return { type: 'noul', instructions: instructions }; }
function score(instructions, criteria) { return { type: 'score', instructions: instructions, criteria: criteria }; }
function choice(instructions, criteria) { return { type: 'choice', instructions: instructions, criteria: criteria }; }

async function ask({ state, questions, timeoutMs }) {
  const k = key();
  if (!k) throw new Error('JEV_API_KEY is not set');
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs || 12000);
  try {
    const r = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + k, 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: MODEL, state: state, questions: questions }),
      signal: ctrl.signal
    });
    const text = await r.text();
    let data = null; try { data = JSON.parse(text); } catch (e) { /* non-JSON error body */ }
    if (!r.ok) {
      const err = new Error('Jev ' + r.status + ': ' + ((data && (data.detail || data.error)) ? JSON.stringify(data.detail || data.error).slice(0, 300) : text.slice(0, 300)));
      err.status = r.status; throw err;
    }
    return data;
  } finally { clearTimeout(t); }
}

module.exports = { ask, noul, score, choice, configured: () => !!key() };
