# Edexcel Business — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Business lessons (Edexcel 1BS0). Quality bar is high: students should be able to **click any link and immediately reach the content** (a YouTube watch page that plays the video, a Spotify/Apple Podcasts episode page that plays the audio, a study tool that loads). The single exception is Movies/TV/Documentaries — those use JustWatch aggregator pages because most films aren't free-to-watch directly.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_business-edexcel/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

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
    "category": "Videos",
    "emoji": "📺",
    "items": [
      { "title": "...", "description": "...", "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ]
  },
  {
    "category": "Movies, TV Shows, Documentaries",
    "emoji": "🎬",
    "items": [
      { "title": "Title (Year)", "description": "...", "url": "https://www.justwatch.com/uk/movie/SLUG" }
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

## Hard rules

- **Each lesson: ≥6 items total**, spanning ALL FOUR categories (≥1 each: Podcasts, Videos, Movies/TV/Docs, Study Tools).
- **Every URL must be clickable** and take the student straight to the content — not a search results page, not a homepage.
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each** with the oembed endpoint before adding:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  If oembed returns an error or HTTP non-200, the video is private / deleted / region-locked — drop it. **DO NOT use HEAD requests** — YouTube returns 200 even for dead videos.
- **Podcasts**: link directly to the EPISODE on Spotify, Apple Podcasts, Google Podcasts, or YouTube. Not the show's homepage, not a search.
  - Good Business sources: BBC Business Daily, BBC The Bottom Line (Evan Davis), Eat Sleep Work Repeat, Diary of a CEO (Steven Bartlett — pick episodes with substantive business content, not pure self-help), How I Built This (Guy Raz, NPR), Money Box (BBC R4), Best of Today (BBC business segments), Marketplace (American but accessible), Planet Money / The Indicator (NPR), Underpinning (Sara Pascoe Business Journal), The Tim Ferriss Show on entrepreneurship.
- **Movies / TV / Documentaries**: use JustWatch UK URLs in the form `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`. JustWatch aggregates "where to watch" so the student lands on a single page that lists Netflix/Amazon/free options. Don't link directly to Netflix/Amazon (region-specific, paywalled).
  - Good Business titles: The Founder (2016, McDonald's), The Social Network (2010), Moneyball (2011), Steve Jobs (2015), Inside Job (2010, financial crisis), The Big Short (2015), Margin Call (2011), The Pursuit of Happyness (2006), Joy (2015), Air (2023, Nike/Jordan), Tetris (2023), Dragons' Den (BBC), The Apprentice UK (BBC), Shark Tank (US), Inside Bill's Brain, Sunderland 'Til I Die, Diary of a CEO (TV adaptation), McMillions, WeWork: Or the Making and Breaking of a $47 Billion Unicorn.
- **Study Tools**: BBC Bitesize topic page, tutor2u, Business Case Studies (businesscasestudies.co.uk), Khan Academy entrepreneurship, the Bank of England's "Knowledge Bank", FT Lex articles (free ones), Companies House, the British Chambers of Commerce site, CIPD for HR topics, MarketingWeek, Marketing Donut, Federation of Small Businesses (FSB) explainer pages. Direct URL to the relevant page, not a homepage.
- **Free YouTube channels for Business**: Two Teachers, tutor2u Business, Geoff Riley (tutor2u), Mr Salles (mostly English but solid), Bbusiness Studies tutor, EconplusDal (cross-over with Econ), CrashCourse Economics, Vox Explained, Bloomberg Quicktake, BBC Reel, FT Film, The Economist YouTube channel.
- **No Wikipedia in primary slots** — Wikipedia is fine as a study tool occasionally but shouldn't be more than 1 of the 6.
- **No Save My Exams, PMT, MME, or other revision-aggregator sites** — banned per pipeline doctrine.
- **No reference to specific past papers, mark schemes, or exam board "model answers"** — that's the copyright moat we're protecting.
- **Tonal match**: items must connect to the LESSON's topic, not just the unit. A "John Lewis ownership model" episode goes on the limited-liability/business-ownership lesson, not the marketing-mix lesson.
- **UK-relevance prefer**: students are British. Where possible, pick UK examples and UK media outlets first; international content is fine if it's the best fit.

## Verification step (mandatory)

For each YouTube URL, run the oembed check before including it. Drop and replace if it fails. For other URLs, sanity-check by reading the URL — does it look like a direct content page? If `?search=` or homepage-like (e.g. `https://www.bbc.co.uk/bitesize`) — replace with a deeper link.

## How to write back

For each lesson in your batch:

1. Read `scripts/_content_business-edexcel/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. **Preserve any existing `related_media` field** — if there's already a "Podcasts" category with a "Lesson Podcast" item (added by the StudyVault podcast generator), DON'T overwrite that item. Add your curated podcasts ALONGSIDE it under the same Podcasts category, with the StudyVault podcast first.
4. Write the JSON back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo the curated content back. Just write to disk and confirm.
