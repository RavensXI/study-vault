# Highlight Mode — Claude Designer kit

Self-contained reference bundle for producing marketing assets (social videos, launch graphics, carousel slides, animated demos) of the StudyVault Highlight Mode feature.

## What's in here

| File | Purpose |
|---|---|
| `sample-lesson.html` | A standalone, working demo page. Open it in any browser to see the full feature — drag to highlight, tap-tap on mobile, pop-over, sweep animation, the lot. Drop into Designer as the visual reference. |
| `highlight-feature.js` | The full feature source. Self-injects its CSS, so Designer can read this one file to understand every visual rule. ~1700 lines. |
| `design-tokens.md` | Colours, typography, spacing, animation timings — the StudyVault visual language Designer should match. |
| `demo-script.md` | Recommended 15-second demo script: shot list + on-screen captions. |
| `flow-states.md` | Each state of the feature (out-of-mode → entering → in-mode → drag → popover → saved → modal). One frame per state — useful for carousel posts and shot-by-shot animation. |

## How to use with Claude Designer

1. **Open `sample-lesson.html` in your browser first**. Take 2–3 screenshots of it in different states (idle, mid-drag, popover open, modal open). These will be your reference images.
2. **Upload the screenshots + `design-tokens.md` + `demo-script.md`** to a Claude Designer conversation.
3. **Prompt suggestions** depending on what you want to produce:

   * *"Generate an animated 15-second product demo as a sequence of frames showing the highlight feature in use. Match the visual language in design-tokens.md and follow the storyboard in demo-script.md."*
   * *"Design a 3-slide LinkedIn carousel introducing this feature. Slide 1: hook ('Notes that survive your revision'). Slide 2: the desktop drag-to-highlight UX. Slide 3: the mobile tap-to-tap UX."*
   * *"Create a Twitter launch graphic (1600×900) announcing this feature. Use the History accent (#c44536) and the StudyVault wordmark style. Show a snippet of highlighted text with a sticky-note style note."*
   * *"Produce a single hero illustration showing the feature concept — a lesson page with three coloured highlights and a popover, in StudyVault's warm/serif aesthetic."*

4. **For motion specifically**: Designer is best at frame sequences and CSS animations rather than rendered video. Take its output (frame stills or HTML/CSS), screen-record it locally, then edit in CapCut/Clipchamp. Or use Designer to design the title cards and intro/outro, and screen-record `sample-lesson.html` for the actual feature footage in the middle.

## Updating this kit when the feature changes

`highlight-feature.js` is a copy of `js/highlight-annotate.js`. When the feature changes meaningfully (new colours, new UI, new interaction):

```bash
cp ../../js/highlight-annotate.js highlight-feature.js
# then update design-tokens.md and demo-script.md if any visual / flow change
```

## Brand snapshot

* **Subject accents** vary by colour theme — History `#c44536`, Geography `#059669`, etc. Use a strong subject colour in marketing visuals (the sample-lesson uses History).
* **Page bg** `#faf8f5` (warm cream). Card bg pure white.
* **Type** Inter for UI, Source Serif 4 for lesson titles & headings.
* **Vibe** Calm, scholarly, premium-but-not-cold. Not "edtech startup". Closer to *The Browser* / *Are.na* aesthetic than Quizlet.
