"""Print the located raw hits for a subject compactly, for hand review."""
import json
import os
import sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "voice")

slug = sys.argv[1]
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
recs = json.load(open(os.path.join(OUT, f"_raw_{slug}.json"), encoding="utf-8"))
for r in recs:
    if not (lo <= r["n"] < hi):
        continue
    print(f"--- #{r['n']}  L{r['lesson_number']}  {r['field']}  "
          f"{'narrated' if r['narrated'] else 'NO-AUDIO'}  id={r['lesson_id']}")
    print(f"    title: {r.get('title')}")
    print(f"    ...{(r.get('before') or '')[-110:]}")
    print(f"    RAW: {r.get('raw')}")
    print(f"    ...{(r.get('after') or '')[:110]}")
