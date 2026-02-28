"""Send all 9 remaining Sport Science matplotlib diagrams through Gemini
to create pictorial isotype infographics. L07 already done.

Backs up matplotlib originals as diagram_name_matplotlib.jpg.

Usage:
    python generate_sport_gemini_infographics.py
"""

import os
import sys
import json
import base64
import time
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY environment variable")
    sys.exit(1)

MODEL = "gemini-3.1-flash-image-preview"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(PROJECT_ROOT, "sport-science", "r180")

COMMON_RULES = """
DESIGN RULES:
- Orange colour scheme (primary: #ea580c, dark: #9a3412, accents: #fb923c, #f97316)
- Landscape orientation, roughly 1800x1050 pixels
- White or very light warm cream background
- Clean modern sans-serif typography
- No watermarks, no photographic elements, no AI artifacts, no hands, no faces
- Flat design, vector-illustration style
- Icons/illustrations should be clean, simple, geometric — NOT realistic or photographic
"""

COMMON_STYLE = """You are a world-class infographic designer creating a pictorial isotype chart for a GCSE Sport Science revision website (students aged 15-16). The site uses an orange theme.

I'm giving you a matplotlib chart with REAL DATA. Transform it into a THEMATIC PICTORIAL INFOGRAPHIC — not just a prettier chart, but one where the visual metaphor matches the topic.

STYLE DIRECTION — PICTORIAL / ISOTYPE:
- Instead of abstract bars or lines, represent the data using THEMATIC ICONS or ILLUSTRATIONS related to the subject
- Think "editorial magazine infographic" or "BBC Bitesize visual" — something a teenager would find engaging and memorable
- The icons/illustrations should be clean, flat-design, vector-style (not realistic or photographic)
"""

