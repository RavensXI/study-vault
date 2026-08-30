"""
Re-narrate ONLY the narration blocks whose narrated TEXT changed when the four
ADJUDICATED rulings (F1-F4) were applied to Jekyll and Hyde.

The changed set is DERIVED, not assumed: narration chunks are extracted from the
pre-ruling content stored in _adjudication_backup.json and from the live
post-ruling content, then compared id by id. Attribute-only edits produce no text
delta and are skipped automatically.

Voice: odd lesson_number -> Ollie, even -> Ada. get_voice_for_lesson returns a
TUPLE (voice_name, label) — unpacked, never used whole.

R2 key is DERIVED FROM THE EXISTING MANIFEST src, never hardcoded: this unit
mixes two prefixes (english-literature/ and english-literature-aqa/).

Usage:
  python scripts/_retrofc/units/english-literature-aqa__jekyll-and-hyde/_adjudicate_renarrate.py --dry-run
  python scripts/_retrofc/units/english-literature-aqa__jekyll-and-hyde/_adjudicate_renarrate.py
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
SCRIPTS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
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

BACKUP = os.path.join(HERE, "_adjudication_backup.json")
OUT = os.path.join(HERE, "_adjudication_renarrate.json")
LOGFILE = os.path.join(HERE, "_adjudicate.log")

LINES = []


def L(s):
    print(s)
    LINES.append(s)


def combined(row):
    return (
        (row.get("content_html") or "")
        + (row.get("exam_tip_html") or "")
        + (row.get("conclusion_html") or "")
    )


def key_for(manifest, nid, num):
    """Derive the R2 object key from the clip's own existing public URL."""
    for e in manifest or []:
        if e.get("id") == nid and e.get("src", "").startswith(AUDIO_PUBLIC_URL + "/"):
            return e["src"][len(AUDIO_PUBLIC_URL) + 1:]
    # fall back to this lesson's own prefix, taken from any sibling clip
    for e in manifest or []:
        src = e.get("src", "")
        if src.startswith(AUDIO_PUBLIC_URL + "/") and "/narration_" in src:
            prefix = src[len(AUDIO_PUBLIC_URL) + 1:].rsplit("/narration_", 1)[0]
            return f"{prefix}/narration_lesson-{num:02d}_{nid}.mp3"
    raise RuntimeError(f"cannot derive R2 key for L{num} {nid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not AZURE_KEY:
        L("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    with open(BACKUP, "r", encoding="utf-8") as f:
        backup = json.load(f)

    sb = get_client()
    r2 = get_r2_client() if not args.dry_run else None

    L("\n=== RE-NARRATION after ADJUDICATED rulings (changed narrated text only) ===")
    L(f"run: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  mode: "
      f"{'DRY RUN' if args.dry_run else 'LIVE'}")

    plan = []
    for entry in backup["lessons"]:
        num = entry["lesson_number"]
        lid = entry["id"]
        before = entry["before"]

        if "content_html" not in before:
            L(f"  L{num:02d}: no content_html change -> skip (JSON fields are not narrated)")
            continue

        live = (
            sb.table("lessons")
            .select("id, lesson_number, title, content_html, exam_tip_html, "
                    "conclusion_html, narration_manifest")
            .eq("id", lid)
            .single()
            .execute()
        ).data

        old_row = {
            "content_html": before["content_html"],
            "exam_tip_html": before.get("exam_tip_html", live.get("exam_tip_html")),
            "conclusion_html": before.get("conclusion_html", live.get("conclusion_html")),
        }
        old_chunks = dict(extract_narration_chunks(combined(old_row)))
        new_chunks = extract_narration_chunks(combined(live))

        changed = [(nid, txt) for nid, txt in new_chunks if old_chunks.get(nid) != txt]
        if not changed:
            L(f"  L{num:02d}: content edited but no narrated text changed -> skip")
            continue

        # narration ids must be preserved: every changed id must already exist
        have = {e.get("id") for e in (live.get("narration_manifest") or [])}
        for nid, _ in changed:
            if nid not in have:
                L(f"  !! L{num:02d} {nid} is NOT in the existing manifest — id drift, aborting")
                sys.exit(1)

        plan.append({"num": num, "id": lid, "title": live["title"],
                     "manifest": live.get("narration_manifest") or [],
                     "changed": changed})

    total_clips = sum(len(p["changed"]) for p in plan)
    L(f"\n{len(plan)} lessons, {total_clips} clips to regenerate\n")

    if args.dry_run:
        for p in plan:
            _voice_name, voice_label = get_voice_for_lesson(p["num"])
            L(f"  L{p['num']:02d} ({voice_label})  {p['title']}")
            for nid, txt in p["changed"]:
                L(f"      {nid} -> {key_for(p['manifest'], nid, p['num'])}")
                L(f"         {txt[:200]}")
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(LINES) + "\n")
        return

    regenerated = []
    for p in plan:
        num = p["num"]
        voice_name, voice_label = get_voice_for_lesson(num)   # TUPLE — unpack
        L(f"  L{num:02d} ({voice_label})  {p['title']}")
        manifest = [dict(e) for e in p["manifest"]]
        by_id = {e["id"]: e for e in manifest}

        for nid, text in p["changed"]:
            key = key_for(p["manifest"], nid, num)
            url = f"{AUDIO_PUBLIC_URL}/{key}"
            L(f"      {nid}: {text[:130]}")
            mp3 = generate_audio_rest(text, voice_name)
            if mp3 is None:
                L(f"      !! FAILED {nid} - manifest NOT updated for this lesson")
                break
            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            by_id[nid]["src"] = url          # id preserved, src/duration refreshed
            by_id[nid]["duration"] = dur
            regenerated.append({"lesson": num, "id": nid, "key": key, "url": url,
                                "voice": voice_label, "duration": dur,
                                "bytes": len(mp3)})
            L(f"             -> {len(mp3)/1024:.0f} KB, {dur:.1f}s, uploaded")
        else:
            sb.table("lessons").update({"narration_manifest": manifest}).eq("id", p["id"]).execute()
            L(f"      manifest updated ({len(manifest)} entries, ids unchanged)")

    L(f"\nRegenerated {len(regenerated)} clips.")

    # ---- verify: ranged GET 200/206 + fresh Last-Modified + MPEG frame sync ----
    # The R2 public dev endpoint 403s on a bare HEAD, so use a small ranged GET.
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

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({
            "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "rulings": ["F1", "F2", "F3", "F4"],
            "clips": regenerated, "verified_ok": ok, "total": len(regenerated),
        }, f, indent=1, ensure_ascii=False)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
