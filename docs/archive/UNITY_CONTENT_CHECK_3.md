# Unity College Content Accuracy Check 3

**Date:** 5 April 2026
**Subjects checked:** Religious Studies (AQA 8062), Music (Eduqas C660U), French (AQA 8652), Spanish (AQA 8692)
**Method:** Compared lesson titles and content_html against exam specification markdown files. Fetched L1, middle, and selected lessons per subject from Supabase.

---

## 1. Religious Studies (AQA 8062) -- 40 lessons, 8 units

### Spec Overview
AQA 8062 has two components:
- **Component 1** (50%): Study of two religions (beliefs, teachings and practices)
- **Component 2** (50%): Four thematic studies from Themes A-H

The spec offers 7 religions (Buddhism, Christianity, Catholic Christianity, Hinduism, Islam, Judaism, Sikhism) and 8 themes (A-F ethical, G-H textual studies on St Mark's Gospel).

### Unit Coverage

| Unit | Lessons | Spec Section |
|------|---------|-------------|
| Christianity: Beliefs & Teachings | 5 | 3.1.2.1 |
| Christianity: Practices | 5 | 3.1.2.2 |
| Islam: Beliefs & Teachings | 5 | 3.1.5.1 |
| Islam: Practices | 5 | 3.1.5.2 |
| Theme A: Relationships & Families | 5 | 3.2.1.1 |
| Theme B: Religion & Life | 5 | 3.2.1.2 |
| Theme D: Religion, Peace & Conflict | 5 | 3.2.1.4 |
| Theme E: Religion, Crime & Punishment | 5 | 3.2.1.5 |

**Religion choice: Christianity + Islam.** This is a valid combination under the spec (Christianity and Catholic Christianity is the only prohibited pair).

**Theme choice: A, B, D, E.** Students must study four themes. Themes C (Existence of God) and F (Human Rights & Social Justice) are omitted. This is a valid selection -- the spec requires exactly four from A-F. No textual studies (G/H), which is also valid (non-textual route).

### Content Spot-Check

**Christianity Beliefs L1 -- "The Nature of God & the Trinity"**
- Covers: God as omnipotent, benevolent, just; problem of evil and suffering; the Trinity (Father, Son, Holy Spirit); Nicene Creed. Scripture references include Luke 1:37, John 3:16, 2 Thessalonians 1:6, Matthew 28:19, Acts 2.
- Spec alignment: GOOD. Matches 3.1.2.1 "Key beliefs" precisely -- nature of God (omnipotent, loving, just), problem of evil, oneness of God and the Trinity.
- No factual errors found.

**Islam Practices L3 -- "Hajj"**
- Despite the title, the lesson actually covers both Zakah AND Hajj (two pillars in one lesson).
- Zakah section: covers 2.5% rate, nisab threshold, Qur'an 9:60, purification purpose, Khums in Shi'a Islam. All correct.
- Hajj section: covers fifth pillar, Ibrahim origins, Qur'an 3:97, Dhul Hijjah timing.
- Spec alignment: GOOD. Matches 3.1.5.2 "Duties and festivals" -- Zakah and Hajj sections.
- Note: The lesson title "Hajj" is misleading since it also extensively covers Zakah. Consider renaming to "Zakah and Hajj" for accuracy.

**Theme B L3 -- "Abortion & Euthanasia"**
- Covers: sanctity vs quality of life, abortion (legal context, Christian views -- Catholic/CofE/Liberal, Islamic views), euthanasia, death and afterlife.
- Scripture: Genesis 1:27, Qur'an 6:2. Legal: Abortion Act 1967 (amended 1990), 24-week limit.
- Spec alignment: GOOD. Matches 3.2.1.2 comprehensively.
- No factual errors found.

### Issues Found

**ISSUE 1 (MODERATE): Duplicate/overlapping lessons across all four thematic units**

Each thematic unit has 5 lessons, but L3 typically covers the same ground as L4 and/or L5 at a different depth level. This creates significant content overlap:

| Unit | Overlapping Lessons |
|------|-------------------|
| Christianity: Beliefs | L4 "Sin, Salvation & Atonement" vs L5 "Sin and Salvation" -- both cover sin, original sin, salvation, atonement with same headings |
| Theme A | L3 "Contraception & Same-Sex Relationships" vs L4 "Families and Contemporary Family Issues" -- L4 re-covers same-sex parents already in L3 |
| Theme B | L3 "Abortion & Euthanasia" vs L4 "Abortion and Euthanasia" -- near-identical titles, both cover abortion and euthanasia with Christian and Islamic views |
| Theme D | L3 "Weapons of Mass Destruction & Peacemaking" vs L4 "Nuclear Weapons and Weapons of Mass Destruction" AND L5 "Peacemaking and Responses to Victims of War" -- L3 covers topics that L4+L5 then expand on |
| Theme E | L3 "Forgiveness & Corporal Punishment" vs L4 "Forgiveness" AND L5 "The Death Penalty" -- same pattern |

It appears that lessons L1-L3 were generated as a "condensed overview" set, and L4-L5 were then added as deeper dives into the same material. A student working through all five lessons in a unit would encounter heavy repetition.

**Recommendation:** Review whether L3 in each thematic unit should be restructured to cover different spec content rather than duplicating L4/L5. Alternatively, if the intent is a "summary then deep dive" approach, make the titles clearer (e.g., "Abortion & Euthanasia: Overview" vs "Abortion & Euthanasia: Religious Perspectives").

**ISSUE 2 (MINOR): Islam Practices L3 title mismatch**

The lesson is titled "Hajj" but the first ~40% of the content is about Zakah. This could confuse students navigating by title. Suggest renaming to "Zakah and Hajj".

**ISSUE 3 (NONE): No missing spec areas**

All required spec areas for the chosen religions (Christianity + Islam) and themes (A, B, D, E) are covered. The omission of Themes C and F is a valid selection, not a gap.

---

## 2. Music (Eduqas C660U) -- 26 lessons, 6 units

### Spec Overview
Eduqas GCSE Music has three components:
- **Component 1** (30%): Performing (NEA)
- **Component 2** (30%): Composing (NEA)
- **Component 3** (40%): Appraising exam across 4 Areas of Study

The revision content focuses on Component 3 (the written/listening exam). Two set works: Bach Badinerie (AoS1) and Toto "Africa" (AoS4).

### Unit Coverage

| Unit | Lessons | Spec Section |
|------|---------|-------------|
| Musical Elements and Listening Skills | 5 | General musical elements |
| AoS1: Musical Forms and Devices | 4 | AoS1 (1650-1910 WCT) |
| AoS2: Music for Ensemble | 4 | AoS2 |
| AoS3: Film Music | 5 | AoS3 |
| AoS4: Popular Music | 5 | AoS4 |
| Set Work: Toto - Africa | 3 | AoS4 set work |

### Content Spot-Check

**AoS1 L1 -- "Binary and Ternary Form"**
- Covers: binary form (AB), ternary form (ABA), contrast, key changes, repeat marks, examples from Baroque/Classical/Romantic.
- Spec alignment: GOOD. Directly maps to AoS1 requirements for binary and ternary forms.
- Correctly references tonic/dominant modulation, Baroque dance origins.
- Mentions Baroque, Classical, and Romantic eras as required.

**AoS3 L3 -- "Instrumentation and Articulation in Film Scores"**
- Covers: four orchestral families (strings, woodwind, brass, percussion), articulation techniques (legato, staccato, pizzicato, arco, con sordino, tremolo), film examples (Jaws, Batman, Hedwig's Theme).
- Spec alignment: GOOD. Matches AoS3 requirements for timbre, tone colour, dynamics, instrumentation.
- No factual errors found. Film examples are well-chosen and accurate.

**Set Work: Toto Africa L1 -- "Overview, Introduction and Verse 1"**
- Covers: background (1981, Toto IV, David Paich/Jeff Porcaro), instrumentation, form (verse-chorus), key ambiguity (B major/E major/A Lydian), time signature (2/2 alla breve), introduction analysis (bars 1-4, bVII-vi-ii chords), riff analysis.
- Spec alignment: EXCELLENT. Detailed bar-by-bar analysis. Mentions key ambiguity correctly noted in official Eduqas materials.
- Release date "30th September 1982" is correct for the single. Album recorded 1981, single released 1982. Accurate.

**AoS1 L4 -- "Bach: Badinerie Set Work Study"**
- Covers: form/structure, melody motifs X and Y, harmony/tonality, rhythm/metre/tempo, texture/instrumentation, Baroque features.
- Key of B minor: correct.
- Flute and string orchestra with harpsichord: correct.
- Binary form analysis: correct.
- MISSING: The catalogue number BWV 1067 is not mentioned anywhere. While not essential for the exam, it's standard reference for this piece.

### Issues Found

**ISSUE 1 (MODERATE): Missing spec terms -- strophic form, minuet and trio, sonata**

The Eduqas spec explicitly lists the following forms that AoS1 must cover: "binary, ternary, minuet and trio, rondo, variation and strophic forms." The term **strophic** does not appear anywhere across all 26 lessons. **Minuet and trio** as a compound form is also absent (minuet is mentioned individually in L1 as a Baroque dance, but the specific "minuet and trio" form structure is never explained). **Sonata** form is listed in the AoS2 ensemble groupings section ("sonatas") and is absent from the content.

- **strophic** -- NOT FOUND in any lesson. This is a gap. Students need to know this form for the exam.
- **minuet and trio** -- NOT FOUND as a form. Minuet is mentioned as a Baroque dance type but the specific minuet-and-trio structure (M|T|M) is not explained.
- **sonata** -- NOT FOUND. The spec lists "sonatas" as an ensemble grouping in AoS2.

**ISSUE 2 (MODERATE): AoS1 Musical Devices lesson is incomplete**

AoS1 L3 "Musical Devices" only covers 7 of the ~20 devices listed in the spec. The lesson has dedicated sections for: sequence, ostinato, imitation, pedal, drone, canon, and cadences. The following spec-listed devices are NOT covered in this lesson:

- repetition (mentioned briefly elsewhere but not taught as a device)
- contrast
- anacrusis (covered in Musical Elements L2 and Toto L1 instead)
- syncopation (listed in L3's title/tags but not given a section)
- dotted rhythms
- conjunct movement (covered in other lessons but not in the devices lesson)
- disjunct movement (covered in other lessons but not in the devices lesson)
- ornamentation (covered in AoS1 L1 and L2)
- broken chord/arpeggio (covered in AoS1 L2 and L4)
- Alberti bass (covered in AoS1 L2)
- regular phrasing
- modulation to dominant and relative minor

Many of these terms DO appear in other lessons across the subject. The issue is that L3 "Musical Devices" doesn't serve as the comprehensive reference it should be for the AoS1 device list. Students studying this lesson alone would miss over half the required devices.

**Recommendation:** Either expand AoS1 L3 to cover all listed devices (even briefly), or add a second devices lesson. Alternatively, add a cross-reference note directing students to where the remaining devices are covered.

**ISSUE 3 (MINOR): BWV 1067 catalogue reference missing from Badinerie lesson**

The Badinerie set work lesson correctly identifies it as the final movement of Orchestral Suite No. 2 in B minor but omits the standard catalogue number BWV 1067. This is a minor gap -- the Eduqas spec cites it explicitly.

**ISSUE 4 (MINOR): No dedicated chamber music content in AoS2**

The spec lists three ensemble genres for AoS2: "jazz and blues, musical theatre and chamber music." AoS2 has dedicated lessons for Jazz & Blues (L3) and Musical Theatre (L4), but no dedicated chamber music lesson. While basso continuo and string quartet are mentioned in passing in AoS2 L1, the chamber music tradition is not explored in depth. Basso continuo is covered in AoS1 L2 and L4 (Badinerie), not in AoS2 where the spec places it.

---

## 3. French (AQA 8652) -- 26 lessons, 3 units

### Spec Overview
AQA GCSE French (new spec, first exams 2026) has three themes:
- **Theme 1:** People and lifestyle (Identity/relationships, Healthy living, Education/work)
- **Theme 2:** Popular culture (Free-time, Customs/festivals, Celebrity culture)
- **Theme 3:** Communication and the world around us (Travel/tourism, Media/technology, Environment/where people live)

Four papers: Listening (25%), Speaking (25%), Reading (25%), Writing (25%). Foundation and Higher tiers.

### Unit Coverage

| Unit | Lessons | Spec Theme |
|------|---------|-----------|
| People and Lifestyle | 10 | Theme 1 |
| Popular Culture | 8 | Theme 2 |
| Communication and the World Around Us | 8 | Theme 3 |

### Content Spot-Check

**People and Lifestyle L1 -- "Family Members and Descriptions"**
- Covers: family member vocabulary (pere, mere, frere, soeur, etc.), possessive adjectives (mon/ma/mes, ton/ta/tes, son/sa/ses), adjective agreement rules, physical appearance (avoir for hair/eyes, etre for height/build), personality adjectives.
- Spec alignment: GOOD. Directly maps to Theme 1 Topic 1 "Identity and relationships with others."
- Grammar is accurate: possessive adjective agreement with noun (not possessor) is correctly explained. The vowel exception (mon amie, not ma amie) is correctly noted.
- French vocabulary is accurate -- checked several terms against spec vocabulary list.

**Communication L5 -- "Technology and Social Media"**
- Covers: technology devices vocabulary (portable, ordinateur, tablette, reseaux sociaux), online activities, advantages/disadvantages structure (d'un cote... de l'autre cote), opinion phrases.
- Spec alignment: GOOD. Maps to Theme 3 Topic 2 "Media and technology."
- Correctly notes that "portable" can mean phone or laptop depending on context.
- Multi-tense approach is appropriately signposted for exam technique.

### Topic Coverage Mapping

| Spec Topic | Covered By |
|-----------|-----------|
| T1.1 Identity and relationships | L1 Family, L2 Friendships, L3 Relationships/Marriage |
| T1.2 Healthy living and lifestyle | L4 Healthy Living, L5 Food/Drink, L6 Illness, L7 Sport |
| T1.3 Education and work | L8 School Subjects, L9 School Life, L10 Jobs/Work/Future |
| T2.1 Free-time activities | L1 Free-Time, L2 Music/Film/TV, L3 Sport |
| T2.2 Customs, festivals and celebrations | L4 French Festivals, L5 Customs |
| T2.3 Celebrity culture | L6 Celebrity Culture |
| T3.1 Travel and tourism | L1 Holidays, L2 Past Holidays, L3 Accommodation, L4 Weather/Transport |
| T3.2 Media and technology | L5 Technology, L7 Social Media (also covered in PopCulture L7) |
| T3.3 Environment and where people live | L6 House/Home, L7 Town/Local Area, L8 Environment/Global Issues |

### Issues Found

**ISSUE 1 (MINOR): "Eating Out" lesson in Popular Culture unit is a borderline fit**

French Popular Culture L8 "Eating Out and Restaurant Conversations" does not map cleanly to any of Theme 2's three topics (Free-time activities, Customs/festivals, Celebrity culture). Eating out could be argued as a "free-time activity" but it's more commonly associated with Theme 1 (Healthy living/lifestyle -- food and drink) or Theme 3 (Travel/tourism). The content itself is fine and vocabulary is spec-aligned; it's just a unit placement question.

Similarly, Spanish Popular Culture L4 has the same "Eating Out" placement.

**ISSUE 2 (MINOR): Social media appears in two units**

"Social Media and Online Life" appears as both Popular Culture L7 AND Communication L5 "Technology and Social Media." This creates some overlap. However, since language subjects benefit from revisiting vocabulary in different contexts, this is less problematic than it would be in a knowledge-based subject.

**ISSUE 3 (NONE): Overall coverage is comprehensive**

All nine spec topics (3 per theme) are covered. No major spec areas are missing. Grammar instruction (possessive adjectives, tenses, structures) is woven into content lessons appropriately. Both Foundation and Higher tier vocabulary appears to be included.

---

## 4. Spanish (AQA 8692) -- 26 lessons, 3 units

### Spec Overview
AQA GCSE Spanish (new spec, first exams 2026) has an identical structure to French:
- **Theme 1:** People and lifestyle (Identity/relationships, Healthy living, Education/work)
- **Theme 2:** Popular culture (Free-time, Customs/festivals, Celebrity culture)
- **Theme 3:** Communication and the world around us (Travel/tourism, Media/technology, Environment/where people live)

### Unit Coverage

| Unit | Lessons | Spec Theme |
|------|---------|-----------|
| People and Lifestyle | 10 | Theme 1 |
| Popular Culture | 8 | Theme 2 |
| Communication and the World Around Us | 8 | Theme 3 |

### Content Spot-Check

**People and Lifestyle L1 -- "Family and Describing People"**
- Covers: family vocabulary (madre, padre, hermano/a, abuelo/a, etc.), mayor/menor for age comparisons, physical appearance with ser and tener, personality adjectives, gender agreement.
- Spec alignment: GOOD. Maps to Theme 1 Topic 1.
- Vocabulary is accurate. Grammar explanation of ser vs tener for descriptions is correct.
- Key vocabulary items checked against spec vocabulary list: all confirmed present.

**Communication L5 -- "Technology and Social Media"**
- Covers: technology vocab (movil, ordenador, portatil, redes sociales), online activities, frequency phrases, advantages/disadvantages, multi-tense usage.
- Spec alignment: GOOD. Maps to Theme 3 Topic 2.
- Correct emphasis on multiple tenses (present, preterite, imperfect, future).

### Topic Coverage Mapping

| Spec Topic | Covered By |
|-----------|-----------|
| T1.1 Identity and relationships | L1 Family, L2 Friendships, L3 Marriage |
| T1.2 Healthy living and lifestyle | L4 Healthy Living, L5 Food/Drink, L6 Illness, L7 Drugs/Smoking/Alcohol |
| T1.3 Education and work | L8 School Subjects, L9 Teachers/School Day, L10 School Rules/Future Plans |
| T2.1 Free-time activities | L1 Free-Time, L2 Music/Film/TV, L3 Sport |
| T2.2 Customs, festivals and celebrations | L5 Spanish Festivals, L6 Customs |
| T2.3 Celebrity culture | L7 Celebrity Culture |
| T3.1 Travel and tourism | L1 Holidays, L2 Accommodation, L3 Transport, L4 Weather |
| T3.2 Media and technology | L5 Technology, L8 Social Media (also in PopCulture L8) |
| T3.3 Environment and where people live | L6 House/Home, L7 Town/Local Area, L8 Environment |

### Issues Found

**ISSUE 1 (MODERATE): Jobs and work experience is underserved**

Theme 1 Topic 3 is "Education and work." French dedicates a full lesson (L10) to "Jobs, Work Experience and Future Plans." Spanish covers school rules and homework in L10, with future plans and jobs mentioned only briefly at the end (two short headings: "The Future Tense" and "Future Plans"). The lesson title "School Rules, Homework and Future Plans" suggests jobs/careers are an afterthought.

Key work vocabulary like job titles, work experience language, and career ambitions deserve more dedicated coverage. The AQA spec vocabulary list includes trabajo, profesion, empleo, carrera, experiencia laboral -- students need practice with these in context.

**Recommendation:** Consider splitting L10 into a dedicated "School Rules and Homework" lesson and a separate "Jobs, Work Experience and Future Plans" lesson, or rebalancing the existing lesson to give equal weight to both areas.

**ISSUE 2 (MINOR): "Eating Out" placement in Popular Culture (same as French)**

Spanish Popular Culture L4 "Eating Out and Restaurant Conversations" has the same borderline unit fit noted for French. Not a content error, but a structural alignment question.

**ISSUE 3 (MINOR): Social media duplication (same as French)**

"Social Media and Online Life" (PopCulture L8) overlaps with Communication L5 "Technology and Social Media." Same note as French -- minor, acceptable for language subjects.

**ISSUE 4 (MINOR): Spanish L7 "Drugs, Smoking and Alcohol" -- spec-valid but niche**

This topic gets a dedicated lesson in Spanish but not in French (where healthy living is covered more broadly). Both are valid -- the vocabulary (drogas, fumar, alcohol) is in the spec vocabulary list -- but allocating a full lesson to this while jobs/careers gets a partial lesson (see Issue 1) seems like a priority mismatch.

---

## Summary of Findings

| Subject | Lessons | Verdict | Critical Issues | Moderate Issues | Minor Issues |
|---------|---------|---------|----------------|----------------|-------------|
| Religious Studies | 40 | GOOD with caveats | 0 | 1 (duplicate lessons) | 1 (title mismatch) |
| Music | 26 | GOOD with gaps | 0 | 2 (missing forms, incomplete devices) | 2 (BWV ref, chamber music) |
| French | 26 | GOOD | 0 | 0 | 2 (eating out placement, social media overlap) |
| Spanish | 26 | GOOD with one gap | 0 | 1 (jobs underserved) | 3 (eating out, social media, lesson weighting) |

### No factual errors were found in any checked lesson content.

All four subjects correctly reference their exam board and specification. Vocabulary, scripture references, musical analysis, and subject-specific terminology were spot-checked and found to be accurate. The issues identified are structural (overlapping content, missing spec terms, lesson weighting) rather than factual inaccuracy.

### Priority actions:
1. **Music:** Add strophic form, minuet and trio form, and sonata to the content (could be added to existing lessons or a new lesson).
2. **Music:** Expand AoS1 L3 "Musical Devices" to cover all 20 spec-listed devices, or add cross-references.
3. **RE:** Restructure or retitle the duplicate lessons in thematic units to reduce repetition.
4. **Spanish:** Rebalance People L10 to give jobs/work experience equal weight, or add a dedicated lesson.
