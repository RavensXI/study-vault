# -*- coding: utf-8 -*-
"""Pearson Edexcel GCSE Religious Studies B (1RB0), "Beliefs in Action" — phase 1.

Port of the sister subject `religious-studies-edexcel` (Spec A, 1RA0) onto the
Spec B shape: two areas of study, each one religion x four sections, no NEA, no
exam-technique unit and no exam-technique guide pages (docs/PIPELINE.md, "removed
entirely"). Phase 1 builds the two pairings almost every centre takes:

    area1-christianity            Area of Study 1, Christianity            6 lessons
    area1-catholic-christianity   Area of Study 1, Catholic Christianity   6 lessons
    area2-islam                   Area of Study 2, Islam                   5 lessons
    area2-judaism                 Area of Study 2, Judaism                 5 lessons

Three things here differ from run_media_eduqas.py / run_stats_edexcel.py:

1. `plan` is DETERMINISTIC. The unit/lesson shape is already fixed by
   scripts/_plan_religious-studies-b-edexcel.md down to unit slugs, lesson splits
   and spec section ranges, so an Opus planning call would only re-derive it, and
   the API budget for this build is $16.45. The stage instead slices the 351k-char
   specification and writes each lesson's `section_markers` as the specification's
   own numbered content points, quoted VERBATIM.
2. `prep` sends a SLIM spec (the four religion-area blocks in scope plus the
   assessment chapters, ~14k tokens) rather than the whole 88k-token document.
   Batched requests carry no cache marker, so the whole spec would be re-billed on
   all 22 requests for content the lesson cannot use.
3. `factcheck` REFUSES TO RUN without `assessment_rules_doc` (the Media rebuild's
   checker ran without one and called true exam facts "fabricated", and applyfixes
   then stripped them). Web search is forced off: the specification is the only
   authority on this qualification.

Stages, in order:
  plan | plancheck | activate | prep | canary | poll | submit | poll |
  fix | pollfix | factcheck | pollfactcheck | applyfixes | pollapplyfixes |
  insert | media | pollmedia | insertmedia | heroes | narrate | guides | gate |
  verify | costs

    python scripts/api_build/run_rs_b_edexcel.py --config <cfg.json> <stage>
"""
import argparse
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts"))
_spec = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py"))
drv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drv)

SRC_SLUG = "religious-studies-edexcel"
# every RS subject on the platform: their heroes seed the finder's `used` set so a
# photograph never appears twice across the religious-studies family
RS_SUBJECT_SLUGS = ["religious-studies-edexcel", "religious-studies-aqa",
                    "religious-studies-ocr", "religious-studies-eduqas"]

# 1-based inclusive line ranges into specs/edexcel/religious-studies-b-1RB0.md.
# Each runs from that religion's "Area of Study NX - <Religion>" heading to the
# line before the next one.
SPEC_BLOCKS = {
    "area1-catholic-christianity": (515, 854, "Catholic Christianity",
                                    "Area of Study 1: Religion and Ethics"),
    "area1-christianity":          (855, 1188, "Christianity",
                                    "Area of Study 1: Religion and Ethics"),
    "area2-islam":                 (3534, 3833, "Islam",
                                    "Area of Study 2: Religion, Peace and Conflict"),
    "area2-judaism":               (4491, 4815, "Judaism",
                                    "Area of Study 2: Religion, Peace and Conflict"),
}
# running headers and page numbers the PDF extract leaves in the text
FOOTER = re.compile(r"^(Pearson Edexcel Level 1/Level 2 GCSE|Specification . Issue 2|\d{1,3}$|"
                    r"[0-9]{1,2}[A-G] (Catholic Christianity|Christianity|Islam|Judaism|"
                    r"Buddhism|Hinduism|Sikhism)$)")
# every content point opens "<topic phrase>: ..."
NEWPOINT = re.compile(r"^[^;.]{2,130}:\s")

ACCENT = {                      # the 1RA0 accent family, per religion
    "area1-christianity":          ("#b91c1c", "#fef2f2"),
    "area1-catholic-christianity": ("#7c2d12", "#fef2f2"),
    "area2-islam":                 ("#15803d", "#f0fdf4"),
    "area2-judaism":               ("#1d4ed8", "#dbeafe"),
}

QUESTION_TYPES = [
    "3 marks — Outline Three",
    "4 marks — Describe Two",
    "4 marks — Explain Two",
    "5 marks — Explain Two with Sources",
    "12 marks — Discuss a Statement",
]

QUOTES = [
    {"quote": "Love your neighbour as yourself.", "author": "Mark 12:31"},
    {"quote": "Whoever saves one life, it is as if he had saved the whole world.",
     "author": "Mishnah Sanhedrin 4:5"},
    {"quote": "God created mankind in his own image.", "author": "Genesis 1:27"},
    {"quote": "Say: He is Allah, the One.", "author": "Surah 112:1"},
    {"quote": "Justice, justice shall you pursue.", "author": "Deuteronomy 16:20"},
    {"quote": "Blessed are the peacemakers, for they will be called children of God.",
     "author": "Matthew 5:9"},
]

