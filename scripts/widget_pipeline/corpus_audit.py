# -*- coding: utf-8 -*-
"""Which lessons across the whole free tier want an interactive, and how
few widgets would cover them?

Two phases, run unattended:

  A. TRIAGE (Haiku, ~$0.0014/lesson) — every live free-tier article
     lesson against the one test that matters: could a student read this
     passage correctly and still picture the idea wrongly? Validated on
     two units first (13/25, keeping physics, rejecting narrative).

  B. CLUSTER (Sonnet) — the same misconception recurs across boards:
     "current gets used up in series" is one idea in seven science
     subjects. A list of lessons therefore wildly overstates the work.
     This groups the qualifying lessons into canonical misconceptions and
     ranks them by how many lessons ONE widget would serve.

Resumable: state is saved continuously, so a crash or a kill loses at
most the calls in flight. Errors are recorded per lesson and reported in
the summary — never swallowed to make the log look clean.

    python scripts/widget_pipeline/corpus_audit.py            # A then B
    python scripts/widget_pipeline/corpus_audit.py --phase a
    python scripts/widget_pipeline/corpus_audit.py --phase b
    python scripts/widget_pipeline/corpus_audit.py --report
"""
import io
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import canary                      # reuse TRIAGE_SYS, models, pricing, jparse
from lib.supabase_client import get_client

STATE = os.path.join(HERE, "_corpus_audit.json")
OUT_MD = os.path.join(HERE, "_corpus_audit.md")
MIN_CONTENT = 800
WORKERS = 8
# Budget is a DELTA for THIS run, not cumulative — the ledger already
# carries the day's earlier spend, so a cumulative cap would halt at once.
RUN_BUDGET_USD = 9.0
SAVE_EVERY = 25

_lock = threading.Lock()

# The ledger is a shared FILE that canary.call() rewrites on every call.
# Eight threads racing it corrupted it overnight; a per-process lock fixed
# that, and then two processes racing it corrupted it again. So this run
# does not touch the file at all: an in-memory token accumulator replaces
# ledger_add, and the totals are folded in once at the end. No contention,
# no partial writes, and the cost figures are still real token counts.
_tok = {"calls": 0, "in": 0, "out": 0, "model": {}}


def _accumulate(tier, model, label, usage):
    with _lock:
        _tok["calls"] += 1
        _tok["in"] += usage.input_tokens
        _tok["out"] += usage.output_tokens
        m = _tok["model"].setdefault(model, {"in": 0, "out": 0, "n": 0})
        m["in"] += usage.input_tokens
        m["out"] += usage.output_tokens
        m["n"] += 1


canary.ledger_add = _accumulate


def spent_this_run():
    total = 0.0
    for model, m in _tok["model"].items():
        pin, pout = canary.PRICES.get(model, (0, 0))
        total += (m["in"] / 1e6 * pin + m["out"] / 1e6 * pout) * canary.CALIBRATION
    return total


def flush_ledger():
    """Fold this run's usage into the shared ledger, once, at the end."""
    led = canary.ledger_load()
    for model, m in _tok["model"].items():
        led["calls"].append({"tier": "corpus", "model": model,
                             "label": "corpus-audit-total",
                             "in": m["in"], "out": m["out"]})
    io.open(canary.LEDGER, "w", encoding="utf-8").write(json.dumps(led, indent=1))


def load():
    if os.path.exists(STATE):
        return json.load(io.open(STATE, encoding="utf-8"))
    return {"lessons": [], "phase_a_done": False, "clusters": None}


def save(s):
    tmp = STATE + ".tmp"
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(s))
    os.replace(tmp, STATE)


def strip(html):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html or "")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------------ phase A
def fetch_lessons():
    """Live FREE-TIER article lessons only. School copies (Unity, Severn
    Vale) duplicate generic content, so including them would double-count
    the same misconception."""
    sb = get_client()
    subs = {r["id"]: r for r in sb.from_("subjects")
            .select("id,slug,name,exam_board,school_id,status")
            .is_("school_id", "null").execute().data}
    units = {r["id"]: r for r in sb.from_("units")
             .select("id,slug,name,subject_id").execute().data}
    out, off = [], 0
    while True:
        page = sb.from_("lessons").select(
            "id,unit_id,lesson_number,title,status,content_html") \
            .eq("status", "live").order("id").range(off, off + 499).execute().data
        if not page:
            break
        for l in page:
            html = l.get("content_html") or ""
            if len(html) < MIN_CONTENT:
                continue                      # practice-format / stubs
            u = units.get(l["unit_id"])
            if not u:
                continue
            s = subs.get(u["subject_id"])
            if not s:
                continue                      # school-specific: skipped
            out.append({
                "lesson_id": l["id"], "subject": s["slug"], "subject_name": s["name"],
                "board": s.get("exam_board"), "unit": u["slug"], "unit_name": u["name"],
                "n": l["lesson_number"], "title": l["title"],
                "text": strip(html)[:9000],
            })
        off += 500
        print("  fetched %d..." % len(out), flush=True)
    return out


