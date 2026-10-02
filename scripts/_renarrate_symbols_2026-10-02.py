"""Re-narrate the paragraphs whose spoken text changed with the maths/science reading list
(narration.py commits a15328d5..ffaa073f, 2 Oct 2026). Tom: keep each lesson's existing voice
(Ollie odd / Ada even). Only the changed paragraphs are re-made.

Each new MP3 goes to a NEW R2 key (..._v2.mp3, _v3 ...) so a browser that cached the old file
cannot replay it. The old file stays in R2 untouched.

Unity rows are skipped: Unity gets a full Harry/Emily re-narration before its launch.

  python scripts/_renarrate_symbols_2026-10-02.py --scan      # build the target list (read only)
  python scripts/_renarrate_symbols_2026-10-02.py --run       # narrate + update manifests
"""
import os, sys, re, json, time, argparse, importlib.util, threading
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib import narration as new

spec = importlib.util.spec_from_file_location("narration_old", os.path.join(HERE, "_narration_before_symbols.py"))
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

OUT = os.path.join(HERE, "_renarrate_symbols_2026-10-02")
os.makedirs(OUT, exist_ok=True)
TARGETS = os.path.join(OUT, "targets.json")
BACKUP = os.path.join(OUT, "manifest_backup.json")
DONE = os.path.join(OUT, "done.jsonl")
LANG_PREFIXES = ("spanish", "french", "german")


def spoken(text, normalise_signs):
    if normalise_signs:   # what generate_audio_rest now does before sending
        text = re.sub(r"\s*−\s*", " minus ", text)
        text = re.sub(r"(?<=\d)\s*×\s*(?=[\d(])", " times ", text)
        text = re.sub(r"(?<=\d)\s*÷\s*(?=[\d(])", " divided by ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\s+([,.;:!?])", r"\1", text)   # spacing alone does not change the audio


# Tested on Ollie 2 Oct 2026: he already says en-dash ranges, =, x, /, degrees, squared/cubed (unicode),
# ohms, micro, plus-or-minus, >=, <=, pi, approximately and square root. He gets these wrong, so only a
# paragraph with one of them is re-made: subscript and other superscript digits, arrows, < and > as maths,
# delta, the U+2212 minus, and HTML powers (<sup>, which the old reader flattened: 2^7 read "27").
OLLIE_FAILS = re.compile("[₀-₉⁰¹⁴-⁹⁺⁻→←↔⇌⇒Δ−≠∝∴∞]")
NEW_WORDS = (" to the power of ", " squared", " cubed", " sub ", " less than ", " greater than ")


def needs(old_t, new_t):
    o, n = spoken(old_t, False), spoken(new_t, True)
    if o == n:
        return False
    if OLLIE_FAILS.search(old_t):
        return True
    return any(w in n and w not in o for w in NEW_WORDS)


def scan():
    sb = get_client()
    unity = [s["id"] for s in sb.table("schools").select("id,name").execute().data if "unity" in s["name"].lower()]
    subs = sb.table("subjects").select("id,slug,school_id").execute().data
    targets, n_lessons = [], 0
    for s in subs:
        if s["school_id"] in unity or s["slug"].startswith(LANG_PREFIXES):
            continue
        for u in sb.table("units").select("id,slug").eq("subject_id", s["id"]).execute().data:
            rows = sb.table("lessons").select(
                "id,lesson_number,content_html,exam_tip_html,conclusion_html,narration_manifest,is_listening"
            ).eq("unit_id", u["id"]).not_.is_("narration_manifest", "null").execute().data
            for r in rows:
                man = r["narration_manifest"] or []
                if not man or r.get("is_listening"):
                    continue
                n_lessons += 1
                html = "".join(r.get(k) or "" for k in ("content_html", "exam_tip_html", "conclusion_html"))
                a = dict(old.extract_narration_chunks(html))
                b = new.extract_narration_chunks(html)
                changed = [cid for cid, t in b if needs(a.get(cid, ""), t)]
                if not changed:
                    continue
                ids_man = [m["id"] for m in man]
                targets.append({"id": r["id"], "label": f"{s['slug']}/{u['slug']}/L{r['lesson_number']:02d}",
                                "lesson_number": r["lesson_number"], "changed": changed,
                                "aligned": ids_man == [cid for cid, _ in b]})
        print(f"  {s['slug']}: {len(targets)} lessons so far", flush=True)
    json.dump(targets, open(TARGETS, "w", encoding="utf-8"), indent=1)
    print(f"\nnarrated lessons scanned {n_lessons}; to re-narrate {len(targets)}; "
          f"paragraphs {sum(len(t['changed']) for t in targets)}; "
          f"manifest out of step with the text {sum(not t['aligned'] for t in targets)}")


