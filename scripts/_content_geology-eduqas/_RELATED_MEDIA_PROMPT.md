# Eduqas Geology — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Geology lessons (Eduqas C180QS / WJEC 3180QS — joint spec). Quality bar: every URL must land directly on the content.

**Subject context.** Geology is well-served by free YouTube content (GeologyHub, Practical Engineering, Real Science, Nick Zentner lectures) and has excellent documentaries (BBC Earth, Attenborough's Planet series, Volcano docs). Documentaries category should be populated on most lessons — geology and its history are a natural documentary subject.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md`
2. Lesson JSONs at `scripts/_content_geology-eduqas/lessons/{lesson_slug}.json`

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
- **Every YouTube URL oembed-verified**: `curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"` — 200+JSON required. NEVER trust HEAD.
- Movies/TV/Docs: JustWatch UK only
- No banned aggregators (Save My Exams, PMT, MME, Primrose Kitten, Study Mind)
- No spec codes ("C180QS", "3180QS")
- No "Eduqas"/"WJEC" in prose (dual-board — use "GCSE Geology")

## Strong free YouTube sources

- **GeologyHub** — short clear geological process explainers
- **Nick Zentner** — university-level geology lectures, accessible
- **Practical Engineering** — civil/geotechnical engineering crossover for hazards/resources lessons
- **Real Science / RealLifeLore** — accessible Earth science
- **Be Smart (PBS)** — geology and Earth science episodes
- **MinuteEarth / MinutePhysics** — short concept explainers
- **SciShow / SciShow Space** — solar system + geological topics
- **The History Guy** for geology history (Hutton, Lyell)
- **BBC Earth** YouTube channel — wildlife adjacent but useful geological footage
- **Earth Science WA** (Australian) — clean tectonics + minerals content
- **Geology Hub** — different to GeologyHub, also good
- **The Bay Area Geology channel** — California faults/quakes

## Strong study tools

- **BBC Bitesize** — limited but useful coverage
- **Eduqas teaching support**: `https://www.eduqas.co.uk/qualifications/geology/`
- **Earthlearningidea** (`https://www.earthlearningidea.com/`) — free geology teaching activities
- **British Geological Survey** education pages (`https://www.bgs.ac.uk/discovering-geology/`)
- **The Open University** OpenLearn geology courses (free)
- **USGS** (US Geological Survey) — `https://www.usgs.gov/` deep links
- **Geology.com** — articles + minerals reference
- **Mindat.org** — comprehensive mineral database

## Documentaries that fit Geology (use generously)

- **Planet Earth (BBC, 2006)** — multi-episode, geological themes throughout
- **Planet Earth II (BBC, 2016)** + **Planet Earth III (2023)**
- **Frozen Planet (BBC, 2011)** — for climate/ice lessons
- **Frozen Planet II (BBC, 2022)**
- **Blue Planet II (BBC, 2017)** — ocean geology + climate
- **A Perfect Planet (BBC, 2021)** — natural forces, volcanoes, weather
- **Earth: One Amazing Day (2017)**
- **Volcano (1997)** + **Dante's Peak (1997)** — hazard lessons (drama, not doc, but fits JustWatch)
- **Pompeii** docs — for volcanic hazards
- **Earthquake (1974)** — disaster movie, JustWatch
- **Werner Herzog's Into the Inferno (2016)** — volcano documentary
- **Fire of Love (2022)** — volcanologists Katia and Maurice Krafft
- **The Day The Earth Nearly Died** (BBC) — Permian extinction
- **The Whole Story (BBC)** — geology history
- **Walking with Dinosaurs (BBC, 1999)** — for fossils + geological time
- **When Worlds Collide** docs — solar system formation

## Articles & Web

- **The Geological Society of London** (`https://www.geolsoc.org.uk/`)
- **British Geological Survey news + articles**
- **The Conversation** geology section
- **Smithsonian Magazine** geology articles
- **National Geographic** geology pieces
- **The Guardian** science pages
- Wikipedia max 1 per lesson

## Verification step (mandatory)

For each YouTube URL: run oembed BEFORE including.
For non-YouTube URLs: deep content links only, not search/homepage.

## How to write back

1. Read `scripts/_content_geology-eduqas/lessons/{lesson_slug}.json`
2. Add `related_media` field (preserve all other fields)
3. Write JSON back via Write tool

## Output

`RELATED_MEDIA_DONE: lessons={N}` plus URL drop notes.
