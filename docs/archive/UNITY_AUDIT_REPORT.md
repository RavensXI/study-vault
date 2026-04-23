# Unity College QA Audit Report

*Generated: 2026-04-05 23:55*

*Automated checks only. Content accuracy, image relevance, narration quality, and answer correctness require human review.*

**Note:** This audit covers Unity's 18 bespoke subjects (528 lessons). Mathematics (48 lessons, practice format) and Music Technology (15 lessons) are generic subjects that Unity subscribes to — they couldn't be audited here because the schools table requires admin access. They should be checked separately.

## Key Findings

1. **All 528 bespoke lessons are `live` status** — no stragglers in `pending_review` or `draft`.
2. **76 broken URLs** — mostly Wikimedia Commons hero images (files removed/moved) plus Spanish R2 audio/image URLs. These need replacing.
3. **Languages have short flashcard sets** — French (19), German (21), and Spanish (23) lessons have only 3-4 flashcard questions instead of the expected 5. Low severity but worth topping up.
4. **Creative iMedia has 6 lessons with only 4 flashcard questions.**
5. **Design & Technology is missing 3 podcasts.**
6. **11 subjects have 0 cinematic videos** — CS, Creative iMedia, D&T, French, Geography, German, RE, Spanish have no YouTube/R2 videos. This is known (cinematic video generation is in progress).
7. **289 guide pages found across all 18 subjects** — all have both exam technique and revision technique guides.
8. **No lesson numbering issues** — all sequences are clean.

## Executive Summary

| Metric | Count |
|--------|-------|
| Total subjects | 18 |
| Total units | 63 |
| Total lessons | 528 |
| Lessons passing all checks | 454 (85%) |
| Lessons with issues | 74 (14%) |
| Status: `live` | 528 |
| Status: `pending_review` | 0 |
| Status: other | 0 |
| Total guide pages | 289 |
| Broken URLs | 76 |
| Numbering issues | 0 |

## Asset Coverage

| Asset | Present | Missing | Coverage |
|-------|---------|---------|----------|
| Content HTML | 514 | 14 | 97% |
| Hero image | 514 | 14 | 97% |
| Narration | 514 | 14 | 97% |
| Podcast | 511 | 17 | 96% |
| Video (YouTube/R2) | 286 | 242 | 54% |
| Practice questions | 514 | 14 | 97% |
| Knowledge checks | 514 | 14 | 97% |
| Flashcard questions | 514 | 14 | 97% |
| Related media | 514 | 14 | 97% |
| Exam tip | 514 | 14 | 97% |
| Conclusion | 514 | 14 | 97% |

## Subject Status Overview

| Subject | Lessons | Live | Pending | Issues | Hero | Narration | Podcast | Video | PQs | KCs | Flash |
|---------|---------|------|---------|--------|------|-----------|---------|-------|-----|-----|-------|
| Business Studies | 30 | 30 | 0 | 0 | 30/30 | 30/30 | 30/30 | 26/30 | 30/30 | 30/30 | 30/30 |
| Computer Science | 23 | 23 | 0 | 0 | 23/23 | 23/23 | 23/23 | 0/23 | 23/23 | 23/23 | 23/23 |
| Creative iMedia | 23 | 23 | 0 | 6 | 23/23 | 23/23 | 23/23 | 0/23 | 23/23 | 23/23 | 23/23 |
| Design & Technology | 20 | 20 | 0 | 3 | 20/20 | 20/20 | 17/20 | 0/20 | 20/20 | 20/20 | 20/20 |
| Drama | 12 | 12 | 0 | 0 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| English Language | 30 | 30 | 0 | 0 | 30/30 | 30/30 | 30/30 | 30/30 | 30/30 | 30/30 | 30/30 |
| English Literature | 42 | 42 | 0 | 1 | 42/42 | 42/42 | 42/42 | 42/42 | 42/42 | 42/42 | 42/42 |
| Food Preparation and Nutrition | 10 | 10 | 0 | 0 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| French | 26 | 26 | 0 | 19 | 26/26 | 26/26 | 26/26 | 0/26 | 26/26 | 26/26 | 26/26 |
| Geography | 54 | 54 | 0 | 0 | 40/54 | 40/54 | 40/54 | 0/54 | 40/54 | 40/54 | 40/54 |
| German | 26 | 26 | 0 | 21 | 26/26 | 26/26 | 26/26 | 0/26 | 26/26 | 26/26 | 26/26 |
| History | 60 | 60 | 0 | 1 | 60/60 | 60/60 | 60/60 | 60/60 | 60/60 | 60/60 | 60/60 |
| Music | 26 | 26 | 0 | 0 | 26/26 | 26/26 | 26/26 | 26/26 | 26/26 | 26/26 | 26/26 |
| Religious Studies | 40 | 40 | 0 | 0 | 40/40 | 40/40 | 40/40 | 0/40 | 40/40 | 40/40 | 40/40 |
| Science | 48 | 48 | 0 | 0 | 48/48 | 48/48 | 48/48 | 48/48 | 48/48 | 48/48 | 48/48 |
| Separate Sciences | 22 | 22 | 0 | 0 | 22/22 | 22/22 | 22/22 | 22/22 | 22/22 | 22/22 | 22/22 |
| Spanish | 26 | 26 | 0 | 23 | 26/26 | 26/26 | 26/26 | 0/26 | 26/26 | 26/26 | 26/26 |
| Sport Science | 10 | 10 | 0 | 0 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |

