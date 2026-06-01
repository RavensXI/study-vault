# History Component Audit — 2026-06-01

Audits whether each free-tier History slug has (a) option groups identified, (b) all options built in Supabase, and (c) a working picker wired in both `js/free-user-filters.js` AND `index.html`.

---

## Picker wiring summary

| Layer | AQA | Edexcel | OCR | Eduqas |
|-------|-----|---------|-----|--------|
| `HISTORY_SLUGS` in `free-user-filters.js` | YES | YES | **NO** | **NO** |
| `historyOptions[board]` in `index.html` | YES | YES | YES | **NO** |
| Options saved to `entry.options` on finish | YES | YES | YES (picker runs) | **NO** (picker skipped — empty object saved) |
| `getAllowedUnitSlugs()` returns filtered list | YES | YES | **NO** (null → all 12 shown) | **NO** (null → all 16 shown) |

Key: `fwHasHistory()` fires for any board once user picks "History" in step 2. OCR gets the picker UI but the filter in `free-user-filters.js` never uses the saved picks because `'history-ocr'` is absent from `HISTORY_SLUGS`. Eduqas has no picker at all — `historyOptions['eduqas']` is undefined, so `buildHistoryPicker()` returns early and `wizardState.history` stays `{}`.

---

## history-aqa (AQA 8145)

### Optionality
Students pick **one per section** across 4 compulsory paper sections (declared at entry):

| Section | Pick | Spec options |
|---------|------|-------------|
| Period Study (Paper 1 Sec A) | 1 of 4 | AA America 1840–1895, AB Germany 1890–1945, AC Russia 1894–1945, AD America 1920–1973 |
| Wider World Depth (Paper 1 Sec B) | 1 of 5 | BA First World War 1894–1918, BB Inter-war Years 1918–39, BC East and West 1945–72, BD Asia 1950–75, BE Gulf and Afghanistan 1990–2009 |
| Thematic Study (Paper 2 Sec A) | 1 of 3 | AA Health and the People, AB Power and the People, AC Migration, Empires and the People |
| British Depth Study (Paper 2 Sec B) | 1 of 4 | BA Norman England, BB Medieval England (Edward I), BC Elizabethan England, BD Restoration England |

Total options: 16 across 4 groups. Student studies 4 units.

### Coverage (16 units in Supabase)

| # | Unit name | Slug | Spec option |
|---|-----------|------|-------------|
| 1 | Germany, 1890-1945 | germany-democracy-dictatorship | Period AB |
| 2 | Russia, 1894-1945 | russia-tsardom-communism | Period AC |
| 3 | America, 1920-1973 | america-opportunity-inequality | Period AD |
| 4 | America, 1840-1895 | america-expansion-consolidation | Period AA |
| 5 | Conflict and Tension: 1918-1939 | conflict-tension-inter-war | WW Depth BB |
| 6 | Conflict and Tension: East and West | conflict-tension-east-west | WW Depth BC |
| 7 | Conflict and Tension: 1894-1918 | conflict-tension-first-world-war | WW Depth BA |
| 8 | Conflict and Tension in Asia | conflict-tension-asia | WW Depth BD |
| 9 | Conflict and Tension: Gulf and Afghanistan | conflict-tension-gulf-afghanistan | WW Depth BE |
| 10 | Britain: Health and the People | britain-health-people | Thematic AA |
| 11 | Britain: Power and the People | britain-power-people | Thematic AB |
| 12 | Britain: Migration, Empires and the People | britain-migration-empires | Thematic AC |
| 13 | Elizabethan England, c1568-1603 | elizabethan-england | British Depth BC |
| 14 | Norman England, c1066-c1100 | norman-england | British Depth BA |
| 15 | Medieval England: the Reign of Edward I | medieval-england-edward-i | British Depth BB |
| 16 | Restoration England, 1660-1685 | restoration-england | British Depth BD |

All 16 spec options built. No gaps.

### Picker
`HISTORY_SLUGS` includes `'history-aqa'` ✓. `historyOptions['aqa']` has all 4 sections ✓. Filter applied in `getAllowedUnitSlugs` ✓.

### Verdict
**OK** — all options built, picker fully wired.

---

## history-edexcel (Edexcel 1HI0)

### Optionality
Students pick **one per paper** across 4 sections:

