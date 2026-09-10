# -*- coding: utf-8 -*-
"""Second vision pass over the Latin heroes, against a subject-specific brief.

The generic hero finder grades an image against the lesson title alone, which
for this subject lets through modern-life stock photography (a family on a
porch for "People, Family and Society") and, worse, material from the wrong
ancient world entirely (a Hebrew manuscript for a lesson on reading Latin).
This pass re-judges every shipped hero against what a Latin course actually
needs, and re-runs the failures with steered, period-specific search queries.

    python scripts/_content_latin-eduqas/heroes_audit_latin.py audit
    python scripts/_content_latin-eduqas/heroes_audit_latin.py repair
"""
import base64
import io
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import anthropic  # noqa: E402
import driver as D  # noqa: E402
from lib.hero_pipeline import HeroFinder  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")
VISION_MODEL = "claude-haiku-4-5-20251001"

BRIEF = """You are auditing the header photograph of a lesson in a GCSE Latin course (students aged 15-16).

LESSON: {title}
ABOUT: {description}

A hero image for this course must be a PHOTOGRAPH of the Latin and Roman world: Roman archaeology, ruins, temples, forums, roads and aqueducts; Roman sculpture, mosaics, frescoes, coins and everyday objects in museums; carved Latin inscriptions; Latin manuscripts and printed Latin texts; or a faithful re-enactment of Roman life. A photograph of a landscape that the lesson's narrative actually crosses (for example the Alps) also passes.

Reply in EXACTLY this format:

VERDICT: KEEP or REPLACE
WHY: one short sentence.

REPLACE if the image is: modern everyday life used as a stand-in (people in modern clothes, modern interiors, modern sport, modern industry, modern tableware); material from a different ancient or later culture presented as Roman (Hebrew, Greek-only, Egyptian, Christian liturgical, medieval European religious objects) where the lesson is about Rome; a drawing, painting, engraving or AI-generated illustration rather than a photograph; a screenshot, logo, watermark or text-heavy graphic; or simply unrelated to the lesson.

KEEP if it is a genuine photograph of the Roman or Latin world, or of a place the lesson's own narrative names, even if it is a plain one.
A Latin manuscript or a Latin inscription always KEEPs for a language lesson. A photograph of a museum object KEEPs even though the object itself is ancient art.
"""

# Period-specific queries for the lessons the audit is most likely to fail, so
# the repair does not go hunting on the same generic terms that failed first.
STEER = {
    "language-paper-method": ["latin inscription stone", "roman inscription carved",
                              "latin manuscript page"],
    "heroes-and-villains": ["roman marble bust", "roman statue museum",
                            "roman relief sculpture"],
    "come-dine-with-me": ["roman mosaic food", "pompeii fresco banquet",
                          "roman pottery vessels museum"],
    "narratives-livy-and-virgil": ["alps mountain pass snow", "roman relief sculpture",
                                   "hercules statue marble"],
    "roman-civilisation": ["roman relief sculpture", "roman temple ruins",
                           "roman altar sacrifice relief"],
    "vocabulary": ["roman inscription carved letters", "roman forum ruins",
                   "roman mosaic figures"],
    "accidence": ["latin manuscript page", "roman inscription stone tablet",
                  "roman writing tablet stylus"],
    "syntax-and-translation": ["latin manuscript page", "roman inscription carved",
                               "ancient latin book page"],
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "StudyVaultHeroBot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def all_lessons(cfg):
    st = D.load_state(cfg)
    units = D.supa(cfg, "GET",
                   "/rest/v1/units?subject_id=eq.%s&select=id,slug,name&order=sort_order"
                   % st["subject_id"])
    out = []
    for u in units:
        rows = D.supa(cfg, "GET",
                      "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,"
                      "description,hero_image_url,hero_image_caption&order=lesson_number"
                      % u["id"])
        for r in rows:
            out.append((u, r))
    return out


def stage_audit(cfg):
    cl = anthropic.Anthropic()
    verdicts = {}
    for u, l in all_lessons(cfg):
        url = l.get("hero_image_url")
        if not url:
            continue
        try:
            jpeg = fetch(url)
        except Exception as e:
            print("  fetch fail", url, e)
            continue
        msg = cl.messages.create(
            model=VISION_MODEL, max_tokens=150,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64",
                                             "media_type": "image/jpeg",
                                             "data": base64.b64encode(jpeg).decode()}},
                {"type": "text", "text": BRIEF.format(
                    title=l["title"], description=l.get("description") or "")}]}])
        text = msg.content[0].text
        D.log_usage(cfg, "hero-audit", VISION_MODEL, "%s-L%02d" % (u["slug"], l["lesson_number"]),
                    msg.usage)
        verdict = "REPLACE" if "VERDICT: REPLACE" in text else "KEEP"
        why = text.split("WHY:")[-1].strip() if "WHY:" in text else ""
        key = "%s-L%02d" % (u["slug"], l["lesson_number"])
        verdicts[key] = {"verdict": verdict, "why": why, "url": url,
                         "lesson_id": l["id"], "unit_slug": u["slug"],
                         "unit_name": u["name"], "lesson_number": l["lesson_number"],
                         "title": l["title"], "description": l.get("description") or ""}
        print("  %-8s %s  %s" % (verdict, key.ljust(30), why[:80]))
    D.write_json(os.path.join(cfg["run_dir"], "hero_audit.json"), verdicts)
    bad = [k for k, v in verdicts.items() if v["verdict"] == "REPLACE"]
    print("\n%d of %d heroes flagged for replacement" % (len(bad), len(verdicts)))


