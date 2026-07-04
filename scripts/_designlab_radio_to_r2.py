"""Publish the desk radio's ambient stations (our own generated tracks,
TPE1=StudyVault) to R2 so the deployed demo has music, and write
design-lab/assets/radio/_stations.json for the radio to read directly —
Vercel serves no directory listings, so the scrape only works in dev.
Keys: demo/radio/{station}/[{season}/]{track}.mp3 on studyvault-audio.
Re-runnable: skips objects that already exist.
"""
import glob, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from lib.r2 import get_r2_client, AUDIO_BUCKET, AUDIO_PUBLIC_URL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RADIO = os.path.join(ROOT, "design-lab", "assets", "radio")
c = get_r2_client()

manifest = {}
files = sorted(glob.glob(os.path.join(RADIO, "**", "*.mp3"), recursive=True))
for i, f in enumerate(files):
    rel = os.path.relpath(f, RADIO).replace("\\", "/")   # e.g. season/winter/x.mp3
    key = "demo/radio/" + rel
    try:
        c.head_object(Bucket=AUDIO_BUCKET, Key=key)
        status = "have"
    except Exception:
        c.upload_file(f, AUDIO_BUCKET, key, ExtraArgs={"ContentType": "audio/mpeg"})
        status = "up  "
    url = AUDIO_PUBLIC_URL + "/" + key
    parts = rel.split("/")
    if parts[0] == "season":
        manifest.setdefault("season", {}).setdefault(parts[1], []).append(url)
    else:
        manifest.setdefault(parts[0], []).append(url)
    print(f"[{i+1}/{len(files)}] {status} {rel}", flush=True)

out = os.path.join(RADIO, "_stations.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(len(v) if isinstance(v, list) else sum(len(x) for x in v.values()) for v in manifest.values())
print(f"\n_stations.json: {len(manifest)} stations, {n} tracks")
