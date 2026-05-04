"""Fix accent_badge to translucent <accent>33 for PE AQA + OCR units.

Memory rule: accent_badge must be `<accent>33`, not a solid darker hex.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

PATCH = {
    "physical-education-aqa": {
        "human-body-and-movement": "#be123c33",
        "socio-cultural-influences-and-wellbeing": "#1d4ed833",
    },
    "physical-education-ocr": {
        "physical-factors-affecting-performance": "#be123c33",
        "socio-cultural-issues-and-sports-psychology": "#1d4ed833",
    },
}

for subj_slug, unit_map in PATCH.items():
    sid = sb.table("subjects").select("id").eq("slug", subj_slug).is_("school_id", "null").execute().data[0]["id"]
    units = sb.table("units").select("id, slug").eq("subject_id", sid).execute().data
    for u in units:
        if u["slug"] in unit_map:
            new_badge = unit_map[u["slug"]]
            sb.table("units").update({"accent_badge": new_badge}).eq("id", u["id"]).execute()
            print(f"  {subj_slug}/{u['slug']} -> {new_badge}")
