# File Structure

```
Study Vault/
├── CLAUDE.md
├── index.html                ← Subject selection / login / dashboard (SPA)
├── lesson.html               ← Dynamic lesson template (Supabase-driven)
├── browse.html               ← Dynamic browse template (subject/unit index)
├── guide.html                ← Dynamic guide template (exam/revision technique)
├── vercel.json               ← Vercel rewrites for dynamic routes
├── css/style.css             ← All styling
├── js/
│   ├── main.js               ← All JS (Phase 1/2 split for dynamic pages)
│   ├── lesson-loader.js      ← Fetches lesson from Supabase, populates template
│   ├── browse-loader.js      ← Fetches subject/unit data, renders cards
│   └── guide-loader.js       ← Fetches guide pages (exam/revision technique)
├── package.json              ← npm deps (jszip, xml2js, pdf-parse, @supabase/supabase-js, @aws-sdk/client-s3)
├── admin/
│   ├── pipeline.html         ← Content generation pipeline UI
│   ├── review.html           ← QC review page (platform_admin only)
│   ├── images.html           ← Image QA tool (hero images + diagrams with Gemini regen)
│   └── editor.html           ← Block-based content editor for teacher QA
├── api/pipeline/             ← Vercel serverless routes
│   └── _lib/                 ← Shared auth.js, supabase.js
├── supabase/
│   └── migrations/           ← DB schema migrations
├── images/                   ← padlock.svg, subject images, PWA icons
├── fonts/opendyslexic-*/     ← OpenDyslexic woff2/woff
├── history/                  ← 4 units × 15 lessons + exam/revision guides
├── business/                 ← 2 themes × 15 lessons + exam/revision guides
├── geography/                ← 2 papers × 20 lessons + exam/revision guides
├── sport-science/            ← 1 unit × 10 lessons + exam/revision guides
├── drama/                    ← Static backups (content served from Supabase)
├── specs/                    ← Exam board specifications
├── docs/                     ← Pipeline & reference docs
│   ├── DIAGRAM_PIPELINE.md
│   ├── NARRATION_PIPELINE.md
│   ├── LESSON_TEMPLATE.md
│   ├── QUESTIONS_PIPELINE.md
│   ├── RELATED_MEDIA_PIPELINE.md
│   ├── SUBJECT_PLAYBOOK.md
│   ├── GENERATION_PROMPT.md
│   ├── PIPELINE_ARCHITECTURE.md
│   ├── UNIT_THEMES.md
│   ├── FUTURE_FEATURES.md
│   └── FILE_STRUCTURE.md
├── scripts/
│   ├── lib/                  ← Shared Python library (supabase, r2, narration, wikimedia, unsplash, gemini, pipeline)
│   ├── generate_narration.py ← Subject-agnostic TTS narration (--job-id)
│   ├── generate_diagrams.py  ← Subject-agnostic Gemini diagrams (--job-id)
│   ├── download_heroes.py    ← Subject-agnostic hero images (--job-id)
│   ├── pipeline_generate.py  ← CLI helper (info, text, write, status, assets, run-all-assets, review)
│   ├── supabase_writer.py    ← Pipeline adapter (DB writes)
│   └── ...                   ← Legacy/migration/compression scripts
├── tts-research-log.md       ← TTS research (external agents)
├── tech-research-log.md      ← EdTech research (external agents)
└── Spec and Materials/       ← Teacher PPTs (untracked)
```

### Path conventions
- **Dynamic pages** (`lesson.html`, `browse.html`, `guide.html`): absolute paths (`/css/style.css`, `/js/main.js`)
- **Static pages** (legacy HTML files still in repo): relative paths (`../../css/style.css`)
- **URL scheme**: `/lesson/{subject}/{unit}/{number}`, `/browse/{subject}/{unit?}`, `/guide/{subject}/{type}/{slug?}`
