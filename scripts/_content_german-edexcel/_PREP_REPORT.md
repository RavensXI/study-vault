# Edexcel German (1GN1) — Phase 3 Scaffolding Prep Report

**Date:** 2026-05-04
**Phase:** 3 (practice content generation — scaffolding only, no content generated yet)
**Subject:** German, Pearson Edexcel 1GN1, free tier
**Supabase subject_id:** `201bf775-6897-4bfe-a537-befc5da89ab0`

## Files created

All under `scripts/_content_german-edexcel/`:

| File | Purpose |
|---|---|
| `_AGENT_PROMPT.md` | Phase 3 content agent system prompt — German-adapted from Spanish Edexcel; embeds noun gender (der/die/das), four cases (Nominativ/Akkusativ/Dativ/Genitiv), verb-second main clauses, verb-final after weil/dass/obwohl/wenn, modal + infinitive at clause end, perfect-tense haben/sein split, separable verbs (prefix to clause end in main clauses; whole at end of subordinate; ge- between prefix and stem in past participle), strong vs weak verbs (irregular vs regular past), Konjunktiv II (würde / hätte / wäre / könnte / sollte / möchte), umlauts ä/ö/ü, ß, noun capitalisation (every noun), du vs Sie (Sie default for all 9 prescribed role-play settings), reflexive verbs accusative vs dative, kein vs nicht, haben + noun idioms, verb + gern. Voices for dictation references: `de-DE-ConradNeural` / `de-DE-KatjaNeural`. SSC drill points: ä/ö/ü, ie vs ei (opposite of English), ch hard /x/ vs soft /ç/, sch single phoneme /ʃ/, sp- /ʃp/ + st- /ʃt/, final-consonant devoicing (-b/-d/-g), -ig as /ɪç/, vocalic -er, eu/äu as /ɔɪ/. |
| `_RELATED_MEDIA_PROMPT.md` | German related-media curation prompt. HEAD-validated ROOT URLs only — sources biased to BBC Bitesize / BBC Sounds / Deutsche Welle (DW Learn German + Slowly Spoken News + Top-Thema) / iPlayer / Languages Online / Easy German / Coffee Break German / Slow German / Lingoni German / Smarter German. No fabricated deep links (per recent retraction). |
| `_reference_lesson.json` | Canonical structural reference — pulled `german-aqa` `people-and-lifestyle` L01 "Family Members and Relationships" (`practice_data` only). |
| `_spec_german-edexcel.txt` | Spec slice extracted from `specs/edexcel/german-2024-1GN1.md`. 8 sections: qualification overview, AOs, themes, role-play settings, vocab Appendix 1 overview + per-theme pointers, grammar Appendix 2 overview, Appendix 3 names, spec changes (incl. Issue 2 May 2025: dative plural -n moved to Foundation; ohne/um... zu and zu-infinitives moved to Foundation; sp- added to SSCs; euere → eure). **Auto-gitignored** via `.gitignore:25` (`scripts/_content_*/_spec_*.txt`). |
| `_source/` (17 files) | AQA German source `practice_data` for every plan lesson with `transfer_score` ∈ {high, medium}. **Auto-gitignored** via `.gitignore:26` (`scripts/_content_*/_source/`). |
| `_batch_t1_personal_world.json` | Theme 1 batch — 5 lessons. |
| `_batch_t2_lifestyle_wellbeing.json` | Theme 2 batch — 5 lessons. |
| `_batch_t3_neighbourhood.json` | Theme 3 batch — 4 lessons. |
| `_batch_t4_media_tech.json` | Theme 4 batch — 4 lessons. |
| `_batch_t5_studying_future.json` | Theme 5 batch — 4 lessons. |
| `_batch_t6_travel_tourism.json` | Theme 6 batch — 5 lessons. |
| `_prep_fetch.py` | One-shot prep script that pulled source lessons, the reference lesson, and built the 6 batch JSONs. Idempotent — read-only against Supabase. |
| `lessons/` | Empty output directory; agents write generated lesson JSONs here. |

## Source files pulled

17 unique files in `_source/`. Plan totals: **15 high + 6 medium + 3 low + 3 fresh = 27 lessons.** Source files cover the 21 high+medium lessons; some AQA source lessons are referenced by multiple Edexcel lessons (e.g. `aqa_people-and-lifestyle_lesson_8.json` is shared by Lifestyle T2 L01 (Daily Routine — medium) and T2 L03 (Physical Wellbeing — high); `aqa_communication-and-world_lesson_4.json` is shared by Travel L02 and L05; `aqa_popular-culture_lesson_3.json` is shared by Media L01 and L02; `aqa_people-and-lifestyle_lesson_5.json` is shared by Personal World L03 and Future L04), so 21 references resolve to 17 distinct files.

