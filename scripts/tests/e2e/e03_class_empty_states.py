# -*- coding: utf-8 -*-
"""A class with no evidence must say so, not print zeroes.

The regression this guards is the one that matters most on a teacher screen: a
practice-first course carries no knowledge check at all, so every attainment
panel is legitimately blank. The old prototype dashboard filled exactly that
gap with invented numbers. A blank that a teacher cannot tell apart from a
broken page is nearly as bad — so each empty panel has to explain itself.

Fixtures are real captures from api/teacher/class-progress:
  practice_progress.json      10M1 maths — a real roll, zero quiz evidence
  misconception_progress.json the misconception table with rows in it (the
                              live misconception rows are all in a subject no
                              class studies, so the populated render path can
                              only be proved from a spliced capture)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from _helpers import MY_CLASSES, fails, fixture, serve_repo, t, teacher_session
from playwright.sync_api import sync_playwright

PORT = 8993
LIT = fixture("real_progress.json")
BY_ID = {LIT["class"]["id"]: LIT,
         "c2": fixture("practice_progress.json"),
         "c3": fixture("misconception_progress.json")}

srv = serve_repo(PORT)


def route(r):
    url = r.request.url
    cid = url.split("class_id=")[-1].split("&")[0] if "class_id=" in url else ""
    r.fulfill(status=200, content_type="application/json",
              body=json.dumps(BY_ID.get(cid, LIT)))


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 1100})
    teacher_session(pg)
    pg.route("**/api/teacher/my-classes*", lambda r: r.fulfill(
        status=200, content_type="application/json", body=json.dumps(MY_CLASSES)))
    pg.route("**/api/teacher/class-progress*", route)

    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)[:160]))
    pg.on("console", lambda m: errors.append("console.error: " + m.text[:160])
          if m.type == "error" else None)

    pg.goto("http://127.0.0.1:%d/teacher/classes.html" % PORT, wait_until="networkidle")
    pg.wait_for_timeout(1200)

    # ---- the practice-first class ----------------------------------------
    pg.select_option("#classSelect", value="c2")
    pg.wait_for_timeout(900)
    body = pg.locator("main").inner_text()
    low = body.lower()

    t("recall accuracy is a dash, never a 0%", "—" in body and "0%" not in body.split("PRACTICE")[0])
    t("the blank accuracy says why", "no quiz answers yet" in body)
    t("nobody is claimed to have been quizzed", "0 of 25" in body)
    t("weakest lessons explains the practice format",
      "practice-first" in body and "no knowledge-check quiz" in body)
    t("the wrong-questions panel is honestly empty",
      "Nothing yet that two or more of them missed" in body)
    t("the misconception panel says nothing was matched, not that nothing happened",
      "No named misconception has been matched" in body)
    t("coverage still reports real progress",
      "where the class has got to" in low and "Algebra" in body and "14 of 14" in body)
    t("practice units are labelled as such", "practice" in low)
    t("the roll is still shown in full", body.count("over a month") >= 25,
      body.count("over a month"))

    # ---- the populated misconception table --------------------------------
    pg.select_option("#classSelect", value="c3")
    pg.wait_for_timeout(900)
    body = pg.locator("main").inner_text()
    t("misconception rows render when there are any",
      "confuse clarinet trumpet" in body)
    t("misconception rows name where the error happens",
      "aos listening" in body.lower())

    t("zero page errors", not errors, errors[:3])
    b.close()

srv.shutdown()
print("e03: %d failure(s)" % fails())
sys.exit(1 if fails() else 0)
