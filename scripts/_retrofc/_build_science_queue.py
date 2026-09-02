"""Append the GCSE science article units to the retro fact-check queue.

Skips practice-format units (subjects.settings.practice_units and any unit
whose live lessons all carry practice_data). Each item carries the spec
file(s) the checker must read, resolved per board + unit prefix, and the
qualification (combined / separate). Idempotent: existing (subject, unit)
items are left alone.

Usage: python scripts/_retrofc/_build_science_queue.py [--dry-run]
"""
import json
import os
import sys
import urllib.request
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, "_queue.json")

# Order: AQA pair, Edexcel pair, OCR Gateway pair, OCR 21C pair.
SUBJECTS = ["science-aqa", "separate-sciences", "science-edexcel", "separate-sciences-edexcel",
            "science-ocr", "separate-sciences-ocr", "science-ocr-b", "separate-sciences-ocr-b"]

SPEC = {
    "science-aqa": {"combined": "specs/aqa/science-8464-8464.md"},
    "separate-sciences": {"biology": "specs/aqa/biology-8461-8461.md", "chemistry": "specs/aqa/chemistry-8462-8462.md",
                          "physics": "specs/aqa/physics-8463-8463.md"},
    "science-edexcel": {"combined": "specs/edexcel/combined-science-1SC0.md"},
    "separate-sciences-edexcel": {"biology": "specs/edexcel/biology-1BI0.md", "chemistry": "specs/edexcel/chemistry-1CH0.md",
                                  "physics": "specs/edexcel/physics-1PH0.md"},
    "science-ocr": {"combined": "specs/ocr/combined-science-a-gateway-J250.md"},
    "separate-sciences-ocr": {"biology": "specs/ocr/biology-a-gateway-J247.md", "chemistry": "specs/ocr/chemistry-a-gateway-J248.md",
                              "physics": "specs/ocr/physics-a-gateway-J249.md"},
    "science-ocr-b": {"combined": "specs/ocr/combined-science-b-21c-J260.md"},
    "separate-sciences-ocr-b": {"biology": "specs/ocr/biology-b-21c-J257.md", "chemistry": "specs/ocr/chemistry-b-21c-J258.md",
                                "physics": "specs/ocr/physics-b-21c-J259.md"},
}


def get(path):
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    req = urllib.request.Request(U + "/rest/v1/" + path, headers={"apikey": K, "Authorization": "Bearer " + K})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def spec_for(subject, unit_slug):
    m = SPEC[subject]
    if "combined" in m:
        return m["combined"]
    for k in ("biology", "chemistry", "physics"):
        if unit_slug.startswith(k):
            return m[k]
    return None


def main():
    dry = "--dry-run" in sys.argv
    q = json.load(open(QUEUE, encoding="utf-8"))
    have = {(i["subject"], i["unit"]) for i in q["items"]}
    slugs = ",".join(SUBJECTS)
    subs = {s["slug"]: s for s in get(f"subjects?select=id,slug,settings&school_id=is.null&slug=in.({slugs})")}
    added = []
    for slug in SUBJECTS:
        s = subs[slug]
        practice = set((s.get("settings") or {}).get("practice_units") or [])
        units = get(f"units?select=id,slug,name,sort_order&subject_id=eq.{s['id']}&order=sort_order")
        ids = ",".join(u["id"] for u in units)
        lessons = get(f"lessons?select=id,unit_id,status,practice_data&unit_id=in.({ids})")
        live = Counter(x["unit_id"] for x in lessons if x.get("status") == "live")
        pdata = Counter(x["unit_id"] for x in lessons if x.get("status") == "live" and x.get("practice_data"))
        for u in units:
            n = live.get(u["id"], 0)
            if not n or u["slug"] in practice or pdata.get(u["id"], 0) == n:
                continue
            if (slug, u["slug"]) in have:
                continue
            spec = spec_for(slug, u["slug"])
            if not spec:
                print("!! no spec for", slug, u["slug"])
                continue
            item = {"subject": slug, "unit": u["slug"], "lessons": n, "status": "queued", "spec": spec,
                    "qualification": "combined" if slug.startswith("science-") else "separate", "family": "science"}
            q["items"].append(item)
            added.append(item)
    for a in added:
        print(f"+ {a['subject']}/{a['unit']} ({a['lessons']}L) -> {a['spec']}")
    print(f"{len(added)} units, {sum(a['lessons'] for a in added)} lessons appended")
    if not dry:
        json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("queue saved")


if __name__ == "__main__":
    main()
