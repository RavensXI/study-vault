# Edexcel Spanish — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Spanish lessons (Edexcel 1SP1). Quality bar is high: students should be able to **click any link and immediately reach the content** (a YouTube watch page that plays the video, a podcast episode page that plays the audio, a study tool that loads). The single exception is Movies/TV/Documentaries — those use JustWatch aggregator pages because most films aren't free-to-watch directly.

**ROOT-URL DISCIPLINE** — we recently shipped fabricated deep-link URLs in another build and had to retract. For this curation, prefer **HEAD-validated ROOT URLs** (the homepage of a known-stable hub). Topic-deep paths (`/topic/zsr2qfr/articles/zg7vhv4`) MUST be HEAD-validated against the live web; if you cannot confirm the path resolves, drop back to the hub root.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_spanish-edexcel/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

## Output schema

For each lesson in your batch, ADD a `related_media` field to its lesson JSON. Schema:

```json
"related_media": [
  {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
      {
        "title": "Episode title",
        "description": "1-line context: who's hosting, what they cover, why it suits the lesson",
        "url": "https://open.spotify.com/episode/... OR https://podcasts.apple.com/.../id123?i=456 OR https://youtu.be/..."
      }
    ]
  },
  {
    "category": "Videos & Channels",
    "emoji": "📺",
    "items": [
      { "title": "...", "description": "...", "url": "https://www.youtube.com/watch?v=VIDEO_ID OR https://www.youtube.com/@channel" }
    ]
  },
  {
    "category": "Documentaries",
    "emoji": "🎬",
    "items": [
      { "title": "...", "description": "...", "url": "https://www.justwatch.com/uk/movie/SLUG OR https://www.bbc.co.uk/iplayer/episodes/..." }
    ]
  },
  {
    "category": "Study Tools",
    "emoji": "🛠️",
    "items": [
      { "title": "...", "description": "...", "url": "https://..." }
    ]
  }
]
```

(Verifier accepts category names: `"Videos & Channels"` for the video category and one of `{"Movies", "TV Shows", "Documentaries"}` for the visual-narrative category. Pick the most accurate label per lesson.)

## Hard rules

- **Each lesson: ≥6 items total**, spanning ALL FOUR categories (≥1 each: Podcasts, Videos & Channels, Documentaries (or Movies/TV Shows), Study Tools).
- **Every URL must be clickable** and take the student straight to the content — not a search results page, not a homepage banner ad.
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID`, `https://youtu.be/VIDEO_ID`, or `https://www.youtube.com/@channelhandle`. **Verify each** with the oembed endpoint before adding:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  If oembed returns an error or HTTP non-200, the video is private / deleted / region-locked — drop it. **DO NOT use HEAD requests for YouTube videos** — YouTube returns 200 even for dead videos.
- **Podcasts**: link directly to the EPISODE on Spotify, Apple Podcasts, BBC Sounds, RTVE Audio (RTVE is Radio Televisión Española — the Spanish state broadcaster), or YouTube. NOT the show's homepage, NOT a search.
  - **Strongly preferred Spanish-learning podcast hubs (HEAD-validate ROOTs):**
    - BBC Sounds Spanish content: `https://www.bbc.co.uk/sounds` (search by topic; pick episode-level links you can confirm)
    - Notes in Spanish: `https://www.notesinspanish.com/` (multi-level Spanish for learners)
    - News in Slow Spanish: `https://www.newsinslowspanish.com/`
    - Coffee Break Spanish: `https://radiolingua.com/coffee-break-spanish/`
    - SpanishPod101: `https://www.spanishpod101.com/`
    - Duolingo Spanish Podcast: `https://podcast.duolingo.com/spanish`
    - Hoy Hablamos: `https://www.hoyhablamos.com/`
    - Españolistos: `https://www.espanolistos.com/`
