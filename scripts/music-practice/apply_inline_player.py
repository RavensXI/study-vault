# -*- coding: utf-8 -*-
"""Swap the browser's default <audio controls> pill for the inline waveform
player across every Music AQA practice drill.

Reads peaks from _drill_peaks.json (build it first with gen_drill_peaks.py) and
embeds them inline, because R2 sends no Access-Control-Allow-Origin header so a
cross-origin fetch of a .peaks.json is blocked in the browser.

Touches three places inside practice_data: passages[].text, worked_examples and
method_card. Any audio file missing from the manifest keeps its plain element —
better a working default control than a silent waveform.

Usage:
    python scripts/music-practice/apply_inline_player.py --dry-run
    python scripts/music-practice/apply_inline_player.py
    python scripts/music-practice/apply_inline_player.py --restore <backup.json>
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

HERE = os.path.dirname(os.path.abspath(__file__))
PEAKS_FILE = os.path.join(HERE, "_drill_peaks.json")
BACKUP = os.path.join(HERE, "_drill_practice_data_backup.json")
UNITS = ["western-classical-1650-1910", "aos-listening", "listening-skills", "score-reading"]

AUDIO_TAG = re.compile(r"<audio\b[^>]*>\s*</audio>", re.I)
SRC = re.compile(r'src="([^"]+)"')

# listening-skills L3's only worked example points at a file that 404s, so the
# demonstration plays silence. exC_perfect is the one existing clip that matches
# the worked answer ("perfect"). Reused deliberately: hearing a perfect cadence
# in the demo and again in a question is reinforcement, not a leak of an answer
# the student has not been taught.
BROKEN = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-aqa/listening-skills/ex015_cadence.mp3"
REPLACEMENT = "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/music-aqa/listening-skills/exC_perfect.mp3"


def fmt(t):
    t = max(0, int(t or 0))
    return "%d:%02d" % (t // 60, t % 60)


def player_html(url, entry):
    payload = json.dumps({"peaks": entry["peaks"], "duration": entry["duration"]},
                         separators=(",", ":"))
    # One row — play, waveform, clock. The old native control was ~54px tall and
    # the worked-example card has no room to spare; a stacked layout pushed the
    # question text out of the card.
    return (
        '<figure class="sv-ap-inline" data-audio="%s">'
        '<button type="button" class="sv-api-play" aria-label="Play">&#9654;</button>'
        '<div class="sv-api-wrap"><canvas class="sv-api-canvas"></canvas></div>'
        '<span class="sv-api-tick">0:00 / %s</span>'
        '<script type="application/json" class="sv-api-peaks">%s</script>'
        '</figure>'
    ) % (url, fmt(entry["duration"]), payload)


class Stats(object):
    def __init__(self):
        self.converted = 0
        self.skipped_no_peaks = 0
        self.rerouted = 0
        self.missing = set()


def convert_string(s, peaks, st):
    def repl(m):
        tag = m.group(0)
        sm = SRC.search(tag)
        if not sm:
            return tag
        url = sm.group(1)
        if url == BROKEN:
            url = REPLACEMENT
            st.rerouted += 1
        entry = peaks.get(url)
        if not entry:
            st.skipped_no_peaks += 1
            st.missing.add(url.rsplit("/", 1)[-1])
            return tag
        st.converted += 1
        return player_html(url, entry)
    return AUDIO_TAG.sub(repl, s)


def walk(node, peaks, st):
    if isinstance(node, str):
        return convert_string(node, peaks, st) if "<audio" in node else node
    if isinstance(node, list):
        return [walk(v, peaks, st) for v in node]
    if isinstance(node, dict):
        return dict((k, walk(v, peaks, st)) for k, v in node.items())
    return node


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()

    if "--restore" in sys.argv:
        path = sys.argv[sys.argv.index("--restore") + 1]
        with open(path, "r", encoding="utf-8") as f:
            saved = json.load(f)
        for lid, pd in saved.items():
            sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
            print("restored", lid[:8])
        print("restored %d lessons" % len(saved))
        return

    if not os.path.exists(PEAKS_FILE):
        sys.exit("run gen_drill_peaks.py first — no %s" % PEAKS_FILE)
    with open(PEAKS_FILE, "r", encoding="utf-8") as f:
        peaks = json.load(f)
    print("peaks manifest: %d files" % len(peaks))

    lessons = []
    for slug in UNITS:
        unit = [u for u in sb.table("units").select("id,slug,name").execute().data if u["slug"] == slug][0]
        for les in sb.table("lessons").select("id,lesson_number,title,practice_data") \
                .eq("unit_id", unit["id"]).order("lesson_number").execute().data:
            lessons.append((slug, les))
    print("drill lessons: %d" % len(lessons))

    # back up BEFORE any write — bulk edits get a way home
    if not dry:
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(dict((l["id"], l["practice_data"]) for _, l in lessons), f)
        print("backup written:", BACKUP)

    total = Stats()
    print()
    for slug, les in lessons:
        pd = les["practice_data"] or {}
        before = json.dumps(pd, ensure_ascii=False)
        if "sv-ap-inline" in before:
            print("  %-28s L%-2d already converted — skipped" % (slug[:28], les["lesson_number"]))
            continue
        st = Stats()
        new = walk(pd, peaks, st)
        total.converted += st.converted
        total.skipped_no_peaks += st.skipped_no_peaks
        total.rerouted += st.rerouted
        total.missing |= st.missing

        after = json.dumps(new, ensure_ascii=False)
        # structural guards: nothing but the audio elements may change
        assert after.count("sv-ap-inline") == st.converted, "player count mismatch"
        assert len(AUDIO_TAG.findall(after)) == st.skipped_no_peaks, "stray audio elements left"
        assert BROKEN not in after, "broken clip still referenced"
        for key in pd:
            assert key in new, "lost practice_data key " + key
        if isinstance(pd.get("problem_bank"), dict):
            for tier in pd["problem_bank"]:
                assert len(new["problem_bank"][tier]) == len(pd["problem_bank"][tier]), \
                    "question count changed in " + tier

        flag = "" if not st.skipped_no_peaks else "  (%d left plain)" % st.skipped_no_peaks
        print("  %-28s L%-2d  %2d player%s%s%s" % (
            slug[:28], les["lesson_number"], st.converted,
            "" if st.converted == 1 else "s",
            "  [rerouted broken clip]" if st.rerouted else "", flag))
        if not dry and st.converted:
            sb.table("lessons").update({"practice_data": new}).eq("id", les["id"]).execute()

    print()
    print("players written : %d" % total.converted)
    print("left plain      : %d %s" % (total.skipped_no_peaks,
                                       sorted(total.missing) if total.missing else ""))
    print("broken clips re-pointed: %d" % total.rerouted)
    if dry:
        print("\nDRY RUN — nothing written")


if __name__ == "__main__":
    main()
