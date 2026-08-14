# -*- coding: utf-8 -*-
"""Verify cohort-year scoping on the sandbox loaders.

The site lessons are pending_review, so the test rewrites the loaders' REST
calls in-flight (status=eq.live -> status=in.(live,pending_review)) to simulate
the post-approval state without touching the DB."""
import http.server
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox"
PORT = 8936


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, p):
        if p.startswith("/lesson/"):
            return os.path.join(ROOT, "lesson.html")
        if p.startswith("/browse/"):
            return os.path.join(ROOT, "browse.html")
        return super().translate_path(p)

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=httpd.serve_forever, daemon=True).start()


def rewrite(route):
    url = route.request.url
    if "/rest/v1/lessons" in url and "status=eq.live" in url:
        route.continue_(url=url.replace("status=eq.live",
                                        "status=in.%28live%2Cpending_review%29"))
    else:
        route.continue_()


CASES = [
    ("2027 student", "localStorage.setItem('studyvault-exam-year','2027');", None),
    ("2028 student", "localStorage.setItem('studyvault-exam-year','2028');", None),
    ("no year set", "", None),
    ("staff w/ 2028", "localStorage.setItem('studyvault-exam-year','2028');"
        "sessionStorage.setItem('studyvault-auth', JSON.stringify({role:'admin'}));", None),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, init, _ in CASES:
        ctx = b.new_context(viewport={"width": 1400, "height": 950})
        if init:
            ctx.add_init_script(init)
        page = ctx.new_page()
        page.route("**/rest/v1/lessons*", rewrite)
        page.goto("http://127.0.0.1:%d/browse/history-aqa/norman-england" % PORT,
                  wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(2500)
        titles = page.evaluate(
            "[...document.querySelectorAll('.lesson-card h3')].map(e=>e.textContent)")
        has27 = any("Hastings" in t for t in titles)
        has28 = any("White Tower" in t for t in titles)
        print("%-14s browse: %2d lessons  hastings(2027)=%s whitetower(2028)=%s"
              % (name, len(titles), has27, has28))
        # nav check on the same context: from live L12, where does Next go?
        page2 = ctx.new_page()
        page2.route("**/rest/v1/lessons*", rewrite)
        page2.goto("http://127.0.0.1:%d/lesson/history-aqa/norman-england/12" % PORT,
                   wait_until="networkidle", timeout=90000)
        page2.wait_for_timeout(2500)
        nxt = page2.evaluate("""(() => {
            const a=[...document.querySelectorAll('a')].find(x=>/next lesson/i.test(x.textContent));
            return a ? a.getAttribute('href') : null; })()""")
        print("%-14s L12 next -> %s" % ("", nxt))
        ctx.close()
    b.close()
httpd.shutdown()
