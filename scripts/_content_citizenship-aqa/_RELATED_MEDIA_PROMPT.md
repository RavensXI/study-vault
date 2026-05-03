# AQA Citizenship Studies — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Citizenship Studies lessons (AQA 8100). Quality bar is high: every URL must take a student straight to the content (a YouTube watch page that plays, a podcast episode page that plays, a study tool that loads). The single exception is Movies/TV/Documentaries — JustWatch UK aggregator pages.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full pipeline rules
2. The lesson JSONs at `scripts/_content_citizenship-aqa/lessons/{lesson_slug}.json` for the lessons you're assigned. Write back to each.

## Output schema

For each lesson, ADD a `related_media` field to its lesson JSON:

```json
"related_media": [
  { "category": "Podcasts", "emoji": "🎙️", "items": [...] },
  { "category": "Videos & Channels", "emoji": "📺", "items": [...] },
  { "category": "Documentaries", "emoji": "🎬", "items": [...] },
  { "category": "Study Tools", "emoji": "🛠️", "items": [...] }
]
```

**EXACT category names** (validator hard-checks these — don't paraphrase):
- `Podcasts`
- `Videos & Channels`
- `Documentaries`
- `Study Tools`

## Hard rules

- **Each lesson: ≥6 items total**, spanning all 4 categories (≥1 each).
- **Every URL clickable + direct** (not search results, not homepages).
- **YouTube URLs** verified via `curl` oembed BEFORE inclusion:
  ```
  curl -s "https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3DVIDEO_ID&format=json"
  ```
  Drop and replace if oembed errors. **DO NOT** use HEAD requests — YouTube returns 200 for deleted videos.
- **DO NOT use browser MCP tools** for verification. Use `curl` via the Bash tool only — browser MCP opens a visible Chrome window that interrupts the user's terminal.
- **Podcasts**: link to a SPECIFIC episode on Spotify, Apple Podcasts, or YouTube.
  - Good citizenship-relevant sources: BBC The Today Podcast (politics), BBC Politics Weekly UK (Guardian collab — careful with editorial line, prefer guests-on-the-issue episodes), Reasons to be Cheerful (Ed Miliband + Geoff Lloyd — careful editorial), The Rest Is Politics (Stewart/Campbell — paired bias-balance is the format's selling point), History of Parliament Podcast, BBC In Our Time (constitution, suffrage, Magna Carta, civil rights), The Bunker, Policy Exchange podcast, Hansard Society podcasts, Political Thinking with Nick Robinson, Newscast (BBC), The Spectator Edition, More or Less (BBC R4 — for media literacy / use-of-data lessons), Beyond the Headlines, BBC Witness History (suffrage, Hillsborough, civil rights moments).
- **Movies / TV / Documentaries** (JustWatch UK):
  - Iron Lady (2011), Suffragette (2015), Made in Dagenham (2010), Pride (2014), I, Daniel Blake (2016), Bend It Like Beckham (2002), Blue Story (2019), Selma (2014), Just Mercy (2019), Hidden Figures (2016), 13th (2016), The Trial of the Chicago 7 (2020), Mrs America (2020 series), The Crown (Netflix — constitution/monarchy episodes), Yes Minister / Yes Prime Minister, Brexit: The Uncivil War (2019), Years and Years (2019 series), Adolescence (2025 — youth crime/social media), The Responder (BBC police drama), Line of Duty (BBC).
  - Documentaries: 13th (Ava DuVernay), The Big Steal: Climate Crime (Netflix), He Named Me Malala (2015), An Inconvenient Truth (2006), Inside the Foreign Office (BBC), Inside Parliament documentaries (BBC), Hillsborough (1996 / 2016), Stephen Lawrence: Has Britain Changed? (BBC).
- **Study Tools**: Parliament UK education site (parliament.uk/education — deep links), BBC Bitesize Citizenship topic pages (deep links to the specific topic), gov.uk explainer pages (e.g. on rights, voting, citizenship), the Hansard Society's Mock Elections resources, UK Youth Parliament site, the Magistrates' Association's school resources, Liberty's rights explainer pages, Amnesty UK education resources, the Equality and Human Rights Commission, the UN Human Rights site (UDHR explainers).
- **Free YouTube channels for citizenship**:
  - **TLDR News UK** — UK politics explainers (high-quality, mostly even-handed)
  - **The Whiteboard** (BBC) — explainers on UK political mechanics
  - **Kurzgesagt** — has democracy / human rights explainers
  - **CGP Grey** — voting systems, parliamentary mechanics, gerrymandering
  - **TED-Ed** — civic engagement, voting, human rights talks
  - **PolicyEd / Hoover Institution** — careful, US-conservative-leaning; use sparingly
  - **History Hit** — citizenship-relevant history (suffrage, constitution)
  - **BBC Reel** — short civic-themed explainers
  - **Crash Course Government & Politics** (US-focused but useful for comparative)
  - **Channel 4 News** — explainer videos on UK political topics
  - **PoliticsJOE** — youth-oriented UK politics; good for engagement-pattern lessons
- **Citizenship-specific impartiality**: when picking podcasts/channels with editorial line, balance perspectives across a lesson AND across the whole subject. Don't load 6 lessons with only one editorial bias. Prefer source variety. Use BBC and academic sources where possible — they have built-in impartiality requirements.
- **No Wikipedia in primary slots** (≤1 per lesson, study-tool category only).
- **No Save My Exams / PMT / MME / Revision World / Study Mind / Primrose Kitten** — banned.
- **No reproduction** of past papers, mark schemes, model answers.
- **Tonal match**: items must connect to the LESSON's specific topic, not just the unit.
- **UK-relevance preferred** (this is a UK civics subject — UK content first, international as comparison).

## Verification step (mandatory)

Run `curl` oembed for every YouTube URL before inclusion. Sanity-check other URLs by reading them — `?search=` or homepage = replace with deeper link.

## How to write back

For each lesson:
1. Read `scripts/_content_citizenship-aqa/lessons/{lesson_slug}.json`
2. Add `related_media` field (preserve all other fields)
3. **Preserve any existing `related_media`** — don't overwrite a "Lesson Podcast" item if present
4. Write back to the same path

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo curated content. Just write + confirm.
