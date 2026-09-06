"""
Corpus-wide mechanical label sweeps over every LIVE lesson.

Two sweeps, both flagged by every checker in the retro fact-check programme
and deliberately left for one consistent pass:

SWEEP 1 - band-ladder names, in practice_questions[*].marks ONLY.
    The generic pipeline invented a ladder "Mastering / Secure / Developing /
    Emerging". House vocabulary is Top band / Upper-mid band / Mid band /
    Lower-mid band / Low band. Rungs are counted PER MARKS STRING (invented
    names plus any house names already there) and mapped by rank onto the
    ladder for that rung count:
        4 rungs -> Top / Upper-mid / Lower-mid / Low
        3 rungs -> Top / Mid / Low
        2 rungs -> Top / Low
        1 rung  -> Mastering|Secure -> Top, Developing -> Mid, Emerging -> Low
    Only the word is replaced; bracketed mark ranges, spacing and the colon
    stay byte-for-byte. Matching is case-sensitive, standalone-word, optional
    " band", optional " (...)", then a colon - so prose uses ("a secure grasp")
    are never touched.
    Also: a trailing "[N marks]" tag that EXCEEDS the question type's tariff is
    recorded, and fixed down to the type tariff when the type carries a single
    integer AND the mark-scheme body does not itself corroborate the larger
    figure (fixing those would contradict the scheme text).

SWEEP 2 - examiner-voice claims, in exam_tip_html and practice_questions[*].marks
    ONLY. content_html and conclusion_html are narrated audio fields and are
    NOT touched here: their hits are counted per subject into
    labels/_narrated_worklist.json for a later narrated pass.
    Rewrites are deterministic phrase-family swaps that keep the rest of the
    sentence. Anything that does not match a family is recorded unchanged in
    labels/_worklist.json. No new claim is ever invented.

exam_tip_html IS narrated (4,118 of 4,275 live tips carry data-narration-id),
so every subject whose exam tips change is re-narrated through
scripts/_retrofc/_renarrate_from_backup.py unless --no-narrate is passed.

SAFETY
  * the content validator runs on the before row and the candidate row; a row
    that gains a NEW violation kind is skipped and logged
  * if more than 5% of a subject's candidate rows are rejected, the whole
    subject is skipped and logged
  * a per-subject backup is written BEFORE any patch
  * rows are patched one at a time via PostgREST
  * knowledge_checks, flashcard_questions, glossary_terms, question text and
    mark numbers are never written

Usage:
    python scripts/_sweeps/sweep_labels.py --dry-run --all
    python scripts/_sweeps/sweep_labels.py --subject business-aqa
    python scripts/_sweeps/sweep_labels.py --all
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from html import unescape as html_unescape

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
OUT = os.path.join(HERE, "labels")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, SCRIPTS)
from _validate_content_json import validate_file  # noqa: E402
try:
    from lib.narration import extract_narration_chunks  # noqa: E402
except Exception:  # narration lib optional for --dry-run on a bare checkout
    extract_narration_chunks = None

U = os.environ["SUPABASE_URL"]
K = os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": K, "Authorization": "Bearer " + K}
COLS = ("id,unit_id,lesson_number,title,description,content_html,exam_tip_html,"
        "conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms")
VALIDATED = ["description", "content_html", "exam_tip_html", "conclusion_html", "practice_questions",
             "knowledge_checks", "flashcard_questions", "glossary_terms", "title"]


# --------------------------------------------------------------------- http
def api(path, method="GET", body=None, tries=5):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    hdr = dict(HDR)
    if data:
        hdr["Content-Type"] = "application/json"
        hdr["Prefer"] = "return=minimal"
    for a in range(tries):
        try:
            req = urllib.request.Request(f"{U}/rest/v1/{path}", data=data, headers=hdr, method=method)
            raw = urllib.request.urlopen(req, timeout=180).read()
            return json.loads(raw) if raw else None
        except Exception as e:  # noqa: BLE001 - retry on any transport error
            if a == tries - 1:
                detail = ""
                if isinstance(e, urllib.error.HTTPError):
                    try:
                        detail = e.read().decode("utf-8", "replace")[:400]
                    except Exception:
                        pass
                raise RuntimeError(f"{method} {path[:120]} failed: {e} {detail}")
            time.sleep(2 * (a + 1))


# ------------------------------------------------------------------ sweep 1
NAMES = "Mastering|Secure|Developing|Emerging"
# A ladder rung label: one invented name, or a compound ("Developing or
# Emerging:"), optionally " band", optionally " (5-6)", then a colon.
INV_RE = re.compile(rf"(?<![A-Za-z0-9\-])((?:{NAMES})(?:\s*(?:/|or)\s*(?:{NAMES}))*)"
                    r"(\s+band)?(\s*\([^)\n]{0,60}\))?(\s*):")
NAME_RE = re.compile(rf"\b({NAMES})\b")
# A prose cross-reference to a rung ("as Secure", "the defining feature of
# Mastering", "a Mastering-level answer") - recorded, never rewritten, because
# the brief is word+colon only. Plain prose ("a developing country") is excluded.
RESIDUE_RE = re.compile(rf"\b(?:as|than|of|to|reach(?:es|ing)?|at)\s+({NAMES})\b|\b({NAMES})[- ]level\b")
HOUSE_RE = re.compile(r"(?<![A-Za-z0-9\-])(Top band|Upper-mid band|Mid band|Lower-mid band|Low band)"
                      r"(\s*\([^)\n]{0,60}\))?(\s*):")
RANK = {"Mastering": 0.0, "Secure": 1.0, "Developing": 2.0, "Emerging": 3.0,
        "Top band": 0.0, "Upper-mid band": 1.0, "Mid band": 1.5, "Lower-mid band": 2.0, "Low band": 3.0}
LADDER = {2: ["Top band", "Low band"],
          3: ["Top band", "Mid band", "Low band"],
          4: ["Top band", "Upper-mid band", "Lower-mid band", "Low band"],
          5: ["Top band", "Upper-mid band", "Mid band", "Lower-mid band", "Low band"]}
SOLO = {"Mastering": "Top band", "Secure": "Top band", "Developing": "Mid band", "Emerging": "Low band"}


def band_plan(marks):
    """Return (mapping invented-name -> house-name, conflict-reason or None)."""
    found = set()
    for m in INV_RE.finditer(marks):
        found.update(NAME_RE.findall(m.group(1)))
    inv = sorted(found, key=lambda n: RANK[n])
    if not inv:
        return {}, None
    house = sorted({m.group(1) for m in HOUSE_RE.finditer(marks)}, key=lambda n: RANK[n])
    rungs = sorted(set(inv) | set(house), key=lambda n: RANK[n])
    n = len(rungs)
    if n == 1:
        return {inv[0]: SOLO[inv[0]]}, None
    if n not in LADDER:
        return {}, f"unmapped rung count {n}: {rungs}"
    target = dict(zip(rungs, LADDER[n]))
    for h in house:  # an existing house label must keep its own name
        if target[h] != h:
            return {}, f"house label '{h}' would move to '{target[h]}' ({n} rungs: {rungs})"
    mapping = {i: target[i] for i in inv}
    if len(set(mapping.values())) != len(mapping):
        return {}, f"non-injective mapping {mapping}"
    return mapping, None


def apply_bands(marks, mapping):
    def sub(m):
        label, _band, paren, ws = m.group(1), m.group(2), m.group(3), m.group(4)
        if not all(n in mapping for n in NAME_RE.findall(label)):
            return m.group(0)
        return NAME_RE.sub(lambda x: mapping[x.group(1)], label) + (paren or "") + (ws or "") + ":"
    return INV_RE.sub(sub, marks)


TAG_END = re.compile(r"\[(\d+)\s*(marks?)\]\s*$")
TAG_END_LOOSE = re.compile(r"\[(\d+)\s*marks?\b[^\]]*\]\s*$")
TYPE_INT = re.compile(r"^\s*(\d+)\s*marks?\s*[—–-]")


def tariff_check(q):
    """(record, fixed_marks_or_None). record is a dict when tag > type tariff."""
    marks, qtype = q.get("marks"), str(q.get("type") or "")
    if not isinstance(marks, str):
        return None, None
    body = marks.rstrip()
    mt = TAG_END_LOOSE.search(body)
    tt = TYPE_INT.match(qtype)
    if not mt or not tt:
        return None, None
    tariff, tag = int(tt.group(1)), int(mt.group(1))
    if tag <= tariff:
        return None, None
    rec = {"type": qtype, "tag": mt.group(0).strip(), "tariff": tariff, "tag_marks": tag}
    plain = TAG_END.search(body)
    stem = body[:mt.start()]
    corroborated = re.search(rf"\b(?:up to|maximum of|total of)?\s*{tag}\s*marks?\b", stem) is not None
    if plain and not corroborated:
        new_tag = f"[{tariff} mark{'' if tariff == 1 else 's'}]"
        rec["action"] = "fixed"
        return rec, body[:plain.start()] + new_tag
    rec["action"] = "recorded (mark scheme body corroborates the larger figure)" if corroborated \
        else "recorded (tag carries extra text)"
    return rec, None


# ------------------------------------------------------------------ sweep 2
# Trigger table. Each entry: (compiled regex, replacement, kind).
# Singular/plural twins of the briefed families are included; the REPLACEMENT
# text is never varied, so no new claim can enter the corpus.
def _f(pattern):
    return re.compile(pattern, re.IGNORECASE)


REL = r"(?:answers|responses|candidates|students|writers?|pupils)\s+(?:that|who|which|where)"
FAMILIES = [
    # -- "Strong answers" -------------------------------------------------
    (_f(rf"(?:the\s+)?examiners?\s+rewards?\s+{REL}"), "Strong answers", "reward"),
    (_f(r"(?:the\s+)?examiners?\s+rewards?"), "Strong answers show", "reward-bare"),
    # -- "A good answer shows" -------------------------------------------
    (_f(r"(?:the\s+)?examiners?\s+(?:is|are)\s+looking\s+for\s+you\s+to"), "A good answer shows that you", "wants"),
    (_f(r"(?:the\s+)?examiners?\s+(?:is|are)\s+looking\s+for"), "A good answer shows", "looking"),
    (_f(r"(?:the\s+)?examiners?\s+wants?\s+to\s+see\s+that\s+you"), "A good answer shows that you", "wants"),
    (_f(r"(?:the\s+)?examiners?\s+wants?\s+to\s+see\s+you"), "A good answer shows that you", "wants"),
    (_f(r"(?:the\s+)?examiners?\s+wants?\s+to\s+see\s+that"), "A good answer shows that", "wants"),
    (_f(r"(?:the\s+)?examiners?\s+wants?\s+to\s+see"), "A good answer shows", "looking"),
    (_f(r"(?:the\s+)?examiners?\s+wants?\s+you\s+to"), "A good answer shows that you", "wants"),
    # -- "Credit goes to" -------------------------------------------------
    (_f(r"the\s+mark\s+scheme\s+rewards?"), "Credit goes to", "mark-scheme"),
    (_f(r"the\s+mark\s+scheme\s+awards?\s+marks?\s+for"), "Credit goes to", "mark-scheme"),
    (_f(r"the\s+mark\s+scheme\s+asks?\s+for"), "Credit goes to", "mark-scheme"),
    # -- "In practice," ---------------------------------------------------
    (_f(r"examiners?\s+consistently\s+reports?\s+that"), "In practice,", "reports"),
    (_f(r"examiners?\s+reports?\s+(?:show|shows|highlight|highlights|note|notes)\s+that"), "In practice,", "reports"),
    (_f(r"the\s+20\d\d\s+examiners?'?\s+reports?\s+(?:highlighted|identified|noted)\s+that"), "In practice,", "reports"),
    # -- misc -------------------------------------------------------------
    (_f(r"will\s+earn\s+the\s+mark"), "is the point that counts", "earn"),
    (_f(r"earns\s+the\s+mark"), "is the point that counts", "earn"),
    (_f(r"is\s+one\s+of\s+the\s+most\s+(?:commonly\s+)?penalised\s+(?:errors|mistakes)"), "is a common slip", "penalised"),
]
DELETE_CLAUSE = [_f(r"\s*,?\s*as\s+examiners\s+report\s*,?")]

# Whole sentences that assert examiner behaviour and teach nothing. Reviewed
# against the live corpus before being hard-coded; every pattern must match a
# COMPLETE sentence.
DELETE_SENTENCES = [
    _f(r"examiners?\s+(?:penalise|penalize)s?\s+(?:this|that|it)\s+(?:every|each)\s+year\s*\."),
    _f(r"th(?:is|at)\s+(?:topic\s+|area\s+)?is\s+examined\s+(?:almost\s+)?every\s+year\s*\."),
    _f(r"(?:pearson|aqa|ocr|eduqas|wjec|the\s+board|the\s+exam\s+board)\s+has\s+"
       r"(?:signalled|signaled|flagged)\s+this\s+(?:topic|area|content)(?:\s+as\s+a\s+priority)?\s*\."),
    _f(r"these\s+(?:specific\s+)?details\s+matter\s+to\s+(?:the\s+)?examiners?\s*\."),
    _f(r"th(?:is|ese)[\w\s,'’“”-]{0,40}\s+impress(?:es)?\s+(?:the\s+)?examiners?\s*\."),
    _f(r"th(?:is|ese)[\w\s,'’“”-]{0,40}\s+signals?\s+sophistication\s+to\s+(?:the\s+)?examiners?\s*\."),
]

# Anything mentioning examiner authority. Used to find hits, matched or not.
PROBE = _f(r"examiner|mark\s*scheme|penalis|penaliz|examined\s+(?:almost\s+)?every\s+year|has\s+signalled")

# Guards. A rewrite is only mechanical when the rest of the sentence still
# parses with the new subject; where it would not, the hit is left alone and
# recorded in the worklist for a human pass.
BARE_BLOCK = _f(r"^\s*[A-Za-z’']+ing\b"                                     # "reward using ..." -> "show using"
                r"|\b(?:and|but|or)\s+(?:penalis|penaliz|expect|want|look|reward|credit|award|mark)"
                r"|\b(?:far\s+)?more\s+(?:highly|heavily)\b|\bheavily\b|\bhighly\b|\bfar\s+more\b"
                r"|\bto\s+award\b")
BARE_BLOCK_NEAR = _f(r"\banswers?\b")          # "reward applied answers" -> "answers show ... answers"
REL_BLOCK = _f(r",\s+and\s+(?:that|who)\b")    # "answers that X, and that Y" loses its subject
GOOD_BLOCK = _f(r"\banswers?\b|\bto\s+award\b")
YOU_BLOCK = {"be", "show", "shows", "showing"}
SENT_SPLIT = re.compile(r"[^.!?]*[.!?]|[^.!?]+$")
CLAUSE_START = set(">.!?,;:—–-\"'“‘()\n\t ")


def plain(html):
    t = html_unescape(re.sub(r"<[^>]+>", " ", html or "")).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()


def _cap(rep, at_sentence_start):
    if at_sentence_start:
        return rep[0].upper() + rep[1:]
    return rep[0].lower() + rep[1:]


def _sentence_start_s(prefix):
    """True when a match opening right after `prefix` also opens a sentence."""
    tail = re.sub(r"(<[^>]+>|\s|&nbsp;)+$", "", prefix)
    return (not tail) or tail[-1] in ".!?"


def _preceded_ok_s(prefix):
    """The phrase must open a clause; a mid-clause use ('the analysis examiners
    reward') is a relative clause and rewriting it would break the sentence."""
    head = re.sub(r"(<[^>]+>)+$", "", prefix)
    if not head:
        return True
    stripped = head.rstrip()
    if not stripped:
        return True
    if len(stripped) < len(head):        # whitespace sits before the match
        return stripped[-1] in CLAUSE_START
    return stripped[-1] in ">.!?,;:—–(\n"


def _sent_of(text, idx):
    return plain(text[max(0, idx - 200):idx + 260])[:320]


def sweep2(text, unmatched_out, where):
    """Rewrite examiner-voice families in one string. Returns (new_text, n_rewrites)."""
    if not isinstance(text, str) or not text:
        return text, 0
    original, n = text, 0

    # 1. whole-sentence deletions (pure examiner-behaviour assertions)
    for pat in DELETE_SENTENCES:
        for _ in range(10):
            m = pat.search(text)
            if not m or not _sentence_start_s(text[:m.start()]):
                break
            text = re.sub(r"  +", " ", text[:m.start()] + text[m.end():])
            n += 1
    # 2. clause deletion ("as examiners report")
    for pat in DELETE_CLAUSE:
        for _ in range(10):
            m = pat.search(text)
            if not m:
                break
            text = re.sub(r"\s+([.,;])", r"\1", re.sub(r"  +", " ", text[:m.start()] + text[m.end():]))
            n += 1
    # 3. family rewrites, left to right
    out, pos = [], 0
    while True:
        best = None
        for pat, rep, kind in FAMILIES:
            m = pat.search(text, pos)
            if m and (best is None or m.start() < best[0].start() or
                      (m.start() == best[0].start() and m.end() > best[0].end())):
                best = (m, rep, kind)
        if not best:
            break
        m, rep, kind = best
        built = "".join(out) + text[pos:m.start()]
        rest = text[m.end():]
        window = plain(rest[:240])
        new = _cap(rep, _sentence_start_s(built))
        if new.lower().endswith("shows") and re.match(r"\s+you\b", rest):
            new += " that"
        reason = None
        if not _preceded_ok_s(built):
            reason = "mid-clause use"
        elif kind == "reward-bare" and (BARE_BLOCK.search(window[:90]) or BARE_BLOCK_NEAR.search(window[:40])):
            reason = "bare 'reward' object would not carry the new subject"
        elif kind == "reward" and REL_BLOCK.search(window.split(".")[0]):
            reason = "coordinated relative clause loses its subject"
        elif kind == "looking" and GOOD_BLOCK.search(window[:60]):
            reason = "'a good answer shows' would echo or orphan the clause"
        if not reason and new.lower().rstrip(".,;: ").endswith("you"):
            nxt = re.match(r"\s*(?:you\s+)?([A-Za-z’']+)", window)
            w = nxt.group(1).lower() if nxt else ""
            if w in YOU_BLOCK or w.endswith("ing"):
                reason = f"'that you {w}' does not parse"
        if reason:
            unmatched_out.append({**where, "reason": reason, "sentence": _sent_of(text, m.start())})
            out.append(text[pos:m.end()])
            pos = m.end()
            continue
        out.append(text[pos:m.start()])
        out.append(new)
        pos = m.end()
        n += 1
    out.append(text[pos:])
    text = "".join(out)

    if n and not _structurally_safe(original, text):
        unmatched_out.append({**where, "reason": "structure guard - field left unchanged",
                              "sentence": plain(original)[:300]})
        return original, 0
    return text, n


def _structurally_safe(before, after):
    """No tag may be damaged and no narration chunk may be emptied."""
    if re.findall(r"<[^>]+>", before) != re.findall(r"<[^>]+>", after):
        return False
    if "data-narration-id" in before and extract_narration_chunks is not None:
        try:
            a = dict(extract_narration_chunks(before))
            b = dict(extract_narration_chunks(after))
        except Exception:
            return True
        if set(a) != set(b):
            return False
        if any(not (b[i] or "").strip() for i in b):
            return False
    return True


# --------------------------------------------------------------- validation
STR_FIELDS = ("description", "content_html", "exam_tip_html", "conclusion_html", "title")


def violations(row):
    """Validator violations for one lesson row. Practice-format lessons carry
    NULL html fields (786 live rows); they are normalised to "" so the
    validator runs, identically on the before and the after row, which keeps
    the differential check honest."""
    payload = {}
    for k in VALIDATED:
        v = row.get(k)
        if v is None:
            v = "" if k in STR_FIELDS else []
        payload[k] = v
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    try:
        viol = set(validate_file(p))
    except Exception as e:  # noqa: BLE001 - a crash must not silently pass a row
        return [f"VALIDATOR ERROR: {type(e).__name__}"]
    finally:
        os.remove(p)
    for f_ in ("content_html", "exam_tip_html", "conclusion_html"):
        h = row.get(f_) or ""
        o, c = len(re.findall(r"<div", h)), h.count("</div>")
        if o != c:
            viol.add(f"div-imbalance {f_}: {o} open vs {c} close")
    return sorted(viol)


def kind(v):
    return re.sub(r"\d+", "#", v.split(":")[0])


# --------------------------------------------------------------- processing
def process_lesson(row, narrated_hits, worklist, subject):
    """Return (patch dict, before dict, stats dict). patch is {} when nothing changes."""
    st = {"band_renames": 0, "band_questions": 0, "tag_fixes": 0, "ev_rewrites": 0}
    where = {"subject": subject, "lesson_id": row["id"], "lesson_number": row.get("lesson_number")}
    patch, before = {}, {}

    # ---- narrated fields: count only
    for f_ in ("content_html", "conclusion_html"):
        txt = row.get(f_)
        if not isinstance(txt, str) or not txt:
            continue
        for s in SENT_SPLIT.findall(plain(txt)):
            s = s.strip()
            if s and PROBE.search(s):
                fam = next((k for p, _r, k in FAMILIES if p.search(s)), None)
                narrated_hits.append({**where, "field": f_, "family": fam, "sentence": s[:300]})

    # ---- practice questions
    pqs = row.get("practice_questions")
    if isinstance(pqs, list):
        new_pqs, changed = [], False
        for i, q in enumerate(pqs):
            if not isinstance(q, dict):
                new_pqs.append(q)
                continue
            q2 = dict(q)
            marks = q2.get("marks")
            if isinstance(marks, str):
                # sweep 1: band ladder
                mapping, conflict = band_plan(marks)
                if conflict:
                    worklist["ladder_conflicts"].append({**where, "q": i, "reason": conflict, "marks": marks[:300]})
                elif mapping:
                    nm = apply_bands(marks, mapping)
                    if nm != marks:
                        st["band_renames"] += sum(len(NAME_RE.findall(m.group(1)))
                                                  for m in INV_RE.finditer(marks))
                        st["band_questions"] += 1
                        marks = nm
                        left = sorted({a or b for a, b in RESIDUE_RE.findall(marks)})
                        if left:
                            # A prose cross-reference ("as Secure, plus ...") to a rung
                            # that has just been renamed. The brief is word+colon only,
                            # so it is recorded rather than rewritten.
                            worklist["ladder_residue"].append(
                                {**where, "q": i, "left": left, "marks": marks[:300]})
                # sweep 1b: tariff tag
                q2["marks"] = marks
                rec, fixed = tariff_check(q2)
                if rec:
                    worklist["tariff_tags"].append({**where, "q": i, **rec})
                if fixed is not None:
                    marks = fixed
                    st["tag_fixes"] += 1
                # sweep 2 on the mark scheme
                marks, nrw = sweep2(marks, worklist["examiner_unmatched"],
                                    {**where, "field": f"practice_questions[{i}].marks"})
                st["ev_rewrites"] += nrw
                # unmatched examiner hits in this marks string
                _record_unmatched(marks, worklist, {**where, "field": f"practice_questions[{i}].marks"})
                if marks != q.get("marks"):
                    q2["marks"] = marks
                    changed = True
                else:
                    q2["marks"] = q.get("marks")
            new_pqs.append(q2)
        if changed:
            patch["practice_questions"] = new_pqs
            before["practice_questions"] = pqs

    # ---- exam tip
    tip = row.get("exam_tip_html")
    if isinstance(tip, str) and tip:
        new_tip, nrw = sweep2(tip, worklist["examiner_unmatched"], {**where, "field": "exam_tip_html"})
        st["ev_rewrites"] += nrw
        _record_unmatched(new_tip, worklist, {**where, "field": "exam_tip_html"})
        if new_tip != tip:
            patch["exam_tip_html"] = new_tip
            before["exam_tip_html"] = tip

    return patch, before, st


def _record_unmatched(text, worklist, where):
    if not isinstance(text, str):
        return
    for s in SENT_SPLIT.findall(plain(text)):
        s = s.strip()
        if not s or not PROBE.search(s):
            continue
        if any(p.search(s) for p, _r, _k in FAMILIES):
            continue
        worklist["examiner_unmatched"].append({**where, "reason": "no family match", "sentence": s[:300]})


# ------------------------------------------------------------------- runner
def load_index():
    subs = api("subjects?select=id,slug,school_id&order=slug")
    units, off = [], 0
    while True:
        b = api(f"units?select=id,subject_id,slug&order=id&limit=1000&offset={off}")
        units += b
        if len(b) < 1000:
            break
        off += 1000
    by_subject = {}
    for u in units:
        by_subject.setdefault(u["subject_id"], []).append(u["id"])
    return subs, by_subject


def fetch_lessons(unit_ids):
    rows = []
    for i in range(0, len(unit_ids), 25):
        chunk = unit_ids[i:i + 25]
        q = urllib.parse.quote(",".join(chunk), safe="")
        rows += api(f"lessons?status=eq.live&unit_id=in.({q})&select={COLS}&order=lesson_number")
    return rows


def git(args):
    return subprocess.run(["git", "-C", ROOT] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def subject_key(s, dupes):
    """Three slugs (computer-science, design-technology, separate-sciences) exist
    TWICE: a Unity row and a free-tier row. Keying resume state or backup files
    on the slug alone silently skips the second row, so disambiguate."""
    if s["slug"] not in dupes:
        return s["slug"]
    return f"{s['slug']}__{'school' if s.get('school_id') else 'free'}"


def run_subject(slug, sid, unit_ids, dry, narrate, totals, worklist, narrated_hits, key=None):
    key = key or slug
    rows = fetch_lessons(unit_ids)
    st = {"subject": slug, "key": key, "lessons_scanned": len(rows), "band_renames": 0, "band_questions": 0,
          "tag_fixes": 0, "ev_rewrites": 0, "rows_changed": 0, "rows_skipped_validator": 0,
          "skipped": False, "reason": None, "renarrated_clips": None}
    plan = []
    for r in rows:
        patch, before, s = process_lesson(r, narrated_hits, worklist, slug)
        for k in ("band_renames", "band_questions", "tag_fixes", "ev_rewrites"):
            st[k] += s[k]
        if not patch:
            continue
        cand = dict(r)
        cand.update(patch)
        pre = violations(r)
        post = violations(cand)
        pre_k = {kind(v) for v in pre}
        new = [v for v in post if kind(v) not in pre_k]
        if any(v.startswith("VALIDATOR ERROR") for v in pre + post):
            new = ["validator could not run on this row"]
        if new:
            st["rows_skipped_validator"] += 1
            worklist["validator_skips"].append({"subject": slug, "lesson_id": r["id"],
                                                "lesson_number": r.get("lesson_number"), "new": new[:5]})
            continue
        plan.append((r, patch, before))
    st["rows_changed"] = len(plan)

    n_cand = len(plan) + st["rows_skipped_validator"]
    if n_cand and st["rows_skipped_validator"] / n_cand > 0.05:
        st["skipped"] = True
        st["reason"] = (f"validator rejected {st['rows_skipped_validator']}/{n_cand} candidate rows "
                        f"({st['rows_skipped_validator'] / n_cand:.0%} > 5%)")
        plan = []
        st["rows_changed"] = 0

    if dry or not plan:
        totals.append(st)
        return st, []

    # backup BEFORE patching
    backup = {"subject": slug, "subject_id": sid,
              "lessons": [{"id": r["id"], "lesson_number": r.get("lesson_number"), "before": b}
                          for r, _p, b in plan]}
    with open(os.path.join(OUT, f"_backup_{key}.json"), "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=1)

    for r, patch, _b in plan:
        api(f"lessons?id=eq.{r['id']}", method="PATCH", body=patch)

    # re-narrate lessons whose exam tip (a narrated field) changed
    # Only lessons that actually carry audio: a lesson with an empty
    # narration_manifest has no clip to refresh, and the re-narrate script
    # aborts the whole batch when it cannot derive an R2 key for one.
    tip_rows = []
    for r, _p, b in plan:
        if "exam_tip_html" not in b:
            continue
        got = api(f"lessons?id=eq.{r['id']}&select=narration_manifest")
        if got and (got[0].get("narration_manifest") or []):
            tip_rows.append((r, b))
        else:
            st.setdefault("tips_without_audio", []).append(r["id"])
    if tip_rows and narrate:
        nb = os.path.join(OUT, f"{key}_backup.json")
        with open(nb, "w", encoding="utf-8") as f:
            json.dump({"subject": slug, "unit": "label-sweep",
                       "lessons": [{"id": r["id"], "lesson_number": r["lesson_number"],
                                    "before": {"exam_tip_html": b["exam_tip_html"]}} for r, b in tip_rows]},
                      f, ensure_ascii=False, indent=1)
        p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "_retrofc", "_renarrate_from_backup.py"),
                            "--backup", nb], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        m = re.search(r"Regenerated (\d+) clips", p.stdout or "")
        st["renarrated_clips"] = int(m.group(1)) if m else f"FAILED rc={p.returncode}"
        if p.returncode != 0:
            st["renarrate_stderr"] = (p.stderr or "")[-600:]
    totals.append(st)
    return st, plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-narrate", action="store_true")
    ap.add_argument("--no-commit", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if not args.subject and not args.all:
        ap.error("pass --subject <slug> or --all")

    subs, units_by_subject = load_index()
    import collections as _c
    dupes = {k for k, v in _c.Counter(x["slug"] for x in subs).items() if v > 1}
    if args.subject:
        subs = [s for s in subs if s["slug"] == args.subject]
        if not subs:
            ap.error(f"no subject with slug {args.subject}")

    totals, narrated_hits = [], []
    worklist = {"examiner_unmatched": [], "tariff_tags": [], "ladder_conflicts": [],
                "ladder_residue": [], "validator_skips": []}
    done_path = os.path.join(OUT, "_done.json")
    done = set()
    if args.all and not args.dry_run and os.path.exists(done_path):
        done = set(json.load(open(done_path, encoding="utf-8")))

    for s in subs:
        skey = subject_key(s, dupes)
        if skey in done:
            print(f"-- {skey}: already done, skipping")
            continue
        uids = units_by_subject.get(s["id"], [])
        if not uids:
            continue
        st, plan = run_subject(s["slug"], s["id"], uids, args.dry_run,
                               not args.no_narrate, totals, worklist, narrated_hits, key=skey)
        print(f"{'[dry] ' if args.dry_run else ''}{skey}: {st['lessons_scanned']} live, "
              f"{st['band_renames']} band renames ({st['band_questions']} q), {st['tag_fixes']} tag fixes, "
              f"{st['ev_rewrites']} examiner rewrites, {st['rows_changed']} rows patched"
              + (f", SKIPPED: {st['reason']}" if st["skipped"] else "")
              + (f", validator-skipped {st['rows_skipped_validator']}" if st["rows_skipped_validator"] else "")
              + (f", renarrated {st['renarrated_clips']}" if st.get("renarrated_clips") is not None else ""),
              flush=True)
        if not args.dry_run and plan and not args.no_commit:
            git(["add", "scripts/_sweeps"])
            msg = (f"Label sweep: {skey} - {st['band_renames']} band renames, "
                   f"{st['tag_fixes']} tag fixes, {st['ev_rewrites']} examiner-voice rewrites\n\n"
                   "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>")
            git(["commit", "-q", "-m", msg])
        if not args.dry_run:
            done.add(skey)
            with open(done_path, "w", encoding="utf-8") as f:
                json.dump(sorted(done), f, indent=1)

    agg = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "mode": "dry-run" if args.dry_run else "live",
           "subjects": len(totals),
           "lessons_scanned": sum(t["lessons_scanned"] for t in totals),
           "sweep1_band_renames": sum(t["band_renames"] for t in totals),
           "sweep1_band_questions": sum(t["band_questions"] for t in totals),
           "sweep1_tag_fixes": sum(t["tag_fixes"] for t in totals),
           "sweep2_rewrites": sum(t["ev_rewrites"] for t in totals),
           "rows_changed": sum(t["rows_changed"] for t in totals),
           "rows_skipped_validator": sum(t["rows_skipped_validator"] for t in totals),
           "subjects_skipped": [t["subject"] for t in totals if t["skipped"]],
           "worklist_examiner_unmatched": len(worklist["examiner_unmatched"]),
           "worklist_tariff_tags": len(worklist["tariff_tags"]),
           "worklist_ladder_conflicts": len(worklist["ladder_conflicts"]),
           "worklist_ladder_residue": len(worklist["ladder_residue"]),
           "narrated_worklist_hits": len(narrated_hits),
           "per_subject": totals}
    out = args.out or os.path.join(OUT, "_dryrun.json" if args.dry_run else "_summary.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(agg, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "_worklist.json" if not args.dry_run else "_worklist_dryrun.json"),
              "w", encoding="utf-8") as f:
        json.dump(worklist, f, ensure_ascii=False, indent=1)
    per_subject = {}
    for h in narrated_hits:
        per_subject[h["subject"]] = per_subject.get(h["subject"], 0) + 1
    with open(os.path.join(OUT, "_narrated_worklist.json" if not args.dry_run
                           else "_narrated_worklist_dryrun.json"), "w", encoding="utf-8") as f:
        json.dump({"generated": agg["generated"], "total_hits": len(narrated_hits),
                   "per_subject": dict(sorted(per_subject.items(), key=lambda kv: -kv[1])),
                   "hits": narrated_hits}, f, ensure_ascii=False, indent=1)
    print("\n== TOTALS ==")
    for k in ("lessons_scanned", "sweep1_band_renames", "sweep1_band_questions", "sweep1_tag_fixes",
              "sweep2_rewrites", "rows_changed", "rows_skipped_validator",
              "worklist_examiner_unmatched", "worklist_tariff_tags", "worklist_ladder_conflicts",
              "worklist_ladder_residue",
              "narrated_worklist_hits"):
        print(f"  {k}: {agg[k]}")
    print(f"  subjects_skipped: {agg['subjects_skipped']}")
    print(f"  written: {out}")


if __name__ == "__main__":
    main()