\* = subscribed generic subject (not bespoke)

## Broken URLs (76)

| Type | Context | URL |
|------|---------|-----|
| hero | Business Studies > Business Plans and External Influences | `https://upload.wikimedia.org/wikipedia/commons/a/ad/What_your_Business_Name_S...` |
| hero | Drama > Costume, Hair & Make-up | `https://upload.wikimedia.org/wikipedia/commons/2/25/Beaivv%C3%A1%C5%A1_S%C3%A...` |
| hero | Drama > Design & Performance Evaluation | `https://upload.wikimedia.org/wikipedia/commons/a/af/Cleveland_High_School_stu...` |
| hero | Drama > Key Moments — Diane Nash & CJ Reminder | `https://upload.wikimedia.org/wikipedia/commons/f/f1/P20220707AS-1629_%2852307...` |
| hero | Drama > Lighting & Sound Design | `https://upload.wikimedia.org/wikipedia/commons/3/3e/A_control_room_or_tech_bo...` |
| hero | Drama > Performance Skills & Semiotics | `https://upload.wikimedia.org/wikipedia/commons/6/6e/Performance_in_the_Theatr...` |
| hero | Drama > Set Design & Staging Types | `https://upload.wikimedia.org/wikipedia/commons/f/fe/Scenic_Design_by_Glenn_Da...` |
| hero | English Language > Writing a Structure Analysis Response | `https://upload.wikimedia.org/wikipedia/commons/4/46/LIFE_OF_PI_-_Ang_Lee_-_35...` |
| hero | English Literature > Banquo & Deception | `https://upload.wikimedia.org/wikipedia/commons/2/2b/Banquo.jpg` |
| hero | English Literature > Context, Allegory & Orwell's Purpose | `https://upload.wikimedia.org/wikipedia/commons/b/b8/George_Orwell_white_plaqu...` |
| hero | English Literature > Exposure & Storm on the Island | `https://upload.wikimedia.org/wikipedia/commons/3/32/Snow_at_the_front_%284687...` |
| hero | English Literature > Lady Macbeth & Gender | `https://upload.wikimedia.org/wikipedia/commons/8/81/Lady_Macbeth_Cattermole.jpg` |
| hero | English Literature > London & Checking Out Me History | `https://upload.wikimedia.org/wikipedia/commons/a/a6/1794_William_Blake_Songs_...` |
| hero | English Literature > Napoleon's Rise to Power | `https://upload.wikimedia.org/wikipedia/commons/9/93/Adelaide_champion_Berkshi...` |
| hero | English Literature > Remains & War Photographer | `https://upload.wikimedia.org/wikipedia/commons/b/b9/War_Photographer_%282001%...` |
| hero | English Literature > Stave 2: Memory & Regret | `https://upload.wikimedia.org/wikipedia/commons/9/99/Charles_Dickens-A_Christm...` |
| hero | English Literature > Structure & Form in Unseen Poetry | `https://upload.wikimedia.org/wikipedia/commons/c/c3/Poems_you_ought_to_know_%...` |
| hero | English Literature > The Battle of the Cowshed & Snowball's Leadership | `https://upload.wikimedia.org/wikipedia/commons/5/5b/Animal_Farm_strip_cartoon...` |
| hero | English Literature > The Charge of the Light Brigade & Bayonet Charge | `https://upload.wikimedia.org/wikipedia/commons/9/9c/Charge_of_the_Light_Briga...` |
| hero | English Literature > The Murder of Duncan | `https://upload.wikimedia.org/wikipedia/commons/6/65/Johann_Heinrich_F%C3%BCss...` |
| hero | English Literature > The Prelude — Power of Nature | `https://upload.wikimedia.org/wikipedia/commons/8/88/Ullswater_MMB_04.jpg` |
| hero | Food Preparation and Nutrition > Energy Needs and Nutritional Analysis | `https://upload.wikimedia.org/wikipedia/commons/e/e9/Egyptian_food_Koshary.jpg` |
| hero | Food Preparation and Nutrition > Food Spoilage, Contamination and Poisoning | `https://upload.wikimedia.org/wikipedia/commons/a/a0/Rotten_Oranges.JPG` |
| hero | Food Preparation and Nutrition > Good Food Hygiene Practices | `https://upload.wikimedia.org/wikipedia/commons/1/11/Food_prep_150410-Z-KE462-...` |
| hero | Food Preparation and Nutrition > Macronutrients: Fats and Carbohydrates | `https://upload.wikimedia.org/wikipedia/commons/c/c8/Avoiding_Trans_Fat_%28185...` |
| hero | Food Preparation and Nutrition > Macronutrients: Protein | `https://upload.wikimedia.org/wikipedia/commons/e/e8/Protein-rich_Foods.jpg` |
| hero | Food Preparation and Nutrition > Micronutrients: Minerals and Water | `https://upload.wikimedia.org/wikipedia/commons/f/f8/2006-02-13_Drop-impact.jpg` |
| hero | Food Preparation and Nutrition > Micronutrients: Vitamins | `https://upload.wikimedia.org/wikipedia/commons/c/ce/Salad_greens_and_vegetabl...` |
| hero | Food Preparation and Nutrition > The Eatwell Guide and Balanced Diets | `https://upload.wikimedia.org/wikipedia/commons/2/23/Regularly_take_balanced_d...` |
| hero | German > Celebrity Culture and Role Models | `https://upload.wikimedia.org/wikipedia/commons/d/d7/Clarissa_und_Michael_K%C3...` |
| hero | Music > Africa: Chorus 3, Outro and Exam Practice | `https://upload.wikimedia.org/wikipedia/commons/0/05/Landscape%2C_Vioolsdrift%...` |
| hero | Music > Africa: Chorus, Links, Verse 2 and Instrumental | `https://upload.wikimedia.org/wikipedia/commons/3/3d/Distant_Rains_..._%285089...` |
| hero | Music > Africa: Overview, Introduction and Verse 1 | `https://upload.wikimedia.org/wikipedia/commons/6/66/Hornbill_Zazu_Chitwa_Sout...` |
| hero | Music > Binary and Ternary Form | `https://upload.wikimedia.org/wikipedia/commons/f/f5/Nocturne_et_Scherzo_de_De...` |
| hero | Music > Minimalism in Film Music | `https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/gcse-music/film-music/les...` |
| hero | Religious Studies > Abortion and Euthanasia | `https://upload.wikimedia.org/wikipedia/commons/2/25/Pro-Choice_Rally_and_Pres...` |
| hero | Religious Studies > Akhirah: Life After Death | `https://upload.wikimedia.org/wikipedia/commons/d/d9/Various_types%2C_etc._Moh...` |
| hero | Religious Studies > Contraception & Same-Sex Relationships | `https://upload.wikimedia.org/wikipedia/commons/4/46/Royal_Wedding_Stockholm_2...` |
| hero | Religious Studies > Creation, the Afterlife & Judgement | `https://upload.wikimedia.org/wikipedia/commons/3/35/Cole_Thomas_Expulsion_fro...` |
| hero | Religious Studies > Families and Contemporary Family Issues | `https://upload.wikimedia.org/wikipedia/commons/6/66/FamiliaOjeda.JPG` |
| hero | Religious Studies > Families, Gender Roles & Equality | `https://upload.wikimedia.org/wikipedia/commons/b/b2/Condoms_-_Teen_Facts.jpg` |
| hero | Religious Studies > Festivals and Commemorations | `https://upload.wikimedia.org/wikipedia/commons/a/a4/Eid_Prayer_Congregation.jpg` |
| hero | Religious Studies > Forgiveness & Corporal Punishment | `https://upload.wikimedia.org/wikipedia/commons/f/f3/Areszt_%C5%9Bledczy_w_Zab...` |
| hero | Religious Studies > Gender Equality, Prejudice and Discrimination | `https://upload.wikimedia.org/wikipedia/commons/0/0e/Suffragette_Parade%2C_23_...` |
| hero | Religious Studies > Good, Evil & Reasons for Crime | `https://upload.wikimedia.org/wikipedia/commons/3/30/The_Good_and_Evil_Angels_...` |
| hero | Religious Studies > Hajj | `https://upload.wikimedia.org/wikipedia/commons/1/17/Supplicating_Pilgrim_at_M...` |
| hero | Religious Studies > Key Beliefs: Sunni and Shi'a Islam | `https://upload.wikimedia.org/wikipedia/commons/9/90/Kabood_%28Blue%29_mosque%...` |
| hero | Religious Studies > Mission, Evangelism and World Poverty | `https://upload.wikimedia.org/wikipedia/commons/c/c0/St._Peter_preaching_the_g...` |
| hero | Religious Studies > Origins of the Universe & Human Life | `https://upload.wikimedia.org/wikipedia/commons/8/89/Approaching_the_Universe%...` |
| hero | Religious Studies > Pilgrimage and Celebrations | `https://upload.wikimedia.org/wikipedia/commons/d/d3/Lourdes_15_aout_2009.JPG` |
| hero | Religious Studies > Punishment: Aims, Types & the Death Penalty | `https://upload.wikimedia.org/wikipedia/commons/6/6f/Capone%E2%80%99s_criminal...` |
| hero | Religious Studies > Relationships, Marriage & Divorce | `https://upload.wikimedia.org/wikipedia/commons/a/a6/Gay_act_up_nyc_manhattan....` |
| hero | Religious Studies > Sin and Salvation | `https://upload.wikimedia.org/wikipedia/commons/4/41/Pietro_Antonio_Novelli_Sa...` |
| hero | Religious Studies > Sin, Salvation & Atonement | `https://upload.wikimedia.org/wikipedia/commons/1/1f/St_Thomas%27s_church%2C_S...` |
| hero | Religious Studies > The Church in the Local Community | `https://upload.wikimedia.org/wikipedia/commons/7/7d/%281%29Mission_Australia_...` |
| hero | Religious Studies > The Death Penalty | `https://upload.wikimedia.org/wikipedia/commons/2/2f/SQ_Lethal_Injection_Room....` |
| hero | Religious Studies > The Environment & Animal Rights | `https://upload.wikimedia.org/wikipedia/commons/3/36/Hopetoun_falls.jpg` |
| hero | Religious Studies > The Nature of God & the Trinity | `https://upload.wikimedia.org/wikipedia/commons/e/ea/Stained-glass_Antwerp_4.jpg` |
| hero | Religious Studies > The Sacraments: Baptism and Holy Communion | `https://upload.wikimedia.org/wikipedia/commons/8/87/Lutheran_baptism.jpg` |
| hero | Religious Studies > Weapons of Mass Destruction & Peacemaking | `https://upload.wikimedia.org/wikipedia/commons/6/6c/Anti_Racism_London_2016_p...` |
| hero | Religious Studies > Worship and Prayer | `https://upload.wikimedia.org/wikipedia/commons/2/24/Worship_at_The_Prayer_Roo...` |
| hero | Religious Studies > Zakah and Sawm | `https://upload.wikimedia.org/wikipedia/commons/d/dc/Fasting.JPG` |
| hero | Science > Forces, Gravity and Resultant Forces | `https://upload.wikimedia.org/wikipedia/commons/0/08/Physicist_Stephen_Hawking...` |
| hero | Science > Internal Energy, Specific Heat Capacity and Latent Heat | `https://upload.wikimedia.org/wikipedia/commons/3/3c/Bouncing_ball_strobe_edit...` |
| hero | Science > Rates of Reaction and Collision Theory | `https://upload.wikimedia.org/wikipedia/commons/b/b9/Thermostat_for_measuring_...` |
| hero | Science > Waves: Properties and Behaviour | `https://upload.wikimedia.org/wikipedia/commons/3/3d/Obstacle-ripple-tank.jpg` |
| hero | Science > Work Done, Elasticity and Hooke's Law | `https://upload.wikimedia.org/wikipedia/commons/a/ad/Hookes_law_nanoscale.jpg` |
| hero | Separate Sciences > Electromagnetic Induction and Transformers | `https://upload.wikimedia.org/wikipedia/commons/f/f4/Philips_N4422_-_power_sup...` |
| hero | Separate Sciences > Space Physics: The Solar System and Beyond | `https://upload.wikimedia.org/wikipedia/commons/7/7e/Tarantula_Nebula_by_JWST....` |
| hero | Separate Sciences > Transition Metals and Nanoparticles | `https://upload.wikimedia.org/wikipedia/commons/2/26/First_row_of_transition_m...` |
| hero | Separate Sciences > Yield, Atom Economy, Molar Concentrations and Gas Volumes | `https://upload.wikimedia.org/wikipedia/commons/d/db/Measurement_of_gas_volume...` |
| hero | Spanish > Customs and Traditions | `https://upload.wikimedia.org/wikipedia/commons/5/58/The_Siesta_MET_DT1952.jpg` |
| hero | Spanish > Eating Out and Restaurant Conversations | `https://upload.wikimedia.org/wikipedia/commons/4/45/Restaurante_Casa_Sira%2C_...` |
| hero | Spanish > Social Media and Online Life | `https://upload.wikimedia.org/wikipedia/commons/8/83/Social_media_addiction.jpg` |
| hero | Spanish > Spanish Festivals and Celebrations | `https://upload.wikimedia.org/wikipedia/commons/f/fc/San_marcos_bullfight_01.jpg` |
| hero | Spanish > Teachers, School Day and Facilities | `https://upload.wikimedia.org/wikipedia/commons/e/e3/Ceip_virgen_paz_vicar_2.jpg` |

