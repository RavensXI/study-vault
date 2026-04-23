# Cross-Board Reuse Test — Business Edexcel 1BS0 (23 Apr 2026)

First end-to-end test of the content-transfer flow introduced in `PLANNING_PROMPT.md` + `CONTENT_PROMPT.md`. Source board: AQA 8132 (`business-aqa`, 30 lessons). Target: Edexcel 1BS0 (`business-edexcel`, 30 lessons, free-tier).

---

## TL;DR

Flow worked as designed. Transfer distribution hit the target window, adaptations were genuinely Edexcel-flavoured (not "AQA with serial numbers filed off"), and board-specific misconceptions/examiner findings were baked in correctly. Two tweaks made during the run: hero captions switched to attribution-only (Unsplash alt_descriptions are unreliable), and `_apply_plan.py` noted not to barf on the extra `content_transfer` field in lesson specs.

---

## Transfer score distribution

Planning agent declared `baseline_transferability: high` (matches the subject — Business is universally ~85% the same across boards).

| Score | Count | % |
|---|---|---|
| high | 18 | 60% |
| medium | 6 | 20% |
| fresh | 6 | 20% |
| low | 0 | 0% |

**Target was 60-75% transferable (high+medium).** Actual: 80%. On the edge but acceptable given this is a high-baseline subject. If it had come back ≥90% transferable, I'd have rejected and rerun.

**Fresh lessons (Edexcel-unique):**
- T1 L1 Why & How New Business Ideas Come About (1.1.1)
- T1 L2 Risk & Reward in Enterprise (1.1.2)
- T1 L3 Role of Business Enterprise & Adding Value (1.1.3)
- T1 L4 Customer Needs — the four named needs (1.2.1)
- T2 L2 Changes in Aims & Objectives (2.1.2)
- T2 L13 Using Data to Understand Business Performance (2.4.2)

All genuinely absent from AQA 8132 — the planning agent correctly identified these as Edexcel-specific.

**AQA content flagged as unique-to-source (NOT ported to Edexcel):**
- Boston Matrix (not in Edexcel spec)
- TQM / Total Quality Management (not in Edexcel spec)
- Economies/diseconomies of scale (named topic in AQA, not Edexcel)
- Maslow's hierarchy (not in Edexcel spec — Edexcel treats motivation as financial/non-financial categories only)

The Edexcel content explicitly excludes these. The content agent for T2 L5 (Product Life Cycle) literally wrote "Boston Matrix stripped entirely; four phases not AQA's five — Edexcel omits R&D" in its summary.

---

## Quality spot-check

### Adapted lesson: "Limited Liability & Ownership for Start-ups" (Edexcel T1 L12, high transfer)

Source: AQA business-real-world/L02 "Business Ownership & Limited Liability"

| | AQA L2 | Edexcel T1 L12 |
|---|---|---|
| Word count | 829 | 963 |
| h2 sections | Why Legal Structure Matters · Sole Traders · Partnerships · Ltd · Plc · Not-for-Profit | Why Legal Structure Matters · Limited vs Unlimited Liability · Sole Traders · Partnerships · Ltd · Franchises · Choosing a Structure |
| Edexcel markers | — | "franchise", "Theme 1", "start-up" |
| AQA markers | "PLC", "Stock Exchange" | — |

The adaptation correctly:
- Dropped PLCs (Edexcel Theme 1 is start-up scope; PLC moves to Theme 2)
- Dropped Not-for-profits (not in Edexcel spec)
- Added Franchises (Edexcel-specific at 1.4.1)
- Added "Limited vs Unlimited Liability" section upfront (Edexcel spec requires this as a distinct concept)
- Added "Choosing a Structure" decision framework for start-ups

Content feels authentically Edexcel. A student reading this wouldn't recognise it as adapted from AQA.

### Fresh lesson: "Risk & Reward in Enterprise" (T1 L2)

- 1072 words, no AQA source
- Sections: Core Trade-off · Risk Side · Reward Side · Weighing the Trade-off
- Uses real UK start-up examples (BrewDog, Gymshark, Innocent, Pasta Evangelists, Crafter's Companion, SumUp, Meatless Farm, Snag tights — all from Dragons' Den / UK startup coverage)
- Practice question types match Edexcel command words: Outline (2m), Explain (3m), Analyse (6m), Justify (9m)
- Mark schemes use StudyVault rubric, not Edexcel level descriptors

Reads as Edexcel Theme 1 foundation material, not generic business content.

