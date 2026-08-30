# -*- coding: utf-8 -*-
"""Bespoke-widget pipeline — CANARY run (Tom's brief, 19 Aug).

Four tiers, cheapest model first, each one only touching what survived
the last:

  1. TRIAGE   (Haiku)  — is there a worthwhile interactive in this
                         lesson, and which interaction VERB suits it?
                         Variety is the point: order-these, spot-the-
                         error, adjust-to-target, predict-then-reveal...
  2. SPEC     (Sonnet) — design it, and write the INVARIANTS that must
                         hold. Written from the LESSON, before any code
                         exists — so the builder cannot mark its own
                         homework.
  3. BUILD    (Opus)   — write the widget to scripts/widget_pipeline/
                         CONTRACT.md: pure derive()/steps() + render().
  4. GATE              — (a) syntax + purity static checks
                         (b) property tests EXECUTED in node against the
                             tier-2 invariants (no browser needed: the
                             model layer is pure by contract)
                         (c) adversarial fact-check (Sonnet, different
                             prompt, sees lesson + widget, hunts errors)

Every API call's real token usage is recorded, so the run reports actual
cost rather than an estimate. Prices below are list prices in USD per
million tokens and are ASSUMPTIONS — the console is the authority.

    python scripts/widget_pipeline/canary.py --tier 1
    python scripts/widget_pipeline/canary.py --tier 2
    python scripts/widget_pipeline/canary.py --tier 3 [--max 4]
    python scripts/widget_pipeline/canary.py --tier 4
    python scripts/widget_pipeline/canary.py --report
"""
import io
import json
import os
import re
import subprocess
import sys
import time

import threading

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

STATE = os.path.join(HERE, "_canary_state.json")
LEDGER = os.path.join(HERE, "_canary_ledger.json")
BUILDS = os.path.join(HERE, "builds")
CONTRACT = io.open(os.path.join(HERE, "CONTRACT.md"), encoding="utf-8").read()
GUIDE = io.open(os.path.join(HERE, "BUILD_GUIDE.md"), encoding="utf-8").read()

HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-5"
OPUS = "claude-opus-5"

# USD per million tokens. CALIBRATION: the first canary computed $7.81
# from this table while Tom's real balance moved $3.47 — a factor of
# 0.44. The console is the authority; these are list-price assumptions.
CALIBRATION = 0.44
PRICES = {
    HAIKU: (1.00, 5.00),
    SONNET: (3.00, 15.00),
    OPUS: (15.00, 75.00),
}

UNITS = [("science-aqa", "physics-paper-1"), ("history-aqa", "elizabethan-england")]

cl = anthropic.Anthropic()


# ------------------------------------------------------------------ ledger
# The corpus audit calls this from 8 threads. Without a lock the
# read-modify-write races and two writers interleave, leaving two JSON
# documents in one file - which is exactly what killed the overnight run
# at lesson 519 of 3,571.
_ledger_lock = threading.Lock()


def ledger_load():
    if os.path.exists(LEDGER):
        return json.load(io.open(LEDGER, encoding="utf-8"))
    return {"calls": []}


def ledger_add(tier, model, label, usage):
    with _ledger_lock:
        led = ledger_load()
        led["calls"].append({
            "tier": tier, "model": model, "label": label,
            "in": usage.input_tokens, "out": usage.output_tokens,
        })
        tmp = LEDGER + ".tmp"
        io.open(tmp, "w", encoding="utf-8").write(json.dumps(led, indent=1))
        os.replace(tmp, LEDGER)          # atomic: never a half-written file


