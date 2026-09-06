"""
Roll the per-subject voice-pass results into voice/_summary.json, and re-probe
the live narrated fields so the summary states what is actually left, not what
was intended.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
OUT = os.path.join(HERE, "voice")
sys.path.insert(0, HERE)
from sweep_labels import plain, SENT_SPLIT, PROBE  # noqa: E402

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": K, "Authorization": "Bearer " + K}


def api(path, tries=5):
    for a in range(tries):
        try:
            return json.loads(urllib.request.urlopen(
                urllib.request.Request(f"{U}/rest/v1/{path}", headers=HDR), timeout=180).read())
        except Exception:
            if a == tries - 1:
                raise
            time.sleep(2 * (a + 1))


wl = json.load(open(os.path.join(HERE, "labels", "_narrated_worklist.json"), encoding="utf-8"))
per_subject_hits = wl["per_subject"]

rows = []
for slug, hits in sorted(per_subject_hits.items()):
    edits_p = os.path.join(OUT, f"edits_{slug}.json")
    res_p = os.path.join(OUT, f"_result_{slug}.json")
    e = json.load(open(edits_p, encoding="utf-8")) if os.path.exists(edits_p) else {"edits": [], "skipped": []}
    r = json.load(open(res_p, encoding="utf-8")) if os.path.exists(res_p) else {}
    rows.append({
        "subject": slug,
        "hits": hits,
        "rewritten": r.get("sentences_rewritten", len(e["edits"])),
        "lessons_patched": r.get("lessons_patched", 0),
        "blocks_renarrated": r.get("renarrated_clips", 0),
        "verified": r.get("verified"),
        "lessons_without_audio": r.get("lessons_without_audio", []),
        "skipped": [{"lesson_id": s.get("lesson_id"), "lesson_number": s.get("lesson_number"),
                     "field": s.get("field"), "reason": s.get("reason"),
                     "sentence": s.get("sentence")} for s in (r.get("skipped") or e.get("skipped", []))],
    })

# ---- re-probe the live narrated fields of every lesson the worklist touched
ids = sorted({h["lesson_id"] for h in wl["hits"]})
by_id = {}
for i in range(0, len(ids), 25):
    q = urllib.parse.quote(",".join(ids[i:i + 25]), safe="")
    for row in api(f"lessons?id=in.({q})&select=id,lesson_number,content_html,conclusion_html"):
        by_id[row["id"]] = row
remaining = []
for h in wl["hits"]:
    row = by_id.get(h["lesson_id"])
    if not row:
        continue
    for s in SENT_SPLIT.findall(plain(row.get(h["field"]) or "")):
        s = s.strip()
        if s and PROBE.search(s) and s[:300] == h["sentence"]:
            remaining.append({"subject": h["subject"], "lesson_id": h["lesson_id"],
                              "field": h["field"], "sentence": s[:300]})

summary = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "worklist_hits": wl["total_hits"],
    "subjects": len(rows),
    "sentences_rewritten": sum(r["rewritten"] for r in rows),
    "sentences_skipped": sum(len(r["skipped"]) for r in rows),
    "lessons_patched": sum(r["lessons_patched"] for r in rows),
    "blocks_renarrated": sum(r["blocks_renarrated"] for r in rows if isinstance(r["blocks_renarrated"], int)),
    "validator_rejections": sum(1 for r in rows for s in r["skipped"] if s.get("reason") == "validator"),
    "hits_still_present_live": len(remaining),
    "hits_still_present_detail": remaining,
    "per_subject": rows,
}
with open(os.path.join(OUT, "_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=1)
for k in ("worklist_hits", "subjects", "sentences_rewritten", "sentences_skipped",
          "lessons_patched", "blocks_renarrated", "validator_rejections", "hits_still_present_live"):
    print(f"  {k}: {summary[k]}")
