# -*- coding: utf-8 -*-
"""Re-home every hero that lives off-platform or in another subject's folder.

URL swap only — same image, same caption, zero visual change. Downloads the
current image, stores it at {subject}/{unit}/lesson-NN-hero.jpg on R2, and
updates hero_image_url. Kills the link-rot risk (hotlinks) and the silent
cross-subject coupling (another subject edits its hero, ours changes too).

Scope: every lesson whose hero is an offsite hotlink or a cross-subject R2
URL, EXCLUDING lessons on the regen worklist (they get new images anyway).
School-bespoke lessons are included — the swap changes no pixels.
Wikimedia URLs are fetched last, slowly, with 429 backoff. Resumable.

    python scripts/_hero_rehome.py [--one]
"""
import io
import json
import os
import re
import sys
import tempfile
import time
import urllib.parse
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.wikimedia import resize_and_compress
from lib.r2 import get_r2_client, IMAGES_BUCKET

R2_HOST = "pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"
R2_PUBLIC = f"https://{R2_HOST}"
UA = "StudyVaultHeroBot/1.0 (https://www.studyvault.co.uk; studyvault.info@gmail.com)"
SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
STATE = os.path.join(SCRATCH, "_hero_rehome_state.json")
WORKLIST = os.path.join(SCRATCH, "_hero_regen_worklist.json")


def classify(url, slug):
    if not url:
        return "none"
    if url.startswith("/") or url.startswith("images/"):
        return "site-local"
    if R2_HOST in url:
        m = re.search(R2_HOST + r"/([^/]+)/", url)
        return "own" if m and m.group(1) == slug else "cross-r2"
    return "wikimedia" if ("wikimedia" in url or "wikipedia" in url) else "hotlink"


def fetch(url, is_wikimedia):
    url = urllib.parse.quote(url, safe=":/?&=%")
    delay = 3.0 if is_wikimedia else 0.4
    for attempt in range(4):
        try:
            time.sleep(delay)
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) < 5000:
                raise ValueError(f"too small ({len(data)}b)")
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                wait = 60 * (attempt + 1)
                print(f"      429 — backing off {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("retries exhausted")


def main():
    one_only = "--one" in sys.argv
    state = {"done": {}, "failed": {}}
    if os.path.exists(STATE):
        state = json.load(io.open(STATE, encoding="utf-8"))
    regen_ids = {r["lesson_id"] for r in json.load(io.open(WORKLIST, encoding="utf-8"))}

    sb = get_client()
    r2 = get_r2_client()

    subs = {s["id"]: s for s in sb.table("subjects").select("id,slug").execute().data}
    units = sb.table("units").select("id,subject_id,slug").execute().data
    unit_by_id = {u["id"]: u for u in units}

    jobs = []
    off = 0
    while True:
        page = (sb.table("lessons").select("id,unit_id,lesson_number,hero_image_url")
                .order("id").range(off, off + 999).execute()).data
        for l in page:
            u = unit_by_id.get(l["unit_id"])
            if not u:
                continue
            s = subs.get(u["subject_id"])
            if not s:
                continue
            kind = classify(l.get("hero_image_url"), s["slug"])
            if kind in ("hotlink", "wikimedia", "cross-r2") \
                    and l["id"] not in regen_ids and l["id"] not in state["done"]:
                jobs.append({"lesson_id": l["id"], "subject": s["slug"],
                             "unit": u["slug"], "n": l["lesson_number"],
                             "url": l["hero_image_url"], "kind": kind})
        if len(page) < 1000:
            break
        off += 1000

    jobs.sort(key=lambda j: (j["kind"] == "wikimedia", j["subject"], j["n"]))
    print(f"to re-home: {len(jobs)} "
          f"({sum(j['kind'] != 'wikimedia' for j in jobs)} fast, "
          f"{sum(j['kind'] == 'wikimedia' for j in jobs)} wikimedia-slow) | "
          f"already done: {len(state['done'])}")

    n_ok = 0
    for j in jobs:
        key = f"{j['subject']}/{j['unit']}/L{j['n']:02d}"
        try:
            data = fetch(j["url"], j["kind"] == "wikimedia")
        except Exception as e:
            print(f"  [FAIL] {key}: {str(e)[:90]}")
            state["failed"][j["lesson_id"]] = {"key": key, "url": j["url"],
                                               "error": str(e)[:200]}
            json.dump(state, io.open(STATE, "w", encoding="utf-8"), indent=1)
            continue

        tmp_src = tmp_dst = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".img") as f:
                tmp_src = f.name
                f.write(data)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                tmp_dst = f.name
            resize_and_compress(tmp_src, tmp_dst, max_width=1200, quality=82)
            with open(tmp_dst, "rb") as f:
                body = f.read()
        except Exception as e:  # truncated/corrupt download — record, move on
            print(f"  [FAIL] {key}: image processing: {str(e)[:90]}")
            state["failed"][j["lesson_id"]] = {"key": key, "url": j["url"],
                                               "error": str(e)[:200]}
            json.dump(state, io.open(STATE, "w", encoding="utf-8"), indent=1)
            continue
        finally:
            for p in (tmp_src, tmp_dst):
                if p:
                    try:
                        os.unlink(p)
                    except OSError:
                        pass

        r2_key = f"{j['subject']}/{j['unit']}/lesson-{j['n']:02d}-hero.jpg"
        r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=body,
                      ContentType="image/jpeg")
        new_url = f"{R2_PUBLIC}/{r2_key}"
        sb.table("lessons").update({"hero_image_url": new_url}) \
            .eq("id", j["lesson_id"]).execute()
        state["done"][j["lesson_id"]] = {"key": key, "old": j["url"],
                                         "new": new_url, "kind": j["kind"]}
        state["failed"].pop(j["lesson_id"], None)
        json.dump(state, io.open(STATE, "w", encoding="utf-8"), indent=1)
        n_ok += 1
        if n_ok % 25 == 0:
            print(f"  {n_ok}/{len(jobs)} re-homed")
        if one_only:
            print(f"  [OK] {key}: {j['kind']} -> {new_url}")
            print("--one: stopping.")
            return

    print(f"\nre-homed {n_ok} | failed {len(state['failed'])} | total done {len(state['done'])}")


if __name__ == "__main__":
    main()
