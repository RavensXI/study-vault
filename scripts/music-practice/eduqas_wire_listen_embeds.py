# -*- coding: utf-8 -*-
"""Convert the 39 dead sv-listen boxes in the ten non-study-piece
music-eduqas articles (Tom's call, 16 Aug): wire an official in-body
YouTube embed where one verifies (the AQA article pattern), delete the
box where none does — removing its narration-manifest clip so nothing
plays against removed content.

Narration safety: a wired box KEEPS its figcaption text and
data-narration-id verbatim on the new sv-embed figure, so existing
clips stay true. Only deletions touch the manifest.

Verification per candidate video: YouTube oEmbed must return 200
(alive + embeddable) AND the title must contain at least one required
keyword AND the author must look plausible for an official source.

Stage 1 (this file, --curate): ask the model for candidate official
videos per work, verify, and write the winners to
_eduqas_listen_embed_map.json for review.
Stage 2 (--apply): rewrite content_html + manifests from that map.
"""
import io
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

MAP_PATH = os.path.join(HERE, "_eduqas_listen_embed_map.json")
BACKUP = os.path.join(HERE, "_backup_listen_embeds_2026-08-16.json")
ART = ["aos1-forms-and-devices", "aos2-music-for-ensemble",
       "aos3-film-music", "aos4-popular-music"]

# (unit, lesson, nid, work label for curation, title keywords — lowercase,
#  any-match)
BOXES = [
    ("aos1-forms-and-devices", 1, "n7",
     "Chopin, Prelude Op. 28 No. 15 'Raindrop'", ["raindrop", "op. 28", "prelude"]),
    ("aos1-forms-and-devices", 1, "n10",
     "Mozart, Rondo alla Turca (Piano Sonata K. 331, 3rd movement)",
     ["alla turca", "turkish", "k. 331", "k331"]),
    ("aos1-forms-and-devices", 1, "n13",
     "Elgar, Enigma Variations — Variation IX 'Nimrod'", ["nimrod", "enigma"]),
    ("aos1-forms-and-devices", 1, "n18",
     "Haydn, Symphony No. 94 'Surprise', 3rd movement (Minuet and Trio)",
     ["94", "surprise"]),
    ("aos1-forms-and-devices", 2, "n7",
     "Pachelbel, Canon in D", ["canon"]),
    ("aos1-forms-and-devices", 2, "n12",
     "Handel, 'Hallelujah' chorus from Messiah", ["hallelujah", "messiah"]),
    ("aos1-forms-and-devices", 2, "n18",
     "Bach, Toccata and Fugue in D minor BWV 565", ["toccata"]),
    ("aos1-forms-and-devices", 2, "n29",
     "The Beatles, 'Let It Be'", ["let it be"]),
    ("aos2-music-for-ensemble", 1, "n8",
     "Mozart, Eine kleine Nachtmusik K. 525, 1st movement",
     ["eine kleine", "nachtmusik", "k. 525", "k525"]),
    ("aos2-music-for-ensemble", 1, "n12",
     "Schubert, 'Trout' Quintet D. 667, 4th movement", ["trout", "forellen"]),
    ("aos2-music-for-ensemble", 1, "n17",
     "Haydn, String Quartet Op. 20 No. 2, 4th movement fugue",
     ["op. 20", "op.20", "op 20"]),
    ("aos2-music-for-ensemble", 1, "n20",
     "Debussy, String Quartet in G minor, 2nd movement",
     ["debussy", "quartet"]),
    ("aos2-music-for-ensemble", 2, "n9",
     "Miles Davis, 'So What'", ["so what"]),
    ("aos2-music-for-ensemble", 2, "n14",
     "Charlie Parker, 'Now's the Time'", ["now's the time", "nows the time"]),
    ("aos2-music-for-ensemble", 2, "n20",
     "Bessie Smith with Louis Armstrong, 'St Louis Blues' (1925)",
     ["st louis blues", "st. louis blues"]),
    ("aos2-music-for-ensemble", 2, "n25",
     "Duke Ellington, 'It Don't Mean a Thing (If It Ain't Got That Swing)'",
     ["mean a thing"]),
    ("aos2-music-for-ensemble", 3, "n5",
     "Les Miserables, 'One Day More'", ["one day more"]),
    ("aos2-music-for-ensemble", 3, "n10",
     "West Side Story, 'Tonight' (Quintet)", ["tonight"]),
    ("aos2-music-for-ensemble", 3, "n15",
     "Haydn, String Quartet Op. 76 No. 3 'Emperor', 2nd movement",
     ["emperor", "op. 76", "op.76", "op 76"]),
    ("aos2-music-for-ensemble", 3, "n19",
     "Nielsen, Wind Quintet Op. 43", ["nielsen", "wind quintet"]),
    ("aos3-film-music", 1, "n8",
     "John Williams, 'The Imperial March' (Star Wars)", ["imperial march"]),
    ("aos3-film-music", 1, "n16",
     "John Williams, Jaws main theme", ["jaws"]),
    ("aos3-film-music", 1, "n23",
     "Bernard Herrmann, Psycho shower scene cue ('The Murder')",
     ["psycho", "murder"]),
    ("aos3-film-music", 1, "n28",
     "Howard Shore, 'Concerning Hobbits' / the Shire theme (The Lord of the "
     "Rings)", ["hobbits", "shire"]),
    ("aos3-film-music", 2, "n8",
     "Maurice Jarre, Lawrence of Arabia — Main Title / Overture",
     ["lawrence of arabia"]),
    ("aos3-film-music", 2, "n14",
     "John Williams, 'The Imperial March' (The Empire Strikes Back)",
     ["imperial march"]),
    ("aos3-film-music", 2, "n19",
     "Bernard Herrmann, Psycho shower scene cue ('The Murder')",
     ["psycho", "murder"]),
    ("aos3-film-music", 2, "n27",
     "Hans Zimmer and Lisa Gerrard, 'Now We Are Free' (Gladiator)",
     ["now we are free", "gladiator"]),
    ("aos3-film-music", 3, "n7",
     "John Williams, Jaws main theme", ["jaws"]),
    ("aos3-film-music", 3, "n12",
     "Bernard Herrmann, Psycho shower scene cue ('The Murder')",
     ["psycho", "murder"]),
    ("aos3-film-music", 3, "n20",
     "John Williams, Jurassic Park main theme", ["jurassic"]),
    ("aos4-popular-music", 1, "n6",
     "Michael Jackson, 'Billie Jean' (official video)", ["billie jean"]),
    ("aos4-popular-music", 1, "n11",
     "The Beatles, 'Let It Be'", ["let it be"]),
    ("aos4-popular-music", 1, "n15",
     "Journey, 'Don't Stop Believin''", ["stop believin"]),
    ("aos4-popular-music", 1, "n20",
     "Adele, 'Someone Like You' (official video)", ["someone like you"]),
    ("aos4-popular-music", 2, "n8",
     "Panjabi MC, 'Mundian To Bach Ke'", ["mundian"]),
    ("aos4-popular-music", 2, "n12",
     "Malkit Singh, 'Gur Nalo Ishq Mitha'", ["gur nalo", "ishq mitha"]),
    ("aos4-popular-music", 2, "n18",
     "Bally Sagoo — a signature remix of a traditional Punjabi song (e.g. "
     "'Chura Liya')", ["sagoo", "chura"]),
    ("aos4-popular-music", 2, "n23",
     "Cornershop, 'Brimful of Asha'", ["brimful"]),
]

