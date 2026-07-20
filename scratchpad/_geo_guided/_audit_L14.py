# -*- coding: utf-8 -*-
"""Self-audit of lesson_L14.json beyond what _validate_geo.py checks."""
import io, json, os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L14.json"), encoding="utf-8"))

problems = []
ALLOWED = {
    "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
    + n for n in [
        "pendle-hill-z16-final.jpg", "yorkshire-dales-z15-final.jpg",
        "lake-district-z16-final.jpg", "northumberland-z15-final.jpg"]}

bad = []
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        path = "%s[%d]" % (tier, i)
        problems.append((path, p))
        if p.get("image") not in ALLOWED:
            bad.append(path + " image not in the verified allow-list: %r" % p.get("image"))
        it = p.get("input_type")
        if it == "multiple_choice" and "unit" in p:
            bad.append(path + " multiple_choice must not carry a unit")
        gs = p.get("guided_steps") or []
        first = next((s for s in gs if s.get("answer") is not None), None)
        if first is None:
            bad.append(path + " no box")
        else:
            pre = first["pre"].lower()
            if not any(w in pre for w in ("find", "easting", "northing", "line", "count",
                                          "grid", "words", "square")):
                bad.append(path + " first box may not be a locating step: " + first["pre"][:70])
        last = gs[-1] if gs else {}
        lastbox = [s for s in gs if s.get("answer") is not None]
        if lastbox and not lastbox[-1].get("done"):
            bad.append(path + " final box has no done note (check step)")
        # MC: final say must name an existing option or 'first'
        if it == "multiple_choice":
            says = [s.get("say", "") for s in gs if s.get("say")]
            if not says:
                bad.append(path + " MC walk has no closing say step")
            for m in p.get("misconceptions") or []:
                e = m.get("expect")
                if e is not None and not (isinstance(e, int) and 0 <= e < len(p["options"])):
                    bad.append(path + " MC expect not a valid option index: %r" % e)
                if e is not None and e in p["solutions"]:
                    bad.append(path + " MC expect equals the correct option")
        # units only on measured quantities
        if p.get("unit") and it == "multiple_choice":
            bad.append(path + " unit on MC")

print("problems:", len(problems))
print("with unit:", [pth for pth, p in problems if p.get("unit")])
print("MC count:", sum(1 for _, p in problems if p.get("input_type") == "multiple_choice"))
print("images used:", sorted({p["image"].rsplit("/", 1)[-1] for _, p in problems}))

# box inventory for manual re-check
for pth, p in problems:
    vals = [s["answer"] for s in p.get("guided_steps", []) if s.get("answer") is not None]
    print("%-10s sol=%-8s boxes=%s" % (pth, p["solutions"], vals))

for k in ("opener",):
    vals = [s["answer"] for s in pd["guided"][k]["steps"] if s.get("answer") is not None]
    print("opener boxes", vals)
for t in ("bronze", "silver", "gold"):
    vals = [s["answer"] for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    print("teach", t, "boxes", vals)

print()
if bad:
    print("ISSUES (%d):" % len(bad))
    for b in bad:
        print("  -", b)
else:
    print("self-audit clean")
