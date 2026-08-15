# -*- coding: utf-8 -*-
"""Museum exhibit 7: the misconception-entry contract.

Imports the REAL validate_entry from enrich_mc.py and pins every house rule:
expect in range and never the correct index, no option-position references,
no sequence words (the bank is shuffled), no board names, no markup, kebab
ids, message length.
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
spec = importlib.util.spec_from_file_location(
    "enrich_mc", os.path.join(ROOT, "scripts", "misconceptions", "enrich_mc.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
validate_entry = mod.validate_entry

fails = 0


def t(name, cond):
    global fails
    if not cond:
        fails += 1
    print(("PASS " if cond else "FAIL ") + name)


def entry(**kw):
    e = {"expect": 1, "id": "tense-confusion",
         "message": "You picked the past tense because the stem looks finished."}
    e.update(kw)
    return e


t("clean entry passes", validate_entry(entry(), 4, 0) == [])
t("expect == correct rejected", any("CORRECT" in p for p in validate_entry(entry(expect=0), 4, 0)))
t("expect out of range rejected", any("range" in p for p in validate_entry(entry(expect=4), 4, 0)))
t("expect non-int rejected", any("range" in p for p in validate_entry(entry(expect="1"), 4, 0)))
t("option-position reference rejected",
  any("position" in p for p in validate_entry(entry(message="Option B is tempting here."), 4, 0)))
t("'the first one' rejected",
  any("position" in p for p in validate_entry(entry(message="You picked the first one by habit."), 4, 0)))
t("sequence word 'again' rejected (bank is shuffled)",
  any("sequence" in p for p in validate_entry(entry(message="You made this mistake again."), 4, 0)))
t("board name rejected",
  any("board" in p for p in validate_entry(entry(message="AQA marks this harshly."), 4, 0)))
t("markup rejected",
  any("markup" in p for p in validate_entry(entry(message="Use the <em>past</em> tense."), 4, 0)))
t("entity rejected",
  any("markup" in p for p in validate_entry(entry(message="It&rsquo;s the ending."), 4, 0)))
t("empty message rejected",
  any("empty" in p for p in validate_entry(entry(message=""), 4, 0)))
t("56-word message rejected",
  any("long" in p for p in validate_entry(entry(message="w " * 56), 4, 0)))
t("uppercase id rejected", validate_entry(entry(id="Tense-Confusion"), 4, 0) != [])
t("two-char id rejected", validate_entry(entry(id="ab"), 4, 0) != [])

print("u03: %d failure(s)" % fails)
sys.exit(1 if fails else 0)
