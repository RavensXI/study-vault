# -*- coding: utf-8 -*-
"""Local review server.

Mimics the Vercel rewrites the loaders depend on: /lesson/... serves
lesson.html, /practice/... practice.html, /browse/... browse.html,
/guide/... guide.html. Static files pass straight through.

    python scripts/_dev_rewrite_server.py [port]
"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8919

REWRITES = [("/lesson/", "lesson.html"), ("/practice/", "practice.html"),
            ("/browse/", "browse.html"), ("/guide/", "guide.html")]


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        for prefix, page in REWRITES:
            if self.path.startswith(prefix):
                self.path = "/" + page
                break
        return super().do_GET()

    def log_message(self, *a):
        pass


print("serving", ROOT, "on http://127.0.0.1:%d" % PORT)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
