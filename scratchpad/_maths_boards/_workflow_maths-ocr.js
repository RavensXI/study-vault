export const meta = {
  name: 'maths-ocr-guided-full-fanout',
  description: 'Full guided-learning + diagrams conversion of all 48 maths-ocr lessons (Opus authors + independent checkers, Fable spec)',
  phases: [
    { title: 'Author', detail: 'verify bank, guided conversion, diagrams, per SPEC_maths-ocrS.md', model: 'opus' },
    { title: 'Check', detail: 'independent adversarial verification of maths, walks, figures', model: 'opus' },
    { title: 'Revise', detail: 'fix confirmed defects, then re-check', model: 'opus' },
  ],
}

const WORKLIST = {"graphs-L01": {"id": "89689a46-7251-4c2a-900e-5fdc240dafd3", "title": "Plotting & Reading Linear Graphs"}, "probability-statistics-L01": {"id": "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3", "title": "Probability Basics & Tree Diagrams"}, "number-L01": {"id": "06eb8087-b07f-4bfa-8bc2-af97e3e06ebf", "title": "Four Operations & Order of Operations"}, "algebra-L01": {"id": "d8a78aa2-a642-4dcd-9cb0-1aa5990761e7", "title": "Simplifying Expressions"}, "ratio-proportion-L01": {"id": "9a6f1e85-41b4-4b82-87c6-e919e48362a9", "title": "Ratio & Proportion"}, "geometry-L01": {"id": "498fd544-0137-4fe2-be55-f4861c72723f", "title": "Angle Facts & Properties"}, "number-L02": {"id": "fe589e29-485c-4272-94df-41687f398c1b", "title": "Fractions"}, "graphs-L02": {"id": "e40e80e4-666f-4cce-a8b3-5f7bb6b5c490", "title": "Equation of a Line"}, "ratio-proportion-L02": {"id": "330ee5b7-1c7b-4990-861a-b9de40f4c2a9", "title": "Percentages & Compound Change"}, "probability-statistics-L02": {"id": "1a8441e6-115c-473e-a9b7-a2276e5b7faa", "title": "Venn Diagrams & Conditional Probability"}, "algebra-L02": {"id": "bbbab852-7730-4d87-a2db-9ba6413f97b1", "title": "Expanding Brackets"}, "geometry-L02": {"id": "7134e062-5209-4de5-894e-c315dc3ee9d0", "title": "Area & Perimeter"}, "number-L03": {"id": "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff", "title": "Decimals & Rounding"}, "algebra-L03": {"id": "44ea1f33-8979-4e3e-83b8-d2bfd93e3ee5", "title": "Factorising"}, "graphs-L03": {"id": "fc1f101a-9d1b-4eab-8bf8-8159f78caea2", "title": "Quadratic Graphs"}, "geometry-L03": {"id": "70586def-170c-4aa7-947b-2b961cfadec2", "title": "Volume & Surface Area"}, "probability-statistics-L03": {"id": "65e7a745-9820-431a-8b99-d96cd7514bf3", "title": "Representing Data"}, "ratio-proportion-L03": {"id": "0ff5cf7c-3a9d-4854-b458-6d816b7df718", "title": "Speed, Density & Pressure"}, "algebra-L04": {"id": "da15f5f9-2162-4b08-b990-ac2efa64f13a", "title": "Formulae & Substitution"}, "graphs-L04": {"id": "fb13c12c-f5c1-4832-871b-40440d729361", "title": "Real-Life Graphs"}, "ratio-proportion-L04": {"id": "f4a69507-b194-4751-ae27-c657ddd23113", "title": "Direct & Inverse Proportion"}, "probability-statistics-L04": {"id": "6e383a58-7e5b-4917-a28d-2881938a3def", "title": "Averages & Spread"}, "number-L04": {"id": "6a2afcf8-1c03-4b07-b228-3999deb3d402", "title": "Factors, Multiples & Primes"}, "geometry-L04": {"id": "9f5d0097-caa6-464c-9f1c-05ce6b836cc9", "title": "Transformations"}, "ratio-proportion-L05": {"id": "ddbb6863-36ab-4898-8090-16df440a9d85", "title": "Proportion Equations & Powers"}, "geometry-L05": {"id": "2d827ad4-80ab-4327-81f8-a2e5cec4f50a", "title": "Pythagoras & Trigonometry (SOHCAHTOA)"}, "number-L05": {"id": "4fd08300-e0fe-44c5-93cd-76b6d900c72d", "title": "Percentages"}, "algebra-L05": {"id": "320a6b1d-a96c-400f-8807-5828376373ea", "title": "Solving Linear Equations"}, "probability-statistics-L05": {"id": "b063ea7d-cb1c-40ca-a28b-ea79c429361f", "title": "Cumulative Frequency, Box Plots & Histograms"}, "graphs-L05": {"id": "acf8619c-92bc-4778-b29c-dd0cb973f59c", "title": "Cubic, Reciprocal & Exponential Graphs"}, "geometry-L06": {"id": "fe05d231-ed67-4625-aa4d-791c6b1d9887", "title": "Sine Rule, Cosine Rule & Area Formula"}, "graphs-L06": {"id": "9f0126b9-ab85-4cbc-bc94-5d1214d5c4c2", "title": "Trigonometric Graphs"}, "algebra-L06": {"id": "0a7ff82d-058f-480c-86fe-63a16ac98dc5", "title": "Factorising Quadratics (a≠1)"}, "number-L06": {"id": "24e576f2-0e8a-43bc-bacd-5397b4da617b", "title": "Powers, Roots & Standard Form"}, "ratio-proportion-L06": {"id": "4e8ba0ab-6dca-4615-98e2-2fac39408f5c", "title": "Rates of Change & Iterative Processes"}, "number-L07": {"id": "e16ccba1-6dc0-4321-835b-98ec18acce00", "title": "Indices, Surds & Bounds"}, "geometry-L07": {"id": "813488f9-f52c-4d54-8b53-c95eded2df12", "title": "Circle Theorems"}, "graphs-L07": {"id": "5ea35085-7e2c-4216-9829-f0eda94acb67", "title": "Graph Transformations"}, "algebra-L07": {"id": "90c8606a-f24d-4140-91ff-20adf463a3f0", "title": "Solving Quadratics by Factorising"}, "geometry-L08": {"id": "47a41e5d-3d22-45fd-a1c0-b29405585d87", "title": "Vectors"}, "algebra-L08": {"id": "1422954b-1171-49c2-a0c0-d5a1feb0da0d", "title": "Quadratic Formula & Completing the Square"}, "graphs-L08": {"id": "cdee2760-731b-4056-9231-cfd7327b0ed4", "title": "Gradients of Curves & Areas Under Graphs"}, "algebra-L09": {"id": "ee2766ef-5043-457b-b6b3-4e38d5ed9d0e", "title": "Simultaneous Equations (Linear)"}, "algebra-L10": {"id": "dd0172cd-6a81-41c6-ae9b-98de9328eb77", "title": "Simultaneous Equations (Quadratic)"}, "algebra-L11": {"id": "04953988-ada8-4eb2-bbd4-401fb67247ff", "title": "Inequalities"}, "algebra-L12": {"id": "971cfba0-badb-4c6b-b0f8-e9d33d450b8c", "title": "Quadratic Inequalities & Regions"}, "algebra-L13": {"id": "44ac4c68-828c-4d38-888a-37758fefde57", "title": "Sequences & nth Term"}, "algebra-L14": {"id": "da768b8a-d62b-4701-8423-7988dc8325a7", "title": "Quadratic nth Term, Functions & Iteration"}}
const KEYS = Object.keys(WORKLIST)
const SPEC = 'C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/SPEC_maths-ocrS.md'

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

function line(k) { return k + ' ("' + WORKLIST[k].title + '", board maths-ocr, Supabase lesson id ' + WORKLIST[k].id + ')' }
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
log('maths-ocr fan-out: ' + out.filter(r => r.status === 'pass').length + ' clean, '
  + out.filter(r => r.status === 'pass-after-revision').length + ' fixed-on-revision, '
  + out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision').length + ' need attention')
return {
  board: 'maths-ocr',
  clean: out.filter(r => r.status === 'pass').map(r => r.key),
  fixedOnRevision: out.filter(r => r.status === 'pass-after-revision').map(r => r.key),
  needAttention: out.filter(r => r.status !== 'pass' && r.status !== 'pass-after-revision'),
}
