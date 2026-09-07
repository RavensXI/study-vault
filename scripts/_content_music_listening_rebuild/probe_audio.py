# -*- coding: utf-8 -*-
"""Gemini timing probe for R2-hosted audio lessons (the sv-ap-wave dock).

Same 3-vote rule as probe.py, but the recording is fed as inline_data rather
than a YouTube file_uri, following the pattern proven in
scripts/music-practice/works_verify.py: download the real R2 mp3 once, clip the
window with ffmpeg, base64 it, send it with mime_type audio/mp3.

Whole-file mode gives absolute timings. Window mode (--win start end) asks about
a narrow clip and adds the offset back, for events the whole-file pass split on.

Usage: python probe_audio.py <key> [--win START END]
"""
import base64, io, json, os, re, subprocess, sys, time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, "_audio")
os.makedirs(TMP, exist_ok=True)
os.makedirs(os.path.join(HERE, "probes"), exist_ok=True)
K = os.environ["GEMINI_API_KEY"]
API = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
MODELS = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-3-flash-preview"]

CFG = json.load(io.open(os.path.join(HERE, "probe_audio_config.json"), encoding="utf-8"))


def fetch(url, dest):
    if os.path.exists(dest):
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
        f.write(r.read())
    print("downloaded %s (%d KB)" % (os.path.basename(dest), os.path.getsize(dest) // 1024))
    return dest


def clip(src, start, end, dest):
    if os.path.exists(dest):
        return dest
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-to", str(end),
                    "-i", src, "-c:a", "libmp3lame", "-b:a", "96k", dest], check=True)
    return dest


def ask(model, b64, prompt):
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": b64}},
                                    {"text": prompt}]}],
            "generationConfig": {"temperature": 0.2}}
    for attempt in range(3):
        try:
            req = urllib.request.Request(API % (model, K), data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as r:
                out = json.load(r)
            t = out["candidates"][0]["content"]["parts"][0]["text"]
            m = re.search(r"\{.*\}", t, re.S)
            try:
                return json.loads(m.group(0))
            except Exception:
                return {"raw": t[:800]}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < 2:
                time.sleep(30)
                continue
            return {"error": e.code, "text": e.read()[:300].decode("utf-8", "replace")}
        except Exception as e:
            if attempt < 2:
                time.sleep(20)
                continue
            return {"error": str(e)[:200]}


key = sys.argv[1]
win = None
if "--win" in sys.argv:
    j = sys.argv.index("--win")
    win = (float(sys.argv[j + 1]), float(sys.argv[j + 2]))
cfg = CFG[key]
src = fetch(cfg["audio"], os.path.join(TMP, key + ".mp3"))
if win:
    path = clip(src, win[0], win[1], os.path.join(TMP, "%s_%g-%g.mp3" % (key, win[0], win[1])))
    scope = ("This is a CLIP taken from %g seconds into the recording. Give every time as mm:ss measured "
             "FROM THE START OF THIS CLIP." % win[0])
    outkey = "%s_w%g" % (key, win[0])
else:
    path = src
    scope = "This is the complete recording. Give every time as mm:ss from the start."
    outkey = key

qs = "\n".join("%d. %s: %s" % (i + 1, k, dsc) for i, (k, dsc) in enumerate(cfg["questions"]))
keys = ", ".join('"%s": "m:ss"' % k for k, _ in cfg["questions"])
prompt = ("You are listening to this recording: %s\n\n%s\n\nListen to the WHOLE audio and report, as mm:ss, "
          "the moment each of the following happens. If an event does not happen, answer \"none\". Be precise: "
          "give the moment the event begins.\n\n%s\n\nAnswer ONLY as JSON: {%s, \"audio_length\": \"m:ss\", "
          "\"confidence_notes\": \"one sentence\"}" % (cfg["piece"], scope, qs, keys))

b64 = base64.b64encode(open(path, "rb").read()).decode()
print("[%s] %.1f MB of audio, %d questions" % (outkey, len(b64) * 0.75 / 1e6, len(cfg["questions"])))
out = {"audio": cfg["audio"], "piece": cfg["piece"], "questions": cfg["questions"],
       "window": win, "votes": {}}
for i, model in enumerate(MODELS):
    res = ask(model, b64, prompt)
    if win:
        for k2, v in list(res.items()):
            if isinstance(v, str) and re.match(r"^\d+:\d{2}$", v.strip()):
                mm, ss = v.strip().split(":")
                res[k2 + "_abs"] = "%d:%02d" % divmod(int(mm) * 60 + int(ss) + int(win[0]), 60)
    out["votes"]["vote%d_%s" % (i + 1, model)] = res
    print("[%s] vote%d %s: %s" % (outkey, i + 1, model, json.dumps(res)[:600]))
    sys.stdout.flush()
io.open(os.path.join(HERE, "probes", outkey + ".json"), "w", encoding="utf-8").write(
    json.dumps(out, indent=1, ensure_ascii=False))
print("[%s] written" % outkey)
