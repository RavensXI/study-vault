# -*- coding: utf-8 -*-
"""StudyVault test suite runner (docs/TEST_SUITE_PLAN.md).

    python scripts/tests/run_tests.py            # --fast: unit + api
    python scripts/tests/run_tests.py --full     # adds e2e (Playwright, mocked)
    python scripts/tests/run_tests.py --live     # adds read-only production smoke

No framework: .py runs under this interpreter, .js under node. A test passes
on exit code 0, fails otherwise. The api ring needs the database — if the
probe fails, api tests report SKIPPED, never FAILED (a down database must not
read as a broken codebase).
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

RINGS = ["unit", "api"]
if "--full" in sys.argv:
    RINGS.append("e2e")
if "--live" in sys.argv:
    RINGS.append("live")

DB_RINGS = {"api", "live"}
TIMEOUT = {"unit": 60, "api": 180, "e2e": 420, "live": 180}


def db_up():
    """Fast probe: can we reach Supabase at all?"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        return False, "SUPABASE_URL / key not in env"
    try:
        req = urllib.request.Request(
            url.rstrip("/") + "/rest/v1/subjects?select=id&limit=1",
            headers={"apikey": key, "Authorization": "Bearer " + key})
        urllib.request.urlopen(req, timeout=8).read()
        return True, ""
    except Exception as e:
        return False, str(e)[:80]


def discover(ring):
    d = os.path.join(HERE, ring)
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d)
                  if (f.endswith(".py") or f.endswith(".js")) and not f.startswith("_"))


def run_one(path, ring):
    cmd = ([sys.executable] if path.endswith(".py") else ["node"]) + [path]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=ROOT, timeout=TIMEOUT[ring])
        return ("PASS" if r.returncode == 0 else "FAIL",
                time.time() - t0, r.stdout, r.stderr)
    except subprocess.TimeoutExpired:
        return "FAIL", time.time() - t0, "", "TIMEOUT after %ds" % TIMEOUT[ring]


def main():
    up, why = db_up()
    results = []          # (ring, name, status, secs)
    detail = []           # full output of failures

    for ring in RINGS:
        tests = discover(ring)
        for path in tests:
            name = os.path.basename(path)
            if ring in DB_RINGS and not up:
                results.append((ring, name, "SKIP", 0.0))
                continue
            status, secs, out, err = run_one(path, ring)
            results.append((ring, name, status, secs))
            if status == "FAIL":
                detail.append((ring, name, out[-2500:], err[-1200:]))

    print("\n" + "=" * 62)
    print("%-6s %-38s %-6s %s" % ("RING", "TEST", "RESULT", "TIME"))
    print("-" * 62)
    for ring, name, status, secs in results:
        print("%-6s %-38s %-6s %4.1fs" % (ring, name, status, secs))
    n = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for _, _, s, _ in results:
        n[s] += 1
    print("-" * 62)
    print("pass %d  fail %d  skip %d" % (n["PASS"], n["FAIL"], n["SKIP"]))
    if not up and n["SKIP"]:
        print("db probe failed (%s) — db-backed rings SKIPPED, not failed" % why)

    for ring, name, out, err in detail:
        print("\n----- FAIL %s/%s -----" % (ring, name))
        if out.strip():
            print(out.rstrip())
        if err.strip():
            print("stderr:", err.rstrip())

    sys.exit(1 if n["FAIL"] else 0)


if __name__ == "__main__":
    main()
