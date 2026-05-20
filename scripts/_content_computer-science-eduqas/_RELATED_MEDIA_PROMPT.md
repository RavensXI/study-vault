# Eduqas Computer Science — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Computer Science lessons (Eduqas C500QS / WJEC 3500QS — same joint spec, no Welsh content). Quality bar: students should be able to **click any link and land directly on the content** (a YouTube watch page that plays, a JustWatch page that shows where to stream, a study tool that loads).

**Subject context.** CS is well-served by free YouTube channels (Crash Course CS, Ben Eater, Computerphile, Tom Scott on networking topics, etc.) and there ARE good documentaries (computing history, hacking, the internet) — fewer "0 items in Documentaries" results here than for fundamentals-style subjects.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules
2. The lesson JSONs at `scripts/_content_computer-science-eduqas/lessons/{lesson_slug}.json` for your assigned lessons. You'll write back to each.

## Output schema

The Supabase row already contains a `Podcasts` category with a `Lesson Podcast` entry (parallel pipeline). The merge script preserves that — **DO NOT** include a Podcasts category. Output four categories:

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

## Hard rules

- **Each lesson: ≥6 items total**, spanning all four categories where you can (Documentaries can be empty `[]` only if no genuine fit — but for most CS topics there IS one).
- **Every URL must be clickable** and land on the actual content — not a search page, not a homepage.
- **YouTube URLs**: `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each with oembed**:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  200 + JSON → keep. 404/401 → drop and replace. **DO NOT use HEAD requests** — YouTube returns 200 even for dead videos.
- **Movies / TV / Docs**: JustWatch UK only — `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`.
- **No banned aggregators**: Save My Exams, Physics & Maths Tutor (PMT), MME, Primrose Kitten, Study Mind.
- **No spec codes** in titles or descriptions ("Eduqas CS C500QS" — never).
- **No "Eduqas" or "WJEC"** in titles/descriptions (this is a dual-board subject — use "GCSE Computer Science").

## Strong free YouTube sources for CS

- **Crash Course Computer Science** (Carrie Anne Philbin) — gold standard, 40 episodes covering most of GCSE CS
- **Ben Eater** — exceptional for hardware, networking (he has whole series on TCP/IP, Ethernet, networking from scratch), CPU internals, RAM
- **Computerphile** — Brady Haran's CS channel — Tom Scott, David Brailsford, others — broad topics including algorithms, security, cryptography, network protocols
- **Tom Scott** — networking and internet topics specifically: cookies, DNS, HTTPS
- **Real Engineering** — solid hardware and history pieces
- **3Blue1Brown** — algorithms and computational complexity (his algorithm visualisations are excellent)
- **CS Dojo** — beginner Python programming
- **Mr. Bit** — UK-focused GCSE CS exam revision channel

## Strong study-tool sources for CS

- **BBC Bitesize Computer Science** (`https://www.bbc.co.uk/bitesize/subjects/z34k7ty`) — good baseline GCSE coverage
- **Teach-ICT** (`https://www.teach-ict.com/`) — UK GCSE CS-focused
- **Eduqas teaching support** (`https://www.eduqas.co.uk/qualifications/computer-science/`)
- **Codecademy Python free tier** for programming-focused lessons
- **CS Field Guide** (`https://www.csfieldguide.org.nz/en/`) — university-style but accessible
- **Logic.ly demo** (`https://logic.ly/demo`) — in-browser logic gate simulator
- **CircuitVerse** (`https://circuitverse.org/`) — logic circuit simulator (for the logic-gates lessons)
- **Khan Academy Algorithms** (`https://www.khanacademy.org/computing/computer-science/algorithms`)

## Articles & Web suggestions

- **GeeksforGeeks** (`https://www.geeksforgeeks.org/`) — for algorithm and data structure topics; deep, free, well-explained
- **TutorialsPoint** for various CS topics
- **The Internet Society** for networking history
- **NCSC (UK National Cyber Security Centre)** explainers for cybersecurity lessons
- **Information Commissioner's Office (ICO)** for Data Protection Act / UK GDPR content
- Wikipedia is fine sparingly (max 1 per lesson)

## Documentaries — actually possible here

CS has genuine documentary options. Match to topic:
- **The Imitation Game (2014)** — Turing, WWII computing
- **General Magic (2018)** — early iPhone-prefigure
- **Halt and Catch Fire (TV, AMC, 2014–17)** — fictional but very accurate 1980s-90s PC industry, JustWatch
- **The Social Dilemma (2020)** — social media + algorithms
- **Inside Bill's Brain (2019 Netflix doc series)** — Bill Gates / Microsoft
- **Citizenfour (2014)** — Snowden, privacy/surveillance (for ethics lessons)
- **The Great Hack (2019)** — Cambridge Analytica, data ethics (for ethics lessons)
- **Lo and Behold: Reveries of the Connected World (2016, Werner Herzog)** — internet history
- For programming topics, fewer doc options — leave `[]` if no genuine fit.

## Verification step (mandatory)

For each YouTube URL: run oembed BEFORE including. Drop and replace failures.
For other URLs: sanity-check the URL — does it look like a direct content page? Replace homepages with deeper links.

## How to write back

For each lesson in your batch:
1. Read `scripts/_content_computer-science-eduqas/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. Write the JSON back to the same path

Do NOT include a Podcasts category — the merge script preserves the existing Podcasts entry from Supabase.

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}
```
plus a brief note on any YouTube IDs you had to drop and replace.
