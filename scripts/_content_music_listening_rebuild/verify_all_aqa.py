# -*- coding: utf-8 -*-
"""Post-rebuild verification for the four music-aqa listening lessons.
Re-reads each from live Supabase, checks the deck contract, checks the dock
survived byte-for-byte apart from pins and any corrected data-dur, and diffs
the preserved fields against the backup taken before any write."""
import io, json, os, re, sys, html as _html
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import _Bal
from lib.supabase_client import get_client
from lib.narration import extract_narration_chunks

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(io.open(os.path.join(HERE, "_rows_index_aqa.json"), encoding="utf-8"))
DUR_FIXES = {"music-aqa__aos2-popular-music__L03": {"187": "172"},
             "music-aqa__aos3-traditional-music__L02": {"300": "225"}}
sb = get_client()
bad = 0
print("%-34s %5s %5s %5s %5s %-8s %-6s %s" % ("lesson", "pins", "cards", "nids", "man", "q/k/f", "desc", "status"))
for r in rows:
    l = sb.table("lessons").select("*").eq("id", r["id"]).single().execute().data
    old = json.load(io.open(os.path.join(HERE, "backups", r["file"]), encoding="utf-8"))
    c = l["content_html"] or ""
    tip, con = l["exam_tip_html"] or "", l["conclusion_html"] or ""
    errs = []

    b = _Bal(); b.feed(c)
    if b.errors or b.stack:
        errs.append("unbalanced tags %s %s" % (b.errors[:3], b.stack[:3]))

    nids = [int(x) for x in re.findall(r'data-narration-id="n(\d+)"', c + tip + con)]
    if nids != list(range(1, len(nids) + 1)):
        errs.append("narration ids across content+tip+conclusion not contiguous")
    if len(set(nids)) != len(nids):
        errs.append("duplicate narration ids")
    for m in re.finditer(r"<(\w+)[^>]*data-narration-id=", c):
        if m.group(1) not in ("h2", "p"):
            errs.append("narration id on <%s> in content" % m.group(1))

    # dock preserved apart from pins and the corrected durations
    cut = '<div class="sv-listening"'
    dn, do = c[:c.index(cut)], old["content_html"][:old["content_html"].index(cut)]
    strip = lambda s: re.sub(r'<button type="button" class="sv-ap-pin".*?</span></button>', "", s, flags=re.S)
    do_fixed = strip(do)
    for a, bb in DUR_FIXES.get(r["file"][:-5], {}).items():
        do_fixed = do_fixed.replace('data-dur="%s"' % a, 'data-dur="%s"' % bb)
    if strip(dn) != do_fixed:
        errs.append("DOCK CHANGED beyond pins and the corrected data-dur")
    if "sv-ap-wave" in do:
        for k in ("data-audio=", "data-peaks=", "sv-ap-canvas", "sv-ap-peaks"):
            if k not in dn:
                errs.append("R2 wave dock lost %s" % k)

    # durations and pin geometry
    durs = {m.group(1): int(m.group(2)) for m in re.finditer(r'data-track="(t\d)"[^>]*data-dur="(\d+)"', dn)}
    if "sv-ap-wave" in dn:
        durs["t1"] = float(re.search(r'class="sv-ap-peaks">\{"duration":([\d.]+)', dn).group(1))
    pins = re.findall(r'class="sv-ap-pin"(?: data-track="(t\d)")? data-cid="([^"]+)" data-t="([\d.]+)" style="left:([\d.]+)%"', dn)
    for trk, cid, t, pct in pins:
        dd = durs[trk or "t1"]
        if abs(float(pct) - 100.0 * float(t) / dd) > 0.02:
            errs.append("pin %s left=%s%% != %.2f%%" % (cid, pct, 100.0 * float(t) / dd))
        if float(t) > dd:
            errs.append("pin %s beyond track length" % cid)
    bytrack = {}
    for trk, cid, t, _ in pins:
        bytrack.setdefault(trk or "t1", []).append(float(t))
    for k, v in bytrack.items():
        if v != sorted(v):
            errs.append("pins out of order on %s" % k)
    pint = {("%g" % float(t)) for _, _, t, _ in pins}
    cids = {cid for _, cid, _, _ in pins}
    for t in re.findall(r'class="sv-ap-ref" data-t="([\d.]+)"', c):
        if t not in pint:
            errs.append("ref data-t=%s has no pin" % t)
    for ch in re.findall(r'data-chapters="([^"]+)"', c):
        for k in ch.split(","):
            if k.strip() not in cids:
                errs.append("data-chapters=%s has no pin" % k)
    # refs must carry data-track exactly when the dock is multi-track
    is_wave = "sv-ap-wave" in dn
    for m in re.finditer(r'<button type="button" class="sv-ap-ref" data-t="[\d.]+"( data-track="t\d")?>', c):
        if is_wave and m.group(1):
            errs.append("wave-dock ref carries data-track")
        if not is_wave and not m.group(1):
            errs.append("multi-track ref missing data-track")

    cards = re.findall(r'<section class="sv-card', c)
    stmts = re.findall(r'<section class="sv-card sv-card--statement".*?</section>', c, re.S)
    if len(stmts) != len(pins):
        errs.append("%d statement cards for %d pins" % (len(stmts), len(pins)))
    if len(cards) != len(pins) + 2:
        errs.append("%d cards, expected pins+2=%d" % (len(cards), len(pins) + 2))
    for m in stmts:
        w = len(_html.unescape(re.sub(r"<[^>]+>", " ", m)).split())
        if w > 92:
            errs.append("statement card %d words" % w)

    for m in re.finditer(r"%[sdr](?![a-zA-Z])", c + tip + con):
        errs.append("unsubstituted format placeholder %r" % m.group(0))
    low = (c + tip + con).lower()
    if "video walkthrough" in low:
        errs.append("Video walkthrough")
    if "<iframe" in low or "youtube.com/embed" in low:
        errs.append("in-card iframe still present")
    for ch, name in (("\u2014", "&mdash;"), ("\u2018", "&lsquo;"), ("\u2019", "&rsquo;"),
                     ("\u201c", "&ldquo;"), ("\u201d", "&rdquo;")):
        if ch in c:
            errs.append("raw %s in content_html" % name)

    chunks = extract_narration_chunks(c + tip + con)
    man = l["narration_manifest"] or []
    if len(man) != len(chunks):
        errs.append("manifest %d != %d narration chunks" % (len(man), len(chunks)))
    if any(not m.get("src", "").startswith("https://") or not m.get("duration") for m in man):
        errs.append("manifest entry malformed")
    if len({m["id"] for m in man}) != len(man):
        errs.append("duplicate ids in manifest")

    if len(l["description"] or "") > 160:
        errs.append("description %d chars" % len(l["description"]))
    for name, n in (("practice", 6), ("kc", 5)):
        key = "practice_questions" if name == "practice" else "knowledge_checks"
        if len(l[key] or []) != n:
            errs.append("%d %s" % (len(l[key] or []), name))
    if not 5 <= len(l["flashcard_questions"] or []) <= 6:
        errs.append("%d flashcards" % len(l["flashcard_questions"] or []))

    for f in ("status", "hero_image_url", "hero_image_alt", "hero_image_caption", "hero_image_position",
              "youtube_video_id", "slug", "lesson_number", "unit_id", "is_listening", "tier"):
        if json.dumps(l[f], default=str) != json.dumps(old[f], default=str):
            errs.append("CHANGED %s: %r -> %r" % (f, old[f], l[f]))
    if json.dumps(l["related_media"], ensure_ascii=False) != json.dumps(old["related_media"], ensure_ascii=False):
        errs.append("CHANGED related_media")
    for f in ("practice_questions", "knowledge_checks", "flashcard_questions"):
        if json.dumps(l[f], ensure_ascii=False) != json.dumps(old[f], ensure_ascii=False):
            errs.append("NOTE %s changed" % f)

    print("%-34s %5d %5d %5d %5d %-8s %-6d %-6s %s"
          % ("%s/L%02d" % (r["unit"], r["lesson"]), len(pins), len(cards), len(nids), len(man),
             "%d/%d/%d" % (len(l["practice_questions"] or []), len(l["knowledge_checks"] or []),
                           len(l["flashcard_questions"] or [])),
             len(l["description"] or ""), l["status"], "OK" if not errs else "FAIL"))
    for e in errs:
        bad += 1
        print("      !! %s" % e)
print("\n%s" % ("ALL CLEAN" if not bad else "%d problems" % bad))