DIAGRAMS = [
    {
        "filename": "diagram_extrinsic_factors.jpg",
        "lesson": "L01",
        "prompt": COMMON_STYLE + """
THIS CHART: Injury rates by sport per 1,000 participation hours (10 sports)
- Soccer: 7.21, Judo: 4.82, Basketball: 4.31, Volleyball: 2.64, Athletics: 2.35,
  Paddle Tennis: 1.72, Tennis: 1.39, Weight Training: 1.12, Cycling: 0.59, Swimming: 0.35

VISUAL FORMAT — THIS IS CRITICAL:
- Instead of plain bars, represent each sport with its OWN THEMATIC ICON (a football for soccer, a swimming figure for swimming, a bicycle for cycling, a judo figure for judo, etc.)
- The SIZE of each icon should be proportional to the injury rate — soccer's icon should be much larger than swimming's
- Arrange horizontally or in a grid, with the injury rate number clearly labelled next to each
- Show the contrast visually: contact sports (big icons, darker orange) vs non-contact (small icons, lighter orange)
- Include a small label or annotation: "Contact/combat sports have higher injury rates"

DATA RULES:
- Preserve ALL numbers exactly as listed above
- Include source: "Prieto-González et al. (2021), Int. J. Environ. Res. Public Health"
- Include key message: "Soccer has 20× the injury rate of swimming"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_intrinsic_factors.jpg",
        "lesson": "L02",
        "prompt": COMMON_STYLE + """
THIS CHART: ACL injury rates by gender and sport (per 100,000 athlete-exposures)
- Girls' Soccer: 12.2, Boys' Soccer: 4.8 (females 2.5× higher)
- Girls' Basketball: 10.3, Boys' Basketball: 2.3 (females 4.5× higher)

VISUAL FORMAT — THIS IS CRITICAL:
- Show TWO SPORTS side by side: Soccer and Basketball
- For each sport, show rows of 10 athlete figures (each figure = ~1.2 per 100,000)
- Use ORANGE figures for female athletes, GREY figures for male athletes
- For soccer: show more orange figures injured (12.2) vs fewer grey figures injured (4.8)
- OR use a comparison where female/male athlete silhouettes are shown with highlighted knees (ACL location)
- The key visual message: females are dramatically more likely to suffer ACL injuries in the same sports
- Include "2.5×" and "4.5×" multiplier callouts prominently

DATA RULES:
- Preserve ALL numbers exactly: 12.2, 4.8, 10.3, 2.3
- Include source: "Comstock et al. (2012), Am. J. Sports Med."
- Include key message: "In comparable sports, females are 2–4.5× more likely to suffer an ACL injury"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_warm_up_components.jpg",
        "lesson": "L03",
        "prompt": COMMON_STYLE + """
THIS CHART: FIFA 11+ structured warm-up programme — injury reduction by body area
- Hamstring: 60% reduction, ACL: 50%, All Knee: 48%, Hip/Groin: 41%, Overall: 39%, Ankle: 32%

VISUAL FORMAT — THIS IS CRITICAL:
- Show a HUMAN BODY OUTLINE (simple flat vector silhouette of an athlete) in the centre
- Around the body, use SHIELD or ARMOUR ICONS on each body part, sized proportionally to the injury reduction percentage
- Hamstring area: large shield icon with "60%" — the biggest protection
- Ankle area: smaller shield icon with "32%" — the least (but still substantial) protection
- Each body area labelled clearly with the percentage
- The visual metaphor: the FIFA 11+ warm-up acts like protective armour on different body parts
- Include the FIFA 11+ name/branding prominently as a title

DATA RULES:
- Preserve ALL numbers exactly: Hamstring 60%, ACL 50%, Knee 48%, Hip/Groin 41%, Overall 39%, Ankle 32%
- Include source: "Sadigursky et al. (2017), BMC Sports Sci. Med. Rehabil."
- Include: "20-minute neuromuscular warm-up programme"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_stretching_types.jpg",
        "lesson": "L04",
        "prompt": COMMON_STYLE + """
THIS CHART: Two panels — (1) Stretching type effect on power/strength, (2) ROM improvement over 4 weeks

Panel 1 — Immediate performance effect:
- Dynamic stretching: +1.3% (improvement)
- Static stretching: -3.7% (decline)
- PNF stretching: -4.4% (decline)

Panel 2 — Hip flexion ROM gain after 4-week programme:
- Control (no stretching): -0.1° (no change)
- Static stretching: +4.7°
- PNF stretching: +15.6° (3.3× greater than static)

VISUAL FORMAT — THIS IS CRITICAL:
- LEFT SIDE: Show three athlete figures doing each stretch type
  - Dynamic: figure in motion with an UP ARROW (green/orange tint) showing +1.3%
  - Static: figure holding a stretch with a DOWN ARROW (red/grey tint) showing -3.7%
  - PNF: figure with partner stretching with a DOWN ARROW showing -4.4%
- RIGHT SIDE: Show flexibility as an ANGLE or ARC icon
  - Control: tiny arc, nearly closed
  - Static: medium arc opening to show +4.7°
  - PNF: wide arc opening to show +15.6°
- Title the two halves: "Power & Strength" and "Flexibility Gains"
- Key insight callout: "Dynamic for warm-ups (maintains power), Static/PNF for cool-downs (builds flexibility)"

DATA RULES:
- Preserve ALL numbers exactly as listed above
- Include sources: "Behm & Chaouachi (2011)" and "Keerthiga et al. (2016)"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_acute_injuries.jpg",
        "lesson": "L05",
        "prompt": COMMON_STYLE + """
THIS CHART: Most common acute sports injuries by type (percentage of all acute injuries)
- Ligament Sprain: 31.7%
- Concussion: 21.0%
- Muscle Strain: 12.2%
- Contusion (bruise): 11.9%
- Fracture: 3.5%
- Other (dislocation, abrasion, etc.): 19.7%

VISUAL FORMAT — THIS IS CRITICAL:
- Use INJURY-SPECIFIC ICONS for each type, sized proportionally to their percentage:
  - Sprain: a twisted/bandaged ankle icon (largest — 31.7%)
  - Concussion: a head with impact stars/circles icon (second largest — 21.0%)
  - Strain: a muscle/leg with a tear/lightning bolt icon (12.2%)
  - Contusion: a bruised area/impact mark icon (11.9%)
  - Fracture: a broken bone icon (small — 3.5%)
  - Other: a medical cross or mixed icon (19.7%)
- Arrange in a WAFFLE CHART or PROPORTIONAL ICON GRID where the number of icons represents the percentage
- OR arrange as a pictorial bar chart where each "bar" is made of stacked injury-specific icons
- Each type clearly labelled with percentage

DATA RULES:
- Preserve ALL numbers exactly as listed
- Include source: "Schroeder et al. (2021), Injury Epidemiology — ~17.4 million injuries"
- Include key message: "Sprains and concussions account for over half of all acute injuries"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_chronic_injuries.jpg",
        "lesson": "L06",
        "prompt": COMMON_STYLE + """
THIS CHART: Achilles tendinopathy prevalence by sport/population
- General Population: 0.6%
- Ball Games (general): 6.0%
- Basketball: 7.7%
- Football (professional): 11.6%
- All Runners: 30.0%
- Elite Runners (lifetime): 52.0%

VISUAL FORMAT — THIS IS CRITICAL:
- Show RUNNER/ATHLETE FIGURES for each sport category, with the ACHILLES TENDON area highlighted in orange/red
- The NUMBER of affected figures out of a group should represent the prevalence:
  - General population: show 100 tiny figures, barely 1 highlighted (0.6%)
  - Elite runners: show 10 runner figures, about 5 highlighted (52%)
- OR use sport-specific icons (running shoe, football, basketball) where the SIZE represents prevalence
- The visual story: the more repetitive running/jumping a sport involves, the more Achilles injuries
- Elite runners at 52% should be dramatically visually dominant

DATA RULES:
- Preserve ALL numbers exactly as listed
- Include source: "PMC Systematic Review & Meta-Analysis (2022)"
- Include key message: "Repetitive impact loading in running causes the highest chronic injury rates"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_treatment_protocols.jpg",
        "lesson": "L08",
        "prompt": COMMON_STYLE + """
THIS CHART: Re-injury rates — proper rehabilitation vs inadequate rehabilitation
Three studies:
- Hamstring (Mendiguchia 2017): 4% with proper rehab vs 25% without (6.3× higher)
- Hamstring (Sherry 2004): 7.1% with proper rehab vs 50% without (7× higher)
- ACL (PMC 2022): 5.6% with proper rehab vs 38.2% without (6.8× higher)

VISUAL FORMAT — THIS IS CRITICAL:
- For each study, show TWO GROUPS of 10 athlete figures side by side:
  - LEFT GROUP (proper rehab): mostly healthy orange figures, with very few injured/red-crossed (matching the low %)
  - RIGHT GROUP (no proper rehab): many injured/red-crossed figures (matching the high %)
- Hamstring (Mendiguchia): left = ~10 healthy, 0 injured / right = ~7-8 healthy, 2-3 injured
- Hamstring (Sherry): left = ~9-10 healthy, 1 injured / right = ~5 healthy, 5 injured
- ACL: left = ~9-10 healthy, 1 injured / right = ~6 healthy, 4 injured
- Use a BIG multiplier callout between each pair: "6.3×", "7×", "6.8×"
- Healthy athletes shown in bold orange, re-injured athletes shown greyed out or with a red cross/injury mark

DATA RULES:
- Preserve ALL numbers exactly: 4% vs 25%, 7.1% vs 50%, 5.6% vs 38.2%
- Include sources: "Mendiguchia et al. (2017); Sherry (2004); PMC9569141"
- Include key message: "Athletes who skip proper rehab are 6–7× more likely to be injured again"
""" + COMMON_RULES
    },
    {
        "filename": "diagram_medical_conditions_1.jpg",
        "lesson": "L09",
        "prompt": COMMON_STYLE + """
THIS CHART: UK prevalence of common medical conditions + key actions for sport
- Asthma: 120 per 1,000 people
- Type 2 Diabetes: 68 per 1,000
- Epilepsy: 9 per 1,000
- Type 1 Diabetes: 4 per 1,000

Plus action panels for each condition (what to do in sport):
- Asthma: carry reliever inhaler, warm up well, avoid cold dry air
- Type 1 Diabetes: monitor blood sugar, carry glucose gel, eat before exercise
- Type 2 Diabetes: regular exercise helps, monitor levels, balanced diet
- Epilepsy: take medication, inform coach/officials, avoid known triggers

VISUAL FORMAT — THIS IS CRITICAL:
- Show CROWD SCENES of simple human figures (10×10 grids = 100 people each)
- For asthma: in a grid of 100 people (each = 10 per 1,000), highlight 12 in orange (120 per 1,000)
- For Type 2 diabetes: highlight ~7 in orange (68 per 1,000)
- For epilepsy: highlight ~1 in orange (9 per 1,000)
- For Type 1 diabetes: less than 1 highlighted
- Below each crowd, show the KEY ACTION using a thematic icon:
  - Asthma: inhaler icon
  - Diabetes: blood sugar monitor / glucose icon
  - Epilepsy: medication/pill icon
- The visual contrast between asthma (very common) and Type 1 diabetes (rare) should be dramatic

DATA RULES:
- Preserve ALL numbers exactly: 120, 68, 9, 4 per 1,000
- Include all action points listed above
""" + COMMON_RULES
    },
    {
        "filename": "diagram_medical_conditions_2.jpg",
        "lesson": "L10",
        "prompt": COMMON_STYLE + """
THIS CHART: How dehydration affects sports performance (% body weight loss vs decline)
- 1% body weight loss: endurance begins to decline
- 2% loss: aerobic performance reduced ~10%
- 2.5% loss: high-intensity exercise capacity reduced ~45%
- 3% loss: VO2max decreases ~5%, strength reduced ~5%
- 5% loss: work capacity decreases ~30%

VISUAL FORMAT — THIS IS CRITICAL:
- Show a ROW OF WATER BOTTLES (or water droplet icons) for each dehydration level, getting progressively EMPTIER
  - 1%: nearly full bottle, slight performance dip
  - 2%: bottle at 80%, moderate dip
  - 2.5%: bottle at ~60%, major dip
  - 3%: bottle at ~50%
  - 5%: bottle nearly empty, severe performance loss
- Next to each bottle, show an ATHLETE FIGURE whose posture degrades:
  - 1%: upright runner, slightly slower
  - 2%: runner slowing, sweat drops
  - 5%: hunched over, exhausted, barely moving
- Label each level with the exact performance decline percentage
- The visual story: as the water drains, the athlete deteriorates

DATA RULES:
- Preserve ALL numbers exactly as listed above
- Include sources: "Human Kinetics; Cheuvront & Kenefick (2014)"
- Include key message: "Don't wait until you feel thirsty — by then you're already dehydrated"
""" + COMMON_RULES
    },
]


