"""Render /join: the signed-out path and the success path."""
import json, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
URL = "http://127.0.0.1:8923/join.html"

SESSION = {"access_token": "tok", "token_type": "bearer", "expires_in": 3600,
           "expires_at": int(time.time()) + 3600, "refresh_token": "r",
           "user": {"id": "u1", "aud": "authenticated", "role": "authenticated",
                    "email": "student@example.com"}}
JOINED = {"joined": True, "alreadyIn": False,
          "class": {"id": "c1", "name": "10L1", "subject": "English Literature",
                    "teacher": "Tom Shaun"},
          "visibility": "Tom Shaun will be able to see how you get on in English "
                        "Literature — your scores, and which questions you find hard. "
                        "They cannot see when you revise, your flashcard settings, or "
                        "anything from your other subjects."}

with sync_playwright() as p:
    b = p.chromium.launch()

    # A: signed out — typing a code and submitting must show the way in, and keep the code
    pg = b.new_page(viewport={"width": 900, "height": 820})
    pg.goto(URL, wait_until="domcontentloaded")
    pg.wait_for_timeout(600)
    pg.fill("#code", "abc234")
    pg.click("#joinBtn")
    pg.wait_for_timeout(600)
    print("A. SIGNED OUT")
    print("   uppercased      :", pg.input_value("#code"))
    print("   sign-in note    :", pg.locator("#signinNote").is_visible(), "(must be True)")
    print("   code kept       :", pg.evaluate("localStorage.getItem('sv-join-code')"))
    pg.screenshot(path=OUT + r"\join_signedout.png")
    pg.close()

    # B: signed in — code survives the round trip, join succeeds
    pg2 = b.new_page(viewport={"width": 900, "height": 820})
    pg2.add_init_script(
        "localStorage.setItem('sb-baipckgywpnwapobwtsy-auth-token', %s);"
        "localStorage.setItem('sv-join-code','ABC234');" % json.dumps(json.dumps(SESSION)))
    pg2.route("**/api/class/join", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(JOINED)))
    errs = []
    pg2.on("pageerror", lambda e: errs.append(str(e)))
    pg2.goto(URL, wait_until="domcontentloaded")
    pg2.wait_for_timeout(700)
    print("\nB. SIGNED IN, code pre-filled from the round trip")
    print("   pre-filled      :", pg2.input_value("#code"))
    pg2.click("#joinBtn")
    pg2.wait_for_timeout(700)
    print("   joined panel    :", pg2.locator(".card.joined").count() == 1)
    print("   class line      :", pg2.locator(".what").inner_text())
    print("   visibility      :", pg2.locator(".visibility").inner_text()[:70] + "...")
    print("   code cleared    :", pg2.evaluate("localStorage.getItem('sv-join-code')") is None)
    print("   page errors     :", errs if errs else "none")
    pg2.screenshot(path=OUT + r"\join_success.png")
    b.close()
