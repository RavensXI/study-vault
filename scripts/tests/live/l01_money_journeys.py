# -*- coding: utf-8 -*-
"""Ring 4: read-only smoke of the five money journeys on PRODUCTION, plus
servedBy proving one AI mark ran in London. Run before pushes that touch
these paths and after deploys. Costs a fraction of a penny (one tiny mark).

1. an article lesson loads and renders content
2. a practice lesson loads and renders a problem
3. the join page serves with its code input
4. /teacher/classes is GATED for the unauthenticated
5. the teacher sign-in door serves
+  /api/ai-mark answers and servedBy contains 'bedrock'
"""
import json
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

BASE = "https://www.studyvault.co.uk"
fails = 0


def t(name, cond, detail=""):
    global fails
    if not cond:
        fails += 1
    print(("PASS " if cond else "FAIL ") + name + (" — " + str(detail) if detail != "" else ""))


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 900})

    # 1 — article lesson renders real content
    pg.goto(BASE + "/lesson/psychology-aqa/memory/1", wait_until="domcontentloaded")
    pg.wait_for_timeout(6000)
    body = pg.locator("#study-notes").inner_text() if pg.locator("#study-notes").count() else ""
    t("lesson loads and renders", len(body) > 500, "%d chars" % len(body))

    # 2 — practice lesson renders a problem (maths is always live)
    pg.goto(BASE + "/practice/maths-aqa/number/1", wait_until="domcontentloaded")
    pg.wait_for_timeout(6000)
    card = pg.locator("#current-problem-card")
    t("practice loads and renders a problem",
      card.count() > 0 and len(card.inner_text().strip()) > 10)

    # 3 — join page serves with its code input
    pg.goto(BASE + "/join", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    t("join page serves a code input",
      pg.locator("input").count() >= 1 and "code" in pg.content().lower())

    # 4 — teacher classes is gated when unauthenticated
    pg.goto(BASE + "/teacher/classes", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    gated = pg.locator(".card").count() == 0
    t("teacher classes gated for anonymous", gated,
      "%d class cards visible" % pg.locator(".card").count())

    # 5 — the sign-in door serves
    pg.goto(BASE + "/teacher/login", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    t("teacher login form serves",
      pg.locator("input[type=email], input[type=password]").count() >= 1)
    b.close()

# + servedBy: one tiny mark through the production route, sent from the
# page context — the route is origin-checked, so a bare urllib POST 403s
with sync_playwright() as pw:
    b2 = pw.chromium.launch()
    pg2 = b2.new_page()
    pg2.goto(BASE + "/lesson/psychology-aqa/memory/1", wait_until="domcontentloaded")
    pg2.wait_for_timeout(2500)
    try:
        resp = pg2.evaluate("""async () => {
          const r = await fetch('/api/ai-mark', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              marks: 2,
              system: 'You are a GCSE marker. Reply with a mark out of 2 and one sentence.',
              prompt: 'QUESTION (2 marks): Name the process that turns experience into a ' +
                      'stored memory.\\nSTUDENT ANSWER: encoding',
              free_tier: true })
          });
          return { status: r.status, body: await r.json() };
        }""")
        served = (resp.get("body") or {}).get("servedBy", "")
        t("ai-mark answers", resp["status"] == 200 and bool(resp["body"].get("result")),
          str(resp)[:90])
        t("servedBy proves London", "bedrock" in served, served)
    except Exception as e:
        fails += 1
        print("FAIL ai-mark route — " + str(e)[:100])
    b2.close()

print("l01: %d failure(s)" % fails)
sys.exit(1 if fails else 0)
