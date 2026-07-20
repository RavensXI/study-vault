# -*- coding: utf-8 -*-
"""Finish L13/L14: repair the one confirmed defect, then propagate to all six variants.

    python scratchpad/_geo_guided/_finish_l13_l14.py --check
    python scratchpad/_geo_guided/_finish_l13_l14.py --apply

The checker on L13 confirmed one fail: silver[4].guided_steps[4].done claims one
contour gap is crossed "across most of a square". Measured on
pendle-hill-z16-final.jpg the grid is 713 px per km and the northern gaps are
19-39 px, about a eighteenth of a square. The stored answer and both box values
are correct; only the description overstates. Rewritten to state the method
without asserting a magnitude the sheet does not support.

The main _propagate.py keys off the pre-fanout dump, which has no entry for
lessons that did not exist, so these two propagate here by explicit id.
"""
import io, json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

CANON = {"L13": "55ede5fd-81e7-43de-95ed-d0b3bb681d06",
         "L14": "aae0e652-fbec-4f5d-b06a-abfea8eeb630"}
TARGETS = {
    "L13": ["b59b539e-6708-4ca0-93bd-577793ebf957", "26042cc8-c877-4a09-97d2-dab4c47bfe44",
            "5af3945f-def9-4554-805d-5427b2bc222c", "5c3592fd-1546-43f7-afec-f152e66ec078",
            "838423a7-abfc-461c-aa23-15174b8eded0"],
    "L14": ["fabe8a83-8dfc-426a-bd9a-5a682fc2a968", "997c917e-aeb5-4b74-b03e-18fc40bc9e6f",
            "8f0701fd-8577-4edf-8e25-02cb8e70e964", "eae20efa-7686-452e-9b52-5de06d4d3c94",
            "38ebdfd6-beb6-43bf-9570-7b35a202148a"],
}

OLD_DONE = ("One interval crossed in a few millimetres on one side and across most of a "
            "square on the other. That is the comparison the question wants.")
NEW_DONE = ("The same height gap is crossed in a shorter walk on one side than the other. "
            "Closer contours mean the ground rises more sharply, and that is the comparison "
            "the question wants.")

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
    with urllib.request.urlopen(r, timeout=90) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def get_pd(rid):
    d = req(B + "?id=eq.%s&select=practice_data" % rid)
    return d[0]["practice_data"] if d else None


def main(apply_it):
    problems = []

    # ---- 1. repair the L13 done note -------------------------------------
    pd13 = get_pd(CANON["L13"])
    step = pd13["problem_bank"]["silver"][4]["guided_steps"][4]
    if step.get("done") == OLD_DONE:
        print("L13 silver[4].guided_steps[4].done: overstated claim found")
        if apply_it:
            step["done"] = NEW_DONE
            req(B + "?id=eq.%s" % CANON["L13"], method="PATCH",
                body={"practice_data": pd13}, extra={"Prefer": "return=minimal"})
            back = get_pd(CANON["L13"])
            ok = back["problem_bank"]["silver"][4]["guided_steps"][4].get("done") == NEW_DONE
            print("   repaired and verified:", ok)
            if not ok:
                problems.append("L13 done-note write did not land")
            pd13 = back
    elif step.get("done") == NEW_DONE:
        print("L13 done note already repaired")
    else:
        problems.append("L13 done note is neither the old nor the new text; left alone")
        print("   !!", repr(step.get("done"))[:100])

    # ---- 2. propagate both to the five variants --------------------------
    for key, rid in CANON.items():
        src = get_pd(rid)
        if not src or not src.get("guided"):
            problems.append("%s canonical row has no guided block; not propagated" % key)
            continue
        differ = [t for t in TARGETS[key] if get_pd(t) != src]
        print("%s  targets=%d  already-identical=%d  to-write=%d"
              % (key, len(TARGETS[key]), len(TARGETS[key]) - len(differ), len(differ)))
        if apply_it and differ:
            for t in differ:
                req(B + "?id=eq.%s" % t, method="PATCH",
                    body={"practice_data": src}, extra={"Prefer": "return=minimal"})
            bad = [t for t in differ if get_pd(t) != src]
            if bad:
                problems.append("%s: post-write mismatch on %d row(s)" % (key, len(bad)))
            else:
                print("    wrote %d, all verified identical to canonical" % len(differ))

    print()
    if problems:
        print("PROBLEMS (%d):" % len(problems))
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        main(True)
    elif "--check" in sys.argv:
        main(False)
    else:
        sys.exit(__doc__)