def cost_report():
    led = ledger_load()
    by = {}
    for c in led["calls"]:
        k = (c["tier"], c["model"])
        agg = by.setdefault(k, {"in": 0, "out": 0, "n": 0})
        agg["in"] += c["in"]; agg["out"] += c["out"]; agg["n"] += 1
    total = 0.0
    print("\n%-6s %-28s %5s %10s %10s %9s" % ("tier", "model", "calls", "in", "out", "USD"))
    for (tier, model), a in sorted(by.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        pin, pout = PRICES.get(model, (0, 0))
        usd = (a["in"] / 1e6 * pin + a["out"] / 1e6 * pout) * CALIBRATION
        total += usd
        print("%-6s %-28s %5d %10d %10d %9.3f" % (tier, model, a["n"], a["in"], a["out"], usd))
    print("%-6s %-28s %5s %10s %10s %9.3f" % ("", "TOTAL", "", "", "", total))
    return total


def cost_so_far():
    """Running calibrated spend, so a long unattended run can stop itself
    before it eats the whole balance."""
    led = ledger_load()
    total = 0.0
    for c in led["calls"]:
        pin, pout = PRICES.get(c["model"], (0, 0))
        total += (c["in"] / 1e6 * pin + c["out"] / 1e6 * pout) * CALIBRATION
    return total


def call(tier, model, label, system, user, max_tokens, temperature=None):
    kw = dict(model=model, max_tokens=max_tokens, system=system,
              messages=[{"role": "user", "content": user}])
    if temperature is not None:
        kw["temperature"] = temperature
    # big generations must stream: the API refuses non-streaming requests
    # that could exceed 10 minutes, which every Opus build does.
    stream = max_tokens > 8000
    for attempt in range(3):
        try:
            if stream:
                text = []
                with cl.messages.stream(**kw) as st:
                    for chunk in st.text_stream:
                        text.append(chunk)
                    r = st.get_final_message()
                out = "".join(text).strip()
            else:
                r = cl.messages.create(**kw)
                out = "".join(getattr(b, "text", "") or "" for b in r.content).strip()
            break
        except Exception as e:
            if attempt == 2:
                raise
            print("   retry (%s)" % str(e)[:60]); time.sleep(4)
    ledger_add(tier, model, label, r.usage)
    if r.stop_reason == "max_tokens" and not out:
        raise ValueError("thinking consumed the whole budget (%d tokens), no text"
                         % r.usage.output_tokens)
    return out


def jparse(raw):
    raw = re.sub(r"```(?:json)?", "", raw)
    m = re.search(r"[{\[][\s\S]*[}\]]", raw)
    if not m:
        raise ValueError("no JSON in response")
    return json.loads(m.group(0))


def state_load():
    if os.path.exists(STATE):
        return json.load(io.open(STATE, encoding="utf-8"))
    return {"lessons": []}


def state_save(s):
    io.open(STATE, "w", encoding="utf-8").write(json.dumps(s, indent=1))


def strip(html):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html or "")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------------ tier 1
TRIAGE_SYS = """You decide whether a GCSE lesson contains an idea that is genuinely HARD OR ABSTRACT IN PROSE, and would become clear if the student could see and touch it.

The test, and the only test:

  CAN A STUDENT READ THIS PASSAGE CORRECTLY AND STILL PICTURE THE IDEA WRONGLY?

Say YES for:
- invisible mechanisms (electron flow, osmosis, what actually moves in a sound wave, how a synapse fires)
- counterintuitive relationships (frequency up means wavelength down; a steeper basin gives a SHORTER lag time)
- interacting variables the student cannot hold in their head at once
- things prose has to flatten (a cross-section, a castle approach, plate movement, anything spatial or simultaneous)
- a specific, nameable misconception the lesson is trying to prevent

Say NO for:
- narrative, chronology and cause-lists that text already handles well
- definitions, terminology, quotation analysis
- anything already concrete in the prose
- anything where the interactive would only restate what the text says

BE HARSH. Roughly one lesson in three should qualify; a widget in every lesson becomes furniture and gets scrolled past. A weak interactive is worse than none, because it teaches the student these are skippable. If you are unsure, say no.

Reply with ONLY JSON:
{"worth_it": true|false,
 "confidence": 0-1,
 "misconception": "<the specific wrong mental picture a student is likely to hold, in one sentence>",
 "idea": "<the ONE idea the interactive must make concrete>",
 "why_visual": "<why seeing/touching beats reading, in one sentence>",
 "verb": "<what the student physically does: adjust, sort, order, match, route, annotate, build, choose...>",
 "why_not": "<only if worth_it is false>"}"""


