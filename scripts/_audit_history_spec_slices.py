"""Did the history-aqa build follow the wrong spec slices?

scripts/_prep_history_aqa_content.py cut one text slice per option out of
specs/aqa/history-8145-8145.md using the line ranges in the plan shell. The
ranges were taken with newline-based line numbers; the slicer used Python's
str.splitlines(), which ALSO breaks on the 43 form feeds the PDF extraction left
in the file. Every slice therefore drifts, and the drift grows down the document,
so each file holds the tail of a neighbouring option.

This checks whether that reached the lessons. For each unit it prints the option
the slice SHOULD have carried, the option it actually carried, and then counts
how often the wrong option's distinctive vocabulary appears in that unit's live
lesson text, against the right option's.

    python scripts/_audit_history_spec_slices.py
"""
import io, json, os, re, sys, urllib.request
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "specs", "aqa", "history-8145-8145.md")
SHELL = os.path.join(ROOT, "scripts", "_plan_history-aqa-shell.json")
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
SUBJECT = "e8cc884b-9619-4303-8c2f-c7531210ab6e"

STOP = set("""the a an and or of to in for on with by from as at is are was were be been being this that these those
it its their his her they them he she we you i not no but if then than so such which who whom whose what when where
how why all any both each few more most other some only own same too very can will just should now students will
be expected understand ways key features aspects site representative period studied part one two three four
their own study focus development including impact role causes consequences reasons changes change developments
and/or eg ie page pages specification aqa gcse history visit resources support""".split())


def words(text):
    return [w for w in re.findall(r"[a-z][a-z'-]{3,}", (text or "").lower()) if w not in STOP]


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())


def main():
    raw = io.open(SPEC, encoding="utf-8").read()
    by_newline = raw.split("\n")          # what the line numbers in the plan mean
    by_splitlines = raw.splitlines()      # what the slicer actually used
    print("spec file: %d lines by newline, %d by splitlines, %d form feeds\n"
          % (len(by_newline), len(by_splitlines), raw.count("\f")))

    shell = json.load(io.open(SHELL, encoding="utf-8"))
    units = {}
    for u in shell["unit_shells"]:
        a, b = (int(x) for x in u["spec_line_range"].split("-"))
        units[u["slug"]] = {
            "right": "\n".join(by_newline[a - 1:b]),
            "wrong": "\n".join(by_splitlines[a - 1:b]),
        }

    rows, off = [], 0
    while True:
        page = get("lessons?select=title,lesson_number,status,description,content_html,units!inner(slug,subject_id)"
                   "&units.subject_id=eq.%s&order=id&limit=200&offset=%d" % (SUBJECT, off))
        rows += page
        if len(page) < 200:
            break
        off += 200
    live = {}
    for r in rows:
        if r["status"] != "live":
            continue
        live.setdefault(r["units"]["slug"], []).append(r)

    # A term is distinctive to an option when it appears in that option's OWN
    # correct slice and in no other option's. Counting shared words ("control",
    # "party", "over") measures nothing: the first run of this script called
    # every unit contaminated on exactly that mistake.
    vocab = {slug: set(words(s["right"])) for slug, s in units.items()}
    distinctive = {}
    for slug, vs in vocab.items():
        others = set().union(*[v for k, v in vocab.items() if k != slug])
        distinctive[slug] = {w for w in vs if w not in others and len(w) >= 5}

    rows2, off = [], 0
    while True:
        page = get("lessons?select=title,lesson_number,status,description,content_html,units!inner(slug,subject_id)"
                   "&units.subject_id=eq.%s&order=id&limit=200&offset=%d" % (SUBJECT, off))
        rows2 += page
        if len(page) < 200:
            break
        off += 200
    live = {}
    for r in rows2:
        if r["status"] == "live":
            live.setdefault(r["units"]["slug"], []).append(r)

    print("%-34s %-8s %-26s %s" % ("unit", "lessons", "own option's own terms", "terms only the leaked option has"))
    flagged = []
    for slug, s in units.items():
        ls = live.get(slug, [])
        if not ls:
            print("%-34s %-8d %s" % (slug[:34], 0, "no live lessons"))
            continue
        text = " ".join((l["title"] or "") + " " + (l["description"] or "") + " " +
                        re.sub(r"<[^>]+>", " ", l["content_html"] or "") for l in ls).lower()
        toks = Counter(re.findall(r"[a-z][a-z'-]{3,}", text))
        mine = sorted(((toks[w], w) for w in distinctive[slug] if toks[w]), reverse=True)
        # what leaked into this unit's slice: the previous option in the file
        leak_words = set(words(s["wrong"])) - set(words(s["right"]))
        leaked_from = sorted(((len(leak_words & distinctive[o]), o) for o in units if o != slug), reverse=True)
        src = leaked_from[0][1] if leaked_from and leaked_from[0][0] else None
        alien = sorted(((toks[w], w) for w in (distinctive.get(src, set()) & leak_words) if toks[w]), reverse=True) if src else []
        print("%-34s %-8d %-26s %s" % (
            slug[:34], len(ls),
            ", ".join("%s(%d)" % (w, n) for n, w in mine[:3]) or "none",
            ("from %s: " % src[:22] + (", ".join("%s(%d)" % (w, n) for n, w in alien[:4]) if alien else "none")) if src else "-"))
        if alien:
            flagged.append((slug, src, alien[:4]))
    print()
    if flagged:
        print("Units carrying vocabulary unique to the option that leaked into their slice:")
        for slug, src, alien in flagged:
            print("  %-34s %s -> %s" % (slug, src, ", ".join("%s(%d)" % (w, n) for n, w in alien)))
    else:
        print("No unit uses a single term unique to the option whose text leaked into its slice.")


if __name__ == "__main__":
    main()
