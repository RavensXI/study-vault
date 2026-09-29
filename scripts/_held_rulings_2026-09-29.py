"""Tom's rulings on the held practice corrections, 29 Sep 2026 (items from scripts/_held_groups.json).

  6  Eduqas Geography Skills L13 gold 4 (Worsaw Hill): reworked. The map shows the thick 200 m
     contour, one large 210 m loop and a tiny 220 m ring right at the summit (checked on the
     zoomed map image). New question: the height of the highest contour drawn = 220.
  7  OCR L11 gold 3: keep the live question (Tom: "relatively clear ... no biggie").
  8  OCR L11 silver 2: new place inside square 6841 so no line has to be counted from off the map.
     Chaigley Hall buildings read at 682414 on the image (68 line x=522, 69 x=1236, 41 y=1117,
     42 y=413; buildings about x 955-980, y 805-825). Tolerance 1001 = one tenth either way.
 10  Unity L13 bronze 1: keep the live question (Tom: the original was right).
 14-16: waiting for Tom to listen (https://claude.ai/artifact/J4AXzVappox5J4tkoshQwC).

  python scripts/_held_rulings_2026-09-29.py          apply 6 and 8, record 7 and 10
"""
import io, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, "_studentwalk_fixdrafts_practice.json")
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}


def rest(path, method="GET", body=None):
    r = urllib.request.Request(U + "/rest/v1/" + path, headers=H, method=method,
                               data=json.dumps(body).encode() if body is not None else None)
    t = urllib.request.urlopen(r, timeout=60).read()
    return json.loads(t) if t else None


Q6 = {
    "hint": "Zoom in on the summit. The smallest ring is easy to miss.",
    "unit": "m",
    "image": "https://images.studyvault-media.co.uk/geography/os-maps/pendle-hill-z16-final.jpg",
    "display": "Worsaw Hill in the north-east of this map is circled by a thick contour labelled 200 m, and the contour interval is 10 m. What is the height of the highest contour drawn on the hill?",
    "solutions": [220],
    "calculator": False,
    "input_type": "single_value",
    "guided_steps": [
        {"say": "Each closed ring inside a contour is one interval higher than the ring outside it."},
        {"pre": "Type the number on the vertical grid line immediately to the left of Worsaw Hill.",
         "done": "Hill located, so you are reading the right summit and not one of its neighbours.",
         "hint": "The eastings read 76, 77, 78.", "answer": 77},
        {"pre": "Type how many closed rings are drawn inside the thick 200 m contour.",
         "done": "Small summit rings are easy to miss, and missing one costs you a whole interval.",
         "hint": "One is a large loop round the whole top. Look again very close to the summit before you settle on a count.",
         "phase": "substitute", "answer": 2},
        {"pre": "Start at 200 m and add 10 m for each ring you counted. Type the height of the highest ring, in metres.",
         "hint": "Two rings, two intervals.", "answer": 220},
        {"say": "Which is true of the summit?",
         "done": "The land reaches 220 m but not 230 m, or the map would have drawn a 230 m ring.",
         "hint": "Ask what the map would have done if the land reached 230 m.",
         "answer": 1,
         "choices": [{"label": "It is between 220 m and 230 m", "value": 1},
                     {"label": "It could be above 230 m", "value": 2}]},
    ],
    "misconceptions": [
        {"note": "missed the tiny summit ring", "expect": 210, "pattern": "missed_summit_ring",
         "message": "210 m is the large loop round the top. Look again right at the summit: there is a tiny ring inside it, one interval higher."},
        {"note": "went one interval past the top ring", "expect": 230, "pattern": "went_past_top_ring",
         "message": "No 230 m ring is drawn, so the land does not reach 230 m. The highest contour drawn is the tiny 220 m ring."},
        {"note": "gave the labelled contour", "expect": 200, "pattern": "gave_labelled_contour",
         "message": "200 m is the labelled contour round the hill, not the highest. Count the rings inside it."},
    ],
}