def tier1():
    sb = get_client()
    s = state_load()
    if s["lessons"]:
        print("state already has %d lessons; reusing" % len(s["lessons"]))
    else:
        for slug, uslug in UNITS:
            subj = sb.from_("subjects").select("id,name,exam_board").eq("slug", slug) \
                .is_("school_id", "null").execute().data[0]
            unit = sb.from_("units").select("id,slug,name").eq("subject_id", subj["id"]) \
                .eq("slug", uslug).execute().data[0]
            rows = sb.from_("lessons").select("id,lesson_number,title,content_html") \
                .eq("unit_id", unit["id"]).eq("status", "live").order("lesson_number").execute().data
            for r in rows:
                s["lessons"].append({
                    "lesson_id": r["id"], "subject": slug, "subject_name": subj["name"],
                    "unit": uslug, "unit_name": unit["name"], "n": r["lesson_number"],
                    "title": r["title"], "text": strip(r["content_html"])[:9000],
                })
        state_save(s)
    todo = [l for l in s["lessons"] if "triage" not in l]
    print("tier 1 triage over %d lessons" % len(todo))
    for i, les in enumerate(todo, 1):
        user = ("SUBJECT: %s\nUNIT: %s\nLESSON %d: %s\n\n%s"
                % (les["subject_name"], les["unit_name"], les["n"], les["title"], les["text"]))
        try:
            v = jparse(call(1, HAIKU, les["title"][:40], TRIAGE_SYS, user, 400))
        except Exception as e:
            v = {"worth_it": False, "why_not": "triage failed: %s" % str(e)[:60]}
        les["triage"] = v
        print("  %2d/%d %-52s %s %s" % (i, len(todo), les["title"][:52],
              "YES" if v.get("worth_it") else "no ", v.get("verb", "")))
        state_save(s)
    yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
    print("\n%d/%d lessons want an interactive" % (yes.__len__(), len(s["lessons"])))
    cost_report()


# ------------------------------------------------------------------ tier 2
SPEC_SYS = """You design ONE interactive for a GCSE lesson, and you write the tests it must pass BEFORE the code exists. You are the specification, not the implementation.

DESIGN FOR COMMIT-THEN-CHECK. If the interaction has a right answer anywhere in it, the student must assemble a whole response and press a Check button before ANY verdict appears - never live feedback they can fiddle towards. Only genuinely exploratory widgets (getting a feel for a wave) give continuous feedback.

DESIGN FOR A 360px PHONE FIRST.

INVENT THE INTERACTION. There is no menu and no house style to conform to. Design what would genuinely teach this lesson's idea to a 15-year-old bored of reading: dragging cards into groups, ordering events on a line, matching pairs, clicking hotspots on a drawing, routing a path and living with the consequences, balancing two competing quantities, spotting a planted error, weighing evidence. If sliders are honestly the best fit use sliders, but do not default to them, and never invent a control that changes nothing meaningful.

The widget will be written to a contract that constrains only the code's SHAPE, never your design: pure initialState/apply(state,action)/derive/regions, plus a render. Any interaction at all fits that shape.

Your invariants are the important part. They must be checkable by calling those pure functions with different states and actions. Derive them from the LESSON's logic, not from any implementation.

Good invariants:
  "derive(s).correctCount equals the number of i where s.assignment[i] === i"
  "applying {t:'drop',card:c,bin:b} never makes derive(s).placed exceed the number of cards"
  "for any reachable state, derive(s).current equals derive(s).power / s.voltage within 1e-9"
  "regions(s,600,300) returns at least one region for every unplaced card"
  "apply(s,a) does not mutate s"

Reply with ONLY JSON:
{"id": "<kebab-slug>",
 "title": "<student-facing, max 8 words>",
 "teaches": "<the one idea>",
 "interaction": "<3-5 sentences: exactly what the student does, sees, and can get wrong>",
 "state_shape": {"<field>": "<meaning>"},
 "actions": [{"t": "<name>", "fields": "<...>", "meaning": "<...>"}],
 "controls": [],
 "derived_fields": [{"key": "", "meaning": ""}],
 "visual": "<what is drawn, concretely - this is a picture, describe it>",
 "commit": "<the Check button label and exactly what is revealed only after it is pressed; 'n/a - exploratory' if there is no right answer>",
 "invariants": ["<mechanical, checkable>"],
 "facts_used": ["<each fact/number taken from the lesson>"]}"""


