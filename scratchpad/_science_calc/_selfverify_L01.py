# -*- coding: utf-8 -*-
import json, io
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/lesson_higher-calculations-L01@34b52b21dc.json"
pd = json.load(io.open(OUT, encoding="utf-8"))
pb = pd["problem_bank"]
problems = 0
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        problems += 1
        sol = p["solutions"]
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if s.get("answer") is not None]
        # final compute box = last box with phase substitute region; the solve box should equal a solution
        answers = [b["answer"] for b in boxes]
        # find the phase:substitute box
        sub_idx = next((j for j, s in enumerate(gs) if s.get("phase") == "substitute"), None)
        assert sub_idx is not None, f"{tier}[{i}] no substitute boundary"
        live_after = sum(1 for s in gs[sub_idx:] if s.get("answer") is not None)
        assert live_after >= 2, f"{tier}[{i}] only {live_after} live boxes after boundary"
        # the substitute box answer should be a solution (the compute step) OR round-to box
        # check that at least one box answer matches each solution within 0.005
        for sv in sol:
            hit = any(abs(a - sv) < 0.005 for a in answers)
            assert hit, f"{tier}[{i}] solution {sv} not hit by any box (answers={answers})"
        # expects outside accept window
        acc = p.get("accept", 0.005)
        for m in p.get("misconceptions") or []:
            e = m.get("expect")
            if e is not None:
                for sv in sol:
                    assert abs(e - sv) > max(acc, 0.011), f"{tier}[{i}] expect {e} inside accept of {sv}"
        # duplicate solutions within tier check
    seen = {}
    for i, p in enumerate(pb[tier]):
        key = tuple(p["solutions"])
        if p.get("input_type") != "multiple_choice":
            assert key not in seen, f"{tier} duplicate solutions {key} at idx {i} and {seen[key]}"
            seen[key] = i
print(f"self-verify OK: {problems} problems, all box chains land on solutions, no dup, expects clean")

# em dash scan
def scan(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            scan(v, path + "." + str(k))
    elif isinstance(o, list):
        for j, v in enumerate(o): scan(v, path + f"[{j}]")
    elif isinstance(o, str) and "—" in o:
        print("EM DASH at", path, ":", o[:60])
scan(pd)
print("em-dash scan done")
