# Practice Build — Master Plan

**Status:** proposal, for Tom to review. Nothing here has been built.
**Written:** 12 August 2026, after the teacher-platform session.
**Question it answers:** the build pipeline predates practice-format lessons. What
would it take to make it build them, and is that the right thing to build?

---

## 1. The finding, in one paragraph

There is no practice pipeline. There are **seven hand-built factories**, one per
subject family, written between April and August, sharing no code and only
partly sharing a schema. Meanwhile the newest and best build machinery —
`scripts/api_build/driver.py`, which produced D&T Edexcel and the Psychology
arms — is **explicitly article-only**: it hardcodes `"practice_units": []` and
treats a practice unit appearing in a plan as a drift error
(`"unexpected practice_units for an article subject"`). So the modern route
actively refuses practice, and the practice route is not a route at all.

The good news, which changes what the fix looks like: **the data format already
generalises.** Every practice family stores the same envelope. Music, built last
week and the most exotic subject we have, needed no schema change whatsoever.

---

## 2. What actually exists (evidence, not memory)

### 2.1 Practice-format subjects live today

36 of 109 live subjects carry `settings.practice_units`. By family:

| Family | Boards | Practice units per board | Sampled problems |
|---|---|---|---|
| English Language | 5 (incl. Unity) | 4 (reading + writing × 2 papers) | 608 |
| Maths | 4 | 6 (number, algebra, graphs, ratio, geometry, prob/stats) | 953 |
| Science (Combined) | 5 | 3 (physics calc, chemistry calc, biology data) | 300 |
| Separate Sciences | 5 | 4 (+ higher-calculations) | 420 |
| Geography | 6 (incl. Edexcel A/B) | 1 (geographical-skills) | 280 |
| Spanish / French / German | 3 each | 3 (AQA) or 6 (Edexcel) | 520 each |
| Statistics | 1 | 3 | 370 |
| Music | 1 | 4 (western-classical, score-reading, listening, aos-listening) | 228 |

### 2.2 The envelope is already common

Every practice lesson stores a `practice_data` object. Blocks observed:

| Block | Maths | EngLang | MFL | Science | Geog | Music | Stats |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `method_card` | ● | ● | ● | ● | ● | ● | ● |
| `problem_bank` | ● | ● | ● | ● | ● | ● | ● |
| `worked_examples` | ● | ● | ● | ● | ● | ● | ● |
| `topic_links` | ● | ● | — | ● | ● | — | ● |
| `exam_context` | — | ● | ● | ● | — | ● | ● |
| `tier_guides` | ● | — | — | ● | ● | — | ● |
| `guided` | ● | — | — | ● | ● | — | ● |
| `passages` | — | ● | — | — | — | ● | — |
| `ai_marking_prompts` | — | ● | ● | — | — | — | — |
| `related_videos` | ● | — | — | ● | ● | — | — |

`problem_bank` is keyed by tier — `bronze`, `silver`, `gold`, plus
`*_description` strings — in **every** family. That is a stronger shared
foundation than the seven separate factories suggest.

### 2.3 Input types actually in use

`input_type` on each problem is what `practice-loader.js` renders.

| Type | Families using it |
|---|---|
| `multiple_choice` | all seven — the universal one |
| `single_value` | Maths, Science, Separate Sciences, Geography, Statistics |
| `ai_mark` | English Language, MFL |
| `translate`, `gap_fill`, `dictation`, `sentence_builder`, `vocab_match`, `spot_correct`, `role_play` | MFL |
| `highlight_evidence`, `traffic_light`, `connotation_picker`, `evidence_match`, `misleading_summary`, `improve_sentence`, `spot_error` | English Language |
| `fraction`, `two_solutions` | Maths, Statistics |
| `xy_pair` | Maths only |
| `standard_form` | Maths, Science, Separate Sciences |
| `reorder` | English Language, MFL, Music |

Counts are lopsided in a way that matters for sequencing: Maths is 65%
`single_value`, Science 89% `single_value`, Geography 58%/42% two types only.
English Language and MFL are the genuinely diverse ones.

