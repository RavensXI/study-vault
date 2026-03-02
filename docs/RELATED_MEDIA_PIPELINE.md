# Related Media Pipeline — Curating Sidebar Content

> **API Integration:** This document is read by the orchestration code and injected into the Claude API call for related media curation. The Related Media prompt section below is sent as the system prompt.

Subject-agnostic process for populating the Related Media sidebar on lesson pages. The goal is to give students genuinely enjoyable content that reinforces learning without feeling like revision.

---

## Overview

Every lesson has a Related Media section in the sidebar with curated links to external content — podcasts, videos, movies, TV shows, documentaries, and study tools. The key principle: **recommend things students might actually enjoy** that happen to be relevant to the topic. A student watching a documentary about the Treaty of Versailles is revising without realising it.

---

## The Process

### Step 1: Spin up research agents (one per lesson)

Launch parallel agents, each assigned a single lesson. The agent's brief:

- **Read the lesson content** to understand the specific topics covered
- **Search for related media** across all categories (see below)
- **Prioritise engaging, accessible content** — things a 15–16 year old would actually watch/listen to
- **Return structured results** with title, URL, and a one-line description explaining the relevance

Agent prompt template:

```
You are researching related media for a GCSE [Subject] lesson on "[Lesson Title]".

The lesson covers: [brief topic summary]

Find engaging external content that students aged 15-16 might enjoy, across these categories:
1. Podcasts — episodes from established podcasts (Spotify, Apple Podcasts, BBC Sounds, NPR)
2. YouTube videos or channels — educational but engaging content creators
3. Movies — feature films related to the topic (use JustWatch UK URLs)
4. TV Shows — series related to the topic (use JustWatch UK URLs)
5. Documentaries — factual programmes (use JustWatch UK URLs)

Guidelines:
- Content should be tangentially relevant at minimum — it doesn't need to be exam-focused
- Prefer UK-accessible content where possible
- For podcasts, link to specific episodes (not just the show)
- For movies/TV/docs, use JustWatch UK (justwatch.com/uk/) so students can find where to stream
- Max 3 items per category — quality over quantity
- Skip any category where nothing genuinely good exists
- Include a one-line description that explains WHY this is relevant to the lesson

Return results in this format:
Category: [category name]
- Title | URL | Description
```

### Step 2: Review and curate

Not everything agents find will be suitable. Check for:

- **Broken or paywalled links** — agents sometimes hallucinate URLs, especially for podcasts
- **Age appropriateness** — some documentaries or movies may not be suitable for 15–16 year olds
- **Genuine relevance** — a tangential connection is fine, but it should still make sense
- **UK accessibility** — prefer content available on UK streaming platforms

### Step 3: Build the HTML

Insert into the lesson's `<aside class="lesson-sidebar">`, after Knowledge Check and before Video (if present).

---

## Category Order

Always follow this order. Omit any category that has no items.

1. **Lesson Podcast** — audio revision for this specific lesson (if narration exists)
2. **Podcasts** — specific episodes from established podcast series
3. **Videos & Channels** — YouTube creators or specific videos
4. **Movies** — feature films
5. **TV Shows** — series
6. **Documentaries** — factual programmes
7. **Study Tools** — always last (BBC Bitesize, Seneca, NotebookLM, official spec pages, etc.)

---

## HTML Structure

### Container

```html
<div class="sidebar-section sidebar-media">
  <div class="sidebar-section-title">Related Media</div>

  <!-- Categories go here, in order -->

</div>
```

### Category (collapsible)

```html
<div class="sidebar-collapsible">
  <button class="sidebar-collapsible-toggle" aria-expanded="false">
    <span>EMOJI Category Name</span>
    <svg class="sidebar-collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  </button>
  <div class="sidebar-collapsible-content">

    <!-- Items go here -->

  </div>
</div>
```

### Item (link)

```html
<a href="URL" target="_blank" rel="noopener noreferrer" class="sidebar-media-item">
  <strong>Title</strong>
  <span>One-line description explaining relevance</span>
</a>
```

