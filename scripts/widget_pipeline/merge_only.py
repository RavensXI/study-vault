"""Merge-only repair: fold the 862 raw clusters into canonical groups.

The full-merge prompt made Sonnet think until it exhausted any budget we
gave it (12k, then 32k twice) without emitting a word. Two changes:
  - thinking disabled: this is matching, not reasoning
  - minimal output: ONLY groups of ids that are the same idea, keep-first,
    instead of re-emitting every cluster's name and teaches
"""
import json, sys
import corpus_audit as ca
import canary

MERGE_MIN = """Different batches produced overlapping cluster labels for the same GCSE misconceptions. Find the duplicates.

Two clusters are the SAME when a single interactive widget - same numbers, same interaction - would teach both. Board and subject wording differences are irrelevant. Do NOT merge ideas that are merely related ("wasted energy disappears" is not "current is used up").

Reply with ONLY JSON - just the groups that contain two or more of the given ids. The FIRST id in each group is kept; the rest fold into it. Clusters not listed stay as they are.
{"groups": [["keep-this-id", "folds-in", "folds-in"], ...]}"""

s = ca.load()
yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
raw = s["clusters_raw"]
print("raw clusters: %d" % len(raw), flush=True)

blob = "\n".join("%s | %s | %s" % (c["id"], c.get("name") or "", (c.get("teaches") or "")[:150])
                 for c in raw)

def call_nothink(label, system, user, max_tokens):
    kw = dict(model=canary.SONNET, max_tokens=max_tokens, system=system,
              messages=[{"role": "user", "content": user}],
              thinking={"type": "disabled"})
    text = []
    with canary.cl.messages.stream(**kw) as st:
        for chunk in st.text_stream:
            text.append(chunk)
        r = st.get_final_message()
    canary.ledger_add(5, canary.SONNET, label, r.usage)
    return "".join(text).strip()

m = None
for attempt in range(3):
    try:
        m = canary.jparse(call_nothink("merge-min", MERGE_MIN, blob, 16000))
        break
    except Exception as e:
        print("attempt %d failed: %s" % (attempt + 1, str(e)[:110]), flush=True)
if not m:
    sys.exit("merge failed")

absorb = {}
for g in m.get("groups", []):
    if len(g) >= 2:
        for a in g[1:]:
            absorb[a] = g[0]
print("fold instructions: %d ids fold into %d keepers"
      % (len(absorb), len(set(absorb.values()))), flush=True)

merged = {}
for c in raw:
    cid = absorb.get(c["id"], c["id"])
    tgt = merged.setdefault(cid, {"id": cid, "name": c.get("name"),
                                  "teaches": c.get("teaches"), "items": []})
    tgt["items"].extend(c.get("items", []))
    if cid == c["id"]:          # the keeper's own label wins
        tgt["name"], tgt["teaches"] = c.get("name"), c.get("teaches")
canon = list(merged.values())
print("merged %d -> %d canonical" % (len(raw), len(canon)), flush=True)

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
print("MERGE DONE", flush=True)
