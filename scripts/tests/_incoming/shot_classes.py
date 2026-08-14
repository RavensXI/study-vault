"""Render teacher/classes.html with the API mocked.

The mock returns the SHAPE api/teacher/my-classes.js actually returned when I
ran it against the live database (Simon Sutton, two maths classes) rather than
invented data — a screenshot of a layout fed by a shape the server never sends
proves nothing.
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")

MY_CLASSES = {
    "classes": [
        {"id": "c1", "name": "10M1", "yearGroup": 10, "subject": "Mathematics",
         "joinCode": "95FJQ9", "joinOpen": True, "size": 25},
        {"id": "c2", "name": "10M2", "yearGroup": 10, "subject": "Mathematics",
         "joinCode": "8KY3JM", "joinOpen": True, "size": 25},
        {"id": "c3", "name": "11L4 Lit", "yearGroup": 11, "subject": "English Literature",
         "joinCode": "Z8Z2ZZ", "joinOpen": False, "size": 1},
    ],
    "subjects": [
        {"id": "s1", "name": "Business Studies", "own": True},
        {"id": "s2", "name": "Computer Science", "own": True},
        {"id": "s3", "name": "Astronomy", "own": False},
        {"id": "s4", "name": "Mathematics", "own": False},
    ],
}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 1000})

    # admit past the auth gate with a stored staff session
    pg.add_init_script(
        "sessionStorage.setItem('studyvault-auth', JSON.stringify("
        "{role:'teacher', teacher_id:'t1', school_id:null, full_name:'Simon Sutton'}));"
    )
    pg.route("**/api/teacher/my-classes*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(MY_CLASSES)))

    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text)
          if m.type == "error" else None)

    pg.goto("http://127.0.0.1:8913/teacher/classes.html", wait_until="networkidle")
    pg.wait_for_timeout(900)

    gate = pg.locator("#auth-gate-loading, .auth-gate, #auth-gate").count()
    print("auth gate blocking :", gate)
    print("cards rendered     :", pg.locator(".card").count())
    print("codes shown        :", pg.locator(".code").all_inner_texts())
    print("closed badge       :", pg.locator(".shut").count())
    print("subject optgroups  :", pg.locator("#csubject optgroup").count())
    print("subject options    :", pg.locator("#csubject option").count())
    print("page errors        :", errors if errors else "none")

    pg.screenshot(path=OUT + r"\classes_page.png", full_page=True)
    print("saved              :", OUT + r"\classes_page.png")
    b.close()
