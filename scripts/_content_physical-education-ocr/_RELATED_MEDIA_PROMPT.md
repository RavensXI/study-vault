# OCR Physical Education — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Physical Education lessons (OCR J587). Quality bar is high: students should be able to **click any link and immediately reach the content** (a YouTube watch page that plays, a Spotify/Apple Podcasts episode page that plays, a study tool that loads). The single exception is Movies/TV/Documentaries — those use JustWatch aggregator pages because most films aren't free-to-watch directly.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_physical-education-ocr/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

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
    "category": "Study Tools",
    "emoji": "🛠️",
    "items": [ { "title": "...", "description": "...", "url": "https://..." } ]
  }
]
```

**IMPORTANT — exact category names** (the `_verify_subject_build.py` validator hard-checks for these strings, so don't paraphrase):
- `Podcasts`
- `Videos & Channels`
- `Documentaries` (or `Movies` / `TV Shows` — pick exactly ONE of these three)
- `Study Tools`

## Hard rules

- **Each lesson: ≥6 items total**, spanning all four categories (≥1 each).
- **Every URL must be clickable** and take the student straight to the content — not a search results page, not a homepage.
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each** with the oembed endpoint before adding:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  If oembed returns an error or HTTP non-200, drop it. **DO NOT use HEAD requests** — YouTube returns 200 even for deleted videos.
- **Podcasts**: link to a specific EPISODE on Spotify, Apple Podcasts, Google Podcasts, or YouTube. Not the show's homepage.
  - Good PE-relevant podcast sources: BBC The Doctor's Kitchen (sports nutrition), The Joe Rogan Experience (sport science episodes — pick carefully), Diary of a CEO (Steven Bartlett — pick athlete/coach episodes: Mo Farah, Jonny Wilkinson, Jess Ennis-Hill, Eddie Hearn etc.), High Performance Podcast (Jake Humphrey & Damian Hughes — packed with athletes and coaches discussing psychology and performance), Sigma Nutrition Radio, Just Fly Performance Podcast, BBC 5 Live Sport Specials, BBC In Our Time (history of sport / Olympic episodes), Test Match Special, Tailenders, On the Mic with Conor McNamara, Don't Tell Me the Score (BBC R5 — Simon Mundie interviews on sport psychology and mindset).
- **Movies / TV / Documentaries**: use JustWatch UK URLs (`https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`).
  - Strong PE titles: Free Solo (2018, Alex Honnold — fear, focus, motivation), The Last Dance (2020, Michael Jordan — psychology of elite performance), Senna (2010 — F1 motivation/anxiety), All or Nothing (Amazon Prime — various football team docu-series), Drive to Survive (Netflix — F1, sport psychology, commercialisation), Untold (Netflix — sport psychology, ethics), Athlete A (2020 — ethics in gymnastics), Icarus (2017 — doping ethics), We Are the Champions (2020), Sunderland 'Til I Die (Netflix — engagement patterns / commercialisation), Bend It Like Beckham (2002 — engagement patterns / cultural influences), I, Tonya (2017 — ethics / psychology), Concussion (2015 — health & well-being), Coach Carter (2005 — leadership / motivation), Moneyball (2011 — use of data in sport), The Program (2015 — Lance Armstrong, doping ethics), When We Were Kings (1996 — sports psychology and culture).
- **Study Tools**: BBC Bitesize PE topic pages, tutor2u PE resources, Anatomy & Physiology Animations from KenHub or TeachMeAnatomy, BHF (British Heart Foundation) explainer pages, NHS resources on healthy lifestyle, English Institute of Sport articles, Sport England participation reports (for socio-cultural lessons), Olympic.org or Team GB profile pages (for engagement/elite-pathway lessons), Anti-Doping Database for ethics lessons. Direct URL to relevant page, not a homepage.
- **Free YouTube channels for PE**:
  - **Two Teachers** — solid GCSE PE summaries
  - **GCSE Wizard / Mr Hawley PE** — GCSE-specific
  - **Crash Course Anatomy & Physiology** — anatomy at a higher level but accessible
  - **Sports Science TV / Bjj Scout** — biomechanics
  - **Mr Sturge PE** — exam technique
  - **TED-Ed sport-science talks**
  - **BBC Reel** sport stories
  - **The Atlas of Skills** (sport psychology)
  - **OCR-aware GCSE PE channels** (where they exist) — favour these over AQA-only channels for OCR lessons
- **No Wikipedia in primary slots** — fine as a study tool occasionally but ≤1 of 6.
- **No Save My Exams / PMT / MME / Revision World / Study Mind / Primrose Kitten** — banned per pipeline doctrine.
- **No reproduction of past papers, mark schemes, or exam board "model answers"** — that's the copyright moat we're protecting.
- **Tonal match**: items must connect to the LESSON's topic, not just the subject. A "Mo Farah on motivation" episode goes on the goal-setting/SMART-targets lesson, not the cardiovascular system lesson.
- **UK-relevance preferred**: students are British. Pick UK examples and outlets first; international fine if best fit.
- **OCR awareness**: where a study tool or channel offers a board-specific revision page (e.g. BBC Bitesize OCR PE), pick the OCR variant over the generic or AQA variant.

## Verification step (mandatory)

For each YouTube URL, run the oembed check before including. Drop and replace if it fails. For other URLs, sanity-check by reading the URL — does it look like a direct content page? If `?search=` or homepage-like (e.g. `https://www.bbc.co.uk/bitesize`) — replace with a deeper link.

## How to write back

For each lesson:
1. Read `scripts/_content_physical-education-ocr/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. **Preserve any existing `related_media`** — if there's already a "Podcasts" category with a "Lesson Podcast" item (from the StudyVault podcast generator), don't overwrite. Add curated podcasts alongside it.
4. Write back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo curated content back. Just write to disk and confirm.
