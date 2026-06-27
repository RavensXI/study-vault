"""Generate one SKETCH-style backdrop per unit for SAM's subjects (the winning
style), so every unit's learning path sits on bespoke, topic-specific art.

Reads  scratch_sam_units.json (from _designlab_sam_discover.py).
Writes design-lab/assets/path-bg-u-<subject>-<unit>.png  (skips if present)
       design-lab/_path_backdrops.json  (manifest: "subject/unit" -> {file,accent})

Run:  python scripts/_designlab_unit_backdrops.py            (all)
      python scripts/_designlab_unit_backdrops.py maths-ocr  (one subject)
"""
import base64, json, os, re, sys
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "design-lab", "assets")
UNITS = json.load(open(os.path.join(ROOT, "scratch_sam_units.json"), encoding="utf-8"))

# subject accent + a plain-words colour name for the prompt
ACCENT = {
    "maths-ocr":             ("#46707a", "muted teal"),
    "english-language-ocr":  ("#7a5a7a", "muted mauve"),
    "english-literature-aqa":("#7d3737", "muted maroon red"),
    "science-aqa":           ("#368352", "muted green"),
    "history-ocr":           ("#5b3776", "muted purple"),
    "geography-edexcel-b":   ("#514bb4", "muted indigo blue"),
    "spanish-edexcel":       ("#b24d4d", "muted brick red"),
    "computer-science":      ("#46688a", "muted slate blue"),
    "religious-studies-aqa": ("#9a6a4a", "muted terracotta brown"),
}

