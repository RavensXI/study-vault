"""Retro fact-check: check one lesson's R2 explainer video against the corrected lesson text (Gemini 3.8 Flash, static mode).

Usage: _video_check.py <subject> <unit> <lesson_number> [--mode static|agentic] [--model gemini-3.8-flash]
Run with scripts/_retrofc/_venv_genai/Scripts/python.exe (google-genai >= 2.0; the repo's global SDK is older).

Reads the live lesson row and the unit's _report.json FIX findings for that lesson, downloads the video to
_video_cache/, uploads it to the Gemini Files API, and asks the model whether the video still voices any
stale claim. The gate is GCSE stakes, not strict accuracy (Tom, 5 Sep 2026): a claim counts as mark_affecting
only if a student repeating it would lose marks or learn a wrong examinable fact; simplifications are pedantry.
Writes units/<subject>__<unit>/_video/L<n>.json and prints a one-line JSON summary. Deletes the cached mp4 and
the Files API upload afterwards.
Pricing (intro to 31 Dec 2026): $0.75/M input, $3.75/M output; tool-use tokens bill as input, thinking as output.
"""
import json, os, re, sys, time, urllib.request
from google import genai

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
subject, unit, ln = sys.argv[1], sys.argv[2], int(sys.argv[3])
mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "static"
model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "gemini-3.8-flash"
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
GBP_PER_USD = 0.74


def get(path):
    return json.load(urllib.request.urlopen(urllib.request.Request(f"{U}/rest/v1/{path}", headers=H), timeout=60))


def strip(h):
    h = re.sub(r"<[^>]+>", " ", h or "")
    for a, b in (("&rsquo;", "'"), ("&lsquo;", "'"), ("&mdash;", " - "), ("&ndash;", "-"), ("&amp;", "&"),
                 ("&ldquo;", '"'), ("&rdquo;", '"'), ("&nbsp;", " "), ("&hellip;", "...")):
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h).strip()


# a slug can exist twice (free tier + a school build): pick the subject that owns this unit
sid = next(s["id"] for s in get(f"subjects?slug=eq.{subject}&select=id")
           if get(f"units?subject_id=eq.{s['id']}&slug=eq.{unit}&select=id"))
uid = get(f"units?subject_id=eq.{sid}&slug=eq.{unit}&select=id")[0]["id"]
row = get(f"lessons?unit_id=eq.{uid}&lesson_number=eq.{ln}&select=id,title,content_html,conclusion_html,youtube_video_id")[0]
video_url = row["youtube_video_id"]
if not (video_url and "r2.dev" in video_url):
    print(json.dumps({"lesson": ln, "skipped": "no R2 video"})); sys.exit(0)

udir = os.path.join(HERE, "units", f"{subject}__{unit}")
rep_path = os.path.join(udir, "_report.json")
findings = []
if os.path.exists(rep_path):
    rep = json.load(open(rep_path, encoding="utf-8"))
    findings = [f for f in rep["findings"] if f.get("lesson") == ln and f.get("verdict") == "FIX"]
fx = "\n".join(f"- {f['id']} [{f['severity']}] The lesson USED TO say: {f['claim']} | Corrected to: {f['truth']}" for f in findings) \
     or "(no findings recorded for this lesson)"
lesson_text = strip(row["content_html"]) + "\n\nKey takeaways: " + strip(row["conclusion_html"])

cache = os.path.join(HERE, "_video_cache"); os.makedirs(cache, exist_ok=True)
vp = os.path.join(cache, f"{subject}__{unit}__L{ln}.mp4")
with urllib.request.urlopen(urllib.request.Request(video_url, headers={"User-Agent": "Mozilla/5.0 StudyVault-videocheck"}), timeout=300) as r, open(vp, "wb") as f:
    f.write(r.read())
size_mb = os.path.getsize(vp) / 1e6

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
t0 = time.time()
vf = client.files.upload(file=vp)
while not vf.state or vf.state.name != "ACTIVE":
    time.sleep(3); vf = client.files.get(name=vf.name)
t_upload = time.time() - t0

