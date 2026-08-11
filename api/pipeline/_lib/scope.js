const { supabase } = require('./supabase');

/**
 * Who is allowed to write to a given piece of content.
 *
 * requireTeacher() proves WHO is calling. It does not say WHAT they may touch,
 * and the update routes were using it as if it did: they wrote by row id with
 * no owner check at all, against a service-key client that bypasses row-level
 * security. Because none of them ever loaded the row, they could not scope by
 * school even in principle. Any of the 56 staff accounts could therefore
 * overwrite any of the 4,312 shared free-tier lessons, for every school and
 * every public visitor at once.
 *
 * The rule, until copy-on-edit exists:
 *
 *   platform_admin  — may edit anything, including the shared free-tier
 *                     corpus. That is how the free tier is maintained.
 *   everyone else   — may edit only content their OWN school owns. Shared
 *                     free-tier content (subjects.school_id IS NULL) is
 *                     refused outright, because there is nowhere for a school
 *                     edit to go yet that is not everybody's copy.
 *
 * When fork-on-edit lands, the free-tier branch below becomes "make this
 * school a copy and edit that" instead of a refusal. Nothing else changes.
 */

function isPlatformAdmin(auth) {
  return !!(auth && auth.profile && auth.profile.role === 'platform_admin');
}

/** Owning school of a lesson, resolved through unit -> subject. */
async function lessonSchoolId(lessonId) {
  const { data, error } = await supabase
    .from('lessons')
    .select('id, units!inner(subjects!inner(id, school_id))')
    .eq('id', lessonId)
    .single();
  if (error || !data) return { found: false };
  return { found: true, schoolId: data.units.subjects.school_id };
}

/** Owning school of a guide page, resolved through subject. */
async function guideSchoolId(guideId) {
  const { data, error } = await supabase
    .from('guide_pages')
    .select('id, subjects!inner(id, school_id)')
    .eq('id', guideId)
    .single();
  if (error || !data) return { found: false };
  return { found: true, schoolId: data.subjects.school_id };
}

/**
 * Gate a write. Sends the error response and returns false when refused, so
 * callers stay a single `if (!(await ...)) return;`.
 */
async function requireOwnership(auth, res, kind, id) {
  if (isPlatformAdmin(auth)) return true;

  const owner = kind === 'guide' ? await guideSchoolId(id) : await lessonSchoolId(id);
  if (!owner.found) {
    res.status(404).json({ error: 'Not found' });
    return false;
  }

  if (owner.schoolId === null) {
    res.status(403).json({
      error: 'This is shared free-tier content used by every school and by the ' +
             'public site, so it cannot be edited from a school account. Ask ' +
             'StudyVault for a copy scoped to your school.'
    });
    return false;
  }

  if (!auth.profile.school_id || owner.schoolId !== auth.profile.school_id) {
    res.status(403).json({ error: 'This content belongs to another school.' });
    return false;
  }

  return true;
}

/**
 * Decide HOW a lesson write should land, rather than just whether it may.
 *
 * Returns null when refused (the response has already been sent), otherwise:
 *   { mode: 'direct' }              — write the lessons row itself. Admin, or a
 *                                     school editing content it owns outright.
 *   { mode: 'override', schoolId }  — a school editing shared free-tier
 *                                     content: copy-on-edit into
 *                                     lesson_overrides, base row untouched.
 *
 * This is where the refusal added on 11 Aug turns into a fork. Nothing else
 * about the ownership rules moved.
 */
async function resolveLessonWrite(auth, res, lessonId) {
  if (isPlatformAdmin(auth)) return { mode: 'direct' };

  const owner = await lessonSchoolId(lessonId);
  if (!owner.found) {
    res.status(404).json({ error: 'Not found' });
    return null;
  }

  const callerSchool = auth.profile && auth.profile.school_id;
  if (!callerSchool) {
    res.status(403).json({ error: 'Your account is not attached to a school.' });
    return null;
  }

  // Shared free-tier content: the school gets its own layer over the top.
  if (owner.schoolId === null) return { mode: 'override', schoolId: callerSchool };

  // The school's own bespoke content: edit it directly, as before.
  if (owner.schoolId === callerSchool) return { mode: 'direct' };

  res.status(403).json({ error: 'This content belongs to another school.' });
  return null;
}

module.exports = { requireOwnership, isPlatformAdmin, resolveLessonWrite };
