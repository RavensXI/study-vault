# History (AQA 8145) — Master Plan Summary

**Subject slug:** `history-aqa` · **School:** free tier (school_id NULL) · **Hero colour:** `#7f1d1d`

**Total: 214 lessons across 16 units** (within the 195-240 calibration band).

Single-planner output is not used — this came from a 1+16 fan-out (one subject-shell call + 16 parallel per-option deep plans). Files: `scripts/_plan_history-aqa-shell.json`, `scripts/_plan_history-aqa-{slug}.json` × 16, merged into `scripts/_plan_history-aqa.json`.

---

## The 16 options at a glance

A student picks one from each section. Sort order within each section is set by best-guess uptake (research-led where stats existed, otherwise spec order).

### Paper 1 Section A — Period Studies (pick 1 of 4) — 55 lessons

| # | Option | Slug | Lessons | Accent | HE site (2026) |
|---|--------|------|--------:|--------|----------------|
| 1 | Germany, 1890-1945 | `germany-democracy-dictatorship` | 14 | `#9a3412` | — |
| 2 | Russia, 1894-1945 | `russia-tsardom-communism` | 14 | `#b91c1c` | — |
| 3 | America, 1920-1973 | `america-opportunity-inequality` | 14 | `#c2410c` | — |
| 4 | America, 1840-1895 | `america-expansion-consolidation` | 13 | `#a16207` | — |

### Paper 1 Section B — Wider World Depth (pick 1 of 5) — 66 lessons

| # | Option | Slug | Lessons | Accent | HE site (2026) |
|---|--------|------|--------:|--------|----------------|
| 5 | Conflict and Tension: 1918-1939 | `conflict-tension-inter-war` | 14 | `#475569` | — |
| 6 | Conflict and Tension: East and West, 1945-1972 | `conflict-tension-east-west` | 14 | `#374151` | — |
| 7 | Conflict and Tension: 1894-1918 | `conflict-tension-first-world-war` | 13 | `#3f6212` | — |
| 8 | Conflict and Tension in Asia, 1950-1975 | `conflict-tension-asia` | 13 | `#0f766e` | — |
| 9 | Conflict and Tension: Gulf and Afghanistan, 1990-2009 | `conflict-tension-gulf-afghanistan` | 12 | `#525252` | — |

### Paper 2 Section A — Thematic Studies (pick 1 of 3) — 42 lessons

| # | Option | Slug | Lessons | Accent | HE site (2026) |
|---|--------|------|--------:|--------|----------------|
| 10 | Britain: Health and the People | `britain-health-people` | 14 | `#4d7c0f` | — |
| 11 | Britain: Power and the People | `britain-power-people` | 14 | `#a16207` | — |
| 12 | Britain: Migration, Empires and the People | `britain-migration-empires` | 14 | `#9d174d` | — |

### Paper 2 Section B — British Depth Studies with Historic Environment (pick 1 of 4) — 47 lessons

| # | Option | Slug | Lessons | Accent | HE site (2026) |
|---|--------|------|--------:|--------|----------------|
| 13 | Elizabethan England, c1568-1603 | `elizabethan-england` | 12 | `#581c87` | — |
| 14 | Norman England, c1066-c1100 | `norman-england` | 12 | `#1e3a8a` | — |
| 15 | Medieval England: the Reign of Edward I, 1272-1307 | `medieval-england-edward-i` | 11 | `#7f1d1d` | — |
| 16 | Restoration England, 1660-1685 | `restoration-england` | 12 | `#14532d` | — |

---

## Confirmed 2026 historic environment sites

All four sourced from `aqa.org.uk/news/gcse-history-historic-environment-sites-2026-2028`:

- **Elizabethan England, c1568-1603** → ?
- **Norman England, c1066-c1100** → ?
- **Medieval England: the Reign of Edward I, 1272-1307** → ?
- **Restoration England, 1660-1685** → ?

Each British depth unit has 2-3 lessons explicitly built around its site, with the 16-mark Historic Environment Essay anchored on the final or second-to-final lesson.

---

## Question types registered

