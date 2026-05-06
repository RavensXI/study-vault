# AQA Sociology — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Sociology lessons (AQA 8192). Quality bar is high: students should be able to **click any link and immediately reach the content** (a YouTube watch page that plays, a Spotify/Apple Podcasts episode page that plays, a study tool that loads, an article that opens). The single exception is Movies/TV/Documentaries — those use JustWatch UK aggregator pages because most films aren't free-to-watch directly.

## CRITICAL — ROOT URLs ONLY for study tools

We have just had a major audit (731 broken URLs across previous builds) caused by agents hallucinating specific topic pages — guide IDs, lesson slugs, deep paths that didn't exist. **For Study Tools, USE ROOT or SUBJECT-LEVEL URLS ONLY.** It is far better to send students to `https://www.tutor2u.net/sociology` (which definitely exists and lets them search) than to invent `https://www.tutor2u.net/sociology/reference/marxist-perspective-on-the-family-2024-revision-guide` (which probably doesn't exist).

**Approved root URLs for Sociology:**
- `https://www.tutor2u.net/sociology` (gold-standard for GCSE/A-level Sociology — let students browse)
- `https://www.bbc.co.uk/bitesize/subjects/zbckjxs` (BBC Bitesize Sociology subject root — verify this exists; otherwise use `https://www.bbc.co.uk/bitesize` and let them search)
- `https://senecalearning.com/en-GB/` (Seneca Learning home — students search for AQA Sociology)
- `https://www.ons.gov.uk/` (Office for National Statistics — for crime, divorce, family stats)
- `https://www.ipsos.com/en-uk` (Ipsos UK — public attitudes data)
- `https://www.jrf.org.uk/` (Joseph Rowntree Foundation — poverty research)

**Do NOT** invent specific topic pages like `https://www.tutor2u.net/sociology/reference/family-functions-revision-guide`. If you're not 100% certain a deep URL exists, use the root.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_sociology-aqa/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

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
- One of: `Documentaries` / `Movies` / `TV Shows` (pick exactly one — `Documentaries` is usually best for Sociology; `TV Shows` works for Crime, Family or Stratification lessons that have strong UK drama)
- `Study Tools`

`Articles & Reading` is optional but recommended for Sociology — lots of strong UK journalism (Guardian, BBC, Joseph Rowntree Foundation, Resolution Foundation, Health Foundation) sits naturally here and pushes the per-lesson item count above 6 comfortably.

## Hard rules

- **Each lesson: ≥6 items total**, spanning the four required categories (≥1 each: Podcasts, Videos & Channels, one of Documentaries/Movies/TV Shows, Study Tools). A 5th category (Articles & Reading) is welcome.
- **Every URL must be clickable** and take the student straight to the content — not a search results page, not a homepage (except for the approved root-URL study tools listed above).
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each** with the oembed endpoint before adding:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  If oembed returns an error or HTTP non-200, drop it. **DO NOT use HEAD requests** — YouTube returns 200 even for deleted videos.
- **Podcasts**: link to a specific EPISODE on Spotify, Apple Podcasts, Google Podcasts, or YouTube. Not the show's homepage.
  - Strong Sociology-relevant podcast sources:
    - **The Sociology Show** podcast — explicit GCSE/A-level Sociology focus. Link to specific episodes on Spotify or Apple Podcasts.
    - **BBC Sounds** factual / current affairs episodes:
      - BBC R4 *Thinking Allowed* (Laurie Taylor, sociology-led, weekly — frequently has Sociology spec topics)
      - BBC R4 *Analysis* (current sociological / political issues — class, family, crime)
      - BBC R4 *Woman's Hour* (relevant feminist sociology episodes)
      - BBC R4 *In Our Time* (occasional sociology-relevant episodes — Durkheim, Marx, Weber)
      - BBC R4 *File on 4* (investigative — crime, safeguarding, social policy)
      - BBC R4 *More or Less* (statistics literacy — useful for crime data, official statistics episodes)
      - BBC R4 *The Briefing Room* (current affairs analysis — useful for poverty, crime, education debates)
    - **Tutor2u Sociology podcast / channel** — explicitly designed for GCSE / A-level Sociology revision.
    - **The Joseph Rowntree Foundation** podcast — poverty / social policy.
    - **The King's Fund** podcast (relevant for life chances / health inequality episodes).
- **Movies / TV / Documentaries**: use JustWatch UK URLs (`https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`).
  - Strong Sociology titles:
    - **Family**: *This Is England* (2006 — class, family, masculinity), *Blue Story* (2019 — youth, family, crime), *I, Daniel Blake* (2016 — welfare state, family stress), *Ladybird* (2017 — mother-daughter, class), *We Need to Talk About Kevin* (2011 — family, deviance), *Boyhood* (2014 — long-form family). UK domestic drama: *EastEnders*, *Coronation Street* (JustWatch UK pages exist for ongoing soaps and offer episode browsing).
    - **Education**: *Educating Yorkshire / Educating Greater Manchester / Educating Cardiff* (Channel 4 documentary series — direct UK comprehensive school observation, *the* Sociology of Education documentary set), *To Sir With Love* (1967), *The Class* (2008), *The Wall* (1979 dystopian critique of education), *Half Nelson* (2006).
    - **Crime and deviance**: *24 Hours in Police Custody* (Channel 4 — Carlen-relevant, Heidensohn-relevant), *Killing Eve*, *Line of Duty*, *Top Boy* (Netflix — youth subcultures, Albert Cohen relevance), *The Wire* (HBO — Becker labelling, Merton strain), *We Need to Talk About Kevin*, *Boys Don't Cry* (1999), *I Am Not Your Negro* (2017 — race, deviance).
    - **Stratification / inequality**: *I, Daniel Blake* (2016), *Sorry We Missed You* (2019 — Loach on the gig economy / Marxist relevance), *Nomadland* (2020 — affluent worker / underclass relevance), *Parasite* (2019 — class internationally), *The Pursuit of Happyness* (2006 — meritocracy myth), *Inside Job* (2010), *The Spirit Level* documentary.
    - **Methods**: *Banksy: Exit Through the Gift Shop* (2010 — covert ethnography parallel), Adam Curtis *HyperNormalisation* (2016) and *Can't Get You Out of My Head* (2021 — sociological non-fiction film).
