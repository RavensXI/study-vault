# Fact-Check Report: Psychology AQA (8182)
**Date:** 2026-05-28
**Lessons checked:** 32 (all units: memory, perception, development, research-methods, social-influence, language-thought-communication, brain-neuropsychology, psychological-problems)

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 3     |
| MEDIUM   | 6     |
| LOW      | 5     |
| **TOTAL**| **14**|

---

## HIGH Severity (fix before ship)

### 1. Müller-Lyer illusion — Gregory's explanation has fin/corner associations inverted
**Lesson:** Perception L03 — Visual Illusions and Gregory's Constructivist Theory (`4f4d2702`)

**Problematic text:**
> "The arrow fins resemble the inside corner of a room (inward, appearing further away) or the outside corner of a building (outward, appearing closer)."

**What's wrong:** The parenthetical explanation is reversed. Inward-pointing fins (`>---<`) resemble the **outside corner of a building** (protruding toward you = closer), NOT the inside corner of a room. Outward-pointing fins (`<---->`) resemble the **inside corner of a room** (receding = further away). The stated result is correct (inward-fin line looks shorter) but the Gregory explanation is inverted. An exam answer using this explanation would lose marks.

**Correct version:** Outward fins (`<---->`) = inside corner of a room → appears further away → size constancy makes it look LONGER. Inward fins (`>---<`) = outside corner of a building → appears closer → size constancy makes it look SHORTER.

**Suggested fix:** "Gregory's explanation: the inward fins (`>---<`) resemble the outside corner of a building (appearing closer); size constancy makes the brain judge the line as shorter. The outward fins (`<---->`) resemble the inside corner of a room (appearing further away); size constancy makes the brain judge that line as longer."

---

### 2. Milgram study entirely missing — no procedure, no 65%, no 450V
**Lesson:** Social Influence L02 — Obedience: Milgram and the Authoritarian Personality (`2a61473b`)

**Problematic text:** The lesson covers Milgram's Agency Theory and social/dispositional factors affecting obedience but contains no description of Milgram's actual study, no mention of the 65% obedience rate, and no reference to the 450V shock generator.

**What's wrong:** The AQA 8182 spec requires students to know Milgram's study as a named study (aim, procedure, findings, conclusion). Every AQA mark scheme for Milgram awards specific marks for: the shock range (15V–450V in 30 increments), the four verbal prods, and the headline finding that **65% of participants administered the maximum 450V**. Without this content, students cannot answer any question asking them to "describe Milgram's study."

**Suggested fix:** Add a Key Fact box with Milgram's study: Aim — to investigate whether ordinary people would obey an authority figure instructed to harm an innocent person. Method — 40 male American participants told to administer electric shocks (15V–450V, in 30 increments of 15V) to a confederate 'learner' for wrong answers; four verbal prods used when participants hesitated ('Please continue' → 'You have no other choice'). Results — **65% of participants administered the full 450V; all participants gave at least 300V**. Conclusion — people obey authority figures even when ordered to cause serious harm, supporting the agentic state explanation.

---

### 3. Peterson & Peterson (1959) missing — named study for STM duration
**Lesson:** Memory L02 — The Multi-Store Model of Memory (`ab626ef1`)

**Problematic text:** The lesson states STM lasts "around 15 to 30 seconds without rehearsal" as an established fact with no study attributed to this figure.

**What's wrong:** The AQA 8182 spec lists Peterson & Peterson (1959) as a named study. Mark schemes award marks for knowing: trigram-plus-counting-task method, retention intervals of 3–18 seconds, recall falling to ~5% at 18 seconds. The figure "15–30 seconds" is floating with no attribution, which means students cannot describe this as a study. Also, the standard AQA figure is 18 seconds (the point at which recall collapsed to ~5%), not 30 seconds — "up to 30 seconds" is a commonly stated upper bound but the key data point is 18s.

**Suggested fix:** Add a named study section for Peterson & Peterson (1959): Aim — to investigate the duration of STM without rehearsal. Method — participants given a consonant trigram (e.g. CHJ), immediately made to count backwards in threes to prevent rehearsal, then tested after 3, 6, 9, 12, 15 or 18 seconds. Results — recall fell sharply; after 18 seconds recall was approximately 5%. Conclusion — STM duration is around 18–30 seconds without rehearsal.