### 2.4 Music proves the envelope stretches

Music score-reading and listening use `passages` with `{id, text, label}` and
problems carrying `passage_id` — the same mechanism English Language uses for
reading extracts. Inline SVG notation and audio players live inside the passage
`text`. **No new schema, no new input types** beyond the universal ones. That is
the single most encouraging fact in this document: a subject nobody anticipated
fitted the format without changing it.

---

## 3. Where the gap actually is

| Layer | State |
|---|---|
| `practice.html` + `practice-loader.js` | **Fine.** Renders every type above. Not the problem. |
| `practice_data` schema | **Fine.** Common envelope, tiered bank, proven across seven families. |
| `api/pipeline/approve-plan.js` | **Fixed 12 Aug.** Now reads `article_units` + `practice_units` and reports `practice_units` for `subjects.settings`. |
| `scripts/api_build/driver.py` | **Article-only by design.** Rejects practice plans. This is the real blocker. |
| Web pipeline generation stage | **Does not exist.** upload → parse → plan → approve, then nothing. Generation is local scripts. |
| `docs/PRACTICE_PIPELINE.md` | **Stale (15 May).** Documents 8 stages and a type registry, but points at `scripts/factory/FACTORY_RULES.md`, which no longer exists — only `_passage_audio/` and `voice_samples/` remain in that directory. Music is absent from the registry. |
| Per-family factories | Seven, unshared. Newest (Music, 10–11 Aug) is the most bespoke: `notation.py`, `audio_features.py`, per-lesson builders. |

**So a department uploading a scheme of work for a practice subject today gets a
correct plan and then nothing.**

---

## 4. Recommendation

### 4.1 Build one practice stage inside `driver.py` — do not build an eighth factory

`driver.py` already has the expensive parts: config, state, resume, usage
logging, cost accounting, Supabase writes, plan checking, reference-lesson
fetching, drift detection. A practice build needs all of those and differs only
in **what it asks for per lesson** and **what shape it writes**.

The change is therefore: teach `driver.py` that a unit has a format, and give it
a practice generation path alongside the article one. Not a parallel programme.

### 4.2 Adopt the eight stages that already work

`docs/PRACTICE_PIPELINE.md` describes stages proven on English Language Paper 1
Reading, and the reason for them is sound and worth preserving verbatim:

> one agent producing a whole lesson's 20 problems thins toward the end (silver
> and gold are worse than bronze)

Sequence: passages/specs → method card → bronze → silver + worked examples →
gold → worked examples → AI-marking prompts (subject-level, once) → topic links.

Two amendments based on what the data now shows:

- **Tier descriptions are part of the bank**, not an afterthought
  (`bronze_description` etc. exist in every family and are currently produced
  inconsistently).
- **`guided` / `guided_steps` need their own stage.** Maths and Science carry
  step-by-step scaffolds inside problems (`guided_steps: [{say, pre, hint,
  answer}]`). These are the highest-value and most error-prone part, and folding
  them into the bronze stage is exactly the thinning problem the staging exists
  to avoid.

### 4.3 Sequence the families by difficulty, not by demand

Do them in this order regardless of which subject is wanted first, because each
one earns the next:

1. **Science calculation units** — 3 input types, 89% one type, existing schema
   doc (`scripts/science-practice/SCIENCE_PRACTICE_SCHEMA.md`), tight
   deterministic answers. This is the canary.
2. **Maths / Statistics** — 6 types, adds `guided_steps`, KaTeX, Chart.js.
   Statistics is Maths with different data-viz, so it comes nearly free.
3. **Geography Skills** — 2 types but custom panels (charts, OS maps, ruler).
   Tests the passage/panel mechanism.
4. **MFL** — 10 types, AI marking, dictation audio (Azure). Highest asset
   dependency.
5. **English Language** — 11 types, passages with narration, AI marking and
   AI writing. Do last; it is the one the staged approach was invented for, and
   by then everything else will have shaken out.

**Music is deliberately not on this list.** It should stay artisanal. Its value
is in curated public-domain audio and hand-checked notation, and a generic
factory would produce worse music lessons than Tom does by hand. Recording that
as a decision is better than discovering it later.

