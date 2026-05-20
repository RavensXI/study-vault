# Eduqas D&T — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Design and Technology lessons (Eduqas C600QS / WJEC 3600QS — same joint spec). Quality bar: every URL must land directly on the content (a YouTube watch page that plays, a JustWatch page that shows where to stream, a study tool that loads).

**Subject context.** D&T has rich free YouTube content (Engineering Mindset, Make:, Engineering Explained, Practical Engineering) and good documentaries (industrial design, manufacturing, materials). Documentaries category should usually have 1+ items.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules
2. Lesson JSONs at `scripts/_content_design-technology-eduqas/lessons/{lesson_slug}.json`

## Output schema

Supabase already has a Podcasts category — merge script preserves it. **DO NOT** include Podcasts. Output four categories:

```json
"related_media": [
  { "category": "Videos & Channels", "emoji": "📺", "items": [...] },
  { "category": "Documentaries", "emoji": "🎬", "items": [...] },
  { "category": "Study Tools", "emoji": "🛠️", "items": [...] },
  { "category": "Articles & Web", "emoji": "📰", "items": [...] }
]
```

## Hard rules

- **≥6 items per lesson** across the 4 categories
- **Every YouTube URL oembed-verified** before inclusion: `curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"` — must return 200+JSON. NEVER trust HEAD.
- Movies/TV/Docs: JustWatch UK only — `https://www.justwatch.com/uk/movie/{slug}` or `https://www.justwatch.com/uk/tv-show/{slug}`
- No banned aggregators (Save My Exams, PMT, MME, Primrose Kitten, Study Mind)
- No spec codes ("C600QS", "3600QS") in titles/descriptions
- No "Eduqas" or "WJEC" board name in prose (dual-board subject — use "GCSE Design and Technology")

## Strong free YouTube sources for D&T

- **Engineering Mindset** — clear materials, mechanisms, manufacturing
- **Practical Engineering** — civil/mechanical engineering deep dives
- **Engineering Explained** — for mechanical systems
- **Real Engineering** — design + materials docs
- **Make: Magazine** — maker culture, prototyping
- **NYU's CIW (Big Things)** — manufacturing/industrial
- **Mark Rober** — engineering creativity (occasional fit)
- **Veritasium** — for materials + physics-of-engineering
- **TED-Ed Design and Technology playlist**
- **Smarter Every Day** — engineering investigations
- **Adam Savage's Tested** — workshop techniques, prototyping

## Strong study tools

- **BBC Bitesize D&T**: `https://www.bbc.co.uk/bitesize/subjects/zdh4r82`
- **Technology Student** (`https://www.technologystudent.com/`) — old but comprehensive UK D&T resource
- **Eduqas teaching support**: `https://www.eduqas.co.uk/qualifications/design-and-technology/`
- **Design Museum London** education pages
- **Khan Academy Engineering**
- **Tinkercad / Onshape free tiers** for CAD lessons

## Documentaries that fit D&T (use where genuinely relevant)

- **Abstract: The Art of Design (Netflix, multi-season)** — every episode is a famous designer (Ive, Sagmeister, etc). JustWatch UK.
- **Objectified (2009)** — Gary Hustwit doc on industrial design
- **Helvetica (2007)** — typography/design history
- **The True Cost (2015)** — fashion industry impact (textile lessons)
- **River Blue (2017)** — fashion industry water pollution
- **Plastic China (2016)** — recycling/sustainability
- **A Plastic Ocean (2016)** — sustainability lessons
- **The Story of Plastic (2019)**
- **Saving Capitalism / Inside Job** — only if lesson covers ethics in design
- **The Founder (2016)** — McDonald's industrial systems thinking, lots of D&T angles

## Articles & Web

- **Dezeen** — design industry news, deep articles
- **Designboom** — same
- **Core77** — industrial design articles
- **Wallpaper magazine**
- **The Design Council** UK
- **WRAP** for sustainability
- **The Daily Mail / Guardian Design** sections
- Wikipedia max 1 per lesson

## Verification step (mandatory)

For each YouTube URL: run oembed BEFORE including. Drop and replace failures.
For other URLs: deep content links only, not search/homepage.

## How to write back

1. Read `scripts/_content_design-technology-eduqas/lessons/{lesson_slug}.json`
2. Add `related_media` field (preserve all other fields)
3. Write JSON back via Write tool

Do NOT include a Podcasts category — merge script preserves it.

## Output

`RELATED_MEDIA_DONE: lessons={N}` plus notes on any URL drops.
