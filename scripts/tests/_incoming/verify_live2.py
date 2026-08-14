"""Live proof, walking the REAL bronze path: sorter, highlighter, then the MC.

Problem order is authored, not shuffled — bronze is always traffic_light,
highlight_evidence, multiple_choice. So the driver answers the first two like
a (careless) student and reaches the MC on rails, then deliberately picks a
diagnosed wrong option and photographs the authored diagnosis.
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


subj = get("subjects?select=id&slug=eq.english-language-aqa")[0]
unit = get("units?select=id&subject_id=eq.%s&slug=eq.paper-1-reading" % subj["id"])[0]
les = get("lessons?select=practice_data&unit_id=eq.%s&lesson_number=eq.1" % unit["id"])[0]
bronze = les["practice_data"]["problem_bank"]["bronze"]
mc = next(p for p in bronze if p.get("input_type") == "multiple_choice")
correct_idx = mc["solutions"][0]
by_text = {}
for m in mc.get("misconceptions") or []:
    by_text[TAGS.sub("", mc["options"][m["expect"]]).strip()] = m
print("target MC:", TAGS.sub(" ", mc.get("question") or "")[:70])
print("diagnosed wrong options:", list(by_text.keys()))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 950})
    pg.goto("https://www.studyvault.co.uk/practice/english-language-aqa/paper-1-reading/1",
            wait_until="domcontentloaded")
    pg.wait_for_timeout(4500)

    for label in ("Got it, let's practise!", "Jump ahead to Practice"):
        try:
            btn = pg.get_by_text(label, exact=False).first
            if btn.count():
                btn.click()
                pg.wait_for_timeout(1300)
        except Exception:
            pass
    for _ in range(4):
        try:
            nb = pg.get_by_role("button", name="Next").first
            if nb.count() and nb.is_visible():
                nb.click()
                pg.wait_for_timeout(500)
            else:
                break
        except Exception:
            break

    def click_visible(cands):
        # .first can land on a hidden node earlier in the DOM; check EVERY match
        for sel in cands:
            try:
                loc = pg.locator(sel)
                for k in range(loc.count()):
                    el = loc.nth(k)
                    if el.is_visible():
                        el.click(timeout=4000)
                        return "%s[%d]" % (sel, k)
            except Exception:
                continue
        return None

    def check_and_next(tag):
        click_visible(["#problem-check-btn"])
        pg.wait_for_timeout(1300)
        pg.screenshot(path=OUT + r"\journey_%s.png" % tag)
        # whatever the advance control is this run: the same button relabelled,
        # or a separate next/continue
        used = click_visible(["button:has-text('Next Problem')",
                              "#problem-check-btn",
                              "button:has-text('Continue')"])
        print("  advanced after %s via %s" % (tag, used))
        pg.wait_for_timeout(1300)

    # generic walk: answer whatever is on screen, advance, stop at the MC
    hit=False
    for step in range(12):
        pg.wait_for_timeout(900)
        mc=pg.locator(".mc-option")
        tl=pg.locator(".tl-stmt")
        hl=pg.locator("#hl-passage-area")
        if mc.count():
            picked=None
            for j,txt in enumerate(mc.all_inner_texts()):
                clean=re.sub(r"\s+"," ",TAGS.sub("",txt)).strip()
                clean=re.sub(r"^[A-D]\s*","",clean)
                for key in by_text:
                    if key and key in clean:
                        picked=(j,key);break
                if picked:break
            if not picked:
                # an MC without one of L1's diagnosed options — answer and move on
                mc.nth(0).click();pg.wait_for_timeout(250)
                click_visible(["#problem-check-btn"]);pg.wait_for_timeout(1100)
                click_visible(["button:has-text('Next Problem')","#problem-check-btn"])
                continue
            j,key=picked
            mc.nth(j).click();pg.wait_for_timeout(300)
            click_visible(["#problem-check-btn"]);pg.wait_for_timeout(1400)
            tip=pg.locator(".misconception-tip")
            ok=tip.count() and "It looks like what happened" in tip.first.inner_text()
            print("DIAGNOSIS VISIBLE:",bool(ok))
            if ok:
                print("  authored id :",by_text[key]["id"])
                print("  on screen   :",re.sub(r"\s+"," ",tip.first.inner_text())[:170])
            pg.screenshot(path=OUT+r"\live_misconception.png")
            print("  screenshot  :",OUT+r"\live_misconception.png")
            hit=True
            break
        if tl.count():
            for i in range(tl.count()):
                try: tl.nth(i).locator(".tl-btn").first.click(timeout=2000)
                except Exception: pass
                pg.wait_for_timeout(90)
        elif hl.count():
            words=hl.locator("span")
            if words.count()>=2:
                try:
                    words.nth(0).hover();pg.mouse.down()
                    words.nth(min(3,words.count()-1)).hover();pg.mouse.up()
                except Exception: pass
                pg.wait_for_timeout(250)
        else:
            # unknown type: click the first plausible interactive thing
            for sel in (".connotation-word",".em-claim",".ms-option",".reorder-item","button.eng-opt"):
                loc=pg.locator(sel)
                if loc.count():
                    try: loc.first.click(timeout=1500)
                    except Exception: pass
                    break
        click_visible(["#problem-check-btn"])
        pg.wait_for_timeout(1200)
        adv=click_visible(["button:has-text('Next Problem')","#problem-check-btn"])
        print("  step %d advanced via %s"%(step,adv))
        if not adv:
            pg.screenshot(path=OUT+r"\journey_stuck_%d.png"%step)
            print("  stuck at step",step)
            break
    if not hit:
        pg.screenshot(path=OUT+r"\journey_mc_fail.png")
        print("walk ended without reaching a diagnosed MC")
    b.close()
