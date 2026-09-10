# -*- coding: utf-8 -*-
"""Practice factory for the GCSE Latin language units.

Component 1 (Latin Language) is 50% of the qualification and is assessed almost
entirely through short deterministic tasks — vocabulary, accidence, syntax and
translation — so its three units are practice-format. This script is the
subject-specific factory that fills `lessons.practice_data`, following
`docs/PRACTICE_PIPELINE.md` and the language precedent in
`scripts/language-practice/PRACTICE_DATA_SCHEMA.md`.

Latin differs from the modern languages in two ways that change the input-type
set: there is no listening or speaking assessment, so `dictation` and
`role_play` are banned; and translation into Latin is restricted by the
specification to simple single-clause sentences drawn from a 101-word list.

Stages (each resumable; batch ids live in the driver's state.json):

    words     partition the 440-word list across the four vocabulary lessons
    s1 / polls1   method card, exam context and the Bronze bank
    s2 / polls2   the Silver bank and its worked example
    s3 / polls3   the Gold bank, the third worked example and AI marking prompts
    assemble      merge, validate shapes and tier counts
    insert        PATCH practice_data onto the lesson rows

Usage: python scripts/_content_latin-eduqas/practice_latin.py <stage>
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")

ALLOWED_TYPES = ["vocab_match", "gap_fill", "multiple_choice", "translate",
                 "sentence_builder", "spot_correct", "reorder", "ai_mark"]

POLICY = """
LATIN PRACTICE POLICY — read before anything else

TARGET LANGUAGE: Latin. `target_lang` is always "la".

ALLOWED input_type values, and NOTHING else:
  vocab_match, gap_fill, multiple_choice, translate, sentence_builder,
  spot_correct, reorder, ai_mark

BANNED input types and why:
  - `dictation` — this qualification has no listening assessment and there is no
    Latin text-to-speech voice on the platform. Never emit one.
  - `role_play` — there is no speaking assessment.
  - any maths type (single_value, fraction, standard_form, two_solutions).

WHAT THE LANGUAGE PAPER ACTUALLY ASKS, so the drilling matches it:
  - comprehension questions in English on a Latin narrative;
  - translation of a passage of Latin into English;
  - and, in a short final section, EITHER translation of a small number of
    simple single-clause sentences from English into Latin, OR the recognition,
    analysis and explanation of accidence and syntax in a short Latin passage.
  - derivation links between Latin and English are also assessed.

TRANSLATION DIRECTION RULES:
  - `translate` with direction "to_english" is the main event. Source text is
    Latin, written WITHOUT macrons, using only defined-vocabulary words (any
    other word must be glossed inside the `hints` array, exactly as the real
    paper glosses it).
  - `translate` with direction "to_target" (English into Latin) is allowed ONLY
    under the specification's restrictions: single-clause sentences; third
    person singular and plural only; present, imperfect and perfect indicative
    active only; first conjugation verbs only; first and second declension nouns
    and adjectives only, nominative and accusative only; common prepositions;
    and only words from the dedicated English-into-Latin list supplied to you.
    At most ONE such problem per lesson, and only at Gold.

LATIN STYLE:
  - No macrons anywhere. The defined vocabulary list is printed without them.
  - Quantities of vocabulary must come from the word list supplied for THIS
    lesson. Do not reach for words outside the defined list without glossing
    them.
  - Grammatical terms students meet: nominative, accusative, genitive, dative,
    ablative, vocative; declension, conjugation, principal parts, indicative,
    subjunctive, participle, deponent, infinitive.

HOUSE RULES (identical to the article lessons):
  - Never name the exam board. Never use a specification, paper, component or
    section code. Write "the language paper", "the short final section",
    "your exam", "the specification".
  - Never invent a mark tariff for the paper itself. The `marks` integer on an
    AI-marked problem is a StudyVault marking weight for the tutor, not a claim
    about the real paper: keep it between 3 and 10.
  - This qualification is NOT tiered. Never set `higher_only`, never mention
    Foundation or Higher.
  - British English throughout.
  - Never reproduce a real exam question or an exam board mark scheme.
  - AI marking prompts address a "GCSE tutor", never an examiner of a named
    board, and reward insight over format.
