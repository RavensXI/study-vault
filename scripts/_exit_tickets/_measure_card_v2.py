"""Measure the endcard length properly, using the FIXED frame decoder.

Walks back from the end over the trailing run of flat frames. No spike
hunting, no assumed constant - just: where does the still card begin?
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
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12

d = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://www.studyvault.co.uk/data/_shorts_manifest.json', headers=H), timeout=90).read())
items = [i for i in (d if isinstance(d, list) else d.get('items', [])) if i.get('created_at')]
aff = sorted([i for i in items if '2026-08-18' <= i['created_at'][:10] <= '2026-08-31'],
             key=lambda i: i['created_at'])
step = max(1, len(aff) // N)
sample = aff[::step][:N]

tmp = tempfile.mkdtemp()
lens = []
for i in sample:
    p = os.path.join(tmp, 'c.mp4')
    try:
        open(p, 'wb').write(urllib.request.urlopen(
            urllib.request.Request(i['url'], headers=H), timeout=240).read())
    except Exception as e:
        print('  download fail', str(e)[:50]); continue
    dur = TE.duration(p)
    # sample the last 6s at 25fps with the fixed decoder
    fr = TE._frames(p, max(0.0, dur - 6.0), min(6.0, dur - 0.5), 25)
    if len(fr) < 20:
        print('  decode fail'); os.remove(p); continue
    flags = [TE._flat(a) for _, a in fr]
    if not flags[-1]:
        print(f"  {i['subject'][:24]:24s} does NOT end flat"); os.remove(p); continue
    k = len(flags) - 1
    while k >= 0 and flags[k]:
        k -= 1
    card = dur - fr[k + 1][0]
    lens.append(card)
    print(f"  {i['created_at'][:10]} {i['subject'][:24]:24s} dur {dur:6.2f}  "
          f"card starts {fr[k + 1][0]:6.2f}  length {card:5.2f}s")
    os.remove(p)

if lens:
    a = np.array(lens)
    print(f"\nn={len(a)}  min {a.min():.2f}  max {a.max():.2f}  "
          f"mean {a.mean():.2f}  median {np.median(a):.2f}  std {a.std():.3f}")
