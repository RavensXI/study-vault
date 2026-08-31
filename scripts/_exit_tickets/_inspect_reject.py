# Why did a clip self-reject? Dump its tail: flatness at the expected card
# position, and the biggest frame-diff spikes in the search window.
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trim_endcard_fixed as TE  # noqa: E402

H = {'User-Agent': 'Mozilla/5.0 (StudyVault QA)'}
IDX = int(sys.argv[1]) if len(sys.argv) > 1 else 6      # 1-based, as printed

d = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://www.studyvault.co.uk/data/_shorts_manifest.json', headers=H), timeout=90).read())
items = [i for i in (d if isinstance(d, list) else d.get('items', [])) if i.get('created_at')]
aff = sorted([i for i in items if '2026-08-18' <= i['created_at'][:10] <= '2026-08-31'],
             key=lambda i: i['created_at'])
c = aff[IDX - 1]
print(f"clip {IDX}: {c['subject']}/{c['unit']}/L{c['lesson_number']}  {c['url'].split('/')[-1]}")

tmp = tempfile.mkdtemp()
p = os.path.join(tmp, 'c.mp4')
open(p, 'wb').write(urllib.request.urlopen(
    urllib.request.Request(c['url'], headers=H), timeout=300).read())
dur = TE.duration(p)
print('duration', round(dur, 2))

# flatness across the last 5 seconds
print('\nflatness by time (std over the frame; <28 = flat card):')
fr = TE._frames(p, max(0, dur - 5.0), 4.98, 10)
for t, a in fr:
    std = float(a.std(axis=(0, 1)).mean())
    mark = '  <-- FLAT' if std <= TE.FLAT_STD_MAX else ''
    print(f'  {t:6.2f}s  std {std:6.1f}{mark}')

# what the detector sees in its window
prior = dur - TE.ENDCARD
start = max(0.0, prior - TE.WINDOW)
fw = TE._frames(p, start, (dur - start) - 0.02, 30)
diffs = [(float(np.abs(fw[i][1] - fw[i - 1][1]).mean()), i) for i in range(1, len(fw))]
diffs.sort(reverse=True)
print(f'\nsearch window {start:.2f}..{dur:.2f}s — top spikes:')
for dv, i in diffs[:5]:
    after = fw[i][1]
    std = float(after.std(axis=(0, 1)).mean())
    print(f'  t={fw[i][0]:6.2f}s  diff {dv:5.1f}  post-frame std {std:6.1f}'
          f'{"  (flat)" if std <= TE.FLAT_STD_MAX else "  (not flat)"}')

for name, t in [('last', dur - 0.08), ('card_pos', dur - 1.3), ('pre_cut', dur - 3.2)]:
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'_reject_{name}.jpg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{max(0,t):.3f}',
                    '-i', p, '-frames:v', '1', out], capture_output=True)
    print('wrote', os.path.basename(out))
