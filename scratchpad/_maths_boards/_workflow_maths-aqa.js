export const meta = {
  name: 'maths-aqa-guided-full-fanout',
  description: 'Full guided-learning + diagrams conversion of all 48 maths-aqa lessons (Opus authors + independent checkers, Fable spec)',
  phases: [
    { title: 'Author', detail: 'verify bank, guided conversion, diagrams, per SPEC_maths-aqaS.md', model: 'opus' },
    { title: 'Check', detail: 'independent adversarial verification of maths, walks, figures', model: 'opus' },
    { title: 'Revise', detail: 'fix confirmed defects, then re-check', model: 'opus' },
  ],
}

const WORKLIST = {"ratio-proportion-L01": {"id": "5cfec765-3128-469b-9d6a-626f042d6161", "title": "Ratio & Proportion"}, "graphs-L01": {"id": "cc326bc8-362b-4a54-875c-f7a7ffc1b77d", "title": "Plotting & Reading Linear Graphs"}, "probability-statistics-L01": {"id": "aa2fb8d9-f47f-4412-8231-28085ce43740", "title": "Probability Basics & Tree Diagrams"}, "number-L01": {"id": "e023770a-3bf9-43e4-9718-fc2da08eda49", "title": "Four Operations & Order of Operations"}, "geometry-L01": {"id": "fe1de83d-e81d-4f39-bc83-036f91da46f0", "title": "Angle Facts & Properties"}, "algebra-L01": {"id": "f4f1368e-d7c2-41f1-8459-de2c0d500c3b", "title": "Simplifying Expressions"}, "number-L02": {"id": "cbc91397-a67c-472a-b0da-308aa9da1653", "title": "Fractions"}, "algebra-L02": {"id": "b749e688-9faa-49ba-ae68-08f8abdc7496", "title": "Expanding Brackets"}, "graphs-L02": {"id": "96f5aef3-e4c8-4faf-ba82-1d587dc4e10e", "title": "Equation of a Line"}, "ratio-proportion-L02": {"id": "5b37c8ce-e970-4d38-9c96-c65baa661fa4", "title": "Percentages & Compound Change"}, "geometry-L02": {"id": "09fd71ca-ab66-4ea3-bf5b-0005f5ae5b6e", "title": "Area & Perimeter"}, "probability-statistics-L02": {"id": "ec35471d-bdb2-419a-9f86-1b8b85d6d5a7", "title": "Venn Diagrams & Conditional Probability"}, "ratio-proportion-L03": {"id": "689bc7ff-0d4c-4f20-a83c-9476935f2ac9", "title": "Speed, Density & Pressure"}, "probability-statistics-L03": {"id": "74d5f6d6-9036-4da3-adf3-d7e2c86fc6b4", "title": "Representing Data"}, "number-L03": {"id": "c8596747-22a3-47f0-8fe7-f0bc6c6d1101", "title": "Decimals & Rounding"}, "graphs-L03": {"id": "c8bc060f-c094-4b04-abec-5577523f8667", "title": "Quadratic Graphs"}, "geometry-L03": {"id": "28c3fccf-544d-4e44-a03f-635e88222391", "title": "Volume & Surface Area"}, "algebra-L03": {"id": "55a5af04-f88a-4be7-b4c0-7f89c607e266", "title": "Factorising"}, "algebra-L04": {"id": "431cf470-df7f-4654-8c83-df7aeb1e0322", "title": "Formulae & Substitution"}, "ratio-proportion-L04": {"id": "6f3f98f9-e772-40d9-8e54-b76a2ed3e8c7", "title": "Direct & Inverse Proportion"}, "number-L04": {"id": "99a85546-e8a4-455d-b1eb-1f9e25808cea", "title": "Factors, Multiples & Primes"}, "graphs-L04": {"id": "b73c61cf-00b8-44c8-9e08-9f7f6f84c60a", "title": "Real-Life Graphs"}, "geometry-L04": {"id": "7f991a30-4b90-4e0e-8cf8-f37a3210006e", "title": "Transformations"}, "probability-statistics-L04": {"id": "9bf07c35-9977-4389-9fbb-7c9b3a67caea", "title": "Averages & Spread"}, "ratio-proportion-L05": {"id": "47e48001-4c4f-45ab-a400-ba16648b2569", "title": "Proportion Equations & Powers"}, "number-L05": {"id": "a65d19a4-17d8-4370-ac24-ef8ae364f72d", "title": "Percentages"}, "algebra-L05": {"id": "d2ed09e5-eea7-4e13-a9b6-2437ace7f664", "title": "Solving Linear Equations"}, "graphs-L05": {"id": "74e144eb-d320-44e4-afed-c9a263b3af36", "title": "Cubic, Reciprocal & Exponential Graphs"}, "geometry-L05": {"id": "93f6b9f1-7ae6-4f12-945b-a5b0c096dc09", "title": "Pythagoras & Trigonometry (SOHCAHTOA)"}, "probability-statistics-L05": {"id": "df1cb4b9-09d1-4692-8674-2427dfe4c393", "title": "Cumulative Frequency, Box Plots & Histograms"}, "geometry-L06": {"id": "6e4a84ec-b6c4-489b-9d86-0cc1a7fb65b0", "title": "Sine Rule, Cosine Rule & Area Formula"}, "ratio-proportion-L06": {"id": "e15d6925-608b-4c05-aa82-c4782d1657b3", "title": "Rates of Change & Iterative Processes"}, "graphs-L06": {"id": "de6bd262-7fb6-4392-a5a3-e0cda56ea7ba", "title": "Trigonometric Graphs"}, "algebra-L06": {"id": "7104a3b3-00b8-40c8-a875-0f55043cc6b8", "title": "Factorising Quadratics (a≠1)"}, "number-L06": {"id": "a4c149cd-abd5-4180-9ea3-449d4ac37f88", "title": "Powers, Roots & Standard Form"}, "graphs-L07": {"id": "063c867c-7ba6-4879-9747-c3546382aaf2", "title": "Graph Transformations"}, "geometry-L07": {"id": "6e789a76-e66f-4ed3-9031-599c6406ca45", "title": "Circle Theorems"}, "algebra-L07": {"id": "80de6f33-3b1d-40af-9068-8e6fc132c36d", "title": "Solving Quadratics by Factorising"}, "number-L07": {"id": "8696e75e-f9fd-40ef-b3a4-df27f5811c73", "title": "Indices, Surds & Bounds"}, "graphs-L08": {"id": "2ce07c9f-af5f-4162-ae95-544d91a71830", "title": "Gradients of Curves & Areas Under Graphs"}, "algebra-L08": {"id": "6589946a-1739-4d22-add3-1a9081309921", "title": "Quadratic Formula & Completing the Square"}, "geometry-L08": {"id": "3e214279-84c2-41dc-a639-94bda78e2da8", "title": "Vectors"}, "algebra-L09": {"id": "5ff3e1eb-2284-4096-af06-4bcb6754b0e1", "title": "Simultaneous Equations (Linear)"}, "algebra-L10": {"id": "0c881c07-49bb-49cd-8c89-41b971335061", "title": "Simultaneous Equations (Quadratic)"}, "algebra-L11": {"id": "4d1cbe2a-483a-400a-9fee-5166ebde6a1b", "title": "Inequalities"}, "algebra-L12": {"id": "4a7608b6-4426-4d97-97b4-551e408f6951", "title": "Quadratic Inequalities & Regions"}, "algebra-L13": {"id": "e0a5f715-f25c-4afd-b0c1-c71ea7f743e3", "title": "Sequences & nth Term"}, "algebra-L14": {"id": "f4814142-6434-44c9-9458-6b95f1e27ec6", "title": "Quadratic nth Term, Functions & Iteration"}}
const KEYS = Object.keys(WORKLIST)
const SPEC = 'C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/SPEC_maths-aqaS.md'

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

function line(k) { return k + ' ("' + WORKLIST[k].title + '", board maths-aqa, Supabase lesson id ' + WORKLIST[k].id + ')' }
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
log('maths-aqa fan-out: ' + out.filter(r => r.status === 'pass').length + ' clean, '
  + out.filter(r => r.status === 'pass-after-revision').length + ' fixed-on-revision, '
  + out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision').length + ' need attention')
return {
  board: 'maths-aqa',
  clean: out.filter(r => r.status === 'pass').map(r => r.key),
  fixedOnRevision: out.filter(r => r.status === 'pass-after-revision').map(r => r.key),
  needAttention: out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision'),
}
