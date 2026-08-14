"""The whole student experience: answer wrongly on the LIVE site and see the
authored diagnosis appear.

Drives production practice as a student would: start the tier, wait for a
multiple-choice problem, deliberately pick a wrong option that HAS a diagnosis
(known from the DB by option text, since display order is shuffled), press
Check Answer, and confirm 'It looks like what happened' shows the authored
message. Pixel proof, not DOM faith.
"""
import json
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = (r"C:\Users\tshau\AppData\Local\Temp\claude"
       r"\C--Users-tshau-Documents-Study-Vault"
       r"\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}
TAGS = re.compile(r"<[^>]+>")


def get(p):
    r = urllib.request.Request(URL + "/rest/v1/" + p, headers=H)
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


# Build a lookup: for every MC problem in L1, the TEXT of each diagnosed wrong
# option -> its message. Display shuffles, so text is the only stable handle.
subj = get("subjects?select=id&slug=eq.english-language-aqa")[0]
unit = get("units?select=id&subject_id=eq.%s&slug=eq.paper-1-reading" % subj["id"])[0]
les = get("lessons?select=practice_data&unit_id=eq.%s&lesson_number=eq.1" % unit["id"])[0]
pb = les["practice_data"]["problem_bank"]

diagnosed = {}      # plain option text -> (id, message)
for tier in ("bronze", "silver", "gold"):
    for p in pb.get(tier) or []:
        if p.get("input_type") != "multiple_choice":
            continue
        for m in p.get("misconceptions") or []:
            opts = p.get("options") or []
            if isinstance(m.get("expect"), int) and 0 <= m["expect"] < len(opts):
                key = TAGS.sub("", opts[m["expect"]]).strip()
                diagnosed[key] = (m["id"], m["message"])
print("diagnosed wrong options in L1:", len(diagnosed))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 950})
    pg.goto("https://www.studyvault.co.uk/practice/english-language-aqa/paper-1-reading/1",
            wait_until="domcontentloaded")
    pg.wait_for_timeout(4000)

    # The real student journey has three doors before a problem appears:
    # the method-card modal, the worked-example phase, then the tier intro.
    for label in ("Got it, let's practise!", "Jump ahead to Practice"):
        try:
            btn = pg.get_by_text(label, exact=False).first
            if btn.count():
                btn.click()
                pg.wait_for_timeout(1400)
        except Exception:
            pass
    try:
        btn = pg.locator("#tier-intro-btn")
        if btn.count() and btn.is_visible():
            btn.click()
            pg.wait_for_timeout(1200)
    except Exception:
        pass

    # a first-run tour tooltip floats over the page; step past it
    for _ in range(4):
        try:
            nb = pg.get_by_role("button", name="Next").first
            if nb.count() and nb.is_visible():
                nb.click(); pg.wait_for_timeout(500)
            else:
                break
        except Exception:
            break

    hit = False
    for attempt in range(22):
        opts = pg.locator(".mc-option")
        if opts.count() == 0:
            # the shuffle dealt a non-MC type; a reload is a fresh deal, and
            # the intro doors remember they have been opened
            pg.reload(wait_until="domcontentloaded")
            pg.wait_for_timeout(2500)
            for label in ("Got it, let's practise!", "Jump ahead to Practice"):
                try:
                    btn = pg.get_by_text(label, exact=False).first
                    if btn.count():
                        btn.click(); pg.wait_for_timeout(1000)
                except Exception:
                    pass
            for _ in range(3):
                try:
                    nb = pg.get_by_role("button", name="Next").first
                    if nb.count() and nb.is_visible():
                        nb.click(); pg.wait_for_timeout(400)
                    else:
                        break
                except Exception:
                    break
            continue
        if False:
            # not an MC problem — answer the visible input wrongly to advance,
            # or use whatever advance control exists
            try:
                box = pg.locator("#problem-input-a")
                if box.count() and box.is_visible():
                    box.fill("0")
                    pg.locator("#problem-check-btn").click()
                    pg.wait_for_timeout(900)
                    nxt = pg.locator("#problem-check-btn")
                    if nxt.count():
                        nxt.click()          # becomes Next after feedback
                        pg.wait_for_timeout(900)
                    continue
            except Exception:
                pass
            pg.wait_for_timeout(800)
            continue

        # an MC problem is up: find a displayed option whose text is diagnosed
        texts = opts.all_inner_texts()
        pick = None
        for j, txt in enumerate(texts):
            clean = re.sub(r"^[A-D]\s*", "", txt.strip().replace("\n", " ")).strip()
            for key in diagnosed:
                if key and key in clean:
                    pick = (j, key)
                    break
            if pick:
                break
        if not pick:
            # MC problem from another lesson pull? choose any option to advance
            opts.nth(0).click()
            pg.locator("#problem-check-btn").click()
            pg.wait_for_timeout(900)
            pg.locator("#problem-check-btn").click()
            pg.wait_for_timeout(900)
            continue

        j, key = pick
        opts.nth(j).click()
        pg.wait_for_timeout(300)
        pg.locator("#problem-check-btn").click()
        pg.wait_for_timeout(1200)

        tip = pg.locator(".misconception-tip")
        if tip.count() and "It looks like what happened" in tip.inner_text():
            print("DIAGNOSIS SHOWN for wrong answer %r" % key[:50])
            print("  tag/message expected:", diagnosed[key][0])
            print("  on screen:", tip.inner_text()[:160])
            pg.screenshot(path=OUT + r"\live_misconception.png")
            print("  screenshot:", OUT + r"\live_misconception.png")
            hit = True
            break
        else:
            print("picked %r but no authored tip; advancing" % key[:40])
            pg.locator("#problem-check-btn").click()
            pg.wait_for_timeout(800)

    if not hit:
        pg.screenshot(path=OUT + r"\live_misconception_fail.png")
        print("NO diagnosis reached in 18 attempts — see live_misconception_fail.png")
    b.close()
