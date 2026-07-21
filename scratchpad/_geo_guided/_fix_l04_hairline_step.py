# -*- coding: utf-8 -*-
"""Stop the L04 opener walk asking students to read a hairline bar.

    python scratchpad/_geo_guided/_fix_l04_hairline_step.py --check
    python scratchpad/_geo_guided/_fix_l04_hairline_step.py --apply

Rescaling the pyramid to 100% shrank its smallest bars, so the 75+ male bar is
now 0.1% -- a hairline on an axis running to about 7. The walk asked students to
read it and then divide by it, and a misread of one tenth swings the answer from
71 to 35. It was fragile before the rescale and worse after.

Tom's call: compare against a bar you can actually read, and take a difference
rather than a ratio.

Both steps move together. Changing only the division would leave the step above
it still reading the hairline, which is the thing being removed. 60-64 sits at
0.8, readable, and far enough up the pyramid that 7.1 against 0.8 still makes
the point about a wide base and a narrow top -- the difference is 6.3 of the
base's 7.1.

The ratio in silver[3] is left alone: 4.4 against 2.0, both easily read.
"""
import copy, json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
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

OLD_READ = "Now read the male bar for 75+, the top row."
OLD_RATIO = "How many times longer is the 0-4 male bar than the 75+ male bar?"

NEW_READ = "Now read the male bar for 60-64, well up towards the top."
NEW_DIFF = "How much longer is the 0-4 male bar than the 60-64 male bar?"


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def fix(pd):
    """Rewrite both steps, taking the numbers from the chart rather than typing
       them, so this stays correct if the pyramid is ever rescaled again."""
    p = pd["problem_bank"]["bronze"][0]
    male = [abs(v) for v in p["chart"]["data"]["datasets"][0]["data"]]
    labels = p["chart"]["data"]["labels"]
    i_base, i_cmp = labels.index("0-4"), labels.index("60-64")
    base, cmp_ = male[i_base], male[i_cmp]
    diff = round(base - cmp_, 1)

    if cmp_ < 0.5:
        sys.exit("60-64 bar is %.1f, still too small to read" % cmp_)

    hits = 0
    for s in p.get("guided_steps") or []:
        if not isinstance(s, dict):
            continue
        if s.get("pre") == OLD_READ:
            s["pre"] = NEW_READ
            s["hint"] = "Count up the rows to 60-64, then read across to the scale."
            s["answer"] = cmp_
            hits += 1
        elif s.get("pre") == OLD_RATIO:
            s["pre"] = NEW_DIFF
            s["hint"] = "Subtract the shorter reading from the longer one."
            s["done"] = ("Almost the whole of the base bar: the pyramid has lost nearly all "
                         "its width by the time it reaches the older bands.")
            s["answer"] = diff
            hits += 1
    return hits, base, cmp_, diff


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
        for l in req(B + "lessons?unit_id=eq.%s&select=id,lesson_number,practice_data" % unit["id"]):
            if l["lesson_number"] != 4:
                continue
            pd = copy.deepcopy(l.get("practice_data") or {})
            hits, base, cmp_, diff = fix(pd)
            if hits != 2:
                problems.append("%s matched %d of 2 steps" % (slug, hits))
                continue
            total += 1
            print("%-20s 0-4=%.1f  60-64=%.1f  difference=%.1f" % (slug, base, cmp_, diff))
            if apply_it:
                req(B + "lessons?id=eq.%s" % l["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % l["id"])[0]["practice_data"]
                if back != pd:
                    problems.append("%s write did not land" % slug)
                st = back["problem_bank"]["bronze"][0]["guided_steps"]
                if any("75+" in str(s.get("pre", "")) for s in st):
                    problems.append("%s still reads the 75+ hairline" % slug)

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
