"""One-off back-catalogue pass: chop the NotebookLM endcard off every banked
short on R2. Detection + trimming live in lib/trim_endcard.py (shared with
the nightly batch, which trims future shorts before upload).

Safety:
- every ORIGINAL is kept locally under scripts/_shorts_originals/<r2 key>
  until Tom deletes the folder;
- a video is only re-uploaded when trim+verify BOTH pass; failures are
  logged and the R2 object is left untouched;
- resumable: state in scripts/_shorts_trim_state.json.

Usage:
  python scripts/_shorts_trim_endcards.py --sample 30     # dry run, no upload
  python scripts/_shorts_trim_endcards.py --all           # the real pass
  python scripts/_shorts_trim_endcards.py --all --limit 50
"""
import argparse
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.trim_endcard import trim, detect_cut, duration  # noqa: E402

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "scripts", "_shorts_manifest.json")
ORIGINALS = os.path.join(ROOT, "scripts", "_shorts_originals")
STATE = os.path.join(ROOT, "scripts", "_shorts_trim_state.json")
WORK = os.path.join(ROOT, "scripts", "_shorts_trim_work")


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError):
        return {"done": {}, "failed": {}}


def save_state(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1)


def r2_key(url):
    return url.split(".r2.dev/")[1]


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "studyvault-trim/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def process(entry, st, upload, r2=None, bucket=None):
    url = entry["url"]
    key = r2_key(url)
    if key in st["done"]:
        return "skip"
    src = os.path.join(WORK, "src.mp4")
    out = os.path.join(WORK, "out.mp4")
    try:
        fetch(url, src)
    except Exception as e:  # noqa: BLE001
        st["failed"][key] = f"download: {e}"
        return "fail"
    rep = trim(src, out)
    if not rep["ok"]:
        st["failed"][key] = rep["why"]
        print(f"FAIL  {key}  {rep['why']}", flush=True)
        return "fail"
    if upload:
        keep = os.path.join(ORIGINALS, key.replace("/", os.sep))
        os.makedirs(os.path.dirname(keep), exist_ok=True)
        os.replace(src, keep)
        with open(out, "rb") as f:
            r2.put_object(Bucket=bucket, Key=key, Body=f.read(),
                          ContentType="video/mp4")
    st["done"][key] = {"endcard": rep["endcard"], "method": rep["method"]}
    st["failed"].pop(key, None)
    print(f"ok    {key}  -{rep['endcard']}s  ({rep['method']})", flush=True)
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="dry-run N spread across the bank, no upload")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    os.makedirs(WORK, exist_ok=True)
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    st = load_state()

    if args.sample:
        step = max(1, len(manifest) // args.sample)
        picks = manifest[::step][:args.sample]
        stats, fails = [], 0
        os.makedirs(os.path.join(WORK, "samples"), exist_ok=True)
        for i, e in enumerate(picks):
            src = os.path.join(WORK, "src.mp4")
            out = os.path.join(WORK, "samples", f"s{i:02d}.mp4")
            try:
                fetch(e["url"], src)
                rep = trim(src, out)
            except Exception as ex:  # noqa: BLE001
                rep = {"ok": False, "why": str(ex), "endcard": None, "method": None}
            tag = "ok  " if rep["ok"] else "FAIL"
            print(f"{tag}  {r2_key(e['url'])}  endcard={rep['endcard']}  {rep['method'] or rep['why']}", flush=True)
            if rep["ok"]:
                stats.append((rep["endcard"], rep["method"]))
            else:
                fails += 1
        lens = sorted(s[0] for s in stats)
        copies = sum(1 for s in stats if s[1] == "copy")
        print(f"\n{len(stats)} trimmed, {fails} failed/left alone")
        if lens:
            print(f"endcard length min {lens[0]} median {lens[len(lens)//2]} max {lens[-1]}")
            print(f"methods: {copies} stream-copy, {len(stats)-copies} re-encode")
        return

    if not args.all:
        ap.print_help()
        return

    from lib.r2 import get_r2_client, VIDEO_BUCKET  # noqa: E402  (creds needed only here)
    r2 = get_r2_client()
    todo = [e for e in manifest if r2_key(e["url"]) not in st["done"]]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(todo)} shorts to trim ({len(st['done'])} already done)", flush=True)
    t0 = time.time()
    counts = {"ok": 0, "fail": 0, "skip": 0}
    for i, e in enumerate(todo):
        counts[process(e, st, upload=True, r2=r2, bucket=VIDEO_BUCKET)] += 1
        if i % 20 == 0:
            save_state(st)
        if i % 100 == 0 and i:
            rate = (time.time() - t0) / i
            print(f"--- {i}/{len(todo)}  ({rate:.1f}s/video, ~{(len(todo)-i)*rate/3600:.1f}h left)", flush=True)
    save_state(st)
    print(f"done: {counts['ok']} trimmed, {counts['fail']} failed (logged, R2 untouched)")


if __name__ == "__main__":
    main()
