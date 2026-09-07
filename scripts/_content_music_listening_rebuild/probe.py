# -*- coding: utf-8 -*-
"""Gemini timing probe for the listening rebuild.
Usage: python probe.py <video_key> [<video_key> ...]
Writes one JSON of the 3 votes per video into probes/<key>.json.
Rule: only STRUCTURAL landmarks (section changes, entries, returns, final chord,
video length) are trusted, and only when 2 of 3 votes agree AND the answer fits
the arithmetic of the score. Timbre identification by machine ear is unreliable.
"""
import os, sys, json, re, io, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "probes"), exist_ok=True)
K = os.environ["GEMINI_API_KEY"]
MODELS = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-3-flash-preview"]

PROBES = json.load(io.open(os.path.join(HERE, "probe_config.json"), encoding="utf-8"))


def build_prompt(cfg):
    qs = "\n".join("%d. %s: %s" % (i + 1, k, d) for i, (k, d) in enumerate(cfg["questions"]))
    keys = ", ".join('"%s": "m:ss"' % k for k, _ in cfg["questions"])
    return (
        "You are listening to this recording: %s\n\n"
        "Listen to the WHOLE video. Report, as mm:ss, the moment each of the following happens IN THIS RECORDING. "
        "If the video has a spoken introduction, titles or applause before the music, say so in intro_before_music. "
        "If an event does not happen in this recording, answer \"none\". Be precise: give the moment the event begins.\n\n%s\n\n"
        "Answer ONLY as JSON: {\"intro_before_music\": \"...\", %s, \"video_length\": \"m:ss\", \"confidence_notes\": \"one sentence\"}"
        % (cfg["piece"], qs, keys)
    )


def ask(model, prompt, url):
    body = {"contents": [{"parts": [{"file_data": {"file_uri": url}}, {"text": prompt}]}],
            "generationConfig": {"temperature": 0.2}}
    for attempt in range(3):
        try:
            r = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (model, K),
                json=body, timeout=900)
        except Exception as e:
            time.sleep(15)
            continue
        if r.status_code == 200:
            # A candidate can come back with no "parts" at all (thinking budget
            # exhausted, or a safety stop). That is a lost vote, not a crash:
            # retry once, then record it so consensus.py counts it as missing.
            try:
                t = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                if attempt < 2:
                    time.sleep(10)
                    continue
                return {"error": "no text part", "raw": json.dumps(r.json())[:400]}
            m = re.search(r"\{.*\}", t, re.S)
            try:
                return json.loads(m.group(0))
            except Exception:
                return {"raw": t[:800]}
        if r.status_code in (429, 500, 503):
            time.sleep(30)
            continue
        return {"error": r.status_code, "text": r.text[:300]}
    return {"error": "retries exhausted"}


for key in sys.argv[1:]:
    cfg = PROBES[key]
    url = "https://www.youtube.com/watch?v=" + cfg["yt"]
    prompt = build_prompt(cfg)
    out = {"yt": cfg["yt"], "piece": cfg["piece"], "questions": cfg["questions"], "votes": {}}
    for i, model in enumerate(cfg.get("models", MODELS)):
        res = ask(model, prompt, url)
        out["votes"]["vote%d_%s" % (i + 1, model)] = res
        print("[%s] vote%d %s: %s" % (key, i + 1, model, json.dumps(res)[:600]))
        sys.stdout.flush()
    io.open(os.path.join(HERE, "probes", key + ".json"), "w", encoding="utf-8").write(
        json.dumps(out, indent=1, ensure_ascii=False))
    print("[%s] written" % key)
    sys.stdout.flush()
