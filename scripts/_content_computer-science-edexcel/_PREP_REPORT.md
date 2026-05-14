# Workspace Prep Report — Computer Science Edexcel (1CP2)

Date: 2026-05-14
Prepared by: workspace setup agent (Phase 3 prep)

## Files created

| File | Purpose |
|------|---------|
| `_AGENT_PROMPT.md` | Content agent instructions — adapted from AQA version |
| `_aqa_source_lessons.json` | 26 AQA 8525 lessons from Supabase (7 units, keyed by unit_slug) |
| `_reference_lesson.json` | RE L01 "Worship & Prayer" structural template (copied from AQA workspace) |
| `_batch_b01.json` | Computational Thinking — 5 lessons |
| `_batch_b02.json` | Data — 4 lessons |
| `_batch_b03.json` | Computers — 4 lessons |
| `_batch_b04.json` | Networks — 4 lessons |
| `_batch_b05.json` | Issues and Impact — 3 lessons |
| `_batch_b06.json` | Programming with Python — 6 lessons |
| `_RELATED_MEDIA_PROMPT.md` | Related media curation prompt (adapted from AQA version, run post-content-gen) |

## Batch breakdown

| Batch | Unit | Lessons | Transfer scores |
|-------|------|---------|----------------|
| b01 | Computational Thinking | 5 | high×2, medium×1, low×1, fresh×1 |
| b02 | Data | 4 | medium×2, low×1, fresh×0 (all have transfer notes) |
| b03 | Computers | 4 | high×2, medium×2 |
| b04 | Networks | 4 | medium×2, high×1, fresh×1 (topologies — AQA-unique) |
| b05 | Issues and Impact | 3 | medium×3 |
| b06 | Programming with Python | 6 | high×1, medium×4, fresh×1 (CSV/validation — AQA-unique) |

**Total: 26 lessons across 6 batches**

## Lesson IDs confirmed

All 26 Edexcel CS lesson shells were confirmed live in Supabase (subject_slug `computer-science-edexcel`, school_id NULL). Each batch file includes the `lesson_id` for every lesson — content agents write directly to these rows.

## AQA source data

26 AQA 8525 lessons fetched from Supabase across 7 units: algorithms (4), programming (5), data-representation (4), computer-systems (4), networks-cyber-security (4), databases-sql (3), ethical-legal-environmental (2). Stored in `_aqa_source_lessons.json` keyed by unit_slug.

Note: the databases-sql and parts of computer-systems units contain AQA-unique content that content agents must NOT transfer. The `content_transfer.adaptation_notes` in each batch lesson documents exactly what to lift and what to drop.

## Key Edexcel divergences flagged in _AGENT_PROMPT.md

1. **Pseudocode policy** — plain-English descriptions ONLY in Unit 1; no formal pseudocode dialect
2. **Python 3 only** — no C# examples anywhere
3. **Binary multiples** — KiB/MiB/GiB/TiB (1024-based), not kB/MB/GB/TB
4. **8 unique-to-Edexcel topics** — two's complement, arithmetic shifts, KiB/TiB, audit trails, network topologies, AI/ML ethics (4 issues), CSV files, pattern-check validation
5. **5 AQA-only topics excluded** — XOR/logic circuits, Huffman/RLE, SQL/databases, biometrics/CAPTCHA, Unicode
6. **14 Edexcel command words** — Discuss (6m) instead of Compare-and-Contrast; no 8-mark Extended Response

## Spec file note

`specs/edexcel/computer-science-1CP1.md` — filename says 1CP1 but content covers the current 1CP2 specification. Content agents are notified in `_AGENT_PROMPT.md`.
