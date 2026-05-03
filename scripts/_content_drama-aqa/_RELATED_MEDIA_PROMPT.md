# AQA Drama — Related Media Curation Prompt

You are curating `related_media` for a small batch of GCSE Drama lessons (AQA 8261). Quality bar high — every URL clicks straight to the content.

## Files to read

1. `docs/RELATED_MEDIA_PIPELINE.md` — full rules
2. The lesson JSONs at `scripts/_content_drama-aqa/lessons/{lesson_slug}.json` for the lessons you're assigned. Write back to each.

## Output schema

```json
"related_media": [
  { "category": "Podcasts", "emoji": "🎙️", "items": [...] },
  { "category": "Videos & Channels", "emoji": "📺", "items": [...] },
  { "category": "Documentaries", "emoji": "🎬", "items": [...] },
  { "category": "Study Tools", "emoji": "🛠️", "items": [...] }
]
```

**EXACT category names** (validator hard-checks):
- `Podcasts`
- `Videos & Channels`
- `Documentaries`
- `Study Tools`

## Hard rules

- **≥6 items per lesson, all 4 categories represented**.
- **Direct links** — not search results, not homepages.
- **YouTube URLs verified via `curl` oembed** before inclusion. **DO NOT use browser MCP tools** — `curl` only via the Bash tool.
- **Podcasts** — link to a SPECIFIC episode.
- **Drama-relevant podcast sources**:
  - BBC R3 Free Thinking (theatre/criticism episodes)
  - BBC R3 Drama on 3 (radio plays)
  - BBC R4 Front Row (theatre reviews)
  - The Stage Podcast
  - Working Class Voices (where relevant — A Taste of Honey, Blood Brothers)
  - National Theatre Conversations / NT Platforms (recorded talks)
  - RSC Podcasts (Romeo and Juliet specifically)
  - Frantic Assembly podcast / Underneath the Radar (physical theatre, Things I Know to Be True)
  - Theatre Voice (London-based theatre interviews)
  - The Almost Maine of Theatre Practitioners — practitioner-focused episodes
- **Movies / TV / Documentaries** (JustWatch UK):
  - The Crucible (1996 film, Daniel Day-Lewis); Witchfinder General (1968 — context for witch hysteria); Good Night, and Good Luck (2005 — McCarthyism)
  - Blood Brothers (1988 BBC production where available; Willy Russell documentaries)
  - Noughts + Crosses (BBC TV adaptation 2020); 13th, Selma, Just Mercy (race/segregation context)
  - Around the World in 80 Days — various film adaptations (1956, 2004); ensemble physical-theatre filmed productions
  - Romeo + Juliet (Luhrmann 1996); Romeo and Juliet (Zeffirelli 1968); Romeo Must Die; West Side Story (1961, 2021)
  - Things I Know to Be True — Frantic Assembly behind-the-scenes recordings (where freely available)
  - A Taste of Honey (Tony Richardson 1961 film); Saturday Night and Sunday Morning; Look Back in Anger (kitchen-sink era)
  - The Great Wave / Indhu Rubasingham interviews
  - The Empress / RSC behind-the-scenes
  - General drama documentaries: Stanislavski (BBC documentary), Brecht (BBC documentary), National Theatre at 50, Inside the National Theatre
- **Free YouTube channels for Drama**:
  - **National Theatre Discover** — practitioner masterclasses, design walkthroughs
  - **NT Education** — set design, performer interviews
  - **RSC Education** — Romeo and Juliet specifically
  - **Frantic Assembly** — physical theatre techniques (especially relevant for Things I Know, Around the World)
  - **TED-Ed** — theatre history talks
  - **Crash Course Theatre** (US-led but accessible)
  - **The School of Life** — practitioner introductions
  - **Globe Theatre** — Shakespeare staging
  - **Donmar Warehouse / Royal Court** education content
- **Study Tools**:
  - BBC Bitesize Drama (per-play topic pages)
  - NT Discover free resources (per-play production resources where available)
  - RSC Education for Romeo and Juliet
  - Frantic Assembly free resource pack — for Things I Know to Be True specifically
  - Drama Online (subscription but free intros)
  - The Stage's archive (free articles)
  - Theatre and Performance Research at universities (free essays)
  - V&A Theatre Collection
- **No Wikipedia in primary slots** (≤1 per lesson, study-tool only).
- **No Save My Exams / PMT / MME / Revision World / Study Mind / Primrose Kitten** — banned.
- **No reproduction** of past papers, mark schemes, or model answers.
- **Tonal match**: items must connect to the LESSON's specific topic (a Stanislavski lesson gets practitioner content, not staging-of-Crucible content). Set-play lessons get play-specific content.
- **UK-relevance preferred** where possible.

## Verification

For every YouTube URL: `curl` oembed before inclusion. Drop and replace if it errors. For other URLs: sanity-check by reading them; replace homepage/search-result URLs with deeper links.

## How to write back

For each lesson:
1. Read `scripts/_content_drama-aqa/lessons/{lesson_slug}.json`
2. Add `related_media` field (preserve all other fields)
3. **Preserve any existing `related_media`** if a "Lesson Podcast" item is already there
4. Write back

## Output

Return only:
```
RELATED_MEDIA_DONE: lessons={N}, files=<comma list>
```

Don't echo content. Just write + confirm.
