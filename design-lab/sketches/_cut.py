"""Cut the single sketches.jpg sheet into individual transparent PNGs.
Auto-segments by connected components (dilation joins each item's strokes),
masks to each component (no neighbour bleed), white -> transparent."""
from PIL import Image, ImageDraw
import numpy as np, os
from scipy import ndimage

SRC = r'C:/Users/tshau/Documents/Study Vault/sketches.jpg'
OUT = os.path.join(os.path.dirname(__file__), 'cut')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):  # clear old cutouts
    if f.endswith('.png'):
        os.remove(os.path.join(OUT, f))

im = Image.open(SRC).convert('RGB')
rgb = np.asarray(im)
gray = rgb.mean(2)
ink = gray < 205
dil = ndimage.binary_dilation(ink, structure=np.ones((13, 13)))
lbl, n = ndimage.label(dil)
comps = [i for i in range(1, n + 1) if (lbl == i).sum() > 1200]

def bbox(i):
    ys, xs = np.where(lbl == i)
    return xs.min(), ys.min(), xs.max(), ys.max()

comps.sort(key=lambda i: (bbox(i)[1] // 40, bbox(i)[0]))  # reading order
alpha_full = np.clip((255 - gray) * 1.5, 0, 255).astype(np.uint8)
H, W = gray.shape
Xc = np.arange(W)[None, :].repeat(H, 0)  # x-coordinate grid

cuts, pad = [], 6
counter = [0]

def save_mask(mask, name):
    ys, xs = np.where(mask)
    if len(xs) < 500:
        return
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(W - 1, x1 + pad), min(H - 1, y1 + pad)
    m = mask[y0:y1 + 1, x0:x1 + 1]
    al = np.where(m, alpha_full[y0:y1 + 1, x0:x1 + 1], 0).astype(np.uint8)
    rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], al])
    p = os.path.join(OUT, f'{name}.png')
    Image.fromarray(rgba, 'RGBA').save(p)
    cuts.append((name, x1 - x0, y1 - y0, p))
    print(f'{name}  box=({x0},{y0},{x1},{y1})  size=({x1-x0}x{y1-y0})')

NAMES = ['timetable', 'mindmap', 'flashcards', 'highlighters', 'pen', 'compass',
         'eraser', 'highlighter', 'ruler', 'notebook', 'scissors', 'pencil',
         'gluestick', 'stapler', 'flashcards2', 'calculator', 'stickynotes', 'paperclips']

def nextname():
    n = NAMES[counter[0]] if counter[0] < len(NAMES) else f'item-{counter[0]:02d}'
    counter[0] += 1
    return n

for i in comps:
    x0, y0, x1, y1 = bbox(i)
    w, h = x1 - x0, y1 - y0
    if w > 650 and h > 750:        # full-page faint scrap -> skip
        continue
    m = (lbl == i)
    if y0 < 400 and w > 400:        # timetable + mind map -> split vertically
        save_mask(m & (Xc < 393), nextname())
        save_mask(m & (Xc >= 393), nextname())
    elif y0 > 770 and x1 < 300 and w > 100:  # flashcards + calculator -> split
        save_mask(m & (Xc < 190), nextname())
        save_mask(m & (Xc >= 190), nextname())
    else:
        save_mask(m, nextname())

# montage for review
cols, cell = 5, 190
rows = (len(cuts) + cols - 1) // cols
mont = Image.new('RGB', (cols * cell, rows * cell), (244, 242, 238))
d = ImageDraw.Draw(mont)
for idx, (k, w, h, p) in enumerate(cuts):
    c = Image.open(p).convert('RGBA'); c.thumbnail((cell - 30, cell - 50))
    cx, cy = (idx % cols) * cell, (idx // cols) * cell
    mont.paste(c, (cx + (cell - c.width) // 2, cy + 12), c)
    d.text((cx + 8, cy + cell - 18), str(k), fill=(70, 70, 70))
mont.save(os.path.join(OUT, '_montage.png'))
print('saved', len(cuts), 'cutouts + _montage.png')
