"""Test the simple idea: cut every clip at duration - 3.08s.

For each sampled clip, report the two things that decide whether a blind
fixed-offset cut is safe:

  after_flat : are ALL frames from the boundary to the end flat? (the card)
  transition : how big is the visual change across the boundary? A real cut
               into the card shows a large difference; if it is small we
               would be slicing through continuous content.
"""
import json
import os
import sys
import tempfile
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trim_endcard_fixed as TE  # noqa: E402

H = {'User-Agent': 'Mozilla/5.0 (StudyVault QA)'}
OFFSET = float(sys.argv[2]) if len(sys.argv) > 2 else 3.08
N = int(sys.argv[1]) if len(sys.argv) > 1 else 15

d = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://www.studyvault.co.uk/data/_shorts_manifest.json', headers=H), timeout=90).read())
items = [i for i in (d if isinstance(d, list) else d.get('items', [])) if i.get('created_at')]
aff = sorted([i for i in items if '2026-08-18' <= i['created_at'][:10] <= '2026-08-31'],
             key=lambda i: i['created_at'])
step = max(1, len(aff) // N)
sample = aff[::step][:N]

tmp = tempfile.mkdtemp()
good = 0
trans = []
for i in sample:
    p = os.path.join(tmp, 'c.mp4')
    try:
        open(p, 'wb').write(urllib.request.urlopen(
            urllib.request.Request(i['url'], headers=H), timeout=240).read())
    except Exception as e:
        print('  download fail', str(e)[:50]); continue
    dur = TE.duration(p)
    b = dur - OFFSET
    after = TE._frames(p, b + 0.06, OFFSET - 0.12, 15)
    before = TE._frames(p, max(0.0, b - 0.40), 0.34, 15)
    if not after or not before:
        print('  decode fail'); os.remove(p); continue
    all_flat = all(TE._flat(a) for _, a in after)
    diff = float(np.abs(after[1][1].astype(np.int16) - before[-1][1].astype(np.int16)).mean())
    trans.append(diff)
    ok = all_flat and diff >= 8.0
    good += ok
    print(f"  {i['subject'][:26]:26s} dur {dur:6.2f}  after_flat {str(all_flat):5s}  "
          f"transition {diff:5.1f}  {'OK' if ok else 'NO'}")
    os.remove(p)

print(f"\noffset {OFFSET}s: {good}/{len(trans)} clips show an all-flat card after the "
      f"boundary AND a clear transition across it")
if trans:
    t = np.array(trans)
    print(f"transition size: min {t.min():.1f} mean {t.mean():.1f} max {t.max():.1f}")