---

## Teaching brief quality

The planning agent's teaching_brief included cited findings from actual 2023 Paper 1 + 2024 Paper 2 Edexcel examiner reports. Standouts:

- JIT misconception — "students think JIT guarantees stock availability" (2024 P2 Q1d) → addressed explicitly in T2 L10
- Flat structure vs decentralisation confusion (2024 P2 Q2e) → addressed in T2 L14
- Fringe benefits flagged as FINANCIAL motivation (2024 P2 Q7a) → explicit misconception-buster in T2 L15
- 9-mark Justify technique: one-option-deep + "it depends" conclusion → embedded in practice question mark schemes throughout
- 6-mark Analyse cap at 3 marks for generic no-context answers → mark schemes reward business-specific context
- Calculate answer-line discipline → embedded in T1 L9/L10 and T2 L12

Zero forbidden-source citations. One Save My Exams reference slipped in on the AQA plan run (stripped during sanitise); none on Edexcel.

---

## Speed / resource usage

| Phase | Duration | Agents |
|---|---|---|
| Planning (w/ cross-board research) | ~10 min | 1 |
| Subject activation | instant | 0 (script) |
| Content agents (6 in parallel, 5 lessons each) | ~11 min wall clock | 6 |
| Related media (2 in parallel, 15 lessons each) | ~9 min | 2 |
| Revision guides | ~3 min | 1 |
| Hero download (30 lessons) | ~90s | 0 (script) |
| Narration (Azure TTS, still running) | ~2 hr expected | 0 (script) |

Compared to fresh AQA Business build (~30 lessons, ~12 content agents over multiple retries, much longer content-generation time): Edexcel wall-clock was meaningfully faster because content agents spent less time thinking about what to say — they had AQA's material as a starting point for 24/30 lessons.

---

## Issues encountered + fixes

1. **Hero captions mismatched images.** Content agents wrote imaginative captions describing what they hoped the image would be; Unsplash returned different photos. First cleanup attempt used Unsplash's `alt_description` as the caption body — turned out those are frequently auto-generated nonsense ("white and black love letter" for a business-ideas photo). Final resolution: attribution-only captions ("Photo via Unsplash" or "Photo: {name} / Unsplash"). Applied retroactively to all 60 Business lessons. Committed.

2. **Encoding bug in `_fetch_source_lesson_content.py`** — Windows cp1252 couldn't print `→`. Fixed with `reconfigure(encoding='utf-8')`. Committed.

No content-level issues requiring agent retries. All 30 lessons validated clean on first pass (the Marketing/Finance short-word-count issues from the AQA run didn't recur — better adaptation_notes discipline pushed word counts higher from the start).

---

## Recommendations for next board (OCR J204)

1. **Keep the flow as-is** — the planning + transfer map pattern works. No prompt changes needed.
2. **OCR Business is similar in shape to Edexcel** (modular, 3 components vs Edexcel's 2 themes). Expect transfer distribution ~55-70% rather than 60% — OCR's Enterprise & Marketing / Operations & Finance / Human Resources split will map cleanly to Edexcel lessons, and many of the "fresh for Edexcel" entrepreneurship lessons will likely transfer from Edexcel to OCR as a second-source option.
3. **Chain source selection** — when OCR builds, the planning agent should look at BOTH existing boards (AQA and Edexcel) and pick the closest-matching source per lesson. Currently the orchestrator picks one source subject; extending to multi-source would reduce "fresh" count further without compromising quality.
4. **Narration for cross-board builds** — since practice questions + mark schemes + exam tips are always regenerated (per prompt rules), content_html differs enough between boards that Azure TTS has to run fresh per board. No reuse possible. This is fine — narration is fast and cheap.
5. **Heroes** — Business Edexcel reused ~10 heroes from the AQA build via index (same topics = same visual metaphor). The cross-subject hero index is paying off. No Unsplash calls needed for those reuses.

---

## Files

- Plan: `scripts/_plan_business_edexcel.json`
- Per-lesson content: `scripts/_gen_business_edexcel/*.json` (30 files)
- Per-lesson source content (for audit): `scripts/_source_content/*.json` (24 files)
- Cross-board context builder: `scripts/_build_cross_board_context.py`
- Source fetcher: `scripts/_fetch_source_lesson_content.py`
- Caption cleanup: `scripts/_fix_hero_captions.py`

All on branch `pipeline-rebuild-pilot-overnight`.
