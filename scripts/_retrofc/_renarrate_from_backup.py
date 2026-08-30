"""
Re-narrate ONLY the narration blocks whose narrated TEXT changed, for any
retro fact-check backup file.

Generalises scripts/_retrofc/units/english-literature-aqa__blood-brothers/
_renarrate.py: it takes the backup path, and it diffs content_html,
exam_tip_html AND conclusion_html (the Blood Brothers original only looked at
lessons whose content_html changed, which would have missed the DNA and Pigeon
English conclusion-only edits).

The changed set is DERIVED, not assumed: for every lesson the backup touched,
narration chunks are extracted from the pre-fix fields in the backup and from
the live post-fix row, then compared id by id. Attribute-only edits (data-def,
data-revision-tip) and tag-only edits (unwrapping a <dfn>) produce no text
delta and are skipped automatically.

Voice: odd lesson_number -> Ollie, even -> Ada (CLAUDE.md convention).
R2 key is DERIVED FROM THE EXISTING MANIFEST src, never hardcoded, because
units in this subject mix key prefixes.

Usage:
  python scripts/_retrofc/_renarrate_from_backup.py --backup <path> --dry-run
  python scripts/_retrofc/_renarrate_from_backup.py --backup <path>
"""
import argparse
import json
import os
import sys
import time
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import (
    extract_narration_chunks,
    generate_audio_rest,
    get_mp3_duration,
    get_voice_for_lesson,
    AZURE_KEY,
)

NARRATED_FIELDS = ("content_html", "exam_tip_html", "conclusion_html")

LINES = []


def L(s):
    print(s)
    LINES.append(s)


def combined(row):
    return "".join((row.get(f) or "") for f in NARRATED_FIELDS)