| Section | Pick | Spec options |
|---------|------|-------------|
| Thematic Study + Historic Environment (Paper 1) | 1 of 4 | 10 Crime+Punishment/Whitechapel, 11 Medicine/Western Front, 12 Warfare/London WWII, 13 Migrants/Notting Hill |
| British Depth Study (Paper 2) | 1 of 4 | B1 Anglo-Saxon+Norman, B2 Richard I+King John, B3 Henry VIII, B4 Early Elizabethan |
| Period Study (Paper 2) | 1 of 5 | P1 Spain+New World, P2 British America, P3 American West, P4 Superpower Cold War, P5 Conflict Middle East |
| Modern Depth Study (Paper 3) | 1 of 4 | 30 Russia, 31 Weimar+Nazi Germany, 32 Mao's China, 33 USA 1954–75 |

Total options: 17 across 4 groups. Student studies 4 units.

### Coverage (17 units in Supabase)

| # | Unit name | Slug | Spec option |
|---|-----------|------|-------------|
| 1 | Medicine in Britain | medicine-in-britain | Thematic 11 |
| 2 | Superpower Relations and the Cold War | superpower-relations | Period P4 |
| 3 | Anglo-Saxon and Norman England | anglo-saxon-norman | British Depth B1 |
| 4 | Weimar and Nazi Germany | weimar-nazi-germany | Modern Depth 31 |
| 5 | Crime and Punishment in Britain | crime-punishment-whitechapel | Thematic 10 |
| 6 | Migrants in Britain | migrants-in-britain | Thematic 13 |
| 7 | Warfare and British Society | warfare-british-society | Thematic 12 |
| 8 | Early Elizabethan England, 1558–88 | early-elizabethan-england | British Depth B4 |
| 9 | Henry VIII and his Ministers, 1509–40 | henry-viii-ministers | British Depth B3 |
| 10 | Richard I and King John, 1189–1216 | richard-i-king-john | British Depth B2 |
| 11 | The American West, c1835–c1895 | american-west | Period P3 |
| 12 | British America, 1713–83 | british-america | Period P2 |
| 13 | Conflict in the Middle East, 1945–95 | conflict-middle-east | Period P5 |
| 14 | Spain and the 'New World', c1490–c1555 | spain-new-world | Period P1 |
| 15 | The USA, 1954–75: Conflict at Home and Abroad | usa-conflict-home-abroad | Modern Depth 33 |
| 16 | Russia and the Soviet Union, 1917–41 | russia-soviet-union | Modern Depth 30 |
| 17 | Mao's China, 1945–76 | maos-china | Modern Depth 32 |

All 17 spec options built. No gaps.

### Picker
`HISTORY_SLUGS` includes `'history-edexcel'` ✓. `historyOptions['edexcel']` has all 4 sections ✓. Filter applied ✓.

### Verdict
**OK** — all options built, picker fully wired.

---

## history-ocr (OCR J410 — History A: Explaining the Modern World)

### Optionality
Students pick one component from each of 3 component groups. The Period Study (International Relations 1918–1975) is **compulsory** for all and taken alongside the Non-British Depth choice.

| Group | Pick | Spec options |
|-------|------|-------------|
| Group 1 — Period Study (fixed) + Non-British Depth | 1 of 5 depth options | China 1950–81, Germany 1925–55, South Africa 1960–94, USA 1919–48, USA 1945–74 |
| Group 2 — British Thematic Study | 1 of 3 | Migration to Britain c.1000–2010, Power: Monarchy & Democracy c.1000–2014, War and British Society c.790–2010 |
| Group 3 — British Depth + Historic Environment | 1 of 3 (linked to Group 2) | Impact of Empire 1688–c.1730 (Spitalfields), English Reformation 1520–1550 (Kenilworth), Personal Rule to Restoration 1629–1660 (Kenilworth) |

Note: Groups 2 and 3 are **linked** — specific pairings are mandatory (e.g. Migration → Impact of Empire). Students study 4 units: Int'l Relations + 1 Non-British Depth + 1 Thematic + 1 British Depth.

Total choosable options: 5 + 3 + 3 = 11 across 3 groups (plus 1 fixed unit). Student studies 4.

### Coverage (12 units in Supabase)

