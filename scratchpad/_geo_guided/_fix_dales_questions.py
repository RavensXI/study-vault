# -*- coding: utf-8 -*-
"""Repoint the Dales sheets at their cropped versions and replace the questions
that were written around missing contour data.

    python scratchpad/_geo_guided/_fix_dales_questions.py --check
    python scratchpad/_geo_guided/_fix_dales_questions.py --apply

Every replacement below rests on a number produced by _measure_castleton.py or
_measure_claims.py, never on reading the picture and trusting it -- that is how
the originals went wrong. Each claim is about what is positively drawn; none
rests on something being absent, because absence is what a failed render looks
like.

Measured support:
  Castleton is in square 1582   grid lines x=154/503/852/1201, y=75/428/780/1132
  1582 vs 1583 contour ink      623.4 vs 153.5  (4.1x)
  steepest of four squares      1384 = 918.2, vs 1483 155.1, 1583 153.5, 1582 623.4
  valley floor vs fell to north 1583 = 153.5 vs 1384 = 918.2
  Dales NW corner vs fell top   175.1 vs 58.7   (3.0x)

Discarded for want of evidence: the old L14 woodland question ("they all lie
beside a river or a stream"). Only 51% of woodland pixels on the Dales sheet and
43% on the Castleton sheet fall near water, so the claim was never true of
either. It is replaced rather than relocated.
"""
import copy, json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
R2 = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
OLD15 = R2 + "yorkshire-dales-z15-final.jpg"
NEW15 = R2 + "yorkshire-dales-z15-w90-final.jpg"
PEAK = R2 + "peak-district-z15-final.jpg"

SUBJECTS = ["geography-aqa", "geography-edexcel-a", "geography-edexcel-b",
            "geography-ocr", "geography-eduqas", "geography"]

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


# --------------------------------------------------------------------------
# Replacements. Keyed by (lesson_number, tier, index).
# --------------------------------------------------------------------------

L13_B4 = {
    "hint": "Spacing is about steepness. The numbers printed on the lines are about height.",
    "image": NEW15,
    "display": "In the north-west corner of this map the contour lines are packed tightly together. Across the top of Cow Close Fell they are spread far apart. What does that difference in spacing tell you?",
    "options": [
        "The north-west corner is steeper than the top of the fell",
        "The north-west corner is higher than the top of the fell",
        "The north-west corner is gentler than the top of the fell",
        "The two areas are equally steep, only drawn differently",
    ],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "guided_steps": [
        {"say": "Two places can be the same height and nothing like the same steepness. Spacing is the reading that separates them."},
        {"pre": "Start in the top-left corner of the map. Type 1 if the brown lines there sit close together, or 2 if they sit far apart.",
         "hint": "Close together means you cross several lines within a short distance.",
         "answer": 1},
        {"pre": "Now find Cow Close Fell, the broad top left of centre with rings around it. Type 1 if its lines sit close together, or 2 if they sit far apart.",
         "done": "Same map, same interval, and the spacing could hardly be more different.",
         "hint": "Rings drawn well apart mean a long walk between one height step and the next.",
         "answer": 2},
        {"pre": "Crossing the same height step in a shorter distance means the ground climbs more sharply. Type 1 if that describes the north-west corner, or 2 if it describes the fell top.",
         "done": "That is the whole of reading steepness from contours: same interval, different spacing.",
         "hint": "Which of the two makes you cross more lines to walk the same distance?",
         "phase": "substitute",
         "answer": 1},
    ],
    "misconceptions": [
        {"expect": 1, "pattern": "spacing_read_as_height",
         "message": "Height and steepness are two different readings. The numbers printed along a contour give height; how close the lines sit gives steepness."},
        {"expect": 2, "pattern": "spacing_inverted",
         "message": "Check which way round the spacing runs. Count how many lines you cross walking a short distance in each of the two places."},
    ],
}