## Lesson Numbering Issues

None found.

---

## Per-Subject Detail

### Business Studies

**30 lessons across 2 units:** Theme 1: Investigating Small Business, Theme 2: Building a Business

**Guide pages:** 19 — {'exam-technique': 8, 'revision-technique': 11}

| Metric | Value |
|--------|-------|
| Status: live | 30/30 |
| Status: pending_review | 0/30 |
| Has content | 30/30 |
| Has hero image | 30/30 |
| Has narration | 30/30 |
| Has podcast | 30/30 |
| Has video | 26/30 |
| Has practice Qs | 30/30 |
| Has knowledge checks | 30/30 |
| Has flashcards | 30/30 |
| Has related media | 30/30 |
| Has exam tip | 30/30 |
| Has conclusion | 30/30 |

**All 30 lessons passed automated checks.**

### Computer Science

**23 lessons across 2 units:** Computer Systems, Computational Thinking, Algorithms & Programming

**Guide pages:** 15 — {'exam-technique': 7, 'revision-technique': 8}

| Metric | Value |
|--------|-------|
| Status: live | 23/23 |
| Status: pending_review | 0/23 |
| Has content | 23/23 |
| Has hero image | 23/23 |
| Has narration | 23/23 |
| Has podcast | 23/23 |
| Has video | 0/23 |
| Has practice Qs | 23/23 |
| Has knowledge checks | 23/23 |
| Has flashcards | 23/23 |
| Has related media | 23/23 |
| Has exam tip | 23/23 |
| Has conclusion | 23/23 |

