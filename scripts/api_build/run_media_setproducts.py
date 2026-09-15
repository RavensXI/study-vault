# -*- coding: utf-8 -*-
"""Rebuild the Eduqas Media Studies set-product lessons FROM THE BOARD'S FACT SHEETS.

Why this exists (15 Sep 2026): the first build wrote the set-product lessons from
the specification alone, so they were generic ("a magazine cover has a masthead")
and never named what is on the actual set products (the July 2021 Vogue cover is
Malala Yousafzai, shot by Nick Knight). In the exam the student gets a copy of the
Component 1 Section A products and must analyse THAT product; Section B and all of
Component 2 are recall of the specific products. The board publishes a public fact
sheet per product. Those sheets are the primary source here, injected per lesson
into the content prompt and into the fact-check, with web search off.

Stages (in order):
  plan | prep | submit | poll | fix | pollfix | factcheck | pollfactcheck |
  applyfixes | pollapplyfixes | patch | media | narrate | videoreset
`python scripts/api_build/run_media_setproducts.py --config <cfg.json> <stage>`
`orchestrate` runs the whole chain, polling every 60 s.
"""
import argparse, importlib.util, io, json, os, re, subprocess, sys, time
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8"); os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace"); sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
_spec = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py")); drv = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(drv)

SUBJECT_ID = "4c765fb9-2a67-4414-9bcc-cf2acd581b0e"

# lesson key -> fact sheets (keys into factsheets/manifest.json). The exam use of
# each product is stated in the prompt from the specification's own words.
SHEETS = {
    "set-products-language-representation-L01": ["vogue-july-2021", "gq-august-2019"],
    "set-products-language-representation-L02": ["man-with-the-golden-gun", "no-time-to-die"],
    "set-products-language-representation-L03": ["guardian-18-jan-2022", "sun-1-jan-2021"],
    "set-products-language-representation-L04": ["guardian-6-may-2025", "sun-22-march-2025"],
    "set-products-language-representation-L05": ["quality-street-1956", "nhs-111-2023"],
    "set-products-industries-audiences-L01": ["sun-1-jan-2021", "sun-22-march-2025"],
    "set-products-industries-audiences-L02": ["desert-island-discs"],
    "set-products-industries-audiences-L03": ["no-time-to-die"],
    "set-products-industries-audiences-L04": ["fortnite"],
    "television-in-depth-L01": ["trigger-point"],
    "television-in-depth-L02": ["man-like-mobeen"],
    "television-in-depth-L03": ["modern-family"],
    "television-in-depth-L04": ["trigger-point", "man-like-mobeen", "modern-family"],
    "music-in-depth-L01": ["lizzo-good-as-hell", "taylor-swift-the-man"],
    "music-in-depth-L02": ["stormzy-superheroes", "set-product-guide"],
    "music-in-depth-L03": ["tlc-waterfalls", "set-product-guide"],
    "music-in-depth-L04": ["stormzy-online-media", "taylor-swift-the-man", "lizzo-good-as-hell", "stormzy-superheroes"],
}
# products with no public sheet: the model must stay to documented, checkable facts
NO_SHEET = {
    "music-in-depth-L02": "Justin Bieber, 'Intentions' (2020, ft. Quavo) has NO fact sheet here. Treat it with care: describe only what is widely documented about the video (shot at the Alexandria House shelter in Los Angeles, real women and families, the charitable link) and keep detailed claims to Stormzy, whose sheet is supplied. Say plainly that the class studies ONE contemporary option pair set by their teacher.",
    "music-in-depth-L03": "Duran Duran, 'Rio' (1982) has NO fact sheet here. Keep claims to the documented: directed by Russell Mulcahy, shot in Antigua, the yacht, the band in pastel suits, the 'Patrick Nagel' album-cover style, New Romantic and MTV context. Keep detailed claims to TLC's 'Waterfalls', whose sheet is supplied. The class studies ONE of the two.",
}
EXAM_USE = {
    "set-products-language-representation": "Component 1 Section A. In the exam the student is GIVEN a copy of one of these products and must analyse its media language (Question 1, 15 marks), explain its context of production (Question 2a, 5 marks) or compare it with an unseen product in the same form (Question 2b, 25 marks, extended response on representation). So the lesson must teach the SPECIFIC product: what is on it, where, why, and what it represents and how.",
    "set-products-industries-audiences": "Component 1 Section B. NO copy is given in the exam. Stepped questions test knowledge and understanding of the media INDUSTRY (Question 3) and AUDIENCES (Question 4) for these products. So the lesson must teach the specific facts: ownership, funding, regulation, distribution, circulation or audience figures, how audiences are targeted, reached and how they respond, with the theoretical framework applied to THIS product.",
    "television-in-depth": "Component 2 Section A. A three-minute extract from the set episode is screened twice; Question 1 (20 marks, two parts) analyses media language OR representation in the extract; Question 2 (10 marks) tests industries, audiences or contexts for the set programme. So the lesson must teach the specific set episode: its narrative, characters, representations, genre conventions, production context, broadcaster, scheduling and audience.",
    "music-in-depth": "Component 2 Section B. NO copy is given. Question 3 (20 marks) asks for judgements and conclusions through analysis of the set music video(s) and the artist's online, social and participatory media, on media language OR representation; Question 4 (10 marks) tests industries, audiences or contexts. So the lesson must teach the specific video: its narrative, performance, star image, representations, intertextuality, and the artist's online presence, with contexts.",
}
FIELDS = ("description", "content_html", "exam_tip_html", "conclusion_html",
          "practice_questions", "knowledge_checks", "flashcard_questions", "glossary_terms")


