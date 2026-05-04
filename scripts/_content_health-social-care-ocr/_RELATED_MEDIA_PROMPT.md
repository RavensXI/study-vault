# OCR Health and Social Care — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE / Cambridge National Health and Social Care lessons (OCR J835, Unit R032 only). Quality bar is high: students should be able to **click any link and immediately reach the content** (a YouTube watch page that plays, a Spotify/Apple Podcasts episode page that plays, a study tool that loads, an article that opens). The single exception is Movies/TV/Documentaries — those use JustWatch UK aggregator pages because most films aren't free-to-watch directly.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_health-social-care-ocr/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

## Output schema

For each lesson in your batch, ADD a `related_media` field to its lesson JSON. Schema:

```json
"related_media": [
  {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
      { "title": "Episode title", "description": "1-line context", "url": "https://open.spotify.com/episode/... OR https://podcasts.apple.com/.../id123?i=456 OR https://youtu.be/..." }
    ]
  },
  {
    "category": "Videos & Channels",
    "emoji": "📺",
    "items": [ { "title": "...", "description": "...", "url": "https://www.youtube.com/watch?v=VIDEO_ID" } ]
  },
  {
    "category": "Documentaries",
    "emoji": "🎬",
    "items": [ { "title": "Title (Year)", "description": "...", "url": "https://www.justwatch.com/uk/movie/SLUG" } ]
  },
  {
    "category": "Articles & Reading",
    "emoji": "📰",
    "items": [ { "title": "...", "description": "...", "url": "https://..." } ]
  },
  {
    "category": "Study Tools",
    "emoji": "🛠️",
    "items": [ { "title": "...", "description": "...", "url": "https://..." } ]
  }
]
```

**IMPORTANT — exact category names** (the `_verify_subject_build.py` validator hard-checks for these strings, so don't paraphrase):
- `Podcasts`
- `Videos & Channels`
- One of: `Documentaries` / `Movies` / `TV Shows` (pick exactly one — `Documentaries` is usually best for HSC)
- `Study Tools`

`Articles & Reading` is optional but strongly recommended for HSC (lots of policy / NHS / SCIE / Care Quality Commission writing that suits this subject) — adding it pushes the per-lesson item count above 6 comfortably.

## Hard rules

- **Each lesson: ≥6 items total**, spanning the four required categories (≥1 each: Podcasts, Videos & Channels, one of Documentaries/Movies/TV Shows, Study Tools). A 5th category (Articles & Reading) is welcome.
- **Every URL must be clickable** and take the student straight to the content — not a search results page, not a homepage.
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each** with the oembed endpoint before adding:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  If oembed returns an error or HTTP non-200, drop it. **DO NOT use HEAD requests** — YouTube returns 200 even for deleted videos.
- **Podcasts**: link to a specific EPISODE on Spotify, Apple Podcasts, Google Podcasts, or YouTube. Not the show's homepage.
  - Good HSC-relevant podcast sources: BBC Radio 4 *Inside Health*, BBC R4 *In the Balance* (NHS / care segments), BBC R4 *File on 4* (safeguarding / scandal investigations — picked carefully for tone), BBC R4 *Woman's Hour* (relevant care episodes — domestic abuse, mental-health support, dementia care), the *NHS Voices* podcast (NHS Confederation), *The Inquiry* (BBC World Service — wider context on UK care system), Nursing Times podcast, *Care Talk* podcast, *Skills for Care* podcast, *The King's Fund* podcast, *The Health Foundation* podcast.
- **Movies / TV / Documentaries**: use JustWatch UK URLs (`https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`).
  - Strong HSC titles: *24 Hours in A&E* (Channel 4), *24 Hours in Police Custody*, *Old People's Home for 4 Year Olds* (Channel 4 — intergenerational care), *Hospital* (BBC documentary series on NHS), *The Pharmacist* (Netflix), *Take Care of Maya* (Netflix — safeguarding tensions), *Sister Helen* (about a residential carer), *Iris* (2001 — dementia), *The Father* (2020 — dementia from inside), *Still Alice* (2014 — early-onset Alzheimer's), *Amour* (2012 — end-of-life care), *Care* (BBC drama, 2018, Sheridan Smith — domiciliary care under pressure), *I, Daniel Blake* (2016 — care system + welfare), *Three Identical Strangers* (2018 — care ethics), *The Lost Daughter* (2021 — caring relationships), *24 Hours in A&E* episode pages on Channel 4.