prompt = f"""You are checking a GCSE explainer video (students aged 15-16) against the CORRECTED text of the lesson it was made from.
The lesson text was fact-checked after the video was produced, so the video may still voice the old claims.

LESSON: {row['title']}

CORRECTIONS MADE TO THE LESSON TEXT (old claim -> corrected claim):
{fx}

CORRECTED LESSON TEXT:
{lesson_text[:12000]}

THE GATE - stakes for a GCSE student, not strict accuracy
Grade every stale or contradictory claim as ONE of:
- "mark_affecting": a student who repeated the video's wording in an exam answer would lose a mark, be marked wrong on a question in this lesson, or come away with the wrong date, name, figure, outcome, definition, equation, quotation, cause or sequence for a point the specification examines.
- "pedantry": strictly imprecise or simplified, but accepted at GCSE; no mark scheme would penalise it and the overall story a student takes away is right. Examples: a teletype hotline called a "phone link"; naming one extra minor participant in an event; "weapons technology" for "weapons"; a rounded figure; a simplified mechanism that is the standard school version.
Be honest and calibrated: most simplifications in a 15-16 year old's explainer are pedantry, and regeneration costs real money. Reserve mark_affecting for things that would actually cost marks or teach a wrong fact.

TASKS
1. For each correction listed: does the video (speech or on-screen text) still state the OLD claim, state the CORRECTED claim, or not mention it? Timestamp (mm:ss) and a short quote. If old, grade the stakes.
2. Independently list any other factual statement in the video that contradicts the corrected lesson text (timestamp, quote, what the lesson says), and grade its stakes.
3. regenerate = true ONLY if at least one item is mark_affecting. Otherwise false.

Return ONLY JSON: {{"corrections": [{{"id": "...", "status": "old|corrected|not_mentioned", "timestamp": "mm:ss", "quote": "...", "stakes": "mark_affecting|pedantry|n/a"}}],
"other_contradictions": [{{"timestamp": "mm:ss", "video_says": "...", "lesson_says": "...", "stakes": "mark_affecting|pedantry"}}],
"regenerate": true|false, "reason": "one sentence naming the mark_affecting item(s), or why none"}}"""

t1 = time.time()
video_part = {"type": "video", "uri": vf.uri, "mime_type": vf.mime_type}
if mode == "agentic":
    video_part["processing"] = "agentic"
res = client.interactions.create(model=model, input=[video_part, {"type": "text", "text": prompt}])
t_model = time.time() - t1
dump = res.model_dump() if hasattr(res, "model_dump") else json.loads(json.dumps(res, default=str))


def texts(o):
    if isinstance(o, dict):
        if o.get("type") == "text" and isinstance(o.get("text"), str):
            yield o["text"]
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


out = "\n".join(t for t in texts(dump.get("outputs", dump)) if t and not t.startswith("You are checking"))
ud = dump.get("usage") or {}
inp = (ud.get("total_input_tokens") or 0) + (ud.get("total_tool_use_tokens") or 0)
outp = (ud.get("total_output_tokens") or 0) + (ud.get("total_thought_tokens") or 0)
cost_usd = inp * 0.75 / 1e6 + outp * 3.75 / 1e6
m = re.search(r"\{.*\}", out, re.S)
try:
    verdict = json.loads(m.group(0)) if m else {"raw": out}
except json.JSONDecodeError:
    verdict = {"raw": out}
items = verdict.get("corrections", []) + verdict.get("other_contradictions", [])
result = {"subject": subject, "unit": unit, "lesson": ln, "lesson_id": row["id"], "title": row["title"], "video_url": video_url,
          "mode": mode, "model": model, "video_mb": round(size_mb, 1), "upload_s": round(t_upload, 1), "model_s": round(t_model, 1),
          "usage": ud, "input_tokens": inp, "output_tokens": outp, "cost_usd": round(cost_usd, 4), "cost_p": round(cost_usd * GBP_PER_USD * 100, 2),
          "findings_checked": len(findings), "regenerate": bool(verdict.get("regenerate")), "reason": verdict.get("reason"),
          "mark_affecting": [c for c in items if c.get("stakes") == "mark_affecting"],
          "pedantry": [c for c in items if c.get("stakes") == "pedantry"], "verdict": verdict,
          "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
os.makedirs(os.path.join(udir, "_video"), exist_ok=True)
json.dump(result, open(os.path.join(udir, "_video", f"L{ln}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: result[k] for k in ("lesson", "title", "cost_p", "findings_checked", "regenerate", "reason")}, ensure_ascii=False))
for fn in (lambda: client.files.delete(name=vf.name), lambda: os.remove(vp)):
    try:
        fn()
    except Exception:
        pass
