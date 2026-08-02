# -*- coding: utf-8 -*-
"""StudyVault Batch-API subject build driver.

Deterministic pipeline that replaces subscription agents with Anthropic API
calls (Batch API + prompt caching) for commercial content generation.
Agents are single-shot and never hold DB keys — this driver does every
Supabase read/write itself. All context is pre-packed into prompts from the
same docs the subscription pipeline uses (docs/CONTENT_PROMPT.md etc.), so
output contracts and validators are unchanged.

Stages (run in order; each is resumable/idempotent via the run dir):

    python driver.py --config config_psychology-ocr.json plan
    python driver.py --config ... plancheck
    python driver.py --config ... activate
    python driver.py --config ... prep
    python driver.py --config ... submit          # warm cache + submit content batch
    python driver.py --config ... poll            # poll batch; on end: download + validate
    python driver.py --config ... fix             # resubmit validation failures
    python driver.py --config ... factcheck       # Opus + web search verification batch
    python driver.py --config ... applyfixes      # apply HIGH/MEDIUM corrections
    python driver.py --config ... insert          # write lessons to Supabase (pending_review)
    python driver.py --config ... costs           # spend report from the ledger

Every API response's usage lands in {run_dir}/costs.jsonl. `costs` prints
the exact spend per stage — this build is the calibration datapoint for
API_GENERATION_COSTS.md.
"""
import argparse
import importlib.util
import io
import json
import os
import re
import sys
import time
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import anthropic

SUPA = "https://baipckgywpnwapobwtsy.supabase.co"

MODEL_CONTENT = "claude-sonnet-5"
MODEL_PLAN = "claude-opus-4-8"
MODEL_FACTCHECK = "claude-opus-5"

# $/MTok. Sonnet 5 is intro pricing through 2026-08-31.
PRICES = {
    "claude-sonnet-5": {"in": 2.0, "out": 10.0},
    "claude-opus-4-8": {"in": 5.0, "out": 25.0},
    "claude-opus-5": {"in": 5.0, "out": 25.0},
}
WEB_SEARCH_PER_1K = 10.0


# ---------------------------------------------------------------- helpers

def load_config(path):
    cfg = json.load(io.open(path, encoding="utf-8"))
    os.makedirs(cfg["run_dir"], exist_ok=True)
    os.makedirs(os.path.join(cfg["run_dir"], "lessons"), exist_ok=True)
    return cfg


def read(path):
    return io.open(path, encoding="utf-8").read()


def write_json(path, obj):
    io.open(path, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False, indent=1))


def state_path(cfg):
    return os.path.join(cfg["run_dir"], "state.json")


def load_state(cfg):
    p = state_path(cfg)
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save_state(cfg, st):
    write_json(state_path(cfg), st)