- **Study Tools**: BBC Bitesize Cambridge National HSC pages (where they exist; otherwise BBC Bitesize generic Health & Social Care pages), Skills for Care explainer pages, NHS England 6Cs / Compassion in Practice resource pages, Care Quality Commission inspection-criteria explainer pages, SCIE (Social Care Institute for Excellence) topic pages, NSPCC Learning safeguarding modules (free overviews), Mencap learning-disability resources, Age UK explainer pages, Disclosure and Barring Service GOV.UK explainer page, RNIB / RNID guidance for sensory-impairment communication.
- **Articles & Reading**: NHS England articles, Skills for Care policy briefings, Care Quality Commission reports, BMJ care-related pieces (where free-to-read), the Francis Report executive summary (free public summary), Cavendish Review summary (free public summary), Health Foundation analysis pieces, King's Fund explainers, Disability Rights UK guidance, Mencap explainers, NSPCC research summaries.
- **Free YouTube channels for HSC**:
  - **Two Teachers** — solid GCSE / Cambridge National HSC summaries
  - **NHS England** official channel — the 6Cs explainer videos and the Compassion in Practice series
  - **Skills for Care** — short videos on dignity, person-centred care, communication
  - **Care Quality Commission** — what inspections look for
  - **NSPCC Learning** — short safeguarding training clips
  - **Mencap** — learning-disability awareness videos
  - **Alzheimer's Society** — dementia-care clips
  - **RNID / RNIB** — sensory-impairment communication
  - **TED talks on care, empathy, dementia** (Atul Gawande, Naomi Feil "Validation Therapy", Wendy Mitchell on living with dementia)
- **No Wikipedia in primary slots** — fine as a study tool occasionally but ≤1 of 6.
- **No Save My Exams / PMT / MME / Revision World / Study Mind / Primrose Kitten** — banned per pipeline doctrine.
- **No reproduction of past papers, mark schemes, or exam board "model answers"** — that's the copyright moat we're protecting.
- **Tonal match**: items must connect to the LESSON's topic, not just the subject. A Makaton-on-CBeebies clip goes on the Special Methods of Communication lesson, not the Safeguarding lesson. *Old People's Home for 4 Year Olds* belongs on a person-centred-values or wellbeing lesson; the Francis Report summary belongs on the safeguarding or 6Cs lesson.
- **UK-relevance preferred**: students are British. Pick UK examples and outlets (NHS, CQC, NSPCC, Skills for Care, Mencap, Age UK, RNIB, RNID, Alzheimer's Society) first; international fine if best fit.
- **Sensitive content**: HSC topics include abuse, neglect, dementia, end-of-life, and serious incidents. Pick study-appropriate sources. Avoid sensationalist tabloid coverage of safeguarding scandals; prefer analytical pieces (BBC, Guardian, Health Service Journal) over front-page tabloids. Do NOT link to graphic abuse footage.

## Verification step (mandatory)

For each YouTube URL, run the oembed check before including. Drop and replace if it fails. For other URLs, sanity-check by reading the URL — does it look like a direct content page? If `?search=` or homepage-like (e.g. `https://www.bbc.co.uk/bitesize`) — replace with a deeper link.

## How to write back

For each lesson:
1. Read `scripts/_content_health-social-care-ocr/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. **Preserve any existing `related_media`** — if there's already a "Podcasts" category with a "Lesson Podcast" item (from the StudyVault podcast generator), don't overwrite. Add curated podcasts alongside it under the same category, with the StudyVault podcast first.
4. Write back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo curated content back. Just write to disk and confirm.
