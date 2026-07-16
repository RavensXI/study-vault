export const meta = {
  name: 'maths-eduqas-guided-full-fanout',
  description: 'Full guided-learning + diagrams conversion of all 48 maths-eduqas lessons (Opus authors + independent checkers, Fable spec)',
  phases: [
    { title: 'Author', detail: 'verify bank, guided conversion, diagrams, per SPEC_maths-eduqasS.md', model: 'opus' },
    { title: 'Check', detail: 'independent adversarial verification of maths, walks, figures', model: 'opus' },
    { title: 'Revise', detail: 'fix confirmed defects, then re-check', model: 'opus' },
  ],
}

const WORKLIST = {"algebra-L01": {"id": "7e5e6d1a-aa08-4fbf-8094-760926f7e56c", "title": "Simplifying Expressions"}, "probability-statistics-L01": {"id": "a28fddf4-3ee1-48dc-b138-aa17facad15d", "title": "Probability Basics & Tree Diagrams"}, "ratio-proportion-L01": {"id": "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714", "title": "Ratio & Proportion"}, "graphs-L01": {"id": "112923c0-364e-4701-91d9-280e7859d6d3", "title": "Plotting & Reading Linear Graphs"}, "geometry-L01": {"id": "89062264-f404-4e8e-8959-06c7a9fd0b7a", "title": "Angle Facts & Properties"}, "number-L01": {"id": "e58f9467-dd87-4589-9b18-b603c1966291", "title": "Four Operations & Order of Operations"}, "graphs-L02": {"id": "8cd3697d-8a79-488d-87f0-7e8f6a40ddbb", "title": "Equation of a Line"}, "probability-statistics-L02": {"id": "7f417926-0bef-4875-a7ad-7eb71bd15506", "title": "Venn Diagrams & Conditional Probability"}, "number-L02": {"id": "09c2b39e-ac37-4058-8de3-22b163764aa7", "title": "Fractions"}, "algebra-L02": {"id": "a1bdc834-74b8-41cf-8671-c1e3e5270619", "title": "Expanding Brackets"}, "ratio-proportion-L02": {"id": "bba25423-da94-4b3e-8415-2e9161014760", "title": "Percentages & Compound Change"}, "geometry-L02": {"id": "5c10e089-e2cc-4a61-b6b3-951a8994a1a0", "title": "Area & Perimeter"}, "number-L03": {"id": "9e521b4c-a8d3-47d8-ac6b-1ce35dabf977", "title": "Decimals & Rounding"}, "algebra-L03": {"id": "7ccfb7aa-adfd-4f9d-9679-35d805ddd77a", "title": "Factorising"}, "ratio-proportion-L03": {"id": "2351f9ce-12fd-4b0e-95ac-c89fb8adc612", "title": "Speed, Density & Pressure"}, "geometry-L03": {"id": "1e9d6465-1ec1-40a3-8138-958197366837", "title": "Volume & Surface Area"}, "graphs-L03": {"id": "39bdcd12-eb3d-45b1-b0c5-d8e2257610df", "title": "Quadratic Graphs"}, "probability-statistics-L03": {"id": "d6cc3827-bbe2-42ae-b116-7c8398b1bf70", "title": "Representing Data"}, "number-L04": {"id": "83d542e3-c94b-4365-b8a9-070845b779ec", "title": "Factors, Multiples & Primes"}, "algebra-L04": {"id": "4feee23f-c960-4264-a828-cde0f9080d45", "title": "Formulae & Substitution"}, "graphs-L04": {"id": "0334612d-1b10-4495-8d37-21ef41d3a925", "title": "Real-Life Graphs"}, "ratio-proportion-L04": {"id": "a48ad66b-78c0-46f9-9db0-828173e35d1f", "title": "Direct & Inverse Proportion"}, "geometry-L04": {"id": "499de8ed-424f-4027-a013-e64b3b083820", "title": "Transformations"}, "probability-statistics-L04": {"id": "54d6fba0-9730-427b-917f-ca3487dc16e9", "title": "Averages & Spread"}, "probability-statistics-L05": {"id": "2e75898f-577a-42bd-b94e-f1435e89ace3", "title": "Cumulative Frequency, Box Plots & Histograms"}, "ratio-proportion-L05": {"id": "93469b0d-2704-499c-a20b-587a84c2e214", "title": "Proportion Equations & Powers"}, "number-L05": {"id": "769be867-fe49-4cf1-b45f-1308b21e81dd", "title": "Percentages"}, "geometry-L05": {"id": "1ee92530-13a8-48bd-901d-f8c28e6bf899", "title": "Pythagoras & Trigonometry (SOHCAHTOA)"}, "graphs-L05": {"id": "295660a5-6ee6-40a4-9c32-c6aa0de7a590", "title": "Cubic, Reciprocal & Exponential Graphs"}, "algebra-L05": {"id": "014f2f50-be82-4870-a8e7-d15963b39e8f", "title": "Solving Linear Equations"}, "geometry-L06": {"id": "a36e47ae-bd22-4127-af9d-5b37e34c0b64", "title": "Sine Rule, Cosine Rule & Area Formula"}, "ratio-proportion-L06": {"id": "ca643606-adf3-40c8-a4dd-8dfb8c25a21f", "title": "Rates of Change & Iterative Processes"}, "graphs-L06": {"id": "683b816a-4d56-4d3d-911b-58cb3bca5efd", "title": "Trigonometric Graphs"}, "algebra-L06": {"id": "32acb3ec-b5ac-410b-984c-d9008683af8e", "title": "Factorising Quadratics (a!=1)"}, "number-L06": {"id": "d15fddc3-0766-4882-bfc8-15a0b7208d89", "title": "Powers, Roots & Standard Form"}, "number-L07": {"id": "d8937c21-f4ad-4d20-971a-03186a285b7f", "title": "Indices, Surds & Bounds"}, "geometry-L07": {"id": "f3574e2a-651d-42a7-af75-8ee52eeb48d8", "title": "Circle Theorems"}, "graphs-L07": {"id": "660796ad-070d-4a2d-af11-900e5a5af1c1", "title": "Graph Transformations"}, "algebra-L07": {"id": "5ead70d6-f265-4790-86b5-573b9b16606a", "title": "Solving Quadratics by Factorising"}, "graphs-L08": {"id": "1d30ba6e-3b9a-41a9-b192-23cab4fd0d5f", "title": "Gradients of Curves & Areas Under Graphs"}, "geometry-L08": {"id": "7f378aaa-68dc-4420-b952-f56d8349b1ed", "title": "Vectors"}, "algebra-L08": {"id": "496a8347-7f03-47a6-9543-49cb82efe3af", "title": "Quadratic Formula & Completing the Square"}, "algebra-L09": {"id": "038c2343-8acf-41e4-b02a-914268bc6572", "title": "Simultaneous Equations (Linear)"}, "algebra-L10": {"id": "27ec4539-cb68-4e60-ad0d-fa0828706d80", "title": "Simultaneous Equations (Quadratic)"}, "algebra-L11": {"id": "8e823cb5-7ee7-49af-b403-2c96a246c229", "title": "Inequalities"}, "algebra-L12": {"id": "66a1ec53-d20f-4b82-b436-1b31fc88e998", "title": "Quadratic Inequalities & Regions"}, "algebra-L13": {"id": "d84411dc-60b7-4f96-8f42-35486f5d7129", "title": "Sequences & nth Term"}, "algebra-L14": {"id": "15c509ec-bdaf-466b-b9e4-1f1803fc4b3d", "title": "Quadratic nth Term, Functions & Iteration"}}
const KEYS = Object.keys(WORKLIST)
const SPEC = 'C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/SPEC_maths-eduqasS.md'

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

function line(k) { return k + ' ("' + WORKLIST[k].title + '", board maths-eduqas, Supabase lesson id ' + WORKLIST[k].id + ')' }
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
log('maths-eduqas fan-out: ' + out.filter(r => r.status === 'pass').length + ' clean, '
  + out.filter(r => r.status === 'pass-after-revision').length + ' fixed-on-revision, '
  + out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision').length + ' need attention')
return {
  board: 'maths-eduqas',
  clean: out.filter(r => r.status === 'pass').map(r => r.key),
  fixedOnRevision: out.filter(r => r.status === 'pass-after-revision').map(r => r.key),
  needAttention: out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision'),
}
