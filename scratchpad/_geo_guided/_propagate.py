# -*- coding: utf-8 -*-
"""Propagate the canonical geography-aqa Geography Skills lessons to the other
five subject variants that share the same 12 lessons.

    python _propagate.py --check     # report only, change nothing
    python _propagate.py --apply     # write, then verify by re-reading

The 72 rows are 12 distinct lessons x 6 subjects (aqa, edexcel-a, edexcel-b,
ocr, eduqas, and Unity's bespoke `geography`). The content is board-neutral by
spec, so the canonical row is copied verbatim. Unity's row is a school row
(school_id set) and is included deliberately: the science-calculation
propagation established the same identity model.

Safety: only ever writes the practice_data column, only to rows whose id is in
the pre-dump for that lesson key, and refuses to run if the canonical row has
not been converted (no `guided` block).
"""
import io, json, os, sys, time, urllib.error, urllib.request

BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(HERE, "..", "_geo_audit", "_pre_dump_all.json")
CANON = "geography-aqa"

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY,
     "Content-Type": "application/json"}


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(r, timeout=90) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw.strip() else None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))


def get_pd(row_id):
    d = req(BASE + "lessons?id=eq.%s&select=practice_data" % row_id)
    return (d[0]["practice_data"] if d else None)


def is_converted(pd):
    return bool(pd) and bool(pd.get("guided")) and bool(pd.get("tier_guides"))


def main(apply_it):
    dump = json.load(io.open(PRE, encoding="utf-8"))
    by_key = {}
    for r in dump:
        by_key.setdefault(r["key"], []).append(r)

    total_written = 0
    problems = []

    for key in sorted(by_key):
        rows = by_key[key]
        canon = next((r for r in rows if r["subject"] == CANON), None)
        if not canon:
            problems.append("%s: no canonical %s row" % (key, CANON))
            continue

        src = get_pd(canon["id"])
        if not is_converted(src):
            problems.append("%s: canonical row not converted yet (no guided/tier_guides), skipped" % key)
            continue

        targets = [r for r in rows if r["subject"] != CANON]
        same, differ = [], []
        for t in targets:
            cur = get_pd(t["id"])
            (same if cur == src else differ).append(t)

        print("%s  canonical OK  targets=%d  already-identical=%d  to-write=%d"
              % (key, len(targets), len(same), len(differ)))

        if apply_it:
            for t in differ:
                req(BASE + "lessons?id=eq.%s" % t["id"], method="PATCH",
                    body={"practice_data": src},
                    extra={"Prefer": "return=minimal"})
                total_written += 1
            # verify by re-reading, never trust the write
            bad = [t["subject"] for t in differ if get_pd(t["id"]) != src]
            if bad:
                problems.append("%s: post-write mismatch on %s" % (key, ", ".join(bad)))
            else:
                if differ:
                    print("    wrote %d, all verified identical to canonical" % len(differ))

    print()
    if apply_it:
        print("rows written: %d" % total_written)
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
