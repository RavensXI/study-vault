# Measure the real endcard length on a sample of affected clips (18-31 Aug).
# Decodes the last SPAN seconds, finds the last hard cut followed by flat
# frames, and reports the cut point so trim_endcard's fixed prior can be
# re-set (or replaced with a search).
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

import numpy as np

H = {'User-Agent': 'Mozilla/5.0 (StudyVault QA)'}
SPAN = 8.0
FPS = 20
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', p], capture_output=True, text=True)
    return float(r.stdout.strip())


def frames(p, start, span, fps, w=64):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{start:.3f}', '-t', f'{span:.3f}',
                        '-i', p, '-vf', f'fps={fps},scale={w}:-2', '-f', 'rawvideo',
                        '-pix_fmt', 'rgb24', '-'], capture_output=True)
    raw = r.stdout
    if not raw:
        return []
    h = next((c for c in range(80, 200) if len(raw) % (w * c * 3) == 0), None)
    if not h:
        return []
    n = len(raw) // (w * h * 3)
    a = np.frombuffer(raw, dtype=np.uint8).reshape(n, h, w, 3).astype(np.int16)
    return [(start + i / fps, a[i]) for i in range(n)]


d = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://www.studyvault.co.uk/data/_shorts_manifest.json', headers=H), timeout=90).read())
items = [i for i in (d if isinstance(d, list) else d.get('items', [])) if i.get('created_at')]
affected = sorted([i for i in items if '2026-08-18' <= i['created_at'][:10] <= '2026-08-31'],
                  key=lambda i: i['created_at'])
step = max(1, len(affected) // N)
sample = affected[::step][:N]
print(f'{len(affected)} clips in the affected range; measuring {len(sample)}\n')

lengths = []
tmp = tempfile.mkdtemp()
for i in sample:
    p = os.path.join(tmp, 'c.mp4')
    try:
        open(p, 'wb').write(urllib.request.urlopen(
            urllib.request.Request(i['url'], headers=H), timeout=180).read())
    except Exception as e:
        print('  download fail', str(e)[:60]); continue
    D = dur(p)
    fr = frames(p, max(0, D - SPAN), SPAN, FPS)
    if len(fr) < 4:
        print('  decode fail'); continue
    diffs = [(float(np.abs(fr[k][1] - fr[k - 1][1]).mean()), k) for k in range(1, len(fr))]
    # last big spike whose following frames are flat (the card)
    cut = None
    for dv, k in sorted(diffs, reverse=True)[:6]:
        after = fr[k:]
        if dv >= 8.0 and len(after) >= 3:
            std = float(np.mean([a[1].std() for a in after[:6]]))
            if std <= 28.0:
                cut = (fr[k][0], dv, std)
                break
    if cut:
        L = D - cut[0]
        lengths.append(L)
        print(f'  {i["created_at"][:10]} {i["subject"][:22]:22s} dur {D:6.2f}s  cut {cut[0]:6.2f}s'
              f'  endcard {L:4.2f}s  (diff {cut[1]:.0f}, flat std {cut[2]:.0f})')
    else:
        print(f'  {i["created_at"][:10]} {i["subject"][:22]:22s} dur {D:6.2f}s  NO CUT FOUND')
    os.remove(p)

if lengths:
    a = np.array(lengths)
    print(f'\nendcard length: n={len(a)} min {a.min():.2f} max {a.max():.2f} '
          f'mean {a.mean():.2f} median {np.median(a):.2f} std {a.std():.2f}')
