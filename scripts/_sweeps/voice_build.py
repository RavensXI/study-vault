"""
Build an edits file for voice_pass.py from fragment swaps against the RAW hit
text located by voice_locate.py.

Typing a raw sentence out by hand risks a silent transcription slip (curly
quotes, en dashes, &ldquo; vs "), so the `find` string is ALWAYS taken
byte-for-byte from _raw_<subject>.json; only the fragment being changed is
typed, and it must occur exactly once inside that sentence.

    echo '{"pairs": [[0, "old fragment", "new fragment"]],
           "skipped": [[3, "false positive - describes the task, not examiners"]]}' \
      | python scripts/_sweeps/voice_build.py <subject>
"""
import json
import os
import sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
# the spec arrives on stdin and carries curly quotes / en dashes verbatim
spec_text = sys.stdin.buffer.read().decode("utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "voice")

slug = sys.argv[1]
spec = json.loads(spec_text)
recs = {r["n"]: r for r in json.load(open(os.path.join(OUT, f"_raw_{slug}.json"), encoding="utf-8"))}

edits, problems = [], []
for n, old, new in spec.get("pairs", []):
    r = recs[n]
    raw = r["raw"]
    # a fragment may run past the flagged sentence (rewriting a subject that the
    # NEXT sentence pronominalises); the find then stretches to cover it
    window = raw + (r.get("after") or "")
    swaps = list(zip(old, new)) if isinstance(old, list) else [(old, new)]
    end, bad, inside = len(raw), False, False
    for o, _nw in swaps:
        if window.count(o) != 1:
            problems.append(f"#{n}: fragment occurs {window.count(o)}x in the sentence: {o!r}\n     {raw!r}")
            bad = True
            continue
        i = window.index(o)
        inside = inside or i < len(raw)
        end = max(end, i + len(o))
    if not bad and not inside:
        problems.append(f"#{n}: no fragment touches the flagged sentence")
        bad = True
    if bad:
        continue
    find = window[:end]
    rep = find
    for o, nw in swaps:
        rep = rep.replace(o, nw, 1)
    edits.append({"lesson_id": r["lesson_id"], "field": r["field"], "n": n,
                  "find": find, "replace": rep})
skipped = [{"lesson_id": recs[n]["lesson_id"], "lesson_number": recs[n]["lesson_number"],
            "field": recs[n]["field"], "reason": why, "sentence": recs[n]["plain"]}
           for n, why in spec.get("skipped", [])]

covered = {e["n"] for e in edits} | {n for n, _ in spec.get("skipped", [])}
missing = sorted(set(recs) - covered)
if problems:
    print("PROBLEMS:\n" + "\n".join(problems))
    sys.exit(1)
if missing:
    print(f"WARNING: {len(missing)} hit(s) neither rewritten nor skipped: {missing}")

path = os.path.join(OUT, f"edits_{slug}.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump({"subject": slug, "edits": edits, "skipped": skipped}, f, ensure_ascii=False, indent=1)
print(f"{slug}: {len(edits)} edits, {len(skipped)} skipped -> {path}")
for e in edits:
    print(f"  #{e['n']} L? {e['field']}\n    - {e['find'][:190]}\n    + {e['replace'][:190]}")
