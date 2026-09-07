# -*- coding: utf-8 -*-
"""Turn the three Gemini votes per recording into a consensus table.
An event is ACCEPTED only when at least 2 of the 3 votes fall inside the
tolerance window; otherwise it is marked SPLIT and the pin must be dropped or
re-probed. Writes timings.json (the audit trail Tom asked for)."""
import io, json, os, sys, glob, itertools
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))


def secs(v):
    if not isinstance(v, str):
        return None
    v = v.strip().lower()
    if v in ("none", "n/a", "", "-"):
        return None
    parts = v.split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(round(float(parts[1])))
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(round(float(parts[2])))
        return int(round(float(v)))
    except Exception:
        return None


def consensus(vals, tol):
    got = [v for v in vals if v is not None]
    if len(got) < 2:
        return None, "no votes"
    best = None
    for a, b in itertools.combinations(range(len(got)), 2):
        if abs(got[a] - got[b]) <= tol:
            grp = [x for x in got if abs(x - got[a]) <= tol or abs(x - got[b]) <= tol]
            if best is None or len(grp) > len(best):
                best = grp
    if not best:
        return None, "split %s" % got
    best = sorted(best)
    return best[len(best) // 2], "%d/%d agree %s" % (len(best), len(vals), best)


out = {}
for f in sorted(glob.glob(os.path.join(HERE, "probes", "*.json"))):
    key = os.path.splitext(os.path.basename(f))[0]
    d = json.load(io.open(f, encoding="utf-8"))
    votes = list(d["votes"].values())
    vl_key = "video_length" if any("video_length" in v for v in votes) else "audio_length"
    keys = [vl_key] + [q[0] for q in d["questions"]]
    vl_vals = [secs(v.get(vl_key)) for v in votes]
    dur, _ = consensus(vl_vals, 3)
    tol = max(3, int(0.012 * (dur or 300)))
    rows = {}
    for k in keys:
        vals = [secs(v.get(k)) for v in votes]
        val, note = consensus(vals, 3 if k == vl_key else tol)
        rows[k] = {"secs": val, "votes": vals, "verdict": note}
    out[key] = {"yt": d.get("yt") or d.get("audio"), "piece": d["piece"][:90], "tolerance_s": tol,
                "window": d.get("window"),
                "intro_notes": [v.get("intro_before_music") for v in votes], "events": rows}
    win = d.get("window")
    print("\n== %s (%s) dur=%s tol=%ds%s" % (key, (d.get("yt") or "R2 audio"), dur, tol,
          (" WINDOW %s" % (win,)) if win else ""))
    for k in keys:
        r = rows[k]
        mark = "OK " if r["secs"] is not None else "SPLIT"
        print("   %-30s %-6s %-8s %s" % (k, mark, r["secs"], r["verdict"]))

prev = {}
p = os.path.join(HERE, "timings.json")
if os.path.exists(p):
    prev = json.load(io.open(p, encoding="utf-8"))
prev.update(out)
io.open(p, "w", encoding="utf-8").write(json.dumps(prev, indent=1, ensure_ascii=False))
print("\nwritten", p)