### 4.4 Canary before fleet

Per the standing rule: build **one Science calculation unit for one board**,
read the real token cost, and only then decide the shape of the rest. An article
arm ran about $9. A practice lesson is 20 problems across three tiers plus
guided steps and worked examples, so expect meaningfully more per lesson — but
guess nothing; measure it.

---

## 5. What this does NOT need

Worth stating so the work doesn't sprawl:

- **No renderer changes.** `practice-loader.js` already handles every type.
- **No schema migration.** The envelope is right. Existing content stays.
- **No new database columns.** `practice_data` and `settings.practice_units`
  already carry everything.
- **No rework of existing practice content.** ~4,000 problems are live and fine.
  This is about building the *next* subject, not rebuilding the last seven.

---

## 6. Decisions only Tom can make

1. **Does a department get to build a practice subject at all?** Article
   generation is one agent per lesson. Practice is roughly eight, over 20
   problems, three tiers. If a department build is included in a licence, the
   cost difference between "History, 40 lessons" and "Maths, 48 practice
   lessons" is large enough to matter to pricing. It may be right to offer
   article-format builds to departments and keep practice as something Tom runs.

2. **Fact-check for practice.** The mandatory Phase 6 fact-check assumes prose.
   A practice bank needs *answer* verification — a wrong `solutions` value is
   worse than a wrong sentence, because the student is told they are wrong when
   they are right. (Today's Tybalt question is exactly this failure in an
   article subject.) That is a different check and probably a different tool.

3. **Does `docs/PRACTICE_PIPELINE.md` become the spec, or get rewritten?** It is
   three months old and points at a deleted file, but its staging rationale is
   still correct and hard-won. Recommend: keep the stages, refresh the registry,
   add Music, fix the dead reference.

---

## 7. Suggested first three days of work

| Day | Work |
|---|---|
| 1 | Refresh `docs/PRACTICE_PIPELINE.md` against reality: add Music, add `guided`/`tier_guides` blocks, fix the `scripts/factory/FACTORY_RULES.md` reference, document the tiered bank shape properly. This is the spec everything else is built against — do it before writing code. |
| 2 | `driver.py`: make units format-aware end to end (plan → plancheck → activate), and stop treating `practice_units` as drift. No generation yet — just make an honest practice plan survive the pipeline. |
| 3 | Stages s1–s3 for one Science calculation unit. Canary the cost. Stop and read the numbers before going further. |

---

## 8. Two things I chased down, one of which is a real risk

### 8.1 The English Language factory is gone, and was never in git

`scripts/factory/` has **never been tracked**. Not deleted — never committed.
`git log --all -- "scripts/factory/*"` returns nothing, and `git ls-files` is
empty for that path. Only `_passage_audio/` and `voice_samples/` remain on disk.

So the factory that produced 608 English Language problems across five boards,
and which `docs/PRACTICE_PIPELINE.md` names as the proven reference
(`scripts/factory/FACTORY_RULES.md`), **cannot be recovered or reused**. It
exists only as whatever the pipeline doc records about it.

Every other family survived properly — language-practice 3/3 `.py` tracked,
science-practice 2/2, music-practice 40/40. The one that got away is the one the
whole staged approach was invented on.

Two consequences:

- English Language moving to last in the sequence (§4.3) turns out to be
  doubly right: it is both the most complex family AND the one with no surviving
  implementation to copy.
- Whatever gets built should live in git from the first commit. Worth a
  `.gitignore` check before starting, since something evidently kept that
  directory out.

### 8.2 Statistics confirmed — it is Maths, with a different mix

370 problems: `single_value` 207, `multiple_choice` 127, `fraction` 25,
`two_solutions` 11. No unique types. It genuinely comes nearly free once Maths
is done, as §4.3 assumes.

`xy_pair` is Maths-only. `two_solutions` and `fraction` are shared with
Statistics; `standard_form` is shared with both sciences. So the "Maths types"
are really *quantitative* types, and the registry should say so.
