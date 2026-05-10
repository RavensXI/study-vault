# Tier Differentiation Plan — Languages + Maths

**Status:** Sciences complete (merged 2026-05-10). This runbook closes out the remaining tiered subjects.

## What we learned from Sciences

GCSE England has only three tiered subject families:

1. **Mathematics** (4 boards) — practice-first format
2. **Combined / Triple Sciences** (8 variants) — article format ✅ done
3. **Modern Foreign Languages** (French, German, Spanish) — article format

The Sciences pipeline produced:
- 1,286 within-content HT chunks tagged across 8 subjects
- 6 fully-HT lessons flagged `tier='higher'` (browse-loader hides them on Foundation)
- 119 spec-point coverage gaps catalogued for future content commissioning

The mechanism (Sciences = canonical):
- Lesson row has `tier` field: `both` | `higher` | `foundation`
- Within lesson content_html, HT-only paragraphs wrapped in `<div class="higher-only">`
- Narration manifest entries get `tier:"higher"` for chunks inside higher-only ancestors
- Browse-loader filters tier='higher' rows for Foundation; lesson-loader skips them in prev/next + shows friendly message on direct URL
- Player skips manifest entries with `tier:"higher"` when body has `tier-foundation` class

**Key audit finding:** Maths' Bronze/Silver/Gold problem tiers are difficulty levels, NOT exam tiers. Foundation students can solve Gold problems too (e.g., `(3x-2)(2x+5)` expansion) — they're just harder. So per-problem tier flags are NOT needed for Maths. The 16 entirely-Higher lessons already filter the right things.

---

## Tomorrow's runbook

### Step 0 — Confirm Sciences QA on live (`www.studyvault.co.uk`)

5 minutes. Just verify the PR #9 merge deployed cleanly. Spot-check on Foundation tier:
- `/browse/separate-sciences-edexcel/physics-paper-2` → 6 cards (or 9 cards if you didn't add Triple practice units before merge — check `scripts/_copy_combined_practice_units_to_triple.py`, that script wrote directly to Supabase so it's live regardless of merge)
- Open one lesson with wraps, verify HT sections hidden visually + skipped in narration

If anything's off, fix before proceeding.

### Step 1 — Maths: no work needed, just verify (10 min)

