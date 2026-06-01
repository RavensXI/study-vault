# Picker Audit: RE, Drama, Film Studies
_Date: 2026-06-01 | Read-only audit — no content modified_

---

## (A) Religious Studies — three slugs

### religious-studies-aqa (AQA 8062)

**Spec offers:**
- Component 1 (religions): 7 religions — Buddhism, Catholic Christianity, Christianity, Hinduism, Islam, Judaism, Sikhism. Each has Beliefs + Practices units.
- Component 2 (themes): Themes A–F (6 non-textual themes) + Themes G & H (St Mark's Gospel textual studies).

**Picker offers:**
- 7 religions (slugs `buddhism`, `catholic-christianity`, `christianity`, `hinduism`, `islam`, `judaism`, `sikhism`), expanded to `{slug}-beliefs` + `{slug}-practices` by the filter.
- 6 themes: A-F only. Themes G & H are absent from the picker.

**Built units (20):**
```
buddhism-beliefs, buddhism-practices
catholic-christianity-beliefs, catholic-christianity-practices
christianity-beliefs, christianity-practices
hinduism-beliefs, hinduism-practices
islam-beliefs, islam-practices
judaism-beliefs, judaism-practices
sikhism-beliefs, sikhism-practices
theme-a-relationships, theme-b-religion-life, theme-c-existence-of-god
theme-d-peace-conflict, theme-e-crime-punishment, theme-f-human-rights-social-justice
```

**Gaps:**
- Themes G and H (St Mark's Gospel) are in the spec but NOT offered by the picker. The picker only supports the non-textual route. Students taking the textual studies route (2B) have no picker option and no built content.
- The spec permits Themes G+H as 2 of the 4 component-2 themes; these are distinct units with entirely separate lesson content. Neither is built.

**VERDICT: PARTIAL-BUILD** — picker deliberately omits the textual studies route (Themes G & H). If you ever add a textual route option to the picker, two units of content would need building first.

---

### religious-studies-edexcel (Edexcel 1RA0)

**Spec offers:**
- Paper 1: 3 religions in depth (Catholic Christianity, Christianity, Islam).
- Paper 2: 7 second-religion options (Catholic, Christianity, Islam, Buddhism, Hinduism, Judaism, Sikhism).
- Paper 3: Philosophy & Ethics — auto-derived to match Paper 1 religion (3 versions).
- Paper 4: Textual Studies — Mark's Gospel OR the Qur'an (2 options). Student sits Paper 3 OR Paper 4.

**Picker offers:**
- Paper 1: 3 options — all match spec.
- Paper 2: 7 options — all match spec.
- Paper 4: 2 options (Marks Gospel, The Qur'an).
- Paper 3 is auto-derived by `RE_EDEXCEL_PAPER3_MAP` in free-user-filters.js; no user choice needed.

**Built units (15):**
```
paper-1-catholic-christianity, paper-1-christianity, paper-1-islam
paper-2-catholic-christianity, paper-2-christianity, paper-2-islam
paper-2-buddhism, paper-2-hinduism, paper-2-judaism, paper-2-sikhism
paper-3-philosophy-ethics-catholic, paper-3-philosophy-ethics-christianity, paper-3-philosophy-ethics-islam
paper-4-marks-gospel, paper-4-quran
```

**Gaps:** None. All picker options have built units.

**VERDICT: OK**

---

### religious-studies-eduqas (Eduqas C120QS)

**Spec offers:**
- Route A: 2 of 5 world faiths (Buddhism, Hinduism, Islam, Judaism, Sikhism) + Christianity (compulsory in Comp 2) + 2 of 4 themes (Relationships, Life & Death, Good & Evil, Human Rights).
- Route B: Catholic Christianity in depth — Comp 1 = Foundational Catholic Theology (Origins & Meaning + Good & Evil); Comp 2 = Applied Catholic Theology (Life & Death + Sin & Forgiveness); Comp 3 = Judaism (mandatory).

**Picker offers:**
- Religions (pick 2): Buddhism, Catholic Christianity, Christianity, Hinduism, Islam, Judaism, Sikhism (7).
- Themes (pick 2): Issues of Life and Death, Good and Evil, Relationships, Human Rights (4).
- Route B triggered when user picks Catholic Christianity (implicit in filter logic).

**Built units (15):**
```
buddhism, christianity, hinduism, islam, judaism, sikhism, catholic-christianity
catholic-foundational-origins-and-meaning, catholic-foundational-good-and-evil
catholic-applied-life-and-death, catholic-applied-sin-and-forgiveness
theme-life-and-death, theme-good-and-evil, theme-relationships, theme-human-rights
```

**Gaps — filter bug for Route B:**
The Route B implicit list in `free-user-filters.js` (`RE_EDUQAS_ROUTE_B_IMPLICIT`) adds only the two Foundational units:
```
catholic-foundational-origins-and-meaning
catholic-foundational-good-and-evil
```
It does NOT add the two Applied Catholic Theology units:
```
catholic-applied-life-and-death
catholic-applied-sin-and-forgiveness
```
These are Component 2 of Route B and are mandatory for Route B students. Both units are built in Supabase but will never appear on the browse page for a Route B picker selection, because the filter does not include them.

The general theme slugs (`theme-life-and-death`, `theme-good-and-evil`, etc.) are Route A cross-religious themes, not the Catholic-specific applied theology content. They should not substitute for the Route B Applied units.

**VERDICT: PARTIAL-BUILD** — content is built but filter does not surface the two Applied Catholic Theology units for Route B users. Fix needed in `js/free-user-filters.js`: add `catholic-applied-life-and-death` and `catholic-applied-sin-and-forgiveness` to `RE_EDUQAS_ROUTE_B_IMPLICIT`.

---

## (B) Drama — drama-aqa (AQA 8261)

**Spec set plays (9):**
The Crucible (Miller), Blood Brothers (Russell), Noughts and Crosses (Blackman/Cooke), Around the World in 80 Days (Verne/Eason), Things I Know to Be True (Bovell), Romeo and Juliet (Shakespeare), A Taste of Honey (Delaney), The Great Wave (Turnly), The Empress (Gupta).

**Picker offers (9 set plays):**
`the-crucible`, `blood-brothers`, `noughts-and-crosses`, `around-the-world-80-days`, `things-i-know-to-be-true`, `romeo-and-juliet`, `a-taste-of-honey`, `the-great-wave`, `the-empress`

**Built play units (9):**
```
blood-brothers, around-the-world-80-days, things-i-know-to-be-true, romeo-and-juliet
the-great-wave, the-crucible, noughts-and-crosses, a-taste-of-honey, the-empress
```

**Universal units (always shown, 3):**
`theatre-roles-stagecraft`, `practitioners-styles`, `live-theatre-review` — all built.

**Gaps:** None. All 9 picker set plays have built units. Spec lists no set play that the picker omits, and picker lists no play the spec doesn't include.

**VERDICT: OK**

---

## (C) Film Studies — film-studies-eduqas (Eduqas C670QS)

**Spec film options (25 total across 5 sections):**

| Section | Films |
|---------|-------|
| Mainstream pair (1 of 5 pairs) | Dracula/Lost Boys; Singin in the Rain/Grease; Pillow Talk/When Harry Met Sally; Rebel/Ferris Bueller; Invasion of Body Snatchers/E.T. |
| US Independent (1 of 5) | Juno, The Hurt Locker, Whiplash, Lady Bird, The Hate U Give |
| Global English (1 of 5) | Slumdog Millionaire, District 9, The Babadook, The Breadwinner, Jojo Rabbit |
| Global Non-English (1 of 5) | Tsotsi, The Wave, Wadjda, Girlhood, The Farewell |
| Contemporary UK (1 of 5) | Submarine, Attack the Block, Skyfall, Blinded by the Light, Rocks |

**Picker FILM_SELECTABLE_LIST (25 lesson slugs):**
All 25 match built Supabase lesson slugs in `film-studies-eduqas`. Note: The Hurt Locker's lesson slug is `the-hurt-locker-and-the-hate-u-give-issue-led-indies` (historical naming artefact); it is a standalone lesson covering only The Hurt Locker, confirmed by title "The Hurt Locker: Bigelow's Iraq Thriller". The Hate U Give has its own separate lesson `the-hate-u-give-and-issue-led-indie`.

**Built film-specific lessons (all 25 verified present):**
- 5 comparative pair lessons (one per pair)
- 5 indie film lessons (Juno, Whiplash, Lady Bird, The Hurt Locker, The Hate U Give)
- 5 global English language lessons
- 5 global non-English language lessons
- 5 contemporary UK film lessons

Non-selectable supporting lessons (overviews, context, specialist writing) are also built and correctly excluded from FILM_SELECTABLE.

**Gaps:** None.

**VERDICT: OK**

---

## Summary

| Slug | Verdict | Issue |
|------|---------|-------|
| `religious-studies-aqa` | PARTIAL-BUILD | Themes G & H (St Mark's Gospel textual route) not offered by picker and not built. Consistent — picker is non-textual-route only — but there is no textual-route content at all. |
| `religious-studies-edexcel` | OK | All picker options built. |
| `religious-studies-eduqas` | PARTIAL-BUILD | Route B Applied Catholic Theology units (`catholic-applied-life-and-death`, `catholic-applied-sin-and-forgiveness`) are built in Supabase but missing from `RE_EDUQAS_ROUTE_B_IMPLICIT` filter list. Route B students cannot see them on the browse page. **Fix required in `js/free-user-filters.js`.** |
| `drama-aqa` | OK | All 9 set plays built and in picker. Universal units all present. |
| `film-studies-eduqas` | OK | All 25 selectable film lessons built and in picker. |

### Action items

1. **RE Eduqas Route B filter (high priority):** In `js/free-user-filters.js`, add to `RE_EDUQAS_ROUTE_B_IMPLICIT`:
   ```js
   var RE_EDUQAS_ROUTE_B_IMPLICIT = [
     'catholic-foundational-origins-and-meaning',
     'catholic-foundational-good-and-evil',
     'catholic-applied-life-and-death',        // ADD
     'catholic-applied-sin-and-forgiveness'    // ADD
   ];
   ```

2. **RE AQA Textual Studies (low priority / parked):** Themes G & H (St Mark's Gospel) are not built and not offered. This is acceptable for now if the target audience is predominantly non-textual-route schools. If textual-route schools are onboarded, build two units before adding them to the picker.
