"""Diagram canary: generate one GPT-Image-2 visual per briefed lesson via Foundry.

Usage: python scripts/diagrams/canary_generate.py <canary_dir> [--only 2,5] [--retry-notes notes.json]
Reads <canary_dir>/briefs.json (from the brief agent) and lessons.json (unit accent),
writes <canary_dir>/out/L{n}.png + L{n}.jpg (max 1000px wide, q82) and results.json
(tokens, seconds, prompt, attempt). Re-runs skip lessons already accepted in results.json
unless --only names them. Retry notes (from the vision gate) are appended to the prompt.
House style + template: docs/DIAGRAM_PIPELINE.md, "GPT-Image-2 house style".
"""
import argparse, base64, io, json, os, subprocess, sys, time, urllib.request
from PIL import Image

STYLE = (
    " Style: a modern GCSE textbook illustration on a warm off-white paper background (#faf8f5), "
    "clean vector-like line work with soft flat colour fills and gentle shading for depth. "
    "Use the accent colour {accent} ONLY for label text, leader lines, arrows, chart lines and axis marks. "
    "Physical materials, people, objects and places keep their natural, period-appropriate muted colours; "
    "abstract shapes with no natural colour in neutral greys. "
    "Clear humanist sans-serif labels with thin leader lines, generous margins, no photographic realism, "
    "no clutter, no logos, no real identifiable people, no faceless people, no exam-board names. "
    "Period insignia, uniforms, flags and badges may appear where they are historically accurate for the date shown."
)
NO_TEXT = (" Do not include a title, a caption or a key. Any lettering on drawn objects (documents, signs, flags, books) "
           "must be real, correctly spelled words in English or the period language, appropriate to the date shown.")


def uenv(n):
    v = os.environ.get(n)
    if v:
        return v
    return subprocess.run(["powershell", "-NoProfile", "-Command",
                           f"[Environment]::GetEnvironmentVariable('{n}','User')"],
                          capture_output=True, text=True).stdout.strip()


def build_prompt(b, accent, retry_note=None):
    labels = "; ".join(b["labels"]) if b["labels"] else "no text at all"
    p = f"{b['diagram_form']} for a GCSE lesson: {b['content']}"
    if b.get("data"):
        p += " Use exactly these figures, verbatim: " + "; ".join(b["data"]) + "."
    if b.get("anchor_figure"):
        p += " " + b["anchor_figure"].rstrip(".") + ", drawn in the same flat style and sharing the chart's baseline."
    p += f" These labels must appear, spelled exactly like this: {labels}."
    if b.get("facts"):
        p += " The picture must show: " + "; ".join(b["facts"]) + "."
    p += NO_TEXT + STYLE.format(accent=accent)
    if retry_note:
        p += f" Correction from the previous attempt, which was rejected: {retry_note}"
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canary_dir")
    ap.add_argument("--only", default="")
    ap.add_argument("--retry-notes", default="")
    ap.add_argument("--size", default="1536x1024")
    a = ap.parse_args()
    D = a.canary_dir
    out = os.path.join(D, "out"); os.makedirs(out, exist_ok=True)
    briefs = json.load(open(os.path.join(D, "briefs.json"), encoding="utf-8"))
    accent = json.load(open(os.path.join(D, "lessons.json"), encoding="utf-8"))["unit"]["accent"]
    rp = os.path.join(D, "results.json")
    results = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
    notes = json.load(open(a.retry_notes, encoding="utf-8")) if a.retry_notes else {}
    only = {int(x) for x in a.only.split(",") if x.strip()}
    EP = uenv("FOUNDRY_ENDPOINT").rstrip("/"); KEY = uenv("FOUNDRY_KEY")
    H = {"Content-Type": "application/json", "api-key": KEY}
    for b in briefs:
        n = b["lesson_number"]; key = f"L{n}"
        if b["visual_form"] == "none":
            results[key] = {"form": "none"}; continue
        if only and n not in only:
            continue
        if not only and results.get(key, {}).get("ok") and not notes.get(key):
            continue
        prompt = build_prompt(b, accent, notes.get(key))
        body = {"prompt": prompt, "model": "gpt-image-2", "size": a.size, "quality": "medium"}
        attempt = results.get(key, {}).get("attempt", 0) + 1
        for tries in range(3):
            t = time.time()
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(
                    EP + "/openai/v1/images/generations", data=json.dumps(body).encode(), headers=H, method="POST"), timeout=300))
                break
            except urllib.error.HTTPError as e:
                msg = e.read()[:200]
                print(key, "HTTP", e.code, msg, file=sys.stderr)
                if e.code == 429:
                    time.sleep(45); continue
                results[key] = {"ok": False, "error": f"HTTP {e.code}: {msg}", "attempt": attempt}; r = None; break
        else:
            results[key] = {"ok": False, "error": "rate-limited x3", "attempt": attempt}; r = None
        if not r:
            json.dump(results, open(rp, "w", encoding="utf-8"), indent=1); continue
        secs = time.time() - t
        raw = base64.b64decode(r["data"][0]["b64_json"])
        png = os.path.join(out, f"{key}.png"); open(png, "wb").write(raw)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width > 1000:
            im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        jpg = os.path.join(out, f"{key}.jpg"); im.save(jpg, "JPEG", quality=82, optimize=True)
        results[key] = {"ok": True, "form": b["visual_form"], "attempt": attempt, "seconds": round(secs, 1),
                        "output_tokens": r.get("usage", {}).get("output_tokens"),
                        "input_tokens": r.get("usage", {}).get("input_tokens"),
                        "png": png, "jpg": jpg, "jpg_bytes": os.path.getsize(jpg), "prompt": prompt}
        print(key, b["visual_form"], f"{secs:.0f}s", r.get("usage", {}).get("output_tokens"), "tokens, attempt", attempt)
        json.dump(results, open(rp, "w", encoding="utf-8"), indent=1)
    done = [k for k, v in results.items() if v.get("ok")]
    toks = sum(v.get("output_tokens", 0) for v in results.values() if v.get("ok"))
    print(f"generated {len(done)} images, {toks} output tokens ≈ £{toks * 30 / 1e6:.2f} at £30/M")


if __name__ == "__main__":
    main()
