# -*- coding: utf-8 -*-
"""Local review server for the lesson-widgets branch.

Mimics the Vercel rewrites the loaders depend on: /lesson/... serves
lesson.html, /practice/... practice.html, /browse/... browse.html,
/guide/... guide.html. Static files pass straight through.

    python scripts/_dev_rewrite_server.py [port]
"""
import http.server
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8919

REWRITES = [("/lesson/", "lesson.html"), ("/practice/", "practice.html"),
            ("/browse/", "browse.html"), ("/guide/", "guide.html")]

# Dev-only stand-in for the production /api/exit-cleanup route (which will
# run on Bedrock London like the marking routes). Repairs dictation, never
# improves the answer: the system prompt forbids adding or tidying content.
CLEANUP_SYSTEM = (
    "You repair speech-to-text transcription errors in a GCSE student's "
    "spoken answer. Fix punctuation, capitalisation, false starts, filler "
    "words and phonetically mangled words - use the question for the "
    "correct spelling of names and terms the recogniser misheard. "
    "PRESERVE the student's own wording, sentence order, reasoning and any "
    "factual mistakes exactly. Never add content, never complete a thought, "
    "never improve the answer. Return ONLY the repaired text."
)


def cleanup_transcript(question, transcript):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("no ANTHROPIC_API_KEY")
    body = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 500,
        "temperature": 0,
        "system": CLEANUP_SYSTEM,
        "messages": [{"role": "user", "content":
                      "The question the student was answering:\n" + question +
                      "\n\nRaw transcript of their spoken answer:\n" + transcript}],
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        out = json.load(r)
    return out["content"][0]["text"].strip()


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        for prefix, page in REWRITES:
            if self.path.startswith(prefix):
                self.path = "/" + page
                break
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/exit-cleanup":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n))
            text = cleanup_transcript(data.get("question", ""),
                                      data.get("transcript", ""))
            payload = json.dumps({"text": text}).encode("utf-8")
            self.send_response(200)
        except Exception as e:
            payload = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(502)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *a):
        pass


print("serving", ROOT, "on http://127.0.0.1:%d" % PORT)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