"""

SCHEMA_TAIL = """
SHAPE RULES THE RENDERER ENFORCES (get these wrong and the problem will not draw)

vocab_match: {"input_type","question","pairs":[{"left": Latin,"right": English}, ...]}
  5-7 pairs, drawn only from this lesson's word list.

gap_fill: {"input_type","question","sentence_parts":[...],"gaps":[{"answer","accept":[...],
  "rule","correct_explain","wrong":{...}}],"word_bank":[...] or omitted}
  `sentence_parts` has exactly one more entry than `gaps`. `wrong` maps a
  plausible wrong form to an explanation of why it is wrong (1-3 entries).
  Bronze uses a `word_bank` (the answers plus 1-3 distractors); Silver and Gold
  omit `word_bank` and add `"english"`, the English meaning of the sentence.

multiple_choice: {"input_type","question","options":[4 strings],"solutions":[index]}
  Never prefix an option with "A." — the renderer adds the letters.

translate: {"input_type","direction":"to_english"|"to_target","source_text",
  "target_lang":"la","model_answers":[...],"hints":[...] or null,"marks",
  "ai_system_prompt"}
  The prompt uses the literal placeholders {source} and {model}.

sentence_builder: {"input_type","question","english","correct_order":[words],
  "distractors":[...],"distractor_labels":{word: why it is wrong}}
  Punctuation stays attached to the final word.

spot_correct: {"input_type","question","sentence","error_word","correction",
  "accept_corrections":[...],"error_type","explanation","translation"}
  EXACTLY ONE error in the sentence; everything else must be correct Latin.

reorder: {"input_type","question","items":[shuffled words],"correct_order":[indices]}
  `correct_order[i]` is the index in `items` of the word that belongs in
  position i. Keep sentences to 5-8 words.

ai_mark: {"input_type","question","marks","ai_system_prompt"}

worked example step: {"label","content"} and the FINAL step carries
  "isAnswer": true.
"""


# ------------------------------------------------------------------ helpers

def load(cfg, name):
    p = os.path.join(cfg["run_dir"], name)
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save(cfg, name, obj):
    D.write_json(os.path.join(cfg["run_dir"], name), obj)


def practice_lessons(plan):
    out = []
    for u in plan["practice_units"]:
        for l in u["lessons"]:
            out.append((u, l))
    return out


def shared_system(cfg):
    schema_doc = D.read(os.path.join(REPO, "scripts", "language-practice",
                                     "PRACTICE_DATA_SCHEMA.md"))
    pipeline_doc = D.read(os.path.join(cfg["docs_dir"], "PRACTICE_PIPELINE.md"))
    ref = json.load(io.open(cfg["reference_practice"], encoding="utf-8"))
    spec = D.read(cfg["spec_md"])
    return [
        {"type": "text", "text":
         "You are the practice-lesson factory for StudyVault, a GCSE revision "
         "platform. You are building drilling content for GCSE Latin. Your "
         "output is JSON consumed directly by the practice renderer — the shape "
         "must be exact. Return ONLY the JSON object, no code fences, no "
         "commentary.\n" + POLICY + SCHEMA_TAIL},
        {"type": "text", "text":
         "REFERENCE DOC — language practice data schema:\n\n" + schema_doc
         + "\n\nREFERENCE DOC — practice pipeline quality rules:\n\n"
         + pipeline_doc},
        {"type": "text", "text":
         "STRUCTURAL REFERENCE — a shipped language practice lesson "
         "(match its shape and its depth of explanation, not its language or "
         "its content):\n" + json.dumps(ref.get("practice_data"),
                                        ensure_ascii=False)},
        {"type": "text", "text":
         "SUBJECT CONTEXT — the specification, the assessment rules, the house "
         "rules and the complete defined vocabulary lists:\n" + spec},
    ]


def lesson_words(cfg, unit_slug, number):
    """The vocabulary slice this lesson owns, if any."""
    part = load(cfg, "practice_words.json")
    if unit_slug != "vocabulary" or not part:
        return None
    return part.get(str(number))


def lesson_brief(cfg, u, l):
    words = lesson_words(cfg, u["slug"], l["number"])
    brief = ("UNIT: %s — %s\nLESSON %d of %d: %s\nDESCRIPTION: %s\n"
             "WHAT THIS LESSON DRILLS: %s\n"
             % (u["name"], u.get("subtitle", ""), l["number"], len(u["lessons"]),
                l["title"], l.get("description", ""),
                "; ".join(l.get("section_markers", []))))
    if words:
        brief += ("\nTHIS LESSON'S VOCABULARY SLICE (%d words from the defined "
                  "list — every problem must draw on these and no others):\n%s\n"
                  % (len(words), "\n".join("%s = %s" % (w["latin"], w["english"])
                                           for w in words)))
    return brief


# ------------------------------------------------------------------ stage: words

NOUNS_PROMPT = """You are splitting the noun entries of the GCSE Latin defined vocabulary list between two revision lessons.

