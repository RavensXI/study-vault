"""Tiny local dev server that mimics Vercel's clean-URL rewrites so the real
StudyVault templates (lesson.html / browse.html / practice.html / guide.html)
render against the sandbox's own css/js + live Supabase content.

Run:  python design-lab/serve.py
Then: http://127.0.0.1:8901/lesson/history-aqa/conflict-tension-first-world-war/5
"""
import http.server
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # worktree root
PORT = 8901

REWRITES = [
    ("/lesson/", "/lesson.html"),
    ("/browse/", "/browse.html"),
    ("/practice/", "/practice.html"),
    ("/guide/", "/guide.html"),
    ("/desk", "/design-lab/dash-desk4.html"),  # Sam's desk (the dashboard)
    ("/classic", "/design-lab/dash-classic.html"),  # the classic (filed) dashboard
    ("/revise", "/revise.html"),  # cross-lesson Leitner review
    ("/bench", "/design-lab/bookbench.html"),  # SVG book workshop (local only)
    ("/shelves", "/design-lab/_shelf_compare.html"),  # coherent vs static comparison
    ("/gold", "/design-lab/gold-lab.html"),  # spine-title gold tuner
    ("/shorts-review", "/design-lab/shorts-review.html"),  # review banked shorts by subject
]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _rewrite(self):
        path = self.path.split("?")[0]
        for prefix, target in REWRITES:
            if path.startswith(prefix):
                # preserve query string for the loader (?sid=, ?tier=, etc.)
                qs = self.path[len(path):]
                self.path = target + qs
                return

    def do_GET(self):
        self._rewrite()
        return super().do_GET()

    def do_HEAD(self):
        self._rewrite()
        return super().do_HEAD()

    def end_headers(self):
        # no-store so CSS/JS edits show on reload (dev only)
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, *args):
        pass  # quiet


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving {ROOT} on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
