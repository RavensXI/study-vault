"""Sweep + surgically repair UTF-8-as-cp1252 mojibake across all lesson and
guide text in Supabase.

  --scan          read-only: report affected rows per subject/field
  --apply         fix and PATCH (writes a jsonl backup of originals first)

!! REVIEW SCAN HITS BEFORE --apply (Jul 2026): a hit is not always mojibake.
Two content_html hits were CONTROL-CHAR-corrupted LaTeX (a JSON double-decode
ate the backslashes: \frac -> formfeed+rac, \bar -> backspace+ar, \rightarrow
-> CR+ightarrow, \text/\times -> tab+...). ftfy DELETES those control chars,
silently breaking the formula further — those rows need targeted restoration
(see the 2026-07-05 fix), and tab-corrupted \text never flags at all, so run
a control-char scan alongside this one.

Repair = ftfy.fix_text per string (handles MIXED clean/mojibake text without
round-trip corruption; NFC-safe, leaves legit text alone). HTML entities are
left exactly as-is (ftfy does not touch &rsquo; etc.), so the *_html-fields-
use-entities rule is preserved. Only changed fields are PATCHed, row by row.
"""
import argparse, io, json, os, sys, time, urllib.request

import ftfy

URL = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HDRS = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}
SC = r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad"

LESSON_FIELDS = ["title", "description", "content_html", "hero_image_caption",
                 "practice_questions", "knowledge_checks", "flashcard_questions",
                 "glossary_terms", "related_media"]
GUIDE_FIELDS = ["title", "content_html"]

CFG = ftfy.TextFixerConfig(unescape_html=False, uncurl_quotes=False,
                           fix_latin_ligatures=False, fix_character_width=False,
                           explain=False)

def fix_str(t):
    return ftfy.fix_text(t, config=CFG)

def fix_any(v):
    """Recursively fix strings inside JSON-ish values. Returns (fixed, changed)."""
    if isinstance(v, str):
        f = fix_str(v)
        return f, f != v
    if isinstance(v, list):
        out, ch = [], False
        for x in v:
            f, c = fix_any(x); out.append(f); ch = ch or c
        return out, ch
    if isinstance(v, dict):
        out, ch = {}, False
        for k, x in v.items():
            f, c = fix_any(x); out[k] = f; ch = ch or c
        return out, ch
    return v, False

def req(method, path, body=None):
    r = urllib.request.Request(URL + path, headers=dict(HDRS), method=method,
                               data=json.dumps(body).encode("utf-8") if body is not None else None)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                d = resp.read()
                return json.loads(d) if d else None
        except urllib.error.HTTPError as e:
            if e.code in (502, 503, 504, 429):
                time.sleep(3 * (attempt + 1)); continue
            print("HTTP", e.code, e.read()[:300]); raise
    raise RuntimeError("retries exhausted: " + path)

def page_rows(table, sel, order="id"):
    off, page = 0, 200
    while True:
        rows = req("GET", f"/rest/v1/{table}?select={sel}&order={order}&limit={page}&offset={off}")
        if not rows: break
        yield from rows
        if len(rows) < page: break
        off += page

def sweep(apply):
    backup = io.open(os.path.join(SC, "mojibake_backup.jsonl"), "a", encoding="utf-8") if apply else None
    stats, fixed_rows = {}, 0
    for table, fields, sel_extra in (
        ("lessons", LESSON_FIELDS, "id,lesson_number,units(slug,subjects(slug,school_id))"),
        ("guide_pages", GUIDE_FIELDS, "id,slug,guide_type,subjects(slug,school_id)"),
    ):
        sel = ",".join([sel_extra] + fields)
        n = 0
        for row in page_rows(table, sel):
            n += 1
            patch, touched = {}, []
            for f in fields:
                v = row.get(f)
                if v is None: continue
                parsed = v
                was_str_json = False
                if f not in ("title", "description", "content_html", "hero_image_caption") and isinstance(v, str):
                    try: parsed = json.loads(v); was_str_json = True
                    except Exception: parsed = v
                fixed, changed = fix_any(parsed)
                if changed:
                    patch[f] = json.dumps(fixed, ensure_ascii=False) if was_str_json else fixed
                    touched.append(f)
            if patch:
                if table == "lessons":
                    sub = (row.get("units") or {}).get("subjects") or {}
                    key = f"{sub.get('slug','?')}{'[school]' if sub.get('school_id') else ''}"
                    where = f"{key}/{(row.get('units') or {}).get('slug','?')}/{row.get('lesson_number')}"
                else:
                    sub = row.get("subjects") or {}
                    key = f"guide:{sub.get('slug','?')}"
                    where = f"{key}/{row.get('guide_type')}/{row.get('slug')}"
                for f in touched:
                    stats.setdefault(key, {}).setdefault(f, 0)
                    stats[key][f] += 1
                if apply:
                    backup.write(json.dumps({"table": table, "id": row["id"],
                        "fields": {f: row.get(f) for f in touched}}, ensure_ascii=False) + "\n")
                    req("PATCH", f"/rest/v1/{table}?id=eq.{row['id']}", patch)
                    fixed_rows += 1
                    print(f"fixed {where}: {'+'.join(touched)}", flush=True)
                else:
                    print(f"HIT  {where}: {'+'.join(touched)}", flush=True)
        print(f"({table}: {n} rows scanned)", flush=True)
    if backup: backup.close()
    print("\n=== summary ===")
    for k in sorted(stats):
        print(k, json.dumps(stats[k]))
    total = sum(sum(v.values()) for v in stats.values())
    print(f"total field-hits: {total}" + (f" | rows patched: {fixed_rows}" if apply else " (scan only)"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    sweep(a.apply)