Lesson 1 — People, Family and Society: nouns naming a person, a group of people, a role, a rank, a relationship, a god or goddess, or an abstract quality of people and social life (courage, anger, care, love, danger to people, and so on).

Lesson 3 — Places, Objects and the Physical World: nouns naming a place, a building, part of a building, the natural world, an animal, food or drink, the body, weapons, ships, objects, money, and units of time.

RULES
- Every entry given to you goes into exactly one lesson. None may be dropped and none may appear twice.
- If a noun could sit in either, put it where a student would most expect it: a personal quality goes to 1, a physical thing goes to 3.
- Return each entry EXACTLY as given, character for character.

Return ONLY this JSON, no code fences: {"1": ["<entry>", ...], "3": ["<entry>", ...]}
"""

# Deterministic part-of-speech signals. Everything the regexes cannot decide is
# sent to the model, so nothing is guessed silently.
VERB_RE = re.compile(
    r"^[a-z]+(?:o|or|eo|io|ior),\s+[a-z]+(?:are|ere|ire|ari|eri|iri|ri|esse|ferre|velle|nolle|ire)\b")
IRREG_VERBS = ("sum, esse", "possum, posse", "absum, abesse", "adsum, adesse",
               "eo, ire", "fero, ferre", "volo, velle", "nolo, nolle",
               "coepi, coepisse", "inquit", "aufero, auferre", "refero, referre",
               "malo, malle", "redeo, redire", "exeo, exire", "abeo, abire",
               "transeo, transire", "ineo, inire", "pereo, perire")
NOUN_RE = re.compile(r",\s*(?:m|f|n|m\.f)\.(?:\s|$|\s*pl\.)")
FUNC_RE = re.compile(r"\(indecl\.\)|\+\s*(?:acc|abl|dat)\b|^-ne\b")


def pos_of(latin):
    l = latin.strip()
    if any(l.startswith(v) for v in IRREG_VERBS) or VERB_RE.match(l):
        return "verb"
    if FUNC_RE.search(l):
        return "function"
    if NOUN_RE.search(l):
        return "noun"
    return "other"          # adjectives, pronouns, numerals -> lesson 4


def stage_words(cfg):
    dvl = json.load(io.open(os.path.join(cfg["build_dir"], "dvl.json"),
                            encoding="utf-8"))["dvl_latin_english"]
    buckets = {"verb": [], "function": [], "noun": [], "other": []}
    for p in dvl:
        buckets[pos_of(p["latin"])].append(p)
    print("part of speech: " + ", ".join("%s=%d" % (k, len(v))
                                         for k, v in buckets.items()))

    nouns = buckets["noun"]
    listing = "\n".join("%s = %s" % (p["latin"], p["english"]) for p in nouns)
    cl = D.client()
    with cl.messages.stream(
        model=D.MODEL_CONTENT, max_tokens=16000,
        system=[{"type": "text", "text": NOUNS_PROMPT}],
        messages=[{"role": "user", "content":
                   "THE NOUN ENTRIES (%d):\n%s\n\nSplit them."
                   % (len(nouns), listing)}],
    ) as stream:
        msg = stream.get_final_message()
    rec = D.log_usage(cfg, "practice-words", D.MODEL_CONTENT, "words", msg.usage)
    text = "".join(b.text for b in msg.content if b.type == "text")
    got = D.parse_json_reply(text)

    by_latin = {p["latin"]: p for p in nouns}
    out = {"1": [], "2": list(buckets["verb"]), "3": [],
           "4": buckets["function"] + buckets["other"]}
    seen = set()
    for key in ("1", "3"):
        for w in got.get(key, []):
            # the model may echo the whole "headword = gloss" line
            head = w.split(" = ")[0].strip()
            p = by_latin.get(head)
            if p and head not in seen:
                seen.add(head)
                out[key].append(p)
    # any noun the model dropped still has to be drilled: default to the
    # physical-world lesson rather than lose it
    stranded = [p for p in nouns if p["latin"] not in seen]
    out["3"] += stranded
    for k in out:
        out[k].sort(key=lambda p: p["latin"])

    total = sum(len(v) for v in out.values())
    save(cfg, "practice_words.json", out)
    print("partition ($%.3f): %s  stranded nouns auto-placed=%d  total=%d/%d"
          % (D.cost_of(rec), {k: len(v) for k, v in out.items()},
             len(stranded), total, len(dvl)))
    assert total == len(dvl), "partition lost or duplicated entries"


# ------------------------------------------------------------------ stages 1-3

STAGE_SPECS = {
    "s1": {
        "name": "practice-s1",
        "ask": """Produce stage one of this lesson: the method card, the exam context and the Bronze problem bank.

