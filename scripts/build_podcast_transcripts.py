"""Podcast transcripts for accessibility (Tom, 1 Oct 2026; preview branch podcast-transcripts).

MAI-Transcribe-2 (Microsoft Foundry) turns a lesson's podcast into a speaker-by-speaker transcript,
saved as transcripts/<subject>/<unit>/l<NN>.json and shown under the podcast player on the lesson
page. Lesson audio only, no pupil data. The podcast files are AAC in an .mp3 name, so each is
converted to 16 kHz mono MP3 first.

  python scripts/build_podcast_transcripts.py info                 podcast URLs + glossary for the preview lessons
  python scripts/build_podcast_transcripts.py build                transcribe the preview lessons
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "transcripts")
PREVIEW = [("history-aqa", "elizabethan-england", 2), ("religious-studies-aqa", "judaism-practices", 1),
           ("computer-science-aqa", "data-representation", 2)]


def gv(n):
    return os.environ.get(n) or subprocess.run(["powershell", "-NoProfile", "-Command",
        "[Environment]::GetEnvironmentVariable('%s','User')" % n], capture_output=True, text=True).stdout.strip()


def rest(p):
    U, K = gv("SUPABASE_URL"), gv("SUPABASE_SERVICE_KEY")
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p,
        headers={"apikey": K, "Authorization": "Bearer " + K}), timeout=30).read())


def lesson(s, u, n):
    r = rest("lessons?select=id,title,glossary_terms,related_media,units!inner(slug,subjects!inner(slug,school_id))"
             "&units.slug=eq.%s&units.subjects.slug=eq.%s&units.subjects.school_id=is.null&lesson_number=eq.%d&limit=1" % (u, s, n))[0]
    rm = r["related_media"]; rm = json.loads(rm) if isinstance(rm, str) else (rm or [])
    # the item the lesson page plays (lesson-loader.js: category Podcasts, title "Lesson Podcast")
    pods = [it.get("url") for c in rm if (c.get("category") or "").lower() == "podcasts" for it in c.get("items", [])
            if it.get("title") == "Lesson Podcast" and it.get("url") not in (None, "", "#")]
    terms = [(t.get("term") if isinstance(t, dict) else t) for t in (r.get("glossary_terms") or [])]
    return r["title"], pods, [t for t in terms if t]


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 StudyVault"}), timeout=180).read()


def transcribe(audio, phrases):
    res_name = re.sub(r"^https://([^.]+)\..*$", r"\1", gv("FOUNDRY_ENDPOINT").rstrip("/"))
    url = "https://%s.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15" % res_name
    definition = {"enhancedMode": {"enabled": True, "model": "MAI-Transcribe-2",
                                   "modelOptions": {"transcribeStyle": "clean", "timestamps": "segment"}},
                  "locales": ["en"], "diarization": {"enabled": True}}
    if phrases: definition["phraseList"] = {"phrases": phrases[:100]}
    b = uuid.uuid4().hex
    body = (("--%s\r\nContent-Disposition: form-data; name=\"definition\"\r\n\r\n%s\r\n" % (b, json.dumps(definition))).encode()
            + ("--%s\r\nContent-Disposition: form-data; name=\"audio\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n" % b).encode()
            + audio + ("\r\n--%s--\r\n" % b).encode())
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Ocp-Apim-Subscription-Key": gv("FOUNDRY_KEY"), "Content-Type": "multipart/form-data; boundary=" + b})
    return json.loads(urllib.request.urlopen(req, timeout=900).read())


def to_turns(res):
    """Phrases -> paragraphs: consecutive phrases by the same speaker merge into one turn."""
    phrases = res.get("phrases") or []
    turns = []
    for p in phrases:
        text = (p.get("text") or "").strip()
        if not text: continue
        spk = p.get("speaker")
        start = (p.get("offsetMilliseconds") or 0) / 1000.0
        end = start + (p.get("durationMilliseconds") or 0) / 1000.0
        if turns and turns[-1]["speaker"] == spk and len(turns[-1]["text"]) < 900:
            turns[-1]["text"] += " " + text; turns[-1]["end"] = round(end, 2)
        else:
            turns.append({"speaker": spk, "start": round(start, 2), "end": round(end, 2), "text": text})
    # speakers renumbered 1, 2 in order of first appearance
    order = []
    for t in turns:
        if t["speaker"] not in order: order.append(t["speaker"])
    for t in turns: t["speaker"] = order.index(t["speaker"]) + 1
    return turns


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"
    for s, u, n in PREVIEW:
        title, pods, terms = lesson(s, u, n)
        print("%s/%s/%d %s | %s | %d terms" % (s, u, n, title, pods, len(terms)))
        if cmd != "build" or not pods: continue
        raw = fetch(pods[0])
        tmp = tempfile.mkdtemp()
        src, dst = os.path.join(tmp, "in.m4a"), os.path.join(tmp, "a.mp3")
        open(src, "wb").write(raw)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "16000", "-b:a", "48k", dst], check=True)
        t = time.time()
        res = transcribe(open(dst, "rb").read(), terms)
        dt = time.time() - t
        turns = to_turns(res)
        dur = (res.get("durationMilliseconds") or 0) / 1000.0
        os.makedirs(os.path.join(OUT, s, u), exist_ok=True)
        json.dump({"lesson": title, "audio": pods[0], "model": "MAI-Transcribe-2", "made": time.strftime("%Y-%m-%d"),
                   "speakers": {"1": "Host A", "2": "Host B"}, "turns": turns},
                  open(os.path.join(OUT, s, u, "l%02d.json" % n), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        spk = sorted({x["speaker"] for x in turns})
        print("  -> %d turns, speakers %s, %.0f s audio in %.1f s" % (len(turns), spk, dur, dt))
        if not turns: print("  raw keys:", list(res.keys()), json.dumps(res)[:400])


if __name__ == "__main__":
    main()