- **Study Tools** — USE THE APPROVED ROOTS:
  - `https://www.tutor2u.net/sociology` (let them search — this is gold standard for AQA Sociology revision)
  - `https://www.bbc.co.uk/bitesize` (or specific Sociology subject page if you can verify it exists)
  - `https://senecalearning.com/en-GB/` (Seneca Learning home — students search AQA Sociology)
  - `https://www.ons.gov.uk/` (ONS — for crime, divorce, family, ethnicity, employment statistics)
  - `https://www.ipsos.com/en-uk` (Ipsos UK — public attitudes data)
  - `https://www.jrf.org.uk/` (Joseph Rowntree Foundation — poverty research)
  - `https://www.resolutionfoundation.org/` (Resolution Foundation — living standards / inequality)
  - `https://www.kingsfund.org.uk/` (King's Fund — health and care inequality)
  - For each, the description field should make the topical connection clear (e.g. "Tutor2u Sociology — search for revision summaries on family functions, perspectives and named theorists.").
- **Articles & Reading**: 
  - **The Conversation UK** academic articles (verified author + topic — academic rigour, free-to-read).
  - **Guardian** (search for relevant journalism — but link to specific articles, NOT to /education or /society section pages).
  - **BBC News** features on relevant policy / family / crime / education stories.
  - **Joseph Rowntree Foundation** / **Resolution Foundation** / **King's Fund** specific reports (executive summaries are free-to-read).
  - **British Sociological Association** publications — BSA Discover Sociology pages.
- **Free YouTube channels for Sociology**:
  - **Tutor2u Sociology** — gold standard for GCSE/A-level Sociology revision videos. Curated playlists per topic.
  - **The Sociology Guy** (and similar revision teachers — verify each video plays via oembed before linking).
  - **Crash Course Sociology** (US-led but topically aligned to AQA 8192 in many places — link individual episodes that fit the lesson).
  - **The School of Life** — broader cultural / sociological short essays (Durkheim, Marx, Weber explainer videos).
  - **TED-Ed / TED talks** — Brené Brown on shame / connection (not on spec but illustrates research methods); Hans Rosling on global statistics (relevant to the dark figure of crime / official statistics critiques).
  - **BBC Ideas** (short-form video essays — frequently sociologically interesting on family, gender, poverty, crime).
- **No Wikipedia in primary slots** — fine as a study tool occasionally but ≤1 of 6.
- **No Save My Exams / PMT / MME / Revision World / Study Mind / Primrose Kitten** — banned per pipeline doctrine.
- **No reproduction of past papers, mark schemes, or exam board "model answers"** — that's the copyright moat we're protecting.
- **Tonal match**: items must connect to the LESSON's topic, not just the subject.
  - The Functions of Families lesson gets Parsons/functionalist + feminist counter media — not generic "family in society" content.
  - The Bowles and Gintis lesson gets correspondence-principle / Marxist-education content — not unrelated school documentaries.
  - The Becker labelling lesson gets stigma / labelling / moral panic content — not generic crime content.
  - The Townsend / Murray lesson gets relative deprivation / underclass / dependency content — not generic poverty pieces.
- **UK-relevance preferred**: students are British. Pick UK examples and outlets (BBC, Guardian, ONS, JRF, Resolution Foundation, King's Fund, BSA) first; international fine if best fit.
- **Sensitive content** — Sociology covers family breakdown, abuse, poverty, racial inequality, gender violence (Walby), crime. Pick study-appropriate sources. Avoid sensationalist tabloid coverage; prefer analytical pieces (BBC Reality Check, Guardian Long Read, BBC Ideas, FT Weekend, The Conversation UK) over front-page tabloids. Do NOT link to graphic content.
- **Political impartiality**: Sociology covers contested social policy. Curate balanced sources where the topic admits political disagreement (poverty, family policy, crime, education). Don't load Articles & Reading with all-Guardian or all-Telegraph items on a single lesson — mix BBC, Guardian, FT, Resolution Foundation, JRF, IFS, etc. so students see the spectrum.

## Verification step (mandatory)

For each YouTube URL, run the oembed check before including. Drop and replace if it fails. For other URLs, sanity-check by reading the URL — does it look like a direct content page? If `?search=` or homepage-like (e.g. raw `https://www.bbc.co.uk/`) — replace with a deeper link OR (for the approved Study Tools roots) make sure the description tells the student what to search for.

## How to write back

For each lesson:
1. Read `scripts/_content_sociology-aqa/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. **Preserve any existing `related_media`** — if there's already a "Podcasts" category with a "Lesson Podcast" item (from the StudyVault podcast generator), don't overwrite. Add curated podcasts alongside it under the same category, with the StudyVault podcast first.
4. Write back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo curated content back. Just write to disk and confirm.
