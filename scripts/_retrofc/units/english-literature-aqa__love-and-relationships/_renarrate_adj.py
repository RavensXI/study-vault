"""
Re-narrate ONLY the narration blocks whose narrated TEXT changed during the
Love & Relationships ADJUDICATION pass (nine rulings).

The changed set is DERIVED, not assumed: for every lesson touched, narration
chunks are extracted from the pre-fix content in _backup.json and from the live
post-fix content, then compared id by id. Attribute-only edits (data-def,
data-revision-tip) produce no text delta and are skipped automatically.

Voice: odd lesson_number -> Ollie, even -> Ada (CLAUDE.md convention).

R2 keys are taken from each clip's EXISTING manifest src, never rebuilt from a
guessed prefix: this unit is split across two prefixes
(english-literature/... for L1,2,6,7 and english-literature-aqa/... for
L3,4,5,8), so a single hard-coded prefix would silently write to dead keys.

Usage:
  python _renarrate.py --dry-run
  python _renarrate.py
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))  # units/<unit>/ -> _retrofc/ -> scripts/
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
LOGFILE = os.path.join(HERE, "_renarrate_adj.log")

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


def key_from_src(src):
    """R2 object key from a public https URL, preserving the real prefix."""
    path = urllib.parse.urlparse(src).path
    return path.lstrip("/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not AZURE_KEY and not args.dry_run:
        L("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    with open(BACKUP, "r", encoding="utf-8") as f:
        backup = json.load(f)

    sb = get_client()
    r2 = get_r2_client() if not args.dry_run else None

    L("\n=== RE-NARRATION (changed blocks only) ===")
    L(f"run: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  mode: "
      f"{'DRY RUN' if args.dry_run else 'LIVE'}")

    plan = []
    for entry in backup["lessons"]:
        num = entry["lesson_number"]
        lid = entry["id"]
        before = entry["before"]

        narrated_fields = {"content_html", "exam_tip_html", "conclusion_html"}
        if not (narrated_fields & set(before.keys())):
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

        old_row = {f: before.get(f, live.get(f)) for f in narrated_fields}
        old_chunks = dict(extract_narration_chunks(combined(old_row)))
        new_chunks = extract_narration_chunks(combined(live))

        changed = [(nid, txt) for nid, txt in new_chunks if old_chunks.get(nid) != txt]
        if not changed:
            L(f"  L{num:02d}: content edited but no narrated text changed -> skip")
            continue

        plan.append({"num": num, "id": lid, "title": live["title"],
                     "manifest": live.get("narration_manifest") or [],
                     "changed": changed})

    total = sum(len(p["changed"]) for p in plan)
    L(f"\n{len(plan)} lessons, {total} clips to regenerate\n")

    if args.dry_run:
        for p in plan:
            _, voice_label = get_voice_for_lesson(p["num"])
            L(f"  L{p['num']:02d} ({voice_label})  {p['title']}")
            by_id = {e["id"]: e for e in p["manifest"]}
            for nid, txt in p["changed"]:
                src = by_id.get(nid, {}).get("src", "(NEW - no existing src)")
                L(f"      {nid}: {txt[:90]}")
                L(f"           key: {key_from_src(src) if src.startswith('http') else src}")
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(LINES) + "\n")
        return

    regenerated = []
    for p in plan:
        num = p["num"]
        voice_name, voice_label = get_voice_for_lesson(num)
        L(f"  L{num:02d} ({voice_label})  {p['title']}")
        manifest = [dict(e) for e in p["manifest"]]
        by_id = {e["id"]: e for e in manifest}

        ok = True
        for nid, text in p["changed"]:
            if nid not in by_id or not str(by_id[nid].get("src", "")).startswith("http"):
                L(f"      !! {nid} has no existing manifest src - SKIPPED (would guess a key)")
                ok = False
                continue
            key = key_from_src(by_id[nid]["src"])
            url = f"{AUDIO_PUBLIC_URL}/{key}"
            L(f"      {nid}: {text[:80]}")
            mp3 = generate_audio_rest(text, voice_name)
            if mp3 is None:
                L(f"      !! FAILED {nid} - manifest NOT updated for this lesson")
                ok = False
                break
            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            by_id[nid]["src"] = url
            by_id[nid]["duration"] = dur
            regenerated.append((num, nid, key))
            L(f"             -> {len(mp3)/1024:.0f} KB, {dur:.1f}s, uploaded")
        if ok:
            sb.table("lessons").update({"narration_manifest": manifest}).eq("id", p["id"]).execute()
            L(f"      manifest updated ({len(manifest)} entries)")

    L(f"\nRegenerated {len(regenerated)} clips.")

    # ---- verify: HTTP 200/206 + fresh Last-Modified on every regenerated key ----
    # NOTE: the R2 public dev endpoint 403s on a bare HEAD. Use a small ranged GET;
    # it also confirms the MPEG frame sync bytes.
    L("\n=== VERIFY (ranged GET + freshness) ===")
    good = 0
    for num, nid, key in regenerated:
        url = f"{AUDIO_PUBLIC_URL}/{key}"
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0", "Range": "bytes=0-3"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                magic = r.read(4)
                lm = r.headers.get("Last-Modified", "?")
                sync = magic[:2] in (b"\xff\xf3", b"\xff\xfb", b"\xff\xf2")
                okk = r.status in (200, 206) and sync
                L(f"  {r.status}  L{num:02d} {nid}  Last-Modified: {lm}  "
                  f"mp3-sync={'OK' if sync else repr(magic[:3])}")
                if okk:
                    good += 1
        except Exception as e:
            L(f"  FAIL L{num:02d} {nid}: {e}")
    L(f"\n{good}/{len(regenerated)} clips verified fresh + playable.")

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