def _cfg_path(cfg, *p): return os.path.join(cfg["run_dir"], *p)
def _sheets_dir(cfg): return cfg["factsheets_dir"]
def _manifest(cfg): return json.load(io.open(os.path.join(_sheets_dir(cfg), "manifest.json"), encoding="utf-8"))
def _sheet_text(cfg, key):
    t = io.open(os.path.join(_sheets_dir(cfg), key + ".txt"), encoding="utf-8").read()
    return re.sub(r"\n{3,}", "\n\n", t)
def _plan(cfg): return json.load(io.open(_cfg_path(cfg, "plan.json"), encoding="utf-8"))


def stage_plan(cfg):
    units = drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug,name,sort_order&order=sort_order" % SUBJECT_ID)
    old = json.load(io.open(cfg["source_plan_run"], encoding="utf-8"))  # the original run's plan: accents, subtitles
    old_units = {u["slug"]: u for u in old["article_units"]}
    plan = {"article_units": [], "question_type_names": old.get("question_type_names", [])}
    for u in units:
        if u["slug"] not in EXAM_USE: continue
        ou = old_units.get(u["slug"], {})
        rows = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,description&order=lesson_number" % u["id"])
        lessons = []
        for r in rows:
            key = drv.lesson_key(u["slug"], r["lesson_number"])
            if key not in SHEETS: print("no sheets mapped for", key, "- skipped"); continue
            lessons.append({"number": r["lesson_number"], "title": r["title"], "description": r.get("description") or "",
                            "lesson_id": r["id"], "sheets": SHEETS[key], "spec_references": [], "section_markers": []})
        plan["article_units"].append({"slug": u["slug"], "name": u["name"], "subtitle": ou.get("subtitle", ""), "accent": ou.get("accent", "#7c3aed"),
                                      "unit_id": u["id"], "lesson_count": len(rows), "lessons": lessons})
    drv.write_json(_cfg_path(cfg, "plan.json"), plan)
    print("plan:", [(u["slug"], len(u["lessons"])) for u in plan["article_units"]])