# known-good ids already verified on AQA (reuse before asking the model)
KNOWN = {
    "n20/aos3-film-music/3": "lDlU08RU7Tk",   # Jurassic Park, AQA-verified
}


def oembed(vid):
    try:
        u = ("https://www.youtube.com/oembed?format=json&url="
             "https://www.youtube.com/watch?v=" + vid)
        d = json.loads(urllib.request.urlopen(u, timeout=15).read()
                       .decode("utf-8"))
        return d.get("title", ""), d.get("author_name", "")
    except Exception:
        return None, None


def vid_of(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", url or "")
    return m.group(1) if m else (url if url and re.fullmatch(r"[\w-]{11}", url)
                                 else None)


BAN = ["trailer", "reaction", "karaoke", "tutorial", "how to play",
       "lesson", "1 hour", "one hour", "slowed", "8d audio", "loop"]
OFFICIALISH = ["vevo", "topic", "official", "records", "orchestra",
               "philharmon", "symphony", "bach society", "sony", "universal",
               "warner", "decca", "deutsche", "halidon", "chandos", "naxos",
               "quartet", "gramophone", "classic fm", "bbc"]


def yt_search(query, limit=8):
    import urllib.parse
    url = ("https://www.youtube.com/results?hl=en&search_query="
           + urllib.parse.quote(query))
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB,en;q=0.9",
        "Cookie": "CONSENT=YES+cb.20240101-00-p0.en+FX+000"})
    html = urllib.request.urlopen(req, timeout=20).read().decode(
        "utf-8", "replace")
    out, seen = [], set()
    for m in re.finditer(
            r'"videoRenderer":\{"videoId":"([\w-]{11})".*?'
            r'"title":\{"runs":\[\{"text":"(.*?)"\}\].*?'
            r'"ownerText":\{"runs":\[\{"text":"(.*?)"', html):
        vid, title, owner = m.group(1), m.group(2), m.group(3)
        if vid in seen:
            continue
        seen.add(vid)
        title = title.encode("utf-8").decode("unicode_escape", "replace")
        owner = owner.encode("utf-8").decode("unicode_escape", "replace")
        out.append((vid, title, owner))
        if len(out) >= limit:
            break
    return out


