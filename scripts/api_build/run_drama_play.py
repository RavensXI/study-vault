# -*- coding: utf-8 -*-
"""Orchestrator: rebuild of one AQA Drama set-play unit, end to end.

Same chain as run_ocr_cluster.py with three differences:
  * NO row swap. The eight lesson rows already exist and are patched in place,
    so lesson ids, slugs and hero images survive the rebuild.
  * the quote gate runs against a corpus built mechanically from the source
    bank's own quoted spans, so the bank's explanatory prose can never be passed
    off as a line of the play.
  * related media is audited and merged by drama_media_merge.py rather than
    replaced wholesale, because the existing rows carry a real lesson podcast.

Usage:  python scripts/api_build/run_drama_play.py the-empress
        python scripts/api_build/run_drama_play.py the-empress --stop-before-insert
"""
import io
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
PLAY = sys.argv[1]
STOP_BEFORE_INSERT = "--stop-before-insert" in sys.argv
# Set only after a human has read the remaining quote-gate misses and judged
# each one to be the lesson's own wording rather than an invented play line.
FORCE_INSERT = "--gate-reviewed" in sys.argv
CFG_PATH = os.path.join(HERE, "config_drama-aqa-%s.json" % PLAY)
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
    print(out[-1800:], flush=True)
    if p.returncode != 0:
        log("STAGE FAILED: %s (rc=%d) — tail: %s" % (name, p.returncode, out[-800:]))
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
    log("=== Drama %s rebuild start ===" % PLAY)
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
    if not state().get("unitcheck_counts"):
        stage("unitcheck")

    fc_path = os.path.join(RUN, "factcheck.json")
    fc = json.load(io.open(fc_path, encoding="utf-8"))
    if not fc.get("_gate_folded"):
        added = 0
        for lesson, spans in gate1.get("lessons_with_misses", {}).items():
            for s in spans:
                fc["findings"].append({
                    "severity": "medium", "field": "content_html", "lesson": lesson,
                    "claim": s,
                    "problem": ("This span is inside quotation marks in the lesson but does not "
                                "appear in the source bank's list of quotable spans. The play is "
                                "in copyright and the source bank is the only authority for its "
                                "wording, so no unverified wording may be presented as the "
                                "playwright's words."),
                    "correction": (
                        "JUDGE THE SPAN FIRST. If the lesson presents it as words spoken or "
                        "written in the play — dialogue, a stage direction, a song lyric, a line "
                        "attributed to a character — remove the quotation marks and rewrite the "
                        "sentence as paraphrase, keeping its teaching point, and do NOT "
                        "substitute a different quotation unless that one is on the "
                        "quotable-span list. If instead it is the lesson's OWN wording — a scene "
                        "label, a scare-quote, an example of a weak student phrase, a term being "
                        "defined, a hypothetical line of an answer — then it is not a quotation "
                        "from the play and you must LEAVE IT EXACTLY AS IT IS. Never add a "
                        "caveat, apology or note about sources: the student must not see one."),
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
        # Every remaining miss is a span the model chose to leave in quotation
        # marks after being asked to judge it. That judgement is the thing a
        # human has to check, so the run stops here by default and the misses
        # are written out for review.
        log("FINAL QUOTE GATE NOT CLEAN — %d lessons carry unmatched quoted spans. "
            "Review them before inserting:\n%s"
            % (len(gate2["lessons_with_misses"]),
               json.dumps(gate2["lessons_with_misses"], ensure_ascii=False, indent=1)[:4000]))
        if not FORCE_INSERT:
            stage("costs")
            raise SystemExit(2)

    if STOP_BEFORE_INSERT:
        log("--stop-before-insert set: content is built, stopping before any DB write")
        stage("costs")
        return

    stage("insert")
    if "media_batch_id" not in state():
        stage("media")
    poll_until("pollmedia", lambda s: s.get("media_batch_id") in s.get("collected_batches", []))
    stage("costs")
    log("=== Drama %s rebuild COMPLETE (media merge runs separately) ===" % PLAY)


if __name__ == "__main__":
    main()