def stage_prep(cfg):
    plan = _plan(cfg); man = _manifest(cfg)
    system = drv.shared_system_blocks(cfg, plan)
    system = [{k: v for k, v in blk.items() if k != "cache_control"} for blk in system]
    reqs = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            key = drv.lesson_key(u["slug"], l["number"])
            sheets = "\n\n".join("<fact_sheet product=\"%s\" source=\"%s\">\n%s\n</fact_sheet>" % (k, man[k]["url"], _sheet_text(cfg, k)) for k in l["sheets"])
            user = (
                "UNIT: %s — %s\nUNIT ACCENT COLOUR: %s\nLESSON %d of %d: %s\n"
                "PLANNED DESCRIPTION (refine to 60-100 chars if needed): %s\n\n"
                "HOW THIS IS EXAMINED (from the specification):\n%s\n\n"
                "PRIMARY SOURCE — THE EXAM BOARD'S OWN FACT SHEETS FOR THESE SET PRODUCTS. Everything specific in the lesson "
                "comes from here: who and what is on the product, the cover lines, headlines, layout, colours, typography, "
                "camera work, mise-en-scene, narrative, the producer, publisher, broadcaster, dates, figures, contexts, and the "
                "theoretical framework points the sheets make. Quote or paraphrase the sheets' facts; do not invent details "
                "the sheets do not give. Where the sheets give figures, use them with their dates.\n\n%s\n\n%s"
                "WRITING BRIEF: this is a revision lesson about the SPECIFIC set product(s), not about the media form in general. "
                "Open with what the product is and what the student will see on it. Walk the product element by element "
                "(media language), then representation, then contexts, then (for industries/audiences lessons) the industry "
                "and audience facts, applying the theoretical framework named in the sheets. Practice questions, knowledge "
                "checks and flashcards must test the SPECIFIC product (names, dates, features, figures), not generic theory. "
                "Never name the exam board: say 'the exam board'. Never mention the non-exam assessment. "
                "Keep the given title. Do NOT include hero_keywords or hero_image_caption changes of substance (the hero is kept).\n\n"
                "Generate the complete lesson as a JSON object."
            ) % (u["name"], u.get("subtitle", ""), u.get("accent") or "", l["number"], u.get("lesson_count", len(u["lessons"])), l["title"],
                 l.get("description", ""), EXAM_USE[u["slug"]], sheets, (NO_SHEET[key] + "\n\n") if key in NO_SHEET else "")
            reqs.append({"custom_id": key, "params": {"model": drv.MODEL_CONTENT, "max_tokens": 32000,
                                                       "system": system, "messages": [{"role": "user", "content": user}]}})
    drv.write_json(_cfg_path(cfg, "requests_content.json"), reqs)
    print("prepped %d content requests; user msgs %dk chars" % (len(reqs), sum(len(r["params"]["messages"][0]["content"]) for r in reqs) // 1000))


def stage_factcheck(cfg):
    """Driver's fact-check shape, with the lesson's own fact sheets in the user turn and no web."""
    st = drv.load_state(cfg); plan = _plan(cfg); man = _manifest(cfg)
    by_key = {drv.lesson_key(u["slug"], l["number"]): (u, l) for u in plan["article_units"] for l in u["lessons"]}
    rules = drv.assessment_rules_block(cfg); cl = drv.client(); reqs = []
    for cid in st.get("content_ok", []):
        u, l = by_key[cid]
        obj = json.load(io.open(_cfg_path(cfg, "lessons", cid + ".json"), encoding="utf-8"))
        payload = {k: obj.get(k) for k in ("content_html", "exam_tip_html", "conclusion_html", "knowledge_checks", "flashcard_questions", "glossary_terms", "practice_questions")}
        sheets = "\n\n".join("<fact_sheet product=\"%s\">\n%s\n</fact_sheet>" % (k, _sheet_text(cfg, k)) for k in l["sheets"])
        user = ("LESSON: %s\nTARGET BOARD: %s GCSE %s — question tariffs on this board: %s\n%s\n%s\n"
                "PRIMARY AUTHORITY — the exam board's fact sheets for this lesson's set products. Any claim about the product "
                "(who is on it, what it shows, dates, figures, producers, contexts) that contradicts these sheets is HIGH. A claim "
                "the sheets do not cover and that is not common documented knowledge is MEDIUM (label it 'unsupported by the sheet'). "
                "Generic media theory the sheets do not mention is fine if correct.\n%s\n\n%s\n\nLESSON JSON:\n%s\n\nFact-check this lesson. Return the findings JSON."
                % (cid, cfg["exam_board"], cfg["subject_name"], " | ".join(plan.get("question_type_names", [])),
                   ("SCOPE FOR THIS UNIT: " + cfg.get("scope_statement", "")) if cfg.get("scope_statement") else "", rules,
                   NO_SHEET.get(cid, ""), sheets, json.dumps(payload, ensure_ascii=False)))
        fc_system = drv.FACTCHECK_SYSTEM + ("\n\n" + cfg["factcheck_system_extra"] if cfg.get("factcheck_system_extra") else "")
        reqs.append({"custom_id": cid, "params": {"model": drv.MODEL_FACTCHECK, "max_tokens": cfg.get("factcheck_max_tokens", 12000),
                                                   "system": [{"type": "text", "text": fc_system}], "messages": [{"role": "user", "content": user}]}})
    b = cl.messages.batches.create(requests=reqs); st["factcheck_batch_id"] = b.id; drv.save_state(cfg, st)
    print("factcheck batch submitted:", b.id, "requests:", len(reqs))


BOARD = re.compile(r"\b(AQA|Eduqas|WJEC|Pearson|OCR)\b")


def stage_patch(cfg):
    """Write every validated lesson back onto its existing row: content fields only.
    Title, hero, slug, id, cohort keys stay. Narration manifest cleared for `narrate`."""
    st = drv.load_state(cfg); plan = _plan(cfg)
    failures = st.get("content_failures", {}); n = 0; held = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = drv.lesson_key(u["slug"], l["number"])
            if cid not in st.get("content_ok", []) or cid in failures: held.append(cid); continue
            obj = json.load(io.open(_cfg_path(cfg, "lessons", cid + ".json"), encoding="utf-8"))
            blob = json.dumps({k: obj.get(k) for k in FIELDS}, ensure_ascii=False)
            if BOARD.search(re.sub(r"<[^>]+>", " ", blob)):
                held.append(cid + " (names a board)"); continue
            patch = {k: obj[k] for k in FIELDS if k in obj}; patch["narration_manifest"] = None
            drv.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["lesson_id"], patch); n += 1
            print("patched", cid)
    st["patched"] = sorted(set(st.get("patched", [])) | {drv.lesson_key(u["slug"], l["number"]) for u in plan["article_units"] for l in u["lessons"]} - set(h.split(" ")[0] for h in held))
    drv.save_state(cfg, st)
    print("patched %d lessons; held: %s" % (n, held))


def stage_media(cfg):
    """Add the official fact sheet(s) to each lesson's Study Tools so the student can read the product."""
    plan = _plan(cfg); man = _manifest(cfg); n = 0
    titles = {"vogue-july-2021": "Vogue (July 2021) — official set product fact sheet", "gq-august-2019": "GQ (August 2019) — official set product fact sheet",
              "man-with-the-golden-gun": "The Man with the Golden Gun poster — official fact sheet", "no-time-to-die": "No Time to Die poster and film industry — official fact sheet",
              "quality-street-1956": "Quality Street (1956) advert — official fact sheet", "nhs-111-2023": "NHS 111 (2023) advert — official fact sheet",
              "guardian-18-jan-2022": "The Guardian (18 January 2022) — official fact sheet", "sun-1-jan-2021": "The Sun (1 January 2021) — official fact sheet",
              "guardian-6-may-2025": "The Guardian (6 May 2025) — official fact sheet", "sun-22-march-2025": "The Sun (22 March 2025) — official fact sheet",
              "desert-island-discs": "Desert Island Discs — official fact sheet", "fortnite": "Fortnite — official fact sheet",
              "trigger-point": "Trigger Point — official fact sheet", "man-like-mobeen": "Man Like Mobeen — official fact sheet", "modern-family": "Modern Family — official fact sheet",
              "lizzo-good-as-hell": "Lizzo, Good as Hell — official fact sheet", "taylor-swift-the-man": "Taylor Swift, The Man — official fact sheet",
              "stormzy-superheroes": "Stormzy, Superheroes — official fact sheet", "stormzy-online-media": "Stormzy online media — official fact sheet",
              "tlc-waterfalls": "TLC, Waterfalls — official fact sheet", "set-product-guide": "Set products guide — the exam board's list"}
    for u in plan["article_units"]:
        for l in u["lessons"]:
            row = drv.supa(cfg, "GET", "/rest/v1/lessons?id=eq.%s&select=related_media" % l["lesson_id"])[0]
            rm = row.get("related_media") or []
            tools = next((c for c in rm if c.get("category") == "Study Tools"), None)
            if tools is None: tools = {"category": "Study Tools", "items": []}; rm.append(tools)
            have = {it.get("url") for c in rm for it in c.get("items", [])}
            added = 0
            for k in l["sheets"]:
                url = man[k]["url"]
                if url in have: continue
                tools["items"].insert(added, {"title": titles.get(k, k), "url": url, "description": "The exam board's own notes on this set product: what is on it, its contexts and the framework points examiners expect."}); added += 1
            if added:
                drv.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["lesson_id"], {"related_media": rm}); n += added
    print("fact-sheet links added:", n)


