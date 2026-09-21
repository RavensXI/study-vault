"""Does any spec slice on disk start or end in the middle of a sentence?

That is the fingerprint of a drifted window. The history-aqa and PE-OCR slices
were cut by line number with Python's str.splitlines(), which breaks on the form
feeds a PDF extraction leaves behind (197 of 209 spec files carry them), while
the line numbers themselves had been read with newline-based numbering. Every
window then starts and ends early, so it opens mid-sentence, carries the tail of
the previous section, and loses the end of its own.

Two tests, because one is not enough. A drifted window usually opens mid-clause,
but it can also land neatly on the previous section's heading — the old
america-opportunity-inequality slice opened "Part three: Stalin's USSR", which
reads like a proper start and is still the wrong option. So the second test asks
whether the opening lines mention what the file is named after.

This does NOT check whether a slice is a verbatim extract. Several subjects'
slices were deliberately edited — page footers stripped, formulae appended — and
an edited slice is fine. What is never fine is a slice that begins mid-clause,
because that means nobody chose where it started.

    python scripts/_audit_spec_slices_fleet.py
    python scripts/_audit_spec_slices_fleet.py --show    # print the first line
"""
import glob, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# a body line that opens a section: a heading, a code, a bullet, or a capital
OPENS = re.compile(r"^\s*(?:[•●▪]|[0-9]+[a-z]?[.)]|[A-Z]{1,2}[A-Z0-9]?[ .:]|Part |Option |Key topic|Section|Paper|Unit|Topic|Version|\d+c?\.\d)")
CONT = re.compile(r"^\s*(?:and|or|the|a|an|of|to|in|for|with|including|its|their|his|her|these|those|that|which|who|when|where|how|why|will|was|were|is|are|be|been|by|from|as|at|on|then|than|so|such|but|if)\b", re.I)


def first_body(text):
    for l in text.splitlines():
        s = l.strip()
        if len(s) > 25 and not s.startswith("="):
            return s
    return ""


def last_body(text):
    out = ""
    for l in text.splitlines():
        s = l.strip()
        if len(s) > 25 and not s.startswith("="):
            out = s
    return out


SLUG_STOP = {"and", "the", "of", "in", "for", "a", "an", "to", "universal", "set", "spec",
             "issues", "content", "study", "studies", "people", "britain", "england", "new"}


def slug_words(name):
    return {w for w in re.split(r"[-_]", name.lower()) if len(w) > 3 and w not in SLUG_STOP}


def main():
    show = "--show" in sys.argv
    print("%-52s %-8s %-14s %s" % ("slice", "size", "starts", "names its own topic"))
    bad = []
    for path in sorted(glob.glob(os.path.join(ROOT, "scripts", "_content_*", "_spec_*.txt"))):
        raw = io.open(path, encoding="utf-8", errors="replace").read()
        head = first_body(raw)
        # a slice that was placed deliberately opens a section; one that drifted
        # opens in the middle of someone else's sentence
        mid = bool(head) and not OPENS.match(head) and (CONT.match(head) or head[:1].islower())
        name = os.path.basename(path)[6:-4]
        # does the top of the slice mention what the file is named after?
        opening = " ".join([l for l in raw.splitlines() if l.strip()][:8]).lower()
        want = slug_words(name)
        names_it = (not want) or bool(want & set(re.findall(r"[a-z]{4,}", opening)))
        label = (os.path.basename(os.path.dirname(path))[9:] + " / " + name)
        print("%-52s %-8s %-14s %s" % (label[:52], "%d KB" % (len(raw) // 1024),
                                       "MID-SENTENCE" if mid else "a section",
                                       "yes" if names_it else "NO"))
        if show or mid or not names_it:
            print("      %s" % head[:110])
        if mid or not names_it:
            bad.append(label)
    print()
    if bad:
        print("%d slice(s) look wrongly placed — check the window before anyone builds from them:" % len(bad))
        for b in bad:
            print("  " + b)
    else:
        print("Every slice opens on a section of its own and names the topic it is filed under.")


if __name__ == "__main__":
    main()
