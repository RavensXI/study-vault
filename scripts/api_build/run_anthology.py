# -*- coding: utf-8 -*-
"""Orchestrator: Eduqas EngLit poetry-anthology unit rebuild, end to end.

Chains the driver stages with polling, runs the deterministic quote gate
before and after fixes, folds gate misses into the fact-check findings, and
only inserts to Supabase if the final gate is clean. Logs to the run dir.

Run from repo root:  python scripts/api_build/run_anthology.py
"""
import io
import json
import os
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_PATH = os.path.join(HERE, "config_englit-eduqas-anthology.json")
CFG = json.load(io.open(CFG_PATH, encoding="utf-8"))
RUN = CFG["run_dir"]
LOG = io.open(os.path.join(RUN, "orchestrator.log"), "a", encoding="utf-8")


def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def stage(name):
    log("stage: " + name)
    p = subprocess.run([sys.executable, os.path.join(HERE, "driver.py"),
                        "--config", CFG_PATH, name],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    LOG.write(out + "\n")
    LOG.flush()
    if p.returncode != 0:
        log("STAGE FAILED: %s (rc=%d) — tail: %s" % (name, p.returncode, out[-400:]))
        raise SystemExit(1)
    return out


def state():
    return json.load(io.open(os.path.join(RUN, "state.json"), encoding="utf-8"))


def poll_until(stage_name, done, max_minutes=240):
    for _ in range(max_minutes // 5):
        stage(stage_name)
        if done(state()):
            return
        time.sleep(300)
    log("TIMEOUT waiting on " + stage_name)
    raise SystemExit(1)


def quote_gate(tag):
    out = os.path.join(RUN, "quote_gate_%s.json" % tag)
    p = subprocess.run([sys.executable, os.path.join(HERE, "quote_gate.py"),
                        CFG["factcheck_context_doc"], os.path.join(RUN, "lessons"), out],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    LOG.write((p.stdout or "") + "\n")
    LOG.flush()
    log("quote gate (%s): rc=%d" % (tag, p.returncode))
    return json.load(io.open(out, encoding="utf-8"))


def main():
    log("=== anthology build start ===")
    stage("prep")
    stage("submit")
    poll_until("poll", lambda st: "content_ok" in st)

    for round_ in (1, 2):
        st = state()
        if not st.get("content_failures") and not st.get("content_errors"):
            break
        log("fix round %d: %d failures" % (round_, len(st.get("content_failures", {}))))
        stage("fix")
        poll_until("pollfix", lambda st: st.get("fix_batch_id") in st.get("collected_batches", []))
    st = state()
    log("content complete: %d ok, %d failing" % (len(st.get("content_ok", [])),
                                                 len(st.get("content_failures", {}))))

    gate1 = quote_gate("pre")

    stage("factcheck")
    poll_until("pollfactcheck",
               lambda st: os.path.exists(os.path.join(RUN, "factcheck.json")))

    # fold quote-gate misses into the findings as HIGH corrections
    fc_path = os.path.join(RUN, "factcheck.json")
    fc = json.load(io.open(fc_path, encoding="utf-8"))
    added = 0
    for lesson, spans in gate1.get("lessons_with_misses", {}).items():
        for s in spans:
            fc["findings"].append({
                "severity": "high", "field": "content_html", "lesson": lesson,
                "claim": s,
                "problem": "Quoted span not found verbatim in the anthology poem texts.",
                "correction": ("If this is presented as a quotation from a poem, replace it "
                               "with an exact phrase from the supplied poem text. If it is "
                               "not a poem quotation (a technical term or exam phrase), "
                               "remove the quotation marks or reword. Never leave an "
                               "invented poem line in place."),
            })
            added += 1
    if added:
        io.open(fc_path, "w", encoding="utf-8").write(json.dumps(fc, ensure_ascii=False, indent=1))
        log("folded %d quote-gate misses into factcheck findings" % added)

    if any(f.get("severity") in ("high", "medium") for f in fc["findings"]):
        stage("applyfixes")
        poll_until("pollapplyfixes",
                   lambda st: st.get("applyfix_batch_id") in st.get("collected_batches", []))
    else:
        log("no HIGH/MEDIUM findings — skipping applyfixes")

    gate2 = quote_gate("post")
    if gate2.get("lessons_with_misses"):
        log("FINAL QUOTE GATE NOT CLEAN — NOT inserting. Human review needed: "
            + json.dumps(gate2["lessons_with_misses"], ensure_ascii=False)[:800])
        raise SystemExit(2)

    stage("insert")
    stage("media")
    poll_until("pollmedia", lambda st: st.get("media_batch_id") in st.get("collected_batches", []))
    stage("insertmedia")
    stage("costs")
    log("=== anthology build COMPLETE ===")


if __name__ == "__main__":
    main()