def stage_narrate(cfg):
    plan = _plan(cfg)
    for u in plan["article_units"]:
        for l in u["lessons"]:
            print("narrating", u["slug"], l["number"])
            subprocess.run([sys.executable, os.path.join(REPO, "scripts", "_narrate_single_lesson.py"), l["lesson_id"]], check=True)


def stage_videoreset(cfg):
    """The explainer videos were made from the generic text. Clear the video and the
    job record so the nightly explainer run regenerates them from the new lessons."""
    plan = _plan(cfg); ids = {l["lesson_id"] for u in plan["article_units"] for l in u["lessons"]}
    sp = os.path.join(REPO, "scripts", "_batch_explainer_state.json")
    st = json.load(io.open(sp, encoding="utf-8"))
    io.open(sp + ".bak-setproducts", "w", encoding="utf-8").write(json.dumps(st))
    jobs = st["jobs"]; removed = 0
    if isinstance(jobs, dict):
        for k in list(jobs):
            j = jobs[k]
            if j.get("lesson_id") in ids or ("media-studies-eduqas/exam-technique" in (j.get("label") or "")) or ("media-studies-eduqas/creating-media-products" in (j.get("label") or "")):
                del jobs[k]; removed += 1
    else:
        keep = [j for j in jobs if not (j.get("lesson_id") in ids or "media-studies-eduqas/exam-technique" in (j.get("label") or "") or "media-studies-eduqas/creating-media-products" in (j.get("label") or ""))]
        removed = len(jobs) - len(keep); st["jobs"] = keep
    io.open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False))
    for lid in ids: drv.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % lid, {"youtube_video_id": None})
    print("explainer job records removed:", removed, "| videos cleared on", len(ids), "lessons (nightly run regenerates)")


