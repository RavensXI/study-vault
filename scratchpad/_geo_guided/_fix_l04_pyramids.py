# -*- coding: utf-8 -*-
"""Make the L04 population pyramids sum to 100% of the population.

    python scratchpad/_geo_guided/_fix_l04_pyramids.py --check
    python scratchpad/_geo_guided/_fix_l04_pyramids.py --apply

Six charts carry a "% of population" axis and their male and female bars total
125.8, 125.8, 109.3, 100.3, 102.4 and 118.5 per cent. Individually the values
look plausible, which is why this survived; collectively they describe more
people than exist. Under the other convention (percent of each sex) the totals
would need to be 100 per series, so the data is wrong either way.

Nothing here was mark-affecting -- every stored answer matches its chart -- so
this is about the geography being true, not about students losing marks.

The bars are scaled by one factor per chart, so every pyramid keeps its exact
shape: a wide base stays a wide base and the ratios the questions turn on are
preserved. Rounding to one decimal leaves a small residue, which is absorbed by
the largest bar so the total lands on 100.0 exactly.

The catch is that the guided walks read individual bars off these charts -- "read
the male bar for 0-4", "add the three female bars" -- so about twenty step
answers move as well. Those are recomputed from the scaled data by the same
formula the step describes, never hand-typed, and always from the ROUNDED values
because that is what a student actually reads off the chart. Ratios are
recomputed rather than assumed scale-invariant for the same reason: 7.2 / 0.2 is
36 even though 9 / 0.2 was 45.

bronze[3] also asked "what percentage of males are aged 40-44" against an axis
reading "% of population" -- two different denominators in one question. Reworded
to match the axis.
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


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def r1(v):
    return round(v + 1e-9, 1)


def scale_to_100(chart):
    """Scale both series by one factor so the bars total 100.0 of the population.

    Rounding 32 bars to one decimal leaves a residue of a few tenths. Dumping
    that on the single largest bar -- the obvious thing, and what this did first
    -- takes 0.6 off the base of the pyramid, which is exactly the bar the
    lesson is about: it left a "wide base" pyramid whose 0-4 male bar was
    shorter than the 5-9 bar above it.

    Largest-remainder instead: floor every bar to a tenth, then hand the spare
    tenths out one at a time to the bars with the biggest truncated fraction.
    The total is exactly 100.0 and no bar moves by as much as 0.1, so the shape
    survives intact.
    """
    dss = chart["data"]["datasets"]
    flat = [(di, i, abs(v), (-1 if v < 0 else 1))
            for di, ds in enumerate(dss) for i, v in enumerate(ds["data"])]
    total = sum(a for _, _, a, _ in flat)
    if total <= 0:
        return None
    k = 100.0 / total

    tenths = []
    for di, i, a, sign in flat:
        exact = a * k * 10.0
        base = int(exact)                      # floor to a whole tenth
        tenths.append([di, i, base, exact - base, sign])

    spare = 1000 - sum(t[2] for t in tenths)   # 100.0% expressed in tenths
    for t in sorted(tenths, key=lambda t: -t[3])[:max(0, spare)]:
        t[2] += 1

    for di, i, base, _, sign in tenths:
        dss[di]["data"][i] = r1(sign * base / 10.0)
    return k


def series(chart):
    dss = chart["data"]["datasets"]
    m = [abs(v) for v in dss[0]["data"]]
    f = [abs(v) for v in dss[1]["data"]]
    return m, f


# Each entry maps a problem to the formula behind every numeric step answer and
# its solution, expressed over the scaled data. Steps whose answer is structural
# (a row number, a count of rows) are listed as None and left alone.
def recompute(key, p):
    """Return a list of (step_index, new_answer) plus an optional new solution.

    Steps are found by matching the text of the instruction, NOT by position.
    Position looked obvious and was wrong: guided_steps opens with a `say` that
    carries no answer, so indexing by position slid every formula one step down
    and silently overwrote a row-number answer with a bar reading. A preview
    caught it. Matching on the wording the step itself uses cannot drift, and
    the assertion below fails loudly if a step is ever reworded.
    """
    m, f = series(p["chart"])
    steps = p.get("guided_steps") or []
    sol = None
    wide = max(range(16), key=lambda i: m[i])

    if key == ("bronze", 0):
        rules = [("male bar for 0-4", m[0]), ("male bar for 75+", m[15]),
                 ("times longer", r1(m[0] / m[15]) if m[15] else None),
                 ("add male and female for 0-4", r1(m[0] + f[0]))]
    elif key == ("bronze", 1):
        rules = [("Read the male bar for 0-4", m[0]), ("Read the female bar for 0-4", f[0]),
                 ("whole 0-4 band", r1(m[0] + f[0])), ("same for 30-34", r1(m[6] + f[6]))]
    elif key == ("bronze", 3):
        rules = [("male bar for 45-49", m[9]), ("male bar for 40-44", m[8]),
                 ("subtract your 40-44", r1(m[9] - m[8]))]
        sol = m[8]
    elif key == ("silver", 0):
        ms, fs = r1(m[13] + m[14] + m[15]), r1(f[13] + f[14] + f[15])
        tot = r1(ms + fs)
        rules = [("three male bars", ms), ("three female bars", fs),
                 ("Add the two totals", tot), ("Round that", int(round(tot)))]
        sol = int(round(tot))
    elif key == ("silver", 3):
        rules = [("Read the male bar for 0-4", m[0]), ("widest row", m[wide]),
                 ("times wider", r1(m[wide] / m[0]) if m[0] else None),
                 ("add male and female for 0-4", r1(m[0] + f[0]))]
    elif key == ("silver", 5):
        ms, fs = r1(sum(m[3:13])), r1(sum(f[3:13]))
        rules = [("Add the male bars", ms), ("Add the female bars", fs),
                 ("Add the two totals", r1(ms + fs))]
        sol = r1(ms + fs)
    else:
        return [], None

    out = []
    for needle, val in rules:
        if val is None:
            continue
        hits = [i for i, s in enumerate(steps)
                if isinstance(s, dict) and "answer" in s and needle.lower() in str(s.get("pre", "")).lower()]
        if len(hits) != 1:
            raise SystemExit("L04 %s[%d]: %r matched %d steps, expected 1"
                             % (key[0], key[1], needle, len(hits)))
        out.append((hits[0], val))
    return out, sol


TARGETS = [("bronze", 0), ("bronze", 1), ("bronze", 3),
           ("silver", 0), ("silver", 3), ("silver", 5)]

OLD_Q = "What percentage of males are aged 40-44?"
NEW_Q = "What percentage of the whole population are males aged 40-44?"


def fix(pd, log):
    pb = pd.get("problem_bank") or {}
    for tier, i in TARGETS:
        items = pb.get(tier)
        if not isinstance(items, list) or i >= len(items):
            continue
        p = items[i]
        if not isinstance(p, dict) or not isinstance(p.get("chart"), dict):
            continue
        before = sum(abs(v) for ds in p["chart"]["data"]["datasets"] for v in ds["data"])
        scale_to_100(p["chart"])
        after = sum(abs(v) for ds in p["chart"]["data"]["datasets"] for v in ds["data"])
        changes, sol = recompute((tier, i), p)
        steps = p.get("guided_steps") or []
        for idx, val in changes:
            if steps[idx].get("answer") != val:
                steps[idx]["answer"] = val
        if sol is not None and p.get("solutions") != [sol]:
            p["solutions"] = [sol]
        if OLD_Q in p.get("display", ""):
            p["display"] = p["display"].replace(OLD_Q, NEW_Q)
            log.append("%s[%d] reworded" % (tier, i))
        log.append("%s[%d] %.1f%%->%.1f%% steps=%d sol=%s"
                   % (tier, i, before, after, len(changes), sol))
    return True


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
            log = []
            fix(pd, log)
            # gate: every pyramid must now total 100.0
            for tier, i in TARGETS:
                ch = pd["problem_bank"][tier][i]["chart"]
                t = sum(abs(v) for ds in ch["data"]["datasets"] for v in ds["data"])
                if abs(t - 100.0) > 0.051:
                    problems.append("%s %s[%d] totals %.1f" % (slug, tier, i, t))
            total += 1
            if slug == "geography-aqa":
                for x in log:
                    print("  ", x)
            if apply_it:
                req(B + "lessons?id=eq.%s" % l["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % l["id"])[0]["practice_data"]
                if back != pd:
                    problems.append("%s write did not land" % slug)
    print()
    print("L04 rows %s: %d" % ("written" if apply_it else "to write", total))
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
