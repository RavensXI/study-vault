"""Reproduce Tom's symptom: the reset form appears, then snaps to the dashboard.

The cause is that the recovery token creates a real session, and the page
redirects anyone who has one. So the test seeds a session AND arrives with a
recovery fragment, then waits longer than the four seconds he counted.
"""
import json, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
BASE = "http://127.0.0.1:8916/teacher/login.html"

SESSION = {
    "access_token": "fake.access.token",
    "token_type": "bearer",
    "expires_in": 3600,
    "expires_at": int(time.time()) + 3600,
    "refresh_token": "fake-refresh",
    "user": {"id": "11111111-2222-3333-4444-555555555555",
             "aud": "authenticated", "role": "authenticated",
             "email": "t.shaun@unity.lancs.sch.uk"},
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 800})
    pg.add_init_script(
        "localStorage.setItem('sb-baipckgywpnwapobwtsy-auth-token', %s);"
        % json.dumps(json.dumps(SESSION)))

    nav = []
    pg.on("framenavigated", lambda f: nav.append(f.url) if f == pg.main_frame else None)

    pg.goto(BASE + "#access_token=fake&refresh_token=fake&type=recovery",
            wait_until="domcontentloaded")

    for t in [1, 3, 5, 7]:
        pg.wait_for_timeout(2000 if t > 1 else 1000)
        try:
            visible = pg.locator("#resetForm").is_visible()
            url = pg.url
        except Exception as e:
            visible, url = "PAGE GONE", str(e)
        print("  t=%ds  reset form visible: %-6s  url: %s" % (t, visible, url.split("/")[-1][:44]))

    print("\nnavigations after load:",
          [u.split('/')[-1][:40] for u in nav[1:]] or "none — stayed put")
    print("still on the login page:", "login.html" in pg.url)
    pg.screenshot(path=OUT + r"\reset_stays.png")
    b.close()