L14_B3 = {
    "hint": "Northings run across the map and are numbered up both sides.",
    "image": PEAK,
    "display": "The village of <strong>Castleton</strong> sits near the middle of this extract, just south of a numbered horizontal grid line. Type the number on that line.",
    "solutions": [83],
    "calculator": False,
    "input_type": "single_value",
    "guided_steps": [
        {"say": "Find the place first, then read the line. Doing it the other way round is how grid references go wrong."},
        {"pre": "Find Castleton, the largest settlement on the extract, near the middle where the main road widens into streets. Type 1 once you have it.",
         "hint": "It is the only place on this sheet drawn with named streets.",
         "answer": 1},
        {"pre": "Look straight up from the village to the nearest numbered horizontal line. Type that number.",
         "done": "Reading the line just north of a feature is how you fix its northing before writing a grid reference.",
         "hint": "The northings are the numbers running up the left and right edges.",
         "phase": "substitute",
         "answer": 83},
    ],
    "misconceptions": [
        {"expect": 82, "pattern": "line_below_not_above",
         "message": "That is the line below the village. The question asks for the one it sits just south of, so look upwards from Castleton."},
        {"expect": 15, "pattern": "easting_for_northing",
         "message": "That number comes from the top and bottom edges, so it is an easting. Northings are read up the sides."},
    ],
}

L14_B7 = {
    "hint": "Look right across each square before deciding; one of them contains a steep valley side.",
    "image": PEAK,
    "display": "Castleton lies in grid square <strong>1582</strong>. The square directly north of it is <strong>1583</strong>. Which of the two has more contour lines crossing it?",
    "options": [
        "1582, the square containing the village",
        "1583, the square north of the village",
        "They have about the same number",
        "Neither square has any contour lines",
    ],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "guided_steps": [
        {"say": "A square takes its name from the line to its left and the line below it, easting first."},
        {"pre": "Find the square with easting 15 down its left side and northing 82 along its base. Type the easting of the line forming its right-hand edge.",
         "hint": "Eastings rise by 1 for every square you move to the right.",
         "answer": 16},
        {"pre": "Square 1582 holds the village on the valley floor and the ground rising south of it. Type 1 if that rising ground carries many brown lines, or 2 if it carries almost none.",
         "hint": "Follow the ground south from the village towards the bottom of the square.",
         "answer": 1},
        {"pre": "Now compare the two squares. Type 1 if 1582 carries more brown line overall, or 2 if 1583 does.",
         "done": "The village square also contains the steep side of the dale, and that is where most of its contour lines are.",
         "hint": "Judge the whole square, not just the part with the houses on it.",
         "phase": "substitute",
         "answer": 1},
    ],
    "misconceptions": [
        {"expect": 1, "pattern": "judged_village_part_only",
         "message": "You may have judged 1582 only by the flat ground the village stands on. Look at the rest of that square as well."},
        {"expect": 3, "pattern": "blank_means_no_contours",
         "message": "Both squares carry contour lines. The question is which has more, not whether either has any."},
    ],
}

