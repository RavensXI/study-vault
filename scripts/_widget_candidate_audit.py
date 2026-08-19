# -*- coding: utf-8 -*-
"""Which lessons across the whole site want an interactive widget?

Widgets are build-once-reuse-with-data, so the useful question is NOT
"which lessons could have one" (thousands) but "which ONE widget buys the
most coverage". This audit is therefore ARCHETYPE-first: it scans every
live article lesson for the signals of each widget archetype, then ranks
archetypes by how many lessons each would serve, split by subject.

Phase 1 (this script) is deterministic and free: no model calls. Every
match records the evidence that fired it, so the report is auditable
rather than a black box — and a candidate list you can argue with is the
whole point. Phase 2 (_widget_candidate_triage.py) sends only the top
clusters to a model to confirm and pick exemplar lessons.

    python scripts/_widget_candidate_audit.py            # full scan
    python scripts/_widget_candidate_audit.py --limit 300  # quick pass

Writes _widget_audit.json (full, machine-readable) and
_widget_audit.md (the readable ranking).
"""
import io
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_CONTENT = 800

# ---------------------------------------------------------------- archetypes
#
# Each archetype: what it would BE, and the signals that suggest a lesson
# would teach better with it. Signals are (regex, weight, label). A lesson
# needs `floor` total weight to count as a candidate — tuned so that a
# passing mention doesn't qualify a lesson, but a lesson that genuinely
# teaches the thing does.
#
ARCHETYPES = [
    {
        "key": "equation-explorer",
        "name": "Equation explorer",
        "what": "Drag one variable, watch the others move, with the equation "
                "staying visibly balanced. One component, per-lesson data: "
                "the equation, variable names, units, sensible ranges.",
        "floor": 5,
        "signals": [
            (r"\\\(|\\\[|\$\$", 1, "LaTeX equation present"),
            (r"\b(equation|formula)\b", 2, "teaches an equation/formula"),
            (r"rearrang(e|ing)|subject of the formula|make .{0,12} the subject", 3, "rearranging"),
            (r"\bunits?\b.{0,40}\b(measured in|in [A-Za-zΩ/·]{1,8})\b", 1, "units taught"),
            (r"v\s*=\s*f|f\s*=\s*|=\s*IR|V\s*=\s*I|P\s*=\s*|speed\s*=|density\s*=|moles?\s*=|"
             r"pressure\s*=|work done\s*=|magnification\s*=|=\s*mc|F\s*=\s*ma", 3, "named GCSE equation"),
            (r"worked example", 1, "worked example present"),
        ],
    },
    {
        "key": "graph-reader",
        "name": "Graph shape explorer",
        "what": "A graph the student changes the inputs of, so the SHAPE "
                "becomes the lesson (hydrograph, rate curve, velocity-time, "
                "cooling curve, demand/supply, climate graph).",
        "floor": 5,
        "signals": [
            (r"\bgraph\b", 2, "graph taught"),
            (r"\baxis|axes\b", 2, "axes discussed"),
            (r"\bgradient|slope\b", 2, "gradient read off"),
            (r"\bcurve\b", 1, "curve"),
            (r"hydrograph|climate graph|distance[- ]time|velocity[- ]time|cooling curve|"
             r"rate of reaction|supply and demand|population pyramid|titration curve", 3, "named graph type"),
            (r"\bplot(ted|ting)?\b|\binterpret\b.{0,20}\bgraph", 2, "plotting/interpreting"),
        ],
    },
    {
        "key": "process-stepper",
        "name": "Process stepper",
        "what": "Step through an ordered process one stage at a time, with "
                "the stage explained as it happens (cycles, algorithms, "
                "digestion, a bill becoming law, a production pipeline).",
        "floor": 5,
        "signals": [
            (r"\bstage\s*\d|\bstep\s*\d", 3, "numbered stages"),
            (r"\b(first|then|next|finally)\b.{0,60}\b(then|next|finally)\b", 2, "sequence language"),
            (r"\bcycle\b", 2, "a cycle"),
            (r"water cycle|carbon cycle|nitrogen cycle|rock cycle|cardiac cycle|cell cycle|"
             r"digestion|photosynthesis|respiration|mitosis|meiosis|the process of", 3, "named process"),
            (r"\bsequence\b|\border\b.{0,30}\bsteps?\b", 2, "ordering"),
            (r"\bflow ?chart\b|\balgorithm\b", 2, "flowchart/algorithm"),
        ],
    },
    {
        "key": "labelled-diagram",
        "name": "Labelled structure explorer",
        "what": "Tap parts of a structure to learn each one, then test "
                "yourself with the labels hidden (heart, eye, kidney, cell, "
                "volcano, castle, wave anatomy, an orchestra).",
        "floor": 5,
        # A lesson only qualifies if it names a real physical thing to
        # label. Without this the archetype ranked #1 on FIGURATIVE
        # language — "structure of the essay", "parts of society" put
        # Lady Macbeth and The Death Penalty top of the list (19 Aug trial).
        "require_any": ["named structure"],
        "signals": [
            (r"\bstructure of\b|\bparts? of\b|\bcomponents? of\b", 2, "structure/parts"),
            (r"\blabel(led|ling)?\b", 2, "labelling"),
            (r"\bcross[- ]section\b|\bdiagram\b", 2, "diagram/cross-section"),
            # UNAMBIGUOUS structure words only. Everyday words that happen to
            # be anatomy ("an eye for an eye", "at the heart of", "keep" as a
            # verb, "spit"/"stack"/"joint") pulled The Death Penalty and the
            # rise of the gentry into this list — see the context signal below.
            (r"\b(kidney|neurone|nephron|alveoli|alveolus|atrium|ventricle|"
             r"synapse|cell membrane|mitochondri|chloroplast|ribosome|stomata|"
             r"xylem|phloem|digestive system|small intestine|retina|cornea|cochlea|"
             r"motte[- ]and[- ]bailey|ox-?bow|meander|corrie|drumlin|longshore drift|"
             r"electrode|transformer coil|circuit diagram)\b", 3, "named structure"),
            # ambiguous anatomy only counts WITH a companion structural term
            (r"\b(heart|eye|ear|brain|lungs?)\b.{0,140}"
             r"\b(chamber|valve|aorta|pupil|lens|eardrum|bronch|lobe|cortex)\b",
             3, "named structure"),
            (r"\bidentify\b.{0,30}\b(parts|features|structures)\b", 2, "identify parts"),
        ],
    },
    {
        "key": "timeline",
        "name": "Interactive timeline",
        "what": "A draggable timeline of events with causes/consequences "
                "revealed — history's single most reusable component, and it "
                "also fixes 'which came first' confusion.",
        "floor": 6,
        "signals": [
            (r"\b1[0-9]{3}\b", 1, "a year"),
            (r"\b(1[0-9]{3})\b.{0,400}\b(1[0-9]{3})\b.{0,400}\b(1[0-9]{3})\b", 3, "three+ dates close together"),
            (r"\bchronolog|\bsequence of events\b|\btimeline\b", 3, "chronology explicit"),
            (r"\bled to\b|\bresulted in\b|\bconsequence\b|\bcaused\b", 2, "causal chain"),
        ],
    },
    {
        "key": "system-model",
        "name": "System model",
        "what": "A small dynamic model the student perturbs and watches "
                "settle — predator/prey, market equilibrium, natural "
                "selection, a food web with a species removed.",
        "floor": 5,
        "signals": [
            (r"\bequilibrium\b", 3, "equilibrium"),
            (r"predator|prey|food (web|chain)|ecosystem|interdependence", 3, "ecological system"),
            (r"supply and demand|market forces|price mechanism|elasticity", 3, "market system"),
            (r"natural selection|evolution|adaptation|gene pool", 2, "selection"),
            (r"\bfeedback\b|homeostasis|thermoregulation|osmoregulation", 3, "feedback loop"),
            (r"\bif\b.{0,40}\b(increases|decreases)\b.{0,60}\b(increases|decreases)\b", 2, "if-then relation"),
        ],
    },
    {
        "key": "classifier",
        "name": "Sort-into-categories drill",
        "what": "Drag items into the right category and get told why — "
                "ferrous vs non-ferrous, rock types, tariff types, "
                "renewable vs non-renewable, fact vs opinion.",
        "floor": 5,
        "signals": [
            (r"\bclassif(y|ied|ication)\b", 3, "classification"),
            (r"\bferrous\b|\bigneous\b|\bsedimentary\b|\bmetamorphic\b|\brenewable\b|"
             r"thermoset|thermoplastic|hardwood|softwood|\bacids? and bases?\b|"
             r"qualitative.{0,20}quantitative|\bprimary\b.{0,40}\bsecondary\b", 3, "named taxonomy"),
            (r"\btwo (main )?(types|groups|categories)\b|\bthree (main )?(types|groups|categories)\b", 3, "types/groups"),
            (r"\bcategor(y|ies|ise)\b", 2, "categories"),
            (r"\bdivided into\b|\bfall into\b|\bgrouped\b", 2, "grouping language"),
            (r"\bwhereas\b|\bin contrast\b|\bdiffer(ence|s) between\b", 1, "contrast"),
        ],
    },
    {
        "key": "map-explorer",
        "name": "Map / spatial explorer",
        "what": "A map with toggleable layers and pins — OS map skills, "
                "trench lines, migration routes, plate boundaries, "
                "case-study locations.",
        "floor": 5,
        "signals": [
            (r"\bmap\b", 2, "map"),
            (r"\bmigration\b|\btrade route|\bsettlement\b|\burban\b.{0,40}\brural\b|"
             r"\bcoastal\b.{0,40}\b(erosion|management|landform)", 2, "spatial subject"),
            (r"\bgrid reference|\bcontour|\bost?\b map|\bscale\b.{0,20}\bmap\b", 3, "map skills"),
            (r"\bplate (boundar|margin)|tectonic", 3, "tectonics"),
            (r"\blocation|\bdistribution\b|\bspatial\b", 2, "spatial language"),
            (r"\bcase study\b", 1, "case study"),
        ],
    },
    {
        "key": "quantity-builder",
        "name": "Build-it-right builder",
        "what": "Assemble something to a specification and be marked on it — "
                "balance an equation, build a circuit, construct a chord, "
                "write a balanced argument.",
        "floor": 5,
        "signals": [
            (r"balanc(e|ing|ed) (the )?equation|conservation of mass", 3, "balancing equations"),
            (r"\bcircuit\b.{0,60}\b(series|parallel)\b|\bcircuit diagram\b", 3, "circuits"),
            (r"\bchord\b|\bcadence\b|\bscale\b.{0,20}\b(major|minor)\b", 3, "music construction"),
            (r"\bconstruct\b|\bbuild\b|\bassemble\b|\bdesign a\b", 2, "construction task"),
        ],
    },
]

