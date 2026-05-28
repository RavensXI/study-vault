"""Clear narration_manifest on the 13 Psychology lessons whose content_html
was modified by the fact-check fixes, so the next _narrate_psychology-aqa.py
run regenerates them.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

LESSON_IDS = [
    "4f4d2702-76ee-437a-b1ee-44b1bd694625",  # perception L3 — Müller-Lyer
    "2a61473b-02dd-49ea-bad9-ae8c4ee160f7",  # social-influence L2 — Milgram (renumbered)
    "ab626ef1-c7cb-4f91-bc33-b498f49f8238",  # memory L2 — Peterson & Peterson (renumbered)
    "fbf12185-4842-45a8-8832-2c4a9db31974",  # psychological-problems L2 — Beck
    "5339426d-d46a-4409-a5a6-642eddbf9812",  # perception L4 — Gilchrist & Nesberg
    "8263fc26-3fc6-48fb-bd4c-802d092910b8",  # social-influence L3 — Piliavin
    "4e05cab1-ccf2-47e3-952b-461b1dcaff8a",  # language-thought-communication L1 — Whorf
    "bf92da7d-40fd-43d0-9a50-639ebc37555a",  # language-thought-communication L2 — Von Frisch
    "e06035e9-3635-4972-8e40-54a2cb1ad51c",  # social-influence L1 — Asch
    "8b25369b-36f4-49a7-a83e-91c32da0b92c",  # memory L3 — Murdock
    "9b516a6c-f5b1-4056-ba30-b48b27482c4a",  # psychological-problems L3 — SSRI
    "6dcb5640-7d05-44fc-8897-effc26e2013f",  # development L2 — Piaget
    "f98b558f-16c5-45dc-a77c-43a3bd66288b",  # brain-neuropsychology L2 — dopamine
]

sb = get_client()
cleared = 0
errors = 0
for lid in LESSON_IDS:
    try:
        row = sb.table("lessons").select("id,title,narration_manifest").eq("id", lid).execute().data
        if not row:
            print(f"  [MISS] {lid}")
            errors += 1
            continue
        title = row[0]["title"]
        sb.table("lessons").update({"narration_manifest": None}).eq("id", lid).execute()
        cleared += 1
        print(f"  [OK]   {lid}  {title[:60]}")
    except Exception as e:
        print(f"  [ERR]  {lid}  {e}")
        errors += 1

print(f"\nCleared {cleared} narration manifests. Errors: {errors}")
print("Next: re-run `python scripts/_narrate_psychology-aqa.py`")
