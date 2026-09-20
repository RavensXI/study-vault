"""Wire the judged widget queue into js/widget-embed.js MAP.
  python scripts/_jev/wire_widget_queue.py [--min-fit 0.8] [--dry]
Reads _results/widget_queue.json (from widget_match_fleet.py). Appends one MAP entry per
queued lesson: file, label, line (copied from the widget's first placement), after (the judged
heading or $end), school: "unity" for Unity lessons. Keys already in the map are skipped.
"""
import io, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
a = sys.argv[1:]; dry = "--dry" in a
min_fit = float(a[a.index("--min-fit") + 1]) if "--min-fit" in a else 0.7
q = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_results", "widget_queue.json"), encoding="utf-8"))["queue"]
p = os.path.join(ROOT, "js", "widget-embed.js"); src = io.open(p, encoding="utf-8").read()
have = set(re.findall(r'"([a-z0-9\-]+/[a-z0-9\-]+/\d+)":\s*\{', src))
def js(s): return json.dumps(s, ensure_ascii=False)
new = []
for r in q:
    if r["fit"] < min_fit or r["key"] in have: continue
    have.add(r["key"])
    ent = '    %s: {\n      file: %s,\n      label: %s,\n      line: %s,\n      after: %s%s\n    },\n' % (
        js(r["key"]), js(r["widget"]), js(r["label"]), js(r["line"]), js(r["after"]), (',\n      school: "unity"' if r["tier"] == "unity" else ""))
    new.append(ent)
m = re.search(r"\n  \};\n", src)                     # the MAP's closing brace
assert m, "MAP close not found"
out = src[:m.start()] + "\n" + "".join(new).rstrip("\n") + src[m.start():]
print("entries to add:", len(new), "| min fit", min_fit, "| dry" if dry else "")
if not dry and new:
    io.open(p, "w", encoding="utf-8", newline="\n").write(out); print("written", p)
