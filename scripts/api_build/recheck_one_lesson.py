# -*- coding: utf-8 -*-
"""Re-run the fact-check for a SINGLE lesson whose batch reply failed to parse,
and merge the result into the run's factcheck.json.

A batch fact-check reply that does not parse leaves the lesson unchecked while
the report records only a synthetic "(parse failure)" finding — which then makes
the apply-fixes step act on nothing. This runs the same prompt sequentially for
that one lesson so the lesson is genuinely checked before it ships.

Usage: python scripts/api_build/recheck_one_lesson.py <config.json> <custom_id>
"""
import importlib.util
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py"))
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)


def main(cfg_path, cid):
    cfg = drv.load_config(cfg_path)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    obj = json.load(io.open(os.path.join(cfg["run_dir"], "lessons", cid + ".json"), encoding="utf-8"))
    payload = {k: obj.get(k) for k in
               ("content_html", "exam_tip_html", "conclusion_html", "knowledge_checks",
                "flashcard_questions", "glossary_terms", "practice_questions")}
    user = ("LESSON: %s\nTARGET BOARD: %s GCSE %s — question tariffs on this board: %s\n%s\n%s\n\n"
            "Fact-check this lesson. Return the findings JSON."
            % (cid, cfg["exam_board"], cfg["subject_name"],
               " | ".join(plan.get("question_type_names", [])),
               ("SCOPE FOR THIS UNIT: " + cfg.get("scope_statement", "")),
               drv.assessment_rules_block(cfg) + json.dumps(payload, ensure_ascii=False)))
    system = [{"type": "text", "text": drv.FACTCHECK_SYSTEM},
              {"type": "text",
               "text": "SOURCE TEXT (primary authority for quotations):\n\n"
                       + drv.read(cfg["factcheck_context_doc"])}]
    cl = drv.client()
    with cl.messages.stream(model=drv.MODEL_FACTCHECK, max_tokens=8000,
                            tools=[{"type": "web_search_20260209", "name": "web_search",
                                    "max_uses": 8}],
                            system=system,
                            messages=[{"role": "user", "content": user}]) as stream:
        msg = stream.get_final_message()
    drv.log_usage(cfg, "factcheck-retry", drv.MODEL_FACTCHECK, cid, msg.usage)
    text = "".join(b.text for b in msg.content if b.type == "text")
    raw_path = os.path.join(cfg["run_dir"], "factcheck_raw_%s.txt" % cid)
    io.open(raw_path, "w", encoding="utf-8").write(text)
    print("raw reply saved to", raw_path, "(%d chars)" % len(text))
    try:
        findings = drv.parse_json_reply(text).get("findings", [])
    except ValueError as e:
        # One malformed finding must not discard the rest: scan the array with a
        # brace counter and parse each object on its own, skipping only the bad
        # ones. A checker's reply is worth salvaging — re-running costs money and
        # the failure is reproducible.
        print("whole-reply parse failed (%s) — salvaging finding by finding" % e)
        findings, skipped, depth, start, instr, esc = [], 0, None, False, False, 0
        for i, ch in enumerate(text):
            if instr:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    instr = False
                continue
            if ch == '"':
                instr = True
            elif ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and start is not None:
                    chunk = text[start:i + 1]
                    if '"severity"' in chunk:
                        try:
                            findings.append(json.loads(chunk))
                        except ValueError:
                            skipped += 1
                    start = None
        print("salvaged %d findings, skipped %d malformed" % (len(findings), skipped))
    for f in findings:
        f["lesson"] = cid
    print("%s: %d findings (%s)" % (cid, len(findings),
                                    ", ".join(sorted({f.get("severity", "?") for f in findings}))))

    fc_path = os.path.join(cfg["run_dir"], "factcheck.json")
    fc = json.load(io.open(fc_path, encoding="utf-8"))
    fc["findings"] = [f for f in fc["findings"]
                      if not (f.get("lesson") == cid and f.get("claim") == "(parse failure)")]
    fc["findings"].extend(findings)
    io.open(fc_path, "w", encoding="utf-8").write(json.dumps(fc, ensure_ascii=False, indent=1))
    io.open(os.path.join(cfg["run_dir"], "factcheck_retry_%s.json" % cid), "w",
            encoding="utf-8").write(json.dumps(findings, ensure_ascii=False, indent=1))
    print("merged into", fc_path)
    for f in findings:
        print(" -", f.get("severity"), f.get("field"), "|", (f.get("problem") or "")[:150])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
