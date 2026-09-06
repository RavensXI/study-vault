"""Merge the label sweep's run fragments into one summary + worklists."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.join("scripts", "_sweeps", "labels")
def load(n):
    p = os.path.join(OUT, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

parts = [load("_summary_canary_business-aqa.json"), load("_summary_part1.json"), load("_summary.json")]
parts = [p for p in parts if p]
per, seen = [], set()
for p in parts:
    for t in p["per_subject"]:
        k = t.get("key") or t["subject"]
        if k in seen: continue
        seen.add(k); per.append(t)
per.sort(key=lambda t: t.get("key") or t["subject"])
agg = {"generated": parts[-1]["generated"], "mode": "live", "runs": len(parts),
       "subjects": len(per),
       "lessons_scanned": sum(t["lessons_scanned"] for t in per),
       "sweep1_band_renames": sum(t["band_renames"] for t in per),
       "sweep1_band_questions": sum(t["band_questions"] for t in per),
       "sweep1_tag_fixes": sum(t["tag_fixes"] for t in per),
       "sweep2_rewrites": sum(t["ev_rewrites"] for t in per),
       "rows_changed": sum(t["rows_changed"] for t in per),
       "rows_skipped_validator": sum(t["rows_skipped_validator"] for t in per),
       "subjects_skipped": [t["subject"] for t in per if t["skipped"]],
       "renarrated_clips": sum(t["renarrated_clips"] for t in per if isinstance(t.get("renarrated_clips"), int)),
       "renarrate_failures": [t.get("key") or t["subject"] for t in per if isinstance(t.get("renarrated_clips"), str)],
       "per_subject": per}

wl = {"examiner_unmatched": [], "tariff_tags": [], "ladder_conflicts": [], "ladder_residue": [], "validator_skips": []}
for n in ("_worklist_part1.json", "_worklist.json"):
    d = load(n)
    if not d: continue
    for k in wl:
        wl[k] += d.get(k, [])
# de-duplicate (the canary subject was scanned twice)
for k in wl:
    seen2, out = set(), []
    for e in wl[k]:
        s = json.dumps(e, sort_keys=True, ensure_ascii=False)
        if s in seen2: continue
        seen2.add(s); out.append(e)
    wl[k] = out
agg["worklist_examiner_unmatched"] = len(wl["examiner_unmatched"])
agg["worklist_tariff_tags"] = len(wl["tariff_tags"])
agg["worklist_ladder_conflicts"] = len(wl["ladder_conflicts"])
agg["worklist_ladder_residue"] = len(wl["ladder_residue"])

hits, seen3 = [], set()
for n in ("_narrated_worklist_part1.json", "_narrated_worklist.json"):
    d = load(n)
    if not d: continue
    for h in d["hits"]:
        s = json.dumps(h, sort_keys=True, ensure_ascii=False)
        if s in seen3: continue
        seen3.add(s); hits.append(h)
psub = {}
for h in hits: psub[h["subject"]] = psub.get(h["subject"], 0) + 1
agg["narrated_worklist_hits"] = len(hits)

json.dump(agg, open(os.path.join(OUT, "_summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(wl, open(os.path.join(OUT, "_worklist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"generated": agg["generated"], "total_hits": len(hits),
           "per_subject": dict(sorted(psub.items(), key=lambda kv: -kv[1])), "hits": hits},
          open(os.path.join(OUT, "_narrated_worklist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in agg.items():
    if k != "per_subject": print(f"  {k}: {v}")
