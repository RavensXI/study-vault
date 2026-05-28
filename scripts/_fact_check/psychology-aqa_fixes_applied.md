# Fact-Check Fixes Applied: Psychology AQA (8182)

**Date applied:** 2026-05-28  
**Applied by:** Claude Code (Sonnet 4.6)  
**Source report:** `psychology-aqa.json` / `psychology-aqa.md`

---

## Per-Finding Results

| # | Severity | File | Status | Note |
|---|----------|------|--------|------|
| 1 | HIGH | perception_L03 (`4f4d2702`) | **PASS** | Müller-Lyer fin/corner explanation corrected: inward fins → outside corner of building (closer/shorter); outward fins → inside corner of room (further/longer). |
| 2 | HIGH | social-influence_L02 (`2a61473b`) | **PASS** | Milgram (1963) study added as new Key Fact block (n8): 40 male participants, 15V–450V in 30 increments, four verbal prods, 65% gave max 450V, all gave ≥300V. Narration IDs n8–n26 shifted to n9–n27. |
| 3 | HIGH | memory_L02 (`ab626ef1`) | **PASS** | Peterson & Peterson (1959) added as new collapsible (n9): trigram + counting task, 3–18s intervals, recall ~5% at 18s. Narration IDs n9–n24 shifted to n10–n25. |
| 4 | MED | psychological-problems_L02 (`fbf12185`) | **PASS** | Beck's Cognitive Triad named explicitly in n18: Beck (1979), cognitive triad, negative view of self/world/future. Attribution-style content retained; context makes both models visible. |
| 5 | MED | perception_L04 (`5339426d`) | **PASS** | Gilchrist & Nesberg method revised: images darkened then participants adjusted brightness; deprived participants systematically *overestimated* brightness — not a matching task. Duration range 1–16 hours added. |
| 6 | MED | social-influence_L03 (`8263fc26`) | **PASS** | Piliavin: drunk confederate now "smelling of alcohol" added; help rates 95% (ill) and ~50% (drunk) added to results; ill victim "typically within 70 seconds" added. |
| 7 | MED | language-thought-communication_L01 (`4e05cab1`) | **PASS** | Whorf/Hopi: Malotki (1983) named; "challenged" upgraded to "widely considered an error"; weak version retained with positive framing. |
| 8 | MED | language-thought-communication_L02 (`bf92da7d`) | **PASS** | Von Frisch: round dance threshold ~50–100m added; waggle dance ">~100m" added; "longer waggle run = greater distance" added. dfn data-def attributes updated to match. |
| 9 | LOW | social-influence_L01 (`e06035e9`) | **PASS** | Asch "several other people" → "several other people (typically seven confederates)". |
| 10 | LOW | social-influence_L01 (`e06035e9`) | **PASS** | "12 out of 18 trials" → "12 out of 18 trials (the critical trials)". |
| 11 | LOW | memory_L03 (`8b25369b`) | **PASS** | Murdock method: "a set rate" → "typically 20 words, presented at a rate of one word per second". |
| 12 | LOW | psychological-problems_L03 (`9b516a6c`) | **PASS** | Antidepressants: "quick-acting relative to talking therapies" → "typically take 2–6 weeks…faster than CBT, but not quick in absolute terms". |
| 13 | LOW | development_L02 (`6dcb5640`) | **PASS** | Piaget: added "his age ranges are now considered conservative" to evaluation paragraph. |
| 14 | LOW | brain-neuropsychology_L02 (`f98b558f`) | **PASS** | Dopamine: "reward-seeking behaviour" + "This mechanism also underlies addiction" added (optional enhancement). |

**Total: 14/14 PASS, 0 FAIL, 0 SKIPPED**

---

## Validator Results

All 13 modified JSON files passed `_validate_content_json.py`:

```
[OK] perception_L03.json
[OK] social-influence_L02.json
[OK] memory_L02.json
[OK] psychological-problems_L02.json
[OK] perception_L04.json
[OK] social-influence_L03.json
[OK] language-thought-communication_L01.json
[OK] language-thought-communication_L02.json
[OK] social-influence_L01.json
[OK] memory_L03.json
[OK] psychological-problems_L03.json
[OK] development_L02.json
[OK] brain-neuropsychology_L02.json
```

---

## Re-narration Required

### Full re-narrate (narration IDs renumbered — clear manifest, re-narrate all chunks)

| lesson_id | File | Reason |
|-----------|------|--------|
| `2a61473b-02dd-49ea-bad9-ae8c4ee160f7` | social-influence_L02 | New n8 block inserted; old n8–n26 shifted to n9–n27 |
| `ab626ef1-c7cb-4f91-bc33-b498f49f8238` | memory_L02 | New n9 block inserted; old n9–n24 shifted to n10–n25 |

### Selective re-narrate (text changed within existing chunks only)

| lesson_id | File | Changed chunk(s) |
|-----------|------|-----------------|
| `4f4d2702-76ee-437a-b1ee-44b1bd694625` | perception_L03 | n10 (Müller-Lyer paragraph) |
| `fbf12185-4842-45a8-8832-2c4a9db31974` | psychological-problems_L02 | n18 (psychological theory paragraph) |
| `5339426d-d46a-4409-a5a6-642eddbf9812` | perception_L04 | n10 (Gilchrist Key Fact block) |
| `8263fc26-3fc6-48fb-bd4c-802d092910b8` | social-influence_L03 | n15 (method), n16 (results) |
| `4e05cab1-ccf2-47e3-952b-461b1dcaff8a` | language-thought-communication_L01 | n13 (Hopi paragraph) |
| `bf92da7d-40fd-43d0-9a50-639ebc37555a` | language-thought-communication_L02 | n11 (Von Frisch results paragraph) |
| `e06035e9-3635-4972-8e40-54a2cb1ad51c` | social-influence_L01 | n17 (method paragraph) |
| `8b25369b-36f4-49a7-a83e-91c32da0b92c` | memory_L03 | n11 (Murdock Key Fact block) |
| `9b516a6c-f5b1-4056-ba30-b48b27482c4a` | psychological-problems_L03 | n18 (evaluation paragraph) |
| `6dcb5640-7d05-44fc-8897-effc26e2013f` | development_L02 | n15 (evaluation paragraph) |
| `f98b558f-16c5-45dc-a77c-43a3bd66288b` | brain-neuropsychology_L02 | n13 (dopamine paragraph) |

---

*All DB updates and JSON file updates applied atomically; no partial states.*
