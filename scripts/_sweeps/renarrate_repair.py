"""Repair pass for the label sweep's re-narration.

scripts/_retrofc/_renarrate_from_backup.py aborts a whole subject when one
lesson in the batch has an EMPTY narration_manifest (it cannot derive an R2
key). Those lessons carry no audio at all, so nothing needs regenerating - but
their narrated siblings in the same batch were skipped with them.

This pass re-reads every <subject>_backup.json the sweep wrote, keeps only the
lessons that really do carry audio, and re-runs the re-narrator on them.

    python scripts/_sweeps/renarrate_repair.py [--dry-run]
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
OUT = os.path.join(HERE, "labels")
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": K, "Authorization": "Bearer " + K}


def get(path):
    req = urllib.request.Request(f"{U}/rest/v1/{path}", headers=HDR)
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    summary = json.load(open(os.path.join(OUT, "_summary.json"), encoding="utf-8"))
    failed = {t["subject"]: t for t in summary["per_subject"]
              if isinstance(t.get("renarrated_clips"), str)}
    print(f"{len(failed)} subject(s) whose re-narration failed: {sorted(failed)}")

    report = {}
    for slug in sorted(failed):
        src = os.path.join(OUT, f"{slug}_backup.json")
        if not os.path.exists(src):
            print(f"-- {slug}: no re-narration backup, nothing to repair")
            continue
        b = json.load(open(src, encoding="utf-8"))
        keep, silent = [], []
        for e in b["lessons"]:
            rows = get(f"lessons?id=eq.{e['id']}&select=narration_manifest")
            if rows and (rows[0].get("narration_manifest") or []):
                keep.append(e)
            else:
                silent.append(e["lesson_number"])
        print(f"-- {slug}: {len(keep)} narrated, {len(silent)} without audio {silent}")
        if not keep:
            report[slug] = {"clips": 0, "no_audio": silent}
            continue
        fix = os.path.join(OUT, f"{slug}-repair_backup.json")
        with open(fix, "w", encoding="utf-8") as f:
            json.dump({"subject": slug, "unit": "label-sweep-repair", "lessons": keep},
                      f, ensure_ascii=False, indent=1)
        cmd = [sys.executable, os.path.join(SCRIPTS, "_retrofc", "_renarrate_from_backup.py"),
               "--backup", fix] + (["--dry-run"] if args.dry_run else [])
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        m = re.search(r"Regenerated (\d+) clips", p.stdout or "")
        v = re.search(r"(\d+)/(\d+) clips verified", p.stdout or "")
        report[slug] = {"clips": int(m.group(1)) if m else f"rc={p.returncode}",
                        "verified": v.group(0) if v else None, "no_audio": silent}
        print(f"   {report[slug]}")
        if p.returncode != 0:
            print((p.stdout or "")[-800:], (p.stderr or "")[-500:])

    with open(os.path.join(OUT, "_renarrate_repair.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
