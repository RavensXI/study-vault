# -*- coding: utf-8 -*-
"""Apply the approved ear-vs-fact worklist (Tom, 16 Aug: "apply all three").

Three moves in western-classical-1650-1910:
  A. Eight rewrites — fact answers become hearable questions, same excerpt.
  B. Nine detaches — good revision questions lose their irrelevant excerpt.
  C. Drop L8 gold[3] — near-duplicate of gold[0] (Handel-vs-Verdi entry).

L6 silver[3] (Chopin period + "how can you tell") KEEPS its excerpt: the
answer names audible features, so it is a genuine listening question.

Backup: _backup_ear_vs_fact_2026-08-16.json (whole practice_data, L1-L8).
Run: python apply_ear_vs_fact.py [--apply]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_ear_vs_fact_2026-08-16.json")

# ---- A: rewrites. Each keeps its excerpt and its slot. -----------------------
REWRITES = {
    (1, "bronze", 0): {
        "question": "Listen to the opening minute. Is the home key major or minor, "
                    "and what tells you?",
        "options": ["Major — the music settles on bright, stable chords",
                    "Minor — it settles on dark, unstable chords",
                    "It has no home key",
                    "You cannot tell without seeing the score"],
        "solutions": [0],
        "explanation": "After the teasing introduction, the fast music lands on bright, "
                       "settled major-key chords and keeps returning to them. That sense "
                       "of a stable home is what 'major key' means in listening terms — "
                       "you are not expected to name the letter of the key by ear.",
    },
    (1, "silver", 0): {
        "question": "Listen to the very first chord (0:00–0:03). It sounds unstable — "
                    "like a question, not an answer. What is happening?",
        "options": ["It is a chord that pulls AWAY from the home key, so the symphony "
                    "opens mid-thought",
                    "It is the home chord played quietly",
                    "The orchestra is tuning",
                    "It is a wrong note by the players"],
        "solutions": [0],
        "explanation": "The opening chord leans away from home and demands an answer, "
                       "which is exactly why it surprised audiences in 1800. Beethoven "
                       "starts with tension and only settles the home key afterwards. "
                       "Hearing 'stable or unstable' is the skill Section A rewards.",
    },
    (2, "bronze", 0): {
        "question": "Listen to the opening 30 seconds. Is this music in a major or a "
                    "minor key, and how can you tell?",
        "options": ["Minor — the restless, dark colour of the theme",
                    "Major — bright and settled",
                    "Neither — it is atonal",
                    "Both at once"],
        "solutions": [0],
        "explanation": "The famous opening theme sighs and presses forward with a dark, "
                       "unsettled colour — the sound of a minor key. Major-key music "
                       "feels brighter and more at rest. Naming major or minor by ear "
                       "is a core Section A skill; naming the letter is not.",
    },
    (3, "bronze", 0): {
        "question": "Listen to the extract. The soloist is a clarinet. Is the music "
                    "major or minor, and what is its character?",
        "options": ["Major — light, dancing and good-humoured",
                    "Minor — dark and stormy",
                    "Major — slow and solemn",
                    "Minor — restless and agitated"],
        "solutions": [0],
        "explanation": "The finale skips along in a bright major key with a "
                       "good-humoured, dance-like character. Pairing 'major or minor' "
                       "with a character word is exactly how to describe tonality in "
                       "the exam without claiming to hear the key's name.",
    },
    (5, "gold", 1): {
        "question": "Baroque pieces usually visit closely related keys. Which "
                    "RELATIONSHIP is the most common first move away from home?",
        "options": ["The dominant — the key five notes above the home key",
                    "A completely unrelated key",
                    "The key one semitone higher",
                    "Baroque music never leaves its home key"],
        "solutions": [0],
        "explanation": "The dominant is the closest relative — one sharp away — so "
                       "Baroque composers move there first, then return home. Knowing "
                       "the RELATIONSHIP is the learnable fact; you are never asked to "
                       "hear the visited key's name.",
        "detach": True,     # theory question — the excerpt added nothing
    },
    (7, "bronze", 1): {
        "question": "Listen to the opening phrase. Is it major or minor — and does the "
                    "music feel settled or searching?",
        "options": ["Major, with a gentle, dreamlike calm",
                    "Minor, uneasy and tense",
                    "Major, march-like and driving",
                    "Minor, fast and dance-like"],
        "solutions": [0],
        "explanation": "Träumerei means 'dreaming', and the music floats in a warm "
                       "major key with no hurry at all. Character words like 'dreamlike' "
                       "or 'calm', tied to the tonality, earn the describing marks.",
    },
    (8, "bronze", 0): {
        "question": "Listen to the opening. Is this music major or minor, and which "
                    "features create its terror?",
        "options": ["Minor — hammering chords, extreme dynamics and rushing scales",
                    "Major — bright fanfares and steady calm",
                    "Major — quiet and hymn-like",
                    "Minor — slow, thin and gentle"],
        "solutions": [0],
        "explanation": "The Dies Irae erupts in a dark minor key, with hammered chords, "
                       "huge dynamic contrasts and scales that rush downwards like "
                       "judgement falling. Feature-plus-effect is the full-mark shape "
                       "for a question like this.",
    },
}

# ---- B: detaches — the question stands, the excerpt goes. --------------------
DETACH = [
    (1, "gold", 1),    # why Beethoven delays C major — recall
    (1, "gold", 3),    # daring-for-1800 — recall (its twin silver[0] keeps the ear framing)
    (2, "bronze", 2),  # relative major of G minor — theory
    (2, "silver", 1),  # why Mozart added clarinets — history
    (2, "gold", 2),    # sonata-form second subject — not hearable in 30s
    (3, "gold", 1),    # basset clarinet range — history
    (5, "bronze", 0),  # Zadok: which occasion — history
    (7, "gold", 1),    # character piece genre — history
    (8, "silver", 0),  # Verdi vs Handel style — comparison recall
    (8, "gold", 0),    # choral entry comparison — needs BOTH pieces, keep as recall
]

DROP = (8, "gold", 3)  # near-duplicate of L8 gold[0]


def main():
    sb = get_client()
    subj = [s for s in sb.table("subjects").select("id,slug").execute().data
            if s["slug"] == "music-aqa"][0]["id"]
    unit = [u for u in sb.table("units").select("id,slug,subject_id").execute().data
            if u["subject_id"] == subj and u["slug"] == "western-classical-1650-1910"][0]["id"]
    rows = {r["lesson_number"]: r for r in sb.table("lessons")
            .select("id,lesson_number,practice_data").eq("unit_id", unit).execute().data}

    backup = {str(n): rows[n]["practice_data"] for n in sorted(rows)}
    touched = set()

    for (les, tier, idx), spec in REWRITES.items():
        p = rows[les]["practice_data"]["problem_bank"][tier][idx]
        print("A L%d %s[%d]: %r -> %r" % (les, tier, idx,
                                          p["question"][:45], spec["question"][:45]))
        assert p["input_type"] == "multiple_choice", (les, tier, idx)
        p["question"] = spec["question"]
        p["options"] = spec["options"]
        p["solutions"] = spec["solutions"]
        p["explanation"] = spec["explanation"]
        p.pop("misconceptions", None)       # stale against the new options
        if spec.get("detach"):
            p.pop("passage_id", None)
        touched.add(les)

    for les, tier, idx in DETACH:
        p = rows[les]["practice_data"]["problem_bank"][tier][idx]
        print("B L%d %s[%d]: detach %s  (%r)" % (les, tier, idx,
                                                 p.get("passage_id"), p["question"][:50]))
        p.pop("passage_id", None)
        touched.add(les)

    les, tier, idx = DROP
    bank = rows[les]["practice_data"]["problem_bank"][tier]
    print("C L%d %s[%d]: DROP %r" % (les, tier, idx, bank[idx]["question"][:60]))
    assert "Compare the choral entry" in bank[idx]["question"], "dup moved — abort"
    del bank[idx]
    touched.add(les)

    # sanity: every remaining problem still has valid solutions/options
    for n in touched:
        for t in ("bronze", "silver", "gold"):
            for i, p in enumerate(rows[n]["practice_data"]["problem_bank"][t]):
                if p.get("input_type") == "multiple_choice":
                    s = p["solutions"][0]
                    assert 0 <= s < len(p["options"]), (n, t, i)
                    assert p.get("explanation"), (n, t, i)

    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for n in sorted(touched):
        sb.table("lessons").update({"practice_data": rows[n]["practice_data"]}) \
            .eq("id", rows[n]["id"]).execute()
    print("applied to lessons:", sorted(touched), "— backup:", BACKUP)


if __name__ == "__main__":
    main()