**All 23 lessons passed automated checks.**

### Creative iMedia

**23 lessons across 4 units:** The Media Industry, Product Design, Pre-Production Planning, Distribution and Media

**Guide pages:** 12 — {'exam-technique': 5, 'revision-technique': 7}

| Metric | Value |
|--------|-------|
| Status: live | 23/23 |
| Status: pending_review | 0/23 |
| Has content | 23/23 |
| Has hero image | 23/23 |
| Has narration | 23/23 |
| Has podcast | 23/23 |
| Has video | 0/23 |
| Has practice Qs | 23/23 |
| Has knowledge checks | 23/23 |
| Has flashcards | 23/23 |
| Has related media | 23/23 |
| Has exam tip | 23/23 |
| Has conclusion | 23/23 |

**Lessons with issues (6/23):**

- **L1: Introduction to Creative iMedia (The Media Industry)**
  - Only 4 flashcard questions (expected 5)
- **L1: Purpose, Style, Content and Layout (Product Design)**
  - Only 4 flashcard questions (expected 5)
- **L2: Mind Maps and Mood Boards (Pre-Production Planning)**
  - Only 4 flashcard questions (expected 5)
- **L4: Job Roles in the Media Industry (Part 1) (The Media Industry)**
  - Only 4 flashcard questions (expected 5)