All links open in a new tab (`target="_blank" rel="noopener noreferrer"`).

---

## Category Emojis

| Category | Emoji | HTML Entity |
|----------|-------|-------------|
| Lesson Podcast | &#127897; | `&#127897;` |
| Podcasts | &#127911; | `&#127911;` |
| Videos & Channels | &#127909; | `&#127909;` |
| Movies | &#127916; | `&#127916;` |
| TV Shows | &#128250; | `&#128250;` |
| Documentaries | &#127909; | `&#127909;` |
| Study Tools | &#128218; | `&#128218;` |

---

## Link URL Conventions

| Content Type | URL Source |
|-------------|-----------|
| Podcasts | Specific episode URL from Spotify, Apple Podcasts, BBC Sounds, or NPR |
| YouTube | Full video or channel URL (`youtube.com/watch?v=` or `youtube.com/@channel`) |
| Movies | JustWatch UK: `justwatch.com/uk/movie/slug` |
| TV Shows | JustWatch UK: `justwatch.com/uk/tv-series/slug` |
| Documentaries | JustWatch UK: `justwatch.com/uk/movie/slug` |
| Study Tools | Direct URL to the resource (BBC Bitesize, Seneca, exam board spec page, etc.) |

JustWatch is preferred for movies/TV/docs because it shows students where to stream content across all UK platforms, rather than linking to a single service they might not have.

---

## Guidance Per Category

### Podcasts
- Link to **specific episodes**, not the show homepage
- Include the show name and episode topic in the title: "How I Built This — Dyson: James Dyson"
- Description should explain relevance: "5,127 prototypes before launching — a case study in risk-taking"
- Good sources: BBC Radio 4, History Extra, NPR's How I Built This, In Our Time, specific subject podcasts

### Videos & Channels
- Can be specific videos or entire channels that cover the subject well
- YouTube revision channels are good here (e.g. "Two Teachers — Business")
- Include estimated duration for specific videos in the description

### Movies & TV Shows
- The connection can be tangential — a WWI movie is relevant to a lesson on the Treaty of Versailles even if it doesn't cover the treaty directly
- Include the year in the title: "Testament of Youth (2014)"
- Description should bridge the connection: "Vera Brittain's WWI memoir — the war that drove demands for peace"

### Documentaries
- Same JustWatch linking as movies
- BBC documentaries are particularly good for UK students
- Include the presenter/director if well-known: "Peter Jackson's colourised WWI footage"

### Study Tools
- Always the last category
- BBC Bitesize pages for the specific topic
- Official exam board specification/past papers page
- Seneca Learning, NotebookLM, or other free revision platforms
- This is the "boring but useful" category — keep it short (1–2 items)

---

## Lesson Podcast Handling

The Lesson Podcast links to audio narration of the lesson content. How it appears depends on narration status:

- **Narration exists** (e.g. Spotify-hosted): Lesson Podcast is its own collapsible category with a real URL
- **Narration planned but not yet recorded**: Lesson Podcast appears inside the Podcasts category with `href="#"` as placeholder
- **No narration planned**: Omit the Lesson Podcast entry entirely

---

## Items Per Category

- **Max 3 items per category** — quality over quantity
- **Min 0** — omit the entire category if nothing good exists
- **Typical total per lesson**: 4–9 items across all categories
- Not every lesson will have movies or TV shows — that's fine, only include what genuinely fits

---

## What Makes Good Related Media

**Include:**
- Content a student might watch/listen to for fun and incidentally learn something
- Real-world examples that bring abstract concepts to life
- Content from trusted sources (BBC, established podcasters, well-reviewed films)
- Content available free or on common UK streaming platforms

**Avoid:**
- Dry, lecture-style content that feels like homework
- Content behind expensive paywalls
- Anything age-inappropriate (certificate 18 films, graphic content)
- Links that are likely to break (temporary URLs, social media posts)
- Stuffing categories just to fill them — empty is better than irrelevant