def tier2():
    s = state_load()
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    if only:
        for l in s["lessons"]:
            if only.lower() in (l.get("triage", {}).get("verb", "") or "").lower():
                l.pop("spec", None); l.pop("build", None); l.pop("gate", None)
        state_save(s)
    todo = [l for l in s["lessons"]
            if l.get("triage", {}).get("worth_it") and "spec" not in l]
    for l in todo:
        l.pop("spec_error", None)
    print("tier 2 spec over %d lessons" % len(todo))
    for i, les in enumerate(todo, 1):
        user = ("LESSON %d: %s (%s)\nINTERACTION VERB: %s\nIDEA TO TEACH: %s\n\n"
                "LESSON TEXT:\n%s"
                % (les["n"], les["title"], les["subject_name"],
                   les["triage"].get("verb"), les["triage"].get("idea"), les["text"]))
        try:
            # 8000 not 2500: Sonnet's thinking blocks can eat the WHOLE
            # budget and return empty text (stop_reason max_tokens, zero
            # chars) — 13 of 23 specs died that way on the first canary.
            les["spec"] = jparse(call(2, SONNET, les["title"][:40], SPEC_SYS, user, 8000))
            print("  %2d/%d %-46s %s (%d invariants)" %
                  (i, len(todo), les["spec"]["title"][:46],
                   (les["spec"].get("actions") and
                    ",".join(a.get("t", "?") for a in les["spec"]["actions"])[:22]) or "controls",
                   len(les["spec"].get("invariants", []))))
        except Exception as e:
            les["spec_error"] = str(e)[:120]
            print("  %2d/%d FAILED %s" % (i, len(todo), str(e)[:70]))
        state_save(s)
    cost_report()


# ------------------------------------------------------------------ tier 3
BUILD_SYS = """You write ONE interactive teaching widget for a GCSE lesson as a single self-contained file. You are given a design spec and the lesson.

%s

Build the best possible version of the spec's interaction. Use whatever the browser offers — real buttons for choices, CSS grid so text lays itself out, SVG for diagrams, canvas for graphs and simulations. Do NOT paint paragraphs of text into a canvas; that is what HTML is for. Do NOT represent a discrete choice as a numeric slider.

It should feel like a small, well-made thing a teacher would be pleased to show a class: clear at a glance what to do, obvious feedback when the student is right or wrong, and worth touching more than once.

Output ONLY the JavaScript file contents (it will be loaded as a script and must set window.SVWidget). No markdown fence, no commentary.""" % (CONTRACT + chr(10)*2 + GUIDE)


def tier3(max_n=None, build_model=OPUS):
    s = state_load()
    if not os.path.isdir(BUILDS):
        os.makedirs(BUILDS)
    todo = [l for l in s["lessons"] if l.get("spec") and "build" not in l]
    if max_n:
        # interleave the units so a sample spans both subjects and several
        # interaction verbs, not just the first unit's sliders
        buckets = {}
        for l in todo:
            buckets.setdefault(l["subject"], []).append(l)
        mixed, keys = [], list(buckets)
        while any(buckets[k] for k in keys):
            for k in keys:
                if buckets[k]:
                    mixed.append(buckets[k].pop(0))
        todo = mixed[:max_n]
    print("tier 3 build over %d widgets" % len(todo))
    for i, les in enumerate(todo, 1):
        spec = les["spec"]
        user = ("SPEC:\n%s\n\nLESSON %d: %s\n\nLESSON TEXT:\n%s"
                % (json.dumps(spec, indent=1), les["n"], les["title"], les["text"][:6000]))
        try:
            # 24000, not 8000: at 8k EVERY build hit the cap and returned
            # truncated code (3 of 6 empty, the other 3 cut mid-statement,
            # $4 wasted). Opus needs room to think AND emit a whole file.
            code = call(3, build_model, spec["id"], BUILD_SYS, user, 24000)
            code = re.sub(r"^```(?:javascript|js)?|```$", "", code.strip(), flags=re.M).strip()
            path = os.path.join(BUILDS, spec["id"] + ".js")
            io.open(path, "w", encoding="utf-8").write(code)
            chk = subprocess.run(["node", "--check", path], capture_output=True, text=True)
            if chk.returncode != 0:
                les["build_error"] = "truncated/invalid: " + (chk.stderr or "")[:120]
                print("  %2d/%d %-40s INVALID (kept for inspection)" % (i, len(todo), spec["id"][:40]))
                state_save(s)
                continue
            les["build"] = {"file": os.path.basename(path), "bytes": len(code)}
            print("  %2d/%d %-40s %5d bytes" % (i, len(todo), spec["id"][:40], len(code)))
        except Exception as e:
            les["build_error"] = str(e)[:150]
            print("  %2d/%d FAILED %s" % (i, len(todo), str(e)[:80]))
        state_save(s)
    cost_report()


