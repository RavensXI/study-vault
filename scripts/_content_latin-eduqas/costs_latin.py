# -*- coding: utf-8 -*-
"""Spend report for the Latin build.

The driver's own `costs` stage only knows the three models its stages use; this
build also spends on Haiku (hero vision grading and caption writing), so it
carries its own price table rather than editing the shared driver, which other
jobs are using concurrently.

The meter reads high — the Psychology calibration measured the driver's
formula at about 1.9x the settled Console figure — so both numbers are printed.

Usage: python scripts/_content_latin-eduqas/costs_latin.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

PRICES = dict(D.PRICES)
PRICES["claude-haiku-4-5-20251001"] = {"in": 1.0, "out": 5.0}
PRICES["claude-haiku-4-5"] = {"in": 1.0, "out": 5.0}

METER_TO_CONSOLE = 1.9   # measured on the Psychology builds, 18-19 Jul 2026


def cost_of(rec):
    p = PRICES.get(rec["model"])
    if not p:
        return 0.0
    mult = 0.5 if rec["batch"] else 1.0
    c = (rec["input_tokens"] * p["in"]
         + (rec["cache_write_5m"] or 0) * p["in"] * 1.25
         + (rec["cache_write_1h"] or 0) * p["in"] * 2.0
         + rec["cache_read"] * p["in"] * 0.1
         + rec["output_tokens"] * p["out"]) / 1e6 * mult
    c += rec.get("web_searches", 0) * D.WEB_SEARCH_PER_1K / 1000.0
    return c


def main():
    cfg = D.load_config(os.path.join(HERE, "config_latin-eduqas.json"))
    path = os.path.join(cfg["run_dir"], "costs.jsonl")
    if not os.path.exists(path):
        print("no ledger yet")
        return
    recs = [json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()]
    by_stage, unknown = {}, set()
    for r in recs:
        if r["model"] not in PRICES:
            unknown.add(r["model"])
        s = by_stage.setdefault(r["stage"], {"n": 0, "in": 0, "out": 0, "cr": 0,
                                             "cw": 0, "ws": 0, "cost": 0.0})
        s["n"] += 1
        s["in"] += r["input_tokens"]
        s["out"] += r["output_tokens"]
        s["cr"] += r["cache_read"]
        s["cw"] += (r["cache_write_5m"] or 0) + (r["cache_write_1h"] or 0)
        s["ws"] += r.get("web_searches", 0)
        s["cost"] += cost_of(r)
    total = 0.0
    print("%-16s %5s %12s %12s %12s %12s %6s %10s"
          % ("stage", "calls", "input", "output", "cache_read", "cache_write",
             "search", "meter"))
    for stage, s in sorted(by_stage.items(), key=lambda kv: -kv[1]["cost"]):
        total += s["cost"]
        print("%-16s %5d %12d %12d %12d %12d %6d %9.3f$"
              % (stage, s["n"], s["in"], s["out"], s["cr"], s["cw"], s["ws"], s["cost"]))
    print("%-16s %74.3f$" % ("METER TOTAL", total))
    print("%-16s %74.2f$   (meter / %.1f, the measured over-count)"
          % ("Console estimate", total / METER_TO_CONSOLE, METER_TO_CONSOLE))
    if unknown:
        print("models with no price entry (counted as zero):", ", ".join(sorted(unknown)))


if __name__ == "__main__":
    main()
