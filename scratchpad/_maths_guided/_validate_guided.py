# -*- coding: utf-8 -*-
"""Deterministic gate for fan-out lessons. Usage:
    python _validate_guided.py <practice_data.json>
Exit 0 = PASS. Any failure prints the reasons and exits 1.
Checks structure, style (no em dashes), guided-step shape, completion
boundaries, budgets. It does NOT check the maths: that is the checker
agent's job (independent fresh-solve of every problem and every box).
"""
import json, io, sys

EM = "—"
fails = []

def fail(msg):
    fails.append(msg)

def words(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])

def scan_dashes(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("note", "guided_skip_reason"):
                continue
            scan_dashes(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_dashes(v, path + "[%d]" % i)
    elif isinstance(obj, str) and EM in obj:
        fail("em dash at " + path + ": ..." + obj[max(0, obj.find(EM) - 25):obj.find(EM) + 25] + "...")

def check_steps(steps, path, need_substitute, min_boxes=3):
    boxes = 0
    sub_at = None
    for i, st in enumerate(steps):
        p = path + "[%d]" % i
        if not isinstance(st, dict):
            fail(p + " not a dict"); continue
        has_box = st.get("answer") is not None
        if has_box:
            boxes += 1
            if not isinstance(st["answer"], (int, float)):
                fail(p + " answer not numeric: " + repr(st["answer"]))
            if not (st.get("hint") or "").strip():
                fail(p + " box has no hint")
            if not (st.get("pre") or "").strip():
                fail(p + " box has no pre text")
        else:
            if not (st.get("say") or "").strip():
                fail(p + " has neither answer nor say")
        if st.get("phase") == "substitute" and sub_at is None:
            sub_at = i
    if boxes < min_boxes:
        fail(path + " has %d boxes, need >= %d" % (boxes, min_boxes))
    if need_substitute:
        if sub_at is None:
            fail(path + " has no phase:'substitute' step (completion boundary)")
        else:
            live = sum(1 for st in steps[sub_at:] if st.get("answer") is not None)
            if live < 2:
                fail(path + " completion boundary leaves only %d live boxes, need >= 2" % live)
            if sub_at < 1:
                fail(path + " completion boundary at step 0: nothing would be pre-worked")
    return boxes

def main(fn):
    pd = json.load(io.open(fn, encoding="utf-8"))

    scan_dashes(pd, "pd")

    pb = pd.get("problem_bank") or {}
    for tier in ("bronze", "silver", "gold"):
        probs = pb.get(tier) or []
        if not probs:
            fail("problem_bank." + tier + " empty")
        if not (pb.get(tier + "_description") or "").strip():
            fail("problem_bank." + tier + "_description missing")
        seen = set()
        for i, p in enumerate(probs):
            path = tier + "[%d]" % i
            if not (p.get("display") or "").strip():
                fail(path + " no display")
            sols = p.get("solutions")
            if not isinstance(sols, list) or not sols or not all(isinstance(x, (int, float)) for x in sols):
                fail(path + " solutions must be a non-empty numeric list")
            else:
                key = tuple(sols)
                if key in seen and p.get("input_type") != "multiple_choice":
                    fail(path + " duplicate solution values within tier: " + repr(sols))
                seen.add(key)
            if not (p.get("hint") or "").strip():
                fail(path + " no hint")
            it = p.get("input_type") or "single_value"
            gs = p.get("guided_steps")
            if it == "multiple_choice" or p.get("guided_skip_reason"):
                pass  # walk optional
            elif not gs:
                fail(path + " missing guided_steps (required unless multiple_choice or guided_skip_reason)")
            if gs:
                check_steps(gs, path + ".guided_steps", need_substitute=True)
            for j, m in enumerate(p.get("misconceptions") or []):
                mp = path + ".misconceptions[%d]" % j
                if not (m.get("message") or "").strip():
                    fail(mp + " no message")
                if "expect" not in m:
                    fail(mp + " missing expect key (null allowed, absent not)")
                e = m.get("expect")
                if e is not None and isinstance(sols, list) and sols:
                    ev = e if isinstance(e, list) else [e]
                    sv = [float(x) for x in sols]
                    if len(ev) == len(sv) and all(isinstance(x, (int, float)) for x in ev):
                        if all(abs(float(a) - b) < 0.011 for a, b in zip(ev, sv)):
                            fail(mp + " expect equals the correct answer")

    tg = pd.get("tier_guides") or {}
    for tier in ("bronze", "silver", "gold"):
        g = tg.get(tier) or {}
        path = "tier_guides." + tier
        if not (g.get("title") or "").strip():
            fail(path + ".title missing")
        steps = g.get("steps") or []
        if not (2 <= len(steps) <= 4):
            fail(path + ".steps must have 2-4 entries")
        total = sum(words(s) for s in steps)
        if total > 115:
            fail(path + ".steps total %d words, budget 115" % total)
        ex = g.get("example") or {}
        if not (ex.get("question") or "").strip() or not ex.get("steps"):
            fail(path + ".example missing question/steps")

    gd = pd.get("guided") or {}
    op = gd.get("opener") or {}
    if not op.get("steps"):
        fail("guided.opener missing/empty")
    else:
        if not any(st.get("answer") is not None for st in op["steps"]):
            fail("guided.opener has no interactive box")
        check_steps(op["steps"], "guided.opener.steps", need_substitute=False, min_boxes=1)
    for tier in ("bronze", "silver", "gold"):
        t = (gd.get("teach") or {}).get(tier) or {}
        if not t.get("steps") or not (t.get("display") or "").strip():
            fail("guided.teach." + tier + " missing display/steps")
        else:
            if sum(1 for st in t["steps"] if st.get("answer") is not None) < 4:
                fail("guided.teach." + tier + " needs >= 4 boxes")

    mc = pd.get("method_card") or {}
    if not (mc.get("title") or "").strip():
        fail("method_card.title missing")
    if words(mc.get("content") or "") > 140:
        fail("method_card.content %d words, budget 140 (slim reference only)" % words(mc.get("content") or ""))
    if len(mc.get("steps") or []) > 4:
        fail("method_card.steps: max 4")

    if fails:
        print("FAIL (%d):" % len(fails))
        for f in fails[:60]:
            print("  -", f)
        sys.exit(1)
    print("PASS: structure, style, budgets all clean")

if __name__ == "__main__":
    main(sys.argv[1])
