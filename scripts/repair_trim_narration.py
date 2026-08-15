# -*- coding: utf-8 -*-
"""Repair the narration debt from the tip trims (16 Aug).

40 trimmed tips carried data-narration-id paragraphs. The trim rebuilt them
as clean <p>s, dropping the ids — but the player is MANIFEST-driven, so the
dropped paragraphs' clips would still play, reading text no longer on the
page.

Mechanical repair from the trim backup, no Azure calls:
- a paragraph whose FULL text survived: restored verbatim from the backup
  (original attributes incl. its narration id) → plays and highlights.
- a paragraph dropped or partially trimmed: its clip entry is REMOVED from
  lessons.narration_manifest (and the trimmed text keeps no id) → the clip
  never plays; the surviving text simply isn't read. Honest silence beats
  ghost audio.

Run: python scripts/repair_trim_narration.py [--apply]
Backup: scripts/_trim_narration_repair_backup.json
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_trim_narration_repair_backup.json")
TAGS = re.compile(r"<[^>]+>")


def norm(s):
    return re.sub(r"\s+", " ", TAGS.sub(" ", s or "")).strip()


def paras(html):
    return re.findall(r"<p[^>]*>.*?</p>", html or "", re.S)


def pid_of(p_html):
    m = re.search(r'data-narration-id="([^"]+)"', p_html)
    return m.group(1) if m else None


def main():
    sb = get_client()
    trims = json.load(io.open(os.path.join(HERE, "_tip_trim_backup.json"),
                              encoding="utf-8"))
    backup, writes = {}, []
    stats = {"restored": 0, "silenced": 0}
    for lid, original in trims.items():
        if "data-narration-id" not in (original or ""):
            continue
        row = sb.table("lessons").select("id,exam_tip_html,narration_manifest") \
            .eq("id", lid).execute().data[0]
        current_text = norm(row.get("exam_tip_html"))
        new_parts, drop_ids = [], []
        for p in paras(original):
            pid = pid_of(p)
            if norm(p) and norm(p) in current_text and \
               all(norm(s) in current_text for s in [p]):
                # full paragraph survived the trim → restore verbatim
                new_parts.append(p)
                if pid:
                    stats["restored"] += 1
            else:
                # dropped, or partially trimmed: find which sentences survive
                kept_bits = [s for s in re.split(r"(?<=[.!?])\s+", norm(p))
                             if s and s in current_text]
                if kept_bits:
                    new_parts.append("<p>" + " ".join(kept_bits) + "</p>")
                if pid:
                    drop_ids.append(pid)
                    stats["silenced"] += 1
        new_tip = "".join(new_parts) or None
        manifest = row.get("narration_manifest") or []
        new_manifest = [m for m in manifest if m.get("id") not in drop_ids]
        if new_tip == row.get("exam_tip_html") and len(new_manifest) == len(manifest):
            continue
        backup[lid] = {"exam_tip_html": row.get("exam_tip_html"),
                       "narration_manifest": manifest}
        writes.append((lid, new_tip, new_manifest))
        print("%s: %d para(s) restored w/ ids, %d clip(s) removed"
              % (lid[:8], sum(1 for p in new_parts if pid_of(p)), len(drop_ids)))

    print("\nlessons: %d | paragraphs restored: %d | clips silenced: %d"
          % (len(writes), stats["restored"], stats["silenced"]))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    prior = json.load(io.open(BACKUP, encoding="utf-8")) if os.path.exists(BACKUP) else {}
    prior.update({k: v for k, v in backup.items() if k not in prior})
    io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(prior))
    for lid, tip, manifest in writes:
        sb.table("lessons").update({"exam_tip_html": tip,
                                    "narration_manifest": manifest}).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
