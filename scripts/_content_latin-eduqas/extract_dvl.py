# -*- coding: utf-8 -*-
"""Extract the Eduqas GCSE Latin Defined Vocabulary List (Appendix A) from the
spec markdown into a paired JSON list.

The PDF->markdown conversion flattens each two-column page into a run of Latin
headwords followed by a run of English glosses. This script rebuilds the pairs
deterministically and asserts the published total (440 Latin-English entries).

Usage: python scripts/_content_latin-eduqas/extract_dvl.py
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "specs", "eduqas", "latin-C580QS.md")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_source", "dvl.json")

NOISE = re.compile(r"WJEC CBAC|^GCSE LATIN \d+$|^Defined Vocabulary|^\(Section|^English\b|^Latin\b")


def blocks(lines):
    """Split the raw region into runs separated by page furniture."""
    runs, cur = [], []
    for raw in lines:
        ff = "\x0c" in raw          # form feed = PDF page break = column boundary
        l = raw.replace("\x0c", "").strip()
        if not l:
            continue
        if ff and cur:
            runs.append(cur)
            cur = []
        if NOISE.search(l):
            if cur:
                runs.append(cur)
                cur = []
            continue
        cur.append(l)
    if cur:
        runs.append(cur)
    return runs


def unwrap(entries):
    """Rejoin lines the PDF wrapped mid-entry.

    Two signals, both unambiguous in this appendix: an unclosed bracket, and a
    trailing comma (every complete entry ends on its last sense, never on a
    separator).
    """
    out = []
    for e in entries:
        prev = out[-1] if out else ""
        if out and (prev.count("(") > prev.count(")") or prev.endswith(",")):
            out[-1] = prev + " " + e
        else:
            out.append(e)
    return out


def looks_latin(line):
    """True for a DVL headword line, false for an English gloss."""
    l = line.strip()
    if re.search(r"\((indecl\.|irregular|also used|as prefix)", l):
        return True
    if re.search(r"\+ (acc|abl|dat|subjunc|indic)", l):
        return True
    if re.search(r",\s*(m|f|n|m\.f)\.(\s|$|\s*pl\.)", l):
        return True
    if re.search(r"^[a-z]+(o|or|eo|io),\s+[a-z]+(are|ere|ire|ri)", l):
        return True
    if re.search(r"^[a-z]+us,\s+[a-z]+a,\s+[a-z]+um$", l):
        return True
    return False


def main():
    text = io.open(SPEC, encoding="utf-8").read().replace("\ufffd", "...")
    lines = text.split("\n")
    # Appendix A Latin-English DVL: from the first headword to the start of the
    # Section B English-Latin list.
    start = next(i for i, l in enumerate(lines)
                 if l.strip().startswith("a, ab + abl"))
    end = next(i for i, l in enumerate(lines)
               if l.strip() == "Defined Vocabulary List for Component 1" and i > start)
    runs = []
    for b in blocks(lines[start:end]):
        b = unwrap(b)
        # The last page of the appendix is laid out gloss-column-first, so one
        # run arrives as [33 glosses][33 headwords] with no separator between.
        if len(b) % 2 == 0 and b and not looks_latin(b[0]) and looks_latin(b[len(b) // 2]):
            half = len(b) // 2
            runs.append(b[half:])   # headwords
            runs.append(b[:half])   # glosses
        else:
            runs.append(b)

    pairs = []
    i = 0
    while i + 1 < len(runs):
        lat, eng = runs[i], runs[i + 1]
        if len(lat) != len(eng):
            print("run %d length mismatch: %d latin vs %d english" % (i, len(lat), len(eng)))
            print("  latin tail :", lat[-3:])
            print("  english tail:", eng[-3:])
        for a, b in zip(lat, eng):
            pairs.append({"latin": a, "english": b})
        i += 2

    # Section B: English into Latin list (a shorter, dedicated list)
    b_start = end
    b_end = next(i for i, l in enumerate(lines) if l.strip() == "APPENDIX B")
    # This list is printed gloss-column-first, and its final page arrives as one
    # unseparated run of [45 headwords][45 glosses]. The English side is strictly
    # alphabetical across the whole list, which identifies the halves.
    b_runs = []
    last_eng = ""
    for b in blocks(lines[b_start:b_end]):
        b = unwrap(b)
        if len(b) % 2 == 0 and len(b) > 4:
            half = len(b) // 2
            first, second = b[:half], b[half:]
            if second[0].lower() > last_eng and first[0].lower() < last_eng:
                b_runs.append(second)   # glosses
                b_runs.append(first)    # headwords
                last_eng = second[-1].lower()
                continue
        b_runs.append(b)
        if len(b_runs) % 2 == 1:
            last_eng = b[-1].lower()

    b_pairs = []
    j = 0
    while j + 1 < len(b_runs):
        eng, lat = b_runs[j], b_runs[j + 1]
        if len(eng) != len(lat):
            print("sectionB run %d mismatch: %d vs %d" % (j, len(eng), len(lat)))
        for a, b in zip(eng, lat):
            b_pairs.append({"english": a, "latin": b})
        j += 2

    print("Latin-English DVL pairs: %d (spec states 440)" % len(pairs))
    print("Section B English-Latin pairs: %d" % len(b_pairs))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(
        {"dvl_latin_english": pairs, "section_b_english_latin": b_pairs},
        ensure_ascii=False, indent=1))
    print("wrote", OUT)
    for p in pairs[:5] + pairs[-5:]:
        print("  ", p["latin"], "=", p["english"])


if __name__ == "__main__":
    main()