TEACHING_BRIEF = {
    "qualification": (
        "A GCSE in which a student studies TWO religions, one for each of their two areas of "
        "study, and must be able to write about beliefs, teachings and practices and then argue "
        "about them. Half the marks are for knowledge and understanding, half for analysis and "
        "evaluation."),
    "what_students_find_hard": [
        "Quoting a source of wisdom and authority accurately. One part of every question needs a "
        "named source; students either quote nothing or invent something. Lessons must give short, "
        "real, correctly referenced teachings students can memorise.",
        "Divergence. The specification repeatedly asks for DIVERGENT views inside one religion "
        "(Catholic and other Christian teaching; Orthodox and Reform Judaism; Sunni and Shi'a "
        "Islam). Students flatten a religion into one voice and lose marks.",
        "Non-religious views. Atheist and Humanist arguments are named in the specification, "
        "together with the believer's response to them. Students learn the religious view and "
        "forget the other half.",
        "Evaluation structure. The 12-mark question needs arguments for, arguments against and a "
        "justified conclusion. Students write one long paragraph of description.",
        "Keeping the two religions apart. A student answering on two religions confuses teachings, "
        "especially on life after death, war and punishment.",
    ],
    "teaching_moves": [
        "Every belief is taught with (a) what it means, (b) a named source of wisdom and authority, "
        "(c) why it matters to a believer today.",
        "Every ethical topic is taught as a real argument: the religious teaching, the divergent "
        "religious view, the non-religious view, and the response to it.",
        "Ethical theories the specification names (situation ethics, utilitarianism) appear where it "
        "names them, explained in one plain sentence, never as a philosophy lecture.",
        "British terms and British examples: a parish, a synagogue, a mosque in this country.",
        "Respectful, accurate register throughout; never present one tradition as the correct one.",
    ],
    "sources_of_wisdom": (
        "Scripture references belong exactly as the specification gives them. Quote short and quote "
        "real: where the exact wording of a verse is not certain, name the passage and summarise its "
        "teaching rather than inventing a quotation."),
    "exam_shape": (
        "Each paper is one hour and forty-five minutes and worth half the qualification. There are "
        "four questions, one per content section, each in parts running from a short recall task to a "
        "twelve-mark evaluation, and one part of each question needs a source of wisdom and "
        "authority. Spelling, punctuation, grammar and specialist terms carry marks. Never name the "
        "exam board, never give paper codes, never quote the board's level descriptors."),
    "banned": ["board names (Pearson, Edexcel, AQA, OCR, Eduqas, WJEC)",
               "the specification code or paper codes", "spec reference numbers such as 2.4",
               "board level descriptors",
               "any claim about the exam that the specification does not state"],
}

