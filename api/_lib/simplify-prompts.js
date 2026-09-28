/**
 * Simplify wording — the prompts, shared by api/simplify.js (generation) and api/simplify-qa.js
 * (QA + the one regeneration). One copy, so the two can never drift apart again.
 *
 * 28 Sep 2026 (v2). Tom: the old prompt "just truncates the text into shorter sentences… pretty much
 * a word-for-word rewrite", and it twice replied to advice paragraphs ("I understand. When rewriting,
 * I will…") instead of rewriting them. Tested on 28 real paragraphs (scripts/_simplify_eval.py,
 * results in scripts/v2_simplify_eval.md): reading grade 12.9 -> 6.8 with Sonnet, QA pass 25/28, no
 * meta-replies; Haiku with the same prompt simplified but guessed wrong meanings, so generation is
 * on Sonnet. The prompt texts live in the .txt files beside this one (the eval reads the same files).
 */
const fs = require('fs');
const path = require('path');

const SIMPLE = fs.readFileSync(path.join(__dirname, 'simplify-prompt-simple.txt'), 'utf8');
const QA_SIMPLE = fs.readFileSync(path.join(__dirname, 'simplify-prompt-qa.txt'), 'utf8');

// Bump when the prompt changes: it is part of the cache key, so paragraphs are re-simplified with
// the new prompt the next time a student asks, instead of serving the old rewrite for ever.
const SIMPLE_VERSION = 'v4';   // v4 28 Sep: Sonnet 5.5 writer; prompt iterated to 30/30 on unseen paragraphs (scripts/_simplify_iterate.py)

function simpleSystem(presentTerms) {
  var terms = presentTerms && presentTerms.length
    ? 'This passage contains these exact subject terms: ' + presentTerms.join(', ') + '. Keep each of them unchanged. Simplify the sentence around them; never swap them for easier words.'
    : 'Keep every specialist subject term that appears unchanged. Simplify the sentence around it; never swap it for an easier word.';
  return SIMPLE.replace('{{TERMS}}', terms);
}

// The paragraph goes inside tags so the model treats it as text to rewrite, not as a message.
function simpleUser(text) {
  return 'Rewrite this passage:\n<passage>\n' + text + '\n</passage>';
}

// A reply to the passage instead of a rewrite of it ("I understand…", "Please provide the text…").
var META = /^\s*(i understand|i will|i'll|i can|i'm ready|i am ready|sure|certainly|of course|here is|here's|okay|ok[,.]|when rewriting|as requested|understood|please (provide|paste|share|send))/i;
function isMetaReply(s) {
  s = String(s || '');
  return META.test(s) || /\b(the text you'?d like me|provide the text|rewrite it for you|following your rules)\b/i.test(s);
}

// The one retry after a failed check: the checker's reasons go back to the writer, which fixes the
// specific fault far more often than a blind second attempt (29/30 -> 30/30 on unseen paragraphs).
function retryUser(text, previous, feedback) {
  return 'Rewrite this passage:\n<passage>\n' + text + '\n</passage>\n\nA checker rejected your previous rewrite:\n' +
    '<previous>\n' + previous + '\n</previous>\nReason: ' + feedback +
    '\nWrite a new rewrite of the passage that fixes this, and follow every rule.';
}

// Sonnet 5.5 thinks by default: low effort keeps it quick, and a generous max_tokens stops the
// thinking from eating the rewrite. It rejects temperature (stripped in api/_lib/claude.js).
const SIMPLE_MODEL = 'claude-sonnet-5-5';
const SIMPLE_PARAMS = { max_tokens: 4000, output_config: { effort: 'low' } };

module.exports = { simpleSystem, simpleUser, retryUser, isMetaReply, QA_SIMPLE, SIMPLE_VERSION, SIMPLE_MODEL, SIMPLE_PARAMS };
