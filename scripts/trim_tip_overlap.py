# -*- coding: utf-8 -*-
"""Trim the 66 exam tips flagged as near-restatements (Tom, 16 Aug: "go
ahead with the trim pass").

DELETION-ONLY by construction: each tip is split into sentences; the model
picks which sentences to KEEP (those adding value beyond the body — a
concrete example, a mark-scheme point, a warning); the tip is rebuilt from
surviving sentences verbatim. No new text can enter, so there is nothing new
to fact-check and narration (body-only) is untouched. A tip whose every
sentence restates is emptied — the loader hides an empty tip box.

Reads the flag list from scripts/_tip_overlap_report.md.
Run: python scripts/trim_tip_overlap.py [--apply]
Backup: scripts/_tip_trim_backup.json  |  Report: scripts/_tip_trim_report.md
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_tip_trim_backup.json")
MODEL = "claude-sonnet-5"
TAGS = re.compile(r"<[^>]+>")

SYSTEM = """You trim GCSE revision exam tips that largely restate the lesson
text above them. You are given the lesson's final section (for reference)
and the tip as NUMBERED SENTENCES.

Choose which sentence numbers to KEEP. Keep a sentence only if it adds
something the body does not already say: a concrete worked phrasing, a mark
scheme point, a common-mistake warning, an instruction. Drop sentences that
merely restate the body's teaching. Keeping nothing is allowed when the
whole tip restates. Prefer a short, sharp tip.

Return ONLY JSON: {"keep": [1, 3]}"""


def sentences(html):
    """[(para_index, sentence_text)] — split inside each <p>, keep order."""
    out = []
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html or "", re.S) or [html or ""]
    for pi, p in enumerate(paras):
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z&<‘“'\"])", p.strip()):
            if TAGS.sub("", s).strip():
                out.append((pi, s.strip()))
    return out


def last_section(content_html):
    parts = re.split(r"<h[23][^>]*>", content_html or "")
    return parts[-1] if len(parts) > 1 else (content_html or "")


def main():
    sb = get_client()
    flags = re.findall(r"- (\d+)%\s+([\w-]+)/([\w-]+)/L(\d+)",
                       io.open(os.path.join(HERE, "_tip_overlap_report.md"),
                               encoding="utf-8").read())
    print("flagged lessons: %d" % len(flags))
    subs = {s["slug"]: s["id"] for s in sb.table("subjects").select("id,slug").execute().data}
    cl = anthropic.Anthropic()

    backup, writes, report = {}, [], []
    for pct, subj, unit, num in flags:
        urow = [u for u in sb.table("units").select("id,slug,subject_id").eq("slug", unit)
                .execute().data if u["subject_id"] == subs.get(subj)]
        if not urow:
            print("SKIP %s/%s — unit not found" % (subj, unit))
            continue
        l = sb.table("lessons").select("id,exam_tip_html,content_html") \
            .eq("unit_id", urow[0]["id"]).eq("lesson_number", int(num)).execute().data[0]
        sents = sentences(l["exam_tip_html"])
        if not sents:
            continue
        body = TAGS.sub(" ", last_section(l["content_html"]))[:2200]
        numbered = "\n".join("%d. %s" % (i + 1, TAGS.sub(" ", s)) for i, (_, s) in enumerate(sents))
        r = cl.messages.create(model=MODEL, max_tokens=400, system=SYSTEM,
                               messages=[{"role": "user", "content":
                                          "LESSON FINAL SECTION:\n%s\n\nTIP SENTENCES:\n%s"
                                          % (body, numbered)}])
        text = "".join(getattr(b, "text", "") or "" for b in r.content)
        m = re.search(r"\{[\s\S]*\}", text)
        try:
            keep = set(json.loads(m.group(0)).get("keep", []))
        except Exception:
            print("SKIP %s/%s/L%s — bad verdict" % (subj, unit, num))
            continue
        keep = {k for k in keep if 1 <= k <= len(sents)}
        if len(keep) == len(sents):
            report.append("- kept whole tip (%s%%): %s/%s/L%s" % (pct, subj, unit, num))
            continue
        # rebuild deletion-only: surviving sentences, original text, original order
        paras = {}
        for i, (pi, s) in enumerate(sents):
            if (i + 1) in keep:
                paras.setdefault(pi, []).append(s)
        new_tip = "".join("<p>%s</p>" % " ".join(v) for _, v in sorted(paras.items())) \
                  if paras else ""
        assert all(s in (l["exam_tip_html"] or "") for v in paras.values() for s in v), \
            "non-verbatim sentence — abort"
        backup[l["id"]] = l["exam_tip_html"]
        writes.append((l["id"], new_tip))
        report.append("- %s/%s/L%s (%s%%): %d -> %d sentence(s)%s"
                      % (subj, unit, num, pct, len(sents), len(keep),
                         " — TIP EMPTIED" if not keep else ""))
        print(report[-1])

    io.open(os.path.join(HERE, "_tip_trim_report.md"), "w", encoding="utf-8").write(
        "# Exam-tip trim pass — deletion-only\n\n" + "\n".join(report))
    print("\ntrims: %d | kept whole: %d" % (len(writes), len(report) - len(writes)))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, tip in writes:
        sb.table("lessons").update({"exam_tip_html": tip or None}).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
