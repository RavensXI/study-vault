export const meta = {
  name: 'science-calc-guided-fanout',
  description: 'Guided conversion of all 60 distinct science calculation lessons, propagated to 165 rows (Opus authors + independent checkers, Fable spec)',
  phases: [
    { title: 'Author', detail: 'verify bank, guided conversion, figures, propagate per SPEC_SCIENCE.md', model: 'opus' },
    { title: 'Check', detail: 'independent adversarial verification incl. propagation identity', model: 'opus' },
    { title: 'Revise', detail: 'fix confirmed defects, then re-check', model: 'opus' },
  ],
}

const WORKLIST = {"higher-calculations-L01@146c1cc6d7": {"canonical_id": "6dc6da50-6253-4e4d-9806-83c34bc567cb", "title": "Titrations and Molar Concentrations", "rows": 1}, "higher-calculations-L02@6e6bcbcbc7": {"canonical_id": "33f0478e-34e4-42ed-b1d1-06aa232a5a65", "title": "Gas Volumes and Atom Economy", "rows": 1}, "higher-calculations-L03@3a05577182": {"canonical_id": "6d1c06c8-5e4e-43e5-a65c-7b2041612fb5", "title": "Moments, Levers and Gears", "rows": 1}, "higher-calculations-L04@b4b6d1f722": {"canonical_id": "cbf5f791-862e-496e-8ecf-65c4cf27002c", "title": "Pressure in Fluids", "rows": 1}, "higher-calculations-L05@07a67444d5": {"canonical_id": "a5bc928e-98eb-4dcb-ae0f-b5003a4397d6", "title": "Nuclear Equations and Half-Life", "rows": 1}, "higher-calculations-L06@a0ecd54583": {"canonical_id": "91158ba8-389c-4771-9735-326785654ccb", "title": "Transformers and Electromagnetic Induction", "rows": 1}, "higher-calculations-L01@34b52b21dc": {"canonical_id": "b88f80db-f004-4ed4-8853-32992a306402", "title": "Titrations and Molar Concentrations", "rows": 1}, "higher-calculations-L02@a3108b4601": {"canonical_id": "fee04afb-d041-4b63-8f67-73da3b882d74", "title": "Gas Volumes and Atom Economy", "rows": 1}, "higher-calculations-L03@4def3c722e": {"canonical_id": "b4864848-f50f-4481-9af7-983e8f3d20d8", "title": "Moments, Levers and Gears", "rows": 1}, "higher-calculations-L04@57e3210892": {"canonical_id": "9941e716-ac52-4486-8f10-a81babbb8cc1", "title": "Pressure in Fluids", "rows": 1}, "higher-calculations-L05@b2761124fc": {"canonical_id": "7876f55a-694d-4932-9bb9-43372697d1d9", "title": "Nuclear Equations and Half-Life", "rows": 1}, "higher-calculations-L06@f59adbb41d": {"canonical_id": "6c88ea75-6f77-4815-aaf3-4097ee027d91", "title": "Transformers and Electromagnetic Induction", "rows": 1}, "physics-calculations-L01@32fbb0cae2": {"canonical_id": "08e03207-3ecf-4964-81dc-a8b94002b3e2", "title": "Energy: KE, GPE and Power", "rows": 7}, "physics-calculations-L02@d5abd25397": {"canonical_id": "1fcee1e4-25c6-422a-9b32-539ba52df304", "title": "Efficiency and Energy Resources", "rows": 7}, "physics-calculations-L03@215be42800": {"canonical_id": "2dc58e27-b4f5-42e5-9d45-0e632c9a2371", "title": "Circuit Calculations", "rows": 7}, "physics-calculations-L04@5f35881bbb": {"canonical_id": "adf9527f-6097-41a2-be07-ed5ddf16405a", "title": "Electrical Power and Energy Bills", "rows": 7}, "physics-calculations-L05@c30ee7c879": {"canonical_id": "5473906a-ccfa-43f0-8230-5b9171181f19", "title": "Density, SHC and Latent Heat", "rows": 7}, "physics-calculations-L06@9a3ee62708": {"canonical_id": "235062c3-62a6-47ea-8337-2d59bed86884", "title": "Forces, Work Done and Elasticity", "rows": 7}, "physics-calculations-L07@ecf99ac00d": {"canonical_id": "48cb4395-c42b-4faa-9a71-44653a691790", "title": "Speed, Acceleration and Graphs", "rows": 7}, "physics-calculations-L08@8ebcc02072": {"canonical_id": "539110f5-5600-4dde-bee7-54fb60554f18", "title": "Newton's Laws, Momentum and Waves", "rows": 7}, "chemistry-calculations-L01@dd9dbc80e5": {"canonical_id": "8b8d72ed-5bdb-44b2-82e8-a7272e91d854", "title": "Relative Formula Mass and Moles", "rows": 7}, "chemistry-calculations-L02@4ec4b1a486": {"canonical_id": "a5766e06-11a6-46fa-8f5a-f97ee39cb784", "title": "Balancing Equations and Reacting Masses", "rows": 7}, "chemistry-calculations-L03@d1de9ba347": {"canonical_id": "43820341-3858-411e-83f2-3eb799cb438c", "title": "Bond Energy Calculations", "rows": 7}, "chemistry-calculations-L04@b7b54666b8": {"canonical_id": "e6963758-b327-488c-87b4-177b336f29e9", "title": "Rates from Graphs and Concentrations", "rows": 7}, "biology-data-skills-L01@d923f94f54": {"canonical_id": "67263d26-a899-4186-80ff-9f2d3ce8644e", "title": "Magnification and Unit Conversions", "rows": 7}, "biology-data-skills-L02@551b362537": {"canonical_id": "cc2d2229-8dc3-496f-abf9-5e3f9b2d14ec", "title": "Punnett Squares and Genetic Probability", "rows": 7}, "biology-data-skills-L03@40fdb75726": {"canonical_id": "9733399d-1134-4649-8166-74c5b738c4a3", "title": "Sampling, Mean and Percentage Change", "rows": 7}, "higher-calculations-L01@b5d94e42c2": {"canonical_id": "98e99005-69e2-4131-bd6b-6018ebac6e9d", "title": "Titrations and Molar Concentrations", "rows": 1}, "higher-calculations-L02@689e4ebed1": {"canonical_id": "4ef45adc-b491-4025-9906-f541fa8a7a8f", "title": "Gas Volumes, Atom Economy and Yield", "rows": 1}, "higher-calculations-L03@efa41fc772": {"canonical_id": "3f80b91f-2691-4e55-a47d-83318e6b8f5c", "title": "Moments, Levers and Gears", "rows": 1}, "higher-calculations-L04@831aee1062": {"canonical_id": "d148ded7-a7ce-47a7-b9a0-ab4de8d5ca05", "title": "Pressure in Fluids", "rows": 1}, "higher-calculations-L05@09acbba067": {"canonical_id": "c0b4f7b9-4bc5-4dcb-af9f-b3bea7be7151", "title": "Half-Life and Nuclear Equations", "rows": 1}, "higher-calculations-L06@d1cc4db5ec": {"canonical_id": "8334cfca-5401-4f27-a3de-3c2903ebe3f2", "title": "Transformers and the National Grid", "rows": 1}, "physics-calculations-L01@087ba4e3f7": {"canonical_id": "e68bcd00-8b3f-47d3-9a5b-e327a9ddde48", "title": "Energy: KE, GPE and Power", "rows": 2}, "physics-calculations-L02@ffe1cce606": {"canonical_id": "bbd5ca5d-b290-4754-9d0a-bd5f5085c82c", "title": "Efficiency and Energy Resources", "rows": 2}, "physics-calculations-L03@330faf0468": {"canonical_id": "b2dd6adb-eb4b-4251-a9fd-3305d8493c16", "title": "Circuit Calculations", "rows": 2}, "physics-calculations-L04@6ac34b4fe4": {"canonical_id": "fc32b93d-51c8-4260-a199-7268fa33979d", "title": "Electrical Power and Energy Bills", "rows": 2}, "physics-calculations-L05@e8e561e58b": {"canonical_id": "d9384cf5-c3b4-4d2d-8f46-346f2c9a8ac6", "title": "Density, SHC and Latent Heat", "rows": 2}, "physics-calculations-L06@5d1494be41": {"canonical_id": "81a530c1-42dc-444f-bcff-64698040356b", "title": "Forces, Work Done and Elasticity", "rows": 2}, "physics-calculations-L07@003464e169": {"canonical_id": "3c4aa292-cf3a-4cda-876d-25b030880bb5", "title": "Speed, Acceleration and Graphs", "rows": 2}, "physics-calculations-L08@d964afae07": {"canonical_id": "af432bd7-94b6-4601-a30d-4356767061bb", "title": "Newton's Laws, Momentum and Waves", "rows": 2}, "chemistry-calculations-L01@7c2373a397": {"canonical_id": "858929dd-19a3-44ac-8f3e-76541c453b86", "title": "Relative Formula Mass and Moles", "rows": 2}, "chemistry-calculations-L02@5b02ac14f2": {"canonical_id": "3b138666-ea0d-44c6-aaf7-55600dfb2244", "title": "Balancing Equations and Reacting Masses", "rows": 2}, "chemistry-calculations-L03@ab6f9a45d2": {"canonical_id": "72ac6bb2-a0ff-4955-98f0-7ead3e2b7423", "title": "Bond Energy Calculations", "rows": 2}, "chemistry-calculations-L04@6f3d09988e": {"canonical_id": "1563a319-bb93-438e-9b64-e079bd7e410a", "title": "Rates from Graphs and Concentrations", "rows": 2}, "biology-data-skills-L01@dfb8522d32": {"canonical_id": "3d8807c5-5c59-40c2-b5d5-dd2ca7d7fb92", "title": "Magnification and Unit Conversions", "rows": 2}, "biology-data-skills-L02@6e66d8eeba": {"canonical_id": "b76fdf39-830d-4e57-b20a-112818a6a3b2", "title": "Punnett Squares and Genetic Probability", "rows": 2}, "biology-data-skills-L03@86a105121c": {"canonical_id": "5bcd7990-52a4-49b0-8e2e-f3d0344df114", "title": "Sampling, Mean and Percentage Change", "rows": 2}, "higher-calculations-L01@0e4807bb9f": {"canonical_id": "70fd3d54-21bd-482e-be20-14a15639623d", "title": "Mole Calculations", "rows": 1}, "higher-calculations-L02@95ac3b54f8": {"canonical_id": "25f5e5e1-21c7-451c-ab9c-81872507edf1", "title": "Concentration and Titration", "rows": 1}, "higher-calculations-L03@2a30c22d67": {"canonical_id": "8767022d-e262-4979-b978-f78b8a249da8", "title": "Yield and Atom Economy", "rows": 1}, "higher-calculations-L04@f4e0c074d0": {"canonical_id": "1b30cd36-ea7e-4210-baa6-cc9f3f30072a", "title": "Forces, Acceleration and Motion Equations", "rows": 1}, "higher-calculations-L05@f4fdd10261": {"canonical_id": "5145c094-e59a-4b76-b50f-368197215ca4", "title": "Energy, Power and Efficiency", "rows": 1}, "higher-calculations-L06@4fbd5cf5b9": {"canonical_id": "8e511d1b-d282-4835-9969-c20a995cc72e", "title": "Waves, Half-Life and Density", "rows": 1}, "higher-calculations-L01@8a0771bf50": {"canonical_id": "d42fee71-d641-4f20-90c6-8bde5e185595", "title": "Hooke's Law, Springs and Elastic Potential Energy", "rows": 1}, "higher-calculations-L02@b3c8bb1c4f": {"canonical_id": "c36f2b4d-aeaa-4c83-a6b2-9a5da3abb976", "title": "Pressure in Fluids and Upthrust", "rows": 1}, "higher-calculations-L03@b360dedf84": {"canonical_id": "a20c4a08-3698-4cb8-9f8c-b8978c3f9060", "title": "Titrations, Concentrations and the Mole", "rows": 1}, "higher-calculations-L04@3c4fcb4f45": {"canonical_id": "123bb55f-1fc8-41fd-9b44-759bc466b766", "title": "Gas Volumes, Atom Economy and Percentage Yield", "rows": 1}, "higher-calculations-L05@c023b518a1": {"canonical_id": "a28c155d-46f2-49af-9cc4-27d907de0ae2", "title": "Nuclear Equations and Half-Life Drill", "rows": 1}, "higher-calculations-L06@e6541c99e0": {"canonical_id": "7053bb43-3e0a-4822-9a37-761fc2402923", "title": "Transformers, Power Transmission and Moments Drill", "rows": 1}}
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