def log_usage(cfg, stage, model, key, usage, batch=False):
    """Append one usage record to the cost ledger."""
    u = usage if isinstance(usage, dict) else usage.model_dump()
    cc = u.get("cache_creation") or {}
    stu = u.get("server_tool_use") or {}
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stage": stage, "model": model, "key": key, "batch": batch,
        "input_tokens": u.get("input_tokens", 0),
        "output_tokens": u.get("output_tokens", 0),
        "cache_read": u.get("cache_read_input_tokens", 0) or 0,
        "cache_write_5m": (cc.get("ephemeral_5m_input_tokens") if cc else None)
            if cc else None,
        "cache_write_1h": (cc.get("ephemeral_1h_input_tokens") if cc else None)
            if cc else None,
        "cache_write_total": u.get("cache_creation_input_tokens", 0) or 0,
        "web_searches": (stu.get("web_search_requests", 0) if isinstance(stu, dict) else 0),
    }
    if rec["cache_write_5m"] is None:
        rec["cache_write_5m"] = rec["cache_write_total"]
        rec["cache_write_1h"] = 0
    with io.open(os.path.join(cfg["run_dir"], "costs.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def cost_of(rec):
    p = PRICES[rec["model"]]
    mult = 0.5 if rec["batch"] else 1.0
    c = (rec["input_tokens"] * p["in"]
         + (rec["cache_write_5m"] or 0) * p["in"] * 1.25
         + (rec["cache_write_1h"] or 0) * p["in"] * 2.0
         + rec["cache_read"] * p["in"] * 0.1
         + rec["output_tokens"] * p["out"]) / 1e6 * mult
    c += rec.get("web_searches", 0) * WEB_SEARCH_PER_1K / 1000.0
    return c


def parse_json_reply(text):
    """Model replies are demanded fence-free, but strip fences defensively."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
        t = re.sub(r"\s*```$", "", t)
    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in reply")
    return json.loads(t[start:end + 1])


def supa(cfg, method, path, body=None, prefer=None):
    key = os.environ["SUPABASE_SERVICE_KEY"]
    headers = {"apikey": key, "Authorization": "Bearer " + key,
               "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(SUPA + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw.strip() else None


def extract_prompt_section(md_text, heading, next_heading):
    """Extract the fenced prompt under `heading`, tolerating nested ``` fences
    inside it (PLANNING_PROMPT.md has one). Takes everything between the first
    fence after the heading and the last fence before the next heading."""
    i = md_text.index(heading)
    j = md_text.index(next_heading, i)
    seg = md_text[i:j]
    a = seg.index("```")
    a = seg.index("\n", a) + 1
    b = seg.rindex("```")
    return seg[a:b]


def slugify(text):
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def client():
    return anthropic.Anthropic()


# ---------------------------------------------------------------- stage: plan

def stage_plan(cfg):
    planning_doc = read(os.path.join(cfg["docs_dir"], "PLANNING_PROMPT.md"))
    system = extract_prompt_section(planning_doc, "## System prompt", "## User message template")
    spec_md = read(cfg["spec_md"])
    aqa_plan = json.load(io.open(cfg["source_plan"], encoding="utf-8"))
    catalog = json.load(io.open(cfg["source_catalog"], encoding="utf-8"))

    existing_plan = {
        "subject": aqa_plan.get("subject"),
        "units": [{"slug": u["slug"], "name": u["name"], "subtitle": u.get("subtitle"),
                   "lesson_count": u.get("lesson_count"),
                   "lesson_titles": [l["title"] for l in u.get("lessons", [])]}
                  for u in aqa_plan.get("article_units", [])],
        "question_type_names": aqa_plan.get("question_type_names"),
        "teaching_brief": aqa_plan.get("teaching_brief"),
    }

    user = (
        "SUBJECT: %s\nEXAM BOARD: %s\nSPEC CODE: %s\nSCHOOL_ID: null\n"
        "TARGET AUDIENCE: free-tier\n\n<spec>\n%s\n</spec>\n\n"
        "<existing_board_plan>\n%s\n</existing_board_plan>\n\n"
        "<existing_board_lessons>\n%s\n</existing_board_lessons>\n\n"
        "Additional constraints for this build:\n"
        "- Subject slug MUST be %s (board-suffixed, matching %s).\n"
        "- source_subject_slug in every content_transfer block MUST be %s.\n"
        "- This is an article-format subject (reference classification in the prompt).\n"
        "Generate the plan JSON."
    ) % (cfg["subject_name"], cfg["exam_board"], cfg["spec_code"], spec_md,
         json.dumps(existing_plan, ensure_ascii=False),
         json.dumps(catalog["lessons"], ensure_ascii=False),
         cfg["slug"], cfg["source_subject_slug"], cfg["source_subject_slug"])

    print("planning call: system %dk chars, user %dk chars" % (len(system) // 1000, len(user) // 1000))
    cl = client()
    with cl.messages.stream(
        model=MODEL_PLAN,
        max_tokens=40000,
        thinking={"type": "adaptive"},
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 12}],
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        msg = stream.get_final_message()

    text = "".join(b.text for b in msg.content if b.type == "text")
    io.open(os.path.join(cfg["run_dir"], "plan_raw.txt"), "w", encoding="utf-8").write(text)
    io.open(os.path.join(cfg["run_dir"], "plan_msg_dump.json"), "w", encoding="utf-8").write(
        json.dumps(msg.model_dump(), ensure_ascii=False, default=str))
    rec = log_usage(cfg, "plan", MODEL_PLAN, "plan", msg.usage)
    print("plan usage: in=%d out=%d searches=%s stop=%s blocks=%s  ($%.3f)" % (
        rec["input_tokens"], rec["output_tokens"], rec["web_searches"],
        msg.stop_reason, [b.type for b in msg.content][:12], cost_of(rec)))
    try:
        plan = parse_json_reply(text)
    except (ValueError, json.JSONDecodeError):
        # Opus with the 2026 search tool family sometimes builds the JSON in
        # the bundled code-execution sandbox and cats it — hunt the tool
        # result blocks for the largest parseable JSON object.
        plan = None
        for b in reversed(msg.model_dump()["content"]):
            blob = json.dumps(b)
            for candidate in re.findall(r'"stdout":\s*"', blob):
                pass
            def hunt(x):
                if isinstance(x, dict):
                    for v in x.values():
                        r = hunt(v)
                        if r:
                            return r
                elif isinstance(x, list):
                    for it in x:
                        r = hunt(it)
                        if r:
                            return r
                elif isinstance(x, str) and x.lstrip().startswith("{") and len(x) > 5000:
                    try:
                        return json.loads(x[x.find("{"):x.rfind("}") + 1])
                    except Exception:
                        return None
                return None
            plan = hunt(b)
            if plan:
                print("plan recovered from a %s block" % b.get("type"))
                break
        if plan is None:
            raise ValueError("no plan JSON found in any content block")
    write_json(os.path.join(cfg["run_dir"], "plan.json"), plan)
    n_lessons = sum(len(u.get("lessons", [])) for u in plan.get("article_units", []))
    print("plan saved: %d units, %d lessons, gaps: %s" % (
        len(plan.get("article_units", [])), n_lessons, plan.get("gaps") or "none"))


# ---------------------------------------------------------------- stage: plancheck

DRIFT_PATTERNS = [
    (r"\bAQA \d{4}\b", "AQA spec code"),
    (r"\bJ\d{3}\b", "OCR spec code"),
    (r"\b\d[A-Z]{2}\d\b", "Edexcel spec code"),
    (r"Component \d", "component code"),
    (r"Paper \d[A-Z]?\b", "paper code"),
    (r"Level [1-9]", "Level descriptor"),
    (r"Nothing worthy of credit", "board rubric phrase"),
]


def drift_grep(text):
    hits = []
    for pat, label in DRIFT_PATTERNS:
        for m in re.finditer(pat, text):
            hits.append("%s: ...%s..." % (label, text[max(0, m.start() - 30):m.end() + 30]))
    return hits


def stage_plancheck(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    problems = []
    units = plan.get("article_units", [])
    if not units:
        problems.append("no article_units")
    if plan.get("practice_units"):
        problems.append("unexpected practice_units for an article subject")
    total = 0
    for u in units:
        ab, ac = u.get("accent_badge", ""), u.get("accent", "")
        if not (len(ab) == 9 and ab.endswith("33") and ab[:7] == ac):
            problems.append("unit %s accent_badge %r not accent+'33' (%r)" % (u.get("slug"), ab, ac))
        for l in u.get("lessons", []):
            total += 1
            if not l.get("content_transfer"):
                problems.append("lesson %s/%s missing content_transfer" % (u.get("slug"), l.get("number")))
            d = l.get("description", "")
            if not (40 <= len(d) <= 120):
                problems.append("lesson %s/%s description length %d" % (u.get("slug"), l.get("number"), len(d)))
    # student-facing drift grep: titles, descriptions, subtitles, question types
    facing = []
    for u in units:
        facing += [u.get("name", ""), u.get("subtitle", "")]
        facing += [l.get("title", "") + " " + l.get("description", "") for l in u.get("lessons", [])]
    facing += plan.get("question_type_names", [])
    hits = drift_grep("\n".join(facing))
    problems += ["drift in student-facing plan text — " + h for h in hits]
    scores = {}
    for u in units:
        for l in u.get("lessons", []):
            s = (l.get("content_transfer") or {}).get("transfer_score", "?")
            scores[s] = scores.get(s, 0) + 1
    print("lessons: %d  transfer mix: %s" % (total, scores))
    if plan.get("gaps"):
        print("GAPS (surface to Tom):")
        for g in plan["gaps"]:
            print("  -", g)
    if problems:
        print("PLANCHECK FAIL (%d):" % len(problems))
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("PLANCHECK PASS")


# ---------------------------------------------------------------- stage: activate

def stage_activate(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    slug = cfg["slug"]
    existing = supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id,slug" % slug)
    if existing:
        print("ABORT: subject %s already exists (%s) — never wipe existing rows" % (slug, existing[0]["id"]))
        sys.exit(1)

    units = plan["article_units"]
    quotes = plan.get("quote_ticker_quotes", [])
    accents = [u["accent"] for u in units] or ["#7c3aed"]

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    items = "".join(
        '<span class="quote-item" style="--q-color: %s;">%s <em>&mdash; %s</em></span>'
        % (accents[i % len(accents)], esc(q["quote"]), esc(q["author"]))
        for i, q in enumerate(quotes))
    ticker = ('<div class="quote-ticker"><div class="quote-ticker-track">%s%s</div></div>'
              % (items, items))

    subject_row = {
        "slug": slug, "name": cfg["subject_name"], "exam_board": cfg["exam_board"],
        "spec_code": cfg["spec_code"], "school_id": None, "status": "live",
        "settings": {"quote_ticker_html": ticker, "practice_units": [],
                     "unit_image_positions": {}},
    }
    created = supa(cfg, "POST", "/rest/v1/subjects", [subject_row], prefer="return=representation")
    subject_id = created[0]["id"]
    print("subject created:", subject_id)

    shells = 0
    for u in units:
        unit_row = {
            "subject_id": subject_id, "slug": u["slug"], "name": u["name"],
            "subtitle": u.get("subtitle"), "body_class": u.get("body_class"),
            "accent": u["accent"], "accent_light": u["accent_light"],
            "accent_badge": u["accent_badge"], "lesson_count": len(u["lessons"]),
            "sort_order": u["sort_order"],
        }
        uc = supa(cfg, "POST", "/rest/v1/units", [unit_row], prefer="return=representation")
        uid = uc[0]["id"]
        rows = [{"unit_id": uid, "lesson_number": l["number"], "title": l["title"],
                 "slug": slugify(l["title"]), "status": "pending_review"}
                for l in u["lessons"]]
        supa(cfg, "POST", "/rest/v1/lessons", rows)
        shells += len(rows)
        print("  unit %-30s %d shells" % (u["slug"], len(rows)))
    st = load_state(cfg)
    st["subject_id"] = subject_id
    save_state(cfg, st)
    print("activation complete: %d units, %d lesson shells" % (len(units), shells))


# ---------------------------------------------------------------- stage: prep

LESSON_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "content_html": {"type": "string"},
        "exam_tip_html": {"type": "string"},
        "conclusion_html": {"type": "string"},
        "practice_questions": {
            "type": "array",
            "items": {"type": "object",
                      "properties": {"text": {"type": "string"}, "type": {"type": "string"},
                                     "marks": {"type": "string"}},
                      "required": ["text", "type", "marks"],
                      "additionalProperties": False},
        },
        "knowledge_checks": {
            "type": "array",
            "items": {"type": "object",
                      "properties": {
                          "type": {"type": "string", "enum": ["mcq", "fill", "match"]},
                          "q": {"type": "string"},
                          "options": {"type": "array", "items": {"type": "string"}},
                          "correct": {"type": "integer"},
                          "left": {"type": "array", "items": {"type": "string"}},
                          "right": {"type": "array", "items": {"type": "string"}},
                          "order": {"type": "array", "items": {"type": "integer"}}},
                      "required": ["type", "q"],
                      "additionalProperties": False},
        },
        "flashcard_questions": {
            "type": "array",
            "items": {"type": "object",
                      "properties": {"q": {"type": "string"}, "a": {"type": "string"}},
                      "required": ["q", "a"], "additionalProperties": False},
        },
        "glossary_terms": {
            "type": "array",
            "items": {"type": "object",
                      "properties": {"term": {"type": "string"}, "definition": {"type": "string"}},
                      "required": ["term", "definition"], "additionalProperties": False},
        },
        "hero_keywords": {"type": "array", "items": {"type": "string"}},
        "hero_image_caption": {"type": "string"},
    },
    "required": ["description", "content_html", "exam_tip_html", "conclusion_html",
                 "practice_questions", "knowledge_checks", "flashcard_questions",
                 "glossary_terms", "hero_keywords", "hero_image_caption"],
    "additionalProperties": False,
}


def shared_system_blocks(cfg, plan):
    """The cached shared prefix: content prompt + reference docs + reference
    lesson + full spec + subject-level brief. Identical across every lesson."""
    content_doc = read(os.path.join(cfg["docs_dir"], "CONTENT_PROMPT.md"))
    sys_prompt = extract_prompt_section(content_doc, "## System prompt", "## User message template")
    lesson_tpl = read(os.path.join(cfg["docs_dir"], "LESSON_TEMPLATE.md"))
    questions_doc = read(os.path.join(cfg["docs_dir"], "QUESTIONS_PIPELINE.md"))
    flashcards_doc = read(os.path.join(cfg["docs_dir"], "FLASHCARD_RULES.md"))
    ref = json.load(io.open(cfg["reference_lesson"], encoding="utf-8"))
    spec_md = read(cfg["spec_md"])

    b = []
    b.append({"type": "text", "text": sys_prompt})
    b.append({"type": "text", "text":
              "REFERENCE DOC — LESSON_TEMPLATE.md:\n\n" + lesson_tpl
              + "\n\nREFERENCE DOC — QUESTIONS_PIPELINE.md:\n\n" + questions_doc
              + "\n\nREFERENCE DOC — FLASHCARD_RULES.md:\n\n" + flashcards_doc})
    b.append({"type": "text", "text":
              "STRUCTURAL REFERENCE LESSON (match its patterns, not its content):\n"
              "<reference_lesson>\n" + (ref.get("content_html") or "")
              + "\n</reference_lesson>\n\nReference lesson practice question example "
              "(StudyVault rubric format):\n"
              + json.dumps((ref.get("practice_questions") or [])[:2], ensure_ascii=False)
              + "\n\nReference knowledge_checks (canonical shapes):\n"
              + json.dumps(ref.get("knowledge_checks") or [], ensure_ascii=False)})
    b.append({"type": "text", "text":
              "FULL EXAM SPECIFICATION (authoritative content source — every fact "
              "comes from here; locate each lesson's sections via its section "
              "markers):\n<spec>\n" + spec_md + "\n</spec>"})
    b.append({"type": "text", "text":
              "SUBJECT: %s (%s)\nTARGET AUDIENCE: free-tier\n\n"
              "TEACHING BRIEF (from planning phase):\n<teaching_brief>\n%s\n</teaching_brief>\n\n"
              "QUESTION TYPES FOR THIS EXAM BOARD:\n%s\n\n"
              "REGISTERED QUESTION TYPE NAMES (your \"type\" field must match one exactly):\n%s"
              % (cfg["subject_name"], cfg["exam_board"],
                 json.dumps(plan.get("teaching_brief", {}), ensure_ascii=False),
                 " | ".join(plan.get("question_type_names", [])),
                 json.dumps(plan.get("question_type_names", []), ensure_ascii=False)),
              "cache_control": {"type": "ephemeral", "ttl": "1h"}})
    return b


def fetch_source_lesson(cfg, transfer):
    """Fetch the AQA source lesson content for a high/medium transfer."""
    src = supa(cfg, "GET",
               "/rest/v1/subjects?slug=eq.%s&select=id" % transfer["source_subject_slug"])
    if not src:
        return None
    units = supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&slug=eq.%s&select=id"
                 % (src[0]["id"], transfer["source_unit_slug"]))
    if not units:
        return None
    rows = supa(cfg, "GET",
                "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s"
                "&select=title,content_html,exam_tip_html,conclusion_html,glossary_terms,"
                "flashcard_questions,knowledge_checks"
                % (units[0]["id"], transfer["source_lesson_number"]))
    return rows[0] if rows else None


def lesson_key(unit_slug, number):
    return "%s-L%02d" % (unit_slug, number)


def stage_prep(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    system = shared_system_blocks(cfg, plan)
    requests = []
    for u in plan["article_units"]:
        for l in u["lessons"]:
            tr = l.get("content_transfer") or {"transfer_score": "fresh"}
            user = (
                "UNIT: %s — %s\nUNIT ACCENT COLOUR: %s\n"
                "LESSON %d of %d: %s\n"
                "PLANNED DESCRIPTION (refine to 60-100 chars if needed): %s\n"
                "SPEC REFERENCES: %s\nSECTION MARKERS (find these in the <spec> above; "
                "they scope THIS lesson's content): %s\n"
            ) % (u["name"], u.get("subtitle", ""), u["accent"],
                 l["number"], len(u["lessons"]), l["title"],
                 l.get("description", ""),
                 json.dumps(l.get("spec_references", []), ensure_ascii=False),
                 json.dumps(l.get("section_markers", []), ensure_ascii=False))
            if tr.get("transfer_score") in ("high", "medium"):
                src = fetch_source_lesson(cfg, tr)
                if src:
                    user += (
                        "\nCONTENT TRANSFER INSTRUCTIONS (from planning agent):\n"
                        "<content_transfer>\n%s\n</content_transfer>\n\n"
                        "<existing_board_content>\n%s\n</existing_board_content>\n"
                    ) % (json.dumps(tr, ensure_ascii=False),
                         json.dumps(src, ensure_ascii=False))
                else:
                    user += "\n(content_transfer source lesson not found — generate fresh from spec)\n"
            elif tr.get("transfer_score") == "low":
                user += ("\nCONTENT TRANSFER: low — treat any prior-board knowledge as tone "
                         "reference only; generate fresh from the spec sections above.\n")
            user += "\nGenerate the complete lesson as a JSON object."
            requests.append({
                "custom_id": lesson_key(u["slug"], l["number"]),
                "params": {
                    "model": MODEL_CONTENT,
                    # Sonnet 5 runs adaptive thinking by default; it bills
                    # against max_tokens (~10-14k/lesson observed) on top of
                    # the ~4-8k lesson JSON. 16000 truncated 23/31 lessons.
                    "max_tokens": 32000,
                    "system": system,
                    "messages": [{"role": "user", "content": user}],
                },
            })
    write_json(os.path.join(cfg["run_dir"], "requests_content.json"), requests)
    total_user = sum(len(r["params"]["messages"][0]["content"]) for r in requests)
    total_sys = sum(len(blk["text"]) for blk in system)
    print("prepped %d content requests. shared system %dk chars, user msgs total %dk chars"
          % (len(requests), total_sys // 1000, total_user // 1000))


# ---------------------------------------------------------------- stage: submit

def try_structured(params):
    """Attach structured outputs if the SDK supports it; else prompt-only JSON."""
    p = dict(params)
    p["output_config"] = {"format": {"type": "json_schema", "schema": LESSON_SCHEMA}}
    return p


def stage_submit(cfg):
    requests = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"), encoding="utf-8"))
    cl = client()
    st = load_state(cfg)

    # 1h-cache pre-warm: same shared system prefix, tiny output. Batch cache
    # hits are best-effort, but a pre-written 1h prefix is the documented way
    # to make them likely.
    warm = dict(requests[0]["params"])
    warm_p = {"model": warm["model"], "max_tokens": 32, "system": warm["system"],
              "messages": [{"role": "user", "content": "warmup — reply with the single word OK"}]}
    use_structured = True
    try:
        msg = cl.messages.create(**try_structured(warm_p))
    except (TypeError, anthropic.BadRequestError) as e:
        print("structured outputs unavailable on warmup (%s) — falling back to prompt-only JSON" % e)
        use_structured = False
        msg = cl.messages.create(**warm_p)
    rec = log_usage(cfg, "warmup", warm["model"], "warmup", msg.usage)
    print("warmup: cache_write_1h=%s cache_read=%s ($%.3f)"
          % (rec["cache_write_1h"], rec["cache_read"], cost_of(rec)))

    batch_requests = []
    for r in requests:
        p = try_structured(r["params"]) if use_structured else r["params"]
        batch_requests.append({"custom_id": r["custom_id"], "params": p})
    batch = cl.messages.batches.create(requests=batch_requests)
    st["content_batch_id"] = batch.id
    st["use_structured"] = use_structured
    save_state(cfg, st)
    print("content batch submitted:", batch.id, "requests:", len(batch_requests))


# ---------------------------------------------------------------- stage: poll

def collect_batch(cfg, batch_id, stage_name, out_subdir):
    cl = client()
    b = cl.messages.batches.retrieve(batch_id)
    print("batch %s: %s  counts=%s" % (batch_id, b.processing_status,
                                       b.request_counts.model_dump()))
    if b.processing_status != "ended":
        return None
    st = load_state(cfg)
    already_logged = batch_id in st.get("collected_batches", [])
    outd = os.path.join(cfg["run_dir"], out_subdir)
    os.makedirs(outd, exist_ok=True)
    results = {}
    errors = {}
    for result in cl.messages.batches.results(batch_id):
        cid = result.custom_id
        if result.result.type == "succeeded":
            m = result.result.message
            if not already_logged:
                log_usage(cfg, stage_name, m.model, cid, m.usage, batch=True)
            text = "".join(blk.text for blk in m.content if blk.type == "text")
            results[cid] = text
        else:
            errors[cid] = result.result.type
    if not already_logged:
        st.setdefault("collected_batches", []).append(batch_id)
        save_state(cfg, st)
    print("collected: %d ok, %d errored (%s)%s" % (
        len(results), len(errors), errors or "",
        " [usage already ledgered]" if already_logged else ""))
    return results, errors


def validate_lessons(cfg, texts):
    """Parse + validate each lesson JSON. Returns (ok_keys, failures dict)."""
    vpath = cfg["validator"]
    spec = importlib.util.spec_from_file_location("val", vpath)
    val = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(val)
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    ok, failures = [], {}
    for cid, text in sorted(texts.items()):
        try:
            obj = parse_json_reply(text)
        except Exception as e:
            failures[cid] = ["JSON parse error: %s" % e]
            continue
        path = os.path.join(lessons_dir, cid + ".json")
        write_json(path, obj)
        problems = []
        try:
            res = val.validate_file(path)
            if res:
                problems += res if isinstance(res, list) else [str(res)]
        except SystemExit:
            problems.append("validator hard-exit")
        except Exception as e:
            problems.append("validator error: %s" % e)
        blob = json.dumps(obj, ensure_ascii=False)
        problems += drift_grep(blob)
        kcs = obj.get("knowledge_checks", [])
        kinds = sorted((k.get("type") or "?") for k in kcs)
        if kinds != ["fill", "fill", "match", "mcq", "mcq"]:
            problems.append("knowledge_checks mix %s != 2 mcq + 2 fill + 1 match" % kinds)
        if problems:
            failures[cid] = problems
        else:
            ok.append(cid)
    return ok, failures


def stage_poll(cfg):
    st = load_state(cfg)
    out = collect_batch(cfg, st["content_batch_id"], "content", "raw_content")
    if out is None:
        return
    st = load_state(cfg)  # reload: collect_batch wrote collected_batches; don't clobber it
    texts, errors = out
    for cid, text in texts.items():
        io.open(os.path.join(cfg["run_dir"], "raw_content", cid + ".txt"), "w",
                encoding="utf-8").write(text)
    ok, failures = validate_lessons(cfg, texts)
    st["content_ok"] = sorted(ok)
    st["content_failures"] = failures
    st["content_errors"] = errors
    save_state(cfg, st)
    print("validated: %d PASS, %d FAIL" % (len(ok), len(failures)))
    for cid, probs in sorted(failures.items()):
        print("  FAIL", cid)
        for p in probs[:6]:
            print("     -", p)


# ---------------------------------------------------------------- stage: fix

def stage_fix(cfg):
    st = load_state(cfg)
    failures = st.get("content_failures", {})
    errored = list(st.get("content_errors", {}))
    if not failures and not errored:
        print("nothing to fix")
        return
    requests = json.load(io.open(os.path.join(cfg["run_dir"], "requests_content.json"), encoding="utf-8"))
    by_id = {r["custom_id"]: r for r in requests}
    cl = client()
    fix_reqs = []
    for cid in sorted(set(list(failures) + errored)):
        base = by_id[cid]
        user = base["params"]["messages"][0]["content"]
        parse_only = cid in failures and all(
            p.startswith("JSON parse error") for p in failures[cid])
        if parse_only:
            pass  # truncated attempt — clean re-run with the raised cap
        elif cid in failures:
            raw_path = os.path.join(cfg["run_dir"], "raw_content", cid + ".txt")
            prev = read(raw_path) if os.path.exists(raw_path) else ""
            user += ("\n\nYOUR PREVIOUS ATTEMPT FAILED VALIDATION. Violations:\n- "
                     + "\n- ".join(failures[cid][:12])
                     + "\n\nPrevious attempt JSON (fix the violations, keep everything "
                       "that was already compliant):\n" + prev[:60000]
                     + "\n\nReturn the corrected complete lesson JSON.")
        p = dict(base["params"])
        p["messages"] = [{"role": "user", "content": user}]
        if st.get("use_structured", True):
            p = try_structured(p)
        fix_reqs.append({"custom_id": cid, "params": p})
    batch = cl.messages.batches.create(requests=fix_reqs)
    st["fix_batch_id"] = batch.id
    save_state(cfg, st)
    print("fix batch submitted:", batch.id, "for", [r["custom_id"] for r in fix_reqs])


def stage_pollfix(cfg):
    st = load_state(cfg)
    out = collect_batch(cfg, st["fix_batch_id"], "content-fix", "raw_content")
    if out is None:
        return
    st = load_state(cfg)  # reload: collect_batch wrote collected_batches; don't clobber it
    texts, errors = out
    for cid, text in texts.items():
        io.open(os.path.join(cfg["run_dir"], "raw_content", cid + ".txt"), "w",
                encoding="utf-8").write(text)
    ok, failures = validate_lessons(cfg, texts)
    st["content_ok"] = sorted(set(st.get("content_ok", []) + ok))
    remaining = {k: v for k, v in st.get("content_failures", {}).items() if k not in ok}
    remaining.update(failures)
    st["content_failures"] = remaining
    st["content_errors"] = errors
    save_state(cfg, st)
    print("after fix: %d total PASS, %d still failing" % (len(st["content_ok"]), len(remaining)))
    for cid, probs in sorted(remaining.items()):
        print("  FAIL", cid, probs[:4])


# ---------------------------------------------------------------- stage: factcheck

FACTCHECK_SYSTEM = """You are fact-checking a GCSE revision lesson before publication. Students sit real exams on this material — factual errors cost marks.

If a SOURCE TEXT document is provided after this prompt (e.g. the full text of set poems), it is the PRIMARY authority: every quotation in the lesson that is attributed to that source MUST appear verbatim in it (allowing only straight/curly quote and whitespace differences). A quotation not found verbatim in the source text is a HIGH finding — supply the nearest real line as the correction. Also verify against the source text: line/stanza counts, form and rhyme claims, speaker and narrative details, and any claim about "the poem says/shows X".

BOARD CONTEXT: the user message states which exam board this lesson targets and lists that board's registered question tariffs. Do NOT flag question mark tariffs, command words, or question formats that match the stated board — different boards use different tariffs, and judging this lesson by another board's format is a false positive.

VERIFY WITH WEB SEARCH every checkable claim:
- Named studies: researcher names, year, procedure, findings, sample details (e.g. a study's condition counts, percentages, age ranges)
- Named theories and their attribution (the theorist actually proposed what the lesson says)
- Direct quotations (must be verbatim from a real source)
- Statistics and figures
- Terminology definitions that could be checked against authoritative psychology sources

DO NOT flag: pedagogical simplification appropriate for GCSE (age 15-16), style, coverage decisions, or paraphrases that preserve meaning.

SEVERITY:
- high: fabricated study/quote, wrong researcher attribution, inverted or wrong finding, procedure described incorrectly in a mark-affecting way
- medium: wrong secondary detail (sample size, year off by more than a year, percentage wrong), misleading simplification
- low: minor imprecision unlikely to cost marks

Return ONLY a JSON object, no code fences:
{
  "findings": [
    {
      "severity": "high" | "medium" | "low",
      "field": "content_html" | "exam_tip_html" | "conclusion_html" | "knowledge_checks" | "flashcard_questions" | "glossary_terms" | "practice_questions",
      "claim": "the exact text from the lesson that is wrong",
      "problem": "what is wrong, with the authoritative source you verified against",
      "correction": "the corrected wording, ready to substitute"
    }
  ]
}
An empty findings array means the lesson verified clean."""


def stage_factcheck(cfg):
    st = load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    cl = client()
    reqs = []
    for cid in st.get("content_ok", []):
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        payload = {k: obj.get(k) for k in
                   ("content_html", "exam_tip_html", "conclusion_html",
                    "knowledge_checks", "flashcard_questions", "glossary_terms",
                    "practice_questions")}
        user = ("LESSON: %s\nTARGET BOARD: %s GCSE %s — question tariffs on this board: %s\n\n"
                "%s\n\nFact-check this lesson. Return the findings JSON."
                % (cid, cfg["exam_board"], cfg["subject_name"],
                   " | ".join(plan.get("question_type_names", [])),
                   json.dumps(payload, ensure_ascii=False)))
        reqs.append({"custom_id": cid, "params": {
            "model": MODEL_FACTCHECK, "max_tokens": 8000,
            "tools": [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}],
            "system": ([{"type": "text", "text": FACTCHECK_SYSTEM},
                        {"type": "text",
                         "text": "SOURCE TEXT (primary authority for quotations):\n\n"
                                 + read(cfg["factcheck_context_doc"]),
                         "cache_control": {"type": "ephemeral", "ttl": "1h"}}]
                       if cfg.get("factcheck_context_doc") else
                       [{"type": "text", "text": FACTCHECK_SYSTEM,
                         "cache_control": {"type": "ephemeral", "ttl": "1h"}}]),
            "messages": [{"role": "user", "content": user}],
        }})
    try:
        batch = cl.messages.batches.create(requests=reqs)
        st["factcheck_batch_id"] = batch.id
        save_state(cfg, st)
        print("factcheck batch submitted:", batch.id, "requests:", len(reqs))
    except anthropic.BadRequestError as e:
        print("batch rejected (%s) — running factcheck sequentially" % e)
        findings = {}
        for r in reqs:
            with cl.messages.stream(**r["params"]) as stream:
                msg = stream.get_final_message()
            log_usage(cfg, "factcheck", MODEL_FACTCHECK, r["custom_id"], msg.usage)
            text = "".join(b.text for b in msg.content if b.type == "text")
            findings[r["custom_id"]] = parse_json_reply(text).get("findings", [])
            print("  %s: %d findings" % (r["custom_id"], len(findings[r["custom_id"]])))
        finish_factcheck(cfg, findings)


def stage_pollfactcheck(cfg):
    st = load_state(cfg)
    out = collect_batch(cfg, st["factcheck_batch_id"], "factcheck", "raw_factcheck")
    if out is None:
        return
    texts, errors = out
    findings = {}
    for cid, text in texts.items():
        try:
            findings[cid] = parse_json_reply(text).get("findings", [])
        except Exception as e:
            findings[cid] = [{"severity": "high", "field": "content_html",
                              "claim": "(parse failure)", "problem": str(e),
                              "correction": ""}]
    if errors:
        print("factcheck errors (rerun these):", errors)
    finish_factcheck(cfg, findings)


def finish_factcheck(cfg, findings):
    st = load_state(cfg)
    all_f = []
    for cid, fl in sorted(findings.items()):
        for f in fl:
            f["lesson"] = cid
            all_f.append(f)
    counts = {"high": 0, "medium": 0, "low": 0}
    for f in all_f:
        counts[f.get("severity", "low")] = counts.get(f.get("severity", "low"), 0) + 1
    report = {"subject": cfg["slug"], "checked": len(findings),
              "counts": counts, "findings": all_f}
    fc_dir = cfg.get("factcheck_out_dir")
    if fc_dir:
        os.makedirs(fc_dir, exist_ok=True)
        write_json(os.path.join(fc_dir, cfg["slug"] + ".json"), report)
        md = ["# Fact-check — %s" % cfg["slug"], "",
              "Checked %d lessons. HIGH=%d MED=%d LOW=%d" %
              (len(findings), counts["high"], counts["medium"], counts["low"]), ""]
        for f in all_f:
            md.append("- **%s** `%s` [%s]: %s → %s" %
                      (f.get("severity"), f.get("lesson"), f.get("field"),
                       (f.get("problem") or "")[:220], (f.get("correction") or "")[:160]))
        io.open(os.path.join(fc_dir, cfg["slug"] + ".md"), "w", encoding="utf-8").write("\n".join(md))
    write_json(os.path.join(cfg["run_dir"], "factcheck.json"), report)
    st["factcheck_counts"] = counts
    save_state(cfg, st)
    print("factcheck complete: HIGH=%d MED=%d LOW=%d across %d lessons"
          % (counts["high"], counts["medium"], counts["low"], len(findings)))


# ---------------------------------------------------------------- stage: applyfixes

def stage_applyfixes(cfg):
    st = load_state(cfg)
    report = json.load(io.open(os.path.join(cfg["run_dir"], "factcheck.json"), encoding="utf-8"))
    by_lesson = {}
    for f in report["findings"]:
        if f.get("severity") in ("high", "medium"):
            by_lesson.setdefault(f["lesson"], []).append(f)
    if not by_lesson:
        print("no HIGH/MEDIUM findings — nothing to apply")
        return
    cl = client()
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    reqs = []
    for cid, fl in sorted(by_lesson.items()):
        obj = json.load(io.open(os.path.join(lessons_dir, cid + ".json"), encoding="utf-8"))
        user = ("Apply ONLY the corrections below to this GCSE %s lesson JSON. "
                "Change nothing else — no rewrites, no restructuring, no new narration IDs "
                "unless a correction forces one. Keep every data-narration-id sequence intact.\n\n"
                "CORRECTIONS:\n%s\n\nLESSON JSON:\n%s\n\n"
                "Return the complete corrected lesson JSON only, no code fences."
                % (cfg["subject_name"], json.dumps(fl, ensure_ascii=False),
                   json.dumps(obj, ensure_ascii=False)))
        p = {"model": MODEL_CONTENT, "max_tokens": 32000,
             "messages": [{"role": "user", "content": user}]}
        if st.get("use_structured", True):
            p = try_structured(p)
        reqs.append({"custom_id": cid, "params": p})
    batch = cl.messages.batches.create(requests=reqs)
    st["applyfix_batch_id"] = batch.id
    save_state(cfg, st)
    print("applyfixes batch submitted:", batch.id, "lessons:", sorted(by_lesson))


def stage_pollapplyfixes(cfg):
    st = load_state(cfg)
    out = collect_batch(cfg, st["applyfix_batch_id"], "applyfixes", "raw_applyfix")
    if out is None:
        return
    texts, errors = out
    ok, failures = validate_lessons(cfg, texts)
    print("applied fixes validated: %d PASS, %d FAIL %s" % (len(ok), len(failures), failures or ""))
    if errors:
        print("errored:", errors)


# ---------------------------------------------------------------- stage: media

MEDIA_SCHEMA = {
    "type": "object",
    "properties": {
        "related_media": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string",
                                 "enum": ["Podcasts", "Videos & Channels", "Movies",
                                          "TV Shows", "Documentaries", "Study Tools"]},
                    "items": {"type": "array", "items": {
                        "type": "object",
                        "properties": {"title": {"type": "string"},
                                       "url": {"type": "string"},
                                       "description": {"type": "string"}},
                        "required": ["title", "url", "description"],
                        "additionalProperties": False}},
                },
                "required": ["category", "items"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["related_media"],
    "additionalProperties": False,
}


def stage_media(cfg):
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    media_doc = read(os.path.join(cfg["docs_dir"], "RELATED_MEDIA_PIPELINE.md"))
    system = [{"type": "text", "text":
               "You are the related-media curation agent for StudyVault, a GCSE revision "
               "platform. Follow the pipeline doc below for category structure, ordering, "
               "and source guidance. Use web_search (a few searches) to find REAL, "
               "currently-existing content — established podcasts, real YouTube channels/"
               "videos, real films/documentaries on JustWatch UK, BBC Bitesize hub pages. "
               "Do NOT exhaustively fetch and open every candidate — a downstream Python "
               "auditor verifies and prunes every URL (oembed for YouTube, body-check for "
               "JustWatch, hub-paths for Bitesize), so your job is breadth of plausible "
               "real candidates, not per-URL verification. Return slightly MORE than the "
               "minimum per category so the auditor has margin after pruning. Do NOT "
               "include a 'Lesson Podcast' item — the platform injects that separately.\n\n"
               + media_doc,
               "cache_control": {"type": "ephemeral", "ttl": "1h"}}]
    cl = client()
    reqs = []
    st = load_state(cfg)
    # Self-healing: skip lessons that already have usable media on file.
    existing = {}
    mpath = os.path.join(cfg["run_dir"], "related_media.json")
    if os.path.exists(mpath):
        existing = json.load(io.open(mpath, encoding="utf-8"))
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = lesson_key(u["slug"], l["number"])
            if cid in existing:
                continue
            user = ("SUBJECT: GCSE %s\nUNIT: %s\nLESSON: %s\nLESSON COVERS: %s\n\n"
                    "Find and return the related media as a JSON object "
                    "{\"related_media\": [{\"category\": ..., \"items\": [{\"title\", \"url\", "
                    "\"description\"}]}]} with categories in the canonical order. Provide "
                    ">=2 per category where sensible so >=8 items total survive pruning, "
                    "covering: podcasts, videos/channels, at least one of movies/TV/"
                    "documentaries, and study tools. Plain unicode in titles and "
                    "descriptions, no HTML entities. Once you have candidates, STOP "
                    "searching and output ONLY the JSON."
                    % (cfg["subject_name"], u["name"], l["title"], l.get("description", "")))
            reqs.append({"custom_id": cid, "params": {
                "model": MODEL_CONTENT, "max_tokens": 10000,
                "tools": [
                    {"type": "web_search_20260209", "name": "web_search", "max_uses": 5},
                ],
                "system": system,
                "messages": [{"role": "user", "content": user}],
            }})
    batch = cl.messages.batches.create(requests=reqs)
    st["media_batch_id"] = batch.id
    save_state(cfg, st)
    print("media batch submitted:", batch.id, "requests:", len(reqs))


def stage_pollmedia(cfg):
    st = load_state(cfg)
    out = collect_batch(cfg, st["media_batch_id"], "media", "raw_media")
    if out is None:
        return
    st = load_state(cfg)  # reload: collect_batch wrote collected_batches; don't clobber it
    texts, errors = out
    mpath = os.path.join(cfg["run_dir"], "related_media.json")
    media = json.load(io.open(mpath, encoding="utf-8")) if os.path.exists(mpath) else {}
    problems = {}
    for cid, text in sorted(texts.items()):
        try:
            obj = parse_json_reply(text)
            rm = obj["related_media"]
            n = sum(len(c["items"]) for c in rm)
            cats = {c["category"] for c in rm}
            probs = []
            if n < 6:
                probs.append("only %d items" % n)
            if "Podcasts" not in cats:
                probs.append("no Podcasts")
            if "Videos & Channels" not in cats:
                probs.append("no Videos")
            if "Study Tools" not in cats:
                probs.append("no Study Tools")
            if not cats & {"Movies", "TV Shows", "Documentaries"}:
                probs.append("no Movies/TV/Docs")
            media[cid] = rm
            if probs:
                problems[cid] = probs
        except Exception as e:
            problems[cid] = ["parse: %s" % e]
    write_json(os.path.join(cfg["run_dir"], "related_media.json"), media)
    st["media_problems"] = problems
    save_state(cfg, st)
    print("media collected for %d lessons; coverage problems: %s"
          % (len(media), problems or "none"))
    if errors:
        print("errored:", errors)


def stage_insertmedia(cfg):
    """PATCH related_media onto lesson shells (with Lesson Podcast placeholder)."""
    st = load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    media = json.load(io.open(os.path.join(cfg["run_dir"], "related_media.json"), encoding="utf-8"))
    units = supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug" % st["subject_id"])
    uid = {u["slug"]: u["id"] for u in units}
    n = 0
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = lesson_key(u["slug"], l["number"])
            if cid not in media:
                continue
            rm = media[cid]
            pod = next((c for c in rm if c["category"] == "Podcasts"), None)
            placeholder = {"url": None, "title": "Lesson Podcast",
                           "description": "Audio overview of this lesson."}
            if pod:
                pod["items"].insert(0, placeholder)
            else:
                rm.insert(0, {"category": "Podcasts", "items": [placeholder]})
            supa(cfg, "PATCH", "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s"
                 % (uid[u["slug"]], l["number"]), {"related_media": rm})
            n += 1
    print("related_media patched onto %d lessons" % n)


# ---------------------------------------------------------------- stage: guides

def stage_guides(cfg):
    """Copy source-board guide pages, rewrite links, batch-adapt examples that
    reference topics absent from this board's spec."""
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    src = supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id" % cfg["source_subject_slug"])
    guides = supa(cfg, "GET",
                  "/rest/v1/guide_pages?subject_id=eq.%s&select=slug,guide_type,title,sort_order,content_html&order=sort_order"
                  % src[0]["id"])
    topics = [u["name"] for u in plan["article_units"]]
    lesson_titles = [l["title"] for u in plan["article_units"] for l in u["lessons"]]
    cl = client()
    reqs = []
    passthrough = {}
    for g in guides:
        html = g["content_html"].replace("/guide/%s/" % cfg["source_subject_slug"],
                                         "/guide/%s/" % cfg["slug"])
        if g["slug"] == "index":
            passthrough[g["slug"]] = dict(g, content_html=html)
            continue
        user = (
            "This is a revision-technique guide page for GCSE %s. It was written for a "
            "different exam board's version of the subject. This board's topic list is:\n%s\n"
            "Lesson titles available on this board:\n%s\n\n"
            "TASK: The pedagogy text is canonical — do not touch it. ONLY adjust the "
            "subject worked examples: if an example references a topic NOT on this "
            "board's topic list above (e.g. visual illusions/perception, topics from "
            "another board), replace that example with an equivalent using one of this "
            "board's topics, matching the original example's depth and format. If every "
            "example already fits this board's topics, return the HTML unchanged. Keep "
            "ALL HTML structure, classes, and entity usage identical. Return ONLY the "
            "full HTML, no code fences, no commentary.\n\nGUIDE HTML:\n%s"
        ) % (cfg["subject_name"], json.dumps(topics), json.dumps(lesson_titles), html)
        reqs.append({"custom_id": "guide-" + g["slug"], "params": {
            "model": MODEL_CONTENT, "max_tokens": 16000,
            "messages": [{"role": "user", "content": user}],
        }})
        passthrough[g["slug"]] = dict(g, content_html=html)
    write_json(os.path.join(cfg["run_dir"], "guides_base.json"), passthrough)
    batch = cl.messages.batches.create(requests=reqs)
    st = load_state(cfg)
    st["guides_batch_id"] = batch.id
    save_state(cfg, st)
    print("guides batch submitted:", batch.id, "(%d technique pages + index passthrough)" % len(reqs))


def stage_pollguides(cfg):
    st = load_state(cfg)
    out = collect_batch(cfg, st["guides_batch_id"], "guides", "raw_guides")
    if out is None:
        return
    texts, errors = out
    base = json.load(io.open(os.path.join(cfg["run_dir"], "guides_base.json"), encoding="utf-8"))
    rows = []
    for slug, g in base.items():
        html = g["content_html"]
        key = "guide-" + slug
        if key in texts:
            t = texts[key].strip()
            if t.startswith("```"):
                t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
                t = re.sub(r"\s*```$", "", t)
            if "<main" in t:
                html = t
        rows.append({"subject_id": st["subject_id"], "slug": slug,
                     "guide_type": g["guide_type"], "title": g["title"],
                     "sort_order": g["sort_order"], "content_html": html})
    existing = supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=slug" % st["subject_id"])
    if existing:
        print("ABORT: %d guide rows already exist for this subject" % len(existing))
        return
    supa(cfg, "POST", "/rest/v1/guide_pages", rows)
    print("inserted %d guide pages (%s)" % (len(rows), ", ".join(r["slug"] for r in rows)))
    if errors:
        print("errored:", errors)


# ---------------------------------------------------------------- stage: insert

def stage_insert(cfg):
    st = load_state(cfg)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    subject_id = st["subject_id"]
    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    units = supa(cfg, "GET", "/rest/v1/units?subject_id=eq.%s&select=id,slug" % subject_id)
    uid = {u["slug"]: u["id"] for u in units}
    hero_kw = {}
    n = 0
    for u in plan["article_units"]:
        for l in u["lessons"]:
            cid = lesson_key(u["slug"], l["number"])
            path = os.path.join(lessons_dir, cid + ".json")
            if not os.path.exists(path):
                print("SKIP (no validated JSON):", cid)
                continue
            obj = json.load(io.open(path, encoding="utf-8"))
            patch = {k: obj[k] for k in
                     ("description", "content_html", "exam_tip_html", "conclusion_html",
                      "practice_questions", "knowledge_checks", "flashcard_questions",
                      "glossary_terms", "hero_image_caption")}
            patch["status"] = "pending_review"
            supa(cfg, "PATCH",
                 "/rest/v1/lessons?unit_id=eq.%s&lesson_number=eq.%s" % (uid[u["slug"]], l["number"]),
                 patch)
            hero_kw[cid] = obj.get("hero_keywords", [])
            n += 1
    write_json(os.path.join(cfg["run_dir"], "hero_keywords.json"), hero_kw)
    check = supa(cfg, "GET",
                 "/rest/v1/lessons?select=id,title,unit_id&content_html=not.is.null"
                 "&unit_id=in.(%s)" % ",".join(uid.values()))
    print("inserted %d lessons; %d rows now have content_html" % (n, len(check)))


# ---------------------------------------------------------------- stage: costs

def stage_costs(cfg):
    path = os.path.join(cfg["run_dir"], "costs.jsonl")
    if not os.path.exists(path):
        print("no ledger yet")
        return
    recs = [json.loads(line) for line in io.open(path, encoding="utf-8") if line.strip()]
    by_stage = {}
    for r in recs:
        s = by_stage.setdefault(r["stage"], {"n": 0, "in": 0, "out": 0, "cr": 0, "cw": 0,
                                             "ws": 0, "cost": 0.0})
        s["n"] += 1
        s["in"] += r["input_tokens"]
        s["out"] += r["output_tokens"]
        s["cr"] += r["cache_read"]
        s["cw"] += (r["cache_write_5m"] or 0) + (r["cache_write_1h"] or 0)
        s["ws"] += r.get("web_searches", 0)
        s["cost"] += cost_of(r)
    total = 0.0
    print("%-14s %5s %12s %12s %12s %12s %6s %10s" %
          ("stage", "calls", "input", "output", "cache_read", "cache_write", "search", "cost"))
    for stage, s in by_stage.items():
        total += s["cost"]
        print("%-14s %5d %12d %12d %12d %12d %6d %9.3f$" %
              (stage, s["n"], s["in"], s["out"], s["cr"], s["cw"], s["ws"], s["cost"]))
    print("%-14s %72.3f$" % ("TOTAL", total))


# ---------------------------------------------------------------- main

STAGES = {
    "plan": stage_plan, "plancheck": stage_plancheck, "activate": stage_activate,
    "prep": stage_prep, "submit": stage_submit, "poll": stage_poll,
    "fix": stage_fix, "pollfix": stage_pollfix,
    "factcheck": stage_factcheck, "pollfactcheck": stage_pollfactcheck,
    "applyfixes": stage_applyfixes, "pollapplyfixes": stage_pollapplyfixes,
    "media": stage_media, "pollmedia": stage_pollmedia, "insertmedia": stage_insertmedia,
    "guides": stage_guides, "pollguides": stage_pollguides,
    "insert": stage_insert, "costs": stage_costs,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("stage", choices=sorted(STAGES))
    args = ap.parse_args()
    cfg = load_config(args.config)
    STAGES[args.stage](cfg)


if __name__ == "__main__":
    main()