def key_for(manifest, nid, num):
    """Derive the R2 object key from the clip's existing public URL."""
    for e in manifest or []:
        if e.get("id") == nid and e.get("src", "").startswith(AUDIO_PUBLIC_URL + "/"):
            return e["src"][len(AUDIO_PUBLIC_URL) + 1:]
    # fall back to the unit's dominant prefix, taken from any sibling clip
    for e in manifest or []:
        src = e.get("src", "")
        if src.startswith(AUDIO_PUBLIC_URL + "/") and "/narration_" in src:
            prefix = src[len(AUDIO_PUBLIC_URL) + 1:].rsplit("/narration_", 1)[0]
            return f"{prefix}/narration_lesson-{num:02d}_{nid}.mp3"
    raise RuntimeError(f"cannot derive R2 key for L{num} {nid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backup", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    backup_path = os.path.abspath(args.backup)
    base = os.path.basename(backup_path)
    if not base.endswith("_backup.json"):
        L(f"ERROR: expected a *_backup.json path, got {base}")
        sys.exit(1)
    stem = base[: -len("_backup.json")]
    d = os.path.dirname(backup_path)
    report_path = os.path.join(d, f"{stem}_report.json")
    log_path = os.path.join(d, f"{stem}_renarrate.log")

    if not AZURE_KEY:
        L("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    with open(backup_path, "r", encoding="utf-8") as f:
        backup = json.load(f)

    sb = get_client()
    r2 = get_r2_client() if not args.dry_run else None

    L("\n=== RE-NARRATION (changed narrated text only) ===")
    L(f"backup: {backup_path}")
    L(f"unit:   {backup.get('subject')} / {backup.get('unit')}")
    L(f"run: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  mode: "
      f"{'DRY RUN' if args.dry_run else 'LIVE'}")

    plan = []
    for entry in backup["lessons"]:
        num = entry["lesson_number"]
        lid = entry["id"]
        before = entry["before"]

        if not any(f in before for f in NARRATED_FIELDS):
            L(f"  L{num:02d}: no narrated field changed -> skip")
            continue

        live = (
            sb.table("lessons")
            .select("id, lesson_number, title, content_html, exam_tip_html, "
                    "conclusion_html, narration_manifest")
            .eq("id", lid)
            .single()
            .execute()
        ).data

        old_row = {f: before.get(f, live.get(f)) for f in NARRATED_FIELDS}
        old_chunks = dict(extract_narration_chunks(combined(old_row)))
        new_chunks = extract_narration_chunks(combined(live))

        changed = [(nid, txt) for nid, txt in new_chunks if old_chunks.get(nid) != txt]
        if not changed:
            L(f"  L{num:02d}: fields edited but no narrated text changed -> skip")
            continue

        plan.append({"num": num, "id": lid, "title": live["title"],
                     "manifest": live.get("narration_manifest") or [],
                     "changed": changed})

    total_clips = sum(len(p["changed"]) for p in plan)
    L(f"\n{len(plan)} lessons, {total_clips} clips to regenerate\n")

    if args.dry_run:
        for p in plan:
            _, voice_label = get_voice_for_lesson(p["num"])
            L(f"  L{p['num']:02d} ({voice_label})  {p['title']}")
            for nid, txt in p["changed"]:
                L(f"      {nid} -> {key_for(p['manifest'], nid, p['num'])}")
                L(f"         {txt[:160]}")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n".join(LINES) + "\n")
        return

    regenerated = []
    for p in plan:
        num = p["num"]
        voice_name, voice_label = get_voice_for_lesson(num)
        L(f"  L{num:02d} ({voice_label})  {p['title']}")
        manifest = [dict(e) for e in p["manifest"]]
        by_id = {e["id"]: e for e in manifest}

        for nid, text in p["changed"]:
            key = key_for(p["manifest"], nid, num)
            url = f"{AUDIO_PUBLIC_URL}/{key}"
            L(f"      {nid}: {text[:110]}")
            mp3 = generate_audio_rest(text, voice_name)
            if mp3 is None:
                L(f"      !! FAILED {nid} - manifest NOT updated for this lesson")
                break
            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            if nid in by_id:
                by_id[nid]["src"] = url
                by_id[nid]["duration"] = dur
            else:
                manifest.append({"id": nid, "src": url, "duration": dur})
            regenerated.append({"lesson": num, "id": nid, "key": key, "url": url,
                                "voice": voice_label, "duration": dur,
                                "bytes": len(mp3)})
            L(f"             -> {len(mp3)/1024:.0f} KB, {dur:.1f}s, uploaded")
        else:
            sb.table("lessons").update({"narration_manifest": manifest}).eq("id", p["id"]).execute()
            L(f"      manifest updated ({len(manifest)} entries)")

    L(f"\nRegenerated {len(regenerated)} clips.")

    # ---- verify: HTTP 200/206 + fresh Last-Modified on every regenerated key ----
    # NOTE: the R2 public dev endpoint 403s on a bare HEAD. Use a small ranged GET;
    # it also confirms the MPEG frame sync bytes.
    L("\n=== VERIFY (ranged GET + freshness) ===")
    ok = 0
    for c in regenerated:
        req = urllib.request.Request(
            c["url"], headers={"User-Agent": "Mozilla/5.0", "Range": "bytes=0-3"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                magic = r.read(4)
                lm = r.headers.get("Last-Modified", "?")
                rng = r.headers.get("Content-Range", r.headers.get("Content-Length", "?"))
                sync = magic[:2] in (b"\xff\xf3", b"\xff\xfb", b"\xff\xf2")
                good = r.status in (200, 206) and sync
                c["verify_status"] = r.status
                c["last_modified"] = lm
                L(f"  {r.status}  L{c['lesson']:02d} {c['id']}  {rng}  "
                  f"Last-Modified: {lm}  mp3-sync={'OK' if sync else repr(magic[:3])}")
                if good:
                    ok += 1
        except Exception as e:
            c["verify_status"] = f"FAIL {e}"
            L(f"  FAIL L{c['lesson']:02d} {c['id']}: {e}")
    L(f"\n{ok}/{len(regenerated)} clips verified HTTP 200/206 with fresh audio.")

    # fold into the matching report
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception:
        report = {}
    report["renarration"] = {
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "clips": regenerated,
        "verified_ok": ok,
        "total": len(regenerated),
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