- **L5: Visualisation Diagrams and Wireframes (Pre-Production Planning)**
  - Only 4 flashcard questions (expected 5)
- **L6: Camera Shots, Angles and Movement (Pre-Production Planning)**
  - Only 4 flashcard questions (expected 5)

### Design & Technology

**20 lessons across 3 units:** Core Technical Principles, Specialist Technical Principles, Designing & Making Principles

**Guide pages:** 14 — {'exam-technique': 6, 'revision-technique': 8}

| Metric | Value |
|--------|-------|
| Status: live | 20/20 |
| Status: pending_review | 0/20 |
| Has content | 20/20 |
| Has hero image | 20/20 |
| Has narration | 20/20 |
| Has podcast | 17/20 |
| Has video | 0/20 |
| Has practice Qs | 20/20 |
| Has knowledge checks | 20/20 |
| Has flashcards | 20/20 |
| Has related media | 20/20 |
| Has exam tip | 20/20 |
| Has conclusion | 20/20 |

**Lessons with issues (3/20):**

- **L1: New & Emerging Technologies (Core Technical Principles)**
  - Missing podcast (not in related media)
- **L2: Energy Generation & Storage (Core Technical Principles)**
  - Missing podcast (not in related media)
- **L3: Modern & Smart Materials (Core Technical Principles)**
  - Missing podcast (not in related media)

### Drama

**12 lessons across 2 units:** Rise Up (Section B), Blood Brothers (Section A)

**Guide pages:** 17 — {'exam-technique': 9, 'revision-technique': 8}