# (unit, lesson number, title, description, (section index, first point, last point),
#  transfer score, [(source unit slug, source lesson number), ...])
LESSONS = [
    ("area1-christianity", 1, "The Trinity, Creation, the Incarnation and the Last Days of Jesus",
     "How Christians describe God, creation, Jesus as the incarnate Son, and his death and resurrection.",
     (0, 1, 4), "high", [("paper-1-christianity", 1), ("paper-1-christianity", 2)]),
    ("area1-christianity", 2, "Salvation, Eschatology and the Problem of Evil",
     "Salvation and atonement, Christian teaching on life after death, and why suffering troubles believers.",
     (0, 5, 8), "high", [("paper-1-christianity", 3), ("paper-1-christianity", 2)]),
    ("area1-christianity", 3, "Marriage and the Family",
     "Christian teaching on marriage, sexual relationships, family life, contraception, divorce and equality.",
     (1, 1, 8), "medium", [("paper-3-philosophy-ethics-christianity", 4),
                           ("paper-3-philosophy-ethics-christianity", 5)]),
    ("area1-christianity", 4, "Living the Christian Life",
     "Worship, sacraments, prayer, pilgrimage, festivals and the work of the local and worldwide Church.",
     (2, 1, 8), "high", [("paper-1-christianity", 4), ("paper-1-christianity", 5)]),
    ("area1-christianity", 5, "Origins of the Universe, the Sanctity of Life and Abortion",
     "Christian teaching on how the universe began, why life is holy, and the debate about abortion.",
     (3, 1, 4), "low", []),
    ("area1-christianity", 6, "Life After Death, Euthanasia and the Natural World",
     "Christian belief in life after death, the euthanasia debate, and Christian care for the planet.",
     (3, 5, 8), "medium", [("paper-1-christianity", 3)]),

    ("area1-catholic-christianity", 1, "The Trinity, Creation and Human Nature",
     "Catholic teaching on the Trinity, the creation accounts, and what it means to be made in God's image.",
     (0, 1, 4), "high", [("paper-1-catholic-christianity", 1)]),
    ("area1-catholic-christianity", 2, "The Incarnation, the Paschal Mystery, Salvation and Eschatology",
     "Jesus as incarnate Son, the Paschal Mystery, grace and salvation, and Catholic teaching on the last things.",
     (0, 5, 8), "high", [("paper-1-catholic-christianity", 2), ("paper-1-catholic-christianity", 3)]),
    ("area1-catholic-christianity", 3, "Marriage and the Family",
     "Catholic teaching on marriage, sexual relationships, family life, contraception, divorce and equality.",
     (1, 1, 8), "medium", [("paper-3-philosophy-ethics-catholic", 4),
                           ("paper-3-philosophy-ethics-catholic", 5)]),
    ("area1-catholic-christianity", 4, "Living the Catholic Life",
     "Sacramental living, the Mass, prayer, pilgrimage, Catholic social teaching, mission and the funeral rite.",
     (2, 1, 8), "high", [("paper-1-catholic-christianity", 4), ("paper-1-catholic-christianity", 5)]),
    ("area1-catholic-christianity", 5, "Origins of the Universe, the Sanctity of Life and Abortion",
     "Catholic teaching on how the universe began, why life is holy, and the debate about abortion.",
     (3, 1, 4), "low", []),
    ("area1-catholic-christianity", 6, "Life After Death, Euthanasia and the Natural World",
     "Catholic belief in life after death, the euthanasia debate, and Catholic care for creation.",
     (3, 5, 8), "medium", [("paper-1-catholic-christianity", 3)]),

    ("area2-islam", 1, "The Six Beliefs, the Five Roots, the Nature of Allah and Risalah",
     "The foundations of Muslim belief: the Six Beliefs, the Five Roots, Allah's nature and prophethood.",
     (0, 1, 4), "high", [("paper-2-islam", 1)]),
    ("area2-islam", 2, "Holy Books, Angels, Predestination and Akhirah",
     "Muslim teaching on the holy books, the angels, al-Qadr and life after death.",
     (0, 5, 8), "high", [("paper-2-islam", 2)]),
    ("area2-islam", 3, "Crime and Punishment",
     "Muslim teaching on justice, crime, good and evil, punishment, forgiveness and the death penalty.",
     (1, 1, 8), "low", []),
    ("area2-islam", 4, "Living the Muslim Life",
     "The Ten Obligatory Acts, the Five Pillars, jihad and the festivals that shape Muslim life.",
     (2, 1, 8), "high", [("paper-2-islam", 3), ("paper-2-islam", 4)]),
    ("area2-islam", 5, "Peace and Conflict",
     "Muslim teaching on peace, peacemaking, conflict, pacifism, just war, holy war and modern weapons.",
     (3, 1, 8), "low", []),

    ("area2-judaism", 1, "The Almighty, Shekhinah, the Messiah and the Covenant with Abraham",
     "How Jews describe the Almighty, the divine presence, the Messiah and the covenant with Abraham.",
     (0, 1, 4), "high", [("paper-2-judaism", 1)]),
    ("area2-judaism", 2, "The Covenant at Sinai, Pikuach Nefesh, the Mitzvot and Life After Death",
     "The Sinai covenant, why life takes precedence, the Mitzvot, and Jewish belief about life after death.",
     (0, 5, 8), "high", [("paper-2-judaism", 2), ("paper-2-judaism", 1)]),
    ("area2-judaism", 3, "Crime and Punishment",
     "Jewish teaching on justice, crime, good and evil, punishment, forgiveness and the death penalty.",
     (1, 1, 8), "low", []),
    ("area2-judaism", 4, "Living the Jewish Life",
     "Synagogue worship, the Tenakh and Talmud, prayer, rituals, Shabbat and the Jewish festivals.",
     (2, 1, 8), "high", [("paper-2-judaism", 3), ("paper-2-judaism", 4)]),
    ("area2-judaism", 5, "Peace and Conflict",
     "Jewish teaching on peace, peacemaking, conflict, pacifism, just war, holy war and modern weapons.",
     (3, 1, 8), "low", []),
]

UNIT_META = {
    "area1-christianity": (1, "Area of Study 1: Religion and Ethics (Christianity)",
        "Christian beliefs, marriage and the family, living the Christian life, and matters of life and death"),
    "area1-catholic-christianity": (2, "Area of Study 1: Religion and Ethics (Catholic Christianity)",
        "Catholic beliefs, marriage and the family, living the Catholic life, and matters of life and death"),
    "area2-islam": (3, "Area of Study 2: Religion, Peace and Conflict (Islam)",
        "Muslim beliefs, crime and punishment, living the Muslim life, and peace and conflict"),
    "area2-judaism": (4, "Area of Study 2: Religion, Peace and Conflict (Judaism)",
        "Jewish beliefs, crime and punishment, living the Jewish life, and peace and conflict"),
}

CANARY = ["area1-christianity-L03", "area2-islam-L05"]


# ---------------------------------------------------------------- spec slicing

def _clean(text):
    return re.sub(r"\n{3,}", "\n\n",
                  "\n".join(l for l in text.split("\n") if not FOOTER.match(l.strip()))).strip()


def _sections(block):
    idx = [(m.start(), m.group(0).strip()) for m in re.finditer(r"^Section \d: .*$", block, re.M)]
    out = []
    for i, (pos, title) in enumerate(idx):
        end = idx[i + 1][0] if i + 1 < len(idx) else len(block)
        body = block[pos + len(title):end].strip()
        body = re.sub(r"^Students should have an understanding of:\s*", "", body)
        out.append({"section": title, "text": re.sub(r"\n{3,}", "\n\n", body).strip()})
    return out


