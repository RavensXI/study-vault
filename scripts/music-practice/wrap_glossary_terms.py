# -*- coding: utf-8 -*-
"""Wrap glossary terms in the 50 new-board music article lessons (Tom's
review find, 16 Aug): the builders filled glossary_terms JSON but never
wrapped occurrences in content, so no underlined hover-definitions
rendered. music-aqa and music-technology are fully wrapped; the gap is
exactly music-eduqas (14), music-ocr (16), music-edexcel (20).

House markup (from history-eduqas):
  <dfn class="term" data-def="Definition text">phrase</dfn>

Rules: first case-insensitive whole-word occurrence per term, prose
text only (never inside h2/h3, figcaption, button, an existing dfn, or
any tag/attribute), longest terms wrapped first so 'concerto grosso'
beats 'concerto'. Wrapping adds NO text, so narration stays valid
(asserted).

Run: python wrap_glossary_terms.py [--apply]
Backup: _backup_glossary_wrap_2026-08-16.json
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_glossary_wrap_2026-08-16.json")
SUBJECTS = {
    "music-eduqas": ("aos1-forms-and-devices", "aos2-music-for-ensemble",
                     "aos3-film-music", "aos4-popular-music"),
    "music-ocr": ("aos2-the-concerto-through-time", "aos3-rhythms-of-the-world",
                  "aos4-film-music", "aos5-conventions-of-pop"),
    "music-edexcel": ("aos1-instrumental-music", "aos2-vocal-music",
                      "aos3-stage-and-screen", "aos4-fusions"),
}
SKIP_TAGS = {"h2", "h3", "figcaption", "button", "dfn", "script", "style"}


def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def wrap_lesson(ch, glossary):
    """Wrap first eligible occurrence of each term. Returns (html, wrapped,
    missed)."""
    wrapped, missed = [], []
    for g in sorted(glossary, key=lambda g: -len(g.get("term") or "")):
        term = (g.get("term") or "").strip()
        definition = (g.get("definition") or "").strip()
        if not term or not definition:
            continue
        tokens = re.split(r"(<[^>]+>)", ch)
        stack = []
        done = False
        for i, tok in enumerate(tokens):
            if done:
                break
            if tok.startswith("<"):
                m = re.match(r"</?([a-zA-Z0-9]+)", tok)
                if m:
                    tag = m.group(1).lower()
                    if tok.startswith("</"):
                        if stack and stack[-1] == tag:
                            stack.pop()
                        elif tag in stack:
                            stack.remove(tag)
                    elif not tok.endswith("/>") and tag not in (
                            "br", "img", "hr", "iframe", "input"):
                        stack.append(tag)
                continue
            if any(t in SKIP_TAGS for t in stack):
                continue
            for pat in (r"\b%s\b" % re.escape(term),
                        r"\b%ss?\b" % re.escape(term.rstrip("s"))):
                m = re.search(pat, tok, re.I)
                if m:
                    dfn = '<dfn class="term" data-def="%s">%s</dfn>' % (
                        esc_attr(definition), m.group(0))
                    tokens[i] = tok[:m.start()] + dfn + tok[m.end():]
                    ch = "".join(tokens)
                    wrapped.append(term)
                    done = True
                    break
        if not done:
            missed.append(term)
    return ch, wrapped, missed


def main():
    sb = get_client()
    units = sb.table("units").select("id,slug,subject_id").execute().data
    subs = {s["slug"]: s["id"] for s in
            sb.table("subjects").select("id,slug,school_id").execute().data
            if not s["school_id"] and s["slug"] in SUBJECTS}
    backup, writes = {}, []
    tot_w = tot_m = 0
    for slug, unit_slugs in SUBJECTS.items():
        umap = {u["slug"]: u["id"] for u in units
                if u["subject_id"] == subs[slug]}
        for uslug in unit_slugs:
            rows = sb.table("lessons").select(
                "id,lesson_number,content_html,glossary_terms") \
                .eq("unit_id", umap[uslug]).order("lesson_number") \
                .execute().data
            for l in rows:
                ch = l.get("content_html") or ""
                gl = l.get("glossary_terms") or []
                if not ch or not gl or 'class="term"' in ch:
                    continue
                new_ch, wrapped, missed = wrap_lesson(ch, gl)
                # safety: no text change, no narration id change
                strip = lambda s: re.sub(r"\s+", "",
                                         re.sub(r"<[^>]+>", "", s))
                assert strip(new_ch) == strip(ch), \
                    "%s %s L%d text changed" % (slug, uslug,
                                                l["lesson_number"])
                assert (re.findall(r'data-narration-id="[^"]+"', new_ch) ==
                        re.findall(r'data-narration-id="[^"]+"', ch))
                tot_w += len(wrapped)
                tot_m += len(missed)
                print("%s %s L%d: %d wrapped%s"
                      % (slug, uslug, l["lesson_number"], len(wrapped),
                         (" | missed: %s" % ", ".join(missed[:4]))
                         if missed else ""))
                if wrapped:
                    backup[l["id"]] = ch
                    writes.append((l["id"], new_ch))
    print("\nterms wrapped: %d | not found in prose: %d | lessons: %d"
          % (tot_w, tot_m, len(writes)))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
