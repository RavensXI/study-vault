const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');
const { forgetSourceIfPublished } = require('./_lib/forget-source');

module.exports = async function handler(req, res) {
  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const isAdmin = auth.profile.role === 'platform_admin';
  const isTeacher = auth.profile.role === 'teacher' || auth.profile.role === 'school_admin';

  /**
   * The subjects this person may see. null = unrestricted (platform_admin).
   *
   * This used to be computed inline, INSIDE the block that builds the filter
   * dropdown — so the dropdown was scoped and the lesson list underneath it was
   * not. A history teacher at Unity opening the review queue with no filter set
   * saw Music AQA's pending lessons, and a teacher at one school would equally
   * have seen another school's bespoke content. Scoping the control and not the
   * data is the whole bug in one sentence.
   *
   * Now computed once and applied to both, so the list cannot show anything the
   * dropdown would not offer.
   */
  async function permittedSubjectIds() {
    if (isAdmin) return null;

    const { data: ts } = await supabase
      .from('teacher_subjects')
      .select('subject_id')
      .eq('teacher_id', auth.profile.id || auth.user.id);

    const assigned = (ts || []).map(function (t) { return t.subject_id; });
    if (assigned.length) return assigned;

    /* No explicit assignment: fall back to their school's own subjects. Note
       this deliberately excludes generic (school_id NULL) content, matching
       what the dropdown has always done — the comment above it claimed
       "+ generic", but the query never included it. Kept as-is rather than
       widened, because widening access is not a thing to do as a side effect of
       fixing a leak. */
    if (auth.profile.school_id) {
      const { data: own } = await supabase
        .from('subjects').select('id').eq('school_id', auth.profile.school_id);
      return (own || []).map(function (s) { return s.id; });
    }
    return [];      // a teacher with no subjects and no school sees nothing
  }

  // GET — fetch review queue, counts, and subject summary
  if (req.method === 'GET') {
    const { status, subject_id, lessons_only } = req.query;

    /* Computed BEFORE the lessons_only fast path, because the fast path is
       exactly the request the review page makes when it refreshes the list —
       and it previously skipped every line of scoping. */
    const allowedSubjectIds = await permittedSubjectIds();

    // Fast path: if lessons_only=1, skip the expensive summary queries
    let subjects = [];
    let counts = {};
    let subjectSummary = [];

    if (!lessons_only) {
      // Fetch all subjects (for filter dropdown + summary). Archived subjects
      // (retired quals, e.g. Eduqas French/Spanish) keep their lessons in the
      // DB but must not clutter the review queue.
      let subjectsQuery = supabase
        .from('subjects')
        .select('id, slug, name, school_id, schools(name)')
        .neq('status', 'archived')
        .order('name');

      // Same permitted set the lesson list below is constrained to.
      if (allowedSubjectIds) {
        subjectsQuery = subjectsQuery.in('id', allowedSubjectIds.length ? allowedSubjectIds
                                                                        : ['00000000-0000-0000-0000-000000000000']);
      }

      const subjectsResult = await subjectsQuery;
      subjects = subjectsResult.data || [];
      const subjectIds = new Set(subjects.map(s => s.id));

      // --- Aggregate all status counts in JS instead of ~6 count queries per
      // subject. With ~90+ subjects the old per-subject loop fired 550+ serial
      // round-trips on every fresh load. We now pull units + lessons in a
      // handful of queries and bucket in memory (same pattern as build-status).

      // Map every unit to its subject (slim columns). Scope to visible subjects
      // so a teacher's payload stays small.
      let unitsQuery = supabase.from('units').select('id, subject_id');
      if (!isAdmin && subjectIds.size > 0) {
        unitsQuery = unitsQuery.in('subject_id', Array.from(subjectIds));
      }
      const { data: allUnits } = await unitsQuery;
      const unitToSubject = {};
      (allUnits || []).forEach(u => { unitToSubject[u.id] = u.subject_id; });

      // Pull all lessons (slim) — paginate past the 1000-row default cap.
      const allLessons = [];
      let page = 0;
      while (true) {
        const { data: chunk, error: chunkErr } = await supabase
          .from('lessons')
          .select('id, unit_id, status')
          .range(page * 1000, page * 1000 + 999);
        if (chunkErr) break;
        allLessons.push(...(chunk || []));
        if (!chunk || chunk.length < 1000) break;
        page++;
        if (page > 20) break; // safety
      }

      // Bucket counts. Global `counts` is scoped to visible subjects (for admin
      // that's everything). Per-subject summary mirrors the old shape.
      const summaryStatuses = ['pending_review', 'ready_for_teacher', 'publishing', 'awaiting_qa', 'live'];
      const perSubject = {};
      for (const L of allLessons) {
        const sid = unitToSubject[L.unit_id];
        if (sid === undefined) continue;          // unit not in scope / orphan lesson
        if (!subjectIds.has(sid)) continue;       // out of scope OR archived subject
        counts[L.status] = (counts[L.status] || 0) + 1;
        if (!perSubject[sid]) perSubject[sid] = {};
        perSubject[sid][L.status] = (perSubject[sid][L.status] || 0) + 1;
      }

      for (const subject of subjects) {
        const ps = perSubject[subject.id];
        if (!ps) continue;
        const summary = { id: subject.id, slug: subject.slug, name: subject.name, school_id: subject.school_id };
        let total = 0;
        for (const s of summaryStatuses) {
          summary[s] = ps[s] || 0;
          total += summary[s];
        }
        if (total > 0) subjectSummary.push(summary);
      }
    }

    // Fetch lessons for the requested status filter
    let query = supabase
      .from('lessons')
      .select('id, lesson_number, slug, title, status, updated_at, reviewed_at, published_at, hero_image_url, hero_image_position, rejection_notes, unit_id, units!inner(name, slug, subject_id, subjects!inner(id, name, slug, school_id, settings))')
      .neq('units.subjects.status', 'archived')
      .order('lesson_number', { ascending: true })
      .limit(200);

    // Apply status filter
    if (status && status !== 'all') {
      query = query.eq('status', status);
    }

    /* THE FIX. Constrain the list to the permitted subjects before any
       user-supplied filter is considered. A filter the client chooses is a
       convenience; this is the boundary. */
    if (allowedSubjectIds) {
      if (!allowedSubjectIds.length) {
        return res.status(200).json({ lessons: [], counts, subjects: subjects || [], subjectSummary });
      }
      const { data: allowedUnits } = await supabase
        .from('units').select('id').in('subject_id', allowedSubjectIds);
      const allowedUnitIds = (allowedUnits || []).map(function (u) { return u.id; });
      if (!allowedUnitIds.length) {
        return res.status(200).json({ lessons: [], counts, subjects: subjects || [], subjectSummary });
      }
      query = query.in('unit_id', allowedUnitIds);
    }

    // Apply subject filter
    if (subject_id) {
      const { data: filteredUnits } = await supabase
        .from('units')
        .select('id')
        .eq('subject_id', subject_id);

      /* and the subject they asked for must be one they may see, or the
         filter becomes the way round the boundary */
      if (allowedSubjectIds && allowedSubjectIds.indexOf(subject_id) === -1) {
        return res.status(403).json({ error: 'That subject is not yours to review.' });
      }

      const filteredUnitIds = (filteredUnits || []).map(u => u.id);
      if (filteredUnitIds.length > 0) {
        query = query.in('unit_id', filteredUnitIds);
      } else {
        return res.status(200).json({ lessons: [], counts, subjects: subjects || [], subjectSummary });
      }
    }

    const { data: lessons, error } = await query;
    if (error) {
      return res.status(500).json({ error: 'Failed to fetch lessons', detail: error.message });
    }

    return res.status(200).json({
      lessons: lessons || [],
      counts,
      subjects: subjects || [],
      subjectSummary
    });
  }

  // POST — status transition actions
  if (req.method === 'POST') {
    const { action, lesson_ids, lesson_id, subject_id, notes } = req.body;

    if (!action) {
      return res.status(400).json({ error: 'Missing action' });
    }

    const changedBy = auth.profile.id || auth.user.id;
    const now = new Date().toISOString();

    // ---- approve: pending_review → live (free-tier) or ready_for_teacher (school content) ----
    if (action === 'approve') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can approve content' });
      }

      const ids = lesson_ids || (lesson_id ? [lesson_id] : []);
      if (ids.length === 0) {
        return res.status(400).json({ error: 'Missing lesson_ids or lesson_id' });
      }

      // Look up each lesson's subject school_id to decide destination status.
      // Free-tier (school_id NULL) → admin approval IS the publish step → 'live'.
      // School-bespoke (school_id set) → still needs teacher review → 'ready_for_teacher'.
      const { data: ctx } = await supabase
        .from('lessons')
        .select('id, units!inner(subjects!inner(school_id))')
        .in('id', ids);

      const freeTierIds = [];
      const schoolIds = [];
      for (const row of (ctx || [])) {
        if (row.units.subjects.school_id == null) freeTierIds.push(row.id);
        else schoolIds.push(row.id);
      }

      let updatedCount = 0;
      const transitions = [];

      if (freeTierIds.length) {
        const { data, error } = await supabase
          .from('lessons')
          .update({
            status: 'live',
            reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
            reviewed_at: now,
            published_by: changedBy !== 'platform_admin' ? changedBy : null,
            published_at: now
          })
          .in('id', freeTierIds)
          .eq('status', 'pending_review')
          .select('id');
        if (error) return res.status(500).json({ error: 'Failed to approve free-tier', detail: error.message });
        updatedCount += (data || []).length;
        for (const row of (data || [])) transitions.push({ id: row.id, to: 'live' });
      }

      if (schoolIds.length) {
        const { data, error } = await supabase
          .from('lessons')
          .update({
            status: 'ready_for_teacher',
            reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
            reviewed_at: now
          })
          .in('id', schoolIds)
          .eq('status', 'pending_review')
          .select('id');
        if (error) return res.status(500).json({ error: 'Failed to approve school content', detail: error.message });
        updatedCount += (data || []).length;
        for (const row of (data || [])) transitions.push({ id: row.id, to: 'ready_for_teacher' });
      }

      // Log transitions
      for (const t of transitions) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: t.id,
          from_status: 'pending_review',
          to_status: t.to,
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || (t.to === 'live' ? 'Free-tier: approved straight to live' : 'Approved via review dashboard')
        });
      }

      /* Source material has done its job once the lessons are live.
         See _lib/forget-source.js: publish rather than build-complete, because
         the gap between those two is exactly where re-runs happen.
         Only freeTierIds went live here — schoolIds moved to
         ready_for_teacher, which is a step BEFORE the department has seen
         them, so their source is very much still needed. */
      await forgetSourceIfPublished(freeTierIds);

      return res.status(200).json({ ok: true, updated: updatedCount });
    }

    // ---- approve_all: approve all pending_review for a subject (admin only).
    // Free-tier subjects (school_id NULL) go straight to 'live'.
    // School subjects go to 'ready_for_teacher' for the teacher to publish.
    if (action === 'approve_all') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can approve content' });
      }

      // Determine target status by subject school_id
      let isFreeTierSubject = false;
      if (subject_id) {
        const { data: subj } = await supabase
          .from('subjects')
          .select('school_id')
          .eq('id', subject_id)
          .single();
        isFreeTierSubject = subj && subj.school_id == null;
      }

      // If no subject_id, we have to split — fetch all pending lessons and bucket by school_id
      let pendingIds = [];
      if (subject_id) {
        const { data: subjectUnits } = await supabase
          .from('units').select('id').eq('subject_id', subject_id);
        const unitIds = (subjectUnits || []).map(u => u.id);
        if (unitIds.length > 0) {
          const { data: pl } = await supabase
            .from('lessons').select('id').eq('status', 'pending_review').in('unit_id', unitIds);
          pendingIds = (pl || []).map(l => l.id);
        }
      } else {
        const { data: pl } = await supabase
          .from('lessons')
          .select('id, units!inner(subjects!inner(school_id))')
          .eq('status', 'pending_review');
        // Bucket by school_id NULL vs set
        const freeIds = [];
        const schoolIds = [];
        for (const r of (pl || [])) {
          if (r.units.subjects.school_id == null) freeIds.push(r.id);
          else schoolIds.push(r.id);
        }
        let total = 0;
        if (freeIds.length) {
          const { data, error } = await supabase
            .from('lessons')
            .update({
              status: 'live',
              reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
              reviewed_at: now,
              published_by: changedBy !== 'platform_admin' ? changedBy : null,
              published_at: now
            })
            .in('id', freeIds)
            .eq('status', 'pending_review')
            .select('id');
          if (error) return res.status(500).json({ error: 'Failed bulk free-tier approve', detail: error.message });
          for (const row of (data || [])) {
            await supabase.from('content_pipeline_logs').insert({
              lesson_id: row.id, from_status: 'pending_review', to_status: 'live',
              changed_by: changedBy !== 'platform_admin' ? changedBy : null,
              notes: notes || 'Free-tier bulk approve → live'
            });
          }
          total += (data || []).length;
        }
        if (schoolIds.length) {
          const { data, error } = await supabase
            .from('lessons')
            .update({
              status: 'ready_for_teacher',
              reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
              reviewed_at: now
            })
            .in('id', schoolIds)
            .eq('status', 'pending_review')
            .select('id');
          if (error) return res.status(500).json({ error: 'Failed bulk school approve', detail: error.message });
          for (const row of (data || [])) {
            await supabase.from('content_pipeline_logs').insert({
              lesson_id: row.id, from_status: 'pending_review', to_status: 'ready_for_teacher',
              changed_by: changedBy !== 'platform_admin' ? changedBy : null,
              notes: notes || 'Bulk approved via review dashboard'
            });
          }
          total += (data || []).length;
        }
        await forgetSourceIfPublished(freeIds);

        return res.status(200).json({ ok: true, approved: total });
      }

      if (pendingIds.length === 0) {
        return res.status(200).json({ ok: true, approved: 0 });
      }

      const targetStatus = isFreeTierSubject ? 'live' : 'ready_for_teacher';
      const updatePayload = isFreeTierSubject
        ? {
            status: 'live',
            reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
            reviewed_at: now,
            published_by: changedBy !== 'platform_admin' ? changedBy : null,
            published_at: now
          }
        : {
            status: 'ready_for_teacher',
            reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
            reviewed_at: now
          };

      const { data, error } = await supabase
        .from('lessons')
        .update(updatePayload)
        .in('id', pendingIds)
        .eq('status', 'pending_review')
        .select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to bulk approve', detail: error.message });
      }

      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'pending_review',
          to_status: targetStatus,
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || (isFreeTierSubject ? 'Free-tier bulk approve → live' : 'Bulk approved via review dashboard')
        });
      }

      await forgetSourceIfPublished((data || []).map(function (r) { return r.id; }));

      return res.status(200).json({ ok: true, approved: (data || []).length });
    }

    // ---- publish: ready_for_teacher → live (teacher who owns subject, or admin) ----
    if (action === 'publish') {
      const ids = lesson_ids || (lesson_id ? [lesson_id] : []);
      if (ids.length === 0) {
        return res.status(400).json({ error: 'Missing lesson_ids or lesson_id' });
      }

      // If teacher (not admin), verify they own the subject
      if (isTeacher && !isAdmin) {
        const { data: lessonsToPublish } = await supabase
          .from('lessons')
          .select('id, unit_id, units!inner(subject_id)')
          .in('id', ids)
          .eq('status', 'ready_for_teacher');

        const subjectIds = [...new Set((lessonsToPublish || []).map(l => l.units.subject_id))];

        // Check teacher_subjects for each subject
        for (const sid of subjectIds) {
          const { data: perm } = await supabase
            .from('teacher_subjects')
            .select('can_publish')
            .eq('teacher_id', auth.profile.id || auth.user.id)
            .eq('subject_id', sid)
            .single();

          if (!perm || !perm.can_publish) {
            return res.status(403).json({ error: 'You do not have permission to publish content for this subject' });
          }
        }
      }

      const { data, error } = await supabase
        .from('lessons')
        .update({
          status: 'publishing',
          published_by: changedBy !== 'platform_admin' ? changedBy : null,
          published_at: now,
          enrichment_started_at: null,
          enrichment_error: null
        })
        .in('id', ids)
        .eq('status', 'ready_for_teacher')
        .select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to publish', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'ready_for_teacher',
          to_status: 'publishing',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'Submitted for publishing via review dashboard'
        });
      }

      return res.status(200).json({ ok: true, published: (data || []).length });
    }

    // ---- publish_all: publish all ready_for_teacher for a subject (or all) ----
    if (action === 'publish_all') {
      // Teachers (not admin) require subject_id and must own it
      if (isTeacher && !isAdmin) {
        if (!subject_id) {
          return res.status(400).json({ error: 'Teachers must specify subject_id for publish_all' });
        }
        const { data: perm } = await supabase
          .from('teacher_subjects')
          .select('can_publish')
          .eq('teacher_id', auth.profile.id || auth.user.id)
          .eq('subject_id', subject_id)
          .single();

        if (!perm || !perm.can_publish) {
          return res.status(403).json({ error: 'You do not have permission to publish content for this subject' });
        }
      }

      let publishQuery = supabase
        .from('lessons')
        .update({
          status: 'publishing',
          published_by: changedBy !== 'platform_admin' ? changedBy : null,
          published_at: now,
          enrichment_started_at: null,
          enrichment_error: null
        })
        .eq('status', 'ready_for_teacher');

      // Scope to subject if provided
      if (subject_id) {
        const { data: subjectUnits } = await supabase
          .from('units')
          .select('id')
          .eq('subject_id', subject_id);

        const unitIds = (subjectUnits || []).map(u => u.id);
        if (unitIds.length > 0) {
          publishQuery = publishQuery.in('unit_id', unitIds);
        }
      }

      const { data, error } = await publishQuery.select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to bulk publish', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'ready_for_teacher',
          to_status: 'publishing',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'Bulk submitted for publishing via review dashboard'
        });
      }

      return res.status(200).json({ ok: true, published: (data || []).length });
    }

    // ---- complete_enrichment: publishing → awaiting_qa (Phase 2 script or admin) ----
    if (action === 'complete_enrichment') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can complete enrichment' });
      }

      const ids = lesson_ids || (lesson_id ? [lesson_id] : []);
      if (ids.length === 0) {
        return res.status(400).json({ error: 'Missing lesson_ids or lesson_id' });
      }

      const { data, error } = await supabase
        .from('lessons')
        .update({
          status: 'awaiting_qa',
          enrichment_completed_at: now
        })
        .in('id', ids)
        .eq('status', 'publishing')
        .select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to complete enrichment', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'publishing',
          to_status: 'awaiting_qa',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'Enrichment complete — awaiting QA'
        });
      }

      return res.status(200).json({ ok: true, updated: (data || []).length });
    }

    // ---- complete_qa: awaiting_qa → live (admin only) ----
    if (action === 'complete_qa') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can complete QA' });
      }

      const ids = lesson_ids || (lesson_id ? [lesson_id] : []);
      if (ids.length === 0) {
        return res.status(400).json({ error: 'Missing lesson_ids or lesson_id' });
      }

      const { data, error } = await supabase
        .from('lessons')
        .update({
          status: 'live',
          published_at: now
        })
        .in('id', ids)
        .eq('status', 'awaiting_qa')
        .select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to complete QA', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'awaiting_qa',
          to_status: 'live',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'QA approved — lesson is now live'
        });
      }

      await forgetSourceIfPublished((data || []).map(function (r) { return r.id; }));

      return res.status(200).json({ ok: true, updated: (data || []).length });
    }

    // ---- reject: send back to pending_review with a note (admin only) ----
    if (action === 'reject') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can reject content' });
      }

      const ids = lesson_ids || (lesson_id ? [lesson_id] : []);
      if (ids.length === 0) {
        return res.status(400).json({ error: 'Missing lesson_ids or lesson_id' });
      }

      // Read current statuses before updating (for audit log)
      const { data: beforeData } = await supabase
        .from('lessons')
        .select('id, status')
        .in('id', ids);

      const beforeMap = {};
      (beforeData || []).forEach(r => { beforeMap[r.id] = r.status; });

      const { data, error } = await supabase
        .from('lessons')
        .update({
          status: 'pending_review',
          rejection_notes: notes || null,
          reviewed_by: null,
          reviewed_at: null
        })
        .in('id', ids)
        .select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to reject', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: beforeMap[row.id] || 'ready_for_teacher',
          to_status: 'pending_review',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'Rejected via review dashboard'
        });
      }

      return res.status(200).json({ ok: true, rejected: (data || []).length });
    }

    return res.status(400).json({ error: 'Unknown action: ' + action });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