COMPILED = [(a, [(re.compile(p, re.I | re.S), w, lab) for p, w, lab in a["signals"]])
            for a in ARCHETYPES]


def strip(html):
    t = re.sub(r"<[^>]+>", " ", html or "")
    return re.sub(r"\s+", " ", t)


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    sb = get_client()
    subs = {s["id"]: s for s in sb.from_("subjects")
            .select("id, slug, name, exam_board, school_id, status").execute().data}
    units = {u["id"]: u for u in sb.from_("units")
             .select("id, slug, name, subject_id").execute().data}

    per_arch = defaultdict(list)
    scanned = 0
    off = 0
    page_size = 200
    while True:
        page = sb.from_("lessons").select(
            "id, unit_id, lesson_number, title, status, content_html") \
            .eq("status", "live").order("id").range(off, off + page_size - 1).execute().data
        if not page:
            break
        for les in page:
            html = les.get("content_html") or ""
            if len(html) < MIN_CONTENT:
                continue
            unit = units.get(les["unit_id"])
            if not unit:
                continue
            subj = subs.get(unit["subject_id"])
            if not subj:
                continue
            text = strip(html)
            title_l = (les["title"] or "").lower()
            if title_l.startswith(("exam technique", "revision technique", "how to revise")):
                continue
            scanned += 1
            for arch, pats in COMPILED:
                score = 0
                why = []
                for rx, weight, label in pats:
                    if rx.search(text):
                        score += weight
                        why.append(label)
                need = arch.get("require_any")
                if need and not any(n in why for n in need):
                    continue
                if score >= arch["floor"]:
                    per_arch[arch["key"]].append({
                        "score": score,
                        "lesson_id": les["id"],
                        "title": les["title"],
                        "subject": subj["slug"],
                        "subject_name": subj["name"],
                        "board": subj.get("exam_board"),
                        "school": bool(subj.get("school_id")),
                        "unit": unit["slug"],
                        "n": les["lesson_number"],
                        "url": "/lesson/%s/%s/%d" % (subj["slug"], unit["slug"], les["lesson_number"]),
                        "why": why,
                    })
        off += page_size
        print("  scanned %d lessons..." % scanned)
        if limit and scanned >= limit:
            break

    # ------------------------------------------------------------- report
    out = {"scanned": scanned, "archetypes": []}
    for arch, _ in COMPILED:
        hits = sorted(per_arch[arch["key"]], key=lambda h: -h["score"])
        by_subject = defaultdict(int)
        for h in hits:
            by_subject[h["subject"]] += 1
        out["archetypes"].append({
            "key": arch["key"], "name": arch["name"], "what": arch["what"],
            "lessons": len(hits),
            "subjects": sorted(by_subject.items(), key=lambda kv: -kv[1]),
            "top": hits[:40],
        })
    out["archetypes"].sort(key=lambda a: -a["lessons"])

    io.open(os.path.join(HERE, "_widget_audit.json"), "w", encoding="utf-8") \
        .write(json.dumps(out, indent=1))

    md = ["# Interactive widget candidates — site-wide audit", "",
          "Deterministic scan of **%d live article lessons**. Archetype-first: "
          "widgets are build-once-reuse-with-data, so what matters is how many "
          "lessons ONE component would serve." % scanned, "",
          "| Rank | Widget archetype | Lessons it would serve | Biggest subjects |",
          "|---|---|---|---|"]
    for i, a in enumerate(out["archetypes"], 1):
        top_subj = ", ".join("%s (%d)" % (s, n) for s, n in a["subjects"][:4])
        md.append("| %d | **%s** | %d | %s |" % (i, a["name"], a["lessons"], top_subj))
    md.append("")
    for a in out["archetypes"]:
        md.append("## %s — %d lessons" % (a["name"], a["lessons"]))
        md.append("")
        md.append(a["what"])
        md.append("")
        md.append("Strongest candidates:")
        md.append("")
        for h in a["top"][:12]:
            md.append("- `%s` **%s** — %s %s · _%s_" %
                      (h["url"], h["title"], h["subject_name"], h["board"] or "",
                       ", ".join(h["why"][:4])))
        md.append("")
    io.open(os.path.join(HERE, "_widget_audit.md"), "w", encoding="utf-8").write("\n".join(md))

    print("\nScanned %d lessons." % scanned)
    for a in out["archetypes"]:
        print("  %-32s %4d lessons" % (a["name"], a["lessons"]))
    print("\nWrote scripts/_widget_audit.json and scripts/_widget_audit.md")


if __name__ == "__main__":
    main()
