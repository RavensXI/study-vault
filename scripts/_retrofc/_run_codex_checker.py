"""Run a retro fact-check checker through the OpenAI Codex CLI (ChatGPT subscription).

Same contract as the Claude checker: reads <unit-dir>/_brief.json + raw/L*.txt,
writes <unit-dir>/_report.json and <unit-dir>/_edits.json. Never writes to
Supabase: the Codex process gets only core environment variables (no service
keys) and a workspace-write sandbox.

Usage:
  python scripts/_retrofc/_run_codex_checker.py <unit-dir> --model gpt-5.6-sol --effort medium
      [--family english-literature|science|history|generic] [--facts "board facts line"]
      [--text "primary text note"] [--timeout-min 40]

Writes <unit-dir>/_codex_run.log, _codex_last_message.md, _codex_done.json
({model, effort, started, finished, minutes, exit_code, report_ok, edits_ok}).
"""
import datetime
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CODEX = r"C:\Users\tshau\AppData\Local\OpenAI\Codex\bin\994e8469124a0d31\codex.exe"
BRIEFS = {"english-literature": "scripts/_retrofc/CHECK_PROMPT.md", "science": "scripts/_retrofc/CHECK_PROMPT_SCIENCE.md",
          "history": "scripts/_retrofc/CHECK_PROMPT_HISTORY.md"}


def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default


def main():
    unit_dir = os.path.abspath(sys.argv[1])
    rel = os.path.relpath(unit_dir, ROOT).replace("\\", "/")
    model = arg("--model", "gpt-5.6-sol")
    effort = arg("--effort", "medium")
    family = arg("--family", "english-literature")
    facts = arg("--facts", "read the spec's assessment section before asserting any exam claim")
    text_note = arg("--text", None)
    timeout_min = float(arg("--timeout-min", "40"))
    brief = json.load(open(os.path.join(unit_dir, "_brief.json"), encoding="utf-8"))
    check_prompt = BRIEFS.get(family, "scripts/_retrofc/CHECK_PROMPT_GENERIC.md")
    primary = brief.get("primary_text")
    text_line = text_note or (f"{primary} (GREP it; never read it whole)" if primary else "in copyright: verify quotations only against sources you can fetch; unverifiable quotations are NOTEs")
    n = len(brief["lessons"])
    prompt = f"""Repo root: {ROOT} (run everything from there; you are already in it).
First read {check_prompt} in full; it is your brief and its rules bind.
Unit to check: {brief['subject']} / {brief['unit']} ({n} lessons). Unit dir: {rel} (this is the ONLY directory you write to; ignore the 'dir' field inside _brief.json).
Brief: {rel}/_brief.json. Spec: {brief['spec']}. Board facts: {facts}
Primary text: {text_line}
Read {rel}/raw/L01.txt ... one at a time. Check every quotation (wording, speaker, scene/chapter), every exam claim against the spec, every answer key against the corrected facts. Write {rel}/_report.json and {rel}/_edits.json exactly in the shapes the brief specifies; `find` strings copied exactly and unique in their field. Do NOT write anywhere else, do NOT modify any other file, do NOT run any script that writes to a database or network service. Verify every `find` string occurs exactly once in its field before finishing (a short python check is fine). Finish with a report under 250 words as the brief describes.
"""
    log = open(os.path.join(unit_dir, "_codex_run.log"), "w", encoding="utf-8")
    started = datetime.datetime.now()
    cmd = [CODEX, "exec", "-m", model, "-c", f'model_reasoning_effort="{effort}"', "-c", 'shell_environment_policy.inherit="core"',
           "-C", ROOT, "-s", "workspace-write", "--add-dir", unit_dir, "--color", "never",
           "-o", os.path.join(unit_dir, "_codex_last_message.md"), prompt]
    log.write(f"# {started.isoformat(timespec='seconds')} model={model} effort={effort}\n# {' '.join(cmd[:-1])} <prompt>\n\n")
    log.flush()
    try:
        p = subprocess.Popen(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        while p.poll() is None:
            if (datetime.datetime.now() - started).total_seconds() > timeout_min * 60:
                p.kill()
                log.write(f"\n# KILLED after {timeout_min} min\n")
                break
            time.sleep(10)
        code = p.returncode
    except Exception as e:  # noqa: BLE001
        log.write(f"\n# LAUNCH ERROR {e}\n")
        code = -1
    finished = datetime.datetime.now()
    log.close()
    done = {"model": model, "effort": effort, "started": started.isoformat(timespec="seconds"), "finished": finished.isoformat(timespec="seconds"),
            "minutes": round((finished - started).total_seconds() / 60, 1), "exit_code": code,
            "report_ok": os.path.exists(os.path.join(unit_dir, "_report.json")), "edits_ok": os.path.exists(os.path.join(unit_dir, "_edits.json"))}
    json.dump(done, open(os.path.join(unit_dir, "_codex_done.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(done))


if __name__ == "__main__":
    main()
