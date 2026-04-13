#!/usr/bin/env python3
"""Insert all science practice units and lessons into Supabase.

Creates 4 new units:
  - Combined Science: Physics Calculations (8), Chemistry Calculations (4), Biology Data Skills (3)
  - Separate Sciences: Higher Calculations (6)

Run: python -m scripts.science-practice.insert_science_practice
"""

import json
import os
import sys
from scripts.lib.supabase_client import get_client

sb = get_client()

# ── Configuration ────────────────────────────────────────────────────────

UNITS_CONFIG = {
    "combined": {
        "subject_slug": "science",
        "units": [
            {
                "slug": "physics-calculations",
                "name": "Physics Calculations",
                "subtitle": "Drill every recall equation for the Physics papers",
                "body_class": "unit-science-phys-calc",
                "accent": "#2563eb",
                "accent_light": "#2563eb22",
                "accent_badge": "#2563eb33",
                "sort_order": 7,
                "lesson_count": 8,
                "json_file": "combined_phys_calc.json"
            },
            {
                "slug": "chemistry-calculations",
                "name": "Chemistry Calculations",
                "subtitle": "Master moles, Mr, bond energies and rates",
                "body_class": "unit-science-chem-calc",
                "accent": "#dc2626",
                "accent_light": "#dc262622",
                "accent_badge": "#dc262633",
                "sort_order": 8,
                "lesson_count": 4,
                "json_file": "combined_chem_calc.json"
            },
            {
                "slug": "biology-data-skills",
                "name": "Biology Data Skills",
                "subtitle": "Magnification, genetics and sampling calculations",
                "body_class": "unit-science-bio-data",
                "accent": "#16a34a",
                "accent_light": "#16a34a22",
                "accent_badge": "#16a34a33",
                "sort_order": 9,
                "lesson_count": 3,
                "json_file": "combined_bio_data.json"
            }
        ]
    },
    "separate": {
        "subject_slug": "separate-sciences",
        "units": [
            {
                "slug": "higher-calculations",
                "name": "Higher Calculations",
                "subtitle": "Titrations, moments, pressure, transformers and more",
                "body_class": "unit-sepsci-higher-calc",
                "accent": "#7c3aed",
                "accent_light": "#7c3aed22",
                "accent_badge": "#7c3aed33",
                "sort_order": 4,
                "lesson_count": 6,
                "json_file": "separate_higher_calc.json"
            }
        ]
    }
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_subject(slug):
    """Find the Unity (school-specific) subject by slug."""
    result = sb.table("subjects").select("id, settings").eq("slug", slug).not_.is_("school_id", "null").execute()
    if not result.data:
        print(f"  ERROR: Could not find Unity subject '{slug}'")
        return None
    return result.data[0]


def ensure_unit(subject_id, unit_config):
    """Create unit if it doesn't exist, return unit ID."""
    existing = sb.table("units").select("id").eq("subject_id", subject_id).eq("slug", unit_config["slug"]).execute()
    if existing.data:
        unit_id = existing.data[0]["id"]
        print(f"  Unit '{unit_config['name']}' already exists: {unit_id[:8]}...")
        return unit_id

    result = sb.table("units").insert({
        "subject_id": subject_id,
        "slug": unit_config["slug"],
        "name": unit_config["name"],
        "subtitle": unit_config["subtitle"],
        "body_class": unit_config["body_class"],
        "accent": unit_config["accent"],
        "accent_light": unit_config["accent_light"],
        "accent_badge": unit_config["accent_badge"],
        "sort_order": unit_config["sort_order"],
        "lesson_count": unit_config["lesson_count"]
    }).execute()
    unit_id = result.data[0]["id"]
    print(f"  Created unit '{unit_config['name']}': {unit_id[:8]}...")
    return unit_id


def insert_lessons(unit_id, lessons):
    """Insert or update lessons for a unit."""
    success = 0
    for lesson in lessons:
        ln = lesson["lesson_number"]

        # Check if lesson already exists
        existing = sb.table("lessons").select("id").eq("unit_id", unit_id).eq("lesson_number", ln).execute()

        record = {
            "unit_id": unit_id,
            "lesson_number": ln,
            "slug": lesson["slug"],
            "title": lesson["title"],
            "description": lesson.get("description", ""),
            "practice_data": lesson["practice_data"],
            "status": "live"
        }

        if existing.data:
            lid = existing.data[0]["id"]
            sb.table("lessons").update(record).eq("id", lid).execute()
            print(f"    Updated L{ln:02d}: {lesson['title']}")
        else:
            result = sb.table("lessons").insert(record).execute()
            print(f"    Inserted L{ln:02d}: {lesson['title']}")
        success += 1

    return success


def update_practice_units(subject_id, unit_slugs):
    """Add unit slugs to subjects.settings.practice_units."""
    subj = sb.table("subjects").select("settings").eq("id", subject_id).single().execute()
    settings = subj.data["settings"] or {}
    practice_units = settings.get("practice_units", [])

    added = []
    for slug in unit_slugs:
        if slug not in practice_units:
            practice_units.append(slug)
            added.append(slug)

    if added:
        settings["practice_units"] = practice_units
        sb.table("subjects").update({"settings": settings}).eq("id", subject_id).execute()
        print(f"  Updated practice_units: added {added}")
    else:
        print(f"  practice_units already up to date")


def main():
    total_lessons = 0

    for group_name, group_config in UNITS_CONFIG.items():
        print(f"\n{'='*60}")
        print(f"Processing: {group_name} ({group_config['subject_slug']})")
        print(f"{'='*60}")

        subj = find_subject(group_config["subject_slug"])
        if not subj:
            continue

        subject_id = subj["id"]
        unit_slugs = []

        for unit_config in group_config["units"]:
            print(f"\n  --- {unit_config['name']} ---")

            # Load JSON
            json_path = os.path.join(SCRIPT_DIR, unit_config["json_file"])
            if not os.path.exists(json_path):
                print(f"  SKIPPING: {unit_config['json_file']} not found")
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                lessons = json.load(f)

            print(f"  Loaded {len(lessons)} lessons from {unit_config['json_file']}")

            # Create unit
            unit_id = ensure_unit(subject_id, unit_config)
            unit_slugs.append(unit_config["slug"])

            # Insert lessons
            count = insert_lessons(unit_id, lessons)
            total_lessons += count

        # Update subject settings
        update_practice_units(subject_id, unit_slugs)

    print(f"\n{'='*60}")
    print(f"Done! Inserted/updated {total_lessons} practice lessons across 4 units.")
    print(f"{'='*60}")
    print(f"\nView at:")
    print(f"  https://www.studyvault.co.uk/browse/science")
    print(f"  https://www.studyvault.co.uk/browse/separate-sciences")


if __name__ == "__main__":
    main()
