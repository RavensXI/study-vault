"""Repair the clustering pass without re-spending the triage.

Two wounds from the overnight run:
  1. Four cluster batches died on JSON parse errors, dropping ~180
     qualifying lessons from every cluster.
  2. The final merge call returned nothing - thinking consumed its whole
     12000-token budget - so the report ranked 681 UNMERGED mini-clusters
     and the top item served only 3 lessons.

This re-clusters only the uncovered lessons (retrying parse failures),
then re-runs the merge with a budget thinking cannot exhaust, rebuilds
the canonical set exactly as phase_b would have, and rewrites the report.
"""
import json, sys
import corpus_audit as ca
import canary

s = ca.load()
yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
raw = s["clusters_raw"]
print("qualifying lessons: %d   raw clusters: %d" % (len(yes), len(raw)), flush=True)

# ---- 1. re-cluster the lessons the failed batches dropped ----------------
covered = set()
for c in raw:
    covered.update(i for i in c.get("items", []) if isinstance(i, int))
missing = [i for i in range(len(yes)) if i not in covered]
print("uncovered by any cluster: %d" % len(missing), flush=True)

BATCH = 30
for start in range(0, len(missing), BATCH):
    idxs = missing[start:start + BATCH]
    # keep GLOBAL indices in the labels - the items the model echoes back
    # must index into `yes`, same as the original run
    items = "\n".join(
        "%d. [%s] %s — %s" % (i, yes[i]["subject"], yes[i]["title"][:70],
                              (yes[i]["triage"].get("misconception") or "")[:190])
        for i in idxs)
    got = None
    for attempt in range(3):
        try:
            got = canary.jparse(canary.call(5, canary.SONNET, "recluster:%d" % start,
                                            ca.CLUSTER_SYS, items, 8000))
            break
        except Exception as e:
            print("  batch %d attempt %d failed: %s" % (start, attempt + 1, str(e)[:100]), flush=True)
    if got:
        raw.extend(got.get("clusters", []))
        print("  batch %d-%d -> %d clusters" % (start, start + len(idxs),
                                                len(got.get("clusters", []))), flush=True)
s["clusters_raw"] = raw
ca.save(s)

# ---- 2. the merge, with a budget thinking cannot exhaust -----------------
blob = json.dumps([{"id": c["id"], "name": c.get("name"), "teaches": c.get("teaches")}
                   for c in raw], indent=0)
m = None
for attempt in range(3):
    try:
        m = canary.jparse(canary.call(5, canary.SONNET, "merge", ca.MERGE_SYS, blob, 32000))
        break
    except Exception as e:
        print("merge attempt %d failed: %s" % (attempt + 1, str(e)[:110]), flush=True)
if not m:
    sys.exit("merge failed three times - stopping rather than reporting unmerged clusters")

absorb = {}
for c in m.get("canonical", []):
    for a in c.get("absorbs", []):
        absorb[a] = c["id"]
merged = {}
for c in raw:
    cid = absorb.get(c["id"], c["id"])
    tgt = merged.setdefault(cid, {"id": cid, "name": c.get("name"),
                                  "teaches": c.get("teaches"), "items": []})
    tgt["items"].extend(c.get("items", []))
for c in m.get("canonical", []):
    if c["id"] in merged:
        merged[c["id"]]["name"] = c.get("name") or merged[c["id"]]["name"]
        merged[c["id"]]["teaches"] = c.get("teaches") or merged[c["id"]]["teaches"]
canon = list(merged.values())
print("merged %d raw clusters -> %d canonical" % (len(raw), len(canon)), flush=True)

# ---- 3. resolve lessons, rank, save, report ------------------------------
for c in canon:
    c["lessons"] = []
    seen = set()
    for idx in c.get("items", []):
        if isinstance(idx, int) and 0 <= idx < len(yes) and idx not in seen:
            seen.add(idx)
            l = yes[idx]
            c["lessons"].append({"subject": l["subject"], "board": l.get("board"),
                                 "unit": l["unit"], "n": l["n"], "title": l["title"],
                                 "url": "/lesson/%s/%s/%s" % (l["subject"], l["unit"], l["n"])})
    c["count"] = len(c["lessons"])
canon.sort(key=lambda c: -c["count"])
s["clusters"] = canon
ca.save(s)

ca.flush_ledger()
ca.report()
print("repair done ($%.2f this run)" % ca.spent_this_run(), flush=True)
