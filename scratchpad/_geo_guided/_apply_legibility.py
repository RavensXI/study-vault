# -*- coding: utf-8 -*-
"""Apply the verified geography-skills legibility fixes to the canonical AQA rows.

    python scratchpad/_geo_guided/_apply_legibility.py --check
    python scratchpad/_geo_guided/_apply_legibility.py --apply

Four kinds of change, all keyed by (lesson, tier, index, step) against the stored
order (which is stable; the shuffle is client-side):

  1. LABEL boxes so the student knows what to type:
     - the 30 genuine "as a decimal / share" boxes  -> "(a decimal)"
     - two L04 bar-reading boxes on a % axis          -> "%"
     - two L04 population counts framed "how many million" -> "million"
     - the final grid-reference box in every L11 problem -> "(4-figure ref)" / "(6-figure ref)"
  2. REWORD the magnitude traps so the multiplicand is not itself a "billion"
     the student then tries to type. bronze[6] is Tom's reported bug.
  3. REWORD the verb-less "Check: X the same way =" fragments into instructions.
  4. Fix two loose-wording steps a reader flagged (compass never names the point;
     the isotherm "lowest whole P could be").

Nothing changes an ANSWER. Every rewrite keeps the stored answer; only the prose,
the box label, and the done-note move. Verified afterwards by the play-through
harness (every answer still accepted) and the legibility scan (magnitude traps
gone).
"""
import copy, io, json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
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


# ---- 1a. decimal labels (30 steps) ---------------------------------------
DEC = json.load(io.open(os.path.join(HERE, "_decimal_labels.json"), encoding="utf-8"))
LABELS = {}  # (n,tier,i,step) -> {"post": "..."}
for d in DEC:
    LABELS[(d["lesson"], d["tier"], d["index"], d["step"])] = {"post": "(a decimal)"}

# ---- 1b. specific unit labels --------------------------------------------
for key, post in {
    (4, "bronze", 0, 3): "%", (4, "bronze", 3, 4): "%",     # bar readings on a % axis
    (4, "gold", 0, 3): "million", (4, "gold", 0, 4): "million",
    (9, "bronze", 6, 4): "thousand", (9, "silver", 1, 2): "thousand",  # flow-line magnitudes
}.items():
    LABELS.setdefault(key, {})["post"] = post

# ---- 2 + 3 + 4. rewrites --------------------------------------------------
# Each entry replaces named fields on that step. Answers are never touched.
REWRITES = {
    # bronze[6] -- Tom's pie chart
    (2, "bronze", 6, 4): {
        "pre": "Multiply your decimal by 500 (the total, counted in billions of litres): ",
        "post": "billion litres"},
    (2, "bronze", 6, 5): {
        "pre": "Now check it. Work out agriculture too: 0.7 of the same 500. Type its usage: ",
        "post": "billion litres",
        "done": "Agriculture 350, industry 100 and domestic 50 rebuild the whole 500 billion litres, so the shares were applied correctly."},
    # L04 dependency-ratio millions
    (4, "gold", 0, 3): {"pre": "The country has 60 million people. How many of them, in millions, are dependants? "},
    (4, "gold", 0, 4): {"pre": "And how many, in millions, are of working age? "},
    # L02 "check ... the same way =" fragments -> instructions
    (2, "silver", 0, 6): {
        "pre": "Check it by working out the tertiary sector the same way. Type its people count: ", "post": "people"},
    (2, "silver", 1, 5): {
        "pre": "Check it by working out the angle for vans the same way. Type it: ", "post": "degrees"},
    (2, "silver", 4, 5): {
        "pre": "Check it by working out the abrasion events the same way. Type the count: ", "post": "events"},
    (2, "gold", 1, 6): {
        "pre": "Check it by working out the 10-20 class the same way. Type its value: "},
    # L12 bronze[1] -- name the compass point at the end
    (12, "bronze", 1, 3): {
        "done": "Right on the map and level means due East, a straight compass point. Back on the question, that is the E option."},
    # L08 silver[5] -- why 8 and not 9
    (8, "silver", 5, 4): {
        "pre": "P is only just warmer than 8°C, so 8 is the coldest value it comes near. For the SMALLEST possible difference, use 8. Type it, in °C: "},
}


def is_ref(v, length):
    return isinstance(v, int) and len(str(v)) == length


def apply_to_lesson(n, pd, log):
    changed = False
    pb = pd.get("problem_bank") or {}
    for tier, items in pb.items():
        if not isinstance(items, list):
            continue
        for i, p in enumerate(items):
            if not isinstance(p, dict):
                continue
            steps = p.get("guided_steps") or []
            sol = (p.get("solutions") or [None])[0]
            for si, st in enumerate(steps):
                if not isinstance(st, dict):
                    continue
                k = (n, tier, i, si)
                if k in LABELS and not st.get("post"):
                    st["post"] = LABELS[k]["post"]
                    log.append("label %s %s[%d].s%d = %r" % (n, tier, i, si, st["post"]))
                    changed = True
                if k in REWRITES:
                    for fld, val in REWRITES[k].items():
                        st[fld] = val
                    log.append("reword %s %s[%d].s%d" % (n, tier, i, si))
                    changed = True
            # grid-reference label on the step that produces the answer, L11 only
            if n == 11 and sol is not None:
                for si, st in enumerate(steps):
                    if isinstance(st, dict) and st.get("answer") == sol and not st.get("post"):
                        length = len(str(sol))
                        if length in (4, 6):
                            st["post"] = "(%d-figure ref)" % length
                            log.append("ref-label 11 %s[%d].s%d = %r" % (tier, i, si, st["post"]))
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
            pd = copy.deepcopy(l.get("practice_data") or {})
            log = []
            if not apply_to_lesson(n, pd, log):
                continue
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
    print("lessons %s: %d" % ("written" if apply_it else "to change", rows))
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
