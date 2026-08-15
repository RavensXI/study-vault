# -*- coding: utf-8 -*-
"""The AI-prompt misconception vocabularies stay well-formed.

The runtime validates tags against /^[a-z0-9-]{3,40}$/ and rejects 'none' —
a malformed tag in the controlled vocab would silently never log. Imports
the REAL constants from enrich_ai_prompts.py.
"""
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
spec = importlib.util.spec_from_file_location(
    "enrich_ai_prompts",
    os.path.join(ROOT, "scripts", "misconceptions", "enrich_ai_prompts.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

fails = 0


def t(name, cond):
    global fails
    if not cond:
        fails += 1
    print(("PASS " if cond else "FAIL ") + name)


for name in ("TAGS_MFL", "TAGS_ENG"):
    raw = getattr(mod, name)
    tags = [x.strip() for x in raw.split(",") if x.strip()]
    t("%s: non-empty" % name, len(tags) >= 5)
    bad = [x for x in tags if not re.fullmatch(r"[a-z0-9-]{3,40}", x)]
    t("%s: every tag matches the runtime pattern" % name, not bad)
    if bad:
        print("   bad:", bad)
    t("%s: no duplicates" % name, len(tags) == len(set(tags)))
    t("%s: 'none' is not a tag" % name, "none" not in tags)

print("u04: %d failure(s)" % fails)
sys.exit(1 if fails else 0)
