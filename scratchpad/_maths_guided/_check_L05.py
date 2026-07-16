# -*- coding: utf-8 -*-
import json

live = json.load(open("_live_L05.json", encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID = "75d6eee2-25e6-4977-b549-e965ddd6c735"

def find_entry(d):
    if isinstance(d, dict):
        if d.get("id") == ID:
            return d
        for v in d.values():
            r = find_entry(v)
            if r: return r
    elif isinstance(d, list):
        for v in d:
            r = find_entry(v)
            if r: return r
    return None

entry = find_entry(dump)
print("pre-dump entry found:", entry is not None)
if entry is not None:
    pre = entry.get("practice_data", entry)
    for fld in ["related_videos", "topic_links", "worked_examples"]:
        same = json.dumps(pre.get(fld), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {fld}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE :", json.dumps(pre.get(fld), ensure_ascii=False)[:500])
            print("  LIVE:", json.dumps(live.get(fld), ensure_ascii=False)[:500])
    print("pre keys:", sorted(pre.keys()))
    print("live keys:", sorted(live.keys()))

EM = "—"
EN = "–"
issues = []

def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if (EM in o or EN in o) and not path.endswith(".note"):
            issues.append(f"EM/EN-DASH at {path}: {o!r}")

walk(live, "root")

def scan_hints(o, path):
    if isinstance(o, dict):
        if "hint" in o and isinstance(o["hint"], str):
            h = o["hint"]
            if "\\(" in h or "$" in h or "\\frac" in h or "<" in h:
                issues.append(f"HINT-not-plain at {path}.hint: {h!r}")
        for k, v in o.items():
            scan_hints(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            scan_hints(v, f"{path}[{i}]")

scan_hints(live, "root")

def scan_boxes(o, path):
    if isinstance(o, dict):
        if "answer" in o and ("pre" in o or "post" in o):
            a = o["answer"]
            if not isinstance(a, (int, float)) or isinstance(a, bool):
                issues.append(f"NON-NUMERIC box answer at {path}: {a!r}")
        for k, v in o.items():
            scan_boxes(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            scan_boxes(v, f"{path}[{i}]")

scan_boxes(live, "root")

print("\n--- style issues ---")
for x in issues:
    print(x)
if not issues:
    print("none")

print("\n--- tier_guide steps word counts (budget 115) ---")
for tier, g in live["tier_guides"].items():
    wc = sum(len(s.split()) for s in g["steps"])
    print(f"{tier}: {wc} words; title={g['title']!r}")
