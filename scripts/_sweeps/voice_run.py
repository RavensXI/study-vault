"""Run voice_pass.py for one or more subjects and commit each subject."""
import json
import os
import subprocess
import sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
OUT = os.path.join(HERE, "voice")

for slug in sys.argv[1:]:
    edits = os.path.join(OUT, f"edits_{slug}.json")
    if not os.path.exists(edits):
        print(f"!! no edits file for {slug}")
        sys.exit(1)
    p = subprocess.run([sys.executable, os.path.join(HERE, "voice_pass.py"), "--edits", edits],
                       cwd=ROOT, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if p.returncode != 0:
        print(f"!! {slug} FAILED rc={p.returncode}")
        sys.exit(p.returncode)
    res = json.load(open(os.path.join(OUT, f"_result_{slug}.json"), encoding="utf-8"))
    n, clips = res["sentences_rewritten"], res["renarrated_clips"]
    msg = (f"Voice pass: {slug} - {n} sentence{'' if n == 1 else 's'} rewritten, "
           f"{clips} block{'' if clips == 1 else 's'} re-narrated\n\n"
           "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>")
    subprocess.run(["git", "-C", ROOT, "add", "scripts/_sweeps"], capture_output=True)
    subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", msg], capture_output=True)
    print(f"   committed: {slug} ({n} sentences, {clips} clips)")
