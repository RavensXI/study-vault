"""Score a bake-off checker run against the Opus reference for the same unit.

Usage: python scripts/_retrofc/_bakeoff_compare.py <bakeoff-unit-dir> [more dirs...]

For each dir: reads _report.json / _edits.json (the candidate) and
_opus_report.json / _opus_edits.json (reference), plus _raw.json (the pre-fix
lessons). Reports severity counts, overlap with the reference findings
(matched by lesson + field + token overlap of claim text), findings unique to
each side, edit validity (every text `find` unique in its field, every JSON
`expect` matching), banned strings in replacements, and run time from
_codex_done.json. Overlap is a screen, not a verdict: unique findings need a
human/Fable read to tell "missed by Opus" from "invented".
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BANNED = re.compile(r"\bAO[1-4]\.[0-9]?|\bLevel\s+[1-9]\b|\bPaper\s+[0-9][A-Z]?\s+Section\b|\bComponent\s+[0-9]|\b(AQA|OCR|Edexcel|Eduqas|WJEC)\s+[0-9A-Z]{3,6}\b|Nothing worthy of credit|Award \d+ marks? for", re.I)


def toks(s):
    return set(re.findall(r"[a-z0-9']{3,}", (s or "").lower()))


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def get_path(obj, path):
    cur = obj
    for m in re.finditer(r"\[(\d+)\]|\.?([A-Za-z_][A-Za-z0-9_]*)", path):
        cur = cur[int(m.group(1))] if m.group(1) is not None else cur[m.group(2)]
    return cur


def validate_edits(edits, raw):
    lessons = {l["lesson_number"]: l for l in raw["lessons"]}
    bad, banned = [], []
    for e in edits:
        L = lessons.get(e.get("lesson"))
        if not L:
            bad.append(f"L{e.get('lesson')} missing")
            continue
        if "find" in e:
            v = L.get(e["field"]) or ""
            c = v.count(e["find"])
            if c != 1:
                bad.append(f"L{e['lesson']} {e['field']} find x{c}: {e['find'][:60]!r}")
            if BANNED.search(e.get("replace", "")):
                banned.append(f"L{e['lesson']} {e['field']}: {e['replace'][:80]!r}")
        else:
            v = L.get(e["field"])
            v = json.loads(v) if isinstance(v, str) else v
            try:
                cur = get_path(v, e["path"])
            except Exception:  # noqa: BLE001
                bad.append(f"L{e['lesson']} {e['field']} bad path {e.get('path')}")
                continue
            if "expect" in e and cur != e["expect"]:
                bad.append(f"L{e['lesson']} {e['field']}{e['path']} expect mismatch")
            if BANNED.search(json.dumps(e.get("value", ""), ensure_ascii=False)):
                banned.append(f"L{e['lesson']} {e['field']}{e['path']}: {str(e.get('value'))[:80]!r}")
    return bad, banned


def match(cands, refs):
    """Greedy match candidate findings to reference findings by lesson+field+token overlap."""
    used = set()
    pairs = []
    for i, c in enumerate(cands):
        best, bj = 0.0, None
        ct = toks(c.get("claim", "")) | toks(c.get("truth", ""))
        for j, r in enumerate(refs):
            if j in used or str(r.get("lesson")) != str(c.get("lesson")):
                continue
            rt = toks(r.get("claim", "")) | toks(r.get("truth", ""))
            if not ct or not rt:
                continue
            s = len(ct & rt) / min(len(ct), len(rt))
            if r.get("field") == c.get("field"):
                s += 0.1
            if s > best:
                best, bj = s, j
        if bj is not None and best >= 0.35:
            used.add(bj)
            pairs.append((i, bj, round(best, 2)))
    return pairs, used


def main():
    for d in sys.argv[1:]:
        cand = load(os.path.join(d, "_report.json"))
        ref = load(os.path.join(d, "_opus_report.json"))
        cedits = load(os.path.join(d, "_edits.json"), [])
        raw = load(os.path.join(d, "_raw.json"))
        done = load(os.path.join(d, "_codex_done.json"), {})
        print(f"\n=== {d}\nrun: {done.get('model')} / {done.get('effort')}  {done.get('minutes')} min  exit={done.get('exit_code')}")
        if not cand or not ref:
            print("  candidate or reference report missing")
            continue
        cf, rf = cand.get("findings", []), ref.get("findings", [])
        sev = lambda fs: {k: sum(1 for f in fs if (f.get("severity") or "").upper().startswith(k)) for k in ("HIGH", "MED", "LOW")}
        print(f"  findings: candidate {len(cf)} {sev(cf)} | opus {len(rf)} {sev(rf)}")
        print(f"  verdicts: candidate FIX {sum(1 for f in cf if f.get('verdict')=='FIX')} / ADJ {sum(1 for f in cf if f.get('verdict')=='ADJUDICATE')} / NOTE {sum(1 for f in cf if f.get('verdict')=='NOTE')}; edits {len(cedits)} (opus {len(load(os.path.join(d,'_opus_edits.json'),[]))})")
        pairs, used = match(cf, rf)
        ref_high = [j for j, r in enumerate(rf) if (r.get("severity") or "").upper() == "HIGH"]
        missed_high = [rf[j] for j in ref_high if j not in used]
        print(f"  overlap: {len(pairs)} of opus's {len(rf)} findings matched; opus HIGH matched {len(ref_high)-len(missed_high)}/{len(ref_high)}")
        for r in missed_high:
            print(f"    MISSED opus HIGH L{r.get('lesson')} [{r.get('field')}]: {r.get('claim','')[:110]}")
        uniq = [c for i, c in enumerate(cf) if i not in {p[0] for p in pairs}]
        print(f"  candidate-only findings: {len(uniq)} (need a cold read: missed-by-Opus vs invented)")
        for c in uniq[:12]:
            print(f"    {c.get('severity')} {c.get('verdict')} L{c.get('lesson')} [{c.get('field')}]: {c.get('claim','')[:110]} -> {c.get('truth','')[:90]}")
        if raw:
            bad, banned = validate_edits(cedits, raw)
            print(f"  edit validity: {len(cedits)-len(bad)}/{len(cedits)} apply cleanly; {len(bad)} bad; banned strings in {len(banned)} edits")
            for b in bad[:6]:
                print("    BAD", b)
            for b in banned[:6]:
                print("    BANNED", b)


if __name__ == "__main__":
    main()