---

## MEDIUM Severity (should fix — may affect exam answers)

### 4. Beck's Cognitive Triad not named — only general negative schemas described
**Lesson:** Psychological Problems L02 — Clinical Depression (`fbf12185`)

Beck's Cognitive Triad (negative views of self, world, future) is not mentioned by name. The lesson instead describes "negative schemas and attributions" with an internal/stable/global attribution style — the latter is Abramson et al.'s learned helplessness model, not Beck's model. AQA mark schemes award marks for naming and describing the triad. Students may also confuse the two models in exam answers.

**Fix:** Name Beck's Cognitive Triad explicitly: negative view of self ("I am worthless"), world ("things always go wrong"), future ("things will never improve"). Keep attribution content but either attribute it to Abramson or frame it as a separate account.

---

### 5. Gilchrist & Nesberg method described as matching task when it was overestimation
**Lesson:** Perception L04 — Factors Affecting Perception (`5339426d`)

The lesson says participants adjusted brightness "to match what they had seen." The actual result is overestimation: deprived participants set the brightness *higher* than the original stimulus, not merely matched it. The results section correctly says "adjusted...to appear brighter than less deprived participants did," but the method framing as a matching task is misleading. For exam evaluation questions on validity, it matters whether this was a matching or overestimation paradigm.

**Fix:** Revise method: "participants adjusted the brightness of the darkened image to reproduce the original; deprived participants systematically overestimated the original brightness."

---

### 6. Piliavin drunk vs ill conditions — smell of alcohol detail missing
**Lesson:** Social Influence L03 — Bystander Behaviour and Piliavin's Study (`8263fc26`)

The drunk confederate carried "a bottle in a bag" but the lesson omits that he also smelled of alcohol — the smell was an integral part of the experimental manipulation distinguishing the two conditions. Specific help rates (ill: ~95%; drunk: ~50%) are also absent. AQA mark schemes credit these statistics.

**Fix:** Add "smelled of alcohol" to drunk condition. Add help rate statistics: ill victim helped ~95% of trials; drunk victim ~50% of trials. Ill victim helped within 70 seconds in 90%+ of trials.

---

### 7. Whorf/Hopi time claim not clearly labelled as discredited
**Lesson:** Language, Thought and Communication L01 — Language and Thought (`4e05cab1`)

The lesson notes "subsequent research has challenged some of Whorf's specific claims" — which is correct but understated. Malotki (1983) showed that Hopi does have tense, directly refuting the specific Hopi-time claim. Students evaluating Sapir-Whorf are expected to say the strong version is "widely rejected" (which the lesson does state) and cite this specific research failure. The current phrasing "challenged some claims" is too soft for what is a well-documented refutation.

**Fix:** Revise to: "Whorf's specific claim that Hopi is 'timeless' has been refuted by Malotki (1983), who documented extensive tense vocabulary in Hopi — this undermines the strong version of the hypothesis specifically. The weak version (linguistic relativity) retains empirical support."

---

### 8. Von Frisch — distance threshold for round vs waggle dance missing
**Lesson:** Language, Thought and Communication L02 — Human and Animal Communication (`bf92da7d`)

The lesson correctly distinguishes round dance (close food) from waggle dance (distant food) but does not specify the ~100 metre threshold at which bees switch from round to waggle dance. AQA mark schemes sometimes credit this figure. The mechanism by which duration encodes distance could also be clearer (longer waggle run = further).

**Fix:** Add: "The round dance is used for food within approximately 50–100 metres; the waggle dance is used for food beyond that distance. Within the waggle dance, a longer waggle run indicates greater distance."

---

## LOW Severity (minor omissions or precision issues)