def next_key(src):
    key = src[len(AUDIO_PUBLIC_URL) + 1:] if src.startswith(AUDIO_PUBLIC_URL) else re.sub(r"^https?://[^/]+/", "", src)
    key = key.split("?")[0]
    m = re.search(r"_v(\d+)\.mp3$", key)
    return re.sub(r"_v\d+\.mp3$", f"_v{int(m.group(1)) + 1}.mp3", key) if m else key[:-4] + "_v2.mp3"


def run(workers, only=None):
    sb, r2 = get_client(), get_r2_client()
    targets = json.load(open(TARGETS, encoding="utf-8"))
    done = set()
    if os.path.exists(DONE):
        done = {json.loads(l)["id"] for l in open(DONE, encoding="utf-8")}
    backup = json.load(open(BACKUP, encoding="utf-8")) if os.path.exists(BACKUP) else {}
    lock = threading.Lock()
    todo = [t for t in targets if t["id"] not in done and (not only or t["label"] in only)]
    print(f"{len(todo)} lessons to do ({len(done)} already done)", flush=True)

    def one(i_t):
        try:
            _one(*i_t)
        except Exception as e:
            print(f"[{i_t[0]}] ERROR {i_t[1]['label']}: {e}", flush=True)

    def _one(i, t):
        r = sb.table("lessons").select("content_html,exam_tip_html,conclusion_html,narration_manifest") \
              .eq("id", t["id"]).execute().data[0]
        man = r["narration_manifest"]
        html = "".join(r.get(k) or "" for k in ("content_html", "exam_tip_html", "conclusion_html"))
        chunks = new.extract_narration_chunks(html)
        a = dict(old.extract_narration_chunks(html))
        voice = new.LEGACY_ODD if t["lesson_number"] % 2 else new.LEGACY_EVEN
        by_id = {m["id"]: m for m in man}
        if [m["id"] for m in man] == [c for c, _ in chunks]:
            redo = {c for c, txt in chunks if needs(a.get(c, ""), txt)}
        else:
            if not any(needs(a.get(c, ""), txt) for c, txt in chunks):
                return
            redo = {c for c, _ in chunks}   # the audio is out of step with the text: remake it all
        if not redo:
            return
        sample = next(iter(man))["src"]
        new_man = []
        for cid, txt in chunks:
            if cid not in redo:
                new_man.append(by_id[cid]); continue
            src = by_id[cid]["src"] if cid in by_id else re.sub(r"_n\d+(_v\d+)?\.mp3", f"_{cid}.mp3", sample.split("?")[0])
            mp3 = new.generate_audio_rest(txt, voice)
            if mp3 is None:
                print(f"[{i}] FAIL {t['label']} {cid}", flush=True)
                return
            # named after THIS lesson: some lessons share another lesson's files, so a bumped
            # name could collide; _r1002 is new, so no browser holds a cached copy
            subj, unit, ln = t["label"].split("/")
            key = f"{subj}/{unit}/narration_lesson-{ln[1:]}_{cid}_r1002.mp3"
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            new_man.append({"id": cid, "src": f"{AUDIO_PUBLIC_URL}/{key}", "duration": new.get_mp3_duration(mp3)})
        with lock:
            backup[t["id"]] = man
            json.dump(backup, open(BACKUP, "w", encoding="utf-8"))
        sb.table("lessons").update({"narration_manifest": new_man}).eq("id", t["id"]).execute()
        with lock:
            open(DONE, "a", encoding="utf-8").write(json.dumps({"id": t["id"], "label": t["label"], "redone": len(redo)}) + "\n")
        print(f"[{i}/{len(todo)}] ok {t['label']} ({len(redo)} paragraphs)", flush=True)

    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(one, enumerate(todo, 1)))
    print("finished", time.strftime("%H:%M"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true"); ap.add_argument("--run", action="store_true")
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    if a.scan: scan()
    if a.run: run(a.workers, a.only)
