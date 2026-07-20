# -*- coding: utf-8 -*-
"""Independent check that the units pass added ONLY `unit` keys.

Compares each lesson_L*.json in the working tree against its committed HEAD
version with every `unit` key stripped from both sides. Anything that still
differs is something the pass changed beyond its brief.

Run from the worktree root:
    python scratchpad/_geo_guided/_verify_units.py
"""
import glob, io, json, os, subprocess, sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass


def strip_units(o):
    if isinstance(o, dict):
        return {k: strip_units(v) for k, v in o.items() if k != "unit"}
    if isinstance(o, list):
        return [strip_units(x) for x in o]
    return o


issues, checked = [], 0
for f in sorted(glob.glob("scratchpad/_geo_guided/lesson_L*.json")):
    key = os.path.basename(f)[7:10]
    gitpath = f.replace(os.sep, "/")
    try:
        raw = subprocess.check_output(["git", "show", "HEAD:" + gitpath],
                                      text=True, encoding="utf-8")
        old = json.loads(raw)
    except Exception as e:
        issues.append("%s: no committed version to compare (%s)" % (key, e))
        continue
    new = json.load(io.open(f, encoding="utf-8"))
    checked += 1
    if strip_units(old) == strip_units(new):
        continue
    for tier in ("bronze", "silver", "gold"):
        oa = (old.get("problem_bank") or {}).get(tier) or []
        nb = (new.get("problem_bank") or {}).get(tier) or []
        if len(oa) != len(nb):
            issues.append("%s %s: problem count changed %d -> %d" % (key, tier, len(oa), len(nb)))
            continue
        for i, (a, b) in enumerate(zip(oa, nb)):
            sa, sb = strip_units(a), strip_units(b)
            if sa == sb:
                continue
            changed = sorted(k for k in set(sa) | set(sb) if sa.get(k) != sb.get(k))
            issues.append("%s %s[%d] also changed: %s" % (key, tier, i, ", ".join(changed)))
    # anything outside the bank
    oo = {k: v for k, v in strip_units(old).items() if k != "problem_bank"}
    nn = {k: v for k, v in strip_units(new).items() if k != "problem_bank"}
    for k in sorted(set(oo) | set(nn)):
        if oo.get(k) != nn.get(k):
            issues.append("%s: top-level '%s' changed" % (key, k))

print("lessons compared:", checked)
print("NON-UNIT CHANGES:", len(issues))
for x in issues[:20]:
    print("  -", x)
if not issues:
    print("clean: the pass added unit keys and nothing else")
