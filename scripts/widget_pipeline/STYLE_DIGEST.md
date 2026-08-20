# House style digest — widgets

Everything a builder needs from the hand-built reference widgets without
reading them. If this conflicts with BUILD_GUIDE.md, the guide wins.

## Card

- The widget renders into a white modal card; the page behind is warm
  ground `#faf8f5`. Do not paint your own page background.
- Ink `#2d2a26`, muted ink `#5b564e`, hairlines `#efe9e0` / `#e0d9cd`.
- Accent comes in as `ctx.accent` (a hex). Use it for the kicker, small
  dots/highlights, and active states. Tint it with alpha suffixes
  (`accent + '22'`) rather than lightening by hand.
- Radius: 12px for inner panels, 8-10px for controls. Soft shadows only.

## Type

- Titles: `"Source Serif 4", Georgia, serif`, 600, ~1.2rem.
- Everything else: `Inter, system-ui, sans-serif`.
- Kicker over the title: .66rem, 700, letter-spacing .11em, uppercase,
  accent colour.
- Body/labels .8-.9rem; captions .78-.84rem muted. Nothing below .66rem.

## Structure that has worked

- Root: one wrapper div with a single class (`.svw-<id>`) carrying scoped
  CSS injected as a <style> tag. EVERY selector starts with the root class.
- Kicker + title, then the working area, then a caption line that does the
  talking (state changes narrate there, not in alerts).
- One primary commit button (`Check` / `Go`), dark ink background, white
  text. Secondary actions are quiet outline buttons.
- Mastery exit per BUILD_GUIDE §0c: 3-in-a-row streak, reset on wrong,
  `Another anyway` after mastery.
- Expose progress on the mounted element:
  `root.dataset.svState = JSON.stringify({..., streak, mastered, attempted})`
  updated on every commit.

## Accessibility

- All controls are real <button>s. Escape backs out of a picked-up state.
- An sr-only live region (1px clip pattern) narrates what changed.
- Respect `ctx.reducedMotion`: skip transitions, never skip information.

## Verify with the harness, not an improvised browser session

    node scripts/widget_pipeline/harness/check.mjs scripts/widget_pipeline/builds/<id>.js

It renders in headless Chrome and checks height budgets at 5 widths,
overflow, internal scrolling, narrow prose, CSS leakage (canary), commit
control, svState, keyboard reach, and inert controls. Iterate until PASS.
Then take ONE screenshot each at 420px and 900px and look at them:

    "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new \
      --screenshot=<out.png> --window-size=420,900 <a file: URL that mounts your widget>

(The harness writes its mount page to a temp dir; simplest is a tiny
test.html of your own that loads the widget file and mounts at one width.)
Fix what looks wrong, re-run the harness, stop.
