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

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

STATE = os.path.join(HERE, "_canary_state.json")
LEDGER = os.path.join(HERE, "_canary_ledger.json")
BUILDS = os.path.join(HERE, "builds")
CONTRACT = io.open(os.path.join(HERE, "CONTRACT.md"), encoding="utf-8").read()

HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-5"
OPUS = "claude-opus-5"

# USD per million tokens (list price assumptions — reconcile with console)
PRICES = {
    HAIKU: (1.00, 5.00),
    SONNET: (3.00, 15.00),
    OPUS: (15.00, 75.00),
}

UNITS = [("science-aqa", "physics-paper-1"), ("history-aqa", "elizabethan-england")]

cl = anthropic.Anthropic()


# ------------------------------------------------------------------ ledger
def ledger_load():
    if os.path.exists(LEDGER):
        return json.load(io.open(LEDGER, encoding="utf-8"))
    return {"calls": []}


def ledger_add(tier, model, label, usage):
    led = ledger_load()
    led["calls"].append({
        "tier": tier, "model": model, "label": label,
        "in": usage.input_tokens, "out": usage.output_tokens,
    })
    io.open(LEDGER, "w", encoding="utf-8").write(json.dumps(led, indent=1))


def cost_report():
    led = ledger_load()
    by = {}
    for c in led["calls"]:
        k = (c["tier"], c["model"])
        agg = by.setdefault(k, {"in": 0, "out": 0, "n": 0})
        agg["in"] += c["in"]; agg["out"] += c["out"]; agg["n"] += 1
    total = 0.0
    print("\n%-6s %-28s %5s %10s %10s %9s" % ("tier", "model", "calls", "in", "out", "USD"))
    for (tier, model), a in sorted(by.items()):
        pin, pout = PRICES.get(model, (0, 0))
        usd = a["in"] / 1e6 * pin + a["out"] / 1e6 * pout
        total += usd
        print("%-6s %-28s %5d %10d %10d %9.3f" % (tier, model, a["n"], a["in"], a["out"], usd))
    print("%-6s %-28s %5s %10s %10s %9.3f" % ("", "TOTAL", "", "", "", total))
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
TRIAGE_SYS = """You decide whether a GCSE revision lesson would genuinely teach better with a small interactive, and if so what KIND of interaction fits.

The bar is high. Say yes ONLY if a student doing something with their hands would teach a specific idea in this lesson better than the prose already does. Say no for lessons that are pure narrative, pure recall, or where an interactive would just be decoration.

Variety matters enormously: the site must not feel like the same slider over and over. Pick the interaction verb that genuinely suits THIS lesson's idea, from (or beyond) this palette:
  adjust-to-see-relationship, adjust-to-hit-a-target, order-the-sequence,
  match-pairs, sort-into-groups, spot-the-deliberate-error,
  predict-then-reveal, step-through-a-process, build-to-a-spec,
  choose-a-path-and-see-consequences, compare-two-cases-side-by-side,
  annotate-the-picture, balance-two-competing-quantities

Reply with ONLY JSON:
{"worth_it": true|false,
 "confidence": 0-1,
 "verb": "<one from the palette, or your own if better>",
 "idea": "<the ONE idea the interactive would teach, in a sentence>",
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
SPEC_SYS = """You design ONE small interactive for a GCSE lesson, and you write the tests it must pass BEFORE anyone writes the code. You are the specification, not the implementation.

You will be given the lesson text and the chosen interaction verb.

Design something a 15-year-old would actually enjoy touching, that teaches the stated idea. It must be genuinely specific to THIS lesson — its numbers, its examples, its vocabulary. Avoid generic sliders; make the interaction match the verb.

The invariants are the important part. They must be checkable by running the widget's pure model function with different inputs and asserting on the outputs. Write them as precise, mechanical statements about params and derived values. They must come from the LESSON's physics/history/logic, not from any implementation.

Good invariants:
  "for any params, derived.current equals derived.power / params.voltage within 1e-9"
  "increasing params.impermeable never increases derived.lagTime"
  "derived.tripped is true exactly when derived.current > 13"
  "steps are non-empty and every step's caption is a non-empty string"
  "the final step's state.sorted array is in ascending order"

Reply with ONLY JSON:
{"id": "<kebab-slug>",
 "title": "<student-facing title, max 8 words>",
 "kind": "explore" | "steps",
 "teaches": "<the one idea>",
 "interaction": "<2-3 sentences: what the student does and sees>",
 "controls": [{"key","label","min","max","step","value","unit"}]  // [] for steps
 "derived_fields": [{"key","meaning"}],
 "visual": "<what is drawn on the canvas, concretely>",
 "invariants": ["<mechanical, checkable statement>", ...],
 "facts_used": ["<each factual claim/number taken from the lesson>"]}"""


def tier2():
    s = state_load()
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
                  (i, len(todo), les["spec"]["title"][:46], les["spec"]["kind"],
                   len(les["spec"].get("invariants", []))))
        except Exception as e:
            les["spec_error"] = str(e)[:120]
            print("  %2d/%d FAILED %s" % (i, len(todo), str(e)[:70]))
        state_save(s)
    cost_report()


# ------------------------------------------------------------------ tier 3
BUILD_SYS = """You write ONE small interactive teaching widget as a single JavaScript file, exactly to the contract below. You are given a design spec and the lesson it belongs to.

%s

Additional requirements:
- Follow the spec's id, kind, controls and derived field names EXACTLY: the widget will be tested against invariants written from that spec before you existed.
- The drawing must be genuinely illustrative of THIS lesson, not a generic chart. Use the canvas properly: label things, show the quantity that matters, make the change visible.
- The site is warm and calm: ink #2d2a26, muted #8d8880, grid #e8e2d9, and the lesson's own accent passed in as `acc`. No gradients, no shadows, no emoji.
- British English.
- Output ONLY the JavaScript file. No markdown fence, no commentary.""" % CONTRACT


def tier3(max_n=None):
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
            code = call(3, OPUS, spec["id"], BUILD_SYS, user, 24000)
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
TESTGEN_SYS = """You write a Node.js test script that checks a widget's PURE model against a list of invariants. You are given the widget's SPEC and the invariants — you are NOT given the widget's code, and you must not assume anything about its internals beyond the contract.

Contract reminder: the module exports an object W with either
  - W.controls (array of {key,min,max,step,value}) and W.derive(params) -> object
  - or W.steps(params) -> array of {caption, state}
plus W.meta, W.render, W.caption.

Write a script that:
1. requires the widget from process.argv[2]
2. builds a parameter sweep from W.controls (min, max, default, and 3 points between; for toggles both booleans) — cap the sweep at 200 combinations by sampling if needed
3. asserts the contract basics: derive/steps never throws, never returns NaN/Infinity/undefined fields, captions are non-empty strings
4. asserts EACH invariant, printing PASS/FAIL with the invariant text
5. exits 0 if all pass, 1 otherwise, and prints a final line "RESULT ok=<n> fail=<n>"

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
                                    if k in ("id", "kind", "controls", "derived_fields")}, indent=1),
                        json.dumps(spec.get("invariants", []), indent=1)))
            try:
                tcode = call(4, SONNET, "test:" + spec["id"], TESTGEN_SYS, tuser, 12000)
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
                                            FACTCHECK_SYS, fuser, 12000))
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
        {"1": tier1, "2": tier2, "3": lambda: tier3(mx), "4": tier4}[t]()
    else:
        print(__doc__)
