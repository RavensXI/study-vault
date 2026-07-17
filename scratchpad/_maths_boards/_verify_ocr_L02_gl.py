# -*- coding: utf-8 -*-
import json, io, re
F = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/lesson_maths-ocr_probability-statistics-L02.json"
pd = json.load(io.open(F, encoding="utf-8"))
errs = []

def svg_region_check(disp, path):
    for svg in re.findall(r"<svg.*?</svg>", disp, re.S):
        if "0 0 260 180" not in svg:
            continue
        nums = []
        for m in re.findall(r'<text x="(\d+)" y="(\d+)"[^>]*>([^<]+)</text>', svg):
            x, y, t = int(m[0]), int(m[1]), m[2]
            if y in (96, 150):
                nums.append(t)
        tot = re.search(r'Total:\s*([\d.]+)', svg)
        if not tot:
            continue
        total = float(tot.group(1))
        try:
            region_vals = [float(t) for t in nums]
        except ValueError:
            continue
        s = round(sum(region_vals), 6)
        if abs(s - total) > 1e-6:
            errs.append("%s: svg regions sum %s != total %s (%s)" % (path, s, total, nums))

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i, p in enumerate(pb[tier]):
        path = "%s[%d]" % (tier, i)
        svg_region_check(p["display"], path)
        boxes = [st for st in p.get("guided_steps",[]) if st.get("answer") is not None]
        sols = p["solutions"]
        if len(sols) == 1:
            if not any(abs(float(b["answer"])-float(sols[0]))<1e-9 for b in boxes):
                errs.append("%s: no box lands on solution %s" % (path, sols))
        else:
            if not (any(abs(float(b["answer"])-sols[0])<1e-9 for b in boxes) and any(abs(float(b["answer"])-sols[1])<1e-9 for b in boxes)):
                errs.append("%s: boxes do not produce %s" % (path, sols))
        for m in p.get("misconceptions",[]):
            e = m.get("expect")
            if e and len(e)==len(sols) and all(abs(float(a)-float(b))<0.011 for a,b in zip(e,sols)):
                errs.append("%s: expect==solution" % path)

gd = pd["guided"]
svg_region_check(gd["opener"]["steps"][0]["display"], "opener")
for tier in ("bronze","silver","gold"):
    svg_region_check(gd["teach"][tier]["display"], "teach."+tier)

for tier in ("bronze","silver","gold"):
    seen = {}
    for i,p in enumerate(pb[tier]):
        k = tuple(p["solutions"])
        if k in seen:
            errs.append("DUP %s: %s also at index %d" % (tier, k, seen[k]))
        seen[k]=i

if errs:
    print("ISSUES:")
    for e in errs: print("  -", e)
else:
    print("ALL CHECKS CLEAN: figure sums, box landings, expects, no duplicates")
print("counts:", {t:len(pb[t]) for t in ("bronze","silver","gold")})