Return ONLY:
{
  "method_card": {"title": "<the lesson title>", "content": "<HTML, 200-400 words>", "steps": ["<3-5 imperative steps>"]},
  "exam_context": {"paper": "<plain description of where this is assessed, no codes>", "marks": "<honest phrase, never an invented tariff>", "frequency": "<how often it comes up>"},
  "worked_examples": [ <exactly one Bronze worked example: {"difficulty": "bronze", "question": ..., "steps": [{"label","content"}, ..., {"label","content","isAnswer": true}]} > ],
  "problem_bank": {"bronze": [ <exactly 8 problems> ]}
}

The method card is STRATEGY plus the minimum reference table a student needs: for a vocabulary lesson, an HTML table of the 12-15 highest-value words in this lesson's slice; for an accidence lesson, the paradigm table being drilled; for a syntax lesson, the pattern and how to spot it. Then a worked model sentence with its English. Do not write a mini-article.

Bronze composition (8 problems, in this order):
  1-2  vocab_match, 6 pairs each, different words
  3-4  gap_fill WITH word_bank, one testing form, one testing meaning
  5-6  multiple_choice (recognising a form, a case, a tense or a meaning)
  7    translate direction "to_english", one short sentence, hints supplied
  8    reorder (5-8 words) OR spot_correct, whichever suits the lesson""",
    },
    "s2": {
        "name": "practice-s2",
        "ask": """Produce stage two of this lesson: the Silver problem bank and its worked example. Stage one is supplied below; do NOT repeat any of its sentences, words in the same pairing, or explanations.

