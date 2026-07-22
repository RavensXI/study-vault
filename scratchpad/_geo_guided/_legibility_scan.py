# -*- coding: utf-8 -*-
"""Scan practice walks for the legibility traps behind Tom's pie-chart report.

    python scratchpad/_geo_guided/_legibility_scan.py <subject-slug> <unit-slug>

Deterministic first pass. It cannot judge whether a 15-year-old will follow a
sentence, but it can catch the mechanical version of the exact bug on L02
bronze[6], where a walk step said "multiply by 500 billion litres", wanted the
bare numeral 100, and gave the box no label to say so.

Flags, per guided step that has a numeric answer box and no `post` label:
  MAGNITUDE  prose carries a scale word (billion/million/thousand) and does not
             state the answer's unit, so the student cannot tell 100 from
             100000000000 -- the exact trap Tom hit
  UNIT       prose names a unit but does not say "in <unit>", so the box is
             genuinely unlabelled (steps that already say "in metres" are fine
             and are NOT flagged)
Independent of the box:
  FRAGMENT   the instruction reads as a fragment: ends "=" or "in the same way"
  DECIMAL    the step assumes converting to a decimal with no lead-in

The player already renders `post` to the right of a step box; MAGNITUDE/UNIT are
the steps that should have carried one and did not.
"""
import json, os, re, sys, urllib.request

S = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
K = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}


def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(S + u, headers=H), timeout=120))


SCALE = re.compile(r"\b(billion|million|thousand|hundred)\b", re.I)
UNIT = re.compile(r"\b(litres?|degrees?|kilometres?|metres?|hectares?|tonnes?|km|mm|cm)\b|%|°", re.I)
STATES_UNIT = re.compile(r"\bin (metres|km|kilometres|litres|degrees|hectares|billions?|millions?|thousands?|per ?cent|tonnes)\b", re.I)
FRAGMENT = re.compile(r"(=\s*$|\bin the same way\b)", re.I)
DECIMAL = re.compile(r"as a decimal", re.I)


def strip(t):
    return re.sub(r"<[^>]+>", "", str(t or "")).strip()


def scan_step(pre, post, ans):
    pre_s = strip(pre)
    flags = []
    numeric = isinstance(ans, (int, float)) and not isinstance(ans, bool)
    labelled = bool(strip(post))
    states_unit = bool(STATES_UNIT.search(pre_s))
    if numeric and not labelled and not states_unit:
        if SCALE.search(pre_s):
            flags.append("MAGNITUDE")
        elif UNIT.search(pre_s):
            flags.append("UNIT")
    if FRAGMENT.search(pre_s):
        flags.append("FRAGMENT")
    if DECIMAL.search(pre_s):
        flags.append("DECIMAL")
    return flags


def main(subj, unit_slug):
    sid = get("subjects?slug=eq.%s&select=id" % subj)[0]["id"]
    units = get("units?subject_id=eq.%s&select=id,slug" % sid)
    unit = next((u for u in units if u["slug"] == unit_slug), None)
    if not unit:
        sys.exit("unit not found: %s" % unit_slug)
    lessons = get("lessons?unit_id=eq.%s&select=lesson_number,title,practice_data" % unit["id"])
    counts = {"MAGNITUDE": 0, "UNIT": 0, "FRAGMENT": 0, "DECIMAL": 0}
    problem_rows = 0
    flagged_problems = 0
    verbose = "-v" in sys.argv
    for l in sorted(lessons, key=lambda x: x["lesson_number"]):
        pb = (l.get("practice_data") or {}).get("problem_bank") or {}
        hits = []
        for tier, items in pb.items():
            if not isinstance(items, list):
                continue
            for i, p in enumerate(items):
                if not isinstance(p, dict):
                    continue
                problem_rows += 1
                pflags = set()
                for si, st in enumerate(p.get("guided_steps") or []):
                    if not isinstance(st, dict):
                        continue
                    for f in scan_step(st.get("pre"), st.get("post"), st.get("answer")):
                        counts[f] += 1
                        pflags.add(f)
                        hits.append("%s[%d].step%d %-9s %s" % (tier, i, si, f, strip(st.get("pre"))[:66]))
                if pflags:
                    flagged_problems += 1
        if hits and verbose:
            print("L%02d  %s" % (l["lesson_number"], l["title"]))
            for h in hits:
                print("     " + h)
    print()
    print("subject=%s unit=%s" % (subj, unit_slug))
    print("problems scanned: %d   problems with >=1 flag: %d" % (problem_rows, flagged_problems))
    print("step flags: " + "  ".join("%s=%d" % (k, v) for k, v in counts.items()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
