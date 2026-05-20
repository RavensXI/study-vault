# Eduqas Electronics — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Electronics lessons (Eduqas C490QS / WJEC 3490QS — same joint spec). Quality bar: students should be able to **click any link and land directly on the content** (a YouTube watch page that plays, a JustWatch page that shows where to stream, a study tool that loads).

**Subject context.** Eduqas/WJEC Electronics is a tiny GCSE — almost no dedicated documentaries or films exist. Lean Videos + Study Tools heavy; Movies/TV/Docs is the hardest category — pick adjacent technology/computing/history docs where genuinely relevant, not forced fits.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules (read fully)
2. The lesson JSONs at `scripts/_content_electronics-eduqas/lessons/{lesson_slug}.json` for the lessons you're assigned. You'll write back to each.

## Output schema

For each lesson in your batch, ADD a `related_media` field to its lesson JSON. The Supabase row will already contain a `Podcasts` category with a `Lesson Podcast` entry (added by a parallel pipeline) — that gets merged in at insert time, so **DO NOT** include the Podcasts category yourself. Output four categories:

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

- **Each lesson: ≥5 items total**, spanning ALL FOUR categories (Documentaries minimum 1 if you can find one, otherwise 0 — don't force fits).
- **Every URL must be clickable** and take the student straight to the content — not a homepage, not a search.
- **YouTube URLs** must be `https://www.youtube.com/watch?v=VIDEO_ID` or `https://youtu.be/VIDEO_ID`. **Verify each** with the oembed endpoint:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  Returns 200 + JSON → keep. 404/401 → drop and replace.
  **DO NOT use HEAD requests** — YouTube returns 200 even for dead videos.
- **Movies / TV / Docs**: use JustWatch UK URLs only: `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`.
- **No banned aggregators**: Save My Exams, Physics & Maths Tutor (PMT), MME, Primrose Kitten, Study Mind — all banned per pipeline doctrine.
- **Tonal match**: items must connect to the LESSON's topic, not just the unit. The 555 timer lesson gets a video on monostable/astable circuits; the op-amp lesson gets a video on inverting/non-inverting configurations.

## Strong free YouTube sources for Electronics

- **GreatScott!** — general circuit tutorials, beginner-friendly
- **ElectroBOOM** — entertaining demos of components and circuit failures
- **All About Electronics** — clean walkthroughs of op-amps, transistors, BJTs
- **Afrotechmods** — older but very high-quality electronics fundamentals
- **EEVblog (Dave Jones)** — pro-level but accessible for many topics
- **Ben Eater** — exceptional for digital logic, flip-flops, counters, 555 timers
- **CircuitBread / Computerphile** — for theory and history

## Strong study-tool sources for Electronics

- **BBC Bitesize** (limited Electronics coverage — usually under Physics/D&T)
- **CircuitVerse** (`https://circuitverse.org/`) — free in-browser digital logic simulator
- **Falstad Circuit Simulator** (`https://www.falstad.com/circuit/`) — interactive analogue simulator
- **All About Circuits** (`https://www.allaboutcircuits.com/textbook/`) — free textbook chapters
- **Eduqas Electronics teaching support** (`https://www.eduqas.co.uk/qualifications/electronics/`)
- **PIC microcontroller datasheets / Microchip resources** for microcontroller lessons
- **Khan Academy Electrical Engineering** (`https://www.khanacademy.org/science/electrical-engineering`)

## Articles & Web suggestions

- **Electronics Tutorials** (`https://www.electronics-tutorials.ws/`) — solid free explainers per topic
- **SparkFun Learn** (`https://learn.sparkfun.com/tutorials`) — practical maker articles
- **Adafruit Learn** for project-style applications
- Wikipedia is fine sparingly (max 1 per lesson; better as Articles & Web than Study Tools)

## Documentaries — limited options, don't force

For Electronics-adjacent docs, candidates worth considering when the lesson is microcontroller / digital / systems-thinking flavoured:
- **General Magic (2018)** — early Apple/iPhone-prefigure documentary, on JustWatch
- **The Imitation Game (2014)** — Turing, computing history. JustWatch.
- **Computer History Museum talks on YouTube** — counts as Videos & Channels not Docs.
- For analogue / electronics lessons specifically: there's often **no good documentary** — leave the Documentaries category with 0 items rather than fabricate.

## Verification step (mandatory)

For each YouTube URL: run oembed BEFORE including. Drop and replace failures.
For other URLs: sanity-check the URL — does it look like a direct content page? If you see `?search=` or it looks like a top-level homepage, replace with a deeper link.

## How to write back

For each lesson in your batch:
1. Read `scripts/_content_electronics-eduqas/lessons/{lesson_slug}.json`
2. Add the `related_media` field to the JSON object (preserve all other fields)
3. Write the JSON back to the same path

Do NOT include a Podcasts category — the parallel pipeline owns that. Insert script will merge.

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```