| Source unit | Files | Lesson numbers |
|---|---|---|
| `people-and-lifestyle` | 7 | 1, 4, 5, 6, 8, 9, 10 |
| `popular-culture` | 4 | 2, 3, 4, 8 |
| `communication-and-world` | 6 | 1, 2, 3, 4, 7, 8 |

## Batch breakdown

| Batch | Unit slug | Lessons | Tier mix | Transfer scores |
|---|---|---|---|---|
| `t1_personal_world` | `my-personal-world` | 5 | 4 both, 1 higher | 3 high, 0 medium, 1 low, 1 fresh |
| `t2_lifestyle_wellbeing` | `lifestyle-and-wellbeing` | 5 | 4 both, 1 higher | 3 high, 1 medium, 0 low, 1 fresh |
| `t3_neighbourhood` | `my-neighbourhood` | 4 | 4 both | 3 high, 0 medium, 1 low, 0 fresh |
| `t4_media_tech` | `media-and-technology` | 4 | 4 both | 1 high, 2 medium, 1 low, 0 fresh |
| `t5_studying_future` | `studying-and-my-future` | 4 | 4 both | 2 high, 1 medium, 0 low, 1 fresh |
| `t6_travel_tourism` | `travel-and-tourism` | 5 | 5 both | 3 high, 2 medium, 0 low, 0 fresh |
| **Totals** | | **27** | 25 both, 2 higher | **15 high, 6 medium, 3 low, 3 fresh** |

## German-specific gotchas baked into the agent prompt

The agent prompt explicitly drills these German-only rules (no English / French / Spanish parallel):

1. **Three genders (der/die/das)** — every noun cited with article in vocab tables. Wrong gender cascades to wrong articles, adjective endings, pronouns and relative pronouns.
2. **Four cases (Nominativ/Akkusativ/Dativ/Genitiv)** — drives article + adjective + pronoun forms. Two-way prepositions (an/auf/in/hinter/neben/über/unter/vor/zwischen) take accusative for motion, dative for static location.
3. **Verb-second word order in main clauses** — verb at position 2 regardless of what's at position 1. Front-loading forces inversion. Common error point.
4. **Verb-final in subordinate clauses** — after weil/dass/obwohl/wenn/ob/während/als/nachdem/bevor/bis/damit/sobald/falls. Highest-frequency error in extended writing.
5. **Modal + infinitive at clause end** — modal at position 2, infinitive at end (Ich muss meine Hausaufgaben machen). Same shape for werden + infinitive (future) and haben/sein + past participle (perfect).
6. **Perfect tense haben vs sein** — sein for movement (gehen, fahren, fliegen, laufen, schwimmen, kommen, reisen) and state-change verbs (werden, bleiben, sein, sterben); haben for everything else.
7. **Separable verbs** — prefix to end in main clauses (Ich stehe auf), whole at end in subordinate (weil ich aufstehe), ge- between prefix and stem in past participle (aufgestanden). Inseparable prefixes (be-, ent-, er-, ge-, ver-, zer-) and -ieren verbs take NO ge- in past participle.
8. **Strong vs weak verbs** — weak follow ge- + stem + -t; strong follow ge- + stem (with vowel change) + -en. Past participles must be memorised.
9. **Konjunktiv II** — würde + infinitive (workhorse), hätte, wäre, könnte, sollte, möchte (Foundation-friendly polite request). Higher-tier writing on social issues / wellbeing leans on man sollte and es wäre.
10. **Umlauts (ä/ö/ü) and ß (eszett)** — write the real characters; ß after long vowels and diphthongs (Fuß, Straße, weiß, heißen); ss after short vowels (dass, essen, muss). Issue 2 (May 2025) confirms sp- + st- as both /ʃ/-initial clusters.
11. **Noun capitalisation** — EVERY noun is capitalised, regardless of role. Lower-case nouns lose marks. Includes nominalised adjectives (das Gute, etwas Schönes) and infinitives used as nouns (das Schwimmen, beim Essen).
12. **Adjective endings (three declensions)** — weak (after der), mixed (after ein/kein/possessive), strong (no article). Predicative adjectives after sein/werden/bleiben take NO ending. Recurring error point.
13. **Du vs Sie register** — Sie is default for all 9 prescribed role-play settings (formal commercial contexts). German is more formal in shop/hotel/doctor settings than French (vous) or Spanish (usted).
14. **kein vs nicht** — kein for noun-phrase negation with indefinite article or no article (kein Geld, keine Zeit, keine Bücher); nicht for verb / adjective / adverb / definite-noun-phrase negation.
15. **haben + noun idioms** — Ich habe Hunger / Durst / Angst / Recht. Ich bin 15 Jahre alt (NOT 'Ich habe 15 Jahre' — French interference).
16. **Reflexive verbs — accusative vs dative pronouns** — sich + accusative (mich/dich/sich) for direct reflexive (Ich wasche mich); sich + dative (mir/dir/sich) when there's a separate direct object (Ich wasche mir die Hände).
17. **Compound nouns** — productive in German (die Umweltverschmutzung, der Klimawandel, das Wohlbefinden, die Sehenswürdigkeit). Compound gender = gender of last element.
18. **SSC drill points** — ä/ö/ü, ie /iː/ vs ei /aɪ/ (opposite of English), ch hard /x/ vs soft /ç/, sch /ʃ/, sp-/st- /ʃp//ʃt/ (Issue 2), final-consonant devoicing -b/-d/-g, -ig /ɪç/, vocalic -er, eu/äu /ɔɪ/, v usually /f/, w /v/, z /ts/.
19. **Country prepositions** — nach + most countries (nach Deutschland, nach Spanien); but in + die Schweiz / in die Türkei / in die USA (countries with article).
20. **Telling time** — halb drei = 2:30 (NOT 3:30 — German 'halfway TO three'). Drill explicitly.

