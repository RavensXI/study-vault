# -*- coding: utf-8 -*-
"""Museum exhibit 9 and the pack contract: the parents' evening pack renders
from the REAL captured student-pack response; warm-up bars must have distinct
heights when scores differ (the flex bug rendered them identical); the AI
draft renders; print view hides the screen chrome and keeps the pack."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from _helpers import MY_CLASSES, fails, fixture, mock_json, serve_repo, t, teacher_session
from playwright.sync_api import sync_playwright

PORT = 8992
srv = serve_repo(PORT)

DRAFT = {"draft": "A steady term with strong Macbeth recall; Romeo and Juliet "
                  "needs the same regular attention before the exam.",
         "servedBy": "bedrock:eu-west-2", "generated": True}

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1240, "height": 1000})
    teacher_session(pg)
    mock_json(pg, "**/api/teacher/my-classes*", MY_CLASSES)
    mock_json(pg, "**/api/teacher/class-progress*", fixture("real_progress.json"))
    mock_json(pg, "**/api/teacher/student-pack*", fixture("real_pack.json"))
    mock_json(pg, "**/api/teacher/pack-summary*", DRAFT)

    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)[:120]))

    pg.goto("http://127.0.0.1:%d/teacher/classes.html" % PORT, wait_until="networkidle")
    pg.wait_for_timeout(1200)

    t("student names are clickable", pg.locator(".namebtn").count() > 0)
    pg.locator(".namebtn").first.click()
    pg.wait_for_selector(".pack", timeout=8000)
    pg.wait_for_timeout(1200)

    t("pack renders", pg.locator(".pack").count() >= 1)
    t("headline tiles render", pg.locator(".kv div").count() >= 2)
    t("unit bars render", pg.locator(".ubar").count() >= 1)

    heights = pg.eval_on_selector_all(
        ".wubars b", "els => els.map(e => Math.round(e.getBoundingClientRect().height))")
    t("warm-up bars render", len(heights) >= 2, heights)
    t("bar heights DIFFER when scores differ (exhibit 9)",
      len(set(heights)) > 1, heights)

    t("AI draft renders", "Macbeth" in pg.locator("#draftbox").inner_text())

    pg.emulate_media(media="print")
    pg.wait_for_timeout(300)
    t("print: masthead hidden", pg.locator(".top").is_hidden())
    t("print: class bar hidden", pg.locator("#classbar").is_hidden())
    t("print: pack still visible", pg.locator(".pack").is_visible())

    t("zero page errors", not errors, errors[:3])
    b.close()
srv.shutdown()
print("e02: %d failure(s)" % fails())
sys.exit(1 if fails() else 0)
