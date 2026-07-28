"""Weekly teacher digest — ONE small-model call per class, over aggregates only.

Reads the teacher dashboard's own aggregate JSON (teach.html?agg=1 renders it
into <pre id="aggjson"> — the same numbers the page shows, never raw answers),
asks claude -p (subscription, --model haiku-equivalent via sonnet default) for
a short teacher brief, and writes design-lab/teach-digest.js.

This is the entire recurring AI cost of the teacher dashboard: one call per
class per week. Run from Task Scheduler alongside the other nightly jobs, or
by hand. Usage: python scripts/_teach_digest.py [--url URL]
"""
import argparse, datetime, html, json, os, re, shutil, subprocess, sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "teach-digest.js")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PROMPT = """You are writing the weekly one-paragraph brief for a GCSE class teacher,
from aggregate revision data (below). Rules:
- 3-4 sentences of flowing prose FIRST: the most important finding (with the numbers
  that justify it), who stands out and why, and one genuine positive.
- Then 2-3 bullet points: the clearest FINDINGS a teacher should know, phrased as
  findings ("X hasn't stuck", "Y is being forgotten", "Z revises daily but little
  sticks") — NEVER as instructions or suggested actions. What to do about a finding
  is the teacher's call, not yours. No "reteach", no "check in with", no "worth doing".
- Warm, professional, zero jargon, zero flattery. Never invent numbers not in the data.
- Retrieval accuracy is retention evidence, not ability — phrase accordingly
  ("hasn't stuck yet", never "weak students").
Output ONLY the HTML fragment (use <b>, <ul><li> — no headings, no markdown, no commentary).

DATA:
"""


def get_agg(url):
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                        "--virtual-time-budget=6000", "--dump-dom", url + "?agg=1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    m = re.search(r'<pre id="aggjson"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m:
        raise SystemExit("no aggregate JSON found at " + url)
    return json.loads(html.unescape(m.group(1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8901/design-lab/teach.html")
    args = ap.parse_args()

    agg = get_agg(args.url)
    exe = shutil.which("claude")
    if not exe:
        raise SystemExit("claude CLI not on PATH")
    r = subprocess.run([exe, "-p", "--model", "sonnet"],
                       input=PROMPT + json.dumps(agg, ensure_ascii=False),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    if r.returncode != 0:
        raise SystemExit("claude -p failed: " + (r.stderr or "")[-300:])
    frag = r.stdout.strip()
    frag = re.sub(r"^```(?:html)?|```$", "", frag, flags=re.M).strip()
    if "<" not in frag or len(frag) < 80:
        raise SystemExit("suspicious digest output, not writing: " + frag[:200])

    stamp = ("Written " + datetime.date.today().strftime("%A %d %B")
             + " · one model call over class aggregates · regenerates weekly")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* Written weekly by scripts/_teach_digest.py — one claude -p call per class\n"
                "   over the page's aggregates (never raw answers, never per student). */\n"
                "window.SV_TEACH_DIGEST = " + json.dumps({"html": frag, "stamp": stamp}, ensure_ascii=False) + ";\n")
    print("digest written ->", OUT)
    print(frag[:400])


if __name__ == "__main__":
    main()
