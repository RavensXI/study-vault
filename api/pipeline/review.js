const { requireTeacher } = require('./_lib/auth');
const { supabase } = require('./_lib/supabase');

module.exports = async function handler(req, res) {
  const auth = await requireTeacher(req, res);
  if (!auth) return;

  const isAdmin = auth.profile.role === 'platform_admin';
  const isTeacher = auth.profile.role === 'teacher' || auth.profile.role === 'school_admin';

  // GET — fetch review queue, counts, and subject summary
  if (req.method === 'GET') {
    const { status, subject_id, lessons_only } = req.query;

    // Fast path: if lessons_only=1, skip the expensive summary queries
    let subjects = [];
    let counts = {};
    let subjectSummary = [];

    if (!lessons_only) {
      // Fetch all subjects (for filter dropdown + summary)
      let subjectsQuery = supabase
        .from('subjects')
        .select('id, slug, name, school_id, schools(name)')
        .order('name');

      // Teachers only see their school's subjects + generic
      if (isTeacher && !isAdmin) {
        const { data: teacherSubjects } = await supabase
          .from('teacher_subjects')
          .select('subject_id')
          .eq('teacher_id', auth.profile.id || auth.user.id);

        const teacherSubjectIds = (teacherSubjects || []).map(ts => ts.subject_id);

        if (teacherSubjectIds.length > 0) {
          subjectsQuery = subjectsQuery.in('id', teacherSubjectIds);
        } else if (auth.profile.school_id) {
          subjectsQuery = subjectsQuery.eq('school_id', auth.profile.school_id);
        }
      }

      const subjectsResult = await subjectsQuery;
      subjects = subjectsResult.data || [];
      const subjectIds = subjects.map(s => s.id);

      // Get unit IDs for scoping (if not admin)
      let scopedUnitIds = null;
      if (!isAdmin && subjectIds.length > 0) {
        const { data: scopedUnits } = await supabase
          .from('units')
          .select('id')
          .in('subject_id', subjectIds);
        scopedUnitIds = (scopedUnits || []).map(u => u.id);
      }

      // Fetch counts by status (scoped to visible subjects)
      const statuses = ['pending_review', 'ready_for_teacher', 'publishing', 'awaiting_qa', 'live', 'draft', 'review', 'approved'];
      for (const s of statuses) {
        let countQuery = supabase
          .from('lessons')
          .select('id', { count: 'exact', head: true })
          .eq('status', s);

        if (scopedUnitIds && scopedUnitIds.length > 0) {
          countQuery = countQuery.in('unit_id', scopedUnitIds);
        }

        const { count } = await countQuery;
        counts[s] = count || 0;
      }

      // Fetch per-subject counts for summary cards
      for (const subject of subjects) {
        const { data: unitIds } = await supabase
          .from('units')
          .select('id')
          .eq('subject_id', subject.id);

        const uids = (unitIds || []).map(u => u.id);
        if (uids.length === 0) continue;

        const summary = { id: subject.id, slug: subject.slug, name: subject.name, school_id: subject.school_id };
        for (const s of ['pending_review', 'ready_for_teacher', 'publishing', 'awaiting_qa', 'live']) {
          const { count } = await supabase
            .from('lessons')
            .select('id', { count: 'exact', head: true })
            .eq('status', s)
            .in('unit_id', uids);
          summary[s] = count || 0;
        }
        if (summary.pending_review + summary.ready_for_teacher + summary.publishing + summary.awaiting_qa + summary.live > 0) {
          subjectSummary.push(summary);
        }
      }
    }

    // Fetch lessons for the requested status filter
    let query = supabase
      .from('lessons')
      .select('id, lesson_number, slug, title, status, updated_at, reviewed_at, published_at, hero_image_url, hero_image_position, rejection_notes, unit_id, units!inner(name, slug, subject_id, subjects!inner(id, name, slug, school_id))')
      .order('lesson_number', { ascending: true })
      .limit(200);

    // Apply status filter
    if (status && status !== 'all') {
      query = query.eq('status', status);
    }

    // Apply subject filter
    if (subject_id) {
      const { data: filteredUnits } = await supabase
        .from('units')
        .select('id')
        .eq('subject_id', subject_id);

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

    // ---- approve: pending_review → ready_for_teacher (admin only) ----
    if (action === 'approve') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can approve content' });
      }

      const ids = lesson_ids || (lesson_id ? [lesson_id] : []);
      if (ids.length === 0) {
        return res.status(400).json({ error: 'Missing lesson_ids or lesson_id' });
      }

      const { data, error } = await supabase
        .from('lessons')
        .update({
          status: 'ready_for_teacher',
          reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
          reviewed_at: now
        })
        .in('id', ids)
        .eq('status', 'pending_review')
        .select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to approve', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'pending_review',
          to_status: 'ready_for_teacher',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'Approved via review dashboard'
        });
      }

      return res.status(200).json({ ok: true, updated: (data || []).length });
    }

    // ---- approve_all: approve all pending_review for a subject (admin only) ----
    if (action === 'approve_all') {
      if (!isAdmin) {
        return res.status(403).json({ error: 'Only admins can approve content' });
      }

      let approveQuery = supabase
        .from('lessons')
        .update({
          status: 'ready_for_teacher',
          reviewed_by: changedBy !== 'platform_admin' ? changedBy : null,
          reviewed_at: now
        })
        .eq('status', 'pending_review');

      // Scope to subject if provided
      if (subject_id) {
        const { data: subjectUnits } = await supabase
          .from('units')
          .select('id')
          .eq('subject_id', subject_id);

        const unitIds = (subjectUnits || []).map(u => u.id);
        if (unitIds.length > 0) {
          approveQuery = approveQuery.in('unit_id', unitIds);
        }
      }

      const { data, error } = await approveQuery.select('id');

      if (error) {
        return res.status(500).json({ error: 'Failed to bulk approve', detail: error.message });
      }

      // Log transitions
      for (const row of (data || [])) {
        await supabase.from('content_pipeline_logs').insert({
          lesson_id: row.id,
          from_status: 'pending_review',
          to_status: 'ready_for_teacher',
          changed_by: changedBy !== 'platform_admin' ? changedBy : null,
          notes: notes || 'Bulk approved via review dashboard'
        });
      }

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
