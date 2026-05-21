# Sport Studies — Related Media Curation Prompt

You are curating `related_media` for a small batch of Sport Studies lessons (Cambridge National qualification on contemporary issues in sport). Quality bar is high: students should be able to **click any link and immediately reach the content**.

Subject context: this is a **vocational Level 1/Level 2 qualification** focused on small UK start-ups. Content choices should suit that audience — practical, founder-led, accessible — and not lean academic. Avoid theoretical economics-podcast picks and prefer founder stories, small-business podcasts, and how-to videos.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_cambridge-nationals-sport-studies/lessons/{lesson_slug}.json` for the lessons you're assigned

## Output schema

For each lesson in your batch, ADD a `related_media` field. Use these EXACT category names — the verifier requires them:

```json
"related_media": [
  {
    "category": "Videos & Channels",
    "emoji": "📺",
    "items": [
      { "title": "...", "description": "...", "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ]
  },
  {
    "category": "Documentaries",
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
  },
  {
    "category": "Articles & Web",
    "emoji": "📰",
    "items": [
      { "title": "...", "description": "...", "url": "https://..." }
    ]
  }
]
```

Note: a separate Podcasts category will be added LATER by the NotebookLM podcast generator. Do NOT add Podcasts here — the generator inserts it.

## Hard rules

- **Each lesson: ≥6 items total** spread across the 4 categories. At least 1 in each of Videos & Channels and Study Tools. Documentaries and Articles & Web are encouraged but can be 0 if nothing fits.
- **Every URL must be clickable** and land on the content — not a search results page, not a homepage.
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each via oembed before including:**
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  If oembed returns non-200 or an error, the video is private/deleted/region-locked — drop it. **NEVER use HEAD requests** — YouTube returns 200 even for dead videos. Agents have historically hallucinated YouTube IDs at ~20% — assume every URL is suspect until oembed-verified.
- **Documentaries**: use JustWatch UK URLs in the form `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`. Don't link directly to Netflix/Amazon.
- **Study Tools**: BBC Bitesize topic page, tutor2u, Companies House, British Chambers of Commerce, Federation of Small Businesses (FSB), gov.uk small business resources, MarketingWeek, Marketing Donut, MoneySavingExpert (for personal-finance / risk lessons), Khan Academy entrepreneurship.
- **Articles & Web**: BBC News business section, The Guardian small business, FT entrepreneurs section (free articles), Forbes UK, Startup Magazine, Real Business, Smallbusiness.co.uk. Deep links to specific articles, not homepages. Wikipedia max 1 per lesson.

## Strong YouTube channels for Sport Studies

- **Two Teachers** (UK business / Cambridge Nationals friendly)
- **tutor2u Business** (Geoff Riley)
- **Mr Roberts Business Studies**
- **Bbusiness Studies tutor**
- **The Diary of a CEO** clips on YouTube (founder stories)
- **Vox Explained**, **Wendover Productions** for accessible business explainers
- **Bloomberg Originals / Quicktake**
- **CNBC Make It** (entrepreneurship)
- **TED-Ed** business clips
- **CrashCourse Entrepreneurship**

## Documentaries / films that fit Sport Studies

- *The Founder* (2016) — McDonald's franchising (great for L7 marketing mix / L11 franchise)
- *The Social Network* (2010) — start-up dynamics (great for L1 entrepreneur characteristics / L2 risk/reward)
- *Joy* (2015) — solo founder, Miracle Mop
- *The Pursuit of Happyness* (2006)
- *Air* (2023) — Nike's Air Jordan launch (marketing mix)
- *Tetris* (2023) — small-deal entrepreneurship
- *Steve Jobs* (2015)
- *Dragons' Den* (BBC) — pitching, ownership, finance (great for L1, L11)
- *The Apprentice UK* (BBC)
- *Shark Tank* (US)
- *Inside Bill's Brain*
- *McMillions* (marketing fraud — only relevant peripherally)
- *WeWork: Or the Making and Breaking of a $47 Billion Unicorn*

## Lesson-topic mapping cheat sheet

- L1 Entrepreneur characteristics → Diary of a CEO founder stories, Dragons' Den, The Social Network
- L2 Risk/reward → Pursuit of Happyness, Joy, BBC Reel founder docs
- L3 Market research → tutor2u "primary vs secondary research", BBC Bitesize segments
- L4 Segmentation → tutor2u, MarketingWeek segmentation explainers
- L5 Costs/revenue/profit → tutor2u, MoneySavingExpert small business
- L6 Break-even/cash → tutor2u break-even, Companies House cash-flow guides
- L7 Marketing mix (4Ps) → tutor2u 4Ps, The Founder (franchise/branding)
- L8 Advertising/promotion → MarketingWeek case studies, Vox "branding" explainers
- L9 Channels/lifecycle → tutor2u product lifecycle, BBC Bitesize
- L10 Pricing → MoneySavingExpert pricing strategy, Vox pricing explainers
- L11 Ownership/capital → Companies House, FSB, Dragons' Den investment pitches
- L12 Support → FSB, British Chambers of Commerce, gov.uk start-a-business

## Hard prohibitions

- **No Save My Exams, PMT, MME, Primrose Kitten, Study Mind**
- **No spec codes** ("J829", "R067", "R068", "R069") in titles/descriptions
- **No "OCR" / "Pearson" / "Edexcel" / "Cambridge Nationals"** in user-facing strings
- **No Wikipedia in primary slots** — max 1 per lesson

## Verification step (mandatory)

For each YouTube URL: run the oembed check BEFORE including. For other URLs: sanity-check by reading the URL — does it look like a direct content page or a homepage/search? Replace homepages with deep links.

## How to write back

For each lesson in your batch:

1. Read `scripts/_content_cambridge-nationals-sport-studies/lessons/{lesson_slug}.json`
2. ADD a `related_media` field to the JSON (preserve all other fields)
3. Write JSON back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo the curated content back. Just write to disk and confirm.
