"""Does the teacher shell narrow the review page — and leave admin alone?

The second half matters as much as the first. Getting the role test backwards
would strip Tom's own console.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
URL = "http://127.0.0.1:8922/admin/review.html"


def look(role, shot):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 860})
        pg.add_init_script(
            "localStorage.setItem('studyvault-auth', JSON.stringify("
            "{role:'%s', teacher_id:'t1', school_id:'s1', full_name:'T', pw:'x'}));"
            "sessionStorage.setItem('studyvault-auth', JSON.stringify("
            "{role:'%s', teacher_id:'t1', school_id:'s1', full_name:'T', pw:'x'}));" % (role, role))
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL, wait_until="domcontentloaded")
        pg.wait_for_timeout(1800)

        staff = pg.evaluate("document.body.getAttribute('data-staff')")
        links = pg.eval_on_selector_all(".admin-nav a", "els=>els.map(e=>e.textContent.trim())")
        groups = pg.eval_on_selector_all(
            ".admin-nav-group", "els=>els.filter(e=>getComputedStyle(e).display!=='none').length")
        bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
        btns = pg.eval_on_selector_all(
            "#batch-approve,#batch-publish,#batch-reject",
            "els=>els.filter(e=>getComputedStyle(e).display!=='none').map(e=>e.textContent.trim())")

        print("role=%-13s data-staff=%-8s nav=%s" % (role, staff, links))
        print("   console menus visible: %s | body bg: %s | errors: %s"
              % (groups, bg, errs[:1] or "none"))
        print("   bulk actions offered : %s" % btns)
        pg.screenshot(path=shot)
        b.close()


look("teacher", OUT + r"\shell_teacher.png")
look("admin", OUT + r"\shell_admin.png")