Q8 = {
    "hint": "Split the square into tenths each way before reading anything, and read from the buildings, not the name.",
    "image": "https://images.studyvault-media.co.uk/geography/os-maps/clitheroe-z16-final.jpg",
    "display": "What is the <strong>six-figure</strong> grid reference of the buildings at <strong>Chaigley Hall</strong>?",
    "solutions": [682414],
    "tolerance": 1001,
    "calculator": False,
    "input_type": "single_value",
    "guided_steps": [
        {"say": "Six figures means two readings each way: the grid line first, then the tenths across the square."},
        {"say": "Find the buildings at Chaigley Hall, south of the main road, towards the bottom right of the extract.",
         "hint": "Locate the feature before reading any numbers.", "answer": 1,
         "choices": [{"label": "I’ve found them", "value": 1}]},
        {"pre": "Read the two-figure number of the grid line down the left side of their square, then type how many tenths across the square they sit. Type all three figures together.",
         "hint": "Picture the square split into ten strips from left to right.", "answer": 682, "tolerance": 1},
        {"pre": "Now the northing the same way: the two-figure line along the bottom, then the tenths up the square. Type all three figures.",
         "hint": "Ten strips again, this time from the bottom upwards.", "answer": 414, "tolerance": 1},
        {"pre": "Put the three easting figures first, then the three northing figures, and type the six-figure reference.",
         "done": "Three figures each way, easting first. That is the whole method.",
         "hint": "Six figures, no spaces.", "post": "(6-figure ref)", "phase": "substitute", "answer": 682414, "tolerance": 1001},
    ],
    "misconceptions": [
        {"expect": 414682, "message": "Right figures, wrong order. The three easting figures always come first.",
         "pattern": "northing_before_easting"},
        {"expect": 6841, "message": "6841 is the right square, but that is a four-figure reference. Six figures needs the tenths across and up the square as well.",
         "pattern": "gave_four_figures"},
    ],
}

RULINGS = {
    "geography-eduqas::geography-eduqas/geographical-skills/13/gold/4": ("apply", Q6),
    "geography-ocr::geography-ocr/geographical-skills/11/silver/2": ("apply", Q8),
    "geography-ocr::geography-ocr/geographical-skills/11/gold/3": ("keep", None),
    "geography-unity::geography/geographical-skills/13/bronze/1": ("keep", None),
}


def main():
    drafts = json.load(io.open(DRAFTS, encoding="utf-8"))
    stamp = time.strftime("%Y-%m-%d %H:%M")
    todo = [(k, drafts[k], q) for k, (act, q) in RULINGS.items() if act == "apply"]
    backup = {d["lesson_id"]: rest("lessons?select=id,practice_data&id=eq.%s" % d["lesson_id"])[0]["practice_data"] for _, d, _ in todo}
    bpath = os.path.join(HERE, "_backup_held_rulings_%s.json" % time.strftime("%Y-%m-%d_%H%M"))
    io.open(bpath, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
    print("backup:", bpath)
    for k, d, q in todo:
        pd = json.loads(json.dumps(backup[d["lesson_id"]]))
        if pd["problem_bank"][d["tier"]][d["i"]] != d["original"]:
            sys.exit("question changed since the walk: " + k)
        pd["problem_bank"][d["tier"]][d["i"]] = q
        rest("lessons?id=eq.%s" % d["lesson_id"], "PATCH", {"practice_data": pd})
        d["draft"] = {"action": "patch", "question": q}
        d["applied"], d["hold"] = stamp, None
        d["tom"] = "29 Sep 2026: reworked per Tom"
        print("applied", k)
    for k, (act, _) in RULINGS.items():
        if act == "keep":
            drafts[k]["hold"] = "Tom 29 Sep 2026: keep the live question"
            drafts[k]["tom"] = "kept live"
            print("kept live", k)
    io.open(DRAFTS, "w", encoding="utf-8").write(json.dumps(drafts, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