def triage_one(les):
    user = ("SUBJECT: %s\nUNIT: %s\nLESSON %s: %s\n\n%s"
            % (les["subject_name"], les["unit_name"], les["n"], les["title"], les["text"]))
    try:
        v = canary.jparse(canary.call(1, canary.HAIKU, les["title"][:32],
                                      canary.TRIAGE_SYS, user, 700))
        les["triage"] = v
        les.pop("error", None)
    except Exception as e:
        les["error"] = str(e)[:180]


def phase_a():
    s = load()
    if not s["lessons"]:
        print("fetching live free-tier article lessons...", flush=True)
        s["lessons"] = fetch_lessons()
        save(s)
    todo = [l for l in s["lessons"] if "triage" not in l]
    print("phase A: %d lessons total, %d to triage" % (len(s["lessons"]), len(todo)), flush=True)
    done = [0]
    start = time.time()

    def work(les):
        if spent_this_run() > RUN_BUDGET_USD:
            return
        triage_one(les)
        with _lock:
            done[0] += 1
            if done[0] % SAVE_EVERY == 0:
                save(s)
                rate = done[0] / max(1e-9, time.time() - start)
                print("  %d/%d  (%.1f/s, ~$%.2f, %d min left)"
                      % (done[0], len(todo), rate, spent_this_run(),
                         int((len(todo) - done[0]) / max(rate, 1e-9) / 60)), flush=True)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(work, todo))
    save(s)
    errs = [l for l in s["lessons"] if l.get("error")]
    yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
    print("\nphase A done: %d qualify of %d triaged (%d errors, $%.2f)"
          % (len(yes), len([l for l in s["lessons"] if l.get("triage")]),
             len(errs), spent_this_run()), flush=True)
    for e in errs[:8]:
        print("   ERROR %s: %s" % (e["title"][:40], e["error"][:90]), flush=True)
    s["phase_a_done"] = True
    save(s)


# ------------------------------------------------------------------ phase B
CLUSTER_SYS = """You group GCSE misconceptions that are THE SAME IDEA into one cluster, so that one interactive widget can serve every lesson in the cluster.

You are given numbered items, each with a subject, a lesson title, and the misconception a triage model identified.

Two items belong together when a SINGLE widget, with the same numbers and the same interaction, would teach both. "Current is used up in a series circuit" from AQA, Edexcel and OCR is ONE cluster — the exam board is irrelevant to the physics. "Wasted energy disappears" is a DIFFERENT cluster from "current is used up", even though both are energy-ish.

Be willing to leave an item in a cluster of one. Do not force merges across genuinely different ideas.

For each cluster give a stable kebab-case id, a short name a teacher would recognise, and the ONE sentence a widget would have to make concrete.

Reply with ONLY JSON:
{"clusters": [{"id": "current-not-used-up",
               "name": "Current is not used up in a series circuit",
               "teaches": "<the one idea the widget must make concrete>",
               "items": [<the numbers of the items in this cluster>]}]}"""

MERGE_SYS = """You are merging cluster labels produced by separate batches, so the same idea does not appear twice under different names.

You are given clusters with ids, names and the idea each teaches. Return the canonical set: where two or more clusters are the same idea, merge them into one and list every id that folds into it.

Reply with ONLY JSON:
{"canonical": [{"id": "<kept id>", "name": "<name>", "teaches": "<...>",
                "absorbs": ["<other id>", ...]}]}"""


