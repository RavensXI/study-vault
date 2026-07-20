# -*- coding: utf-8 -*-
"""Deterministic gate for the Geography Skills guided fan-out.

    python _validate_geo.py <practice_data.json> [LESSON_KEY]

Exit 0 = PASS. Any failure prints reasons and exits 1.

Checks structure, style, guided-step shape, completion boundaries, budgets,
answer leakage, and (when LESSON_KEY is given) stimulus preservation against
the pre-fanout dump. It does NOT check geography facts or arithmetic: that is
the checker agent's job.
"""
import json, io, os, re, sys

# Windows consoles default to cp1252 and die on the unicode this content is
# full of (thin spaces, degree signs, arrows). Force UTF-8 on the way out.
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

EM = "—"
HERE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(HERE, "..", "_geo_audit", "_pre_dump_all.json")

fails = []
def fail(m): fails.append(m)

def words(s):
    return len([w for w in str(s).split() if w])

def strip_html(s):
    return re.sub(r"<[^>]+>", " ", str(s))

def walk(obj, path, fn):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, path + "." + str(k), fn)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, path + "[%d]" % i, fn)
    else:
        fn(obj, path)

EXEMPT_KEYS = ("note", "guided_skip_reason", "internal")

def scan_dashes(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in EXEMPT_KEYS:
                continue
            scan_dashes(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_dashes(v, path + "[%d]" % i)
    elif isinstance(obj, str) and EM in obj:
        i = obj.find(EM)
        fail("em dash at " + path + ": ..." + obj[max(0, i - 30):i + 30] + "...")

def scan_svg(obj, path):
    def check(v, p):
        if not isinstance(v, str) or "<svg" not in v:
            return
        for i, chunk in enumerate(v.split("<svg")[1:]):
            tag = chunk.split(">", 1)[0]
            sp = p + " svg#%d" % i
            if "viewBox" not in tag: fail(sp + " missing viewBox")
            if 'role="img"' not in tag: fail(sp + ' missing role="img"')
            if "aria-label" not in tag: fail(sp + " missing aria-label")
        low = v.lower()
        if "http://" in low or "https://" in low or "xlink:href" in low:
            fail(p + " svg references external resources")
        if len(v) > 12000:
            fail(p + " display with svg exceeds 12000 chars")
    walk(obj, path, check)

def collect_images(pd):
    out = set()
    def grab(v, p):
        if isinstance(v, str) and ("r2.dev" in v or v.startswith("http")) and p.endswith(".image"):
            out.add(v)
    walk(pd, "pd", grab)
    return out

def check_steps(steps, path, need_substitute, min_boxes=3):
    boxes, sub_at = 0, None
    for i, st in enumerate(steps):
        p = path + "[%d]" % i
        if not isinstance(st, dict):
            fail(p + " not a dict"); continue
        if st.get("answer") is not None:
            boxes += 1
            if not isinstance(st["answer"], (int, float)) or isinstance(st["answer"], bool):
                fail(p + " answer not numeric: " + repr(st["answer"]))
            if not str(st.get("hint") or "").strip(): fail(p + " box has no hint")
            if not str(st.get("pre") or "").strip(): fail(p + " box has no pre text")
        elif not str(st.get("say") or "").strip():
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
                fail(path + " completion boundary leaves %d live boxes, need >= 2" % live)
            if sub_at < 1:
                fail(path + " completion boundary at step 0: nothing pre-worked")
    return boxes

def leaks(text, sols, itype):
    """True if student-facing text states the correct answer."""
    if itype == "multiple_choice":
        return False           # solutions are option indices, meaningless as text
    t = strip_html(text)
    for s in sols:
        r = ("%g" % float(s))
        if len(r) >= 3 and re.search(r"(?<![\d.])" + re.escape(r) + r"(?![\d.])", t):
            return r
    return False

def main(fn, key=None):
    pd = json.load(io.open(fn, encoding="utf-8"))

    scan_dashes(pd, "pd")
    scan_svg(pd, "pd")

    # ---- stimulus preservation + no invented URLs -------------------------
    if key and os.path.exists(PRE):
        dump = json.load(io.open(PRE, encoding="utf-8"))
        mine = [r for r in dump if r["key"] == key]
        if mine:
            before = collect_images(mine[0]["pd"])
            after = collect_images(pd)
            known = set()
            for r in dump:
                known |= collect_images(r["pd"])
            for lost in sorted(before - after):
                fail("stimulus DROPPED: " + lost)
            for new in sorted(after - known):
                fail("stimulus INVENTED (not in pre-dump): " + new)
            nb = sum(1 for t in ("bronze", "silver", "gold")
                     for p in (mine[0]["pd"].get("problem_bank") or {}).get(t) or []
                     if p.get("chart"))
            na = sum(1 for t in ("bronze", "silver", "gold")
                     for p in (pd.get("problem_bank") or {}).get(t) or []
                     if p.get("chart"))
            if na < nb:
                fail("chart count fell from %d to %d (charts must be preserved)" % (nb, na))

    # ---- problem bank -----------------------------------------------------
    pb = pd.get("problem_bank") or {}
    for tier in ("bronze", "silver", "gold"):
        probs = pb.get(tier) or []
        if not probs:
            fail("problem_bank." + tier + " empty")
        if not str(pb.get(tier + "_description") or "").strip():
            fail("problem_bank." + tier + "_description missing (geography must ADD these)")
        seen = set()
        for i, p in enumerate(probs):
            path = tier + "[%d]" % i
            itype = p.get("input_type") or "single_value"
            if not str(p.get("display") or "").strip():
                fail(path + " no display")
            sols = p.get("solutions")
            if not isinstance(sols, list) or not sols or \
               not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in sols):
                fail(path + " solutions must be a non-empty numeric list")
                sols = []
            else:
                k = tuple(sols)
                if k in seen and itype != "multiple_choice":
                    fail(path + " duplicate solution values within tier: " + repr(sols))
                seen.add(k)
            if itype == "multiple_choice":
                opts = p.get("options") or []
                if len(opts) < 2:
                    fail(path + " multiple_choice with <2 options")
                for s in sols:
                    if not (isinstance(s, int) and 0 <= s < len(opts)):
                        fail(path + " MC solution %r is not a valid option index" % s)
            if not str(p.get("hint") or "").strip():
                fail(path + " no hint")

            # walks
            gs = p.get("guided_steps")
            if not gs and not p.get("guided_skip_reason"):
                fail(path + " missing guided_steps (MC needs them too unless guided_skip_reason)")
            if gs:
                check_steps(gs, path + ".guided_steps", need_substitute=True)
                first_box = next((s for s in gs if s.get("answer") is not None), None)
                if first_box is None:
                    fail(path + ".guided_steps has no box at all")

            # misconceptions
            for j, m in enumerate(p.get("misconceptions") or []):
                mp = path + ".misconceptions[%d]" % j
                if m.get("check") == "wrong":
                    fail(mp + " still uses catch-all check:'wrong' (must be expect-matched)")
                msg = str(m.get("message") or "")
                if not msg.strip():
                    fail(mp + " no message")
                if "expect" not in m:
                    fail(mp + " missing expect key (null allowed, absent not)")
                lk = leaks(msg, sols, itype)
                if lk:
                    fail(mp + " message states the correct answer (" + lk + ")")
                e = m.get("expect")
                if e is not None and sols:
                    ev = e if isinstance(e, list) else [e]
                    if len(ev) == len(sols) and all(isinstance(x, (int, float)) for x in ev):
                        if all(abs(float(a) - float(b)) < 1e-9 for a, b in zip(ev, sols)):
                            fail(mp + " expect equals the correct answer")
            lk = leaks(str(p.get("hint") or ""), sols, itype)
            if lk:
                fail(path + ".hint states the correct answer (" + lk + ")")

    # ---- tier guides ------------------------------------------------------
    tg = pd.get("tier_guides") or {}
    for tier in ("bronze", "silver", "gold"):
        g = tg.get(tier) or {}
        path = "tier_guides." + tier
        if not str(g.get("title") or "").strip():
            fail(path + ".title missing")
        steps = g.get("steps") or []
        if not (2 <= len(steps) <= 4):
            fail(path + ".steps must have 2-4 entries")
        if sum(words(s) for s in steps) > 115:
            fail(path + ".steps total %d words, budget 115" % sum(words(s) for s in steps))
        ex = g.get("example") or {}
        if not str(ex.get("question") or "").strip() or not ex.get("steps"):
            fail(path + ".example missing question/steps")

    # ---- guided ------------------------------------------------------------
    gd = pd.get("guided") or {}
    op = gd.get("opener") or {}
    if not op.get("steps"):
        fail("guided.opener missing/empty")
    else:
        if not any(st.get("answer") is not None for st in op["steps"]):
            fail("guided.opener has no interactive box")
        check_steps(op["steps"], "guided.opener.steps", need_substitute=False, min_boxes=1)
        if len([s for s in op["steps"] if s.get("answer") is not None]) > 3:
            fail("guided.opener has more than 3 boxes (keep it 2-3)")
    for tier in ("bronze", "silver", "gold"):
        t = (gd.get("teach") or {}).get(tier) or {}
        if not t.get("steps") or not str(t.get("display") or "").strip():
            fail("guided.teach." + tier + " missing display/steps")
        elif sum(1 for st in t["steps"] if st.get("answer") is not None) < 4:
            fail("guided.teach." + tier + " needs >= 4 boxes")

    # ---- method card -------------------------------------------------------
    mc = pd.get("method_card") or {}
    if not str(mc.get("title") or "").strip():
        fail("method_card.title missing")
    if words(strip_html(mc.get("content") or "")) > 140:
        fail("method_card.content %d words, budget 140" % words(strip_html(mc.get("content") or "")))
    if len(mc.get("steps") or []) > 4:
        fail("method_card.steps: max 4")

    # ---- board neutrality --------------------------------------------------
    BOARDS = re.compile(r"\b(AQA|Edexcel|Eduqas|WJEC|OCR|Pearson)\b")
    def bn(v, p):
        if isinstance(v, str) and not any(p.endswith("." + k) for k in EXEMPT_KEYS):
            m = BOARDS.search(v)
            if m:
                fail("names an exam board at " + p + ": " + m.group(0))
    walk(pd, "pd", bn)

    if fails:
        print("FAIL (%d):" % len(fails))
        for f in fails[:80]:
            print("  -", f)
        sys.exit(1)
    print("PASS: structure, style, budgets, stimulus, leakage all clean")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
