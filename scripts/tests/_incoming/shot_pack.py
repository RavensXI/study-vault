"""Render the parents' evening pack, fed by the REAL student-pack response."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")

PROG = json.load(open(OUT + r"\real_progress.json", encoding="utf-8"))
PACK = json.load(open(OUT + r"\real_pack.json", encoding="utf-8"))
MY = {"classes": [{"id": "a54a74db-7622-4ce2-a77a-e741ee35ef98", "name": "10L1",
                   "yearGroup": 10, "subject": "English Literature",
                   "joinCode": "QENSA9", "joinOpen": True, "size": 25}],
      "subjects": [{"id": "s1", "name": "English Literature", "own": False}]}
DRAFT = {"draft": "Charlie has engaged with revision on only two days in the last four weeks, "
                  "which is a concern given the GCSE is approaching. The evidence we have is "
                  "limited but encouraging: he achieved perfect recall on Macbeth questions, "
                  "demonstrating he can master the material when he does revise. To build a "
                  "fuller picture across both texts, Charlie would benefit most from regular "
                  "revision on Romeo and Juliet.",
         "servedBy": "bedrock:eu-west-2", "generated": True}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1240, "height": 1000})
    pg.add_init_script("sessionStorage.setItem('studyvault-auth', JSON.stringify("
                       "{role:'teacher',teacher_id:'t1',school_id:null,full_name:'T',pw:'x'}));")
    pg.route("**/api/teacher/my-classes*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(MY)))
    pg.route("**/api/teacher/class-progress*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(PROG)))
    pg.route("**/api/teacher/student-pack*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(PACK)))
    pg.route("**/api/teacher/pack-summary*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(DRAFT)))

    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:8919/teacher/classes.html", wait_until="networkidle")
    pg.wait_for_timeout(1000)

    print("student name is clickable :", pg.locator(".namebtn").count() > 0)
    pg.locator(".namebtn").first.click()
    pg.wait_for_selector(".pack", timeout=6000)
    pg.wait_for_timeout(1200)

    print("pack rendered   :", pg.locator(".pack").count())
    print("headline tiles  :", pg.locator(".kv div").all_inner_texts())
    print("unit bars       :", pg.locator(".ubar").count())
    print("warm-up bars    :", pg.locator(".wubars i").count())
    hs=pg.eval_on_selector_all(".wubars b","els=>els.map(e=>Math.round(e.getBoundingClientRect().height))")
    print("bar heights     :", hs, "distinct:", len(set(hs)))
    print("draft text      :", pg.locator("#draftbox").inner_text()[:70])
    print("draft footnote  :", pg.locator("#draftfoot").inner_text())
    print("errors          :", errs if errs else "none")

    pg.screenshot(path=OUT + r"\pack_screen.png", full_page=True)

    # what actually comes out of the printer
    pg.emulate_media(media="print")
    pg.wait_for_timeout(250)
    print("print: masthead hidden :", pg.locator(".top").is_hidden())
    print("print: classbar hidden :", pg.locator("#classbar").is_hidden())
    print("print: pack visible    :", pg.locator(".pack").is_visible())
    pg.screenshot(path=OUT + r"\pack_print.png", full_page=True)
    print("saved                  :", OUT + r"\pack_print.png")
    b.close()
