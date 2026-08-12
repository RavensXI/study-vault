# -*- coding: utf-8 -*-
"""Wire the real excerpts into listening-skills L1 (tonality) and L3 (texture).

Task #46. Whole tiers are converted, never individual questions: a lone real
clip among synthetic ones stands out as the odd item for reasons that have
nothing to do with music, which would hand the student a free answer.

  L1 gold   -> 4 questions, all real recordings (was 3 constructed)
  L3 bronze -> 4 questions, all real recordings (was 3 constructed)

The question stem never names the work — the student has to hear it. The
EXPLANATION always names it, so the answer key stays auditable by anyone,
musically trained or not.

    python wire_real_excerpts.py [--dry-run|--restore]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

BACKUP = os.path.join(HERE, "_wire_real_backup.json")
MANIFEST = os.path.join(HERE, "_real_excerpts.json")
EX = {e["id"]: e for e in json.load(open(MANIFEST, encoding="utf-8"))}

PLAYER = ('<div style="text-align:center"><p style="font-family:Inter,system-ui,sans-serif;'
          'font-size:.9rem;margin:0 0 .6rem">Listen to the excerpt, then answer.</p>'
          '<audio controls preload="metadata" src="%s" style="width:100%%;max-width:460px"></audio>'
          '<p style="font-size:.72rem;opacity:.55;margin:.5rem 0 0">Public domain recording.</p></div>')

TONALITY = [("real_major_beethoven", "major"), ("real_minor_mozart40", "minor"),
            ("real_major_k622", "major"), ("real_minor_verdi", "minor")]
TEXTURE = [("real_tex_melacc_chopin", "melody and accompaniment"),
           ("real_tex_homophonic_zadok", "homophonic"),
           ("real_tex_melacc_traumerei", "melody and accompaniment"),
           ("real_tex_homophonic_verdi", "homophonic")]

TON_OPTS = ["Major", "Minor", "Pentatonic", "Chromatic"]
TEX_OPTS = ["Monophonic — a single line with no accompaniment",
            "Melody and accompaniment — a tune supported underneath",
            "Homophonic — parts moving together in the same rhythm",
            "Imitative polyphony — parts entering one after another with the same idea"]


def build(kind, items):
    qs, passages = [], []
    for cid, feature in items:
        e = EX[cid]
        pid = "p-" + cid
        passages.append({"id": pid, "label": "Listening excerpt", "text": PLAYER % e["url"]})
        if kind == "tonality":
            opts, idx = TON_OPTS, (0 if feature == "major" else 1)
            stem = "Listen to the excerpt. What is its tonality?"
        else:
            opts = TEX_OPTS
            idx = 1 if feature == "melody and accompaniment" else 2
            stem = "Listen to the excerpt. Which best describes its texture?"
        qs.append({"input_type": "multiple_choice", "passage_id": pid, "question": stem,
                   "options": opts, "solutions": [idx],
                   "explanation": "%s This is %s. %s" % (
                       ("The answer is %s." % opts[idx].split(" — ")[0].lower()),
                       e["work"], e["why"])})
    return qs, passages


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()
    sub = [x for x in sb.table("subjects").select("id,slug,school_id")
           .eq("slug", "music-aqa").execute().data if not x["school_id"]][0]
    unit = [u for u in sb.table("units").select("id,slug").eq("subject_id", sub["id"])
            .execute().data if u["slug"] == "listening-skills"][0]["id"]

    if "--restore" in sys.argv:
        for lid, pd in json.load(open(BACKUP, encoding="utf-8")).items():
            sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
        print("restored")
        return

    saved = {}
    for num, tier, kind, items in ((1, "gold", "tonality", TONALITY),
                                   (3, "bronze", "texture", TEXTURE)):
        row = sb.table("lessons").select("id,practice_data").eq("unit_id", unit) \
            .eq("lesson_number", num).single().execute().data
        pd = json.loads(json.dumps(row["practice_data"]))
        before = len(pd["problem_bank"][tier])
        qs, passages = build(kind, items)

        # drop the passages that only the replaced questions used
        old_pids = {q.get("passage_id") for q in pd["problem_bank"][tier]}
        still = set()
        for t, lst in pd["problem_bank"].items():
            if t == tier:
                continue
            for q in lst:
                still.add(q.get("passage_id"))
        pd["passages"] = [p for p in pd["passages"]
                          if p["id"] not in (old_pids - still)] + passages
        pd["problem_bank"][tier] = qs

        ids = {p["id"] for p in pd["passages"]}
        for t, lst in pd["problem_bank"].items():
            assert len(lst) >= 4, (num, t, len(lst))
            for q in lst:
                assert q["passage_id"] in ids, (num, q["passage_id"])
                assert 0 <= q["solutions"][0] < len(q["options"])
        # the whole tier must be real — no mixing
        assert all("/real/" in [p for p in pd["passages"] if p["id"] == q["passage_id"]][0]["text"]
                   for q in pd["problem_bank"][tier]), num
        saved[row["id"]] = row["practice_data"]
        if not dry:
            sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
        print("  L%d %-7s %d -> %d questions, all real recordings" % (num, tier, before, len(qs)))

    if not dry and saved and not os.path.exists(BACKUP):
        json.dump(saved, open(BACKUP, "w", encoding="utf-8"))
        print("backup ->", BACKUP)
    print(("DRY RUN — " if dry else "") + "done")


if __name__ == "__main__":
    main()
