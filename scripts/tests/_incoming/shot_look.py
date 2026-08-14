"""Render the class view, fed by the REAL class-progress response.

real_progress.json was captured by running api/teacher/class-progress.js against
the live database (English Literature class 10L1, 25 students). Rendering a
layout against invented data would prove the layout, not the feature.
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")

REAL = json.load(open(OUT + r"\real_progress.json", encoding="utf-8"))

MY_CLASSES = {
    "classes": [
        {"id": "a54a74db-7622-4ce2-a77a-e741ee35ef98", "name": "10L1", "yearGroup": 10,
         "subject": "English Literature", "joinCode": "QENSA9", "joinOpen": True, "size": 25},
        {"id": "c2", "name": "10L2", "yearGroup": 10, "subject": "English Literature",
         "joinCode": "8KY3JM", "joinOpen": True, "size": 0},
    ],
    "subjects": [{"id": "s1", "name": "English Literature", "own": False}],
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 1100})
    pg.add_init_script(
        "sessionStorage.setItem('studyvault-auth', JSON.stringify("
        "{role:'teacher', teacher_id:'t1', school_id:null, full_name:'Simon Sutton', pw:'x'}));")
    pg.route("**/api/teacher/my-classes*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(MY_CLASSES)))
    pg.route("**/api/teacher/class-progress*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(REAL)))

    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    pg.goto("http://127.0.0.1:8914/teacher/classes.html", wait_until="networkidle")
    pg.wait_for_timeout(700)

    print("empty class says   :", pg.locator(".thin").first.inner_text())
    pg.locator("[data-look]").first.click()
    pg.wait_for_selector("#look table", timeout=5000)
    pg.wait_for_timeout(400)

    print("panel opened       :", pg.locator("#look").count())
    print("tables in panel    :", pg.locator("#look table").count())
    print("missed-item rows   :", pg.locator("#look table").nth(0).locator("tbody tr").count())
    print("student rows       :", pg.locator("#look table").last.locator("tbody tr").count())
    print("first wrong answer :", pg.locator("#look .wrong").first.inner_text())
    print("page errors        :", errs if errs else "none")

    pg.locator("#look").scroll_into_view_if_needed()
    pg.screenshot(path=OUT + r"\class_look.png", full_page=True)
    print("saved              :", OUT + r"\class_look.png")
    b.close()