Every entry below will need a route in `getGuideUrl()` before content generation. All names are generic — no AQA spec/paper/component codes.

- 4 marks — Compare Interpretations
- 4 marks — Why Interpretations Differ
- 8 marks — Evaluate an Interpretation
- 4 marks — Describe Two Features
- 8 marks — Explain Effects
- 12 marks — Period Essay
- 4 marks — Source Analysis
- 12 marks — Source Evaluation
- 8 marks — Narrative Account
- 16 marks — Source-Based Essay
- 8 marks — Source Evaluation
- 8 marks — Explain Significance
- 4 marks — Two Ways Similar or Different
- 16 marks — Factors Essay
- 8 marks — Explain a Development
- 16 marks — Period Argument

Period studies lean on the 4-mark interpretation pair, 8-mark Explain Effects, 8-mark Evaluate an Interpretation, and the 12-mark Bullet-Format Essay. Wider world depth lessons cycle 4-mark Source Analysis, 12-mark Source Utility, 8-mark Narrative Account, and the 16-mark Source-Based Essay. Thematic uses 4-mark Two Ways Similar/Different, 8-mark Explain Significance, 8-mark Explain a Development, 16-mark Factors Essay. British depth uses 4-mark Describe Two Features, 8-mark Explain Effects, 8-mark Explain Significance, and the 16-mark Historic Environment Essay (the only place that one appears).

---

## Subject-wide examiner signals (from the shell)

- Top-band source-utility responses always integrate all three of content, provenance and the student's own contextual knowledge — not two of the three.
- The 16-mark historic environment essay rewards explicit links between the specified site and wider events of the period; describing the site without linking back loses marks.
- On 12-mark bullet-format essays in Period Studies, the highest-band answers reach a substantiated overall judgement rather than just covering both bullet points.
- SPaG marks (4) on each paper reward consistent accuracy and a wide range of specialist historical terms — students who avoid historical vocabulary cap themselves at the threshold band.
- AO weighting tilts towards AO1/AO2 (35% each) over AO3/AO4 (15% each); knowledge and analysis matter more than source/interpretation work over the full course.

## Subject-wide misconceptions (top of the brief)

- **Source utility** — Students judge a source's usefulness purely by who wrote it ('biased therefore not useful'), instead of weighing content, provenance and contextual knowledge together.
- **Narrative accounts** — Students write 'first X happened, then Y, then Z' chronologies with no causal links between events, and so cannot reach the top mark band.
- **Interpretations** — Students confuse 'why interpretations differ' (focus on authors, evidence, purpose, time of writing) with 'how they differ' (focus on what each one says) and answer the wrong question.
- **Significance** — Students treat 'significance' as a synonym for 'importance at the time' and ignore importance over time, which is needed for full marks on the 8-mark thematic question.
- **Eyewitness narrative voice** — Students answer extended-response questions in the first person or as a diary entry, which prevents them meeting the AO2 analytical-link descriptors.
- **Factor essays** — Students list factors one after another (war, religion, government...) without weighing the stated factor against the others, missing the judgement required by AO2.

---

## Spec changes for 2026

- Specified historic environment sites are updated for the 2026-2028 cycle in each of the four British depth study options. Site names are released by AQA three years in advance and downstream per-option planners must use the 2026 site for that option.
- No subject-content changes for 2026 — the spec remains the version dated 24 September 2019 (version 1.3); the assessment structure of Paper 1 (84 marks, two hours) and Paper 2 (84 marks, two hours) is unchanged.

---

## Per-option highlights

Pulled from each per-option planner. Detail lives in `scripts/_plan_history-aqa-{slug}.json`.

