# -*- coding: utf-8 -*-
"""Single-vote Gemini CONTENT probe: does this recording actually contain the
instruments and features a GCSE listening card would claim? Screening only --
timings come later from the 3-vote probe in probe.py."""
import os, sys, io, json, re, time, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.environ["GEMINI_API_KEY"]
CAND = json.load(io.open(os.path.join(HERE, "ytpick", "candidates.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "ytpick", "screen.json")
prev = json.load(io.open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}


def ask(model, prompt, url):
    body = {"contents": [{"parts": [{"file_data": {"file_uri": url}}, {"text": prompt}]}],
            "generationConfig": {"temperature": 0.2}}
    for _ in range(3):
        try:
            r = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (model, K),
                json=body, timeout=900)
        except Exception:
            time.sleep(20)
            continue
        if r.status_code == 200:
            t = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            m = re.search(r"\{.*\}", t, re.S)
            try:
                return json.loads(m.group(0))
            except Exception:
                return {"raw": t[:900]}
        if r.status_code in (429, 500, 503):
            time.sleep(35)
            continue
        return {"error": r.status_code, "text": r.text[:300]}
    return {"error": "retries exhausted"}


keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(CAND.keys())
for key in keys:
    c = CAND[key]
    if key in prev and "--force" not in sys.argv:
        print("skip", key)
        continue
    prompt = ("Listen to this recording carefully. It is claimed to be: %s\n\n%s\n\n"
              "Answer ONLY as JSON: {\"is_what_is_claimed\": \"yes/no/partly\", \"instruments_heard\": [\"...\"], "
              "\"metre_or_cycle\": \"...\", \"audio_quality\": \"...\", \"spoken_intro\": \"...\", "
              "\"structure_summary\": \"one or two sentences\", \"length\": \"m:ss\", "
              "\"features_confirmed\": [\"...\"], \"features_NOT_heard\": [\"...\"], \"verdict\": \"one sentence\"}"
              % (c["claim"], c["ask"]))
    res = ask("gemini-3-flash-preview", prompt, "https://www.youtube.com/watch?v=" + c["yt"])
    prev[key] = {"yt": c["yt"], "claim": c["claim"], "res": res}
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(prev, indent=1, ensure_ascii=False))
    print("\n== %s (%s)\n%s" % (key, c["yt"], json.dumps(res, ensure_ascii=False)[:1600]))
    sys.stdout.flush()
