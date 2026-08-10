/**
 * Single entry point for every Claude call the API makes.
 *
 * WHY THIS EXISTS
 *   Five routes (ai-mark, tutor, simplify, simplify-qa, revision-strategy)
 *   each built their own fetch to api.anthropic.com, which meant pupil work
 *   left the UK on five separate code paths. Routing them through here lets
 *   one env-var change move all five into Europe.
 *
 * HOW IT ROUTES
 *   AWS credentials present  -> Amazon Bedrock, London (eu-west-2), EU
 *                               inference profile. Data stays in the EEA.
 *   AWS credentials absent   -> api.anthropic.com, exactly as before.
 *
 *   The fallback is deliberate: until AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
 *   / AWS_REGION are set in Vercel, behaviour is byte-for-byte what it was.
 *   Nothing to co-ordinate, nothing to roll back if the keys are wrong.
 *
 * CALLERS PASS A NORMAL MESSAGES-API BODY.
 *   Same object you would have handed to fetch(). Model IDs stay first-party
 *   (`claude-haiku-4-5-20251001`); the Bedrock prefix and the Sonnet upgrade
 *   are applied here so no call site has to know which transport it is on.
 *   The return value is the parsed Message, so `data.content[0].text` and
 *   `(data.content || []).map(b => b.text)` keep working unchanged.
 */

// Which Bedrock model serves the "bigger than Haiku" tier — the exam tier in
// ai-mark, the explain model in simplify, the QA model in simplify-qa, and
// revision-strategy.
//
// ⚠ Sonnet 5 is DENIED on this AWS account (AccessDeniedException, "not
// available for this account", 10 Aug 2026) — a new-account entitlement gate,
// not a per-region model-access setting. Until AWS grants it, this points at
// Haiku, which the bake-off (scripts/model-eval/) found scores BETTER than
// Sonnet at production settings anyway: 81% vs 69%, because Sonnet overruns
// max_tokens on half its calls and gets truncated.
//
// Change this ONE line when AWS opens up a bigger model:
//   'anthropic.claude-opus-4-8'  — if Opus 4.8 is available
//   'anthropic.claude-sonnet-5'  — once the Sonnet gate is lifted
const SONNET_TIER = 'anthropic.claude-haiku-4-5';

// Bedrock carries an `anthropic.` provider prefix and drops date suffixes.
// NOTE: there is no `anthropic.claude-sonnet-4-6` — Sonnet 4.6 is not served
// on Bedrock at all, so every 4.6 caller has to move regardless.
const BEDROCK_MODEL_IDS = {
  'claude-haiku-4-5-20251001': 'anthropic.claude-haiku-4-5',
  'claude-haiku-4-5': 'anthropic.claude-haiku-4-5',
  'claude-sonnet-4-6': SONNET_TIER,
  'claude-sonnet-5': SONNET_TIER,
  'claude-opus-4-8': 'anthropic.claude-opus-4-8',
};

// Sonnet 5 rejects a non-default `temperature` outright (HTTP 400,
// "`temperature` is deprecated for this model"). simplify.js and
// simplify-qa.js both send 0.2 with what used to be Sonnet 4.6, so without
// this both routes would break the moment Bedrock is switched on.
const REJECTS_TEMPERATURE = new Set([
  'anthropic.claude-sonnet-5',
  'claude-sonnet-5',
]);

function useBedrock() {
  return Boolean(
    process.env.AWS_ACCESS_KEY_ID &&
    process.env.AWS_SECRET_ACCESS_KEY &&
    process.env.AWS_REGION
  );
}

let _bedrock = null;
function bedrockClient() {
  if (!_bedrock) {
    // Required lazily so the dependency is only needed once Bedrock is
    // actually configured — a deploy without the package still serves every
    // route via the direct path rather than failing at import time.
    const { AnthropicBedrockMantle } = require('@anthropic-ai/bedrock-sdk');
    _bedrock = new AnthropicBedrockMantle({ awsRegion: process.env.AWS_REGION });
  }
  return _bedrock;
}


/**
 * Send a Messages API request. Returns the parsed response object.
 * Throws Error on failure, with the provider's detail in the message.
 */
async function callClaude(body) {
  const onBedrock = useBedrock();
  const payload = Object.assign({}, body);

  if (onBedrock) {
    const mapped = BEDROCK_MODEL_IDS[payload.model];
    if (!mapped) {
      // An unmapped model is a bug, not a runtime condition — fail loudly here
      // rather than letting Bedrock return an opaque 404 on a model ID it has
      // never heard of.
      throw new Error('No Bedrock model mapping for "' + payload.model + '"');
    }
    payload.model = mapped;
  }

  // Applied AFTER mapping and on BOTH transports: Sonnet 5 rejects the
  // parameter wherever it is served, so stripping it only on the Bedrock path
  // would still 400 anyone who moves a caller to Sonnet 5 directly.
  if (REJECTS_TEMPERATURE.has(payload.model)) delete payload.temperature;

  return onBedrock ? viaBedrock(payload) : viaAnthropic(payload);
}


async function viaBedrock(payload) {
  try {
    return await bedrockClient().messages.create(payload);
  } catch (err) {
    throw new Error('Bedrock error: ' + (err && err.message ? err.message : err));
  }
}


async function viaAnthropic(body) {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) throw new Error('ANTHROPIC_API_KEY not configured');

  const resp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const detail = await resp.text();
    throw new Error('Anthropic API error: ' + resp.status + ' ' + detail);
  }
  return resp.json();
}


/** Convenience for the common "system + one user turn, give me the text" shape. */
async function callClaudeText(body) {
  const data = await callClaude(body);
  return (data.content || []).map(b => b.text || '').join('');
}


module.exports = { callClaude, callClaudeText, useBedrock };