L14_S2 = {
    "hint": "The more brown line packed into a square, the steeper the ground it describes.",
    "image": PEAK,
    "display": "Compare grid squares <strong>1384</strong>, <strong>1483</strong>, <strong>1583</strong> and <strong>1582</strong>. Which one shows the steepest ground?",
    "options": ["1384", "1483", "1583", "1582"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "guided_steps": [
        {"say": "Steepness is a comparison here, so all four squares have to be found before any of them is judged."},
        {"pre": "Find 1384 first: easting 13 down its left side, northing 84 along its base. Type the easting of its right-hand edge.",
         "hint": "It sits in the upper left of the extract.",
         "answer": 14},
        {"pre": "Type 1 if 1384 is crowded with brown lines, or 2 if it is mostly open white space.",
         "hint": "Compare it with the squares nearer the middle of the sheet.",
         "answer": 1},
        {"pre": "Now judge all four. Type the four-figure reference of the square carrying the most brown line.",
         "done": "That corner of the extract climbs onto the moor, and the packed lines are what a steep climb looks like on a map.",
         "hint": "Three of the four sit on or near the valley floor; one does not.",
         "phase": "substitute",
         "answer": 1384},
    ],
    "misconceptions": [
        {"expect": 3, "pattern": "chose_village_square",
         "message": "1582 does carry a lot of contour line, but compare it square for square with the one in the upper left of the sheet."},
        {"expect": 2, "pattern": "chose_valley_shelf",
         "message": "That square is one of the gentlest on the extract. Look for the square where the lines are most tightly packed."},
    ],
}

L14_S6 = {
    "hint": "Judge a route by what the map shows along each possible line, not by what sounds sensible.",
    "image": PEAK,
    "display": "The main road on this extract runs east to west along the floor of the valley and never climbs over the fells. Which piece of map evidence best explains that route?",
    "options": [
        "Along the valley floor the contour lines are widely spaced, while the ground to the north has them packed close together",
        "The fells are covered in woodland, so no road could be cut across them",
        "The valley is the only part of the map with a stream in it",
        "The road is drawn in red, and red roads always follow rivers",
    ],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "guided_steps": [
        {"say": "A road builder is avoiding climbing. Contour spacing is the map's record of how much climbing there is."},
        {"pre": "Trace the red road across the middle of the extract. Type 1 if the lines it runs between are widely spaced, or 2 if they are packed tight.",
         "hint": "Follow it from the western edge through Castleton and out to the east.",
         "answer": 1},
        {"pre": "Now look at the ground in the upper left of the sheet, away from the road. Type 1 if the lines there are widely spaced, or 2 if they are packed tight.",
         "hint": "Square 1384 is the clearest example.",
         "answer": 2},
        {"pre": "A route that stays between widely spaced contours is a route that avoids climbing. Type 1 if that matches the road you traced, or 2 if it does not.",
         "done": "Roads follow the gentle line the relief offers, which in a dale means the valley floor.",
         "hint": "Compare what you typed for the road with what you typed for the fell.",
         "phase": "substitute",
         "answer": 1},
    ],
    "misconceptions": [
        {"expect": 1, "pattern": "woodland_as_barrier",
         "message": "Woodland is drawn in green and does not cover those fells. Look at what the brown lines are doing instead."},
        {"expect": 3, "pattern": "colour_as_evidence",
         "message": "Road colour records how important a road is, not what the ground beneath it does."},
    ],
}

L14_G2 = {
    "hint": "Site questions are answered by listing what the square actually contains.",
    "image": PEAK,
    "display": "The village of <strong>Castleton</strong> lies in grid square <strong>1582</strong>. Which combination of map evidence best explains why a village grew on this spot?",
    "options": [
        "Gently sloping valley-floor land beside a stream, with a main road running the length of the dale and higher ground rising on either side",
        "High exposed ground with wide views, where the contour lines are packed close on every side",
        "Thick woodland covering the whole square, giving timber and shelter",
        "A coastal position with a natural harbour and a bridging point",
    ],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "guided_steps": [
        {"say": "Answer this from the square itself. Read what is drawn there before reaching for a reason."},
        {"pre": "Find square 1582 and look at what runs through the village. Type 1 if a road passes through it, or 2 if none does.",
         "hint": "The red line is the main road through the dale.",
         "answer": 1},
        {"pre": "Type 1 if there is a watercourse drawn at or beside the village, or 2 if there is none.",
         "hint": "Watercourses are the thin blue lines.",
         "answer": 1},
        {"pre": "Type 1 if the ground rises away from the village to north and south, or 2 if the whole square is level.",
         "done": "Water to drink, level ground to build on, a road along the dale and shelter on both sides: that list is the answer.",
         "hint": "Look at the brown lines above and below the village.",
         "phase": "substitute",
         "answer": 1},
    ],
    "misconceptions": [
        {"expect": 1, "pattern": "site_read_as_summit",
         "message": "That describes the fells around the dale, not the square the village sits in. Read what 1582 itself contains."},
        {"expect": 2, "pattern": "woodland_overread",
         "message": "There is some woodland nearby, but it does not fill the square, and it is not what put a village here."},
    ],
}

L12_S4 = {
    "hint": "Direction is measured from the first place named to the second.",
    "image": NEW15,
    "display": "In which compass direction is <strong>Wilson's Pasture</strong> from <strong>Cow Close Fell</strong>?",
    "options": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "guided_steps": [
        {"say": "Start at the place you are measuring from, or the answer comes out backwards."},
        {"pre": "Find Cow Close Fell, left of centre with rings around it. Type 1 once you have it.",
         "hint": "It is the broad top in the middle of the sheet.",
         "answer": 1},
        {"pre": "Now find Wilson's Pasture, higher up the sheet. Type 1 if it lies above Cow Close Fell on the map, or 2 if it lies below.",
         "hint": "Up the sheet is north.",
         "answer": 1},
        {"pre": "It sits almost straight above, barely off to either side. Type 1 for due north, or 2 for north-east.",
         "done": "Almost no sideways shift means the direction stays on the cardinal point rather than the diagonal.",
         "hint": "A diagonal answer needs a clear shift sideways as well as upwards.",
         "phase": "substitute",
         "answer": 1},
    ],
    "misconceptions": [
        {"expect": 4, "pattern": "direction_reversed",
         "message": "That is the direction of Cow Close Fell from Wilson's Pasture. Measure from the first place named to the second."},
        {"expect": 1, "pattern": "diagonal_overreach",
         "message": "A north-east answer needs a clear shift to the right as well as upwards. Check how far across the sheet the two really are."},
    ],
}

PATCH = {
    (12, "silver", 4): L12_S4,
    (13, "bronze", 4): L13_B4,
    (14, "bronze", 3): L14_B3,
    (14, "bronze", 7): L14_B7,
    (14, "silver", 2): L14_S2,
    (14, "silver", 6): L14_S6,
    (14, "gold", 2): L14_G2,
}


def rewrite(pd, lesson_no, log):
    """Swap in replacements and repoint any surviving reference to the crop."""
    changed = False
    bank = pd.get("problem_bank") or {}
    for tier, items in bank.items():
        for i, p in enumerate(items):
            key = (lesson_no, tier, i)
            if key in PATCH:
                items[i] = copy.deepcopy(PATCH[key])
                log.append("L%d %s[%d] replaced" % (lesson_no, tier, i))
                changed = True
    # Anything still pointing at the clipped sheet moves to the crop. Those
    # questions are all west of easting 90, so pixel positions are unchanged.
    blob = json.dumps(pd)
    if OLD15 in blob:
        n = blob.count(OLD15)
        pd = json.loads(blob.replace(OLD15, NEW15))
        log.append("L%d repointed %d reference(s) to the cropped sheet" % (lesson_no, n))
        changed = True
    return pd, changed


def main(apply_it):
    problems, total = [], 0
    for slug in SUBJECTS:
        subj = req(B + "subjects?slug=eq.%s&select=id" % slug)
        if not subj:
            continue
        units = req(B + "units?subject_id=eq.%s&select=id,slug" % subj[0]["id"])
        unit = next((u for u in units if u["slug"] == "geographical-skills"), None)
        if not unit:
            continue
        lessons = req(B + "lessons?unit_id=eq.%s&select=id,lesson_number,practice_data" % unit["id"])
        for l in sorted(lessons, key=lambda x: x["lesson_number"]):
            if l["lesson_number"] not in (12, 13, 14):
                continue
            pd = l.get("practice_data") or {}
            log = []
            new_pd, changed = rewrite(copy.deepcopy(pd), l["lesson_number"], log)
            if not changed:
                continue
            total += 1
            print("%-20s %s" % (slug, "; ".join(log)))
            if apply_it:
                req(B + "lessons?id=eq.%s" % l["id"], method="PATCH",
                    body={"practice_data": new_pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % l["id"])[0]["practice_data"]
                if back != new_pd:
                    problems.append("%s L%d write did not land" % (slug, l["lesson_number"]))
                if OLD15 in json.dumps(back):
                    problems.append("%s L%d still references the clipped sheet" % (slug, l["lesson_number"]))

    print()
    print("rows %s: %d" % ("written" if apply_it else "to write", total))
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    if apply_it:
        print("all writes verified")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        main(True)
    elif "--check" in sys.argv:
        main(False)
    else:
        sys.exit(__doc__)
