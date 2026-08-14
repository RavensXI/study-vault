"""Screenshot the 'With your school' shelf on welcome.html.

The live-Chrome route cannot do this: Page.captureScreenshot freezes on this page
under CDP (already recorded in memory for the wizard and planner). Playwright
drives its own browser, so it is unaffected.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 950})
    pg.goto("http://127.0.0.1:8912/welcome.html", wait_until="networkidle")

    sec = pg.locator(".sec-schools")
    sec.scroll_into_view_if_needed()
    pg.wait_for_timeout(1400)          # let the reveal animation settle

    link = pg.locator(".signinline a")
    print("link count      :", link.count())
    print("link text       :", link.first.inner_text())
    print("link href       :", link.first.get_attribute("href"))
    print("link visible    :", link.first.is_visible())

    sec.screenshot(path=OUT + r"\schools_shelf.png")
    print("saved           :", OUT + r"\schools_shelf.png")

    # also prove the link goes somewhere real once rewritten by Vercel
    pg.goto("http://127.0.0.1:8912/teacher/login.html", wait_until="domcontentloaded")
    print("teacher/login   :", pg.title())
    b.close()
