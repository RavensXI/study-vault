"""Re-narrate ONLY the narration blocks whose text changed in the
Boys Don't Cry name-swap / Curious Incident AO / A Christmas Carol fixes.

R2 keys are derived from the existing manifest and overwritten in place.
Also generates the three new ids created when duplicate narration-id
collisions were cleared, and regenerates the content-side ids whose key had
been clobbered by those collisions.

    python scripts/_bdc_renarrate.py --dry-run
    python scripts/_bdc_renarrate.py
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import requests  # noqa: E402
from lib.supabase_client import get_client  # noqa: E402
from lib.narration import (extract_narration_chunks, generate_audio_rest,  # noqa: E402
                           get_mp3_duration, get_voice_for_lesson)
from lib.r2 import (get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET,  # noqa: E402
                    AUDIO_PUBLIC_URL)

OUT_DIR = os.path.join(SCRIPT_DIR, "_content_englit-edexcel")
BACKUP = os.path.join(OUT_DIR, "_bdc_nameswap_backup.json")
LOG = os.path.join(OUT_DIR, "_bdc_renarrate.log")

DRY = "--dry-run" in sys.argv
PARTS = ("content_html", "exam_tip_html", "conclusion_html")

# Ids whose TEXT is unchanged but whose R2 key held the wrong audio because a
# duplicate narration id elsewhere in the lesson overwrote it. lesson id -> ids
FORCE = {
    "c81cefe5-ecc1-4cc0-a8c6-1e30dbb7aee5": ["n28"],              # BDC L6 content
    "a99b8f7e-a44a-4a17-a6e2-b9da16bb5336": ["n33", "n34", "n35"],  # CI L8 content
}

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


def main():
    sb = get_client()
    backup = json.load(open(BACKUP, encoding="utf-8"))
    r2 = None if DRY else get_r2_client()

    log("=" * 78)
    log(f"Re-narration run {datetime.now(timezone.utc).isoformat()}  dry_run={DRY}")

    grand_chars = 0
    grand_clips = 0
    summary = []

    for lid, meta in backup.items():
        row = sb.table("lessons").select(
            "id,lesson_number,title,unit_id,content_html,exam_tip_html,"
            "conclusion_html,narration_manifest").eq("id", lid).single().execute().data
        unit = sb.table("units").select("slug,subject_id").eq("id", row["unit_id"]).single().execute().data
        subject = sb.table("subjects").select("slug").eq("id", unit["subject_id"]).single().execute().data
        subject_slug, unit_slug = subject["slug"], unit["slug"]
        num = row["lesson_number"]
        voice, vlabel = get_voice_for_lesson(num)

        # Old row = backed-up fields merged over the current row.
        old_row = dict(row)
        old_row.update({k: v for k, v in meta["fields"].items() if k in PARTS})
        old_chunks = chunks_of(old_row)
        new_chunks = chunks_of(row)
        old_manifest = meta["narration_manifest"] or []

        assert len(old_chunks) == len(new_chunks) == len(old_manifest), (
            f"{meta['label']}: chunk/manifest length mismatch "
            f"{len(old_chunks)}/{len(new_chunks)}/{len(old_manifest)}")

        forced = set(FORCE.get(lid, []))
        todo = []
        for i, ((oid, otext), (nid, ntext)) in enumerate(zip(old_chunks, new_chunks)):
            changed = (otext != ntext) or (oid != nid) or (nid in forced)
            if changed:
                reason = ("text" if otext != ntext else
                          "renumbered" if oid != nid else "collision-repair")
                todo.append((i, nid, ntext, reason))

        log("")
        log(f"── {meta['label']}  [{lid}]  L{num}  voice={vlabel}  "
            f"{len(todo)}/{len(new_chunks)} clips")
        chars = sum(len(t) for _, _, t, _ in todo)
        grand_chars += chars
        grand_clips += len(todo)
        for i, nid, ntext, reason in todo:
            log(f"    {nid:>5}  [{reason:<16}] {len(ntext):>4} chars  {ntext[:72]!r}")

        if DRY:
            summary.append((meta["label"], len(todo), 0))
            continue

        new_dur = {}
        sizes = {}
        for i, nid, ntext, reason in todo:
            key = f"{subject_slug}/{unit_slug}/narration_lesson-{num:02d}_{nid}.mp3"
            before = None
            try:
                before = r2.head_object(Bucket=AUDIO_BUCKET, Key=key)["ContentLength"]
            except Exception:
                before = None
            mp3 = None
            for attempt in range(3):
                mp3 = generate_audio_rest(ntext, voice)
                if mp3:
                    break
                time.sleep(3)
            if not mp3:
                log(f"    !! FAILED to generate {nid} ({key})")
                continue
            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            after = r2.head_object(Bucket=AUDIO_BUCKET, Key=key)["ContentLength"]
            new_dur[i] = dur
            sizes[nid] = (before, after, key)
            log(f"    {nid:>5}  uploaded  {(before or 0)//1024}KB -> {after//1024}KB  "
                f"{dur:.1f}s  {key}")

        # Rebuild the manifest: same order, ids from the new content.
        manifest = []
        for i, (nid, ntext) in enumerate(new_chunks):
            key = f"{subject_slug}/{unit_slug}/narration_lesson-{num:02d}_{nid}.mp3"
            entry = {"id": nid, "src": f"{AUDIO_PUBLIC_URL}/{key}",
                     "duration": new_dur.get(i, old_manifest[i].get("duration"))}
            if "tier" in old_manifest[i]:
                entry["tier"] = old_manifest[i]["tier"]
            manifest.append(entry)
        sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lid).execute()
        log(f"    manifest updated: {len(manifest)} entries")

        # HTTP verification on the overwritten keys.
        ok = bad = 0
        for nid, (before, after, key) in sizes.items():
            url = f"{AUDIO_PUBLIC_URL}/{key}"
            try:
                resp = requests.get(url, headers={"Cache-Control": "no-cache"}, timeout=30)
                code = resp.status_code
                live = len(resp.content)
            except Exception as e:
                log(f"    !! HTTP error {nid}: {e}")
                bad += 1
                continue
            same = (before is not None and before == after)
            flag = "OK" if code == 200 else "HTTP-FAIL"
            if code != 200:
                bad += 1
            else:
                ok += 1
            log(f"    verify {nid:>5} {flag} {code}  r2={after}B live={live}B  "
                f"{'size-unchanged' if same else 'size-changed'}")
        summary.append((meta["label"], len(todo), ok))
        if bad:
            log(f"    !! {bad} verification failures")

    log("")
    log(f"TOTAL: {grand_clips} clips, {grand_chars} chars, "
        f"est ${grand_chars * 16 / 1_000_000:.3f}")
    for label, n, ok in summary:
        log(f"  {label}: {n} clips re-narrated, {ok} verified HTTP 200")
    if DRY:
        log("[DRY RUN] no audio generated, no writes.")


if __name__ == "__main__":
    main()