def _split_points(sec):
    """The specification's numbered content points for one section, verbatim.

    The PDF extract emits runs of bare point numbers ahead of their paragraphs,
    breaks some points across two paragraphs, and occasionally runs two points
    together with no blank line. Walk the paragraphs in document order: a
    paragraph only starts a new point when the one before it ended in a full
    stop AND it opens like a content point."""
    paras = [re.sub(r"\s+", " ", p).strip()
             for p in re.split(r"\n\s*\n", sec["text"]) if p.strip()]
    refs, bodies = set(), []
    for flat in paras:
        if re.fullmatch(r"\d+\.\d+\*?", flat):
            refs.add(int(flat.split(".")[1].rstrip("*")))
            continue
        m = re.match(r"^(\d+\.\d+\*?)\s+(.*)$", flat)
        if m:
            refs.add(int(m.group(1).split(".")[1].rstrip("*")))
            bodies.append(m.group(2))
        elif bodies and not (bodies[-1][-1:] == "."
                             and (flat[:1].isupper() or NEWPOINT.match(flat))):
            bodies[-1] += " " + flat
        else:
            bodies.append(flat)
    total = max(refs)
    boundary = re.compile(r"(?<=\.) (?=[A-Z][A-Za-z'’ ]{2,60}:)")
    while len(bodies) < total:
        for i, b in enumerate(bodies):
            m = boundary.search(b)
            if m:
                bodies[i:i + 1] = [b[:m.start()].strip(), b[m.end():].strip()]
                break
        else:
            break
    if len(bodies) != total:
        raise SystemExit("spec parse: %s expected %d points, got %d"
                         % (sec["section"], total, len(bodies)))
    return bodies


def slice_spec(cfg):
    """Return (blocks, slim spec markdown)."""
    lines = drv.read(cfg["spec_md"]).split("\n")
    blocks, slim = {}, []
    for slug, (a, b, religion, area) in SPEC_BLOCKS.items():
        raw = _clean("\n".join(lines[a - 1:b]))
        blocks[slug] = {"religion": religion, "area": area, "sections": _sections(raw)}
        slim.append("# %s — %s\n\n%s" % (area, religion, raw))
    grab = lambda a, b: _clean("\n".join(lines[a - 1:b]))
    head = ("# Pearson Edexcel GCSE (9-1) Religious Studies B (1RB0) — specification extract\n\n"
            "## Content and assessment overview\n\n" + grab(264, 330) + "\n\n" + grab(331, 386)
            + "\n\n" + grab(387, 440) + "\n\n## Per-paper assessment notes\n\n" + grab(2810, 2830)
            + "\n\n## Assessment objectives\n\n" + grab(7535, 7600)
            + "\n\n## Appendix 3: Command words\n\n" + grab(8062, 8118) + "\n\n")
    return blocks, head + "\n\n".join(slim) + "\n"


# ---------------------------------------------------------------- stage: plan

