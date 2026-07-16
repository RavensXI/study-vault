# -*- coding: utf-8 -*-
"""Generate one board fan-out workflow script (plain ASCII strings only:
no apostrophes or backslashes in JS string literals, learned the hard way).
Usage: python _gen_workflow.py maths-aqa"""
import json, io, os, sys

board = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
wl = json.load(io.open(os.path.join(HERE, "_worklist_%s.json" % board), encoding="utf-8"))
targets = {k: {"id": v["id"], "title": v["title"]} for k, v in wl.items()}

TPL = """export const meta = {
  name: 'BOARD-guided-full-fanout',
  description: 'Full guided-learning + diagrams conversion of all 48 BOARD lessons (Opus authors + independent checkers, Fable spec)',
  phases: [
    { title: 'Author', detail: 'verify bank, guided conversion, diagrams, per SPEC_BOARDS.md', model: 'opus' },
    { title: 'Check', detail: 'independent adversarial verification of maths, walks, figures', model: 'opus' },
    { title: 'Revise', detail: 'fix confirmed defects, then re-check', model: 'opus' },
  ],
}

const WORKLIST = WORKLIST_JSON
const KEYS = Object.keys(WORKLIST)
const SPEC = 'C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/SPEC_BOARDS.md'

const AUTHOR_SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    patched: { type: 'boolean' },
    validator_clean: { type: 'boolean' },
    problems_fixed: { type: 'integer' },
    figures_added: { type: 'integer' },
    summary: { type: 'string' },
  },
  required: ['key', 'patched', 'validator_clean', 'problems_fixed', 'figures_added', 'summary'],
  additionalProperties: false,
}
const CHECK_SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    pass: { type: 'boolean' },
    maths_errors: { type: 'integer' },
    findings: { type: 'array', items: { type: 'string' }, maxItems: 25 },
  },
  required: ['key', 'pass', 'maths_errors', 'findings'],
  additionalProperties: false,
}

function line(k) { return k + ' ("' + WORKLIST[k].title + '", board BOARD, Supabase lesson id ' + WORKLIST[k].id + ')' }
function authorPrompt(k) {
  return 'Read this spec and the two specs it references, all in full: "' + SPEC + '". You are the AUTHOR doing the complete guided-learning + diagrams conversion of one maths lesson. Your lesson: ' + line(k) + '. Fresh-solve and repair the bank first (trust nothing), then the full conversion, figures where the exam would print one, ship gate (validator PASS, PATCH live, shard + changes files). Verify every number you write. Return: key, patched, validator_clean, problems_fixed, figures_added, summary (max 80 words).'
}
function checkPrompt(k, re) {
  return 'Read the spec "' + SPEC + '" and both referenced specs, especially the checker briefs. You are the independent adversarial CHECKER for lesson ' + line(k) + '.' + (re ? ' This is a RE-CHECK after revision.' : '') + ' Fresh-solve every problem, recompute every guided box, reproduce every misconception expect, cross-check every figure label, on the LIVE row. Return: key, pass, maths_errors, findings with exact paths.'
}
function revisePrompt(k, f) {
  return 'Read the spec in full: "' + SPEC + '". You are REVISING lesson ' + line(k) + ' after an independent check found defects: ' + f + ' ... Fix every defect with verification, redo the ship gate (validator PASS, PATCH live, update files). Return the author schema.'
}

const results = await pipeline(
  KEYS,
  k => agent(authorPrompt(k), { label: 'author:' + k, phase: 'Author', model: 'opus', effort: 'high', schema: AUTHOR_SCHEMA }),
  (a, k) => {
    if (!a || !a.patched) return { author: a, check: null }
    return agent(checkPrompt(k, false), { label: 'check:' + k, phase: 'Check', model: 'opus', effort: 'high', schema: CHECK_SCHEMA })
      .then(c => ({ author: a, check: c }))
  },
  (r, k) => {
    if (!r || !r.check) return { key: k, status: r && r.author ? 'check-missing' : 'author-failed' }
    if (r.check.pass) return { key: k, status: 'pass', findings: r.check.findings }
    const f = JSON.stringify(r.check.findings).slice(0, 5000)
    return agent(revisePrompt(k, f), { label: 'revise:' + k, phase: 'Revise', model: 'opus', effort: 'high', schema: AUTHOR_SCHEMA })
      .then(() => agent(checkPrompt(k, true), { label: 'recheck:' + k, phase: 'Revise', model: 'opus', effort: 'high', schema: CHECK_SCHEMA }))
      .then(c2 => ({ key: k, status: c2 && c2.pass ? 'pass-after-revision' : 'STILL-FAILING', findings: c2 ? c2.findings : ['recheck died'] }))
  }
)

const out = results.filter(Boolean)
log('BOARD fan-out: ' + out.filter(r => r.status === 'pass').length + ' clean, '
  + out.filter(r => r.status === 'pass-after-revision').length + ' fixed-on-revision, '
  + out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision').length + ' need attention')
return {
  board: 'BOARD',
  clean: out.filter(r => r.status === 'pass').map(r => r.key),
  fixedOnRevision: out.filter(r => r.status === 'pass-after-revision').map(r => r.key),
  needAttention: out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision'),
}
"""

script = TPL.replace("WORKLIST_JSON", json.dumps(targets, ensure_ascii=False)).replace("BOARD", board)
out = os.path.join(HERE, "_workflow_%s.js" % board)
io.open(out, "w", encoding="utf-8", newline="").write(script)
print("wrote", out, len(script), "chars")
