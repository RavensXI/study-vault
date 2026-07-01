"""Extract a poster frame (~1.2s in) from each banked short video.
Posters mirror the R2 key under design-lab/_posters/ so the feed can derive
the path deterministically:  .../shorts/<key>.mp4  ->  _posters/shorts/<key>.jpg
Downloads with a browser UA (r2.dev 403s bot UAs) then runs ffmpeg locally.
"""
import json, os, subprocess, tempfile, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "scripts", "_shorts_manifest.json")
OUT = os.path.join(ROOT, "design-lab", "_posters")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def poster_rel(url):
    # everything from 'shorts/' onward, .mp4 -> .jpg
    key = url.split(".r2.dev/", 1)[1]
    return os.path.splitext(key)[0] + ".jpg"

def one(e):
    url = e["url"]
    rel = poster_rel(url)
    dst = os.path.join(OUT, rel.replace("/", os.sep))
    if os.path.exists(dst) and os.path.getsize(dst) > 2000:
        return f"skip {rel}"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=60).read()
    except Exception as ex:
        return f"DL FAIL {rel}: {ex}"
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tf:
        tf.write(data); tmp = tf.name
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-ss", "1.2", "-i", tmp, "-frames:v", "1",
             "-vf", "scale=540:-2", "-q:v", "4", dst],
            capture_output=True, text=True)
        ok = os.path.exists(dst) and os.path.getsize(dst) > 2000
        return (f"ok   {rel} ({os.path.getsize(dst)//1024}KB)" if ok
                else f"FF FAIL {rel}: {r.stderr.strip()[-160:]}")
    finally:
        os.unlink(tmp)

def main():
    man = json.load(open(MAN, encoding="utf-8"))
    man = [e for e in man if e.get("url")]
    print(f"{len(man)} videos -> posters")
    with ThreadPoolExecutor(max_workers=4) as ex:
        for line in ex.map(one, man):
            print(" ", line)

if __name__ == "__main__":
    main()