def stage_plan(cfg):
    blocks, slim = slice_spec(cfg)
    drv.write_json(os.path.join(cfg["run_dir"], "spec_blocks.json"), blocks)
    io.open(os.path.join(cfg["run_dir"], "spec_slim.md"), "w", encoding="utf-8").write(slim)
    print("slim spec: %d chars (~%dk tokens) from %d chars"
          % (len(slim), len(slim) // 4000, os.path.getsize(cfg["spec_md"])))

    units = {}
    for slug, number, title, desc, (sec_i, first, last), score, sources in LESSONS:
        sort_order, name, subtitle = UNIT_META[slug]
        accent, light = ACCENT[slug]
        u = units.setdefault(slug, {
            "slug": slug, "name": name, "subtitle": subtitle,
            "body_class": "unit-religious-studies-b-edexcel-%d" % sort_order,
            "accent": accent, "accent_light": light, "accent_badge": accent + "33",
            "sort_order": sort_order, "lessons": []})
        sec = blocks[slug]["sections"][sec_i]
        pts = _split_points(sec)
        n = int(sec["section"].split(":")[0].split()[1])
        whole = (first == 1 and last == len(pts))
        markers = [(p if whole else "%d.%d %s" % (n, i + 1, p))
                   for i, p in enumerate(pts) if first <= i + 1 <= last]
        tr = {"transfer_score": score, "source_subject_slug": SRC_SLUG}
        if sources:
            tr["source_unit_slug"] = sources[0][0]
            tr["source_lesson_number"] = sources[0][1]
            tr["sources"] = [{"unit_slug": s, "lesson_number": ln} for s, ln in sources]
            tr["notes"] = ("Reuse the explanation, structure and pedagogy of the source lesson(s) "
                           "where they teach the same idea. The CONTENT SCOPE is the section markers, "
                           "which come from a different specification: drop anything the markers do "
                           "not ask for and add everything they do.")
        else:
            tr["notes"] = ("No close source lesson on the sister specification; build from the "
                           "section markers.")
        u["lessons"].append({
            "number": number, "title": title, "description": desc,
            "spec_references": ["%s — %s, points %d.%d–%d.%d"
                                % (blocks[slug]["area"], sec["section"], n, first, n, last)],
            "section_markers": markers, "content_transfer": tr})

    ordered = sorted(units.values(), key=lambda u: u["sort_order"])
    for u in ordered:
        u["lesson_count"] = len(u["lessons"])
    plan = {
        "subject": {"slug": cfg["slug"], "name": cfg["subject_name"],
                    "exam_board": cfg["exam_board"], "spec_code": cfg["spec_code"],
                    "school_id": None, "format": "article"},
        "article_units": ordered, "practice_units": [],
        "question_type_names": QUESTION_TYPES, "teaching_brief": TEACHING_BRIEF,
        "quote_ticker_quotes": QUOTES,
        "gaps": ["Phase 1 builds two of the seven religion options per area (Area of Study 1 "
                 "Christianity and Catholic Christianity; Area of Study 2 Islam and Judaism). "
                 "Area of Study 3 and the other religions are phase 2 and add units without "
                 "renaming anything."],
    }
    drv.write_json(os.path.join(cfg["run_dir"], "plan.json"), plan)
    total = sum(len(u["lessons"]) for u in ordered)
    print("plan: %d units, %d lessons" % (len(ordered), total))
    for u in ordered:
        print(" ", u["slug"])
        for l in u["lessons"]:
            print("    L%d %-58s %d markers | %s" % (l["number"], l["title"][:58],
                  len(l["section_markers"]), l["content_transfer"]["transfer_score"]))


# ---------------------------------------------------------------- stage: prep

def stage_prep(cfg):
    """driver.stage_prep, but on the slim spec and with multi-source transfer."""
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    slim = os.path.join(cfg["run_dir"], "spec_slim.md")
    if not os.path.exists(slim):
        raise SystemExit("run `plan` first: %s is missing" % slim)
    full = cfg["spec_md"]
    cfg["spec_md"] = slim
    try:
        system = drv.shared_system_blocks(cfg, plan)
    finally:
        cfg["spec_md"] = full
    system = [{k: v for k, v in b.items() if k != "cache_control"} for b in system]
    system.append({"type": "text", "text":
                   "EXAM RULES FOR THIS QUALIFICATION (the only authority on how the exam works; "
                   "anything about the exam that is not stated here must not be claimed):\n"
                   + drv.read(cfg["assessment_rules_doc"])})
    requests = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            tr = l["content_transfer"]
            user = ("UNIT: %s — %s\nUNIT ACCENT COLOUR: %s\nLESSON %d of %d: %s\n"
                    "PLANNED DESCRIPTION (refine to 60-100 chars if needed): %s\n"
                    "THIS LESSON'S SCOPE IS THE SPECIFICATION CONTENT POINTS BELOW, QUOTED "
                    "VERBATIM. Teach all of them and nothing beyond them. Every phrase after a "
                    "colon in a point ('including reference to ...') is assessable and must appear "
                    "in the lesson.\n<content_points>\n%s\n</content_points>\n"
                    % (u["name"], u.get("subtitle", ""), u["accent"], l["number"],
                       len(u["lessons"]), l["title"], l.get("description", ""),
                       "\n\n".join(l["section_markers"])))
            srcs = tr.get("sources") or []
            fetched = []
            for s in srcs:
                row = drv.fetch_source_lesson(cfg, {
                    "source_subject_slug": tr["source_subject_slug"],
                    "source_unit_slug": s["unit_slug"],
                    "source_lesson_number": s["lesson_number"]})
                if row:
                    fetched.append(row)
            if fetched:
                user += ("\nCONTENT TRANSFER (%s): %s\n<existing_board_content>\n%s\n"
                         "</existing_board_content>\n"
                         % (tr["transfer_score"], tr["notes"],
                            json.dumps(fetched, ensure_ascii=False)))
            else:
                user += ("\nCONTENT TRANSFER: none — write this lesson from the content "
                         "points above.\n")
            user += "\nGenerate the complete lesson as a JSON object."
            requests.append({"custom_id": drv.lesson_key(u["slug"], l["number"]),
                             "params": {"model": drv.MODEL_CONTENT, "max_tokens": 32000,
                                        "system": system,
                                        "messages": [{"role": "user", "content": user}]}})
    drv.write_json(os.path.join(cfg["run_dir"], "requests_content.json"), requests)
    sys_chars = sum(len(b["text"]) for b in system)
    usr_chars = sum(len(r["params"]["messages"][0]["content"]) for r in requests)
    print("prepped %d requests | shared system %dk chars | user total %dk chars | ~%dk in-tokens"
          % (len(requests), sys_chars // 1000, usr_chars // 1000,
             (len(requests) * sys_chars + usr_chars) // 4000))


def _submit(cfg, ids):
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                             encoding="utf-8"))
    st = drv.load_state(cfg)
    done = set(st.get("content_ok", []))
    picked = [r for r in reqs if r["custom_id"] in ids and r["custom_id"] not in done]
    if not picked:
        print("nothing to submit")
        return
    cl = drv.client()
    use_structured = st.get("use_structured")
    if use_structured is None:
        try:
            probe = {"model": picked[0]["params"]["model"], "max_tokens": 32,
                     "messages": [{"role": "user", "content": "reply with the single word OK"}]}
            msg = cl.messages.create(**drv.try_structured(probe))
            drv.log_usage(cfg, "probe", probe["model"], "probe", msg.usage)
            use_structured = True
        except Exception as e:
            print("structured outputs unavailable (%s)" % e)
            use_structured = False
    batch = cl.messages.batches.create(requests=[
        {"custom_id": r["custom_id"],
         "params": drv.try_structured(r["params"]) if use_structured else r["params"]}
        for r in picked])
    st["content_batch_id"] = batch.id
    st["use_structured"] = use_structured
    drv.save_state(cfg, st)
    print("batch submitted:", batch.id, "requests:", [r["custom_id"] for r in picked])


def stage_canary(cfg):
    """Two lessons first: the two written from the specification alone."""
    _submit(cfg, set(CANARY))


def stage_submit(cfg):
    reqs = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"),
                             encoding="utf-8"))
    _submit(cfg, {r["custom_id"] for r in reqs})


