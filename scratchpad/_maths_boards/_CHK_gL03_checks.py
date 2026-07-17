import json, re

live = json.load(open("_CHK_gL03_live.json", encoding="utf-8"))[0]["practice_data"]

# --- em dash / en dash scan in student-facing strings ---
def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            # skip internal note fields
            if k == "note":
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj

print("=== EM DASH (U+2014) / EN DASH (U+2013) SCAN ===")
found = False
for path, s in walk(live):
    if "—" in s:
        print("EM DASH at", path, "::", repr(s[:80]))
        found = True
    if "–" in s:
        print("EN DASH at", path, "::", repr(s[:80]))
        found = True
if not found:
    print("none")

# --- HTML entity scan in plain-text fields ---
print("\n=== HTML ENTITY SCAN (&...;) in hint/pre/post/message ===")
ent = re.compile(r"&[a-zA-Z]+;|&#\d+;")
for path, s in walk(live):
    if ent.search(s) and any(x in path for x in [".hint", ".pre", ".post", ".message", ".display"]):
        print("ENTITY at", path, "::", repr(s[:80]))

# --- non-numeric guided_step answers ---
print("\n=== NON-NUMERIC BOX ANSWERS ===")
pb = live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i, p in enumerate(pb[tier]):
        for gi, s in enumerate(p.get("guided_steps", [])):
            if "answer" in s and not isinstance(s["answer"], (int, float)):
                print(f"{tier}[{i}].guided_steps[{gi}] answer not numeric: {s['answer']!r}")
# teach + opener
for tier in ["bronze","silver","gold"]:
    for gi, s in enumerate(live["guided"]["teach"][tier]["steps"]):
        if "answer" in s and not isinstance(s["answer"], (int,float)):
            print(f"teach.{tier}[{gi}] non-numeric {s['answer']!r}")
for gi, s in enumerate(live["guided"]["opener"]["steps"]):
    if "answer" in s and not isinstance(s["answer"], (int,float)):
        print(f"opener[{gi}] non-numeric {s['answer']!r}")

# --- phase boundary check ---
print("\n=== PHASE BOUNDARY (>=1 before, >=2 live boxes at/after) ===")
for tier in ["bronze","silver","gold"]:
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps", [])
        boxes = [gi for gi,s in enumerate(gs) if "answer" in s]
        phase_idx = [gi for gi,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not gs:
            print(f"{tier}[{i}] NO guided_steps (input_type={p.get('input_type')})")
            continue
        if not phase_idx:
            print(f"{tier}[{i}] NO phase tag")
            continue
        first_phase = phase_idx[0]
        before = [b for b in boxes if b < first_phase]
        after = [b for b in boxes if b >= first_phase]
        flag = "" if (len(before)>=1 and len(after)>=2) else "  <-- VIOLATION"
        print(f"{tier}[{i}] boxes_before={len(before)} boxes_at_after={len(after)}{flag}")
