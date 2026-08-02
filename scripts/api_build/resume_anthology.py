# -*- coding: utf-8 -*-
"""Resume the anthology build after the quote-gate adjudication: final gate,
insert, media, costs. Run from repo root."""
import io
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_PATH = os.path.join(HERE, "config_englit-eduqas-anthology.json")
CFG = json.load(io.open(CFG_PATH, encoding="utf-8"))
RUN = CFG["run_dir"]


def run(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(p.stdout)
    if p.stderr:
        print(p.stderr)
    return p.returncode


def stage(name):
    print("== stage:", name, flush=True)
    rc = run([os.path.join(HERE, "driver.py"), "--config", CFG_PATH, name])
    if rc != 0:
        print("STAGE FAILED:", name)
        raise SystemExit(1)


def state():
    return json.load(io.open(os.path.join(RUN, "state.json"), encoding="utf-8"))


print("== final quote gate (word-level)")
rc = run([os.path.join(HERE, "quote_gate.py"), CFG["factcheck_context_doc"],
          os.path.join(RUN, "lessons"), os.path.join(RUN, "quote_gate_final.json")])
if rc != 0:
    print("GATE STILL NOT CLEAN — stopping for human review")
    raise SystemExit(2)

stage("insert")
stage("media")
for _ in range(48):
    stage("pollmedia")
    if state().get("media_batch_id") in state().get("collected_batches", []):
        break
    time.sleep(300)
stage("insertmedia")
stage("costs")
print("== anthology build COMPLETE ==")