### 9. Asch — number of confederates not specified (7)
**Lesson:** Social Influence L01 (`e06035e9`). "Several other people" should be "seven confederates." The specific number supports evaluation of the group size variable (Asch's variation studies tested 1–15 confederates).

### 10. Asch — "critical trials" terminology absent from method description
**Lesson:** Social Influence L01 (`e06035e9`). "12 out of 18 trials" is correct but calling them "critical trials" is AQA-standard terminology. Fix: "12 out of 18 trials (the critical trials)."

### 11. Murdock (1962) — specific list length and rate not given
**Lesson:** Memory L03 (`8b25369b`). "A set rate" should specify "one word per second" and "a list of twenty words" — these are the most commonly cited parameters in AQA resources and mark schemes.

### 12. Antidepressants described as "quick-acting" without qualification
**Lesson:** Psychological Problems L03 (`9b516a6c`). SSRIs take 2–6 weeks for full effect — not quick in absolute terms, only relative to a full CBT course. Students should know the 2–6 week timeline for exam questions about limitations of drug treatments.

### 13. Piaget stage ages — no mention that critics find them underestimates
**Lesson:** Development L02 (`6dcb5640`). Stage ages are correct (0–2, 2–7, 7–11, 11+) but the lesson doesn't flag here that critics argue abilities emerge earlier — this is covered in L03, so the overall set is balanced. Flagging the link explicitly would help students integrate the evaluation.

---

## Units not flagged with issues

The following units/lessons were checked and found factually accurate for AQA purposes:

- **Memory L01** — Processes and Types of Memory: episodic/semantic/procedural distinctions correct.
- **Memory L04** — Reconstructive Memory: Bartlett's War of the Ghosts procedure and findings correctly described.
- **Perception L01** — Sensation, Perception and Depth Cues: monocular/binocular cue terminology accurate; 6–7 cm eye separation stated correctly.
- **Perception L02** — Gibson's Direct Theory: optic array, motion parallax, bottom-up processing correctly described. S.B. (Gregory & Wallace) correctly cited.
- **Development L01** — Early Brain Development: sequence (brain stem → thalamus → cerebellum → cortex) correct.
- **Development L03** — Conservation and Egocentrism: McGarrigle & Donaldson ages (4–6) and naughty teddy procedure correct. Hughes policeman doll procedure correct.
- **Development L04** — Mindset/Willingham: Dweck's fixed/growth mindset correctly described. Willingham's criticism of learning styles (meshing hypothesis not supported) correctly attributed. AQA verbalisers/visualisers distinction correctly handled.
- **Research Methods L01–L05** — Sampling methods, experimental designs, validity/reliability, ethical guidelines, descriptive statistics: all definitions and formulas (mean, median, mode, range) correct. BPS ethical guidelines correctly listed.
- **Social Influence L04** — Crowd behaviour: deindividuation, social loafing, collective behaviour correctly described.
- **Language, Thought and Communication L03** — NVC: Yuki's emoticon study method and findings correctly described. Darwin's evolutionary theory of NVC correctly framed.
- **Brain L01** — Nervous System and Fight or Flight: CNS/PNS/ANS/somatic divisions correct. James-Lange theory (1884) correctly attributed and dated.
- **Brain L02** — Neurons and Synaptic Transmission: sensory/relay/motor sequence correct. Synaptic transmission steps (vesicles, neurotransmitters, receptor sites, reuptake) correct. Hebb (1949) correctly cited.
- **Brain L03** — Brain Structure: four lobe functions correct. Broca's area (frontal lobe, speech production) and Wernicke's area (temporal lobe, comprehension) correctly localised. Penfield's stimulation study correctly described.
- **Brain L04** — Neuropsychology: CT/PET/fMRI distinctions correct. Tulving's Gold memory study (PET, right prefrontal = episodic, left prefrontal = semantic) correctly described.
- **Psychological Problems L01** — Mental Health in Context: ICD framework correctly cited. Three factors driving rising incidence rates correctly identified.
- **Psychological Problems L03** — Therapies: SSRI mechanism (block serotonin reuptake → more serotonin in synapse) correctly described. Wiles' study framing correct.
- **Psychological Problems L04** — Addiction: ICD dependence syndrome criteria correct. Kaij's twin study correctly described (Swedish male twins, higher MZ concordance than DZ).
