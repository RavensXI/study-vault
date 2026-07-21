# -*- coding: utf-8 -*-
"""Retire every OS sheet with a render defect from L11 and L12.

    python scratchpad/_geo_guided/_retire_broken_maps.py --check
    python scratchpad/_geo_guided/_retire_broken_maps.py --apply

Tom: even where the question does not depend on relief, he does not want a sheet
with contours cut off in front of a student.

Six sheets go: clitheroe-z15, south-downs-z15/z16, dorset-coast-z15/z16 (contour
layer failed -- Clayton Windmills stand at about 230 m on the South Downs scarp
and their sheet draws no contour at all) and norfolk-broads-z16, which turned out
to carry a solid black rectangle across its lower left. That one is a corrupt
render rather than a contour problem, and it has been live in L11.

Two kinds of change:

1. Image-only, for the three Norfolk questions. A grid reference describes the
   ground, not the sheet, so norfolk-broads-z15 covers the same squares and the
   authored answers stand untouched -- including gold[3], whose confluence still
   falls in the centre of the frame. Nothing is re-derived that was already
   checked, because overwriting a verified answer with my own estimate is a way
   to break something that was right.

2. Replacement, where no clean sheet covers that ground. Every answer here comes
   from _grid_ref.py, which was validated first against two references known to
   be correct (Walker Fold 6741, Castleton 1582).

Answers used, all tool-computed:
  Chaigley Hall 6841 / Chadswell Home Farm 677422   clitheroe-z16
  Thurne 4016                                       norfolk-broads-z15
  Castleton 1582 / Marston Farm 158834              peak-district-z15
  Losehill Hall 154838                              peak-district-z15
  Woodseats -> Spring House Farm  2.00 km, 94 deg E
  Red Barn -> Rowter Farm         2.57 km -> 2.5
  Castleton -> Knowlegates Farm   1.41 km -> 1.5
  Long Plantation -> Nu Farm      1.08 km -> 1.0    clitheroe-z16
  Dunscar Farm -> Marston Farm    1.58 km, 92 deg E
  Chadswell Home Farm -> Chaigley Hall  132 deg SE

Bearings were only used where the tool reported a comfortable margin from the
sector boundary; anything it flagged as borderline was discarded rather than
rounded into place.
"""
import copy, json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
R2 = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
NORFOLK = R2 + "norfolk-broads-z15-final.jpg"
CLITH = R2 + "clitheroe-z16-final.jpg"
PEAK = R2 + "peak-district-z15-final.jpg"

RETIRE = ["clitheroe-z15-final.jpg", "south-downs-z15-final.jpg", "south-downs-z16-final.jpg",
          "dorset-coast-z15-final.jpg", "dorset-coast-z16-final.jpg", "norfolk-broads-z16-final.jpg"]

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


def ref4(feature, answer, image, where, hint, wrong_e, wrong_n):
    """A four-figure reference question. Robust: whole-square, so a small error
       reading the label position cannot change the answer."""
    return {
        "hint": hint,
        "image": image,
        "display": "What is the <strong>four-figure</strong> grid reference of the grid square containing <strong>%s</strong>?" % feature,
        "solutions": [answer],
        "calculator": False,
        "input_type": "single_value",
        "guided_steps": [
            {"say": "Nothing here is a calculation. It is all reading numbers off the edges of the map."},
            {"pre": "Find %s on the map, %s. Type 1 once you have it." % (feature, where),
             "hint": "Take your time locating it before reading any numbers.",
             "answer": 1},
            {"pre": "A vertical grid line runs down the left side of its square. Read that line's two-figure number from the top or bottom edge and type it.",
             "hint": "Eastings are the numbers along the top and bottom.",
             "answer": int(str(answer)[:2])},
            {"pre": "Now the horizontal grid line along the bottom of that same square. Read its two-figure number from the side and type it.",
             "hint": "Northings are the numbers up the left and right edges.",
             "answer": int(str(answer)[2:])},
            {"pre": "Join the two pairs, easting first, into one four-figure reference and type it.",
             "done": "Along the corridor and up the stairs: easting first, northing second, every time.",
             "hint": "No spaces, no comma, four figures.",
             "phase": "substitute",
             "answer": answer},
        ],
        "misconceptions": [
            {"expect": wrong_n, "pattern": "northing_before_easting",
             "message": "Those are the right two pairs the wrong way round. The easting, read along the top, always comes first."},
            {"expect": wrong_e, "pattern": "line_above_or_right",
             "message": "Check which lines you read. A square is named by the line down its left side and the line along its bottom."},
        ],
    }


