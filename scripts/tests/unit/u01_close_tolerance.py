# -*- coding: utf-8 -*-
"""Museum exhibit 5: close() and the repr('76.0') bug.

An integral answer key rounded 'to the nearest degree' must tolerate ±0.5 —
repr(76.0) reading as ONE decimal place shrank the tolerance tenfold and
failed a key against its own exact value.
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
spec = importlib.util.spec_from_file_location(
    "qa_answers", os.path.join(ROOT, "scripts", "_qa_practice_answers.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
close = mod.close

fails = 0


def t(name, cond):
    global fails
    if not cond:
        fails += 1
    print(("PASS " if cond else "FAIL ") + name)


# the founding bug: integral key, nearest-degree ask
t("76 vs 76.392 passes (nearest degree)", close(76, 76.392) is True)
t("76 vs 76.6 fails (past half a degree)", close(76, 76.6) is False)
# decimal keys keep last-place tolerance
t("3.14 vs 3.1449 passes (2dp key)", close(3.14, 3.1449) is True)
# beyond both the last-place tolerance AND the 0.5% sig-fig slack
t("3.14 vs 3.20 fails (outside every tolerance)", close(3.14, 3.20) is False)
# inside the sig-fig slack even though outside the dp tolerance — by design
t("3.14 vs 3.147 passes via 0.5% relative slack", close(3.14, 3.147) is True)
# significant-figure slack
t("1234 vs 1235 passes on relative slack", close(1234, 1235) is True)
# exact + null handling
t("exact match passes", close(2.5, 2.5) is True)
t("None stored fails safely", close(None, 1) is False)
t("None computed fails safely", close(1, None) is False)

print("u01: %d failure(s)" % fails)
sys.exit(1 if fails else 0)