## Three "fresh" lessons (no AQA source)

| Theme | Lesson | Tier | Notes |
|---|---|---|---|
| T1 L04 Equality and Inclusion | higher | Build from Edexcel Higher-tier social-issues lexis (Gleichberechtigung, Ungleichheit, Diskriminierung, Rassismus, Sexismus, Vielfalt). Drill subordinate-clause word order with weil/obwohl/dass + verb-final in opinion-stacking arguments. Drill Konjunktiv II for advisory framing (man sollte, es wäre wichtig). |
| T2 L04 Mental Wellbeing | higher | Build from Edexcel emotion/wellbeing vocab (Wohlbefinden, Stress, Gleichgewicht, Lebensqualität). Drill reflexive sich fühlen + adjective (Ich fühle mich gestresst) and Konjunktiv II for hypothetical advice (man sollte mehr schlafen, es wäre besser). Lean into compound-noun formation. |
| T5 L03 Jobs and Work Experience | both | German AQA has NO dedicated jobs lesson (mirrors Spanish AQA gap). Build from Edexcel Appendix 1 vocab (Beruf, Arbeit, Praktikum, Bewerbung). Drill ser-equivalent rule in German: 'Ich bin Lehrer' (NO article after sein with profession). Drill -in feminine suffix (Lehrer/Lehrerin, Arzt/Ärztin, Koch/Köchin with umlaut). |

## Unmatched / gaps

None. All 21 high/medium plan lessons resolved to source files. All 27 target lesson IDs resolved in Supabase.

## Verification

- Spec slice path matches `_AGENT_PROMPT.md` and the batch JSON `spec_slice_path` field.
- Reference lesson path matches batch JSON `reference_lesson_path` field.
- Agent prompt path matches batch JSON `agent_prompt_path` field.
- `output_dir` = `scripts/_content_german-edexcel/lessons` (the empty dir created above).
- `subject_id` in every batch matches Supabase: `201bf775-6897-4bfe-a537-befc5da89ab0`.
- `_spec_german-edexcel.txt` is auto-gitignored via `.gitignore:25` (`scripts/_content_*/_spec_*.txt`).
- `_source/` is auto-gitignored via `.gitignore:26` (`scripts/_content_*/_source/`).

## Touched files

All work confined to `scripts/_content_german-edexcel/`. No files outside this directory were created or modified.

## Next step

Phase 3 content generation: dispatch each `_batch_t{1-6}_*.json` to a Sonnet 4.6 content agent with `_AGENT_PROMPT.md` as the system prompt. Agents write to `lessons/{slug}.json`. Validate via `scripts/_validate_content_json.py` before insertion.
