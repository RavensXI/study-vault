# -*- coding: utf-8 -*-
"""Manifest for the headless play-through, plus the checks that need no browser.

    python scratchpad/_geo_guided/_playcheck_build.py

Two things a paper check cannot tell you:

  - whether typing the intended answer is actually marked correct by the real
    checkAnswer(), with its tolerances, its unit handling and its shuffled
    multiple-choice indices. Options are rendered in a shuffled order and mapped
    back through data-idx, so a solution index that drifted during a rewrite
    would look right in the JSON and be wrong on screen.
  - whether the guided walk lands on the answer it is walking towards. A walk
    whose last substitute step disagrees with the stored solution teaches one
    number and marks another.

The second needs no browser and is done here. The first is emitted as a manifest
for _playcheck_probe.html to drive.
"""
import io, json, os, re, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

AUTHORED = {
    4:  [("bronze", 0), ("bronze", 1), ("bronze", 3), ("silver", 0), ("silver", 3), ("silver", 5)],
    11: [("bronze", 2), ("bronze", 4), ("bronze", 5), ("silver", 2), ("silver", 5), ("gold", 2),
         ("bronze", 7), ("silver", 6), ("gold", 3)],
    12: [("silver", 4), ("bronze", 1), ("bronze", 2), ("bronze", 5), ("silver", 1),
         ("silver", 5), ("gold", 1)],
    13: [("bronze", 4)],
    14: [("bronze", 3), ("bronze", 7), ("silver", 2), ("silver", 6), ("gold", 2)],
}


def req(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    subj = req(B + "subjects?slug=eq.geography-aqa&select=id")[0]["id"]
    unit = [u for u in req(B + "units?subject_id=eq.%s&select=id,slug" % subj)
            if u["slug"] == "geographical-skills"][0]["id"]
    lessons = {l["lesson_number"]: l for l in
               req(B + "lessons?unit_id=eq.%s&select=lesson_number,practice_data" % unit)}

    manifest, problems = [], 0
    walk_fail, no_walk, leak, unread = [], [], [], []

    for n, picks in sorted(AUTHORED.items()):
        pb = (lessons[n].get("practice_data") or {}).get("problem_bank") or {}
        for tier, i in picks:
            p = pb[tier][i]
            problems += 1
            sol = (p.get("solutions") or [None])[0]
            # _problemBank is SHUFFLED on load, so the database index is not the
            # position the player uses -- match on the question text instead.
            # It must be the FULL text: every four-figure question opens with the
            # same 60 characters, so a prefix match silently selected a different
            # question and then reported the right answer as rejected.
            key = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", p.get("display") or "")).strip()
            manifest.append({"lesson": n, "tier": tier, "index": i, "solution": sol,
                             "input_type": p.get("input_type") or "single_value",
                             "match": key})   # full text: 60 chars collided

            steps = [s for s in (p.get("guided_steps") or []) if isinstance(s, dict)]
            subs = [s for s in steps if s.get("phase") == "substitute"]
            tag = "L%d %s[%d]" % (n, tier, i)

            # The walk must PRODUCE the answer somewhere along the way.
            #
            # Checking the last substitute step instead -- the obvious reading --
            # failed five sound questions. "substitute" marks where the completion
            # card hands over to the student, not where the walk ends, and several
            # walks close on a deliberate verification step ("type the last two
            # figures"). So the invariant is that the solution appears as some
            # step's answer, not that it is the final one.
            if not subs:
                no_walk.append(tag)
            elif p.get("input_type") != "multiple_choice" and isinstance(sol, (int, float)):
                reached = any(isinstance(s.get("answer"), (int, float))
                              and abs(float(s["answer"]) - float(sol)) < 0.011 for s in steps)
                if not reached:
                    walk_fail.append("%s: solution %s never reached; walk gives %s"
                                     % (tag, sol, [s.get("answer") for s in steps if "answer" in s]))

            # no message may hand over the answer
            for mc in (p.get("misconceptions") or []):
                if not isinstance(mc, dict):
                    continue
                msg = str(mc.get("message", "")).lower()
                if sol is not None and len(str(sol)) > 2 and str(sol).lower() in msg:
                    leak.append("%s: misconception contains %s" % (tag, sol))
            for s in steps:
                for fld in ("say", "pre", "hint"):
                    t = str(s.get(fld, "")).lower()
                    if sol is not None and len(str(sol)) > 2 and str(sol).lower() in t:
                        leak.append("%s: step %s contains %s" % (tag, fld, sol))

            # a value too small to read off its own chart
            ch = p.get("chart")
            if isinstance(ch, dict):
                vals = [abs(v) for ds in (ch.get("data") or {}).get("datasets", [])
                        for v in ds.get("data", []) if isinstance(v, (int, float))]
                if vals:
                    span = max(vals)
                    for s in steps:
                        a = s.get("answer")
                        if isinstance(a, (int, float)) and 0 < a < span * 0.10 \
                                and any(abs(a - v) < 1e-9 for v in vals):
                            unread.append("%s: step asks to read %s off an axis to %.1f" % (tag, a, span))

    io.open(os.path.join(HERE, "_playcheck_manifest.json"), "w", encoding="utf-8").write(
        json.dumps(manifest, indent=1))

    print("authored problems: %d" % problems)
    print()
    for name, rows in (("walk does not land on the solution", walk_fail),
                       ("answer leaked into a message", leak),
                       ("value too small to read", unread),
                       ("no substitute step (walk cannot complete)", no_walk)):
        print("%-42s %d" % (name, len(rows)))
        for r in rows[:8]:
            print("    -", r)
    print()
    print("manifest written for the browser pass")
    if walk_fail or leak or unread:
        sys.exit(1)


if __name__ == "__main__":
    main()