# ------------------------------------------------------------------ tier 4
TESTGEN_SYS = """You write a Node.js test script that checks a widget's PURE model against a list of invariants. You are given the widget's SPEC and its invariants. You are NOT given the widget's code and must not assume anything beyond the contract.

Contract — the module exports W with EXACT signatures:
  W.meta            : {id, title, teaches}
  W.initialState()  -> state              (pure)
  W.apply(state, action) -> newState      (pure, must not mutate state)
  W.derive(state)   -> object             (pure)
  W.regions(state, w, h) -> [{x,y,w,h,action}]   (pure; may be [])
  W.controls        : array (may be absent/empty); control changes arrive
                      as the action {t:'set', key:<key>, v:<value>}
  W.render(ctx, state, derived, w, h, acc)   -- DO NOT CALL, needs a canvas
  W.caption(state, derived) -> string      (TWO arguments - always pass both)

Write a script that:
1. requires the widget from process.argv[2]
2. explores the state space: from initialState(), repeatedly take the actions
   offered by regions(s,600,300) (and {t:'set'} actions across each control's
   min/mid/max), breadth-first, visiting up to 300 distinct states
3. asserts the contract basics on every visited state: apply/derive/regions
   never throw, derive returns no NaN/Infinity/undefined field, caption(s,
   derive(s)) is a non-empty string, and apply(s,a) leaves s unchanged
   (deep-compare a JSON snapshot taken before the call)
4. asserts EACH invariant, printing "PASS: <text>" or "FAIL: <text> [detail]"
5. distinguishes a BROKEN TEST from a broken widget: if your own harness
   throws (bad signature, missing field you assumed), print
   "HARNESS-ERROR: <what>" and do not count it as a widget failure
6. exits 0 only if there are zero FAILs, and prints a final line
   "RESULT ok=<n> fail=<n> harness=<n>"

Use only Node built-ins. Output ONLY the JavaScript. No fence, no commentary."""

FACTCHECK_SYS = """You are an adversarial checker for a GCSE teaching widget. You see the LESSON and the WIDGET CODE. Your job is to find what is WRONG — assume something is.

Check, in order of seriousness:
1. Does the model compute the science/maths/logic correctly? Work through the arithmetic yourself.
2. Does any number, date, name or unit contradict the lesson, or GCSE fact?
3. Would the widget teach a MISCONCEPTION — e.g. implying a relationship that does not hold, or letting the student practise something wrong?
4. Does the caption text claim more than the lesson supports?
5. Is the interaction pointless — a control that changes nothing meaningful?

Be specific and quote the offending line. Do not report style or aesthetics.

Reply with ONLY JSON:
{"verdict": "pass" | "fix" | "reject",
 "findings": [{"severity":"high|medium|low","what":"...","where":"<line or function>","fix":"..."}]}"""