def phase_b():
    s = load()
    yes = [l for l in s["lessons"] if l.get("triage", {}).get("worth_it")]
    if not yes:
        print("nothing qualified; run phase A first")
        return
    print("phase B: clustering %d qualifying lessons" % len(yes), flush=True)
    BATCH = 45
    raw = []
    for start in range(0, len(yes), BATCH):
        chunk = yes[start:start + BATCH]
        if spent_this_run() > RUN_BUDGET_USD:
            print("  budget cap hit, stopping clustering", flush=True)
            break
        items = "\n".join(
            "%d. [%s] %s — %s" % (start + i, l["subject"], l["title"][:70],
                                  (l["triage"].get("misconception") or "")[:190])
            for i, l in enumerate(chunk))
        try:
            r = canary.jparse(canary.call(5, canary.SONNET, "cluster:%d" % start,
                                          CLUSTER_SYS, items, 8000))
            raw.extend(r.get("clusters", []))
            print("  batch %d-%d -> %d clusters ($%.2f)"
                  % (start, start + len(chunk), len(r.get("clusters", [])),
                     spent_this_run()), flush=True)
        except Exception as e:
            print("  batch %d FAILED: %s" % (start, str(e)[:120]), flush=True)
        s["clusters_raw"] = raw
        save(s)

    # merge equivalent clusters across batches
    canon = raw
    try:
        blob = json.dumps([{"id": c["id"], "name": c.get("name"),
                            "teaches": c.get("teaches")} for c in raw], indent=0)
        m = canary.jparse(canary.call(5, canary.SONNET, "merge", MERGE_SYS, blob, 12000))
        absorb = {}
        for c in m.get("canonical", []):
            for a in c.get("absorbs", []):
                absorb[a] = c["id"]
        merged = {}
        for c in raw:
            cid = absorb.get(c["id"], c["id"])
            tgt = merged.setdefault(cid, {"id": cid, "name": c.get("name"),
                                          "teaches": c.get("teaches"), "items": []})
            tgt["items"].extend(c.get("items", []))
        for c in m.get("canonical", []):
            if c["id"] in merged:
                merged[c["id"]]["name"] = c.get("name") or merged[c["id"]]["name"]
                merged[c["id"]]["teaches"] = c.get("teaches") or merged[c["id"]]["teaches"]
        canon = list(merged.values())
        print("  merged %d raw clusters -> %d canonical" % (len(raw), len(canon)), flush=True)
    except Exception as e:
        print("  merge FAILED (%s) — using unmerged clusters" % str(e)[:110], flush=True)

    for c in canon:
        c["lessons"] = []
        for idx in c.get("items", []):
            if isinstance(idx, int) and 0 <= idx < len(yes):
                l = yes[idx]
                c["lessons"].append({"subject": l["subject"], "board": l.get("board"),
                                     "unit": l["unit"], "n": l["n"], "title": l["title"],
                                     "url": "/lesson/%s/%s/%s" % (l["subject"], l["unit"], l["n"])})
        c["count"] = len(c["lessons"])
    canon.sort(key=lambda c: -c["count"])
    s["clusters"] = canon
    save(s)
    print("phase B done: %d canonical misconceptions ($%.2f)"
          % (len(canon), spent_this_run()), flush=True)


# ------------------------------------------------------------------ report
def report():
    s = load()
    lessons = s["lessons"]
    triaged = [l for l in lessons if l.get("triage")]
    yes = [l for l in triaged if l["triage"].get("worth_it")]
    errs = [l for l in lessons if l.get("error")]
    clusters = s.get("clusters") or []
    covered = sum(c["count"] for c in clusters)

    md = ["# Which lessons want an interactive — whole free tier", "",
          "Every live free-tier article lesson put through the misconception test:",
          "*could a student read this passage correctly and still picture the idea wrongly?*",
          "School copies are excluded — they duplicate generic content.", "",
          "| | |", "|---|---|",
          "| Lessons triaged | %d |" % len(triaged),
          "| Qualify for an interactive | **%d** (%.0f%%) |"
          % (len(yes), 100.0 * len(yes) / max(1, len(triaged))),
          "| Distinct misconceptions behind them | **%d** |" % len(clusters),
          "| Lessons covered by those clusters | %d |" % covered,
          "| Triage errors | %d |" % len(errs), ""]
    if clusters:
        md += ["## Build these first — ranked by how many lessons one widget serves", "",
               "| # | Misconception | Lessons | Subjects |", "|---|---|---|---|"]
        for i, c in enumerate(clusters[:40], 1):
            subs = sorted(set(l["subject"] for l in c["lessons"]))
            md.append("| %d | **%s** | %d | %s |"
                      % (i, c.get("name") or c["id"], c["count"],
                         ", ".join(subs[:5]) + ("…" if len(subs) > 5 else "")))
        md.append("")
        md.append("## What each one has to make concrete")
        md.append("")
        for c in clusters[:25]:
            md.append("**%s** — %d lessons" % (c.get("name") or c["id"], c["count"]))
            md.append("")
            md.append("> %s" % (c.get("teaches") or ""))
            md.append("")
            for l in c["lessons"][:4]:
                md.append("- `%s` %s — %s" % (l["url"], l["title"][:60], l["subject"]))
            if c["count"] > 4:
                md.append("- …and %d more" % (c["count"] - 4))
            md.append("")
    if errs:
        md += ["## Errors", ""] + ["- %s: %s" % (e["title"][:50], e["error"][:110])
                                   for e in errs[:25]] + [""]
    io.open(OUT_MD, "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md[:20]))
    print("\nwrote", OUT_MD)
    canary.cost_report()


if __name__ == "__main__":
    a = sys.argv
    ph = a[a.index("--phase") + 1] if "--phase" in a else "all"
    if "--report" in a:
        report()
    else:
        if ph in ("a", "all"):
            phase_a()
        if ph in ("b", "all"):
            phase_b()
        flush_ledger()
        report()
