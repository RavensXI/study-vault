# -*- coding: utf-8 -*-
"""Act on what the blind checkers found.

    python scratchpad/_geo_guided/_fix_checker_findings.py --check
    python scratchpad/_geo_guided/_fix_checker_findings.py --apply

Three defects, all mine, none of which the earlier passes caught.

1. L12 bronze[5] named "Nu Farm" as a distance endpoint. clitheroe-z16 carries
   TWO separate Nu Farm labels about 0.8 km apart, each with its own buildings,
   giving different answers. The question is unanswerable. I listed both labels
   when I read that sheet and did not notice they were the same name.
   -> Chadswell Home Farm to Darwens Farm, measured 1.48 km, so 1.5 to the
      nearest half. Both names appear once.

2. L11 bronze[5] asked which square contains Castleton. The village straddles
   the 83 northing almost evenly -- 276 building pixels north of the line
   against 310 south -- so neither 1582 nor 1583 is right, and four-figure
   answers are matched exactly with no tolerance.
   -> Dunscar Farm, which sits 0.28 across and 0.51 up its square, comfortably
      inside 1483. Located independently by a checker, so the name is not
      duplicated.

3. L11 silver[6] stored 407183 for Low Farm. Two independent measurements put
   the northing tenth at 1 (fraction 0.198, sub-pixel from the boundary) and 2.
   Six-figure answers allow one either way, so 183 would mark a correct reading
   of 181 wrong.
   -> 407182, whose window covers 181 to 183.

Also softened, rather than left to assert something contestable: two L14
questions stated "Castleton lies in grid square 1582". Those questions are about
what the square contains, not about which square the village is in, so the claim
was doing no work and is removed.
"""
import copy, importlib.util, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
R2 = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
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

# reuse the question builders rather than restating their shape
spec = importlib.util.spec_from_file_location("rb", os.path.join(HERE, "_retire_broken_maps.py"))
rb = importlib.util.module_from_spec(spec)
_argv = sys.argv            # restore: clobbering argv made this script ignore its own flags
sys.argv = ["_"]
spec.loader.exec_module(rb)
sys.argv = _argv


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


NEW_B5 = rb.ref4("Dunscar Farm", 1483, rb.PEAK, "left of centre, north of the valley road",
                 "Read the line down the left of its square and the line along its bottom.",
                 1383, 8314)
NEW_L12_B5 = rb.dist("Chadswell Home Farm", "Darwens Farm", 1.5, rb.CLITH, rb.RULER16,
                     "one in the upper left of the sheet, the other over to the right")

# L14: stop asserting which square the village is in
L14_EDITS = [
    (14, "bronze", 7,
     [("Castleton lies in grid square <strong>1582</strong>. The square directly north of it is <strong>1583</strong>. Which of the two has more contour lines crossing it?",
       "Compare grid squares <strong>1582</strong> and <strong>1583</strong>, one directly above the other on this extract. Which of the two has more contour lines crossing it?"),
      ("Square 1582 holds the village on the valley floor and the ground rising south of it. Type 1 if that rising ground carries many brown lines, or 2 if it carries almost none.",
       "Square 1582 holds valley floor and the ground rising south of it. Type 1 if that rising ground carries many brown lines, or 2 if it carries almost none."),
      ("The village square also contains the steep side of the dale, and that is where most of its contour lines are.",
       "That square also contains the steep side of the dale, and that is where most of its contour lines are."),
      ("1582, the square containing the village", "1582, the lower square")]),
    (14, "gold", 2,
     [("The village of <strong>Castleton</strong> lies in grid square <strong>1582</strong>. Which combination of map evidence best explains why a village grew on this spot?",
       "The village of <strong>Castleton</strong> sits on the valley floor near the middle of this extract. Which combination of map evidence best explains why a village grew on this spot?"),
      ("Find square 1582 and look at what runs through the village. Type 1 if a road passes through it, or 2 if none does.",
       "Find Castleton and look at what runs through the village. Type 1 if a road passes through it, or 2 if none does.")]),
]


def apply_edits(p, pairs, log, tag):
    blob = json.dumps(p, ensure_ascii=False)
    hits = 0
    for old, new in pairs:
        if old in blob:
            blob = blob.replace(old, new)
            hits += 1
    if hits != len(pairs):
        log.append("%s: matched %d of %d edits" % (tag, hits, len(pairs)))
    return json.loads(blob), hits


def fix(pd, n, log):
    changed = False
    pb = pd.get("problem_bank") or {}
    if n == 11:
        pb["bronze"][5] = copy.deepcopy(NEW_B5)
        log.append("L11 bronze[5] -> Dunscar Farm 1483")
        s6 = pb["silver"][6]
        if s6.get("solutions") == [407183]:
            s6["solutions"] = [407182]
            for st in s6.get("guided_steps") or []:
                if st.get("answer") == 407183:
                    st["answer"] = 407182
                elif st.get("answer") == 183:
                    st["answer"] = 182
            log.append("L11 silver[6] 407183 -> 407182")
        changed = True
    if n == 12:
        pb["bronze"][5] = copy.deepcopy(NEW_L12_B5)
        log.append("L12 bronze[5] -> Chadswell Home Farm to Darwens Farm, 1.5 km")
        changed = True
    if n == 14:
        for (ln, tier, idx, pairs) in L14_EDITS:
            if ln != 14:
                continue
            newp, hits = apply_edits(pb[tier][idx], pairs, log, "L14 %s[%d]" % (tier, idx))
            pb[tier][idx] = newp
            if hits:
                log.append("L14 %s[%d] de-asserted the village square (%d edits)" % (tier, idx, hits))
                changed = True
    return changed


def main(apply_it):
    problems, rows = [], 0
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
            n = l["lesson_number"]
            if n not in (11, 12, 14):
                continue
            pd = copy.deepcopy(l.get("practice_data") or {})
            log = []
            if not fix(pd, n, log):
                continue
            blob = json.dumps(pd)
            if "Nu Farm" in blob and n == 12:
                problems.append("%s L12 still names Nu Farm" % slug)
            if "grid square <strong>1582</strong>" in blob and n == 14:
                problems.append("%s L14 still asserts the village square" % slug)
            rows += 1
            if slug == "geography-aqa":
                for x in log:
                    print("  ", x)
            if apply_it:
                req(B + "lessons?id=eq.%s" % l["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % l["id"])[0]["practice_data"]
                if back != pd:
                    problems.append("%s L%d write did not land" % (slug, n))
    print()
    print("rows %s: %d" % ("written" if apply_it else "to write", rows))
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
