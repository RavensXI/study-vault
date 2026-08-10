# -*- coding: utf-8 -*-
"""Audit every music-aqa practice lesson for learn-mode visibility bugs and
data integrity.

Checks per lesson:
  A. worked_examples that reference an excerpt/extract/passage but embed no
     <audio>/<img> in the question HTML (invisible in learn mode).
  B. problem_bank passage_id values that do not exist in passages.
  C. passages with no media (no <audio>, no <img>) when problems reference them.
  D. steps not in {label, content} dict shape, or with empty content.
  E. every R2 media URL answers HTTP 200.
  F. MCQ problems with missing solutions or <2 options.

Usage: python scripts/music-practice/audit_practice_integrity.py
"""
import io
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client

REF_RE = re.compile(r"\b(excerpt|extract|passage|score|source)\s+([A-H1-9])\b", re.I)
REF_LOOSE_RE = re.compile(r"\b(the|this)\s+(excerpt|extract|passage|score)\b", re.I)
MEDIA_RE = re.compile(r"<(audio|img)\b", re.I)
URL_RE = re.compile(r"(?:src)=[\"'](https?://[^\"']+)[\"']")


def check_url(url, cache={}):
    if url in cache:
        return cache[url]
    try:
        # r2.dev 403s bare HEAD requests: use a ranged GET with a browser UA
        req = urllib.request.Request(url, headers={"Range": "bytes=0-0", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            cache[url] = 200 if r.status in (200, 206) else r.status
    except Exception as e:
        code = getattr(e, "code", None)
        cache[url] = code if code else str(e)[:60]
    return cache[url]


def main():
    sb = get_client()
    subj = sb.from_("subjects").select("id").eq("slug", "music-aqa").is_("school_id", "null").execute().data[0]
    units = sb.from_("units").select("id, slug").eq("subject_id", subj["id"]).execute().data
    findings = []
    urls = set()

    for u in sorted(units, key=lambda x: x["slug"]):
        lessons = sb.from_("lessons").select(
            "id, lesson_number, title, status, practice_data").eq("unit_id", u["id"]).order("lesson_number").execute().data
        for L in lessons:
            tag = "%s/L%d" % (u["slug"], L["lesson_number"])
            pd = L.get("practice_data")
            if not pd:
                findings.append((tag, "NO-PRACTICE-DATA", ""))
                continue
            passages = {p["id"]: p.get("text", "") for p in pd.get("passages", [])}
            for pid, txt in passages.items():
                urls.update(URL_RE.findall(txt or ""))

            # A. worked examples referencing unseen media
            for i, ex in enumerate(pd.get("worked_examples", [])):
                q = ex.get("question", "")
                refs = REF_RE.findall(q) or REF_LOOSE_RE.findall(q)
                if refs and not MEDIA_RE.search(q):
                    findings.append((tag, "EXAMPLE-REFS-UNSEEN-MEDIA",
                                     "example %d: %r -> no <audio>/<img> in question" % (i + 1, refs[:2])))
                urls.update(URL_RE.findall(q))
                # D. step shape
                for j, st in enumerate(ex.get("steps", [])):
                    if not isinstance(st, dict):
                        findings.append((tag, "STEP-NOT-DICT", "example %d step %d" % (i + 1, j + 1)))
                    elif not (st.get("content") or "").strip():
                        findings.append((tag, "STEP-EMPTY", "example %d step %d" % (i + 1, j + 1)))
                if not ex.get("steps"):
                    findings.append((tag, "EXAMPLE-NO-STEPS", "example %d" % (i + 1)))

            # B/F. problems
            bank = pd.get("problem_bank", {})
            for tier, probs in bank.items():
                for k, pr in enumerate(probs or []):
                    pid = pr.get("passage_id")
                    if pid and pid not in passages:
                        findings.append((tag, "PROBLEM-BAD-PASSAGE-ID", "%s[%d] -> %r" % (tier, k, pid)))
                    if pid and pid in passages and not MEDIA_RE.search(passages[pid] or ""):
                        findings.append((tag, "PASSAGE-NO-MEDIA", "%s[%d] -> passage %r has no audio/img" % (tier, k, pid)))
                    q = pr.get("question", "")
                    if not pid and (REF_RE.search(q) or REF_LOOSE_RE.search(q)) and not MEDIA_RE.search(q):
                        findings.append((tag, "PROBLEM-REFS-UNSEEN-MEDIA", "%s[%d]" % (tier, k)))
                    urls.update(URL_RE.findall(q))
                    it = pr.get("input_type", "")
                    if it == "multiple_choice":
                        if not pr.get("solutions"):
                            findings.append((tag, "MCQ-NO-SOLUTION", "%s[%d]" % (tier, k)))
                        if len(pr.get("options") or []) < 2:
                            findings.append((tag, "MCQ-FEW-OPTIONS", "%s[%d]" % (tier, k)))

    print("=== structural findings: %d ===" % len(findings))
    for tag, kind, detail in findings:
        print("%-28s %-26s %s" % (tag, kind, detail))

    print("\n=== media URLs: %d ===" % len(urls))
    bad = 0
    for url in sorted(urls):
        st = check_url(url)
        if st != 200:
            bad += 1
            print("%-6s %s" % (st, url))
    print("bad URLs: %d / %d" % (bad, len(urls)))


if __name__ == "__main__":
    main()
