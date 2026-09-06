# -*- coding: utf-8 -*-
"""Orchestrator: OCR J352 poetry-cluster rebuild, end to end.

Same chain as run_anthology.py, with three differences:
  * the config is chosen on the command line (one per cluster);
  * the deterministic quote gate runs against cfg["quote_gate_corpus"], which
    holds the ten full poem texts plus the curated allow-list spans for the five
    guide-only poems — OCR's guide prose is excluded so guide commentary cannot
    be passed off as a poem line;
  * the Supabase row swap (backup, delete, fifteen skeletons) runs immediately
    before insert, and only after the final gate is clean.

Usage:  python scripts/api_build/run_ocr_cluster.py conflict
"""
import io
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
CLUSTER = sys.argv[1]
CFG_PATH = os.path.join(HERE, "config_englit-ocr-%s.json" % CLUSTER)
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
    print(out[-1500:], flush=True)
    if p.returncode != 0:
        log("STAGE FAILED: %s (rc=%d) — tail: %s" % (name, p.returncode, out[-600:]))
        raise SystemExit(1)
    return out


def state():
    return json.load(io.open(os.path.join(RUN, "state.json"), encoding="utf-8"))


def poll_until(stage_name, done, max_minutes=300):
    for _ in range(max_minutes // 5):
        stage(stage_name)
        if done(state()):
            return
        time.sleep(300)
    log("TIMEOUT waiting on " + stage_name)
    raise SystemExit(1)


def quote_gate(tag):
    out = os.path.join(RUN, "quote_gate_%s.json" % tag)
    corpus = CFG.get("quote_gate_corpus") or CFG["factcheck_context_doc"]
    p = subprocess.run([sys.executable, os.path.join(HERE, "quote_gate.py"),
                        corpus, os.path.join(RUN, "lessons"), out],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    LOG.write((p.stdout or "") + "\n")
    LOG.flush()
    print(p.stdout, flush=True)
    log("quote gate (%s): rc=%d" % (tag, p.returncode))
    return json.load(io.open(out, encoding="utf-8"))


def main():
    log("=== OCR %s cluster build start ===" % CLUSTER)
    if not os.path.exists(os.path.join(RUN, "requests_content.json")):
        stage("prep")
    st = state()
    if "content_batch_id" not in st:
        stage("submit")
    poll_until("poll", lambda s: "content_ok" in s)

    for round_ in (1, 2):
        st = state()
        if not st.get("content_failures") and not st.get("content_errors"):
            break
        log("fix round %d: %d failures" % (round_, len(st.get("content_failures", {}))))
        stage("fix")
        poll_until("pollfix", lambda s: s.get("fix_batch_id") in s.get("collected_batches", []))
    st = state()
    log("content complete: %d ok, %d failing" % (len(st.get("content_ok", [])),
                                                 len(st.get("content_failures", {}))))

    gate1 = quote_gate("pre")

    if not os.path.exists(os.path.join(RUN, "factcheck.json")):
        stage("factcheck")
        poll_until("pollfactcheck",
                   lambda s: os.path.exists(os.path.join(RUN, "factcheck.json")))

    fc_path = os.path.join(RUN, "factcheck.json")
    fc = json.load(io.open(fc_path, encoding="utf-8"))
    if not fc.get("_gate_folded"):
        added = 0
        for lesson, spans in gate1.get("lessons_with_misses", {}).items():
            for s in spans:
                fc["findings"].append({
                    "severity": "high", "field": "content_html", "lesson": lesson,
                    "claim": s,
                    "problem": ("Quoted span not found verbatim in the supplied poem texts or "
                                "in the quotable-span list for a guide-sourced poem."),
                    "correction": ("Remove the quotation marks and rewrite the sentence as "
                                   "paraphrase, so that no unverified wording is presented as a "
                                   "line of the poem. The sentence must still make sense and keep "
                                   "its teaching point. Do NOT substitute a different quotation "
                                   "unless you are certain it is verbatim. Never leave an invented "
                                   "poem line in place, and never add any caveat, apology or note "
                                   "about sources — the student must not see one."),
                })
                added += 1
        fc["_gate_folded"] = True
        io.open(fc_path, "w", encoding="utf-8").write(json.dumps(fc, ensure_ascii=False, indent=1))
        log("folded %d quote-gate misses into factcheck findings" % added)

    st = state()
    if any(f.get("severity") in ("high", "medium") for f in fc["findings"]) \
            and "applyfix_batch_id" not in st:
        stage("applyfixes")
        poll_until("pollapplyfixes",
                   lambda s: s.get("applyfix_batch_id") in s.get("collected_batches", []))
    elif "applyfix_batch_id" in st:
        poll_until("pollapplyfixes",
                   lambda s: s.get("applyfix_batch_id") in s.get("collected_batches", []))
    else:
        log("no HIGH/MEDIUM findings — skipping applyfixes")

    gate2 = quote_gate("post")
    if gate2.get("lessons_with_misses"):
        log("FINAL QUOTE GATE NOT CLEAN — NOT inserting. Human review needed: "
            + json.dumps(gate2["lessons_with_misses"], ensure_ascii=False)[:1200])
        raise SystemExit(2)

    if not state().get("rows_swapped"):
        log("stage: swap rows (backup, delete 8, insert 15 skeletons)")
        p = subprocess.run([sys.executable, os.path.join(HERE, "swap_ocr_rows.py"), CLUSTER],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        LOG.write((p.stdout or "") + (p.stderr or "") + "\n")
        LOG.flush()
        print(p.stdout, p.stderr, flush=True)
        if p.returncode != 0:
            log("ROW SWAP FAILED")
            raise SystemExit(1)
        s = state()
        s["rows_swapped"] = True
        io.open(os.path.join(RUN, "state.json"), "w", encoding="utf-8").write(json.dumps(s, indent=1))

    stage("insert")
    if "media_batch_id" not in state():
        stage("media")
    poll_until("pollmedia", lambda s: s.get("media_batch_id") in s.get("collected_batches", []))
    stage("insertmedia")
    stage("costs")
    log("=== OCR %s cluster build COMPLETE ===" % CLUSTER)


if __name__ == "__main__":
    main()
