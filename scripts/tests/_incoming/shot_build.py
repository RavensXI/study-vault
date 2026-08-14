"""Is the build door shown only to a school teacher?

Written with plain named handlers: the previous inline-lambda version blew up
inside Playwright's routing rather than in the page, which looked like a page
failure and was not one.
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
PROG = json.load(open(OUT + r"\real_progress.json", encoding="utf-8"))
URL = "http://127.0.0.1:8921/teacher/classes.html"

CLASSES = [{"id": "a54a74db-7622-4ce2-a77a-e741ee35ef98", "name": "10L1", "yearGroup": 10,
            "subject": "English Literature", "joinCode": "QENSA9", "joinOpen": True, "size": 25}]
SUBJECTS = [{"id": "s1", "name": "English Literature", "own": False}]


def run(canBuild, shot=None):
    body = json.dumps({"canBuild": canBuild, "classes": CLASSES, "subjects": SUBJECTS})
    prog = json.dumps(PROG)

    def on_classes(route):
        route.fulfill(status=200, content_type="application/json", body=body)

    def on_progress(route):
        route.fulfill(status=200, content_type="application/json", body=prog)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 900})
        pg.add_init_script(
            "sessionStorage.setItem('studyvault-auth', JSON.stringify("
            "{role:'teacher',teacher_id:'t1',school_id:null,full_name:'T',pw:'x'}));")
        pg.route("**/api/teacher/my-classes*", on_classes)
        pg.route("**/api/teacher/class-progress*", on_progress)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        pg.goto(URL, wait_until="domcontentloaded")
        # options are never "visible" to Playwright — wait on the DOM instead
        pg.wait_for_function("document.querySelectorAll('#classSelect option').length > 0",
                             timeout=15000)
        pg.wait_for_timeout(900)

        visible = pg.locator("#buildbar").is_visible()
        print("canBuild=%-5s -> build door visible: %-5s | page errors: %s"
              % (canBuild, visible, errs[:1] or "none"))
        if shot and visible:
            print("   heading:", pg.locator("#buildbar h3").inner_text())
            print("   promise:", pg.locator("#buildbar p").inner_text())
            pg.locator("#buildbar").scroll_into_view_if_needed()
            pg.wait_for_timeout(300)
            pg.screenshot(path=shot)
            print("   saved  :", shot)
        b.close()


run(True, OUT + r"\build_door.png")
run(False)
