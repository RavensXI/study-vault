# -*- coding: utf-8 -*-
"""Crop the two Yorkshire Dales sheets back to the ground that has contour data.

    python scratchpad/_geo_guided/_crop_dales.py            # measure + write locally
    python scratchpad/_geo_guided/_crop_dales.py --upload   # push to R2

Both sheets lose every contour east of easting 90 -- the same straight cut at two
different zoom levels, so it is a tile boundary in the OS Terrain 50 layer, not
terrain. Everything east of that line is drawn as if it were flat, which is what
made the sheets look broken and what four questions were mistakenly written
around.

The crop keeps the western side and stops on the grid line itself, so the sheet
still ends on a feature a student can name rather than in the middle of nowhere.

Attribution is checked, not assumed: the OS/OSM credit sits bottom-left and must
survive the crop, or we would be publishing OS data with the copyright line cut
off. The script refuses to write if the strip is not fully inside the box.

New keys rather than overwriting: the originals stay put as a rollback, and a new
name cannot be served stale from a CDN cache.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_mapcache")
OUT = os.path.join(HERE, "_cropped")

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from PIL import Image, ImageFilter

SHEETS = ["yorkshire-dales-z15-final.jpg", "yorkshire-dales-z16-final.jpg"]
SUFFIX = "-w90"          # west of easting 90


def thin_cols(im):
    """Per-column count of thin brown (contour) pixels."""
    w, h = im.size
    px = im.load()
    m = Image.new("L", (w, h), 0)
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 110 and r - b > 30 and 15 < r - g < 95 and g >= b and r < 240:
                mp[x, y] = 255
    ep = m.filter(ImageFilter.MinFilter(3)).load()
    cols = [0] * w
    for y in range(h):
        for x in range(w):
            if mp[x, y] and not ep[x, y]:
                cols[x] += 1
    return cols


def find_edge(im):
    """x (in im coords) where contour ink stops and does not resume."""
    cols = thin_cols(im)
    n, h = len(cols), im.size[1]
    lo, hi = int(n * 0.12), int(n * 0.95)
    best = None
    for i in range(lo, hi):
        left = sum(cols[:i]) / float(i * h)
        right = sum(cols[i:]) / float(max(1, n - i) * h)
        if left < 0.004:
            continue
        ratio = right / left
        if ratio > 0.08:
            continue
        score = left * (1 - ratio)
        if not best or score > best[1]:
            best = (i, score)
    return best[0] if best else None


def attribution_box(im):
    """Bounding x of the dark attribution text along the bottom strip."""
    w, h = im.size
    px = im.load()
    x_max = 0
    for y in range(int(h * 0.975), h):
        for x in range(w):
            r, g, b = px[x, y]
            if r < 120 and g < 120 and b < 120:
                if x > x_max:
                    x_max = x
    return x_max


def main(upload):
    os.makedirs(OUT, exist_ok=True)
    done = []
    for name in SHEETS:
        src = os.path.join(CACHE, name)
        if not os.path.exists(src):
            sys.exit("missing cached sheet: %s" % name)
        im0 = Image.open(src).convert("RGB")
        W, H = im0.size
        small = im0.resize((900, int(H * 900.0 / W)))
        body = small.crop((0, 0, 900, int(small.size[1] * 0.975)))
        e = find_edge(body)
        if e is None:
            print("%-34s no clean edge found - SKIPPED" % name)
            continue
        x = int(e * W / 900.0)

        attr_x = attribution_box(im0)
        if attr_x >= x:
            sys.exit("%s: crop at %d would cut the OS attribution (ends at %d)" % (name, x, attr_x))

        out = im0.crop((0, 0, x, H))
        dst_name = name.replace("-final.jpg", SUFFIX + "-final.jpg")
        dst = os.path.join(OUT, dst_name)
        out.save(dst, "JPEG", quality=88, optimize=True)
        kept = 100.0 * x / W
        print("%-34s cut at x=%-5d keeps %2d%%  attribution ends x=%-4d  -> %s (%dx%d)"
              % (name, x, round(kept), attr_x, dst_name, out.size[0], out.size[1]))
        done.append((dst_name, dst))

    if not upload:
        print("\nlocal only; review %s then rerun with --upload" % OUT)
        return

    import boto3
    s3 = boto3.client(
        "s3",
        endpoint_url="https://%s.r2.cloudflarestorage.com" % os.environ["R2_ACCOUNT_ID"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    for dst_name, path in done:
        key = "geography/os-maps/" + dst_name
        with io.open(path, "rb") as f:
            s3.put_object(Bucket="studyvault-images", Key=key, Body=f.read(),
                          ContentType="image/jpeg")
        print("uploaded", key)


if __name__ == "__main__":
    main("--upload" in sys.argv)