# ---------------------------------------------------------------- stage: factcheck

def stage_factcheck(cfg):
    """The driver's fact-check, with two hard preconditions.

    Without `assessment_rules_doc` the checker judges exam claims against nothing
    and calls true exam facts fabricated (Media Eduqas, 15 Sep 2026), and
    applyfixes then strips them out of the lessons. Web search stays off: the
    specification is the authority for this qualification, and the lesson's own
    content points are the authority for its scope."""
    p = cfg.get("assessment_rules_doc")
    if not p or not os.path.exists(p):
        raise SystemExit("REFUSING to fact-check: assessment_rules_doc missing (%r). Build it "
                         "from the specification's assessment chapters first." % p)
    if cfg.get("factcheck_search_max", 0) != 0:
        raise SystemExit("REFUSING to fact-check: factcheck_search_max must be 0 for this build.")
    print("assessment rules: %s (%d chars)" % (os.path.basename(p), os.path.getsize(p)))
    drv.stage_factcheck(cfg)


# ---------------------------------------------------------------- stage: heroes

def stage_heroes(cfg):
    from lib.hero_pipeline import HeroFinder
    st = drv.load_state(cfg)
    finder = HeroFinder()
    seeded = 0
    for slug in RS_SUBJECT_SLUGS:
        subs = drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id" % slug)
        for s in subs:
            for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id" % s["id"]):
                for r in drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=hero_image_url"
                                  "&hero_image_url=not.is.null" % u["id"]):
                    finder.used.add(r["hero_image_url"])
                    seeded += 1
    print("seeded %d existing religious-studies heroes into the no-repeat set" % seeded)
    units = drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug,name&order=sort_order"
                     % st["subject_id"])
    done = fail = 0
    for u in units:
        for l in drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,"
                          "description,hero_image_url&order=lesson_number" % u["id"]):
            if (l.get("hero_image_url") or "").strip():
                finder.used.add(l["hero_image_url"])
                continue
            res = finder.find(subject_slug=cfg["slug"], subject_name=cfg["subject_name"],
                              unit_slug=u["slug"], unit_name=u["name"],
                              lesson_number=l["lesson_number"], title=l["title"],
                              description=l.get("description") or "")
            if not res:
                print("  NO HERO", u["slug"], l["lesson_number"])
                fail += 1
                continue
            drv.supa(cfg, "PATCH", "/rest/v1/lessons?id=eq.%s" % l["id"],
                     {"hero_image_url": res["url"], "hero_image_alt": res["shows"],
                      "hero_image_caption": res["caption"], "hero_image_position": "center"})
            print("  %s L%02d -> %s" % (u["slug"], l["lesson_number"], res["caption"][:90]))
            done += 1
    print("heroes: %d assigned, %d failed, %d vision calls" % (done, fail, finder.vision_calls))


def stage_narrate(cfg):
    st = drv.load_state(cfg)
    for u in drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug&order=sort_order"
                      % st["subject_id"]):
        for r in drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number"
                          "&content_html=not.is.null&order=lesson_number" % u["id"]):
            print("narrating", u["slug"], r["lesson_number"])
            subprocess.run([sys.executable, os.path.join(REPO, "scripts", "_narrate_single_lesson.py"),
                            r["id"]], check=True)


# ---------------------------------------------------------------- stage: guides

GUIDE_RULES = (
    "You write for StudyVault, a GCSE revision site. Audience: students aged 15-16. Plain English, "
    "short sentences, British spelling. Output HTML fragments only (no <html>, <head> or <body>), "
    "using named entities for special characters (&mdash; &rsquo; etc.). Never name an exam board "
    "(no AQA, Eduqas, WJEC, Pearson, Edexcel, OCR): write 'the exam board'. Never give a "
    "specification or paper code. No coloured left-border stripes. No non-exam assessment content.")

GUIDE_TOPICS = (
    "This course studies TWO religions. The topics available are:\n"
    "Area of Study 1 (Christianity or Catholic Christianity): beliefs (Trinity, creation, "
    "incarnation, salvation, eschatology, the problem of evil); marriage and the family; living the "
    "faith (worship, sacraments, prayer, pilgrimage, festivals, the local and worldwide Church); "
    "matters of life and death (origins of the universe, sanctity of life, abortion, life after "
    "death, euthanasia, the natural world).\n"
    "Area of Study 2 (Islam or Judaism): beliefs (the Six Beliefs and Five Roots, the nature of "
    "Allah, risalah, holy books, angels, predestination, akhirah; the Almighty, Shekhinah, the "
    "Messiah, the covenants, Pikuach Nefesh, the Mitzvot, life after death); crime and punishment; "
    "living the faith (the Five Pillars and Ten Obligatory Acts, jihad, festivals; synagogue "
    "worship, Tenakh and Talmud, prayer, rituals, Shabbat, festivals); peace and conflict "
    "(peacemaking, pacifism, just war, holy war, weapons of mass destruction).\n"
    "Questions run from a short recall task to a twelve-mark evaluation, and one part of each "
    "question needs a source of wisdom and authority.")