- **Movies / TV / Documentaries**: use JustWatch UK URLs in the form `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`. JustWatch aggregates "where to watch" so the student lands on a single page that lists Netflix/Amazon/free options. Don't link directly to Netflix/Amazon (region-specific, paywalled). For BBC iPlayer Spanish-language content (occasional), use the iPlayer episode page directly — ROOT-validated.
  - **Good Spanish-language film/TV titles** (verify on JustWatch before linking): Pan's Labyrinth (2006, Guillermo del Toro), Roma (2018), The Motorcycle Diaries (2004), All About My Mother (1999, Almodóvar), Volver (2006, Almodóvar), Y Tu Mamá También (2001), Coco (2017, mostly English but Spanish themes), Encanto (2021, mostly English but Colombian setting), Money Heist / La Casa de Papel (Netflix series), Élite (Netflix), Narcos (Netflix), Vis a Vis (Locked Up).
  - **Spanish-language documentaries** (RTVE / iPlayer / YouTube): RTVE Documentales hub `https://www.rtve.es/play/videos/documentales/`, BBC Reel: Spanish-themed pieces.
- **Study Tools**: BBC Bitesize Spanish topic pages are a strong root option (`https://www.bbc.co.uk/bitesize/subjects/zfckjxs` for Spanish), Languages Online (Victoria State Schools — `https://www.education.vic.gov.au/languagesonline/spanish/spanish.htm`, an open educational resource), SpanishDict (`https://www.spanishdict.com/`), Conjuguemos for verb practice (`https://conjuguemos.com/`), Linguno (`https://www.linguno.com/`), Olesur for grammar drills (`https://www.olesur.com/educacion/`). Direct URL to the relevant page where you've validated the path; otherwise the hub root.
- **Free YouTube channels for Spanish** (channel handle URLs are stable):
  - Dreaming Spanish (`https://www.youtube.com/@DreamingSpanish`) — comprehensible-input lessons
  - Butterfly Spanish (`https://www.youtube.com/@ButterflySpanish`) — Ana from Mexico
  - Why Not Spanish? (`https://www.youtube.com/@WhyNotSpanish`)
  - Español con Juan (`https://www.youtube.com/@1001ReasonsToLearnSpanish`)
  - Spanish with Paul (`https://www.youtube.com/@SpanishwithPaul`)
  - Light Speed Spanish (`https://www.youtube.com/@LightSpeedSpanish`)
  - Senor Jordan (`https://www.youtube.com/@senorjordan`) — beginner GCSE-friendly
  - LingoMarina (`https://www.youtube.com/@LingoMarina`) — multilingual learning hacks (Spanish content)
  - Easy Spanish (`https://www.youtube.com/@EasySpanish`) — street interviews with subtitles
  - SpanishPod101 (`https://www.youtube.com/@SpanishPod101`)
- **No Wikipedia in primary slots** — Wikipedia is fine as a study tool occasionally but shouldn't be more than 1 of the 6.
- **No Save My Exams, PMT, MME, or other revision-aggregator sites** — banned per pipeline doctrine.
- **No reference to specific past papers, mark schemes, or exam board "model answers"** — that's the copyright moat we're protecting.
- **Tonal match**: items must connect to the LESSON's topic, not just the unit. A "vocabulary for ordering tapas" episode goes on the Theme 6 L04 (Eating Out) lesson, not the family/relationships lesson.
- **UK-relevance prefer**: students are British. Where possible, pick UK-hosted media outlets (BBC, Bitesize) first; Spanish-language native content (RTVE, Notes in Spanish) is excellent for immersion. American Spanish-learning content is fine where it's the best fit.

## Verification step (mandatory)

For each YouTube URL (watch or channel), run the oembed check before including it. Drop and replace if it fails. For other URLs, prefer HEAD-validated ROOTs from the lists above. If you must include a deeper path, sanity-check by reading the URL — does it look like a direct content page? If `?search=` or `/search?q=` — replace with the hub root or a different URL.

## How to write back

For each lesson in your batch:

1. Read `scripts/_content_spanish-edexcel/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. **Preserve any existing `related_media` field** — if there's already a "Podcasts" category with a "Lesson Podcast" item (added by the StudyVault podcast generator), DON'T overwrite that item. Add your curated podcasts ALONGSIDE it under the same Podcasts category, with the StudyVault podcast first.
4. Write the JSON back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo the curated content back. Just write to disk and confirm.
