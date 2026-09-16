"""Verify the mitosis animation in installed Chrome and save the proof frames.

Serve the repo first, then run this:

    python _dev_server.py                  # http://127.0.0.1:8904
    python animations/mitosis/verify.py

It checks that every clip loads, that each scene is exactly its clip plus
the beat, that playback advances with the audio, that the scrub jumps
scenes, that reduced motion still renders, and that the console is clean.
Nineteen frames plus a poster, a phone width and a reduced-motion frame go
to animations/mitosis/proof/.
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8904/animations/mitosis/index.html"
OUT = Path(__file__).resolve().parent / "proof"
OUT.mkdir(parents=True, exist_ok=True)
SHOT = {"type": "jpeg", "quality": 88}

# (scene index, progress through the clip, file name)
MOMENTS = [
    (0, 1.00, "01-tissue"),
    (1, 1.00, "02-neighbours-dividing"),
    (2, 1.00, "03-wound-closing"),
    (3, 0.58, "04-slate-cell-cycle"),
    (4, 0.80, "05-labelled-cell"),
    (5, 0.86, "06-slate-46-chromosomes"),
    (6, 0.82, "07-two-pairs"),
    (7, 0.84, "08-growth"),
    (8, 0.55, "09-slate-copy-drawing-on"),
    (8, 1.00, "10-slate-copy-joined"),
    (9, 1.00, "11-slate-two-copies"),
    (10, 1.00, "12-slate-identical"),
    (11, 0.60, "13-envelope-breaking"),
    (12, 0.92, "14-slate-spindle"),
    (13, 0.80, "15-lined-up-at-the-equator"),
    (14, 0.48, "16-chromatids-separating"),
    (15, 0.86, "17-two-nuclei"),
    (16, 0.78, "18-furrow"),
    (17, 1.00, "19-two-identical-cells"),
]


def main():
    errs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1300, "height": 980})
        msgs = []
        pg.on("console", lambda m: msgs.append((m.type, m.text)))
        pg.on("pageerror", lambda e: msgs.append(("pageerror", str(e))))
        failed = []
        pg.on("requestfailed", lambda r: failed.append(r.url + " :: " + str(r.failure)))
        pg.on("response", lambda r: failed.append("HTTP %d %s" % (r.status, r.url)) if r.status >= 400 else None)

        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_function("window.__mitosis && window.__mitosis.ready", timeout=20000)
        pg.wait_for_timeout(900)   # let the webfonts land

        info = pg.evaluate("() => ({scenes: window.__mitosis.scenes, total: window.__mitosis.total, "
                           "beat: window.__mitosis.beat, errors: window.__mitosis.errors, "
                           "reduced: window.__mitosis.reduced})")

        print("total %.2fs  beat %.2fs  reduced=%s  load errors=%s"
              % (info["total"], info["beat"], info["reduced"], info["errors"]))
        print("%-3s %-10s %8s %8s %8s %6s" % ("#", "key", "clip", "scene", "audioDur", "rs"))
        for s in info["scenes"]:
            ad = s["audioDuration"]
            ok_clip = abs(s["scene"] - s["clip"] - info["beat"]) < 0.002
            ok_audio = ad is not None and abs(ad - s["clip"]) < 0.06
            ok_ready = s["readyState"] >= 1
            print("%-3d %-10s %8.2f %8.2f %8.2f %6d %s%s%s"
                  % (s["n"], s["key"], s["clip"], s["scene"], ad or -1, s["readyState"],
                     "" if ok_clip else " CLIP-MISMATCH",
                     "" if ok_audio else " AUDIO-MISMATCH",
                     "" if ok_ready else " NOT-LOADED"))
            if not (ok_clip and ok_audio and ok_ready):
                errs.append("scene %d sync" % s["n"])

        pg.locator(".mt-card").screenshot(path=str(OUT / "00-poster.jpg"), **SHOT)

        for scene, p, name in MOMENTS:
            pg.evaluate("([i,p]) => window.__mitosis.seek(i,p)", [scene, p])
            pg.wait_for_timeout(260)
            pg.locator(".mt-card").screenshot(path=str(OUT / (name + ".jpg")), **SHOT)

        # phone width
        pg.set_viewport_size({"width": 400, "height": 900})
        pg.wait_for_timeout(400)
        pg.evaluate("() => window.__mitosis.seek(13,1)")
        pg.wait_for_timeout(300)
        pg.locator(".mt-card").screenshot(path=str(OUT / "phone-400.jpg"), **SHOT)
        pg.set_viewport_size({"width": 1300, "height": 980})

        # play for real and confirm the clock advances with the audio
        pg.wait_for_timeout(300)
        pg.evaluate("() => window.__mitosis.seek(0,0)")
        pg.click("#mt-play")
        pg.wait_for_timeout(2500)
        st = pg.evaluate("() => window.__mitosis.state()")
        print("after 2.5s of play:", st)
        if not st["playing"] or st["local"] < 1.2:
            errs.append("playback did not advance (%s)" % st)
        pg.evaluate("() => window.__mitosis.pause()")

        # the segmented scrub jumps to a scene and changes the sentence
        pg.locator(".mt-seg").nth(13).click()
        pg.wait_for_timeout(500)
        st2 = pg.evaluate("() => window.__mitosis.state()")
        sent = pg.inner_text("#mt-sentence")
        print("scrub to segment 14 ->", st2["idx"], "|", sent[:44])
        if st2["idx"] != 13 or not sent.startswith("They take hold"):
            errs.append("scrub did not jump to scene 14")
        pg.evaluate("() => window.__mitosis.pause()")

        # reduced motion: still renders, still steps
        pg2 = b.new_page(viewport={"width": 1300, "height": 980})
        pg2.emulate_media(reduced_motion="reduce")
        rm_errs = []
        pg2.on("pageerror", lambda e: rm_errs.append(str(e)))
        pg2.goto(URL, wait_until="networkidle")
        pg2.wait_for_function("window.__mitosis && window.__mitosis.ready", timeout=20000)
        pg2.wait_for_timeout(600)
        red = pg2.evaluate("() => window.__mitosis.reduced")
        pg2.evaluate("() => window.__mitosis.seek(16, 0)")
        pg2.wait_for_timeout(300)
        pg2.locator(".mt-card").screenshot(path=str(OUT / "reduced-motion-scene-17.jpg"), **SHOT)
        print("reduced motion flag:", red, "errors:", rm_errs or "none")
        if not red or rm_errs:
            errs.append("reduced motion")
        pg2.close()

        bad = [m for m in msgs if m[0] in ("error", "pageerror")]
        print("console errors:", bad or "none")
        print("failed requests:", failed or "none")
        if bad:
            errs.append("console errors")
        if failed:
            errs.append("failed requests")
        b.close()

    print("\nRESULT:", "PASS" if not errs else "FAIL " + json.dumps(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
