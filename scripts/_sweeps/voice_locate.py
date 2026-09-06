"""
Locate every narrated examiner-voice hit inside its RAW field text.

labels/_narrated_worklist.json stores the PLAIN-TEXT sentence (tags stripped,
entities unescaped, whitespace collapsed). A find/replace patch has to target
the RAW html, so this script rebuilds the plain text with a character-level
map back into the raw string and cuts the exact raw substring for each hit.

    python scripts/_sweeps/voice_locate.py --subject astronomy-edexcel
    python scripts/_sweeps/voice_locate.py --all

Writes scripts/_sweeps/voice/_raw_<subject>.json:
    [{n, lesson_id, lesson_number, field, plain, raw, before, after, occurrences}]
`raw` is byte-for-byte from the live column: paste it into an edit's "find".
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "voice")
os.makedirs(OUT, exist_ok=True)
WORKLIST = os.path.join(HERE, "labels", "_narrated_worklist.json")

U = os.environ["SUPABASE_URL"]
K = os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": K, "Authorization": "Bearer " + K}

ENT = re.compile(r"&(#\d+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")


def api(path, tries=5):
    for a in range(tries):
        try:
            req = urllib.request.Request(f"{U}/rest/v1/{path}", headers=HDR)
            return json.loads(urllib.request.urlopen(req, timeout=180).read())
        except Exception:
            if a == tries - 1:
                raise
            time.sleep(2 * (a + 1))


def tokenise(html):
    """[(plain_char, raw_start, raw_len)] reproducing sweep_labels.plain()."""
    toks, i, n = [], 0, len(html)
    while i < n:
        c = html[i]
        if c == "<":
            j = html.find(">", i)
            if j == -1:
                toks.append((c, i, 1))
                i += 1
                continue
            toks.append((" ", i, j - i + 1))
            i = j + 1
            continue
        if c == "&":
            m = ENT.match(html, i)
            if m:
                s = unescape(m.group(0))
                if s != m.group(0):
                    for k, ch in enumerate(s):
                        toks.append((ch, i, len(m.group(0)) if k == 0 else 0))
                    i = m.end()
                    continue
        toks.append((c, i, 1))
        i += 1
    # \xa0 -> space, then collapse whitespace runs into one space
    out, prev_ws = [], False
    for ch, s, ln in toks:
        if ch == "\xa0":
            ch = " "
        if ch.isspace():
            if prev_ws and out:
                ch0, s0, l0 = out[-1]
                out[-1] = (ch0, s0, max(l0, s + ln - s0))
                continue
            out.append((" ", s, ln))
            prev_ws = True
        else:
            out.append((ch, s, ln))
            prev_ws = False
    while out and out[0][0] == " ":
        out.pop(0)
    while out and out[-1][0] == " ":
        out.pop()
    return out


def locate(html, sentence):
    """Return (raw_substring, raw_start, raw_end, occurrences) or None."""
    toks = tokenise(html)
    text = "".join(t[0] for t in toks)
    occ = text.count(sentence)
    if occ == 0:
        return None
    i = text.index(sentence)
    j = i + len(sentence)
    start = toks[i][1]
    end = max(s + ln for _c, s, ln in toks[i:j])
    return html[start:end], start, end, occ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--pad", type=int, default=130)
    args = ap.parse_args()

    wl = json.load(open(WORKLIST, encoding="utf-8"))
    hits = wl["hits"]
    subjects = sorted({h["subject"] for h in hits}) if args.all else [args.subject]
    if not args.all and not args.subject:
        ap.error("pass --subject or --all")

    for slug in subjects:
        mine = [h for h in hits if h["subject"] == slug]
        ids = sorted({h["lesson_id"] for h in mine})
        rows = {}
        for i in range(0, len(ids), 25):
            q = urllib.parse.quote(",".join(ids[i:i + 25]), safe="")
            for r in api(f"lessons?id=in.({q})&select=id,lesson_number,title,"
                         f"content_html,conclusion_html,narration_manifest"):
                rows[r["id"]] = r
        recs = []
        for k, h in enumerate(mine):
            row = rows.get(h["lesson_id"])
            html = (row or {}).get(h["field"]) or ""
            got = locate(html, h["sentence"]) if html else None
            rec = {"n": k, "lesson_id": h["lesson_id"], "lesson_number": h["lesson_number"],
                   "title": (row or {}).get("title"), "field": h["field"],
                   "narrated": bool((row or {}).get("narration_manifest")),
                   "plain": h["sentence"]}
            if got is None:
                rec["raw"] = None
                rec["error"] = "sentence not found in live field (truncated at 300 chars?)"
                # retry on the 300-char-truncated prefix
                got2 = locate(html, h["sentence"][:200]) if html else None
                if got2:
                    rec["raw_prefix"] = got2[0]
            else:
                raw, s, e, occ = got
                rec.update({"raw": raw, "occurrences": occ,
                            "raw_occurrences": html.count(raw),
                            "before": html[max(0, s - args.pad):s],
                            "after": html[e:e + args.pad]})
            recs.append(rec)
        p = os.path.join(OUT, f"_raw_{slug}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(recs, f, ensure_ascii=False, indent=1)
        bad = sum(1 for r in recs if not r.get("raw"))
        dup = sum(1 for r in recs if r.get("raw_occurrences", 1) != 1)
        print(f"{slug}: {len(recs)} hits -> {p}"
              + (f"  ({bad} unlocated)" if bad else "")
              + (f"  ({dup} non-unique)" if dup else ""))


if __name__ == "__main__":
    main()
