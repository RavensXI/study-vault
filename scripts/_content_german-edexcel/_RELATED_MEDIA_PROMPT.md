# Edexcel German — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE German lessons (Edexcel 1GN1). Quality bar is high: students should be able to **click any link and immediately reach the content** (a YouTube watch page that plays the video, a podcast episode page that plays the audio, a study tool that loads). The single exception is Movies/TV/Documentaries — those use JustWatch aggregator pages because most films aren't free-to-watch directly.

**ROOT-URL DISCIPLINE** — we recently shipped fabricated deep-link URLs in another build and had to retract. For this curation, prefer **HEAD-validated ROOT URLs** (the homepage of a known-stable hub). Topic-deep paths (`/topic/zsr2qfr/articles/zg7vhv4`) MUST be HEAD-validated against the live web; if you cannot confirm the path resolves, drop back to the hub root.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_german-edexcel/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

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
- **Podcasts**: link directly to the EPISODE on Spotify, Apple Podcasts, BBC Sounds, Deutsche Welle (DW), or YouTube. NOT the show's homepage, NOT a search.
  - **Strongly preferred German-learning podcast hubs (HEAD-validate ROOTs):**
    - BBC Sounds German content: `https://www.bbc.co.uk/sounds` (search by topic; pick episode-level links you can confirm)
    - Deutsche Welle (DW) Learn German hub: `https://learngerman.dw.com/en/overview/s-9528` (DW is Germany's international broadcaster — gold standard for graded German content)
    - DW Slowly Spoken News (Langsam gesprochene Nachrichten): `https://learngerman.dw.com/en/slowly-spoken-news/s-9509` (daily news read at slow pace)
    - DW Top-Thema mit Vokabeln: `https://learngerman.dw.com/en/top-thema/s-8031`
    - Coffee Break German: `https://radiolingua.com/coffeebreakgerman/`
    - GermanPod101: `https://www.germanpod101.com/`
    - Easy German Podcast: `https://easygerman.fm/`
    - News in Slow German: `https://www.newsinslowgerman.com/`
    - Slow German with Annik Rubens: `https://slowgerman.com/`
    - Deutsch — Warum nicht? (Deutsche Welle radio course): `https://learngerman.dw.com/en/learning-german/s-2473`
- **Movies / TV / Documentaries**: use JustWatch UK URLs in the form `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`. JustWatch aggregates "where to watch" so the student lands on a single page that lists Netflix/Amazon/free options. Don't link directly to Netflix/Amazon (region-specific, paywalled). For BBC iPlayer German-language content (occasional), use the iPlayer episode page directly — ROOT-validated.
  - **Good German-language film/TV titles** (verify on JustWatch before linking): Good Bye Lenin! (2003), The Lives of Others (Das Leben der Anderen, 2006), Run Lola Run (Lola rennt, 1998), Downfall (Der Untergang, 2004), Toni Erdmann (2016), The Wave (Die Welle, 2008), Cherry Blossoms (Kirschblüten — Hanami, 2008), The White Ribbon (Das weiße Band, 2009), Dark (Netflix series, 2017), Babylon Berlin (Sky Atlantic / iPlayer), Deutschland 83/86/89 (Channel 4 / Walter Presents), How to Sell Drugs Online (Fast) (Netflix), Charité (BBC Four — when available), Tatort (long-running detective series — selected episodes on iPlayer/Channel 4).
  - **German-language documentaries** (DW / iPlayer / YouTube): DW Documentaries hub `https://www.dw.com/en/tv/dw-documentary/s-100313`, BBC Reel German-themed pieces, Arte (Franco-German cultural broadcaster) selected English-subtitled docs.
- **Study Tools**: BBC Bitesize German topic pages are a strong root option (Bitesize covers GCSE German via Eduqas/CCEA/AQA — German content is found by browsing the languages section, e.g. `https://www.bbc.co.uk/bitesize/subjects/zcj2tfr` for KS3 German plus signposts to GCSE-relevant content; verify the path), Languages Online (Victoria State Schools — `https://www.education.vic.gov.au/languagesonline/german/german.htm`, an open educational resource with structured grammar drills), Linguee for German-English translation context (`https://www.linguee.com/english-german`), Conjuguemos for verb practice (`https://conjuguemos.com/`), Linguno (`https://www.linguno.com/`), Reverso Conjugator (`https://conjugator.reverso.net/conjugation-german.html`), Schubert Verlag online German exercises (`https://www.schubert-verlag.de/aufgaben/index.htm`). Direct URL to the relevant page where you've validated the path; otherwise the hub root.
- **Free YouTube channels for German** (channel handle URLs are stable):
  - Easy German (`https://www.youtube.com/@EasyGerman`) — street interviews with subtitles in German + English
  - Deutsch für Euch (`https://www.youtube.com/@DeutschFuerEuch`) — Katja explains grammar
  - Learn German with Anja (`https://www.youtube.com/@LearnGermanwithAnja`) — beginner-friendly
  - Learn German with Herr Antrim (`https://www.youtube.com/@LearnGermanwithHerrAntrim`) — GCSE-level grammar focus
  - Get Germanized (`https://www.youtube.com/@GetGermanized`) — Dominik covers culture + language
  - Deutsche Welle Learn German (`https://www.youtube.com/@dwlearngerman`)
  - GermanPod101 (`https://www.youtube.com/@GermanPod101`)
  - Smarter German (`https://www.youtube.com/@smartergerman`) — Michael Schmitz
  - Lingoni German (`https://www.youtube.com/@LingoniGERMAN`) — Jenny B
  - Authentic German Learning (`https://www.youtube.com/@AuthenticGermanLearning`)
- **No Wikipedia in primary slots** — Wikipedia is fine as a study tool occasionally but shouldn't be more than 1 of the 6.
- **No Save My Exams, PMT, MME, or other revision-aggregator sites** — banned per pipeline doctrine.
- **No reference to specific past papers, mark schemes, or exam board "model answers"** — that's the copyright moat we're protecting.
- **Tonal match**: items must connect to the LESSON's topic, not just the unit. A "vocabulary for ordering in restaurants" episode goes on the Theme 6 L04 (Eating Out) lesson, not the family/relationships lesson.
- **UK-relevance prefer**: students are British. Where possible, pick UK-hosted media outlets (BBC, Bitesize) first; native-German content (Deutsche Welle, Easy German, Tatort, Babylon Berlin) is excellent for immersion. American German-learning content is fine where it's the best fit.

## Verification step (mandatory)

For each YouTube URL (watch or channel), run the oembed check before including it. Drop and replace if it fails. For other URLs, prefer HEAD-validated ROOTs from the lists above. If you must include a deeper path, sanity-check by reading the URL — does it look like a direct content page? If `?search=` or `/search?q=` — replace with the hub root or a different URL.

## How to write back

For each lesson in your batch:

1. Read `scripts/_content_german-edexcel/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. **Preserve any existing `related_media` field** — if there's already a "Podcasts" category with a "Lesson Podcast" item (added by the StudyVault podcast generator), DON'T overwrite that item. Add your curated podcasts ALONGSIDE it under the same Podcasts category, with the StudyVault podcast first.
4. Write the JSON back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo the curated content back. Just write to disk and confirm.
