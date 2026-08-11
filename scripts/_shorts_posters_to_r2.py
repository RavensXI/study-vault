# -*- coding: utf-8 -*-
"""Move the shorts poster frames to R2 as WebP.

WHY: /desk and the shorts feed were the last two pages pulling from
design-lab/, which is now excluded from the deploy. The posters were the only
images on the whole site not already on R2 — heroes, audio and video all live
there — because they were generated in the workshop and never needed to leave.
97.5MB across 1,579 files, growing with every shorts batch.

FORMAT: WebP quality 72 at native 540x958, calibrated on a 30-file sample
before committing to the fleet:

    JPEG q72   7% smaller   (barely worth the re-encode)
    WebP q82  24% smaller
    WebP q72  45% smaller   <- chosen
    WebP q62  51% smaller   (6 more points for visible loss on photographic
                             frames; not worth it)

Dimensions are left alone. 540x958 is already right for a phone at 1x-1.5x,
and shrinking further would show if the feed ever goes full-screen on a large
handset.

NOT using upload_bytes_to_r2(): for IMAGES_BUCKET it re-encodes anything with
an image/* content type to JPEG q82 and then hardcodes content_type to
image/jpeg. With WebP input it would keep the WebP bytes (they are smaller, so
its "only if smaller" guard returns the original) while labelling them as
JPEG — the worst of both. put_object directly instead.

    python _shorts_posters_to_r2.py [--dry-run] [--limit N]
"""
import io, json, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
from lib.r2 import get_r2_client, IMAGES_BUCKET, IMAGES_PUBLIC_URL

SRC = os.path.join(HERE, "..", "design-lab", "_posters", "shorts")
PREFIX = "shorts/posters"
QUALITY = 72
DONE = os.path.join(HERE, "_shorts_posters_uploaded.json")


def key_for(path):
    rel = os.path.relpath(path, SRC).replace(os.sep, "/")
    return "%s/%s" % (PREFIX, rel.rsplit(".", 1)[0] + ".webp")


def main():
    dry = "--dry-run" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    files = []
    for root, _dirs, names in os.walk(SRC):
        for n in sorted(names):
            if n.lower().endswith(".jpg"):
                files.append(os.path.join(root, n))
    files.sort()
    if limit:
        files = files[:limit]

    done = set()
    if os.path.exists(DONE):
        done = set(json.load(open(DONE, encoding="utf-8")))
    todo = [f for f in files if key_for(f) not in done]
    print("posters: %d total, %d already uploaded, %d to do" % (len(files), len(files) - len(todo), len(todo)))

    r2 = None if dry else get_r2_client()
    src_bytes = out_bytes = 0
    uploaded = []

    def one(path):
        nonlocal src_bytes, out_bytes
        raw = os.path.getsize(path)
        im = Image.open(path).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=QUALITY, method=6)
        data = buf.getvalue()
        k = key_for(path)
        if not dry:
            r2.put_object(Bucket=IMAGES_BUCKET, Key=k, Body=data,
                          ContentType="image/webp",
                          CacheControl="public, max-age=31536000, immutable")
        src_bytes += raw
        out_bytes += len(data)
        return k

    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, k in enumerate(ex.map(one, todo), 1):
            uploaded.append(k)
            if i % 200 == 0 or i == len(todo):
                print("  %d/%d  (%.1f MB -> %.1f MB so far)" % (i, len(todo), src_bytes/1e6, out_bytes/1e6))

    if not dry and uploaded:
        json.dump(sorted(done | set(uploaded)), open(DONE, "w", encoding="utf-8"))

    if src_bytes:
        print("\n%.1f MB -> %.1f MB  (%.0f%% smaller)"
              % (src_bytes/1e6, out_bytes/1e6, 100 * (1 - out_bytes/src_bytes)))
    if uploaded:
        print("example: %s/%s" % (IMAGES_PUBLIC_URL, uploaded[0]))
    print(("DRY RUN — " if dry else "") + "done")


if __name__ == "__main__":
    main()