BOARD_RE = re.compile(r"\b(AQA|Eduqas|WJEC|Pearson|Edexcel|OCR)\b")


def stage_guides(cfg):
    """Revision-technique guides adapted from the sister subject. Exam-technique
    guides are NOT built (retired in the spring 2026 pipeline rebuild)."""
    src = drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&school_id=is.null&select=id"
                   % SRC_SLUG)[0]["id"]
    guides = drv.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=slug,guide_type,"
                      "title,sort_order,content_html&order=sort_order" % src)
    reqs, passthrough = [], {}
    for g in guides:
        if g["guide_type"] != "revision-technique":
            print("skipping non revision-technique guide:", g["slug"], g["guide_type"])
            continue
        html = g["content_html"].replace("/guide/%s/" % SRC_SLUG, "/guide/%s/" % cfg["slug"])
        passthrough[g["slug"]] = dict(g, content_html=html)
        if g["slug"] == "index":
            continue
        reqs.append({"custom_id": "rt-" + g["slug"], "params": {
            "model": drv.MODEL_CONTENT, "max_tokens": 16000, "thinking": {"type": "disabled"},
            "system": [{"type": "text", "text": GUIDE_RULES}],
            "messages": [{"role": "user", "content":
                          "Adapt this revision-technique guide from one GCSE Religious Studies "
                          "course to another. The pedagogy text stays exactly as it is. ONLY "
                          "change the subject worked examples, so that every example uses a topic "
                          "this course actually studies. Keep the HTML structure, classes, entity "
                          "usage and length.\n\n" + GUIDE_TOPICS + "\n\nGUIDE HTML:\n" + html
                          + "\n\nReturn ONLY the adapted HTML fragment, no code fences."}]}})
    cl = drv.client()
    b = cl.messages.batches.create(requests=reqs)
    st = drv.load_state(cfg)
    st["guides_batch_id"] = b.id
    drv.save_state(cfg, st)
    drv.write_json(os.path.join(cfg["run_dir"], "guides_base.json"), passthrough)
    print("guides batch submitted:", b.id, "(%d technique pages + index passthrough)" % len(reqs))


def stage_pollguides(cfg):
    st = drv.load_state(cfg)
    out = drv.collect_batch(cfg, st["guides_batch_id"], "guides", "raw_guides")
    if out is None:
        return
    texts, errors = out
    base = json.load(io.open(os.path.join(cfg["run_dir"], "guides_base.json"), encoding="utf-8"))
    rows, problems = [], []
    for slug, g in base.items():
        html = g["content_html"]
        key = "rt-" + slug
        if key in texts:
            t = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", texts[key].strip())
            if t.startswith("<"):
                html = t
            else:
                problems.append(key + ": not html")
        if BOARD_RE.search(re.sub(r"<[^>]+>", " ", html)):
            problems.append(slug + ": names a board")
        rows.append({"subject_id": st["subject_id"], "slug": slug, "guide_type": g["guide_type"],
                     "title": g["title"], "sort_order": g["sort_order"], "content_html": html})
    drv.write_json(os.path.join(cfg["run_dir"], "guide_rows.json"), rows)
    print("rows ready: %d | errors: %s | problems: %s" % (len(rows), errors or "none",
                                                          problems or "none"))
    if problems or errors:
        print("NOT inserted; fix and re-run pollguides")
        return
    existing = drv.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=id"
                        % st["subject_id"])
    if existing:
        print("ABORT: %d guide rows already exist" % len(existing))
        return
    drv.supa(cfg, "POST", "/rest/v1/guide_pages", rows, prefer="return=minimal")
    print("inserted %d guide pages (%s)" % (len(rows), ", ".join(r["slug"] for r in rows)))


# ---------------------------------------------------------------- stage: gate

OPTIONS = {
    "area1": {
        "label": "Area of Study 1 religion",
        "helper": "The religion studied for Area of Study 1: Religion and Ethics",
        "required": True,
        "choices": [{"name": "Christianity", "slug": "area1-christianity"},
                    {"name": "Catholic Christianity", "slug": "area1-catholic-christianity"}],
    },
    "area2": {
        "label": "Area of Study 2 religion",
        "helper": ("A second religion for Area of Study 2: Religion, Peace and Conflict. It must be "
                   "a different religion from the first area of study, and Catholic Christianity "
                   "and Christianity count as the same religion for that rule."),
        "required": True,
        "choices": [{"name": "Islam", "slug": "area2-islam"},
                    {"name": "Judaism", "slug": "area2-judaism"}],
    },
}