Return ONLY:
{
  "worked_examples": [ <exactly one Silver worked example, same shape as stage one's> ],
  "problem_bank": {"silver": [ <exactly 6 problems> ]}
}

Silver composition (6 problems, in this order):
  1-2  gap_fill with NO word_bank, each carrying an "english" field
  3    spot_correct (exactly one error)
  4    sentence_builder (0-1 distractors, with distractor_labels)
  5    translate direction "to_english", a longer sentence, hints still supplied
  6    multiple_choice or reorder, testing the same grammar at greater length

Silver is a real step up from Bronze: longer sentences, less scaffolding, and the distractors must be the mistakes a student actually makes (wrong case, wrong tense, wrong person, adjective not agreeing).""",
    },
    "s3": {
        "name": "practice-s3",
        "ask": """Produce stage three of this lesson: the Gold problem bank, the Gold worked example and the lesson's AI marking prompts. Stages one and two are supplied below; do NOT repeat their sentences or explanations.

Return ONLY:
{
  "worked_examples": [ <exactly one Gold worked example, same shape as before> ],
  "problem_bank": {"gold": [ <exactly 6 problems> ]},
  "ai_marking_prompts": {"translate_to_english": "<system prompt>", "translate_to_latin": "<system prompt>", "grammar_explanation": "<system prompt>"}
}

Gold composition (6 problems, in this order):
  1-2  translate direction "to_english", multi-clause sentences, hints null
  3    sentence_builder with 2-3 distractors
  4    gap_fill (no word_bank) or spot_correct on the hardest point in the lesson
  5    translate direction "to_target" — English into Latin, and it MUST obey the
       restrictions in the policy above (single clause, third person, first
       conjugation, first and second declension, words from the English-into-Latin
       list). If this lesson's grammar cannot be tested that way, use another
       translate "to_english" instead and say nothing about it.
  6    ai_mark — either an extended translation, or a task asking the student to
       identify and explain the accidence and syntax in a short Latin sentence
       (which is exactly what the short final section allows as the alternative).

The ai_marking_prompts are shared system prompts using the literal placeholders {source} and {model}. Each must ask for the JSON reply the platform expects: {"quality":"excellent|good|needs_work|not_valid","feedback":"...","improvement":"..."}.""",
    },
}


def build_requests(cfg, plan, stage):
    spec = STAGE_SPECS[stage]
    system = shared_system(cfg)
    system = [{k: v for k, v in b.items() if k != "cache_control"} for b in system]
    prior = {}
    for earlier in ("s1", "s2"):
        if earlier == stage:
            break
        prior[earlier] = load(cfg, "practice_%s.json" % earlier)
        if stage == "s2":
            break
    reqs = []
    for u, l in practice_lessons(plan):
        cid = D.lesson_key(u["slug"], l["number"])
        user = lesson_brief(cfg, u, l) + "\n"
        for earlier, blob in prior.items():
            if cid in blob:
                user += ("\n<%s_output>\n%s\n</%s_output>\n"
                         % (earlier, json.dumps(blob[cid], ensure_ascii=False), earlier))
        user += "\n" + spec["ask"]
        reqs.append({"custom_id": cid, "params": {
            "model": D.MODEL_CONTENT, "max_tokens": 24000,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }})
    return reqs


def stage_submit(cfg, plan, stage):
    reqs = build_requests(cfg, plan, stage)
    cl = D.client()
    batch = cl.messages.batches.create(requests=reqs)
    st = D.load_state(cfg)
    st["practice_%s_batch" % stage] = batch.id
    D.save_state(cfg, st)
    print("%s batch submitted: %s (%d requests, user msgs avg %dk chars)"
          % (stage, batch.id, len(reqs),
             sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
             // max(1, len(reqs)) // 1000))


def stage_poll(cfg, stage):
    st = D.load_state(cfg)
    out = D.collect_batch(cfg, st["practice_%s_batch" % stage],
                          STAGE_SPECS[stage]["name"], "raw_practice_" + stage)
    if out is None:
        return
    texts, errors = out
    got = load(cfg, "practice_%s.json" % stage)
    bad = {}
    for cid, text in sorted(texts.items()):
        try:
            got[cid] = D.parse_json_reply(text)
        except Exception as e:
            bad[cid] = str(e)
    save(cfg, "practice_%s.json" % stage, got)
    print("%s: %d parsed, %d unparseable %s, %d errored %s"
          % (stage, len(got), len(bad), bad or "", len(errors), errors or ""))


# ------------------------------------------------------------------ assemble

TIER_TARGET = {"bronze": 8, "silver": 6, "gold": 6}


def check_problem(p):
    t = p.get("input_type")
    probs = []
    if t not in ALLOWED_TYPES:
        return ["input_type %r not allowed" % t]
    if t == "vocab_match":
        pairs = p.get("pairs") or []
        if not (5 <= len(pairs) <= 7):
            probs.append("vocab_match has %d pairs" % len(pairs))
        for pr in pairs:
            if not (pr.get("left") and pr.get("right")):
                probs.append("vocab_match pair missing a side")
    elif t == "gap_fill":
        gaps = p.get("gaps") or []
        parts = p.get("sentence_parts") or []
        if len(parts) != len(gaps) + 1:
            probs.append("gap_fill sentence_parts %d vs gaps %d"
                         % (len(parts), len(gaps)))
        for g in gaps:
            if not g.get("answer") or not isinstance(g.get("accept"), list):
                probs.append("gap missing answer/accept")
            if not g.get("correct_explain"):
                probs.append("gap missing correct_explain")
    elif t == "multiple_choice":
        if len(p.get("options") or []) != 4:
            probs.append("multiple_choice needs 4 options")
        sol = p.get("solutions")
        if not (isinstance(sol, list) and sol and all(isinstance(i, int) for i in sol)):
            probs.append("multiple_choice solutions must be a list of indices")
        for o in p.get("options") or []:
            if re.match(r"^[A-D][.)]\s", o or ""):
                probs.append("option is letter-prefixed: %r" % o)
    elif t == "translate":
        if p.get("direction") not in ("to_english", "to_target"):
            probs.append("translate direction %r" % p.get("direction"))
        if not p.get("source_text"):
            probs.append("translate missing source_text")
        if not (p.get("model_answers") or []):
            probs.append("translate missing model_answers")
        if not p.get("ai_system_prompt"):
            probs.append("translate missing ai_system_prompt")
        if p.get("target_lang") != "la":
            probs.append("translate target_lang %r" % p.get("target_lang"))
    elif t == "sentence_builder":
        if not (p.get("correct_order") or []):
            probs.append("sentence_builder missing correct_order")
        for d in p.get("distractors") or []:
            if d not in (p.get("distractor_labels") or {}):
                probs.append("distractor %r has no label" % d)
    elif t == "spot_correct":
        for k in ("sentence", "error_word", "correction", "explanation"):
            if not p.get(k):
                probs.append("spot_correct missing %s" % k)
        if p.get("error_word") and p.get("sentence") and \
                p["error_word"] not in p["sentence"]:
            probs.append("spot_correct error_word not in sentence")
    elif t == "reorder":
        items = p.get("items") or []
        order = p.get("correct_order") or []
        if len(items) != len(order) or sorted(order) != list(range(len(items))):
            probs.append("reorder correct_order is not a permutation of items")
    elif t == "ai_mark":
        if not p.get("ai_system_prompt"):
            probs.append("ai_mark missing ai_system_prompt")
    m = p.get("marks")
    if m is not None and not (isinstance(m, int) and 1 <= m <= 12):
        probs.append("marks %r out of range" % m)
    if p.get("higher_only"):
        probs.append("higher_only set on a non-tiered subject")
    return probs


def stage_assemble(cfg, plan):
    s1, s2, s3 = (load(cfg, "practice_%s.json" % s) for s in ("s1", "s2", "s3"))
    out, report = {}, {}
    for u, l in practice_lessons(plan):
        cid = D.lesson_key(u["slug"], l["number"])
        a, b, c = s1.get(cid), s2.get(cid), s3.get(cid)
        if not (a and b and c):
            report[cid] = ["missing stage output: %s"
                           % ",".join(n for n, x in (("s1", a), ("s2", b), ("s3", c))
                                      if not x)]
            continue
        pd = {
            "method_card": a["method_card"],
            "exam_context": a["exam_context"],
            "worked_examples": (a.get("worked_examples", [])
                                + b.get("worked_examples", [])
                                + c.get("worked_examples", [])),
            "problem_bank": {
                "bronze": a["problem_bank"]["bronze"],
                "silver": b["problem_bank"]["silver"],
                "gold": c["problem_bank"]["gold"],
            },
            "ai_marking_prompts": c.get("ai_marking_prompts", {}),
            "topic_links": {"prerequisites": []},
        }
        probs = []
        for tier, want in TIER_TARGET.items():
            n = len(pd["problem_bank"][tier])
            if n != want:
                probs.append("%s has %d problems (want %d)" % (tier, n, want))
            for i, p in enumerate(pd["problem_bank"][tier]):
                probs += ["%s[%d] %s" % (tier, i, x) for x in check_problem(p)]
        for i, w in enumerate(pd["worked_examples"]):
            # the renderer lowercases this, but keep the stored value canonical
            w["difficulty"] = (w.get("difficulty") or "").lower()
            steps = w.get("steps") or []
            if not steps or not steps[-1].get("isAnswer"):
                probs.append("worked_example[%d] final step missing isAnswer" % i)
        tiers = [w.get("difficulty") for w in pd["worked_examples"]]
        if sorted(tiers) != ["bronze", "gold", "silver"]:
            probs.append("worked example tiers %s (want one each)" % tiers)
        blob = json.dumps(pd, ensure_ascii=False)
        probs += D.drift_grep(blob)
        for banned in ("Eduqas", "WJEC", "C580QS", "higher tier", "Higher tier",
                       "dictation", "role_play"):
            if banned in blob:
                probs.append("banned string present: %s" % banned)
        if probs:
            report[cid] = probs
        out[cid] = pd

    # sequential topic links within each unit
    for u in plan["practice_units"]:
        for l in u["lessons"]:
            cid = D.lesson_key(u["slug"], l["number"])
            if cid not in out:
                continue
            links = []
            for other in u["lessons"]:
                if other["number"] in (l["number"] - 1, l["number"] + 1):
                    links.append({"title": other["title"],
                                  "slug": "%s/%d" % (u["slug"], other["number"])})
            out[cid]["topic_links"] = {"prerequisites": links}

    save(cfg, "practice_data.json", out)
    print("assembled %d practice lessons" % len(out))
    if report:
        print("PROBLEMS:")
        for cid, probs in sorted(report.items()):
            print(" ", cid)
            for p in probs[:12]:
                print("    -", p)
    else:
        print("all practice lessons pass shape + tier + drift checks")
    save(cfg, "practice_report.json", report)


# ------------------------------------------------------------------ insert

def stage_insert(cfg, plan):
    st = D.load_state(cfg)
    data = load(cfg, "practice_data.json")
    report = load(cfg, "practice_report.json")
    units = D.supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug"
                   % st["subject_id"])
    uid = {u["slug"]: u["id"] for u in units}
    n = 0
    for u, l in practice_lessons(plan):
        cid = D.lesson_key(u["slug"], l["number"])
        if cid not in data:
            print("SKIP (no assembled data):", cid)
            continue
        if report.get(cid):
            print("SKIP (unresolved problems):", cid)
            continue
        D.supa(cfg, "PATCH",
               "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s"
               % (uid[u["slug"]], l["number"]),
               {"practice_data": data[cid], "description": l["description"],
                "status": "pending_review", "youtube_video_id": "practice-only"})
        n += 1
    print("practice_data written to %d lessons" % n)


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["words", "s1", "polls1", "s2", "polls2",
                                      "s3", "polls3", "assemble", "insert"])
    args = ap.parse_args()
    cfg = D.load_config(CFG_PATH)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"),
                             encoding="utf-8"))
    s = args.stage
    if s == "words":
        stage_words(cfg)
    elif s in ("s1", "s2", "s3"):
        stage_submit(cfg, plan, s)
    elif s.startswith("poll"):
        stage_poll(cfg, s[4:])
    elif s == "assemble":
        stage_assemble(cfg, plan)
    elif s == "insert":
        stage_insert(cfg, plan)


if __name__ == "__main__":
    main()