def artist_tokens(work):
    # channel plausibility: first comma-separated chunk of the work label
    head = re.split(r"[,—]", work)[0]
    return [t.lower() for t in re.findall(r"[A-Za-z']{4,}", head)]


def pick_for(key, work, kws):
    pool = []
    if key in KNOWN:
        pool.append((KNOWN[key], None, None))
    for vid, title, owner in yt_search(work + " official"):
        pool.append((vid, title, owner))
    toks = artist_tokens(work)
    for vid, title, owner in pool:
        if title is None:
            title, owner = oembed(vid)
            if title is None:
                continue
        tl, ol = title.lower(), (owner or "").lower()
        if not any(k in tl for k in kws):
            continue
        if any(b in tl for b in BAN):
            continue
        if not (any(t in ol for t in toks)
                or any(o in ol for o in OFFICIALISH)
                or any(t in tl for t in toks) and "official" in tl):
            continue
        # final gate: oEmbed proves embeddability even for search finds
        t2, a2 = oembed(vid)
        if t2 is None:
            continue
        return {"vid": vid, "title": t2, "author": a2}
    return None


def curate():
    result = {}
    for u, n, nid, w, kws in BOXES:
        key = "%s/%s/%d" % (nid, u, n)
        try:
            picked = pick_for(key, w, kws)
        except Exception as e:
            print("  ! %s search error: %s" % (key, e))
            picked = None
        result[key] = picked
        print("%s %s -> %s" % ("OK " if picked else "DEL", key,
                               "%s | %s | %s" % (picked["vid"],
                                                 picked["title"][:45],
                                                 picked["author"][:35])
                               if picked else "no verified video"))
    io.open(MAP_PATH, "w", encoding="utf-8").write(
        json.dumps(result, indent=1, ensure_ascii=False))
    ok = sum(1 for v in result.values() if v)
    print("\nmap written: %d wired, %d to delete -> %s"
          % (ok, len(result) - ok, MAP_PATH))


def apply():
    emap = json.load(io.open(MAP_PATH, encoding="utf-8"))
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "music-eduqas") \
        .execute().data[0]["id"]
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug,subject_id").execute().data
             if u["subject_id"] == sub}
    by_lesson = {}
    for u, n, nid, w, kws in BOXES:
        by_lesson.setdefault((u, n), []).append(nid)
    backup, writes = {}, []
    wired = deleted = 0
    for (uslug, num), nids in sorted(by_lesson.items()):
        row = sb.table("lessons").select(
            "id,content_html,narration_manifest") \
            .eq("unit_id", units[uslug]).eq("lesson_number", num) \
            .execute().data[0]
        ch, manifest = row["content_html"], row["narration_manifest"] or []
        removed_ids = []
        for nid in nids:
            figm = re.search(
                r'<figure class="sv-listen"[^>]*data-narration-id="%s".*?'
                r"</figure>" % nid, ch, re.S)
            assert figm, "%s L%d %s: figure not found" % (uslug, num, nid)
            fig = figm.group(0)
            pick = emap["%s/%s/%d" % (nid, uslug, num)]
            if pick:
                capm = re.search(
                    r"<figcaption[^>]*>(.*?)</figcaption>", fig, re.S)
                cap = capm.group(1) if capm else re.sub(
                    r"</?figure[^>]*>|</?figcaption[^>]*>", "",
                    re.sub(r'<figure[^>]*>', "", fig))
                new = ('<figure class="sv-embed" data-narration-id="%s">'
                       '<div class="sv-embed-frame"><iframe '
                       'src="https://www.youtube.com/embed/%s" '
                       'title="%s" loading="lazy" allow="fullscreen" '
                       "allowfullscreen></iframe></div>"
                       '<figcaption class="sv-embed-cap">%s</figcaption>'
                       "</figure>"
                       % (nid, pick["vid"],
                          pick["title"].replace('"', "&quot;"), cap))
                ch = ch.replace(fig, new)
                wired += 1
            else:
                ch = ch.replace(fig, "")
                removed_ids.append(nid)
                deleted += 1
        new_manifest = [c for c in manifest if c["id"] not in removed_ids]
        upd = {"content_html": ch}
        if removed_ids:
            upd["narration_manifest"] = new_manifest
        backup[row["id"]] = {"content_html": row["content_html"],
                             "narration_manifest": manifest}
        writes.append((row["id"], upd))
        print("%s L%d: %d wired, %d deleted (manifest %d -> %d)"
              % (uslug, num, len(nids) - len(removed_ids), len(removed_ids),
                 len(manifest), len(new_manifest)))
    print("\ntotal: %d wired, %d deleted" % (wired, deleted))
    if "--apply" not in sys.argv:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, upd in writes:
        sb.table("lessons").update(upd).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    if "--curate" in sys.argv:
        curate()
    else:
        apply()