def stage_repair(cfg):
    verdicts = json.load(io.open(os.path.join(cfg["run_dir"], "hero_audit.json"),
                                 encoding="utf-8"))
    bad = {k: v for k, v in verdicts.items() if v["verdict"] == "REPLACE"}
    if not bad:
        print("nothing to repair")
        return
    finder = HeroFinder()
    # every hero currently in use stays blocked, so a repair cannot duplicate one
    for v in verdicts.values():
        finder.used.add(v["url"])

    for key, v in sorted(bad.items()):
        queries = STEER.get(v["unit_slug"], ["roman ruins", "latin inscription"])
        finder.suggest_queries = lambda *a, **k: list(queries)
        print("\n  repairing %s — %s" % (key, v["title"]))
        res = finder.find(
            subject_slug="latin-eduqas",
            subject_name="Latin and the ancient Roman world (Roman archaeology, "
                         "inscriptions, mosaics, sculpture and Latin manuscripts)",
            unit_slug=v["unit_slug"], unit_name=v["unit_name"],
            lesson_number=v["lesson_number"], title=v["title"],
            description=v["description"], reuse_pool=None)
        if not res:
            print("      NO REPLACEMENT FOUND — leaving the existing image")
            continue
        D.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % v["lesson_id"], {
            "hero_image_url": res["url"], "hero_image_alt": res["shows"],
            "hero_image_caption": res["caption"], "hero_image_position": "center"})
        print("      -> %s" % res["caption"])
    print("\nrepair pass complete (%d vision calls)" % finder.vision_calls)


CAPTION_BRIEF = """Write the caption for this image, which is the header of a GCSE Latin lesson.

LESSON: {title}
ABOUT: {description}

RULES
- Describe ONLY what is visibly in the image. Never guess what an inscription says, what a scene depicts, or what a person is doing beyond what you can see.
- Never state or imply that the image is useful, suitable, illustrative or typical. No "illustrating", "showing", "representing", "demonstrating", "suitable for", "typical of".
- Never name the medium of the picture: no "photograph", "photo", "image", "close-up", "shot".
- Naming the object itself is fine and good: "marble bust", "stone inscription", "mosaic floor", "manuscript page".
- British English. No full stop at the end. 14 words maximum, and shorter is better.

Reply with the caption text and nothing else."""


def stage_captions(cfg):
    """Normalise every caption to the house standard: a short, strictly visible
    description, then the credit already established for that image."""
    cl = anthropic.Anthropic()
    changed = 0
    for u, l in all_lessons(cfg):
        url = l.get("hero_image_url")
        old = l.get("hero_image_caption") or ""
        if not url:
            continue
        credit = ""
        if old.rstrip().endswith(")") and "(" in old:
            credit = old[old.rindex("("):]
        try:
            jpeg = fetch(url)
        except Exception as e:
            print("  fetch fail", url, e)
            continue
        msg = cl.messages.create(
            model=VISION_MODEL, max_tokens=120,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64",
                                             "media_type": "image/jpeg",
                                             "data": base64.b64encode(jpeg).decode()}},
                {"type": "text", "text": CAPTION_BRIEF.format(
                    title=l["title"], description=l.get("description") or "")}]}])
        D.log_usage(cfg, "hero-caption", VISION_MODEL,
                    "%s-L%02d" % (u["slug"], l["lesson_number"]), msg.usage)
        desc = msg.content[0].text.strip().strip('"').rstrip(".")
        from lib.hero_pipeline import briticise
        desc = briticise(desc)
        caption = ("%s %s" % (desc, credit)).strip()
        if caption != old:
            D.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["id"],
                   {"hero_image_caption": caption, "hero_image_alt": desc})
            changed += 1
        print("  %s-L%02d  %s" % (u["slug"], l["lesson_number"], caption))
    print("\ncaptions rewritten: %d" % changed)


def main():
    cfg = D.load_config(CFG_PATH)
    stage = sys.argv[1] if len(sys.argv) > 1 else "audit"
    {"audit": stage_audit, "repair": stage_repair,
     "captions": stage_captions}[stage](cfg)


if __name__ == "__main__":
    main()