| Metric | Value |
|--------|-------|
| Status: live | 12/12 |
| Status: pending_review | 0/12 |
| Has content | 12/12 |
| Has hero image | 12/12 |
| Has narration | 12/12 |
| Has podcast | 12/12 |
| Has video | 12/12 |
| Has practice Qs | 12/12 |
| Has knowledge checks | 12/12 |
| Has flashcards | 12/12 |
| Has related media | 12/12 |
| Has exam tip | 12/12 |
| Has conclusion | 12/12 |

**All 12 lessons passed automated checks.**

### English Language

**30 lessons across 4 units:** Paper 1 Reading: Analysing Fiction, Paper 1 Writing: Creative Writing, Paper 2 Reading: Non-Fiction Analysis, Paper 2 Writing: Transactional Writing

**Guide pages:** 18 — {'exam-technique': 9, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 30/30 |
| Status: pending_review | 0/30 |
| Has content | 30/30 |
| Has hero image | 30/30 |
| Has narration | 30/30 |
| Has podcast | 30/30 |
| Has video | 30/30 |
| Has practice Qs | 30/30 |
| Has knowledge checks | 30/30 |
| Has flashcards | 30/30 |
| Has related media | 30/30 |
| Has exam tip | 30/30 |
| Has conclusion | 30/30 |

**All 30 lessons passed automated checks.**

### English Literature

**42 lessons across 5 units:** Macbeth, A Christmas Carol, Animal Farm, Power & Conflict Poetry, Unseen Poetry

**Guide pages:** 17 — {'exam-technique': 8, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 42/42 |
| Status: pending_review | 0/42 |
| Has content | 42/42 |
| Has hero image | 42/42 |
| Has narration | 42/42 |
| Has podcast | 42/42 |
| Has video | 42/42 |
| Has practice Qs | 42/42 |
| Has knowledge checks | 42/42 |
| Has flashcards | 42/42 |
| Has related media | 42/42 |
| Has exam tip | 42/42 |
| Has conclusion | 42/42 |

**Lessons with issues (1/42):**

- **L6: Banquo & Deception (Macbeth)**
  - Only 4 flashcard questions (expected 5)

### Food Preparation and Nutrition

**10 lessons across 1 units:** Food, Nutrition and Health

**Guide pages:** 15 — {'exam-technique': 6, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 10/10 |
| Status: pending_review | 0/10 |
| Has content | 10/10 |
| Has hero image | 10/10 |
| Has narration | 10/10 |
| Has podcast | 10/10 |
| Has video | 10/10 |
| Has practice Qs | 10/10 |
| Has knowledge checks | 10/10 |
| Has flashcards | 10/10 |
| Has related media | 10/10 |
| Has exam tip | 10/10 |
| Has conclusion | 10/10 |

**All 10 lessons passed automated checks.**

### French

**26 lessons across 3 units:** People and Lifestyle, Popular Culture, Communication and the World Around Us

**Guide pages:** 18 — {'exam-technique': 9, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 26/26 |
| Status: pending_review | 0/26 |
| Has content | 26/26 |
| Has hero image | 26/26 |
| Has narration | 26/26 |
| Has podcast | 26/26 |
| Has video | 0/26 |
| Has practice Qs | 26/26 |
| Has knowledge checks | 26/26 |
| Has flashcards | 26/26 |
| Has related media | 26/26 |
| Has exam tip | 26/26 |
| Has conclusion | 26/26 |

**Lessons with issues (19/26):**

- **L10: Jobs, Work Experience and Future Plans (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L1: Family Members and Descriptions (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L2: Friendships and Qualities (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L2: Past Holidays and Experiences (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L3: Accommodation and Hotels (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L3: Sport and Sporting Events (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L4: Countries, Weather and Transport (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L4: Healthy Living and Lifestyle (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L5: Customs and How We Celebrate (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L5: Food, Drink and Mealtimes (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L5: Technology and Social Media (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L6: Celebrity Culture and Role Models (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L6: My House and Home (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L7: My Town and Local Area (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L7: Social Media and Online Life (Popular Culture)**
  - Only 3 flashcard questions (expected 5)
- **L8: Eating Out and Restaurant Conversations (Popular Culture)**
  - Only 3 flashcard questions (expected 5)
- **L8: School Subjects and Opinions (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L8: The Environment and Global Issues (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L9: School Life, Rules and Uniform (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)

### Geography

**54 lessons across 3 units:** Paper 1: Physical Geography, Paper 2: Human Geography, Geographical Skills

**Guide pages:** 16 — {'exam-technique': 7, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 54/54 |
| Status: pending_review | 0/54 |
| Has content | 40/54 |
| Has hero image | 40/54 |
| Has narration | 40/54 |
| Has podcast | 40/54 |
| Has video | 0/54 |
| Has practice Qs | 40/54 |
| Has knowledge checks | 40/54 |
| Has flashcards | 40/54 |
| Has related media | 40/54 |
| Has exam tip | 40/54 |
| Has conclusion | 40/54 |

**All 54 lessons passed automated checks.**

### German

**26 lessons across 3 units:** People and Lifestyle, Popular Culture, Communication and the World

**Guide pages:** 18 — {'exam-technique': 9, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 26/26 |
| Status: pending_review | 0/26 |
| Has content | 26/26 |
| Has hero image | 26/26 |
| Has narration | 26/26 |
| Has podcast | 26/26 |
| Has video | 0/26 |
| Has practice Qs | 26/26 |
| Has knowledge checks | 26/26 |
| Has flashcards | 26/26 |
| Has related media | 26/26 |
| Has exam tip | 26/26 |
| Has conclusion | 26/26 |

**Lessons with issues (21/26):**

- **L10: School Life, Rules and Uniform (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L1: Free-Time Activities and Hobbies (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L2: Accommodation and Hotels (Communication and the World)**
  - Only 4 flashcard questions (expected 5)
- **L2: Personality and Character (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L2: Sport and Exercise (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L3: Music, Film and Television (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L3: Physical Appearance (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L3: Transport and Directions (Communication and the World)**
  - Only 4 flashcard questions (expected 5)
- **L4: Eating Out and Restaurant Conversations (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L4: Friendships and Ideal Friends (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L4: Weather and Holiday Activities (Communication and the World)**
  - Only 4 flashcard questions (expected 5)
- **L5: German Festivals and Celebrations (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L5: Relationships, Marriage and Future Plans (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L6: Customs and Daily Life in German-Speaking Countries (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L6: My House and Home (Communication and the World)**
  - Only 4 flashcard questions (expected 5)
- **L7: Celebrity Culture and Role Models (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L7: My Town and Local Area (Communication and the World)**
  - Only 4 flashcard questions (expected 5)
- **L8: Health, Fitness and Lifestyle (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L8: Social Media and Online Life (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L8: The Environment and Global Issues (Communication and the World)**
  - Only 4 flashcard questions (expected 5)
- **L9: School Subjects and Opinions (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)

### History

**60 lessons across 4 units:** Conflict & Tension, Health & the People, Elizabethan England, America, 1920–1973

**Guide pages:** 16 — {'exam-technique': 8, 'revision-technique': 8}

| Metric | Value |
|--------|-------|
| Status: live | 60/60 |
| Status: pending_review | 0/60 |
| Has content | 60/60 |
| Has hero image | 60/60 |
| Has narration | 60/60 |
| Has podcast | 60/60 |
| Has video | 60/60 |
| Has practice Qs | 60/60 |
| Has knowledge checks | 60/60 |
| Has flashcards | 60/60 |
| Has related media | 60/60 |
| Has exam tip | 60/60 |
| Has conclusion | 60/60 |

**Lessons with issues (1/60):**

- **L13: The Essex Rebellion (Elizabethan England)**
  - No key-fact boxes found

### Music

**26 lessons across 6 units:** AoS3: Film Music, AoS1: Musical Forms and Devices, AoS4: Popular Music, Musical Elements and Listening Skills, Set Work: Toto — Africa, AoS2: Music for Ensemble

**Guide pages:** 15 — {'exam-technique': 6, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 26/26 |
| Status: pending_review | 0/26 |
| Has content | 26/26 |
| Has hero image | 26/26 |
| Has narration | 26/26 |
| Has podcast | 26/26 |
| Has video | 26/26 |
| Has practice Qs | 26/26 |
| Has knowledge checks | 26/26 |
| Has flashcards | 26/26 |
| Has related media | 26/26 |
| Has exam tip | 26/26 |
| Has conclusion | 26/26 |

**All 26 lessons passed automated checks.**

### Religious Studies

**40 lessons across 8 units:** Christianity: Beliefs & Teachings, Christianity: Practices, Islam: Beliefs & Teachings, Islam: Practices, Theme A: Relationships & Families, Theme B: Religion & Life, Theme D: Religion, Peace & Conflict, Theme E: Religion, Crime & Punishment

**Guide pages:** 15 — {'exam-technique': 7, 'revision-technique': 8}

| Metric | Value |
|--------|-------|
| Status: live | 40/40 |
| Status: pending_review | 0/40 |
| Has content | 40/40 |
| Has hero image | 40/40 |
| Has narration | 40/40 |
| Has podcast | 40/40 |
| Has video | 0/40 |
| Has practice Qs | 40/40 |
| Has knowledge checks | 40/40 |
| Has flashcards | 40/40 |
| Has related media | 40/40 |
| Has exam tip | 40/40 |
| Has conclusion | 40/40 |

**All 40 lessons passed automated checks.**

### Science

**48 lessons across 6 units:** Biology Paper 1, Biology Paper 2, Chemistry Paper 1, Chemistry Paper 2, Physics Paper 1, Physics Paper 2

**Guide pages:** 16 — {'exam-technique': 7, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 48/48 |
| Status: pending_review | 0/48 |
| Has content | 48/48 |
| Has hero image | 48/48 |
| Has narration | 48/48 |
| Has podcast | 48/48 |
| Has video | 48/48 |
| Has practice Qs | 48/48 |
| Has knowledge checks | 48/48 |
| Has flashcards | 48/48 |
| Has related media | 48/48 |
| Has exam tip | 48/48 |
| Has conclusion | 48/48 |

**All 48 lessons passed automated checks.**

### Separate Sciences

**22 lessons across 3 units:** Biology (Separate), Chemistry (Separate), Physics (Separate)

**Guide pages:** 16 — {'exam-technique': 7, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 22/22 |
| Status: pending_review | 0/22 |
| Has content | 22/22 |
| Has hero image | 22/22 |
| Has narration | 22/22 |
| Has podcast | 22/22 |
| Has video | 22/22 |
| Has practice Qs | 22/22 |
| Has knowledge checks | 22/22 |
| Has flashcards | 22/22 |
| Has related media | 22/22 |
| Has exam tip | 22/22 |
| Has conclusion | 22/22 |

**All 22 lessons passed automated checks.**

### Spanish

**26 lessons across 3 units:** People and Lifestyle, Popular Culture, Communication and the World Around Us

**Guide pages:** 18 — {'exam-technique': 9, 'revision-technique': 9}

| Metric | Value |
|--------|-------|
| Status: live | 26/26 |
| Status: pending_review | 0/26 |
| Has content | 26/26 |
| Has hero image | 26/26 |
| Has narration | 26/26 |
| Has podcast | 26/26 |
| Has video | 0/26 |
| Has practice Qs | 26/26 |
| Has knowledge checks | 26/26 |
| Has flashcards | 26/26 |
| Has related media | 26/26 |
| Has exam tip | 26/26 |
| Has conclusion | 26/26 |

**Lessons with issues (23/26):**

- **L10: School Rules, Homework and Future Plans (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L1: Family and Describing People (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L1: Holidays and Travel Plans (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L2: Accommodation and Hotels (Communication and the World Around Us)**
  - Only 3 flashcard questions (expected 5)
- **L2: Music, Film and Television (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L3: Relationships and Marriage (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L3: Sport and Exercise (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L3: Transport and Directions (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L4: Eating Out and Restaurant Conversations (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L4: Healthy Living and Lifestyle (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L4: Weather and Holiday Activities (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L5: Food, Drink and Mealtimes (People and Lifestyle)**
  - Only 5 practice questions (expected 6)
  - Only 4 flashcard questions (expected 5)
- **L5: Technology and Social Media (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L6: Body Parts, Illness and Ailments (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L6: Customs and Traditions (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L6: My House and Home (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L7: Celebrity Culture and Role Models (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L7: Drugs, Smoking and Alcohol (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L7: My Town and Local Area (Communication and the World Around Us)**
  - Only 3 flashcard questions (expected 5)
- **L8: School Subjects and Opinions (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)
- **L8: Social Media and Online Life (Popular Culture)**
  - Only 4 flashcard questions (expected 5)
- **L8: The Environment and Global Issues (Communication and the World Around Us)**
  - Only 4 flashcard questions (expected 5)
- **L9: Teachers, School Day and Facilities (People and Lifestyle)**
  - Only 4 flashcard questions (expected 5)

### Sport Science

**10 lessons across 1 units:** R180: Reducing the Risk of Sports Injuries

**Guide pages:** 14 — {'exam-technique': 6, 'revision-technique': 8}

| Metric | Value |
|--------|-------|
| Status: live | 10/10 |
| Status: pending_review | 0/10 |
| Has content | 10/10 |
| Has hero image | 10/10 |
| Has narration | 10/10 |
| Has podcast | 10/10 |
| Has video | 10/10 |
| Has practice Qs | 10/10 |
| Has knowledge checks | 10/10 |
| Has flashcards | 10/10 |
| Has related media | 10/10 |
| Has exam tip | 10/10 |
| Has conclusion | 10/10 |

**All 10 lessons passed automated checks.**

---

## Recommended Manual QA (for Tom)

These checks cannot be automated and need human review:

1. **Content accuracy** — sample 2-3 lessons per subject, check facts against the spec
2. **Hero image relevance** — do images match the topic? (spot-check 1 per unit)
3. **Diagram quality** — visual clarity, correct labels, not misleading
4. **Narration quality** — listen to 1-2 per subject for mispronunciations
5. **Practice question accuracy** — are answers actually correct? (especially Maths/Science)
6. **Related media relevance** — are YouTube videos still live and on-topic?