| # | Unit name | Slug | Group |
|---|-----------|------|-------|
| 1 | International Relations 1918-1975 | international-relations-1918-1975 | Fixed (all students) |
| 2 | China 1950-1981: The People and the State | china-people-state-1950-1981 | Group 1 |
| 3 | Germany 1925-1955: The People and the State | germany-people-state-1925-1955 | Group 1 |
| 4 | South Africa 1960-1994: The People and the State | south-africa-people-state-1960-1994 | Group 1 |
| 5 | The USA 1919-1948: The People and the State | usa-people-state-1919-1948 | Group 1 |
| 6 | The USA 1945-1974: The People and the State | usa-people-state-1945-1974 | Group 1 |
| 7 | Migration to Britain c.1000-c.2010 | migration-to-britain-1000-2010 | Group 2 |
| 8 | Power: Monarchy and Democracy in Britain c.1000-2014 | power-monarchy-democracy-1000-2014 | Group 2 |
| 9 | War and British Society c.790-c.2010 | war-british-society-790-2010 | Group 2 |
| 10 | Impact of Empire on Britain 1688-c.1730 with Spitalfields | impact-empire-britain-1688-1730 | Group 3 |
| 11 | The English Reformation c.1520-c.1550 with Kenilworth Castle | english-reformation-1520-1550 | Group 3 |
| 12 | Personal Rule to Restoration 1629-1660 with Kenilworth Castle | personal-rule-restoration-1629-1660 | Group 3 |

All 11 choosable + 1 fixed option built. No gaps.

### Picker
`historyOptions['ocr']` in `index.html` IS defined (3 sections: Non-British Depth, Thematic Study, British Depth Study). The wizard DOES show the picker when the user selects History + OCR. Options ARE saved to `entry.options` in `finishWizard()`.

**However:** `HISTORY_SLUGS` in `js/free-user-filters.js` is `['history-aqa', 'history-edexcel']` — `'history-ocr'` is absent. `getAllowedUnitSlugs('history-ocr')` always returns `null`, meaning the browse page ignores the saved picks and shows all 12 units unfiltered.

Additionally, Group 2–3 linked pairing logic is not encoded anywhere — if a student picks a Group 2 thematic, the linked Group 3 British Depth is not auto-included.

### Verdict
**MISSING-PICKER** — all options built and picker UI exists in wizard, but `free-user-filters.js` never applies the filter. `'history-ocr'` must be added to `HISTORY_SLUGS`. The fixed Period Study unit (`international-relations-1918-1975`) must also be auto-included in the filter output (same role as `DRAMA_UNIVERSAL` / `ENGLIT_COMPULSORY`).

---

## history-eduqas (Eduqas C100QS)

### Optionality
Students pick **one per component** across 4 sections (2 per component × 2 components):

**Component 1 — Studies in Depth (50%)**

| Group | Pick | Spec options |
|-------|------|-------------|
| British Study in Depth | 1 of 4 | 1A Conflict and Upheaval England 1337–1381, 1B Elizabethan Age 1558–1603, 1C Empire, Reform and War: Britain 1890–1918, 1D Austerity, Affluence and Discontent 1951–1979 |
| Non-British Study in Depth | 1 of 4 | 1E The Crusades c.1095–1149, 1F Voyages of Discovery 1492–1522, 1G Germany in Transition 1919–1939, 1H USA: A Nation of Contrasts 1910–1929 |

Note: British and Non-British must be from different historical eras.

**Component 2 — Studies in Breadth (50%)**

| Group | Pick | Spec options |
|-------|------|-------------|
| Period Study | 1 of 4 | 2A Development of the USA 1929–2000, 2B Development of Germany 1919–1991, 2C Development of the USSR 1924–1991, 2D Development of the UK 1919–1990 |
| Thematic Study | 1 of 4 | 2E Crime and Punishment in Britain c.500–present, 2F Health and Medicine in Britain c.500–present, 2G Development of Warfare in Britain c.500–present, 2H Entertainment and Leisure in Britain c.500–present |

Total options: 16 across 4 groups. Student studies 4 units.

### Coverage (16 units in Supabase)

