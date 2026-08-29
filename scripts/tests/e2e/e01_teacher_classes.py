# -*- coding: utf-8 -*-
"""The consolidated teacher classes screen renders from the real API shapes:
class cards with join codes, the closed badge, the subject picker, and the
class-progress table — with zero page errors. The regression this guards:
the classes page broke three days after its proof script was abandoned."""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from _helpers import MY_CLASSES, fails, fixture, mock_json, serve_repo, t, teacher_session
from playwright.sync_api import sync_playwright

PORT = 8991
srv = serve_repo(PORT)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1240, "height": 1000})
    teacher_session(pg)
    mock_json(pg, "**/api/teacher/my-classes*", MY_CLASSES)
    mock_json(pg, "**/api/teacher/class-progress*", fixture("real_progress.json"))

    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)[:120]))
    pg.on("console", lambda m: errors.append("console.error: " + m.text[:120])
          if m.type == "error" else None)

    pg.goto("http://127.0.0.1:%d/teacher/classes.html" % PORT, wait_until="networkidle")
    pg.wait_for_timeout(1200)

    t("auth gate admits the stored session",
      pg.locator("#auth-gate-loading, .auth-gate, #auth-gate").count() == 0)
    # the consolidated screen: one class bar, a dropdown driving everything
    t("class bar shows", pg.locator("#classbar").is_visible())
    opt_text = " ".join(pg.locator("#classSelect option").all_inner_texts())
    t("dropdown lists all three classes",
      all(n in opt_text for n in ("10L1", "10M2", "11L4")), opt_text[:60])
    codes = pg.locator(".code").all_inner_texts()
    t("selected class shows its join code", any("QENSA9" in c for c in codes), codes)

    # the progress table for the selected class (fixture: 25 real students).
    # .last, not "every tbody" — the screen now carries several tables and a
    # bare row count passed while the student table was empty.
    rows = pg.locator("tbody").last.locator("tr").count()
    t("progress table renders the class", rows == 25, "%d rows" % rows)
    names = pg.locator("tbody").last.inner_text()[:2000]
    t("a student name renders", "Albie" in names)

    # the class-level blocks, all from the same real capture
    body = pg.locator("main").inner_text()
    low = body.lower()
    t("attainment strip renders a real accuracy",
      "recall accuracy" in low and "75%" in body and "over 284 answers" in body)
    t("coverage renders against the started units",
      "where the class has got to" in low and "21 of 28" in body and "Romeo and Juliet" in body)
    t("untouched units are counted, not listed", "26 other units" in body)
    t("weakest lessons render with real titles",
      "weakest lessons" in low and "Act 1: The Feud and the Party" in body)
    t("misconceptions have an honest empty state",
      "No named misconception has been matched" in body)
    t("no study-habit figure reaches the screen",
      not any(w in low for w in ("study hours", "streak", "minutes", "logged in", "homework")))

    # the closed class carries the shut badge once selected
    pg.select_option("#classSelect", index=2)
    pg.wait_for_timeout(900)
    t("closed class carries the shut badge", pg.locator(".shut").count() >= 1)

    t("zero page errors", not errors, errors[:3])
    b.close()
srv.shutdown()
print("e01: %d failure(s)" % fails())
sys.exit(1 if fails() else 0)
