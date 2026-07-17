# -*- coding: utf-8 -*-
"""Generate the science-calculations fan-out workflow (ASCII-safe JS strings)."""
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
wl = json.load(io.open(os.path.join(HERE, "_worklist_versions.json"), encoding="utf-8"))
targets = {k: {"canonical_id": v["canonical_id"], "title": v["title"],
               "rows": len(v["all_row_ids"])} for k, v in wl.items()}

TPL = """export const meta = {
  name: 'science-calc-guided-fanout',
  description: 'Guided conversion of all 60 distinct science calculation lessons, propagated to 165 rows (Opus authors + independent checkers, Fable spec)',
  phases: [
    { title: 'Author', detail: 'verify bank, guided conversion, figures, propagate per SPEC_SCIENCE.md', model: 'opus' },
    { title: 'Check', detail: 'independent adversarial verification incl. propagation identity', model: 'opus' },
    { title: 'Revise', detail: 'fix confirmed defects, then re-check', model: 'opus' },
  ],
}

const WORKLIST = WORKLIST_JSON
const KEYS = Object.keys(WORKLIST)
const SPEC = 'C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/SPEC_SCIENCE.md'

const AUTHOR_SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    patched: { type: 'boolean' },
    validator_clean: { type: 'boolean' },
    rows_patched: { type: 'integer' },
    problems_fixed: { type: 'integer' },
    figures_added: { type: 'integer' },
    summary: { type: 'string' },
  },
  required: ['key', 'patched', 'validator_clean', 'rows_patched', 'problems_fixed', 'figures_added', 'summary'],
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

function line(k) {
  const v = WORKLIST[k]
  return k + ' ("' + v.title + '", canonical row ' + v.canonical_id + ', propagates to ' + v.rows + ' rows)'
}
function authorPrompt(k) {
  return 'Read this spec and everything it references, in full: "' + SPEC + '". You are the AUTHOR converting one science calculation lesson to the guided format and propagating it. Your work-list entry: ' + line(k) + ' (full details incl. all_row_ids are in the work-list file the spec names). Fresh-solve and repair the bank first, then the full conversion, then the ship gate including patching EVERY id in all_row_ids identically. Verify every number. Return: key, patched, validator_clean, rows_patched, problems_fixed, figures_added, summary (max 80 words).'
}
function checkPrompt(k, re) {
  return 'Read the spec "' + SPEC + '" and its referenced specs, especially the checker briefs. You are the independent adversarial CHECKER for work-list entry ' + line(k) + '.' + (re ? ' This is a RE-CHECK after revision.' : '') + ' Fresh-solve every problem, recompute every box, reproduce every expect against the accept window, verify board-neutral phrasing, and verify propagation identity across at least two of all_row_ids. Return: key, pass, maths_errors, findings with exact paths.'
}
function revisePrompt(k, f) {
  return 'Read the spec in full: "' + SPEC + '". You are REVISING work-list entry ' + line(k) + ' after an independent check found defects: ' + f + ' ... Fix every defect with verification, redo the ship gate including re-propagation to all_row_ids. Return the author schema.'
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
log('science fan-out: ' + out.filter(r => r.status === 'pass').length + ' clean, '
  + out.filter(r => r.status === 'pass-after-revision').length + ' fixed-on-revision, '
  + out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision').length + ' need attention')
return {
  clean: out.filter(r => r.status === 'pass').map(r => r.key),
  fixedOnRevision: out.filter(r => r.status === 'pass-after-revision').map(r => r.key),
  needAttention: out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision'),
}
"""

script = TPL.replace("WORKLIST_JSON", json.dumps(targets, ensure_ascii=False))
out = os.path.join(HERE, "_workflow_science.js")
io.open(out, "w", encoding="utf-8", newline="").write(script)
print("wrote", out, len(script), "chars")
