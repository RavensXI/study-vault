"""Re-narrate ONLY the narration blocks whose text changed in the four
EngLit surgical fixes.

Old text comes from _final_fixes_backup.json, new text from the live row.
R2 keys are taken from each lesson's EXISTING manifest src, so clips are
overwritten in place. Voice follows the Ollie(odd)/Ada(even) rule.

    python scripts/_content_englit-misc/_renarrate_fixes.py --dry-run
    python scripts/_content_englit-misc/_renarrate_fixes.py
"""
import json, os, sys, time
from datetime import datetime, timezone
from urllib.parse import urlparse

os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
import requests  # noqa: E402
from lib.supabase_client import get_client  # noqa: E402
from lib.narration import (extract_narration_chunks, generate_audio_rest,  # noqa: E402
                           get_mp3_duration, get_voice_for_lesson)
from lib.r2 import (get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET,  # noqa: E402
                    AUDIO_PUBLIC_URL)

OUT = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(OUT, "_final_fixes_backup.json")
LOG = os.path.join(OUT, "_renarrate_fixes.log")

DRY = "--dry-run" in sys.argv
PARTS = ("content_html", "exam_tip_html", "conclusion_html")

logf = open(LOG, "a", encoding="utf-8")


def log(msg):
    print(msg)
    logf.write(msg + "\n")
    logf.flush()


def chunks_of(row):
    out = []
    for f in PARTS:
        out += extract_narration_chunks(row.get(f) or "")
    return out


def key_from_src(src):
    """R2 object key from a manifest src URL — overwrite in place."""
    return urlparse(src).path.lstrip("/")


def main():
    sb = get_client()
    backup = json.load(open(BACKUP, encoding="utf-8"))
    r2 = None if DRY else get_r2_client()

    log("=" * 78)
    log(f"EngLit fix re-narration {datetime.now(timezone.utc).isoformat()}  dry_run={DRY}")

    grand_chars = grand_clips = 0
    summary = []

    for lid, meta in backup.items():
        row = sb.table("lessons").select(
            "id,lesson_number,title,content_html,exam_tip_html,"
            "conclusion_html,narration_manifest").eq("id", lid).single().execute().data
        num = row["lesson_number"]
        voice, vlabel = get_voice_for_lesson(num)

        old_row = {f: meta["fields"].get(f) for f in PARTS}
        old_chunks = chunks_of(old_row)
        new_chunks = chunks_of(row)
        manifest = [dict(e) for e in (row["narration_manifest"] or [])]

        assert len(old_chunks) == len(new_chunks) == len(manifest), (
            f"{meta['label']}: chunk/manifest length mismatch "
            f"{len(old_chunks)}/{len(new_chunks)}/{len(manifest)}")

        by_id = {e["id"]: i for i, e in enumerate(manifest)}
        todo = []
        for (oid, otext), (nid, ntext) in zip(old_chunks, new_chunks):
            assert oid == nid, f"{meta['label']}: narration id moved {oid} -> {nid}"
            if otext != ntext:
                todo.append((nid, ntext))

        log("")
        log(f"── {meta['label']}  L{num}  voice={vlabel}  "
            f"{len(todo)}/{len(new_chunks)} clips changed")
        if not todo:
            log("    (no narrated text changed — nothing to do)")
            summary.append((meta["label"], 0, 0))
            continue

        chars = sum(len(t) for _, t in todo)
        grand_chars += chars
        grand_clips += len(todo)
        for nid, ntext in todo:
            log(f"    {nid:>5}  {len(ntext):>4} chars  {ntext[:88]!r}")

        if DRY:
            summary.append((meta["label"], len(todo), 0))
            continue

        results = {}
        for nid, ntext in todo:
            idx = by_id[nid]
            key = key_from_src(manifest[idx]["src"])
            try:
                h = r2.head_object(Bucket=AUDIO_BUCKET, Key=key)
                before = (h["ContentLength"], h["LastModified"])
            except Exception:
                before = (None, None)

            mp3 = None
            for _ in range(3):
                mp3 = generate_audio_rest(ntext, voice)
                if mp3:
                    break
                time.sleep(3)
            if not mp3:
                log(f"    !! FAILED to generate {nid} ({key})")
                continue

            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            h2 = r2.head_object(Bucket=AUDIO_BUCKET, Key=key)
            after = (h2["ContentLength"], h2["LastModified"])
            manifest[idx]["duration"] = dur
            results[nid] = (before, after, key)
            log(f"    {nid:>5} uploaded {(before[0] or 0)//1024}KB -> "
                f"{after[0]//1024}KB  {dur:.1f}s  {key}")

        sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lid).execute()
        log(f"    manifest updated: {len(manifest)} entries")

        ok = bad = 0
        for nid, (before, after, key) in results.items():
            url = f"{AUDIO_PUBLIC_URL}/{key}"
            try:
                resp = requests.get(url, headers={"Cache-Control": "no-cache"}, timeout=30)
                code, live = resp.status_code, len(resp.content)
            except Exception as e:
                log(f"    !! HTTP error {nid}: {e}")
                bad += 1
                continue
            fresher = (before[1] is None) or (after[1] > before[1])
            if code == 200 and fresher:
                ok += 1
            else:
                bad += 1
            log(f"    verify {nid:>5} HTTP {code}  r2={after[0]}B live={live}B  "
                f"mtime {before[1]} -> {after[1]}  "
                f"{'FRESH' if fresher else 'STALE-TIMESTAMP'}")
        summary.append((meta["label"], len(todo), ok))
        if bad:
            log(f"    !! {bad} verification failures")

    log("")
    log(f"TOTAL: {grand_clips} clips, {grand_chars} chars, "
        f"est ${grand_chars * 16 / 1_000_000:.3f}")
    for label, n, ok in summary:
        log(f"  {label}: {n} re-narrated, {ok} verified HTTP 200 + fresh timestamp")
    if DRY:
        log("[DRY RUN] no audio generated, no writes.")


if __name__ == "__main__":
    main()