Lesson-level filtering is already correct (16/48 entire lessons are `tier='higher'`; Foundation users don't see them). Bronze/Silver/Gold is difficulty within a lesson, not tier. No within-lesson differentiation needed for the practice-first format.

**Verification only:**
```bash
PYTHONIOENCODING=utf-8 python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'scripts')
from lib.supabase_client import get_client
sb=get_client()
for slug in ['maths-aqa','maths-edexcel','maths-ocr','maths-eduqas']:
    s = sb.table('subjects').select('id').eq('slug',slug).is_('school_id','null').single().execute().data
    units = sb.table('units').select('id').eq('subject_id', s['id']).execute().data
    h = b = 0
    for u in units:
        L = sb.table('lessons').select('tier').eq('unit_id', u['id']).execute().data
        h += sum(1 for l in L if l.get('tier')=='higher')
        b += sum(1 for l in L if l.get('tier') in ('both', None))
    print(f'{slug}: Foundation visible={b}, Higher visible={b+h}')
"
```

Expected: ~32 Foundation, ~48 Higher per board. If matches, Maths is DONE.

### Step 2 — Languages: lesson-level tier audit (15 min)

MFL specs don't have inline HT markers like Sciences (different spec convention — language acquisition tiering is topic-level, not paragraph-level). Most lessons are tier='both'. We need to identify which lessons are entirely Higher-only and flip those.

**Investigate which MFL grammar topics are HT-only per board.** AQA examples typically:
- Subjunctive mood
- Pluperfect tense
- Passive voice with all tenses
- Conditional perfect
- Some uses of relative pronouns

**Method:**
1. Read each MFL spec's Foundation vs Higher grammar matrix (usually pages 30-50 of the PDF).
2. Map to existing lesson titles in `spanish-aqa`, `french-aqa`, `german-aqa` (and Edexcel variants).
3. Flip matching lessons to `tier='higher'`.

Don't dispatch agents for this — it's a ~50-line manual mapping per subject (smaller than Sciences). One Python script with a hardcoded list of "lesson title → tier" mappings derived from the spec.

**Decision rule:** if a lesson's title contains a grammar topic that's Higher-only per spec, flip it. Otherwise leave as `both`. Skip vocabulary/topic-content lessons (those are both tiers, just deeper for Higher).

### Step 3 — Languages: within-content HT wraps (optional)

The AQA MFL subjects already have some scattered `higher-only` spans (7-13 per subject). Whether to formalise these via the Sciences pipeline depends on agent yield. Worth a small pilot:

1. Run extract_ht_per_paper-style script on `specs/aqa/spanish-8692-8692.md` (it has 2 HT markers — likely too few for a useful extract).
2. If yield is low, skip the agent pipeline for Languages entirely. The existing scattered wraps + lesson-level filter is enough.

**My recommendation:** skip Step 3. MFL practice-first format doesn't reward paragraph-level tier wrapping the way Sciences article format does. Time better spent elsewhere.

### Step 4 — Memory + docs updates

After Steps 1-2 complete:

#### A. Update CLAUDE.md
Add a "Tier Differentiation Status" section under the subjects table:

```
## Tier differentiation status

- **Sciences (8 variants)** — full differentiation: lesson-row tier + within-content `.higher-only` divs + narration tier-flag filtering.
- **Mathematics (4 boards)** — lesson-row tier only (16/48 Higher-only topics). No within-lesson differentiation needed — Bronze/Silver/Gold is difficulty, not tier.
- **Languages (Spa/Fr/Ge × AQA/Edexcel)** — lesson-row tier only (Higher-only grammar topics flipped).
- All others: single-tier (no Foundation/Higher split in the reformed 9-1 spec).
```

#### B. Save memory file: `feedback_tier_differentiation_pipeline.md`

```markdown
---
name: Tier differentiation pipeline for Foundation/Higher subjects
description: How StudyVault handles Foundation vs Higher tier filtering across the three tiered GCSE families. Different mechanism per format (article vs practice).
type: feedback
---

GCSE England's reformed 9-1 spec has Foundation/Higher tiering on only:
- Mathematics
- Combined Science / Triple Science
- Modern Foreign Languages (French, German, Spanish — since 2024 reform)

**Article-format subjects (Sciences):** full pipeline.
1. Lesson row `tier` field: `both` | `higher` | `foundation`.
2. Within lesson content_html, wrap HT-only paragraphs in `<div class="higher-only">`.
3. Narration manifest entries inside higher-only ancestors get `tier:"higher"`.
4. browse-loader filters tier='higher' rows for Foundation users.
5. lesson-loader skips them in prev/next + shows friendly message on direct URL.
6. main.js narration player drops manifest entries with `tier:"higher"` when body has `tier-foundation`.

**Practice-format subjects (Maths, MFL):** lesson-row tier only.
- Mark entire HT-only topic lessons as `tier='higher'`.
- Don't tag individual problems — Bronze/Silver/Gold is difficulty within a topic, not tier.
- browse-loader filters as usual.

**When adding a new tiered subject's board variant** (e.g. new MFL board):
- Lesson plans must classify topics as Foundation/Higher per the spec.
- For article format: agents must wrap HT-only paragraphs.
- For practice format: mark entire HT-only topic lessons.

**HT marker conventions per board (Sciences):**
- AQA: `(HT only)` inline annotation — preserved by markitdown.
- Edexcel Combined: bold formatting only (stripped by markitdown — use PyMuPDF).
- Edexcel Triple: B/C/P suffix on spec codes (e.g. 2.10B = HT) — survives markdown.
- OCR (both Gateway and 21st Century): bold but mixed with chapter headings — use Claude vision PDF reading.

Pipeline script: `scripts/_pilot_higher_only/` (reusable for future builds).

**Coverage gaps doc:** `docs/ht-coverage-gaps/` lists HT spec points not yet developed in lesson prose, per subject. Input for future content-commissioning.
```

#### C. Update `docs/CONTENT_PROMPT.md`

Add a new section after the article-format schema:

```markdown
## Tier differentiation (Foundation/Higher subjects only)

For lessons in tiered subject families (Maths, Sciences, Modern Foreign Languages):

**Article-format lessons (Sciences only currently):**
- Identify spec points marked as HT-only (board-specific markers — see memory `feedback_tier_differentiation_pipeline`).
- Wrap matching paragraphs/sections in `<div class="higher-only">...</div>`.
- Wrap whole `<p data-narration-id>` elements — don't split paragraphs.
- Existing higher-only blocks: don't touch.
- If an entire lesson is HT-only (whole topic is Higher), the lesson row's `tier` field must be `'higher'` instead of wrapping content_html.

**Practice-format lessons (Maths, MFL):**
- Don't differentiate at the problem level (Bronze/Silver/Gold is difficulty, not tier).
- Whole-topic HT-only lessons: mark the lesson row's `tier='higher'`.
```

#### D. Update `docs/PIPELINE.md`

Add a Phase 7 or similar for tiered subjects:

```markdown
## Phase: Tier differentiation (tiered subjects only)

Skip for single-tier subjects. For Maths/Sciences/MFL board builds:

1. Generate HT extract per paper from the board's spec markdown (AQA) or PDF (Edexcel/OCR via PyMuPDF or Claude vision).
2. For article-format papers: dispatch agents per paper to wrap HT content.
3. For practice-format papers: identify whole-topic Higher-only lessons and flip their `tier` field.
4. Backfill narration manifest tier flags (article format only).
5. Detect fully-HT lessons (>=90% of content_html narration IDs inside .higher-only) and flip `tier='higher'`.
6. Verify browse-loader + lesson-loader filter correctly on Foundation tier preview.
```

### Step 5 — Future language boards

When a new MFL board variant comes in (e.g. spanish-ocr, french-eduqas):

1. Build subject as normal per `docs/PIPELINE.md`.
2. After content lands: identify HT-only grammar topics from the spec.
3. Flip those lesson rows `tier='higher'`.
4. Add the new subject to TIERED_OVERVIEW + TIERED arrays in `js/browse-loader.js`.
5. Add to TIERED_SUBJECTS + TIERED_LABELS in `index.html`.
6. Verify Foundation filter works on preview before merge.

### Step 6 — Future Sciences board builds

Same pipeline as this rollout. Reference scripts:
- `scripts/_pilot_higher_only/extract_ht_per_paper.py` — AQA-style markdown extraction
- `scripts/_pilot_higher_only/extract_ht_from_pdf.py` — Edexcel/OCR bold-aware PyMuPDF extraction
- `scripts/_pilot_higher_only/apply_and_backfill.py` — applies tagged content + manifest backfill
- `scripts/_pilot_higher_only/aggregate_coverage_gaps.py` — collects per-paper gap reports

---

## Estimated time tomorrow

- Step 0: 5 min QA
- Step 1: 10 min Maths verification
- Step 2: ~1 hour MFL spec audit + flip lessons across 6 subjects
- Step 4: 30 min memory + doc updates
- **Total: ~2 hours**

No agents needed. No risky operations. No supervision required between steps.

## What to do if something looks off

- Lesson disappearing wrongly on Foundation: check `subjects.settings.practice_units` and the lesson's `tier` field
- Lesson body empty on Foundation: that lesson is entirely HT — flip its row `tier='higher'`
- Foundation filter not firing: check `localStorage.studyvault-tiers` key matches subject slug (base or full)
- Browse-loader not recognising subject as tiered: add slug to `TIERED_OVERVIEW` + `TIERED` arrays in `js/browse-loader.js`
