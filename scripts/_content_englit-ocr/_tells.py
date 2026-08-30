# -*- coding: utf-8 -*-
"""Quantify AI-register tells per lesson, normalised per 1000 words."""
import sys, os, json, re, glob
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING","utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

def unesc(s):
    import html
    return html.unescape(s or "")

def prose(r):
    """Visible prose across the narrated fields."""
    out=[]
    for f in ("description","content_html","exam_tip_html","conclusion_html"):
        v = r.get(f) or ""
        v = unesc(v)
        v = re.sub(r'data-def="[^"]*"',' ',v)          # drop tooltip defs
        v = re.sub(r'data-revision-tip="[^"]*"',' ',v)  # drop revision tips
        v = re.sub(r'<[^>]+>',' ',v)
        out.append(v)
    return re.sub(r'\s+',' ',' '.join(out))

TELLS = {
 "emdash":            r'—',
 "not-just-X-its-Y":  r"(?i)\b(?:isn't|is not|aren't|are not|wasn't|was not|not)\s+(?:just|merely|simply|only)\b",
 "not-X-but-Y":       r"(?i)\bnot\s+\w[\w'’\- ]{0,28}?,?\s+but\s+",
 "crucially":         r"(?i)\b(?:crucially|importantly|notably|significantly|essentially|ultimately|indeed)\b",
 "in-fact/of-course": r"(?i)\b(?:in fact|of course|after all|to be clear|that said)\b",
 "remember:":         r"(?i)\bremember[:,]",
 "lets-opener":       r"(?i)(?:^|[.!?]\s|>)\s*Let(?:'|’)s\b",
 "heres-the-thing":   r"(?i)\bhere(?:'|’)s (?:the thing|why|how|what)\b",
 "its-worth-noting":  r"(?i)\bit(?:'|’)s worth (?:noting|remembering)\b",
 "think-of-it-as":    r"(?i)\bthink of (?:it|this) as\b",
 "the-X-is-Y-aphor":  r"(?i)\bthat(?:'|’)s (?:not|what|the) \w+",
}
rows=[]
for p in sorted(glob.glob(sys.argv[1])):
    r = json.load(open(p,encoding="utf-8"))
    t = prose(r)
    w = len(t.split())
    d = {"file":os.path.basename(p), "words":w}
    for k,rx in TELLS.items():
        d[k]=len(re.findall(rx,t))
    rows.append(d)

keys=list(TELLS.keys())
hdr = "%-22s %6s " % ("file","words") + " ".join("%6s"%k[:6] for k in keys)
print(hdr); print("-"*len(hdr))
for d in rows:
    print("%-22s %6d " % (d["file"][:22], d["words"]) + " ".join("%6d"%d[k] for k in keys))
print()
print("per-1000-words (em-dash density is the one to compare):")
for d in rows:
    per = 1000.0*d["emdash"]/max(d["words"],1)
    print("  %-22s %5.1f em-dash/1k  (%d dashes / %d words)" % (d["file"][:22], per, d["emdash"], d["words"]))
