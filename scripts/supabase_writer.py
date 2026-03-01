"""
Supabase Writer — Pipeline adapter for writing content to Supabase.

Provides the same interface as writing to HTML files, but targets the database.
Used by generation scripts (narration, diagrams, etc.) to update lesson data.

Usage:
    from supabase_writer import SupabaseWriter

    writer = SupabaseWriter()
    writer.upsert_lesson(unit_id, lesson_number, { ... })
    writer.update_narration(lesson_id, manifest)
    writer.update_diagrams(lesson_id, diagrams_list)
    writer.mark_for_review(lesson_id)

Env vars required:
    SUPABASE_URL            (project URL)
    SUPABASE_SERVICE_KEY    (service role key — bypasses RLS)
"""

import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from supabase import create_client


class SupabaseWriter:
    """Pipeline adapter for writing content to Supabase."""

    def __init__(self, url=None, key=None):
        self.url = url or os.environ.get("SUPABASE_URL")
        self.key = key or os.environ.get("SUPABASE_SERVICE_KEY")

        if not self.url or not self.key:
            raise ValueError(
                "Missing SUPABASE_URL or SUPABASE_SERVICE_KEY environment variables."
            )

        self.client = create_client(self.url, self.key)

    # ---- Lookup helpers ----

    def get_school_id(self, slug):
        """Get school ID by slug."""
        result = self.client.table("schools").select("id").eq("slug", slug).single().execute()
        return result.data["id"]

    def get_subject_id(self, school_id, slug):
        """Get subject ID by school and slug."""
        result = (
            self.client.table("subjects")
            .select("id")
            .eq("school_id", school_id)
            .eq("slug", slug)
            .single()
            .execute()
        )
        return result.data["id"]

    def get_unit_id(self, subject_id, slug):
        """Get unit ID by subject and slug."""
        result = (
            self.client.table("units")
            .select("id")
            .eq("subject_id", subject_id)
            .eq("slug", slug)
            .single()
            .execute()
        )
        return result.data["id"]

    def get_lesson_id(self, unit_id, lesson_number):
        """Get lesson ID by unit and number."""
        result = (
            self.client.table("lessons")
            .select("id")
            .eq("unit_id", unit_id)
            .eq("lesson_number", lesson_number)
            .single()
            .execute()
        )
        return result.data["id"]

    def find_lesson(self, subject_slug, unit_slug, lesson_number, school_slug="unity-college"):
        """Find a lesson ID from subject/unit/number slugs."""
        school_id = self.get_school_id(school_slug)
        subject_id = self.get_subject_id(school_id, subject_slug)
        unit_id = self.get_unit_id(subject_id, unit_slug)
        return self.get_lesson_id(unit_id, lesson_number)

    # ---- Content operations ----

    def upsert_lesson(self, unit_id, lesson_number, data):
        """Create or update a lesson.

        Args:
            unit_id: UUID of the parent unit
            lesson_number: integer lesson number
            data: dict with any lesson column values, e.g.:
                {
                    'title': '...',
                    'content_html': '...',
                    'exam_tip_html': '...',
                    'conclusion_html': '...',
                    'practice_questions': [...],
                    'knowledge_checks': [...],
                    'glossary_terms': [...],
                    'related_media': [...],
                }
        """
        record = {
            "unit_id": unit_id,
            "lesson_number": lesson_number,
            "slug": f"lesson-{lesson_number:02d}",
            **data,
        }

        result = self.client.table("lessons").upsert(
            record, on_conflict="unit_id,lesson_number"
        ).execute()

        return result.data[0]["id"]

    def update_hero_image(self, lesson_id, url, alt=None, position=None, caption=None):
        """Update hero image for a lesson."""
        updates = {"hero_image_url": url}
        if alt is not None:
            updates["hero_image_alt"] = alt
        if position is not None:
            updates["hero_image_position"] = position
        if caption is not None:
            updates["hero_image_caption"] = caption

        self.client.table("lessons").update(updates).eq("id", lesson_id).execute()

    def update_narration(self, lesson_id, manifest):
        """Update narration manifest for a lesson.

        Args:
            lesson_id: UUID
            manifest: list of { id, src, duration } dicts
        """
        self.client.table("lessons").update(
            {"narration_manifest": manifest}
        ).eq("id", lesson_id).execute()

    def update_diagrams(self, lesson_id, diagrams):
        """Update diagram list for a lesson.

        Args:
            lesson_id: UUID
            diagrams: list of { url, alt } dicts
        """
        self.client.table("lessons").update(
            {"diagrams": diagrams}
        ).eq("id", lesson_id).execute()

    def update_questions(self, lesson_id, practice_questions=None, knowledge_checks=None):
        """Update questions for a lesson."""
        updates = {}
        if practice_questions is not None:
            updates["practice_questions"] = practice_questions
        if knowledge_checks is not None:
            updates["knowledge_checks"] = knowledge_checks
        if updates:
            self.client.table("lessons").update(updates).eq("id", lesson_id).execute()

    def update_related_media(self, lesson_id, media):
        """Update related media for a lesson.

        Args:
            lesson_id: UUID
            media: list of { category, emoji, items: [{ title, url, description }] }
        """
        self.client.table("lessons").update(
            {"related_media": media}
        ).eq("id", lesson_id).execute()

    def update_youtube(self, lesson_id, video_id):
        """Set YouTube video ID for a lesson."""
        self.client.table("lessons").update(
            {"youtube_video_id": video_id}
        ).eq("id", lesson_id).execute()

    def update_content_html(self, lesson_id, content_html):
        """Update the main article HTML for a lesson."""
        self.client.table("lessons").update(
            {"content_html": content_html}
        ).eq("id", lesson_id).execute()

    # ---- Status operations ----

    def mark_for_review(self, lesson_id, changed_by=None):
        """Move a lesson to 'review' status."""
        self.client.table("lessons").update(
            {"status": "review"}
        ).eq("id", lesson_id).execute()

        # Log the transition
        log = {
            "lesson_id": lesson_id,
            "from_status": "draft",
            "to_status": "review",
            "notes": "Marked for review by pipeline",
        }
        if changed_by:
            log["changed_by"] = changed_by
        self.client.table("content_pipeline_logs").insert(log).execute()

    def approve(self, lesson_id, changed_by=None):
        """Move a lesson to 'live' status."""
        self.client.table("lessons").update(
            {"status": "live", "approved_at": "now()"}
        ).eq("id", lesson_id).execute()

        log = {
            "lesson_id": lesson_id,
            "from_status": "review",
            "to_status": "live",
            "notes": "Approved by pipeline",
        }
        if changed_by:
            log["changed_by"] = changed_by
        self.client.table("content_pipeline_logs").insert(log).execute()

    def set_status(self, lesson_id, status, notes=None, changed_by=None):
        """Set arbitrary status on a lesson."""
        updates = {"status": status}
        if status == "live":
            updates["approved_at"] = "now()"

        self.client.table("lessons").update(updates).eq("id", lesson_id).execute()

        if notes or changed_by:
            log = {
                "lesson_id": lesson_id,
                "to_status": status,
                "notes": notes,
            }
            if changed_by:
                log["changed_by"] = changed_by
            self.client.table("content_pipeline_logs").insert(log).execute()

    # ---- School / Subject / Unit creation ----

    def upsert_school(self, data):
        """Create or update a school. Returns school ID."""
        result = self.client.table("schools").upsert(
            data, on_conflict="slug"
        ).execute()
        return result.data[0]["id"]

    def upsert_subject(self, data):
        """Create or update a subject. Returns subject ID."""
        result = self.client.table("subjects").upsert(
            data, on_conflict="school_id,slug"
        ).execute()
        return result.data[0]["id"]

    def upsert_unit(self, data):
        """Create or update a unit. Returns unit ID."""
        result = self.client.table("units").upsert(
            data, on_conflict="subject_id,slug"
        ).execute()
        return result.data[0]["id"]

    def upsert_guide(self, data):
        """Create or update a guide page. Returns guide ID."""
        result = self.client.table("guide_pages").upsert(
            data, on_conflict="subject_id,guide_type,slug"
        ).execute()
        return result.data[0]["id"]