### 1. Germany, 1890-1945 (14 lessons)
- *Misconception:* **Spartacist vs Kapp Putsch** — Students confuse the Spartacist uprising (Jan 1919, far-left, Liebknecht and Luxemburg) with the Kapp Putsch (Mar 1920, far-right, Wolfgang Kapp). Examiner reports flag this regularly because the periods of unrest blur t
- *Misconception:* **Cause direction in 1929-33** — Students write that 'Hitler caused the Depression' or that the Nazis were always popular. The Depression caused Hitler's rise — the Nazis polled only 2.6% in 1928, then 37% in July 1932 only after mass unemployment.
- *Historiography:* Sonderweg thesis — Germany followed a 'special path' away from Western liberal democracy because of Prussian militarism, weak liberalism and the survival of pre-modern elites; this culminated in Nazism. (Hans-Ulrich Wehler and the Bielefeld school)

### 2. Russia, 1894-1945 (14 lessons)
- *Misconception:* **1917 — confusing the two revolutions** — Students treat 'the Russian Revolution' as a single event in October 1917, ignoring the spontaneous February Revolution that overthrew the Tsar eight months earlier. They then credit the Bolsheviks with overthrowing Nich
- *Misconception:* **The Provisional Government** — Students assume the Provisional Government was elected and democratic. In fact it was self-appointed from the old Duma's Progressive Bloc, lacked any popular mandate, and kept postponing the Constituent Assembly election
- *Historiography:* Treats the October Revolution as a coup imposed by a small fanatical party rather than a mass revolution. Sees 1917-1991 as a single tragic experiment rooted in Lenin's authoritarianism.

### 3. America, 1920-1973 (14 lessons)
- *Misconception:* **What ended the Depression** — Students often write that the New Deal ended the Depression. Unemployment did fall sharply but only the war economy from 1941 returned the USA to full employment; the New Deal cushioned suffering and rebuilt confidence r
- *Misconception:* **Who benefited from the Boom** — Students assume the 1920s Boom raised every American's living standard. In fact, farmers, sharecroppers, African-Americans in the South, Native Americans, recent immigrants and many industrial workers were excluded — ine

### 4. America, 1840-1895 (13 lessons)
- *Historiography:* Frederick Jackson Turner's 1893 Frontier Thesis cast the West as the engine of American democracy — a view dominant for most of the 20th century.

### 5. Conflict and Tension: 1918-1939 (14 lessons)
- *Historiography:* U

### 6. Conflict and Tension: East and West, 1945-1972 (14 lessons)

### 7. Conflict and Tension: 1894-1918 (13 lessons)
- *Historiography:* Origins of the war

### 8. Conflict and Tension in Asia, 1950-1975 (13 lessons)

### 9. Conflict and Tension: Gulf and Afghanistan, 1990-2009 (12 lessons)
- *Misconception:* **Saddam-al-Qaeda link** — Students assume the 2003 Iraq invasion was a direct response to 9/11 and that Saddam was operationally linked to al-Qaeda.
- *Misconception:* **End of the Gulf War** — Students think the 1991 Gulf War ended Saddam's regime.

### 10. Britain: Health and the People (14 lessons)
- *Misconception:* **Medieval medicine was 'backward' with no progress** — Students assume nothing useful happened in medicine between c1000 and c1500 because supernatural causes and bleeding patients look ridiculous to modern eyes.
- *Misconception:* **Vesalius and Harvey 'changed medicine'** — Students write that Vesalius's Fabrica (1543) or Harvey's De Motu Cordis (1628) immediately transformed medical practice in Britain.

### 11. Britain: Power and the People (14 lessons)
- *Misconception:* **?** — Magna Carta 'gave rights to the British people' or 'started democracy'.
- *Misconception:* **?** — The Chartists 'won' because they got their demands.

### 12. Britain: Migration, Empires and the People (14 lessons)

### 13. Elizabethan England, c1568-1603 (12 lessons)

### 14. Norman England, c1066-c1100 (12 lessons)

### 15. Medieval England: the Reign of Edward I, 1272-1307 (11 lessons)
- *Historiography:* Edward as efficient administrator and law-giver

