"""Pipeline helpers — query pending lessons, mark completion, progress summaries.

Shared by all asset scripts (narration, diagrams, heroes, media).
"""


def get_pending_lessons(sb, job_id, asset_flag, specific_lessons=None):
    """Query pipeline_steps for lessons where the given asset flag is false.

    Args:
        sb: Supabase client.
        job_id: Upload job UUID.
        asset_flag: Column name like 'narration_done', 'diagrams_done', 'hero_done'.
        specific_lessons: Optional list of lesson numbers to filter to.

    Returns:
        List of pipeline_step dicts (joined with lesson data).
    """
    query = (
        sb.table("pipeline_steps")
        .select("*, lessons(id, title, content_html, exam_tip_html, conclusion_html, hero_image_url, diagrams, narration_manifest)")
        .eq("job_id", job_id)
        .eq("content_done", True)
        .eq(asset_flag, False)
        .order("unit_slug")
        .order("lesson_number")
    )

    if specific_lessons:
        query = query.in_("lesson_number", specific_lessons)

    result = query.execute()
    return result.data or []


def mark_asset_done(sb, step_id, asset_flag):
    """Set an asset flag to true on a pipeline_step row.

    Args:
        sb: Supabase client.
        step_id: pipeline_steps.id UUID.
        asset_flag: Column name like 'narration_done'.
    """
    sb.table("pipeline_steps").update({
        asset_flag: True,
        "last_error": None,
    }).eq("id", step_id).execute()


def mark_asset_error(sb, step_id, error_message):
    """Record an error on a pipeline_step row and increment retry_count.

    Args:
        sb: Supabase client.
        step_id: pipeline_steps.id UUID.
        error_message: Error description string.
    """
    step = sb.table("pipeline_steps").select("retry_count").eq("id", step_id).single().execute()
    current = step.data.get("retry_count", 0) if step.data else 0
    sb.table("pipeline_steps").update({
        "last_error": error_message[:500],
        "retry_count": current + 1,
    }).eq("id", step_id).execute()


def get_job_subject_slug(sb, job_id):
    """Get the subject_slug for a job (from upload_jobs or first pipeline_step)."""
    job = sb.table("upload_jobs").select("subject_slug, subject_config").eq("id", job_id).single().execute()
    if job.data:
        slug = job.data.get("subject_slug")
        if slug:
            return slug
        config = job.data.get("subject_config") or {}
        name = config.get("subject_name", "")
        if name:
            return name.lower().replace(" ", "-")

    # Fallback: check pipeline_steps.subject_slug
    step = sb.table("pipeline_steps").select("subject_slug").eq("job_id", job_id).limit(1).execute()
    if step.data and step.data[0].get("subject_slug"):
        return step.data[0]["subject_slug"]

    return "unknown"


def update_job_phase(sb, job_id, phase):
    """Update the current_phase on an upload_job."""
    sb.table("upload_jobs").update({"current_phase": phase}).eq("id", job_id).execute()


def get_progress_summary(sb, job_id):
    """Return a dict summarising asset completion for a job.

    Returns:
        {
            'total': int,
            'content': int, 'diagrams': int, 'heroes': int,
            'narration': int, 'media': int, 'errors': int,
        }
    """
    steps = (
        sb.table("pipeline_steps")
        .select("content_done, diagrams_done, hero_done, narration_done, media_done, last_error")
        .eq("job_id", job_id)
        .execute()
    )

    data = steps.data or []
    return {
        "total": len(data),
        "content": sum(1 for s in data if s["content_done"]),
        "diagrams": sum(1 for s in data if s["diagrams_done"]),
        "heroes": sum(1 for s in data if s["hero_done"]),
        "narration": sum(1 for s in data if s["narration_done"]),
        "media": sum(1 for s in data if s["media_done"]),
        "errors": sum(1 for s in data if s.get("last_error")),
    }
