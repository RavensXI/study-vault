/**
 * Single entry point for every Claude call the API makes.
 *
 * WHY THIS EXISTS
 *   Four routes (ai-mark, tutor, simplify, simplify-qa) each built their own
 *   fetch to api.anthropic.com, which meant pupil work left the UK on four
 *   separate code paths. Routing them through here lets one env-var change
 *   move all of them into Europe. (A fifth, revision-strategy, went the same
 *   way and was deleted — nothing had ever called it.)
 *
 * HOW IT ROUTES
 *   AWS credentials present  -> Amazon Bedrock, London (eu-west-2), EU
 *                               inference profile. Data stays in the EEA.
 *                               A failure here is an ERROR, not a quiet
 *                               retry in the US — see "FAILS CLOSED" below.
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
// ai-mark, the explain model in simplify, and the QA model in simplify-qa.
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

// WHICH BEDROCK INTEGRATION.
//
// Bedrock has two. `AnthropicBedrockMantle` speaks the newer Messages-API
// endpoint (bedrock-mantle.{region}.api.aws); `AnthropicBedrock` speaks the
// older bedrock-runtime InvokeModel API. They take DIFFERENT model IDs and
// DIFFERENT IAM actions.
//
// This account has the legacy one. Evidence: every ID tried against Mantle
// returned "does not exist" — including the exact ID that
// `aws bedrock list-foundation-models --region eu-west-2` reports
// (anthropic.claude-haiku-4-5-20251001-v1:0) — while the console playground
// reaches the same models fine. The version-suffixed ID format is itself the
// legacy scheme.
//
// IAM: legacy needs bedrock:InvokeModel, NOT bedrock-mantle:CreateInference.
// A policy granting only the latter fails here with AccessDenied.
const USE_MANTLE = false;

let _bedrock = null;
function bedrockClient() {
  if (!_bedrock) {
    // Required lazily so the dependency is only needed once Bedrock is
    // actually configured — a deploy without the package still serves every
    // route via the direct path rather than failing at import time.
    const sdk = require('@anthropic-ai/bedrock-sdk');
    const Client = USE_MANTLE ? sdk.AnthropicBedrockMantle : sdk.AnthropicBedrock;
    _bedrock = new Client({ awsRegion: process.env.AWS_REGION });
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

  // FAILS CLOSED WHEN BEDROCK IS NOT CONFIGURED AT ALL.
  //
  // The path below this line already refuses to fall back once Bedrock IS
  // configured. This branch was the remaining hole: with the AWS variables
  // simply absent, every route quietly used api.anthropic.com and said nothing.
  // That is not a hypothetical — it is what happened the first time the
  // parents'-evening summary ran, and the only reason anyone noticed was that
  // the route reports servedBy. A preview deploy, a fresh environment, or one
  // deleted variable produces the same silence with real pupil work in it.
  //
  // "Configured for London" and "actually in London" have to be the same
  // sentence, and the way to guarantee that is for the unconfigured case to be
  // an error rather than a destination.
  if (!onBedrock) {
    if (!process.env.ALLOW_US_FALLBACK) {
      throw new Error(
        'UK AI region is not configured (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, ' +
        'AWS_REGION), and this deployment will not send content outside the UK. ' +
        'Set them, or set ALLOW_US_FALLBACK=1 to deliberately accept US processing.');
    }
    console.error('[claude] ALLOW_US_FALLBACK is set and Bedrock is NOT configured —',
      'this request is going to the US. DATA IS LEAVING THE UK. Model:', payload.model);
    const out = await viaAnthropic(payload);
    out._servedBy = 'anthropic-direct (US; BEDROCK NOT CONFIGURED)';
    return out;
  }

  // FAILS CLOSED. Once Bedrock is configured, a Bedrock failure is an error —
  // it does NOT quietly re-run the request against api.anthropic.com.
  //
  // The temptation is obvious: falling back keeps marking alive during a
  // Bedrock outage. But a residency promise that silently suspends itself
  // whenever it is inconvenient is not a promise. If we tell a school that
  // pupils' work is processed in the UK, the failure mode has to be "the
  // marking is unavailable for ten minutes", not "the marking quietly went to
  // Virginia and nobody was told".
  //
  // The escape hatch is deliberately explicit and deliberately ugly to type.
  // ALLOW_US_FALLBACK exists for a real incident where availability genuinely
  // outranks residency for a while — set it, and every fallback logs loudly and
  // is reported in servedBy, so the exposure is visible rather than assumed.
  // Unset it again afterwards.
  if (!process.env.ALLOW_US_FALLBACK) return viaBedrock(payload);

  try {
    return await viaBedrock(payload);
  } catch (err) {
    console.error('[claude] ALLOW_US_FALLBACK is set — Bedrock failed and this',
      'request is being re-run in the US. DATA IS LEAVING THE UK. Model:',
      payload.model, '| Error:', err.message);
    const out = await viaAnthropic(Object.assign({}, body));
    out._servedBy = 'anthropic-direct (US FALLBACK; bedrock failed: '
      + String(err.message).replace(/\s+/g, ' ').slice(0, 200) + ')';
    return out;
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
  // Cross-region inference profiles (the eu./us./apac. prefixes) belong to the
  // Mantle endpoint. On the legacy API the bare, version-suffixed ID is the
  // one that resolves, so try it first and keep the prefixed form only as a
  // second guess for whenever this account gains Mantle access.
  const region = String(process.env.AWS_REGION || '');
  const geo = region.startsWith('eu-') ? 'eu.'
    : region.startsWith('us-') ? 'us.'
    : region.startsWith('ap-') ? 'apac.'
    : '';
  // Prefixed FIRST on both integrations. eu-west-2 is not an "in-region only"
  // region, so it cannot serve a model on on-demand throughput at all — it
  // requires an inference profile, and the profile ID is the model ID with a
  // geography prefix. Verified from the provider's own error:
  //   "Invocation of model ID anthropic.claude-haiku-4-5-20251001-v1:0 with
  //    on-demand throughput isn't supported. Retry your request with the ID or
  //    ARN of an inference profile that contains this model."
  if (!geo) return [model];
  return [geo + model, model];
}


async function viaBedrock(payload) {
  const candidates = modelCandidates(payload.model);
  let lastErr = null;

  for (const model of candidates) {
    try {
      const out = await bedrockClient().messages.create(
        Object.assign({}, payload, { model: model })
      );
      out._servedBy = 'bedrock:' + (process.env.AWS_REGION || '?') + ':' + model;
      return out;
    } catch (err) {
      lastErr = err;
      const msg = (err && err.message) || String(err);
      // Only a "no such model" is worth retrying under a different ID form.
      // A permission or validation error means the ID was understood and the
      // problem is elsewhere — retrying just doubles the latency of the failure.
      // "inference profile" and "on-demand throughput" matter as much as the
      // not-found cases: that is the error a region gets when it needs a
      // profile ID, and omitting it here is why the retry silently never fired.
      if (!/does not exist|ValidationException|ResourceNotFound|inference profile|on-demand throughput/i.test(msg)) break;
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
  const out = await resp.json();
  out._servedBy = 'anthropic-direct:' + body.model;
  return out;
}


/** Convenience for the common "system + one user turn, give me the text" shape. */
async function callClaudeText(body) {
  const data = await callClaude(body);
  return (data.content || []).map(b => b.text || '').join('');
}


/**
 * Same as callClaudeText but also reports WHICH transport answered.
 *
 * Without this there is no way to tell from the outside whether a response
 * came from London or from the US fallback — the call sites report the model
 * they asked for, not the one that served them, so a silently failing Bedrock
 * looks identical to a working one. `servedBy` is the difference between
 * "configured for London" and "actually in London".
 */
async function callClaudeDetailed(body) {
  const data = await callClaude(body);
  return {
    text: (data.content || []).map(b => b.text || '').join(''),
    servedBy: data._servedBy || 'unknown',
  };
}


module.exports = { callClaude, callClaudeText, callClaudeDetailed, useBedrock };