| # | Unit name | Slug | Spec option |
|---|-----------|------|-------------|
| 1 | Conflict and Upheaval: England, 1337-1381 | conflict-upheaval-england-1337-1381 | British Depth 1A |
| 2 | The Elizabethan Age, 1558-1603 | elizabethan-age-1558-1603 | British Depth 1B |
| 3 | Empire, Reform and War: Britain, 1890-1918 | empire-reform-war-1890-1918 | British Depth 1C |
| 4 | Austerity, Affluence and Discontent, 1951-1979 | austerity-affluence-discontent-1951-1979 | British Depth 1D |
| 5 | The Crusades, c.1095-1149 | crusades-1095-1149 | Non-British Depth 1E |
| 6 | Voyages of Discovery and Conquest of the Americas | voyages-discovery-conquest-americas-1492-1522 | Non-British Depth 1F |
| 7 | Germany in Transition, 1919-1939 | germany-transition-1919-1939 | Non-British Depth 1G |
| 8 | The USA: A Nation of Contrasts, 1910-1929 | usa-nation-contrasts-1910-1929 | Non-British Depth 1H |
| 9 | The Development of the USA, 1929-2000 | development-usa-1929-2000 | Period Study 2A |
| 10 | The Development of Germany, 1919-1991 | development-germany-1919-1991 | Period Study 2B |
| 11 | The Development of the USSR, 1924-1991 | development-ussr-1924-1991 | Period Study 2C |
| 12 | The Development of the UK, 1919-1990 | development-uk-1919-1990 | Period Study 2D |
| 13 | Changes in Crime and Punishment in Britain | crime-punishment-britain-c500-present | Thematic 2E |
| 14 | Changes in Health and Medicine in Britain | health-medicine-britain-c500-present | Thematic 2F |
| 15 | The Development of Warfare in Britain | warfare-britain-c500-present | Thematic 2G |
| 16 | Changes in Entertainment and Leisure in Britain | entertainment-leisure-britain-c500-present | Thematic 2H |

All 16 spec options built. No gaps.

### Picker
`historyOptions['eduqas']` does **not exist** in `index.html`. When a user picks History + Eduqas board, `buildHistoryPicker()` finds `opts = undefined`, returns early, and `wizardState.history` stays `{}`. `entry.options` is saved as an empty object `{}`. `historyFilter()` checks `Object.keys(pref.options).length` → 0 → returns `null`. The browse page shows all 16 units unfiltered.

`'history-eduqas'` is also absent from `HISTORY_SLUGS` in `free-user-filters.js`.

### Verdict
**MISSING-PICKER** — all 16 options built, but picker is entirely absent from `historyOptions` in `index.html`, and `'history-eduqas'` is missing from `HISTORY_SLUGS` in `free-user-filters.js`. Both must be added.

---

## Summary table

| Slug | Options | Groups | Picker (index.html) | Filter (free-user-filters.js) | Verdict |
|------|---------|--------|--------------------|-----------------------------|---------|
| history-aqa | 16 across 4 groups, all built | Period Study (4), Wider World Depth (5), Thematic (3), British Depth (4) | YES — `historyOptions['aqa']` | YES — in `HISTORY_SLUGS` | **OK** |
| history-edexcel | 17 across 4 groups, all built | Thematic+Historic Env (4), British Depth (4), Period Study (5), Modern Depth (4) | YES — `historyOptions['edexcel']` | YES — in `HISTORY_SLUGS` | **OK** |
| history-ocr | 11 choosable + 1 fixed, all built | Non-British Depth (5), Thematic (3), British Depth (3) | YES — `historyOptions['ocr']` exists but Group 2/3 link logic absent | NO — missing from `HISTORY_SLUGS`; filter returns null | **MISSING-PICKER** |
| history-eduqas | 16 across 4 groups, all built | British Depth (4), Non-British Depth (4), Period Study (4), Thematic (4) | NO — `historyOptions['eduqas']` undefined; picker skipped | NO — missing from `HISTORY_SLUGS` | **MISSING-PICKER** |

---

## Fix checklist

### history-ocr
1. Add `'history-ocr'` to `HISTORY_SLUGS` in `js/free-user-filters.js`.
2. Update `historyFilter()` in `free-user-filters.js` to also include the compulsory `international-relations-1918-1975` slug (the fixed unit) for OCR — same approach as `DRAMA_UNIVERSAL`. Or add an OCR-specific branch in `getAllowedUnitSlugs`.
3. (Optional, UX improvement) Encode the Group 2/3 mandatory pairing in the picker so selecting a Thematic auto-selects the linked British Depth, or at least validate the combination before saving.

### history-eduqas
1. Add `historyOptions['eduqas']` to `index.html` with 4 sections (British Study in Depth, Non-British Study in Depth, Period Study, Thematic Study) and all 16 option slugs.
2. Add `'history-eduqas'` to `HISTORY_SLUGS` in `js/free-user-filters.js`.
3. Note: Eduqas spec restricts British + Non-British options to come from different eras — this combination validation is not strictly required for the filter to work (units just show/hide), but could be noted in picker UI.
