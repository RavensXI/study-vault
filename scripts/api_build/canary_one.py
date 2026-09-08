# -*- coding: utf-8 -*-
"""Run ONE prepped content request synchronously and validate it.

The fleet rule is canary-before-fleet: a broken prompt found on lesson 1 costs
cents, found on the whole batch it costs the batch. This runs a single request
from requests_content.json, writes the lesson JSON into the run dir, validates
it, and ledgers its usage like any other stage.

Usage: python scripts/api_build/canary_one.py <config.json> <custom_id>
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import driver  # noqa: E402


def main(cfg_path, cid):
    cfg = driver.load_config(cfg_path)
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                             encoding="utf-8"))
    req = next(r for r in reqs if r["custom_id"] == cid)
    params = driver.try_structured(req["params"])
    cl = driver.client()
    with cl.messages.stream(**params) as stream:
        msg = stream.get_final_message()
    rec = driver.log_usage(cfg, "canary", params["model"], cid, msg.usage)
    text = "".join(b.text for b in msg.content if b.type == "text")
    raw_dir = os.path.join(cfg["run_dir"], "raw_content")
    os.makedirs(raw_dir, exist_ok=True)
    io.open(os.path.join(raw_dir, cid + ".txt"), "w", encoding="utf-8").write(text)
    print("canary %s: in=%d out=%d stop=%s ($%.3f)"
          % (cid, rec["input_tokens"], rec["output_tokens"], msg.stop_reason, driver.cost_of(rec)))
    ok, failures = driver.validate_lessons(cfg, {cid: text})
    print("validate:", "PASS" if ok else "FAIL")
    for k, v in failures.items():
        for p in v:
            print("   -", p)
    st = driver.load_state(cfg)
    st["canary_cid"] = cid
    driver.save_state(cfg, st)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
