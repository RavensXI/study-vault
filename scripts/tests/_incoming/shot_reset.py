"""Does teacher/login.html switch into recovery mode when a reset link arrives?

Uses a fake recovery fragment. supabase-js will fail to exchange the fake token,
which is exactly why the page must ALSO read the hash directly rather than rely
only on the PASSWORD_RECOVERY event.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
BASE = "http://127.0.0.1:8915/teacher/login.html"

with sync_playwright() as p:
    b = p.chromium.launch()

    # 1. normal visit — must look exactly as before
    pg = b.new_page(viewport={"width": 900, "height": 800})
    pg.goto(BASE, wait_until="networkidle")
    pg.wait_for_timeout(400)
    print("NORMAL VISIT")
    print("  title        :", pg.locator(".card-title").inner_text())
    print("  login form   :", pg.locator("#loginForm").is_visible())
    print("  reset form   :", pg.locator("#resetForm").is_visible(), "(must be False)")
    print("  forgot link  :", pg.locator("#forgotLink").is_visible())

    # 2. arriving from a reset email
    pg2 = b.new_page(viewport={"width": 900, "height": 800})
    pg2.goto(BASE + "#access_token=fake&refresh_token=fake&type=recovery",
             wait_until="networkidle")
    pg2.wait_for_timeout(700)
    print("\nFROM A RESET LINK")
    print("  title        :", pg2.locator(".card-title").inner_text())
    print("  subtitle     :", pg2.locator(".card-subtitle").inner_text())
    print("  reset form   :", pg2.locator("#resetForm").is_visible(), "(must be True)")
    print("  login form   :", pg2.locator("#loginForm").is_visible(), "(must be False)")

    # mismatch check, without touching a real account
    pg2.fill("#newPassword", "abcdefgh")
    pg2.fill("#newPassword2", "different")
    pg2.click("#resetBtn")
    pg2.wait_for_timeout(400)
    print("  mismatch says:", pg2.locator("#resetError").inner_text())

    pg2.fill("#newPassword", "short")
    pg2.fill("#newPassword2", "short")
    pg2.click("#resetBtn")
    pg2.wait_for_timeout(400)
    print("  too short    :", pg2.locator("#resetError").inner_text())

    pg2.screenshot(path=OUT + r"\reset_form.png")
    print("  saved        :", OUT + r"\reset_form.png")
    b.close()