def ref6(feature, answer, image, where, hint):
    e3, n3 = str(answer)[:3], str(answer)[3:]
    return {
        "hint": hint,
        "image": image,
        "display": "What is the <strong>six-figure</strong> grid reference of <strong>%s</strong>?" % feature,
        "solutions": [answer],
        "calculator": False,
        "input_type": "single_value",
        "guided_steps": [
            {"say": "Six figures means two readings each way: the grid line first, then the tenths across the square."},
            {"pre": "Find %s, %s. Type 1 once you have it." % (feature, where),
             "hint": "Locate the feature before reading any numbers.",
             "answer": 1},
            {"pre": "Read the two-figure number of the grid line down the left side of its square, then type how many tenths across the square it sits. Type all three figures together.",
             "hint": "Picture the square split into ten strips from left to right.",
             "answer": int(e3)},
            {"pre": "Now the northing the same way: the two-figure line along the bottom, then the tenths up the square. Type all three figures.",
             "hint": "Ten strips again, this time from the bottom upwards.",
             "answer": int(n3)},
            {"pre": "Put the three easting figures first, then the three northing figures, and type the six-figure reference.",
             "done": "Three figures each way, easting first. That is the whole method.",
             "hint": "Six figures, no spaces.",
             "phase": "substitute",
             "answer": answer},
        ],
        "misconceptions": [
            {"expect": int(n3 + e3), "pattern": "northing_before_easting",
             "message": "Right figures, wrong order. The three easting figures always come first."},
            {"expect": int(e3[:2] + n3[:2]), "pattern": "gave_four_figures",
             "message": "That is the four-figure reference. Six figures needs the tenths across and up the square as well."},
        ],
    }


def dist(a, b, answer, image, ruler, where):
    p = {
        "hint": "Measure %s to %s in centimetres, then divide by the number of centimetres that stand for 1 km." % (a, b),
        "unit": "km",
        "image": image,
        "display": "Using the ruler tool, measure the straight-line distance from <strong>%s</strong> to <strong>%s</strong>. Give your answer in km to the nearest 0.5 km." % (a, b),
        "solutions": [answer],
        "calculator": True,
        "input_type": "single_value",
        "guided_steps": [
            {"say": "Straight-line distance means as the crow flies, not along the road."},
            {"pre": "Find %s and %s on the map, %s. Type 1 once you have both." % (a, b, where),
             "hint": "Both have to be located before anything is measured.",
             "answer": 1},
            {"pre": "Type 1 if the scale bar shows %d cm standing for 1 km, or 2 if it shows something else." % ruler["cmPerKm"],
             "hint": "The scale is printed with the ruler tool.",
             "answer": 1},
            {"pre": "Measure between them and give the distance in km, to the nearest 0.5 km.",
             "done": "Measure, then convert with the scale. Never estimate straight to kilometres.",
             "hint": "Divide your centimetre reading by the centimetres that stand for 1 km.",
             "phase": "substitute",
             "answer": answer},
        ],
        "misconceptions": [
            {"expect": answer * 2, "pattern": "forgot_to_divide",
             "message": "That looks like the centimetre reading rather than the distance on the ground. Convert it with the scale."},
            {"expect": round(answer / 2.0, 1), "pattern": "divided_twice",
             "message": "That is half the ground distance. Check the scale: how many centimetres stand for one kilometre?"},
        ],
    }
    if ruler:
        p["ruler"] = ruler
    return p


DIRS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def direction(a, b, point, image, where, opposite):
    return {
        "hint": "Direction is measured from the first place named to the second.",
        "image": image,
        "display": "In which compass direction is <strong>%s</strong> from <strong>%s</strong>?" % (b, a),
        "options": list(DIRS),
        "solutions": [DIRS.index(point)],
        "calculator": False,
        "input_type": "multiple_choice",
        "guided_steps": [
            {"say": "Start at the place you are measuring from, or the answer comes out backwards."},
            {"pre": "Find %s, %s. Type 1 once you have it." % (a, where),
             "hint": "This is the place you measure from.",
             "answer": 1},
            {"pre": "Now find %s. Type 1 if it lies to the right of %s on the map, or 2 if it lies to the left." % (b, a),
             "hint": "Right on the map is east.",
             "answer": 1},
            {"pre": "It sits almost level with it rather than clearly above or below. Type 1 for a straight compass point, or 2 for a diagonal.",
             "done": "Little or no shift up or down keeps the answer on the cardinal point.",
             "hint": "A diagonal needs a clear shift up or down as well as across.",
             "phase": "substitute",
             "answer": 1},
        ],
        "misconceptions": [
            {"expect": DIRS.index(opposite), "pattern": "direction_reversed",
             "message": "That is the direction the other way round. Measure from the first place named to the second."},
            {"expect": DIRS.index("NE") if point == "E" else DIRS.index("E"),
             "pattern": "diagonal_overreach",
             "message": "A diagonal answer needs a clear shift up or down the map as well as across. Check how level the two really are."},
        ],
    }