# concrete, sketchable motifs per unit (keyed subject/unit-slug)
MOTIFS = {
 # Mathematics
 "maths-ocr/algebra": "a balancing scale weighing two sides, a quadratic parabola curve, nested brackets, an x and y symbol, a spiral of growing squares, a line-graph axis, a row of dominoes",
 "maths-ocr/geometry": "a pair of compasses, a protractor, a right-angled triangle, a circle with a radius line, an unfolded cube net, an arrow vector, interlocking polygons, a set square",
 "maths-ocr/graphs": "a coordinate grid with a plotted straight line, a parabola curve, a wavy sine curve, an exponential curve climbing, points marked on axes, a curve with a tangent line, a ruler",
 "maths-ocr/number": "stacked fraction bars, a percent sign, a sieve grid of prime numbers, a place-value abacus, exponents stacked as powers, a square-root symbol, scattered loose digits",
 "maths-ocr/probability-statistics": "a probability tree diagram, two overlapping Venn circles, a pair of dice, a small bar chart, a box-and-whisker plot, a tally chart, a spinner",
 "maths-ocr/ratio-proportion": "a recipe card with scaled ingredients, a speedometer dial, two meshing gears, a map scale bar, a pie split into a ratio, a measuring jug, a growth arrow",
 # English Language
 "english-language-ocr/component-1-reading": "an open Victorian newspaper, a magnifying glass over a column of text, a quill and ink bottle, a stack of non-fiction books, reading spectacles, a folded broadsheet, a highlighter stroke",
 "english-language-ocr/component-1-writing": "a fountain pen mid-stroke, a speaker at a lectern with a megaphone, an envelope and letter, a planning spider-diagram, a sheet of lined paper, a crossed-out draft, a pencil",
 "english-language-ocr/component-2-reading": "an open storybook, a magnifying glass, a theatre mask, swirling imagery lines, a large quotation mark, a candle beside a book, a bookmark ribbon, an inkwell",
 "english-language-ocr/component-2-writing": "an open notebook with a story opening, a lightbulb of an idea, a winding narrative arrow, a character-sketch face, a storm cloud for atmosphere, a fountain pen, a full stop",
 # English Literature
 "english-literature-aqa/macbeth": "a king's crown, a bloodied dagger, three hooded witch silhouettes, a bubbling cauldron, a Scottish castle on a crag, a perched raven, an empty throne",
 "english-literature-aqa/a-christmas-carol": "a chained ghost, a Christmas turkey, a glowing fireplace hearth, a hand-bell, a tombstone, a Victorian street lamp, a candlestick, holly leaves",
 "english-literature-aqa/an-inspector-calls": "an Edwardian dining table set for an engagement dinner, a ringing telephone, an inspector's silhouette with a notebook, a sinking ocean liner, a framed photograph, a wine decanter, a doorbell",
 "english-literature-aqa/power-and-conflict": "a crumbling colossal statue half-buried in desert sand, a cavalry charge of horses, a bayonet rifle, a war photographer's camera, a single poppy, a craggy mountain peak, a diving warplane",
 "english-literature-aqa/unseen-poetry": "an open book of poetry, a quill, scattered loose lines of verse, a magnifying glass over a stanza, a pressed flower, two poems side by side, an inkblot",
 # Combined Science
 "science-aqa/biology-paper-1": "a microscope, a single rounded biological animal cell with a clearly visible round nucleus and cell membrane (a microscope cell, NOT an egg or food), a beating heart with vessels, a leaf cross-section, bacteria in a petri dish, a vaccine syringe, a pair of lungs",
 "science-aqa/biology-paper-2": "a DNA double helix, a branching neuron, a side profile of a brain, a Punnett inheritance square, an eye, a kidney, a simple food chain of creatures",
 "science-aqa/chemistry-paper-1": "a Bohr atom with orbiting electrons, a single periodic-table tile, a conical flask, two atoms bonded together, a Bunsen burner flame, electrolysis electrodes in a beaker, a balance scale",
 "science-aqa/chemistry-paper-2": "an oil-refinery fractionating column, a rising reaction-rate curve, a chromatography strip, the Earth wrapped in atmosphere, a long polymer chain, a rack of test tubes, a gas jar",
 "science-aqa/physics-paper-1": "a forked lightning bolt of static, a circuit with a bulb and battery, a decaying radioactive atom, an energy-transfer arrow, a thermometer, a wind turbine, a single wave",
 "science-aqa/physics-paper-2": "force arrows pushing a box, a stretched coil spring, a speeding car with motion lines, a planet orbiting in space, a horseshoe magnet with field lines, a lever on a pivot, a wave",
 # History
 "history-ocr/international-relations-1918-1975": "a rolled peace-treaty scroll with wax seals, a globe for the League of Nations, a slab of the Berlin Wall, a nuclear missile, a fighter jet, a map of a divided Germany, a peace dove",
 "history-ocr/germany-people-state-1925-1955": "a 1920s cabaret theatre poster, a crashing-economy graph, a marching crowd of silhouettes, a draped plain banner on a building, an old radio broadcasting, a coil of barbed wire, a divided city",
 "history-ocr/migration-to-britain-1000-2010": "a Norman longship with round shields, a medieval walled city gate, a tall sailing trade ship, a steam locomotive, a suitcase by a ship's gangway, a bustling multicultural street, a stamped passport",
 "history-ocr/usa-people-state-1919-1948": "a vintage Model-T motor car, a jazz saxophone, a Wall Street ticker with a crashing share graph, the Statue of Liberty, art-deco skyscrapers, a Depression-era bread queue, a great dam",
 # Geography
 "geography-edexcel-b/geographical-skills": "a bar chart, a line graph, a pie chart, a scatter plot with a trend line, a population pyramid, a grid-reference map square, a compass rose, a pair of dividers",
 "geography-edexcel-b/global-geographical-issues": "a swirling spiral tropical cyclone, the Earth banded with climate zones, tectonic plates with an erupting volcano, a megacity skyline, a rain gauge, a thermometer, an arrow of change",
 "geography-edexcel-b/people-environment-issues": "a dense tropical rainforest canopy, a snowy taiga of pine trees, a globe of biomes, a wind turbine beside a solar panel, a water droplet, an oil barrel, a protected single tree",
 "geography-edexcel-b/uk-geographical-issues": "an eroding coastline with a cliff and a sea stack, a river meandering to the sea, a UK city skyline with cranes, a flood-defence wall, rolling hills, a fieldwork clipboard, the outline of Britain",
 # Spanish
 "spanish-edexcel/lifestyle-and-wellbeing": "a plate of healthy food, a running shoe, an alarm clock, a glass of water, a dumbbell, a heart symbol, a bowl of fruit",
 "spanish-edexcel/media-and-technology": "a television set, headphones with music notes, a smartphone with blank app icons, a game controller, a film clapperboard, a play button, a laptop",
 "spanish-edexcel/my-neighbourhood": "a row of little town shops, a city bus, a shopping bag, a folded street map, a park tree, a market stall, a signpost",
 "spanish-edexcel/my-personal-world": "a family group of silhouettes, two friends side by side, a pair of clasped hands, a portrait mirror, a speech bubble, a heart, a balance of equality",
 "spanish-edexcel/studying-and-my-future": "a school satchel with books, a graduation cap, a classroom clock, a signpost of different jobs, a pencil and ruler, a briefcase, a forking path arrow",
 "spanish-edexcel/travel-and-tourism": "a suitcase with travel stickers, an aeroplane, a beach umbrella with a sun, a hotel reception bell, a map with a dotted route, a passport, a camera",
 # Computer Science
 "computer-science/computational-thinking": "a flowchart with decision diamonds, a branching binary-search tree, two nested loops, a beetle bug being debugged, a block of pseudocode lines, bars being sorted into order, a truth-table grid",
 "computer-science/computer-systems": "a CPU chip with pins, a stick of RAM, a spinning hard-disk platter, a network of connected nodes, a column of binary digits, a router, a padlock, an operating-system window",
 # Religious Studies
 "religious-studies-aqa/christianity-beliefs": "a Christian cross, a Trinity triangle, a descending dove, an open Bible, a pair of praying hands, a chalice, rays of creation light",
 "religious-studies-aqa/christianity-practices": "a church with a steeple, a baptism font with water, praying hands, a chalice with bread, a pilgrim's walking staff, a lit candle, an Advent wreath",
 "religious-studies-aqa/islam-beliefs": "a crescent moon and star, an open Qur'an on a wooden stand, a mosque dome and minaret, a string of prayer beads, a pointed arch with star pattern, rays of light, a geometric tile",
 "religious-studies-aqa/islam-practices": "a mosque with a minaret, a prayer mat facing a mihrab niche, the cube of the Kaaba, a crescent moon for fasting, charity coins in an open hand, prayer beads, a pilgrim's robe",
 "religious-studies-aqa/theme-a-relationships": "two interlocked wedding rings, a family silhouette, a pair of joined hands, a heart, a small house, a balance of equality, a cradle",
 "religious-studies-aqa/theme-b-religion-life": "a globe with stars for creation, a green leaf with a small animal, scales weighing life and death, a candle, an hourglass, a growing tree, a dove",
 "religious-studies-aqa/theme-d-peace-conflict": "a dove carrying an olive branch, a broken rifle, balanced scales of justice, two hands shaking, a circular peace symbol, a white flag, a peace candle",
 "religious-studies-aqa/theme-e-crime-punishment": "scales of justice, prison bars, a judge's gavel, two contrasting masks of good and evil, a key, an open hand of forgiveness, a candle",
}