def _wait(cfg, stage, key_done, poll_stage, every=60, limit=7200):
    """Run poll_stage every `every` seconds until state[key_done] appears."""
    t0 = time.time()
    while time.time() - t0 < limit:
        STAGES[poll_stage](cfg)
        st = drv.load_state(cfg)
        if st.get(key_done): return True
        time.sleep(every)
    return False


def stage_orchestrate(cfg):
    stage_plan(cfg); stage_prep(cfg); STAGES["submit"](cfg)
    # poll writes content_ok / content_failures when the batch has ended
    t0 = time.time()
    while True:
        STAGES["poll"](cfg); st = drv.load_state(cfg)
        if st.get("content_ok") or st.get("content_failures"): break
        if time.time() - t0 > 7200: print("content batch timed out"); return
        time.sleep(60)
    st = drv.load_state(cfg)
    if st.get("content_failures"):
        STAGES["fix"](cfg); t0 = time.time()
        while True:
            STAGES["pollfix"](cfg); st = drv.load_state(cfg)
            if not st.get("fix_batch_id") or st["fix_batch_id"] in st.get("collected_batches", []): break
            if time.time() - t0 > 3600: break
            time.sleep(60)
    stage_factcheck(cfg); t0 = time.time()
    while True:
        STAGES["pollfactcheck"](cfg); st = drv.load_state(cfg)
        if st.get("factcheck_counts"): break
        if time.time() - t0 > 7200: print("factcheck timed out"); return
        time.sleep(60)
    STAGES["applyfixes"](cfg); st = drv.load_state(cfg)
    if st.get("applyfix_batch_id"):
        t0 = time.time()
        while True:
            STAGES["pollapplyfixes"](cfg); st = drv.load_state(cfg)
            if st["applyfix_batch_id"] in st.get("collected_batches", []): break
            if time.time() - t0 > 7200: break
            time.sleep(60)
    stage_patch(cfg); stage_media(cfg); stage_narrate(cfg); stage_videoreset(cfg)
    print("ORCHESTRATE COMPLETE")


STAGES = dict(drv.STAGES)
STAGES.update({"plan": stage_plan, "prep": stage_prep, "factcheck": stage_factcheck, "patch": stage_patch, "media": stage_media,
               "narrate": stage_narrate, "videoreset": stage_videoreset, "orchestrate": stage_orchestrate})


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); ap.add_argument("stage", choices=sorted(STAGES))
    a = ap.parse_args(); cfg = json.load(io.open(a.config, encoding="utf-8")); os.makedirs(cfg["run_dir"], exist_ok=True)
    STAGES[a.stage](cfg)


if __name__ == "__main__":
    main()