RULER15 = {"cmPerKm": 2, "pxPerKm": 351}
RULER16 = {"cmPerKm": 4, "pxPerKm": 708}

REPLACE = {
    # L11 -- grid references
    (11, "bronze", 2): ref4("Chaigley Hall", 6841, CLITH, "in the lower right of the extract",
                            "Read the line down the left of the square and the line along its bottom.", 6941, 4168),
    (11, "bronze", 4): ref4("Thurne", 4016, NORFOLK, "a village in the lower right of the extract",
                            "The village name sits inside the square you want.", 4116, 1640),
    (11, "bronze", 5): ref4("Castleton", 1582, PEAK, "the largest settlement, near the middle",
                            "Find the village first, then read the two lines that name its square.", 1682, 8215),
    (11, "silver", 2): ref6("Chadswell Home Farm", 677422, CLITH, "in the upper left of the extract",
                            "Split the square into tenths each way before reading anything."),
    (11, "silver", 5): ref6("Marston Farm", 158834, PEAK, "on the main road east of the village",
                            "The farm sits where a lane meets the main road."),
    (11, "gold", 2): ref6("Losehill Hall", 154838, PEAK, "north-east of the village",
                          "Work the easting fully before starting the northing."),
    # L12 -- distance and direction
    (12, "bronze", 1): direction("Dunscar Farm", "Marston Farm", "E", PEAK,
                                 "left of centre on the extract", "W"),
    (12, "bronze", 2): dist("Woodseats", "Spring House Farm", 2.0, PEAK, RULER15,
                            "both on the higher ground north of the valley"),
    (12, "bronze", 5): dist("Long Plantation", "Nu Farm", 1.0, CLITH, RULER16,
                            "one near the top of the sheet, one to its lower right"),
    (12, "silver", 1): dist("Red Barn", "Rowter Farm", 2.5, PEAK, RULER15,
                            "one north of the valley, one to the south-west"),
    (12, "silver", 5): direction("Chadswell Home Farm", "Chaigley Hall", "SE", CLITH,
                                 "in the upper left of the extract", "NW"),
    (12, "gold", 1): dist("Castleton", "Knowlegates Farm", 1.5, PEAK, RULER15,
                          "the village, and a farm to the west of it"),
}

# The three Norfolk questions keep their text and answers; only the sheet changes.
IMAGE_ONLY = {(11, "bronze", 7): NORFOLK, (11, "silver", 6): NORFOLK, (11, "gold", 3): NORFOLK}


def rewrite(pd, n, log):
    changed = False
    for tier, items in (pd.get("problem_bank") or {}).items():
        if not isinstance(items, list):
            continue
        for i, p in enumerate(items):
            if not isinstance(p, dict):
                continue
            k = (n, tier, i)
            if k in REPLACE:
                items[i] = copy.deepcopy(REPLACE[k])
                log.append("%s[%d] replaced" % (tier, i))
                changed = True
            elif k in IMAGE_ONLY:
                if p.get("image") != IMAGE_ONLY[k]:
                    p["image"] = IMAGE_ONLY[k]
                    log.append("%s[%d] sheet swapped" % (tier, i))
                    changed = True
    return changed


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
        for l in sorted(req(B + "lessons?unit_id=eq.%s&select=id,lesson_number,practice_data" % unit["id"]),
                        key=lambda x: x["lesson_number"]):
            if l["lesson_number"] not in (11, 12):
                continue
            pd = copy.deepcopy(l.get("practice_data") or {})
            log = []
            if not rewrite(pd, l["lesson_number"], log):
                continue
            left = [m for m in RETIRE if m in json.dumps(pd)]
            if left:
                problems.append("%s L%d still references %s" % (slug, l["lesson_number"], ", ".join(left)))
            total += 1
            print("%-20s L%-3d %s" % (slug, l["lesson_number"], "; ".join(log)))
            if apply_it:
                req(B + "lessons?id=eq.%s" % l["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % l["id"])[0]["practice_data"]
                if back != pd:
                    problems.append("%s L%d write did not land" % (slug, l["lesson_number"]))

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