STRICT = ("STRICT: vertical portrait. Warm off-white paper (#f7f6f4) fills the ENTIRE image. Place every "
          "drawing ONLY in the far-left and far-right margins; the whole central vertical third MUST stay "
          "completely empty — bare paper, reserved for an overlay. Keep everything pale, faded and "
          "low-contrast. ABSOLUTELY NO text, words, letters, numbers, labels or captions. No frame, no "
          "border, no watermark.")

def sketch_prompt(motifs, word, hexc):
    return (f"VERY ROUGH, loose, UNFINISHED hand-sketch — quick scratchy biro/pencil doodles of {motifs}, "
            f"drawn fast and imperfectly with wobbly lines and several shapes only half-drawn, sparse and "
            f"gestural, NOT a finished drawing. Thin faint single {word} line ({hexc}) on warm paper, no "
            f"shading, no fills. " + STRICT)

def fallback_motifs(unit):
    ts = unit.get("titles", [])[:6]
    return ", ".join(re.sub(r"[^A-Za-z &'-]", " ", t).strip() for t in ts) or unit["name"]

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not set")
    only = sys.argv[1] if len(sys.argv) > 1 else None
    client = OpenAI()
    manifest = {}
    made = skipped = failed = 0
    for skey, sub in UNITS.items():
        if only and skey != only:
            continue
        hexc, word = ACCENT[skey]
        for u in sub["units"]:
            key = f'{skey}/{u["slug"]}'
            fname = f'path-bg-u-{skey}-{u["slug"]}.png'
            out = os.path.join(ASSETS, fname)
            manifest[key] = {"file": fname, "accent": hexc, "name": u["name"]}
            if os.path.exists(out) and os.path.getsize(out) > 20000:
                skipped += 1
                continue
            motifs = MOTIFS.get(key) or fallback_motifs(u)
            prompt = sketch_prompt(motifs, word, hexc)
            # Religious-sensitivity guard: many faiths forbid figural depiction of prophets (and Islamic
            # art is aniconic). Keep RE backdrops to symbols, architecture and objects only — no people.
            if skey == "religious-studies-aqa":
                prompt += (" IMPORTANT religious-sensitivity rule: use ONLY symbols, architecture and objects — "
                           "absolutely NO human figures, NO faces, and NO depiction of any prophet, deity or "
                           "religious person (aniconic). Empty crosses, not crucified figures.")
            ok = False
            for model in ("gpt-image-2", "gpt-image-1"):
                try:
                    print(f"[{key}] {model}…", flush=True)
                    r = client.images.generate(model=model, prompt=prompt, size="1024x1536", quality=os.environ.get("DL_QUALITY", "medium"))
                    with open(out, "wb") as f:
                        f.write(base64.b64decode(r.data[0].b64_json))
                    print(f"[{key}] saved ({os.path.getsize(out)//1024} KB)", flush=True)
                    made += 1; ok = True; break
                except Exception as e:
                    print(f"[{key}] {model} failed: {e}", flush=True)
            if not ok:
                failed += 1
    # manifest always reflects the full intended set (so the dashboard knows the filenames)
    mpath = os.path.join(ROOT, "design-lab", "_path_backdrops.json")
    full = {}
    for skey, sub in UNITS.items():
        hexc, word = ACCENT[skey]
        for u in sub["units"]:
            key = f'{skey}/{u["slug"]}'
            full[key] = {"file": f'path-bg-u-{skey}-{u["slug"]}.png', "accent": hexc, "name": u["name"]}
    json.dump(full, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\ndone — made {made}, skipped {skipped}, failed {failed}; manifest -> {mpath}")

if __name__ == "__main__":
    main()
