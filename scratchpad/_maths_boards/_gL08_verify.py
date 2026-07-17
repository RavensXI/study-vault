# -*- coding: utf-8 -*-
import json, io, re, os
pd = json.load(io.open(os.path.join(os.path.dirname(__file__), "lesson_maths-eduqas_graphs-L08.json"), encoding="utf-8"))
errs = []

def coords(text):
    # find \((a, b)\) pairs
    return [(float(a), float(b)) for a, b in re.findall(r"\\\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\\\)", text)]

def heights(text):
    return [float(x) for x in re.findall(r"y_\d+\s*=\s*(-?\d+(?:\.\d+)?)", text)]

def to_num(x):
    return int(x) if float(x).is_integer() else x

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        path = "%s[%d]" % (tier, i)
        it = p.get("input_type")
        sol = p["solutions"]
        disp = p["display"]
        # duplicate within tier (non-mc)
        if it != "multiple_choice":
            k = tuple(sol)
            if k in seen:
                errs.append("%s dup solution %s (also %s)" % (path, sol, seen[k]))
            seen[k] = path
        # fresh solve
        cs = coords(disp)
        hs = heights(disp)
        if it == "single_value" and "tangent" in disp and len(cs) >= 2:
            (x1, y1), (x2, y2) = cs[0], cs[1]
            m = (y2 - y1) / (x2 - x1)
            if abs(m - sol[0]) > 1e-9:
                errs.append("%s gradient recompute %s != sol %s" % (path, m, sol[0]))
            # svg labels must contain both coords
            for (cx, cy) in (cs[0], cs[1]):
                lbl = "(%s, %s)" % (to_num(cx) if cx >= 0 else "−%s" % to_num(abs(cx)),
                                    to_num(cy) if cy >= 0 else "−%s" % to_num(abs(cy)))
                if lbl not in disp:
                    errs.append("%s svg missing coord label %s" % (path, lbl))
            # svg run/rise labels
            run = to_num(x2 - x1); rise = y2 - y1
            if ("run %s" % (run if run >= 0 else "−%s" % abs(run))) not in disp and rise != 0:
                errs.append("%s svg missing run label" % path)
        if "trapezium" in disp and hs:
            n = disp.count("strips")
            # infer h
            mh = re.search(r"h\s*=\s*(\d+)", disp)
            if mh:
                h = float(mh.group(1))
            else:
                # y=x^2 from 0 to X with (len-1) strips, h=1 here
                h = 1.0
            ends = hs[0] + hs[-1]; mids = sum(hs[1:-1]); area = (h / 2) * (ends + 2 * mids)
            if abs(area - sol[0]) > 1e-9:
                errs.append("%s trap recompute %s != sol %s (h=%s heights=%s)" % (path, area, sol[0], h, hs))
        # misconceptions
        for j, mm in enumerate(p.get("misconceptions", [])):
            if "expect" not in mm:
                errs.append("%s.misc[%d] no expect key" % (path, j))
            e = mm.get("expect")
            if e is not None and abs(float(e) - float(sol[0])) < 1e-9:
                errs.append("%s.misc[%d] expect==sol" % (path, j))
        # guided steps final box lands on sol (non-mc)
        gs = p.get("guided_steps")
        if gs:
            boxes = [st for st in gs if st.get("answer") is not None]
            if it == "single_value" and "tangent" in disp:
                # gradient step (3rd box) should equal sol
                if abs(boxes[2]["answer"] - sol[0]) > 1e-9:
                    errs.append("%s gs gradient box %s != sol" % (path, boxes[2]["answer"]))
            if "trapezium" in disp:
                if abs(boxes[-1]["answer"] - sol[0]) > 1e-9:
                    errs.append("%s gs area box %s != sol" % (path, boxes[-1]["answer"]))

# verify expects derive from the described error
# inverted: run/rise ; sign: |m|? ; nodouble & hfactor recompute
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        disp = p["display"]; sol = p["solutions"][0]
        for mm in p.get("misconceptions", []):
            pat = mm.get("pattern"); e = mm.get("expect")
            if e is None:
                continue
            cs = coords(disp); hs = heights(disp)
            if pat == "rise_run_inverted" and len(cs) >= 2:
                (x1, y1), (x2, y2) = cs[0], cs[1]
                inv = (x2 - x1) / (y2 - y1)
                if abs(inv - e) > 1e-9:
                    errs.append("%s[%d] inverted expect %s != run/rise %s" % (tier, i, e, inv))
            if pat == "sign_error" and len(cs) >= 2:
                (x1, y1), (x2, y2) = cs[0], cs[1]
                flip = abs((y2 - y1) / (x2 - x1))
                if abs(flip - e) > 1e-9:
                    errs.append("%s[%d] sign expect %s != |m| %s" % (tier, i, e, flip))
            if pat == "middles_not_doubled" and hs:
                mh = re.search(r"h\s*=\s*(\d+)", disp); h = float(mh.group(1)) if mh else 1.0
                val = (h / 2) * (hs[0] + hs[-1] + sum(hs[1:-1]))
                if abs(val - e) > 1e-9:
                    errs.append("%s[%d] nodouble expect %s != %s" % (tier, i, e, val))
            if pat == "wrong_h_factor" and hs:
                val = 0.5 * (hs[0] + hs[-1] + 2 * sum(hs[1:-1]))
                if abs(val - e) > 1e-9:
                    errs.append("%s[%d] hfactor expect %s != %s" % (tier, i, e, val))

# em dash scan (full)
def scan(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            scan(v, path + "." + k)
    elif isinstance(o, list):
        for j, v in enumerate(o): scan(v, "%s[%d]" % (path, j))
    elif isinstance(o, str) and "—" in o:
        errs.append("EM DASH at " + path)
scan(pd, "pd")

print("ERRORS:" if errs else "CLEAN: all recomputes match, no dups, expects derive, no em dash")
for e in errs:
    print("  -", e)