def tier4():
    s = state_load()
    todo = [l for l in s["lessons"] if l.get("build") and "gate" not in l]
    print("tier 4 gate over %d widgets" % len(todo))
    for i, les in enumerate(todo, 1):
        spec, path = les["spec"], os.path.join(BUILDS, les["build"]["file"])
        code = io.open(path, encoding="utf-8").read()
        gate = {}

        # (a) static: syntax + purity
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        gate["syntax"] = "ok" if r.returncode == 0 else (r.stderr or "")[:200]
        impure = [w for w in ("Math.random", "new Date", "Date.now", "document.",
                              "window.", "fetch(") if w in code.split("render")[0]]
        gate["purity"] = "ok" if not impure else "impure model: " + ",".join(impure)

        # (b) property tests, written from the SPEC (not the code) then executed
        if gate["syntax"] == "ok":
            tuser = ("SPEC:\n%s\n\nINVARIANTS:\n%s"
                     % (json.dumps({k: spec[k] for k in spec
                                    if k in ("id", "controls", "state_shape", "actions",
                                             "derived_fields")}, indent=1),
                        json.dumps(spec.get("invariants", []), indent=1)))
            try:
                tcode = call(4, SONNET, "test:" + spec["id"], TESTGEN_SYS, tuser, 24000)
                tcode = re.sub(r"^```(?:javascript|js)?|```$", "", tcode.strip(), flags=re.M).strip()
                tpath = os.path.join(BUILDS, spec["id"] + ".test.js")
                io.open(tpath, "w", encoding="utf-8").write(tcode)
                tr = subprocess.run(["node", tpath, path], capture_output=True,
                                    text=True, timeout=60)
                out = (tr.stdout or "") + (tr.stderr or "")
                gate["tests_exit"] = tr.returncode
                gate["tests_tail"] = out.strip().splitlines()[-6:] if out.strip() else []
            except Exception as e:
                gate["tests_exit"] = -1
                gate["tests_tail"] = [str(e)[:150]]

        # (c) adversarial fact-check
        try:
            fuser = ("LESSON %d: %s\n\nLESSON TEXT:\n%s\n\nWIDGET CODE:\n%s"
                     % (les["n"], les["title"], les["text"][:6000], code[:12000]))
            gate["factcheck"] = jparse(call(4, SONNET, "fc:" + spec["id"],
                                            FACTCHECK_SYS, fuser, 16000))
        except Exception as e:
            gate["factcheck"] = {"verdict": "error", "findings": [{"what": str(e)[:120]}]}

        les["gate"] = gate
        fc = gate.get("factcheck", {})
        highs = [f for f in fc.get("findings", []) if f.get("severity") == "high"]
        print("  %2d/%d %-34s syntax:%s tests:%s fc:%s%s"
              % (i, len(todo), spec["id"][:34],
                 "ok" if gate["syntax"] == "ok" else "FAIL",
                 gate.get("tests_exit"), fc.get("verdict"),
                 (" %d HIGH" % len(highs)) if highs else ""))
        state_save(s)
    cost_report()


def report():
    s = state_load()
    tot = len(s["lessons"])
    yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
    built = [l for l in s["lessons"] if l.get("build")]
    gated = [l for l in s["lessons"] if l.get("gate")]
    clean = [l for l in gated
             if l["gate"].get("syntax") == "ok" and l["gate"].get("tests_exit") == 0
             and l["gate"].get("factcheck", {}).get("verdict") == "pass"]
    print("lessons scanned      %d" % tot)
    print("worth an interactive %d (%.0f%%)" % (len(yes), 100.0 * len(yes) / max(1, tot)))
    print("widgets built        %d" % len(built))
    print("through the gate     %d clean of %d" % (len(clean), len(gated)))
    verbs = {}
    for l in yes:
        verbs[l["triage"].get("verb", "?")] = verbs.get(l["triage"].get("verb", "?"), 0) + 1
    print("interaction verbs    " + ", ".join("%s x%d" % (k, v) for k, v in
                                              sorted(verbs.items(), key=lambda kv: -kv[1])))
    total = cost_report()
    if built:
        print("\ncost per built widget: $%.3f" % (total / len(built)))
        print("extrapolated to 4,063 lessons at this hit rate: $%.0f"
              % (total / max(1, tot) * 4063))


if __name__ == "__main__":
    a = sys.argv
    if "--report" in a:
        report()
    elif "--tier" in a:
        t = a[a.index("--tier") + 1]
        mx = int(a[a.index("--max") + 1]) if "--max" in a else None
        {"1": tier1, "2": tier2, "3": lambda: tier3(mx, SONNET if "--sonnet" in a else OPUS), "4": tier4}[t]()
    else:
        print(__doc__)
