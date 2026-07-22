# -*- coding: utf-8 -*-
"""Apply the vetted maths answer-box labels, per board.

    python scratchpad/_maths_legibility/_apply_maths_labels.py --check
    python scratchpad/_maths_legibility/_apply_maths_labels.py --apply

Reads _labels_<board>.json (produced and vetted by _classify_maths.py) and sets
`post` on each named step. Only labels a box that currently has no `post`, only
on the step whose answer still matches, and asserts that the ONLY change to a
lesson's practice_data is added `post` fields -- if anything else differs, the
lesson is skipped and flagged. Labels are display-only, so no answer can move;
the assertion makes that a guarantee, not a hope.
"""
import copy, glob, io, json, os, sys, urllib.request

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


def only_posts_added(before, after):
    """True iff after == before except for added 'post' strings on steps."""
    def strip_posts(pd):
        pd = copy.deepcopy(pd)
        for items in (pd.get("problem_bank") or {}).values():
            if not isinstance(items, list):
                continue
            for p in items:
                if not isinstance(p, dict):
                    continue
                for st in p.get("guided_steps") or []:
                    if isinstance(st, dict) and "post" in st:
                        del st["post"]
        return pd
    return strip_posts(before) == strip_posts(after)


def main(apply_it):
    boards = [os.path.basename(f)[len("_labels_"):-len(".json")]
              for f in sorted(glob.glob(os.path.join(HERE, "_labels_maths-*.json")))]
    grand, problems = 0, []
    for board in boards:
        labels = json.load(io.open(os.path.join(HERE, "_labels_%s.json" % board), encoding="utf-8"))
        # group labels by (unit, lesson)
        by_lesson = {}
        for r in labels:
            by_lesson.setdefault((r["unit"], r["lesson"]), []).append(r)
        sid = req(B + "subjects?slug=eq.%s&select=id" % board)[0]["id"]
        units = {u["slug"]: u["id"] for u in req(B + "units?subject_id=eq.%s&select=id,slug" % sid)}
        applied = 0
        for (uslug, ln), recs in by_lesson.items():
            uid = units.get(uslug)
            if not uid:
                problems.append("%s: unit %s missing" % (board, uslug))
                continue
            rows = req(B + "lessons?unit_id=eq.%s&lesson_number=eq.%d&select=id,practice_data" % (uid, ln))
            if not rows:
                problems.append("%s %s L%d missing" % (board, uslug, ln))
                continue
            row = rows[0]
            before = row["practice_data"]
            pd = copy.deepcopy(before)
            pb = pd.get("problem_bank") or {}
            hit = 0
            for r in recs:
                items = pb.get(r["tier"])
                if not isinstance(items, list) or r["index"] >= len(items):
                    continue
                steps = items[r["index"]].get("guided_steps") or []
                if r["step"] >= len(steps):
                    continue
                st = steps[r["step"]]
                if not isinstance(st, dict) or st.get("post"):
                    continue
                if abs(float(st.get("answer", 1e18)) - float(r["answer"])) > 1e-9:
                    continue   # step moved; skip rather than mislabel
                st["post"] = r["label"]
                hit += 1
            if hit == 0:
                continue
            if not only_posts_added(before, pd):
                problems.append("%s %s L%d: non-post diff, SKIPPED" % (board, uslug, ln))
                continue
            applied += hit
            if apply_it:
                req(B + "lessons?id=eq.%s" % row["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % row["id"])[0]["practice_data"]
                if not only_posts_added(before, back):
                    problems.append("%s %s L%d: readback shows non-post change" % (board, uslug, ln))
        print("%-16s labels %s: %d" % (board, "applied" if apply_it else "to apply", applied))
        grand += applied
    print()
    print("TOTAL %s: %d" % ("applied" if apply_it else "to apply", grand))
    if problems:
        print("PROBLEMS (%d):" % len(problems))
        for p in problems[:20]:
            print("  -", p)
        sys.exit(1)
    if apply_it:
        print("all writes verified: only post labels added, no answer touched")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        main(True)
    elif "--check" in sys.argv:
        main(False)
    else:
        sys.exit(__doc__)
