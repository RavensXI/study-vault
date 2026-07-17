import json
for f in ["_L09_live_fresh.json","lesson_maths-aqa_algebra-L09.json"]:
    d = json.load(open(f, encoding="utf-8"))
    pd = d["practice_data"] if "practice_data" in d else d
    g0 = pd["problem_bank"]["gold"][0]["display"]
    op = pd["guided"]["opener"]["display"]
    print("FILE:", f)
    print("  gold0 codepoints for non-ascii:", [hex(ord(c)) for c in g0 if ord(c) > 127])
    print("  opener disp:", repr(op))
    print("  opener codepoints:", [hex(ord(c)) for c in op if ord(c) > 127])
    # also opener step pre
    for s in pd["guided"]["opener"]["steps"]:
        if s.get("pre"):
            print("   step pre:", repr(s["pre"]), [hex(ord(c)) for c in s["pre"] if ord(c)>127])
