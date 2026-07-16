import json, re

live = json.load(open("_CHK_L13_live.json", encoding="utf-8"))

# --- find pre-dump entry ---
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID = "a33d3e1a-9399-4ea4-9132-b391a705d6a7"

def find_entry(obj):
    # pre-dump could be list of rows or dict keyed
    if isinstance(obj, list):
        for row in obj:
            if isinstance(row, dict) and row.get("id") == ID:
                return row
    if isinstance(obj, dict):
        if ID in obj:
            return obj[ID]
        # maybe keyed by lesson key
        for k, v in obj.items():
            if isinstance(v, dict) and v.get("id") == ID:
                return v
    return None

entry = find_entry(pre)
print("pre entry type:", type(pre), "found:", entry is not None)
if entry is not None:
    pd_pre = entry.get("practice_data", entry)
    print("pre pd keys:", list(pd_pre.keys()) if isinstance(pd_pre, dict) else "?")
    for fld in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pd_pre.get(fld), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {fld}: {'SAME' if a==b else 'CHANGED'}")
        if a != b:
            print("  PRE :", a[:500])
            print("  LIVE:", b[:500])

# --- em dash scan in student-facing strings ---
EMDASH = "—"
hits = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            # skip internal note fields
            if k in ("note", "expect_note", "check", "pattern"):
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if EMDASH in o:
            hits.append((path, o))
walk(live, "root")
print("\nEM DASH hits (student-facing):", len(hits))
for p, s in hits:
    print("  ", p, "::", s[:80])

# --- check all box answers are numeric ---
badbox = []
def check_boxes(steps, path):
    for i, st in enumerate(steps):
        if isinstance(st, dict) and "answer" in st:
            if not isinstance(st["answer"], (int, float)) or isinstance(st["answer"], bool):
                badbox.append((f"{path}[{i}]", st["answer"]))
g = live["guided"]
check_boxes(g["opener"]["steps"], "guided.opener.steps")
for t in ("bronze","silver","gold"):
    check_boxes(g["teach"][t]["steps"], f"guided.teach.{t}.steps")
for tier in ("bronze","silver","gold"):
    for pi, prob in enumerate(live["problem_bank"][tier]):
        for gi, st in enumerate(prob.get("guided_steps", [])):
            if "answer" in st and not isinstance(st["answer"], (int,float)):
                badbox.append((f"{tier}[{pi}].guided_steps[{gi}]", st["answer"]))
print("\nNon-numeric box answers:", badbox)