### 16. Restoration England, 1660-1685 (12 lessons)
- *Misconception:* **What the Restoration restored** — Students assume 1660 was a return to absolute monarchy and that the Civil War was 'forgotten'. In fact Parliament emerged stronger, taxation became a negotiated relationship, and unresolved tensions over religion and suc
- *Misconception:* **Plague vs Fire chronology** — Students confuse 1665 (Plague) and 1666 (Fire) and assume one caused or cured the other. The plague was waning before the Fire began on 2 September 1666; the Fire did not 'burn out' the plague.
- *Historiography:* Tim Harris's revisionist work (Restoration, 2005; Revolution, 2006) reframes Charles II as a politically skilful king navigating real party formation rather than a 'merry monarch'.

---

## Gaps to review (41 entries)

Most gap entries are deliberate (out-of-scope notes, paywalled examiner reports, "we don't name historians at GCSE"). Skim for genuine to-decide items:


**conflict-tension-east-west:**
- This option is a wider world depth study (Paper 1 Section B), not a British depth study, so no specified historic environment site applies. Field set to null per schema.
- Spec does not require named historians at GCSE. Lessons reference disagreement about Cold War origins generically (orthodox vs revisionist framing) without naming Gaddis or Westad in student-facing content, per the brief's guidance to use historiography only if examiner reports flag it.
- Spec ends at 1972 with SALT 1; the breakdown of Détente in the late 1970s and the second Cold War of the 1980s sit outside this option. Lesson 14 flags the misconception that Détente equals the end of the Cold War without teaching post-1972 events.

**conflict-tension-first-world-war:**
- Spec does not require historiography but the donkeys cliche dominates student writing on this option. Resolved by surfacing revisionist work (Sheffield, Todman) inside Lessons 7 and 9 as a misconception inoculation rather than examinable content.
- Background only. Surfaced as a one-sentence note in Lessons 1-5 to give students a sense of the debate without making it examinable.
- Not in this option's spec — sits in Britain Health/People and other thematic studies. Mentioning briefly only where it directly bears on the blockade in Lesson 13.

