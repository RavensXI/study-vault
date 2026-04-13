#!/usr/bin/env python3
"""Insert Physics Calculations unit + L1 (Energy) into Combined Science for preview.

Run: python -m scripts.science-practice.insert_preview_l1
"""

import json
import sys
from scripts.lib.supabase_client import get_client

sb = get_client()

# ── Find Unity Combined Science subject ──────────────────────────────────
subj = sb.table("subjects").select("id, settings").eq("slug", "science").not_.is_("school_id", "null").execute().data
if not subj:
    print("ERROR: Could not find Unity science subject")
    sys.exit(1)

SUBJECT_ID = subj[0]["id"]
settings = subj[0]["settings"] or {}
print(f"Found science subject: {SUBJECT_ID}")

# ── Check if unit already exists ─────────────────────────────────────────
existing = sb.table("units").select("id").eq("subject_id", SUBJECT_ID).eq("slug", "physics-calculations").execute().data
if existing:
    UNIT_ID = existing[0]["id"]
    print(f"Unit already exists: {UNIT_ID}")
else:
    # Create Physics Calculations unit
    result = sb.table("units").insert({
        "subject_id": SUBJECT_ID,
        "slug": "physics-calculations",
        "name": "Physics Calculations",
        "subtitle": "Drill every recall equation for the Physics papers",
        "body_class": "unit-science-phys-calc",
        "accent": "#2563eb",
        "accent_light": "#2563eb22",
        "accent_badge": "#2563eb33",
        "sort_order": 7,
        "lesson_count": 8
    }).execute()
    UNIT_ID = result.data[0]["id"]
    print(f"Created unit: {UNIT_ID}")

# ── Load lesson data ─────────────────────────────────────────────────────
with open("scripts/science-practice/combined_phys_calc.json", "r", encoding="utf-8") as f:
    lessons = json.load(f)

lesson_data = lessons[0]  # L1 only

# ── Check if lesson already exists ───────────────────────────────────────
existing_lesson = sb.table("lessons").select("id").eq("unit_id", UNIT_ID).eq("lesson_number", 1).execute().data
if existing_lesson:
    # Update existing
    lid = existing_lesson[0]["id"]
    sb.table("lessons").update({
        "practice_data": lesson_data["practice_data"],
        "title": lesson_data["title"],
        "slug": lesson_data["slug"],
        "description": lesson_data["description"],
    }).eq("id", lid).execute()
    print(f"Updated lesson: {lid}")
else:
    # Insert new
    result = sb.table("lessons").insert({
        "unit_id": UNIT_ID,
        "lesson_number": 1,
        "slug": lesson_data["slug"],
        "title": lesson_data["title"],
        "description": lesson_data["description"],
        "practice_data": lesson_data["practice_data"],
        "status": "live"
    }).execute()
    print(f"Inserted lesson: {result.data[0]['id']}")

# ── Update subject settings to include practice_units ────────────────────
practice_units = settings.get("practice_units", [])
if "physics-calculations" not in practice_units:
    practice_units.append("physics-calculations")
    settings["practice_units"] = practice_units
    sb.table("subjects").update({"settings": settings}).eq("id", SUBJECT_ID).execute()
    print(f"Updated practice_units: {practice_units}")
else:
    print("practice_units already includes physics-calculations")

print("\nDone! View at: https://www.studyvault.co.uk/practice/science/physics-calculations/1")
