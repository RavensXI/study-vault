"""Scan English practice lessons for the fault classes the visual walk found.

The visual walk (scripts/_qa_visual_walk.py) looks at pixels and flagged 73 of 991
screens in Edexcel English Language 2.0 on 22 Sep 2026. Pixels say THAT something
looks wrong; this says WHY, from the stored problem, so every instance of a class
is found — not only the ones a screenshot happened to catch — and so the false
positives can be told apart from real faults.

Classes (each is a precise data signature):
  TL_MISSING   traffic light whose stem offers three choices (true / partly / false)
               while its statements use fewer — the renderer derives choices from
               the answers, so the missing one is never offered and colours shift
  REF_OTHER    stem names "Model B" / "Source C" but the problem is attached to a
               different passage, so the wrong text sits beside the question
  REF_ABSENT   stem names a passage letter the lesson does not have
  COMPARE      stem compares two named passages; the panel can show only one
  EM_ORPHAN    evidence-match claim with no quote marked as its answer (throws)
  HL_EMPTY     highlight question with no passage text to highlight
  HL_PARA      highlight question that points at "the second paragraph" of a
               passage the highlighter flattens into one block
  SE_SPACING   spot-the-error sentence that renders "issue ," or "companys ."
  STEM_PLACEHOLDER  the stem is the placeholder "Answer using the extract." (build.py filled
               it in when the model returned a problem with no stem at all)
  TL_NAMED     informational: traffic lights with more than three categories, which the
               renderer now draws as named dropdowns

  python scripts/_qa_englang_faults.py                          # 1EN2, every lesson
  python scripts/_qa_englang_faults.py --subject english-language-edexcel
  python scripts/_qa_englang_faults.py --class TL_MISSING --show
"""
import io, json, os, re, sys, urllib.request
from collections import Counter, defaultdict

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}

THREE_WAY = re.compile(r"\bpartly\b|\bamber\b|\bpartially\b|three (options|choices|categories)", re.I)
REF = re.compile(r"\b(Model|Source|Extract|Text|Draft|Response)\s+([A-E])\b")
PUNCT = re.compile(r"^[.,;:!?)\]’”]")


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())


def stem_of(q):
    return q.get("question") or q.get("ask") or q.get("prompt") or ""


def passage_letter(p):
    m = re.search(r"\b(Model|Source|Extract|Text|Draft|Response)\s+([A-E])\b", (p or {}).get("label") or "")
    return (m.group(1).lower(), m.group(2)) if m else None


def categories(q):
    cats = []
    for s in q.get("statements") or []:
        c = s.get("correct") if isinstance(s, dict) else None
        if isinstance(c, str) and c not in cats:
            cats.append(c)
    return cats


def rendered_tokens(q):
    """The spot-error sentence exactly as renderSpotError() joins it."""
    toks = [t.get("text", "") for t in (q.get("tokens") or []) if isinstance(t, dict)]
    own = any(re.search(r"\s", t) for t in toks)
    out = ""
    for i, t in enumerate(toks):
        if i > 0 and not own and not PUNCT.match(t):
            out += " "
        out += t
    return out