**conflict-tension-asia:**
- AQA does not publish official examiner principal-moderator commentary in the form of a freely downloadable single 'examiner report' for Option BD - the primary public examiner artefact is AQA-81451BD-EX 'Answers and Commentaries' (used as t
- Historic environment site is not applicable - this is a wider-world depth study (Paper 1), not a British depth study (Paper 2). Field intentionally null per schema.
- BBC Bitesize and BBC History pages were not accessible to the search agent's user agent and could not be cross-referenced; substitute factual sources used were History Today and history.com plus AQA's own published spec, sources booklet (AQ
- Historiographical debate (orthodox Lewy 'tragic-but-necessary' vs revisionist Karnow 'quagmire'; domino-theory failure vs successful elsewhere-containment) is referenced lightly in the teaching brief but is not foregrounded in lessons becau

**britain-health-people:**
- Sydenham is in the spec under 'methods of treating disease' though not separately listed by name; included for completeness because examiner reports mention him as a higher-band reference.
- Not named in the spec but consistently appears in mark schemes as a valid alternative response on Crimean nursing; included to give students breadth on the war factor.
- Spec line 'development of the pharmaceutical industry' is broad — covered through penicillin mass production and the rise of antibiotics. If a future depth pass is wanted, Big Pharma post-1980s and NICE could become a half-lesson sidebar.
- Spec lists 'alternative treatments' but examiner emphasis is light; a single paragraph in L12 is sufficient. Extended treatment could go into L14 if desired.
- All major Acts (Old Age Pensions, School Meals, School Medicals, NIA 1911) are covered. People's Budget and Lords crisis are mentioned but not deeply — they belong more to Power and the People.
- Light touch — NHS funding, ageing population, antibiotic resistance, mental health, COVID context. Deliberately not a full lesson because exam questions on this are rare and the 16-mark essay is more important.
- Health and the People is a thematic study, not a British depth study. There is no historic environment requirement, so historic_environment_site_2026 is null.

**britain-power-people:**
- AQA's specified historic environment site does not apply to Paper 2 Section A thematic options — that is a Section B requirement only — so historic_environment_site_2026 is intentionally null for this unit.
- The spec leaves the precise date range of 'progress towards equality in the second half of the 20th century' (Part 4 women's rights bullet) open — the plan covers the major Equal Pay Act 1970, Sex Discrimination Act 1975 and Equality Act 20
- Lesson 14 is positioned as a synthesis-and-technique lesson rather than introducing new spec content. If a 15th lesson is ever added, the natural addition would be a stand-alone 'Black Lives Matter UK and protest in the 2010s-2020s' lesson 
- The spec mentions 'campaigning groups and their methods and impact' (Part 3) without specifying which to teach. The plan covers anti-slavery, anti-Corn Law, factory reform and social reform in Lesson 9; teachers wanting to add Chartist link
- The 2026 examiner-report search did not surface a dedicated 'Power and the people' misconception report; misconceptions used in this plan are drawn from the AQA mark schemes/sample mark schemes, AQA principal-examiner subject-wide reports, 

**britain-migration-empires:**
- {"gap": "Medieval Jewish communities and the 1290 Edict of Expulsion are implied by the spec's c790-present framing and 'migration to and from Britain' theme but are not named in any Part 1-4 bullet. Lesson 5 ('Medieval Migrants: Hanseatic 
- {"gap": "The spec lists imperial 'propaganda' but examiner reports rarely cite specific case studies. Suggested teaching exemplars (the Rhodes Colossus 1892 cartoon, Empire Day 1902, music-hall jingoism) are conventional but not named in sp
- {"gap": "Sensitivity content: the slave trade (Lesson 6), the Indian Rebellion's reprisals (Lesson 9), the Boer War concentration camps (Lesson 10), the Mau Mau emergency (Lesson 12), and the Windrush scandal (Lesson 13) all require careful
- {"gap": "AQA does not require a named historic environment site for thematic studies (only for Section B British depth studies). historic_environment_site_2026 is therefore null."}

**elizabethan-england:**
- AQA's published answers and commentaries (8145/2BC) are referenced from the AQA filestore but the specific examiner-quote phrasings could not be transcribed verbatim; the planning brief paraphrases their substance. Content agents should pul
- Lesson 13 covers The Globe as the 2026 historic environment site. Confirmed via aqa.org.uk/news/gcse-history-historic-environment-sites-2026-2028. If a school is using this content for the 2027 or 2028 cycle the site may differ — the lesson
- Daily life topics in Part 2 of the spec (education, family life beyond fashion, food, music) are folded into Lessons 9 and 12 rather than given a dedicated lesson, in order to keep the historic environment with two lessons of run-up (12 and

**norman-england:**
- Lesson 7 (Castles) introduces the White Tower in passing. If AQA later confirms a different 2026 site (highly unlikely — the 2026-2028 cycle is publicly announced), the Pevensey-specific synthesis in Lesson 13 would need a rebuild.

_(...11 more gap entries — see master JSON `aggregated_gaps`)_

---

## Files written

- `scripts/_plan_history-aqa.json` (552 KB) — master plan, the input for Phase 2 subject activation
- `scripts/_plan_history-aqa-shell.json` — subject shell from the first planner pass
- `scripts/_plan_history-aqa-{slug}.json` × 16 — per-option deep plans
- `scripts/_plan_history-aqa-summary.md` — this document

## What I want you to look at first

1. The 16 options table above — sort order within each section is opinionated (Germany first in periods, Inter-War first in wider world, Health first in thematic, Elizabethan first in British depth). Push back if a different order matches your sense of school uptake better.
2. Accent palette — every unit has a hex set. Section families are visually grouped (warm/cool/earthy/regal). Browse `scripts/_plan_history-aqa-shell.json` lines 57-313 to scan.
3. Question types list above — these get hard-coded into `getGuideUrl()` at activation time. Add or rename if anything reads wrong.
4. Slug — currently `history-aqa`. Existing free-tier Edexcel sits at bare `history`. Decide whether to rename Edexcel to `history-edexcel` for consistency, or leave the inconsistency with a doc note.
5. The gap list above — mostly housekeeping but a couple may want your call (e.g. "medieval migrants are spec-implied not spec-named" on the Migration option).

Once you give the nod, I move to Phase 2 (subject activation) and Phase 3 (content generation for 214 lessons in parallel batches).