def call_gemini(prompt_text, image_path, output_path):
    """Send image + prompt to Gemini, save result."""
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [
            {"text": prompt_text},
            {"inlineData": {"mimeType": "image/jpeg", "data": img_data}}
        ]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  HTTP {e.code}: {body[:300]}")
        return False

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  -> Saved ({len(img_bytes) / 1024:.0f} KB)")
                return True
            elif "text" in part:
                txt = part["text"][:150]
                if txt.strip():
                    print(f"  Gemini note: {txt}")

    print("  No image returned!")
    print(json.dumps(result, indent=2)[:500])
    return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = len(DIAGRAMS)
    success = 0

    for i, d in enumerate(DIAGRAMS, 1):
        fname = d["filename"]
        src = os.path.join(OUT_DIR, fname)
        backup = os.path.join(OUT_DIR, fname.replace(".jpg", "_matplotlib.jpg"))

        print(f"\n[{i}/{total}] {d['lesson']}: {fname}")

        if not os.path.exists(src):
            print(f"  SKIP — source file not found: {src}")
            continue

        # Back up matplotlib original (if not already backed up)
        if not os.path.exists(backup):
            os.rename(src, backup)
            print(f"  Backed up matplotlib -> {os.path.basename(backup)}")
        else:
            print(f"  Matplotlib backup already exists")

        # Use the matplotlib backup as input
        if call_gemini(d["prompt"], backup, src):
            success += 1
        else:
            # Restore matplotlib if Gemini failed
            if not os.path.exists(src):
                import shutil
                shutil.copy2(backup, src)
                print(f"  Restored matplotlib as fallback")

        # Rate limit — be kind to the API
        if i < total:
            print("  Waiting 5s...")
            time.sleep(5)

    print(f"\n{'='*50}")
    print(f"Done. {success}/{total} diagrams upgraded to pictorial infographics.")
    if success < total:
        print(f"  {total - success} failed — matplotlib versions remain in place.")


if __name__ == "__main__":
    main()