def stage_gate(cfg):
    """settings.options, question_type_names, has_exam_guides, unit images."""
    st = drv.load_state(cfg)
    subject = drv.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&school_id=is.null"
                       "&select=id,settings" % cfg["slug"])[0]
    units = drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug,image_url"
                     "&order=sort_order" % subject["id"])
    settings = dict(subject.get("settings") or {})
    settings["options"] = OPTIONS
    settings["question_type_names"] = QUESTION_TYPES
    settings["has_exam_guides"] = False
    settings["practice_units"] = []
    positions = dict(settings.get("unit_image_positions") or {})
    for u in units:
        positions[u["slug"]] = "center center"
        if not (u.get("image_url") or "").strip():
            rows = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.1"
                            "&select=hero_image_url" % u["id"])
            hero = (rows[0].get("hero_image_url") if rows else None)
            if hero:
                drv.supa(cfg, "PATCH", "/rest/v1/units?id=eq.%s" % u["id"], {"image_url": hero})
                print("unit image set:", u["slug"])
    settings["unit_image_positions"] = positions
    drv.supa(cfg, "PATCH", "/rest/v1/subjects?id=eq.%s" % subject["id"], {"settings": settings})
    print("settings written: options(area1/area2), question_type_names(%d), has_exam_guides=False"
          % len(QUESTION_TYPES))


# ---------------------------------------------------------------- stage: verify

def stage_verify(cfg):
    """Row-level check of everything the student sees, before the browser pass."""
    st = drv.load_state(cfg)
    units = drv.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug,name,image_url,"
                     "lesson_count&order=sort_order" % st["subject_id"])
    bad_text = re.compile(r"\[object Object\]|undefined|NaN|&mdash;|&amp;|&nbsp;")
    issues, n = [], 0
    for u in units:
        if not (u.get("image_url") or "").strip():
            issues.append("unit %s has no image_url" % u["slug"])
        rows = drv.supa(cfg, "GET", "/rest/v1/lessons?unit_id=eq.%s&select=id,lesson_number,title,"
                        "slug,description,content_html,exam_tip_html,conclusion_html,"
                        "practice_questions,knowledge_checks,flashcard_questions,glossary_terms,"
                        "related_media,hero_image_url,hero_image_caption,narration_manifest,status"
                        "&order=lesson_number" % u["id"])
        if len(rows) != u["lesson_count"]:
            issues.append("unit %s lesson_count %s but %d rows" % (u["slug"], u["lesson_count"], len(rows)))
        for l in rows:
            n += 1
            k = "%s/%s" % (u["slug"], l["lesson_number"])
            for f in ("content_html", "exam_tip_html", "conclusion_html", "description",
                      "hero_image_url", "hero_image_caption"):
                if not (l.get(f) or "").strip():
                    issues.append("%s missing %s" % (k, f))
            for f, want in (("practice_questions", 6), ("knowledge_checks", 5)):
                got = len(l.get(f) or [])
                if got != want:
                    issues.append("%s %s = %d (want %d)" % (k, f, got, want))
            # FLASHCARD_RULES.md post-retrofit: 8-15 per lesson, 6-18 tolerated
            nfc = len(l.get("flashcard_questions") or [])
            if not (6 <= nfc <= 18):
                issues.append("%s flashcard_questions = %d (want 8-15)" % (k, nfc))
            media = sum(len(c.get("items") or []) for c in (l.get("related_media") or []))
            if media < 9:            # 8 real items + the Lesson Podcast placeholder
                issues.append("%s related_media has %d items" % (k, media))
            if not (l.get("narration_manifest") or []):
                issues.append("%s has no narration" % k)
            if l.get("status") != "pending_review":
                issues.append("%s status is %s" % (k, l.get("status")))
            visible = re.sub(r"<[^>]+>", " ", " ".join(
                str(l.get(f) or "") for f in ("content_html", "exam_tip_html", "conclusion_html",
                                              "description", "hero_image_caption")))
            blob = visible + " " + json.dumps(
                [l.get(f) for f in ("practice_questions", "knowledge_checks",
                                    "flashcard_questions", "glossary_terms")], ensure_ascii=False)
            for m in set(bad_text.findall(blob)):
                issues.append("%s visible text contains %r" % (k, m))
            for m in set(BOARD_RE.findall(blob)):
                issues.append("%s names the board %r" % (k, m))
            for h in drv.drift_grep(blob):
                issues.append("%s drift: %s" % (k, h[:120]))
    guides = drv.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=slug,guide_type"
                      % st["subject_id"])
    if len(guides) != 8:
        issues.append("guide pages: %d (want index + 7 techniques)" % len(guides))
    if any(g["guide_type"] != "revision-technique" for g in guides):
        issues.append("a non revision-technique guide exists")
    print("checked %d lessons, %d units, %d guides" % (n, len(units), len(guides)))
    if issues:
        print("ISSUES (%d):" % len(issues))
        for i in issues:
            print("  -", i)
    else:
        print("VERIFY PASS")


STAGES = dict(drv.STAGES)
STAGES.update({"plan": stage_plan, "prep": stage_prep, "canary": stage_canary,
               "submit": stage_submit, "factcheck": stage_factcheck, "heroes": stage_heroes,
               "narrate": stage_narrate, "guides": stage_guides, "pollguides": stage_pollguides,
               "gate": stage_gate, "verify": stage_verify})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    STAGES[args.stage](drv.load_config(args.config))


if __name__ == "__main__":
    main()
