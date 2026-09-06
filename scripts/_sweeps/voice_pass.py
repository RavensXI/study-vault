"""
Examiner-voice pass over the NARRATED fields (content_html, conclusion_html).

sweep_labels.py deliberately left these two fields alone and counted their
examiner-voice sentences into labels/_narrated_worklist.json (604 hits). Each
one has been read in its paragraph and rewritten BY HAND into the site's own
voice; this script is the applicator, not the author.

Input: a per-subject edits file (written by hand, one per subject)

    {"subject": "astronomy-edexcel",
     "edits":   [{"lesson_id": "...", "field": "content_html",
                  "find": "<raw substring>", "replace": "<raw substring>"}],
     "skipped": [{"lesson_id": "...", "reason": "false positive - ..."}]}

Per subject it will:
  1. fetch the live rows and verify every `find` occurs EXACTLY ONCE
  2. guard the html: the tag sequence and the data-narration-id chunk ids must
     be byte-identical before and after, and no chunk may end up empty
  3. run the content validator on the before row and the candidate row and skip
     (with a logged row) any lesson that gains a NEW violation kind
  4. write voice/_backup_<subject>.json BEFORE patching
  5. PATCH the rows one at a time through PostgREST
  6. re-narrate the changed blocks via
     scripts/_retrofc/_renarrate_from_backup.py, which regenerates only the
     chunks whose narrated TEXT changed and verifies each MP3 on R2
  7. write voice/_result_<subject>.json

Usage:
    python scripts/_sweeps/voice_pass.py --edits scripts/_sweeps/voice/edits_<subject>.json --dry-run
    python scripts/_sweeps/voice_pass.py --edits scripts/_sweeps/voice/edits_<subject>.json
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
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
ROOT = os.path.dirname(SCRIPTS)
OUT = os.path.join(HERE, "voice")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

from sweep_labels import violations, kind, COLS  # noqa: E402  identical validator gate
try:
    from lib.narration import extract_narration_chunks  # noqa: E402
except Exception:
    extract_narration_chunks = None

U = os.environ["SUPABASE_URL"]
K = os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": K, "Authorization": "Bearer " + K}
NARRATED = ("content_html", "conclusion_html")


def api(path, method="GET", body=None, tries=5):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    hdr = dict(HDR)
    if data:
        hdr["Content-Type"] = "application/json"
        hdr["Prefer"] = "return=minimal"
    for a in range(tries):
        try:
            req = urllib.request.Request(f"{U}/rest/v1/{path}", data=data, headers=hdr, method=method)
            raw = urllib.request.urlopen(req, timeout=180).read()
            return json.loads(raw) if raw else None
        except Exception as e:  # noqa: BLE001
            if a == tries - 1:
                detail = ""
                if isinstance(e, urllib.error.HTTPError):
                    try:
                        detail = e.read().decode("utf-8", "replace")[:400]
                    except Exception:
                        pass
                raise RuntimeError(f"{method} {path[:120]} failed: {e} {detail}")
            time.sleep(2 * (a + 1))


def structurally_safe(before, after):
    """Tags byte-for-byte, narration chunk ids unchanged, no chunk emptied."""
    if re.findall(r"<[^>]+>", before) != re.findall(r"<[^>]+>", after):
        return "tag sequence changed"
    if "data-narration-id" in before and extract_narration_chunks is not None:
        try:
            a = dict(extract_narration_chunks(before))
            b = dict(extract_narration_chunks(after))
        except Exception:
            return None
        if set(a) != set(b):
            return "narration chunk ids changed"
        if any(not (b[i] or "").strip() for i in b):
            return "a narration chunk would be empty"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edits", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-narrate", action="store_true")
    args = ap.parse_args()

    spec = json.load(open(args.edits, encoding="utf-8"))
    slug = spec["subject"]
    edits = spec.get("edits", [])
    skipped = list(spec.get("skipped", []))
    print(f"== {slug}: {len(edits)} edits, {len(skipped)} logged skips ==")

    ids = sorted({e["lesson_id"] for e in edits})
    rows = {}
    for i in range(0, len(ids), 25):
        q = urllib.parse.quote(",".join(ids[i:i + 25]), safe="")
        for r in api(f"lessons?id=in.({q})&select={COLS},narration_manifest"):
            rows[r["id"]] = r
    missing = [i for i in ids if i not in rows]
    if missing:
        raise SystemExit(f"lesson(s) not found: {missing}")

    # ---------------------------------------------------------------- apply
    plan, hard = [], []
    for lid in ids:
        row = rows[lid]
        mine = [e for e in edits if e["lesson_id"] == lid]
        cand = dict(row)
        applied = []
        for e in mine:
            f_ = e["field"]
            if f_ not in NARRATED:
                raise SystemExit(f"{lid}: field {f_} is not a narrated field")
            cur = cand.get(f_) or ""
            c = cur.count(e["find"])
            if c != 1:
                hard.append({"lesson_id": lid, "lesson_number": row.get("lesson_number"),
                             "field": f_, "reason": f"find occurs {c} times, expected exactly 1",
                             "find": e["find"][:200]})
                continue
            cand[f_] = cur.replace(e["find"], e["replace"], 1)
            applied.append(e)
        if not applied:
            continue
        bad = None
        for f_ in NARRATED:
            if (cand.get(f_) or "") != (row.get(f_) or ""):
                bad = structurally_safe(row.get(f_) or "", cand.get(f_) or "")
                if bad:
                    bad = f"{f_}: {bad}"
                    break
        if bad:
            hard.append({"lesson_id": lid, "lesson_number": row.get("lesson_number"),
                         "reason": f"structure guard - {bad}"})
            continue
        pre, post = violations(row), violations(cand)
        pre_k = {kind(v) for v in pre}
        new = [v for v in post if kind(v) not in pre_k]
        if any(v.startswith("VALIDATOR ERROR") for v in pre + post):
            new = ["validator could not run on this row"]
        if new:
            skipped.append({"lesson_id": lid, "lesson_number": row.get("lesson_number"),
                            "reason": "validator", "new": new[:5]})
            print(f"  L{row.get('lesson_number')}: VALIDATOR SKIP {new[:2]}")
            continue
        patch = {f_: cand[f_] for f_ in NARRATED
                 if (cand.get(f_) or "") != (row.get(f_) or "")}
        before = {f_: row.get(f_) for f_ in patch}
        plan.append({"row": row, "patch": patch, "before": before, "n": len(applied)})

    if hard:
        print(json.dumps(hard, ensure_ascii=False, indent=1)[:4000])
        raise SystemExit(f"{len(hard)} edit(s) could not be applied cleanly - fix the edits file")

    n_sent = sum(p["n"] for p in plan)
    print(f"  {len(plan)} lessons, {n_sent} sentences rewritten, "
          f"{len([s for s in skipped if s.get('reason') == 'validator'])} validator skips")
    if args.dry_run:
        for p in plan:
            print(f"  L{p['row'].get('lesson_number'):>3}  {p['n']} edit(s)  "
                  f"fields={sorted(p['patch'])}")
        return

    # ------------------------------------------------------- backup + patch
    backup = {"subject": slug, "unit": "voice-pass",
              "lessons": [{"id": p["row"]["id"], "lesson_number": p["row"].get("lesson_number"),
                           "before": p["before"]} for p in plan]}
    spec_backup = os.path.join(OUT, f"_backup_{slug}.json")
    with open(spec_backup, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=1)

    for p in plan:
        api(f"lessons?id=eq.{p['row']['id']}", method="PATCH", body=p["patch"])
    print(f"  patched {len(plan)} rows; backup {spec_backup}")

    # ---------------------------------------------------------- re-narrate
    result = {"subject": slug, "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "lessons_patched": len(plan), "sentences_rewritten": n_sent,
              "skipped": skipped, "backup": spec_backup}
    narrated = [p for p in plan if (p["row"].get("narration_manifest") or [])]
    silent = [p["row"].get("lesson_number") for p in plan if p not in narrated]
    result["lessons_without_audio"] = silent
    if narrated and not args.no_narrate:
        # the re-narrator insists on a *_backup.json basename
        nb = os.path.join(OUT, f"{slug}_backup.json")
        with open(nb, "w", encoding="utf-8") as f:
            json.dump({"subject": slug, "unit": "voice-pass",
                       "lessons": [{"id": p["row"]["id"],
                                    "lesson_number": p["row"]["lesson_number"],
                                    "before": p["before"]} for p in narrated]},
                      f, ensure_ascii=False, indent=1)
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "_retrofc", "_renarrate_from_backup.py"),
             "--backup", nb], cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        so = proc.stdout or ""
        m = re.search(r"Regenerated (\d+) clips", so)
        v = re.search(r"(\d+)/(\d+) clips verified", so)
        result["renarrated_clips"] = int(m.group(1)) if m else f"FAILED rc={proc.returncode}"
        result["verified"] = v.group(0) if v else None
        result["renarrate_rc"] = proc.returncode
        if proc.returncode != 0 or not m:
            result["renarrate_stderr"] = (proc.stderr or "")[-800:]
            print(so[-1500:])
            print((proc.stderr or "")[-800:])
        print(f"  re-narrated: {result['renarrated_clips']} clips, verified {result['verified']}")
    else:
        result["renarrated_clips"] = 0

    with open(os.path.join(OUT, f"_result_{slug}.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"  wrote {os.path.join(OUT, f'_result_{slug}.json')}")


if __name__ == "__main__":
    main()
