# -*- coding: utf-8 -*-
"""Post-rebuild verification for the four music-ocr aos3-rhythms-listening
lessons. Re-reads each row from live Supabase and checks the deck contract, the
dock geometry, the narration manifest, and that nothing which had to be
preserved was touched. Also re-audits every related-media URL and confirms each
docked recording is still embeddable.

Usage: python verify_all_ocr.py [--skip-net]
"""
import io, json, os, re, sys, html as _html
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
from deck import _Bal
from lib.supabase_client import get_client
from lib.narration import extract_narration_chunks

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(io.open(os.path.join(HERE, "_rows_index_ocr.json"), encoding="utf-8"))
NET = "--skip-net" not in sys.argv
# durations reported by a real YouTube IFrame player on the studyvault.co.uk origin
TRUE_DUR = {"JzdkIrQ73iY": 246, "pPZFlxmfqrM": 312, "WvFh7PmMmXk": 513, "_3Ksv4Z1q4o": 186,
            "7-CEt1XQ2A4": 292, "oToZfPGMMBY": 337, "2dGbBoQNeCU": 274, "BWcwonrBw0w": 498}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}

sb = get_client()
bad = 0
print("%-6s %5s %5s %5s %5s %-8s %-5s %-4s %-16s %s"
      % ("lesson", "pins", "cards", "nids", "man", "q/k/f", "desc", "rm", "status", ""))
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
    for m in re.finditer(r"<(\w+)[^>]*data-narration-id=", c):
        if m.group(1) not in ("h2", "p"):
            errs.append("narration id on <%s> in content" % m.group(1))

    # ---- dock -------------------------------------------------------------
    if not c.startswith('<figure class="sv-annotated-player sv-ap-yt"'):
        errs.append("content does not open with the annotated player")
    if '<div class="sv-listening"' not in c:
        errs.append("no sv-listening stage")
    tracks = re.findall(r'class="sv-ap-trackbtn[^"]*" data-track="(t\d)" data-yt="([\w-]{11})" data-dur="(\d+)"', c)
    if len(tracks) != 2:
        errs.append("%d track buttons, expected 2" % len(tracks))
    if c.count("sv-ap-trackbtn--on") != 1:
        errs.append("%d tracks marked --on, expected 1" % c.count("sv-ap-trackbtn--on"))
    durs = {}
    for tid, yt, dur in tracks:
        durs[tid] = int(dur)
        if yt not in TRUE_DUR:
            errs.append("unknown video %s" % yt)
        elif int(dur) != TRUE_DUR[yt]:
            errs.append("data-dur=%s for %s but the player reports %d" % (dur, yt, TRUE_DUR[yt]))

    pins = re.findall(r'class="sv-ap-pin" data-track="(t\d)" data-cid="([^"]+)" data-t="(\d+)" style="left:([\d.]+)%"', c)
    cids = [p[1] for p in pins]
    if len(set(cids)) != len(cids):
        errs.append("duplicate pin cids")
    for trk, cid, t, pct in pins:
        if trk not in durs:
            errs.append("pin %s on undeclared track %s" % (cid, trk)); continue
        if abs(float(pct) - 100.0 * int(t) / durs[trk]) > 0.02:
            errs.append("pin %s left=%s%% != %.2f%%" % (cid, pct, 100.0 * int(t) / durs[trk]))
        if int(t) > durs[trk]:
            errs.append("pin %s beyond track length" % cid)
    for trk in durs:
        ts = [int(p[2]) for p in pins if p[0] == trk]
        if ts != sorted(ts):
            errs.append("pins out of time order on %s" % trk)
        if not ts:
            errs.append("track %s has no pins" % trk)

    pint = {(p[0], int(p[2])) for p in pins}
    refs = re.findall(r'class="sv-ap-ref" data-t="(\d+)" data-track="(t\d)"', c)
    if len(refs) != len(re.findall(r'class="sv-ap-ref"', c)):
        errs.append("some sv-ap-ref buttons are missing data-t or data-track")
    for t, trk in refs:
        if (trk, int(t)) not in pint:
            errs.append("ref data-t=%s on %s has no pin" % (t, trk))
    for ch in re.findall(r'data-chapters="([^"]+)"', c):
        for k in ch.split(","):
            if k.strip() not in cids:
                errs.append("data-chapters=%s has no pin" % k)
    # a statement card must declare the same track as the pin it points at
    for m in re.finditer(r'<section class="sv-card sv-card--statement"[^>]*data-track="(t\d)" data-chapters="([^"]+)"', c):
        owner = [p[0] for p in pins if p[1] == m.group(2)]
        if owner and owner[0] != m.group(1):
            errs.append("card for %s declares %s, pin is on %s" % (m.group(2), m.group(1), owner[0]))

    cards = re.findall(r'<section class="sv-card', c)
    stmts = re.findall(r'<section class="sv-card sv-card--statement".*?</section>', c, re.S)
    if len(stmts) != len(pins):
        errs.append("%d statement cards for %d pins" % (len(stmts), len(pins)))
    if len(cards) != len(pins) + 2:
        errs.append("%d cards, expected pins+2=%d" % (len(cards), len(pins) + 2))
    if len(re.findall(r'<section class="sv-card sv-card--cover', c)) != 1:
        errs.append("expected exactly one cover card")
    for m in stmts:
        w = len(_html.unescape(re.sub(r"<[^>]+>", " ", m)).split())
        if w > 92:
            errs.append("statement card %d words" % w)
        if "Listen for:" not in m:
            errs.append("statement card with no 'Listen for:' line")

    for m in re.finditer(r"%[sdr](?![a-zA-Z])", c + tip + con):
        errs.append("unsubstituted format placeholder %r" % m.group(0))
    low = (c + tip + con).lower()
    if "<iframe" in low or "youtube.com/embed" in low:
        errs.append("in-card iframe")
    if "video walkthrough" in low:
        errs.append("Video walkthrough")
    for ch, name in (("\u2014", "&mdash;"), ("\u2018", "&lsquo;"), ("\u2019", "&rsquo;"),
                     ("\u201c", "&ldquo;"), ("\u201d", "&rdquo;"), ("\u2013", "&ndash;")):
        if ch in c:
            errs.append("raw %s in content_html" % name)

    # ---- narration --------------------------------------------------------
    chunks = extract_narration_chunks(c + tip + con)
    man = l["narration_manifest"] or []
    if len(man) != len(chunks):
        errs.append("manifest %d != %d narration chunks" % (len(man), len(chunks)))
    if any(not m.get("src", "").startswith("https://") or not m.get("duration") for m in man):
        errs.append("manifest entry malformed")
    if len({m["id"] for m in man}) != len(man):
        errs.append("duplicate ids in manifest")
    chunk_ids = {cid for cid, _ in chunks}
    if {m["id"] for m in man} != chunk_ids:
        errs.append("manifest ids do not match the narration ids in the HTML")

    # ---- row fields -------------------------------------------------------
    if l["practice_data"] not in (None, {}):
        errs.append("practice_data not cleared")
    if l["is_listening"] is not True:
        errs.append("is_listening is %r" % l["is_listening"])
    if l["youtube_video_id"] is not None:
        errs.append("youtube_video_id is %r" % l["youtube_video_id"])
    if len(l["description"] or "") > 160:
        errs.append("description %d chars" % len(l["description"]))
    if len(l["practice_questions"] or []) != 6:
        errs.append("%d practice questions" % len(l["practice_questions"] or []))
    if len(l["knowledge_checks"] or []) != 5:
        errs.append("%d knowledge checks" % len(l["knowledge_checks"] or []))
    if not 5 <= len(l["flashcard_questions"] or []) <= 6:
        errs.append("%d flashcards" % len(l["flashcard_questions"] or []))
    for q in (l["knowledge_checks"] or []):
        if set(q) != {"q", "type", "correct", "options"} or not 0 <= q["correct"] < len(q["options"]):
            errs.append("malformed knowledge check %r" % q.get("q", "")[:40])
    txt = json.dumps([l["practice_questions"], l["knowledge_checks"], l["flashcard_questions"]], ensure_ascii=False)
    for entity in ("&mdash;", "&lsquo;", "&rsquo;", "&ldquo;", "&rdquo;", "&ndash;", "&amp;", "<p>", "<em>"):
        if entity in txt:
            errs.append("question fields contain %s" % entity)

    # things the rebuild must NOT have changed
    for f in ("status", "hero_image_url", "slug", "lesson_number", "unit_id", "tier"):
        if json.dumps(l[f], default=str) != json.dumps(old[f], default=str):
            errs.append("CHANGED %s: %r -> %r" % (f, old[f], l[f]))
    # L2 and L4 were deliberately re-heroed (the drill build left a West African
    # djembe on the Middle East lesson and a drum-kit snare on the Americas one,
    # and a listening lesson shows its hero on the cover card). Same R2 key, so
    # the URL is unchanged; the caption and alt must match rehero_log.json.
    rehero = json.load(io.open(os.path.join(HERE, "ytpick", "rehero_log.json"), encoding="utf-8"))
    key = str(r["lesson"])
    if key in rehero:
        for f, want in (("hero_image_caption", rehero[key]["caption"]), ("hero_image_alt", rehero[key]["alt"])):
            if l[f] != want:
                errs.append("%s does not match the re-hero log: %r" % (f, l[f]))
        if l["hero_image_caption"] == old["hero_image_caption"]:
            errs.append("hero caption never updated after the re-hero")
    else:
        for f in ("hero_image_alt", "hero_image_caption", "hero_image_position"):
            if json.dumps(l[f], default=str) != json.dumps(old[f], default=str):
                errs.append("CHANGED %s: %r -> %r" % (f, old[f], l[f]))
    hr = requests.head(l["hero_image_url"], timeout=30) if NET else None
    if hr is not None and hr.status_code != 200:
        errs.append("hero image HTTP %s" % hr.status_code)

    # ---- related media ----------------------------------------------------
    rm = l["related_media"] or []
    n_items = sum(len(cat.get("items") or []) for cat in rm)
    if not 4 <= n_items <= 8:
        errs.append("%d related-media items" % n_items)
    if NET:
        for cat in rm:
            for it in (cat.get("items") or []):
                u = it["url"]
                m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})", u)
                try:
                    if m:
                        rr = requests.get("https://www.youtube.com/oembed",
                                          params={"url": u, "format": "json"}, timeout=30)
                    else:
                        rr = requests.get(u, headers=UA, timeout=40, allow_redirects=True)
                    if rr.status_code != 200:
                        errs.append("related media %s -> HTTP %s" % (u, rr.status_code))
                except Exception as e:
                    errs.append("related media %s -> %s" % (u, str(e)[:60]))
    if NET:
        for tid, yt, dur in tracks:
            rr = requests.get("https://www.youtube.com/oembed",
                              params={"url": "https://www.youtube.com/watch?v=" + yt, "format": "json"}, timeout=30)
            if rr.status_code != 200:
                errs.append("docked video %s oEmbed %s (not embeddable)" % (yt, rr.status_code))

    print("%-6s %5d %5d %5d %5d %-8s %-5d %-4d %-16s %s"
          % ("L%02d" % r["lesson"], len(pins), len(cards), len(nids), len(man),
             "%d/%d/%d" % (len(l["practice_questions"] or []), len(l["knowledge_checks"] or []),
                           len(l["flashcard_questions"] or [])),
             len(l["description"] or ""), n_items, l["status"], "OK" if not errs else "FAIL"))
    for e in errs:
        bad += 1
        print("      !! %s" % e)

# routing: the unit must no longer be listed as a practice unit
s = sb.table("subjects").select("settings").eq("slug", "music-ocr").is_("school_id", "null").execute().data[0]
pu = (s["settings"] or {}).get("practice_units") or []
if "aos3-rhythms-listening" in pu:
    bad += 1
    print("      !! aos3-rhythms-listening is still in subjects.settings.practice_units")
else:
    print("routing OK: practice_units =", pu)

n = sb.table("lessons").select("id", count="exact").eq("is_listening", True).execute().count
print("site-wide is_listening = true:", n)
print("\n%s" % ("ALL CLEAN" if not bad else "%d problems" % bad))
