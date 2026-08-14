# -*- coding: utf-8 -*-
"""Two auth fixes:
 1. Sign out must now appear on admin pages (.admin-nav, not just .header-nav).
 2. A stale staff session with no stored password must trigger an in-place
    re-auth prompt instead of a dead-end 401.
The real 401 path needs Vercel functions, so here we stub /api/pipeline/review
to 401 and /api/auth/login to succeed, and drive the whole flow."""
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"
BASE = "http://127.0.0.1:8901"

# a staff session exactly like the one Tom has: admitted, but NO pw
STALE = """
localStorage.setItem('studyvault-auth', JSON.stringify(
  {role:'admin', teacher_id:'abc', school_id:null, full_name:'Tom Shaun'}));
localStorage.setItem('studyvault-cookie-consent','essential');
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 960})
    pg.add_init_script(STALE)
    errs = []
    pg.on("console", lambda m: errs.append(m.text[:140]) if m.type == "error" else None)

    calls = {"review": 0, "login": 0}

    def review_route(route):
        calls["review"] += 1
        # 401 until the client presents the password, then succeed
        hdr = route.request.headers.get("x-admin-password")
        if hdr == "letmein":
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"lessons": [], "subjects": [], "summary": [], "counts": {}}))
        else:
            route.fulfill(status=401, content_type="application/json",
                          body=json.dumps({"error": "Not authenticated. Log in first."}))

    def login_route(route):
        calls["login"] += 1
        body = route.request.post_data_json or {}
        if body.get("password") == "letmein":
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"role": "admin"}))
        else:
            route.fulfill(status=401, content_type="application/json",
                          body=json.dumps({"error": "Incorrect password"}))

    pg.route("**/api/pipeline/review*", review_route)
    pg.route("**/api/auth/login", login_route)

    pg.goto(BASE + "/admin/review.html", wait_until="load")
    pg.wait_for_timeout(3500)

    print("1) Sign out button on an admin page")
    out = pg.evaluate("""() => {
      const b = document.querySelector('.auth-logout-btn');
      return {present: !!b, parent: b ? b.parentElement.className : null,
              text: b ? b.textContent : null};
    }""")
    print("   ", out)
    ok1 = bool(out["present"]) and "admin-nav" in (out["parent"] or "")

    print("2) Stale session -> re-auth prompt appears")
    prompt = pg.locator("#reauth-pw")
    appeared = prompt.count() > 0 and prompt.is_visible()
    print("    prompt visible:", appeared, "| review calls so far:", calls["review"])
    pg.screenshot(path=OUT + r"\reauth_prompt.png")
    ok2 = appeared

    ok3 = False
    if appeared:
        print("3) Wrong password is rejected, right one unlocks and retries")
        prompt.fill("nope")
        pg.locator("#reauth-go").click()
        pg.wait_for_timeout(900)
        err = pg.locator(".reauth-err")
        print("    error shown:", err.is_visible(), "|", err.inner_text()[:40])
        prompt.fill("letmein")
        pg.locator("#reauth-go").click()
        pg.wait_for_timeout(1800)
        gone = pg.locator("#reauth-pw").count() == 0
        saved = pg.evaluate("""() => {
          const s = JSON.parse(localStorage.getItem('studyvault-auth') || '{}');
          return {hasPw: !!s.pw, role: s.role};
        }""")
        print("    prompt closed:", gone, "| session repaired:", saved,
              "| review calls:", calls["review"], "| login calls:", calls["login"])
        ok3 = gone and saved["hasPw"] and calls["review"] >= 2
        pg.screenshot(path=OUT + r"\reauth_after.png")

    print()
    print("console errors:", errs[:3] or "none")
    print("logout button   :", "PASS" if ok1 else "FAIL")
    print("re-auth prompt  :", "PASS" if ok2 else "FAIL")
    print("unlock + retry  :", "PASS" if ok3 else "FAIL")
    b.close()