def scan(rows):
    found = defaultdict(list)
    for r in rows:
        pd = r["practice_data"] or {}
        passages = {p.get("id"): p for p in (pd.get("passages") or []) if isinstance(p, dict)}
        letters = {}
        for pid, p in passages.items():
            pl = passage_letter(p)
            if pl:
                letters[pl[1]] = pid
        where = "%s/%s" % (r["units"]["slug"], r["lesson_number"])
        for tier, qs in (pd.get("problem_bank") or {}).items():
            if not isinstance(qs, list):
                continue
            for i, q in enumerate(qs):
                if not isinstance(q, dict):
                    continue
                t, stem = q.get("input_type"), stem_of(q)
                tag = {"where": where, "tier": tier, "i": i, "type": t, "stem": stem[:150], "lesson_id": r["id"]}
                if t == "traffic_light":
                    cats = categories(q)
                    if THREE_WAY.search(stem) and len(cats) < 3 and not q.get("categories"):
                        found["TL_MISSING"].append(dict(tag, cats=cats))
                    # more than three categories: practice.html names each choice in a
                    # dropdown since 22 Sep 2026, so this is informational, not a fault
                    if len(q.get("categories") or cats) > 3:
                        found["TL_NAMED"].append(dict(tag, cats=q.get("categories") or cats))
                refs = [(k.lower(), L) for k, L in REF.findall(stem)]
                named = sorted({L for _, L in refs})
                own = passages.get(q.get("passage_id"))
                own_l = passage_letter(own)[1] if passage_letter(own) else None
                if len(named) >= 2:
                    # resolved when the problem carries both passages (passage_ids), and
                    # not a fault when it plans a comparison from ONE text on purpose
                    solo = re.search(r"\bONLY this (passage|extract|text)\b|a second text you have read", stem, re.I)
                    if not solo and not (isinstance(q.get("passage_ids"), list) and len(q["passage_ids"]) > 1):
                        found["COMPARE"].append(dict(tag, named=named, own=own_l, has=sorted(letters)))
                elif len(named) == 1:
                    L = named[0]
                    if L not in letters:
                        found["REF_ABSENT"].append(dict(tag, named=L, has=sorted(letters)))
                    elif own_l != L:
                        found["REF_OTHER"].append(dict(tag, named=L, own=own_l, should=letters[L]))
                if stem.strip() == "Answer using the extract.":
                    found["STEM_PLACEHOLDER"].append(tag)
                if t == "evidence_match":
                    claims = q.get("claims") or []
                    answered = {qq.get("correctClaim") for qq in (q.get("quotes") or []) if isinstance(qq, dict)}
                    orphans = [ci for ci in range(len(claims)) if ci not in answered]
                    if orphans:
                        found["EM_ORPHAN"].append(dict(tag, orphans=orphans))
                if t == "highlight_evidence":
                    text = (passages.get(q.get("passage_id")) or {}).get("text") or q.get("passage") or ""
                    if not re.sub(r"<[^>]+>", "", text).strip():
                        found["HL_EMPTY"].append(tag)
                    elif re.search(r"\b(first|second|third|fourth|final|last|opening|closing)\s+paragraph\b", stem, re.I):
                        # the highlighter keeps paragraph breaks since 22 Sep 2026; only a
                        # passage stored with none leaves the question unanswerable
                        if not re.search(r"\n\s*\n|<p\b|<br", text):
                            found["HL_PARA"].append(tag)
                if t == "spot_error":
                    s = rendered_tokens(q)
                    if re.search(r"\s[.,;:!?]|\s{2,}", s):
                        found["SE_SPACING"].append(dict(tag, rendered=s[:110]))
    return found


def main():
    subject = sys.argv[sys.argv.index("--subject") + 1] if "--subject" in sys.argv else "english-language-2-edexcel"
    only = sys.argv[sys.argv.index("--class") + 1] if "--class" in sys.argv else None
    show = "--show" in sys.argv
    sub = get("subjects?select=id&slug=eq.%s" % subject)
    if not sub:
        print("no subject", subject); return
    rows = get("lessons?select=id,lesson_number,status,practice_data,units!inner(slug,subject_id)"
               "&units.subject_id=eq.%s&limit=500" % sub[0]["id"])
    found = scan(rows)
    print("%s — %d lessons\n" % (subject, len(rows)))
    for cls in ["TL_MISSING", "REF_OTHER", "REF_ABSENT", "COMPARE", "EM_ORPHAN", "HL_EMPTY", "HL_PARA", "SE_SPACING", "STEM_PLACEHOLDER", "TL_NAMED"]:
        if only and cls != only:
            continue
        items = found.get(cls, [])
        print("%-11s %4d" % (cls, len(items)))
        if show or only:
            for it in items[:60]:
                extra = {k: v for k, v in it.items() if k not in ("where", "tier", "i", "type", "stem", "lesson_id")}
                print("    %-22s %-6s %-2d %-18s %s  %s" % (it["where"], it["tier"], it["i"], it["type"], it["stem"][:70], extra))
    return found


if __name__ == "__main__":
    main()
