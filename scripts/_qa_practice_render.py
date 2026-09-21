"""Renderer-contract gate for practice_data. The check that was missing.

scripts/_qa_practice_data.py validates generic shape: are solutions a list, is there an ask,
is the lesson the right size. It passed clean on 20 problems that rendered NOTHING and on 104
whose colour key contradicted itself, because it never asks the only question that matters:
does each problem carry the fields the RENDERER reads, in a form it can use?

Two site-wide faults found in minutes on 21 Sep 2026 (Tom): misleading_summary problems
carrying `statements`/`options` instead of `summaryParts`, so renderMS threw and the next
problem bled into the card; and traffic_light categories ordered so the green dot landed on
the false answer. Both classes are now checked here.

Contracts are taken from practice.html's render functions. Add a row when a type is added.

  python scripts/_qa_practice_render.py                 # every live practice lesson
  python scripts/_qa_practice_render.py --all           # include pending_review
  python scripts/_qa_practice_render.py --subject SLUG
Exit code 1 if anything is broken, so it can gate a build.
"""
import json, os, sys, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}

# input_type -> fields the renderer dereferences without guarding
REQUIRED = {
    "multiple_choice":    ["options", "solutions"],
    "traffic_light":      ["statements"],
    "highlight_evidence": ["answer_text"],
    "connotation_picker": ["chips"],
    "evidence_match":     ["claims", "quotes"],
    "misleading_summary": ["summaryParts"],
    # ai_mark / ai_write are checked below: the renderer accepts EITHER an inline
    # ai_system_prompt (the MFL convention) OR an ai_prompt_key into ai_marking_prompts.
    "ai_mark":            [],
    "ai_write":           [],
    "improve_sentence":   ["original"],
    "spot_error":         ["tokens"],
    "reorder":            ["items", "correct_order"],
    "single_value":       ["solutions"],
    "two_solutions":      ["solutions"],
    "fraction":           ["solutions"],
    "standard_form":      ["solutions"],
}
NEG = ("not ", "no ", "false", "unsupported", "stretch", "misleading", "wrong", "inaccurate", "incorrect")
POS = ("true", "supported", "correct", "accurate", "yes")

def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())

def check(q, prompts):
    """-> list of problem descriptions."""
    out = []
    t = q.get("input_type")
    for f in REQUIRED.get(t, []):
        if q.get(f) in (None, [], {}):
            out.append("%s missing %s - renders blank" % (t, f))
    if t in ("ai_mark", "ai_write"):
        if q.get("ai_prompt_key"):
            if q["ai_prompt_key"] not in (prompts or {}):
                out.append("%s points at ai_prompt_key '%s', which this lesson does not define" % (t, q["ai_prompt_key"]))
        elif not q.get("ai_system_prompt"):
            out.append("%s has neither ai_system_prompt nor ai_prompt_key - falls back to a generic marker" % t)
    if t == "traffic_light":
        cats = []
        for s in (q.get("statements") or []):
            c = s.get("correct") if isinstance(s, dict) else None
            if not isinstance(c, str):
                out.append("traffic_light category %r is not a string - throws in renderTL" % (c,)); break
            if c not in cats: cats.append(c)
        if len(cats) >= 2:
            first, rest = cats[0].lower(), " ".join(cats[1:]).lower()
            if any(w in first for w in NEG) and any(w in rest for w in POS) and not any(w in first for w in POS):
                out.append("traffic_light puts the green dot on '%s' - the key contradicts itself" % cats[0])
        if any(str(c).lower() in ("green", "amber", "red", "yellow") for c in cats):
            out.append("traffic_light categories are colour words; the renderer colours by position, not by name")
    if t == "misleading_summary" and not any(isinstance(p, dict) and "wrong" in p for p in (q.get("summaryParts") or [])):
        out.append("misleading_summary has no clickable part - every summaryPart needs a 'wrong' key")
    if t == "multiple_choice":
        sol, opts = q.get("solutions"), q.get("options") or []
        if isinstance(sol, list) and any(not isinstance(i, int) or i < 0 or i >= len(opts) for i in sol):
            out.append("multiple_choice solutions %r out of range for %d options" % (sol, len(opts)))
    return out

def main():
    only = sys.argv[sys.argv.index("--subject") + 1] if "--subject" in sys.argv else None
    everything = "--all" in sys.argv
    rows, off = [], 0
    while True:
        page = get("lessons?select=title,lesson_number,status,practice_data,units!inner(slug,subjects!inner(slug))"
                   "&practice_data=not.is.null&order=id&limit=500&offset=%d" % off)
        rows += page
        if len(page) < 500: break
        off += 500
    bad = 0; seen = 0
    for r in rows:
        sub = r["units"]["subjects"]["slug"]
        if only and sub != only: continue
        if r["status"] != "live" and not (everything or only): continue
        pd = r["practice_data"] or {}
        pb = pd.get("problem_bank")
        if not isinstance(pb, dict): continue
        prompts = pd.get("ai_marking_prompts") or {}
        for tier, qs in pb.items():
            if not isinstance(qs, list): continue
            for i, q in enumerate(qs):
                if not isinstance(q, dict): continue
                seen += 1
                for msg in check(q, prompts):
                    bad += 1
                    print("  %-26s %-20s L%-3s %s[%d]  %s" % (sub, r["units"]["slug"], r["lesson_number"], tier, i, msg))
    print("\n%d problems checked against the renderer contract | %d broken" % (seen, bad))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
