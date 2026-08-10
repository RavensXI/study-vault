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
 *   Prefer callClaudeText() — it joins every text block. Do NOT read
 *   content[0].text: a thinking-enabled model (Sonnet 5 thinks by default)
 *   returns [thinking, text], so content[0] is the thinking block and has no
 *   .text. callClaude() returns the raw Message for callers that need usage
 *   or stop_reason.
 */

// Which Bedrock model serves the "bigger than Haiku" tier — the exam tier in
// ai-mark, the explain model in simplify, the QA model in simplify-qa, and
// revision-strategy.
//
// Sonnet 4.6 — the model the exam tier ran on before this migration, so on
// Bedrock the marking behaviour is unchanged and only its location moves.
// Sonnet 5 is listed in eu-west-2 but returned AccessDeniedException on this
// account (10 Aug 2026), a per-model entitlement gate; retry it here once AWS
// lifts that, since untruncated it was the best marker in the bake-off (98%).
// Do NOT put Haiku here: it marks long answers far too generously — 5/6 for
// invented Dickens quotations, 2/4 for a conservation-of-energy error.
const SONNET_TIER = 'anthropic.claude-sonnet-4-6';

// Bedrock carries an `anthropic.` provider prefix and drops date suffixes.
// NOTE: there is no `anthropic.claude-sonnet-4-6` — Sonnet 4.6 is not served
// on Bedrock at all, so every 4.6 caller has to move regardless.
// IDs verified against this account with:
//   aws bedrock list-foundation-models --region eu-west-2 --by-provider anthropic
// Note they are NOT uniform: Haiku 4.5 carries a date and version suffix,
// while Sonnet 4.6 / Sonnet 5 / the Opus 4.7+ line are bare. Guessing a
// consistent scheme is what produced "The model ... does not exist" twice.
const BEDROCK_MODEL_IDS = {
  'claude-haiku-4-5-20251001': 'anthropic.claude-haiku-4-5-20251001-v1:0',
  'claude-haiku-4-5': 'anthropic.claude-haiku-4-5-20251001-v1:0',
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

  if (!onBedrock) return viaAnthropic(payload);

  // TEMPORARY SAFETY NET (10 Aug 2026).
  //
  // Bedrock is refusing every model ID we have tried in eu-west-2 — both the
  // bare `anthropic.claude-haiku-4-5` and the `eu.`-prefixed inference-profile
  // form come back "does not exist", while the same account reaches Haiku fine
  // in the console playground. The likeliest explanation is that the playground
  // uses Bedrock's older InvokeModel integration and this account has no access
  // to the newer bedrock-mantle endpoint at all, in which case the fix is the
  // legacy client rather than a different ID.
  //
  // Until that is settled with evidence rather than guesswork, a Bedrock
  // failure falls back to the direct API instead of taking AI marking, the
  // tutor and simplify down with it. The fallback is LOUD (console.error, one
  // line per failure) precisely so this cannot become permanent by accident:
  // while it is firing, pupil work is still going to the US and the residency
  // claim is NOT yet true.
  //
  // Remove this the moment the correct transport is confirmed.
  try {
    return await viaBedrock(payload);
  } catch (err) {
    console.error('[claude] Bedrock failed, falling back to api.anthropic.com —',
      'DATA IS LEAVING THE UK. Model:', payload.model, '| Error:', err.message);
    return viaAnthropic(Object.assign({}, body));
  }
}


/**
 * Model IDs to try, in order.
 *
 * eu-west-2 is not one of Bedrock's "in-region only" regions, so it cannot
 * serve a bare model ID — it needs a cross-region inference profile, which is
 * the same ID carrying a geography prefix (`eu.` for European regions, `us.`
 * for US, `apac.` for Asia-Pacific). A bare ID there fails with the unhelpful
 * "The model 'x' does not exist" rather than anything about profiles.
 *
 * Both forms are tried because which one a region accepts is not reliably
 * documented and does vary: `us-east-1` takes the bare ID, `eu-west-2` does
 * not. Trying costs one wasted round trip on the first call after a deploy;
 * guessing wrong costs an outage.
 */
function modelCandidates(model) {
  const region = String(process.env.AWS_REGION || '');
  const geo = region.startsWith('eu-') ? 'eu.'
    : region.startsWith('us-') ? 'us.'
    : region.startsWith('ap-') ? 'apac.'
    : '';
  return geo ? [geo + model, model] : [model];
}


async function viaBedrock(payload) {
  const candidates = modelCandidates(payload.model);
  let lastErr = null;

  for (const model of candidates) {
    try {
      return await bedrockClient().messages.create(
        Object.assign({}, payload, { model: model })
      );
    } catch (err) {
      lastErr = err;
      const msg = (err && err.message) || String(err);
      // Only a "no such model" is worth retrying under a different ID form.
      // A permission or validation error means the ID was understood and the
      // problem is elsewhere — retrying just doubles the latency of the failure.
      if (!/does not exist|ValidationException|ResourceNotFound/i.test(msg)) break;
    }
  }

  throw new Error('Bedrock error: ' + ((lastErr && lastErr.message) || lastErr));
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
