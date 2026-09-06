# -*- coding: utf-8 -*-
"""Post-rebuild verification. Re-reads every rebuilt lesson from live Supabase
and checks the whole contract, then diffs the preserved fields against the
backup taken before any write."""
import io, json, os, re, sys, html as _html
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import _Bal
from lib.supabase_client import get_client
from lib.narration import extract_narration_chunks

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(io.open(os.path.join(HERE, "_rows_index.json"), encoding="utf-8"))
sb = get_client()
bad = 0
print("%-46s %-6s %5s %5s %4s %4s %4s %-14s" % ("lesson", "pins", "cards", "nids", "man", "q/k/f", "desc", "status"))
for r in rows:
    if r["lesson"] == 2 and r["unit"] == "aos1-instrumental-music":
        continue  # the approved exemplar, not part of this rebuild
    l = sb.table("lessons").select("*").eq("id", r["id"]).single().execute().data
    old = json.load(io.open(os.path.join(HERE, "backups", r["file"]), encoding="utf-8"))
    c = l["content_html"] or ""
    errs = []

    b = _Bal(); b.feed(c)
    if b.errors or b.stack:
        errs.append("unbalanced tags %s %s" % (b.errors[:3], b.stack[:3]))

    nids = [int(x) for x in re.findall(r'data-narration-id="n(\d+)"', c)]
    if nids != list(range(1, len(nids) + 1)):
        errs.append("narration ids not contiguous")
    for m in re.finditer(r"<(\w+)[^>]*data-narration-id=", c):
        if m.group(1) not in ("h2", "p"):
            errs.append("narration id on <%s>" % m.group(1))

    dur = int(re.search(r'data-dur="(\d+)"', c).group(1))
    pins = re.findall(r'class="sv-ap-pin" data-track="t1" data-cid="([^"]+)" data-t="(\d+)" style="left:([\d.]+)%"', c)
    pin_t = {int(t) for _, t, _ in pins}
    pin_cid = {cid for cid, _, _ in pins}
    for cid, t, pct in pins:
        if abs(float(pct) - 100.0 * int(t) / dur) > 0.02:
            errs.append("pin %s left%% wrong" % cid)
        if int(t) > dur:
            errs.append("pin %s beyond video length" % cid)
    if [int(t) for _, t, _ in pins] != sorted(int(t) for _, t, _ in pins):
        errs.append("pins out of time order")
    for t in re.findall(r'class="sv-ap-ref" data-t="(\d+)"', c):
        if int(t) not in pin_t:
            errs.append("ref data-t=%s has no pin" % t)
    for cid in re.findall(r'data-chapters="([^"]+)"', c):
        if cid not in pin_cid:
            errs.append("chapters %s has no pin" % cid)

    cards = re.findall(r'<section class="sv-card', c)
    if len(cards) > 9:
        errs.append("%d cards" % len(cards))
    words = []
    for m in re.finditer(r'<section class="sv-card sv-card--statement".*?</section>', c, re.S):
        w = len(_html.unescape(re.sub(r"<[^>]+>", " ", m.group(0))).split())
        words.append(w)
        if w > 92:
            errs.append("statement card %d words" % w)
    if len(words) != len(pins):
        errs.append("%d statement cards for %d pins" % (len(words), len(pins)))

    for m in re.finditer(r"%[sdr](?![a-zA-Z])", c + (l["exam_tip_html"] or "") + (l["conclusion_html"] or "")):
        errs.append("unsubstituted format placeholder %r" % m.group(0))
    low = (c + (l["exam_tip_html"] or "") + (l["conclusion_html"] or "")).lower()
    if "video walkthrough" in low:
        errs.append("Video walkthrough")
    if "<iframe" in low or "youtube.com/embed" in low:
        errs.append("second embed")
    if r["subject"] == "music-eduqas":
        for w in ("eduqas", "wjec"):
            if w in low or w in (l["title"] or "").lower() or w in (l["description"] or "").lower():
                errs.append("names the board: %s" % w)

    chunks = extract_narration_chunks(c + (l["exam_tip_html"] or "") + (l["conclusion_html"] or ""))
    man = l["narration_manifest"] or []
    if len(man) != len(chunks):
        errs.append("manifest %d != %d narration chunks" % (len(man), len(chunks)))
    if any(not m.get("src", "").startswith("https://") or not m.get("duration") for m in man):
        errs.append("manifest entry malformed")

    if len(l["description"] or "") > 160:
        errs.append("description %d chars" % len(l["description"]))
    if len(l["practice_questions"] or []) != 6:
        errs.append("%d practice questions" % len(l["practice_questions"] or []))
    if len(l["knowledge_checks"] or []) != 5:
        errs.append("%d knowledge checks" % len(l["knowledge_checks"] or []))
    if not 5 <= len(l["flashcard_questions"] or []) <= 6:
        errs.append("%d flashcards" % len(l["flashcard_questions"] or []))
    for q in l["practice_questions"] or []:
        if set(q) != {"text", "type", "marks"}:
            errs.append("practice shape %s" % sorted(q))
        if re.search(r"award\s+\d+\s+marks?\s+for", str(q.get("marks", "")), re.I):
            errs.append("banned mark-scheme phrasing")
    for q in l["knowledge_checks"] or []:
        if set(q) != {"q", "type", "correct", "options"} or q["type"] != "mcq":
            errs.append("kc shape %s" % sorted(q))
        if len(set(q["options"])) != len(q["options"]):
            errs.append("kc duplicate options")
        if not 0 <= q["correct"] < len(q["options"]):
            errs.append("kc correct out of range")
    for q in l["flashcard_questions"] or []:
        if set(q) != {"q", "a"}:
            errs.append("flashcard shape %s" % sorted(q))
    plain = json.dumps([l["practice_questions"], l["knowledge_checks"], l["flashcard_questions"]], ensure_ascii=False)
    for ent in ("&mdash;", "&lsquo;", "&rsquo;", "&ldquo;", "&rdquo;", "&ndash;", "<p>", "<em>"):
        if ent in plain:
            errs.append("entity/tag %s in a plain-text field" % ent)
    for ch, name in (("\u2014", "&mdash;"), ("\u2018", "&lsquo;"), ("\u2019", "&rsquo;"),
                     ("\u201c", "&ldquo;"), ("\u201d", "&rdquo;")):
        if ch in c:
            errs.append("raw %s in content_html" % name)

    # preserved fields
    for f in ("status", "hero_image_url", "hero_image_alt", "hero_image_caption", "hero_image_position",
              "youtube_video_id", "slug", "lesson_number", "unit_id", "is_listening", "tier"):
        if json.dumps(l[f], default=str) != json.dumps(old[f], default=str):
            errs.append("CHANGED %s: %r -> %r" % (f, old[f], l[f]))
    if json.dumps(l["related_media"], ensure_ascii=False) != json.dumps(old["related_media"], ensure_ascii=False):
        errs.append("CHANGED related_media")

    tag = "OK" if not errs else "FAIL"
    print("%-46s %-6s %5d %5d %4d %s %4d %-14s %s"
          % ("%s/%s/L%02d" % (r["subject"], r["unit"], r["lesson"]), len(pins), len(cards), len(nids), len(man),
             "%d/%d/%d" % (len(l["practice_questions"] or []), len(l["knowledge_checks"] or []),
                           len(l["flashcard_questions"] or [])),
             len(l["description"] or ""), l["status"], tag))
    for e in errs:
        bad += 1
        print("      !! %s" % e)
print("\n%s" % ("ALL CLEAN" if not bad else "%d problems" % bad))
