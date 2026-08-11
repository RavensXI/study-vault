/**
 * End-to-end check of copy-on-edit, against real rows.
 *
 *   node scripts/_test_fork_on_edit.js          run the checks
 *   node scripts/_test_fork_on_edit.js --clean  remove the test override
 *
 * Creates (idempotently) a throwaway school so nothing touches Unity or Severn
 * Vale, then proves the property that actually matters: a school's edit must
 * reach that school and NOTHING ELSE. The base lesson is snapshotted field by
 * field before and after, because "we did not mean to write to it" is not
 * evidence — the whole reason this work exists is that three routes wrote
 * somewhere nobody intended.
 *
 * Requires scripts/_create_lesson_overrides.sql to have been run first; there
 * is no SQL RPC on this project, so the table cannot be created from here.
 */
const path = require('path');
const REPO = path.resolve(__dirname, '..');
const { createClient } = require(path.join(REPO, 'node_modules/@supabase/supabase-js'));
const { resolveLessonWrite } = require(path.join(REPO, 'api/pipeline/_lib/scope.js'));
const { writeOverride, applyOverride, baseVersion, ALL_FIELDS } =
  require(path.join(REPO, 'api/pipeline/_lib/overrides.js'));

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const SCHOOL_SLUG = 'fork-test-school';
const STUDENT_CODE = 'forktest2026';

let failures = 0;
function check(name, ok, detail) {
  if (!ok) failures++;
  console.log('  ' + (ok ? 'PASS  ' : 'FAIL  ') + name + (detail ? '   ' + detail : ''));
}
function fakeRes() {
  const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; };
  r.json = b => { r.body = b; return r; };
  return r;
}

(async () => {
  // ---- test school ---------------------------------------------------------
  let { data: school } = await sb.from('schools').select('id, name, settings')
    .eq('slug', SCHOOL_SLUG).maybeSingle();
  if (!school) {
    const ins = await sb.from('schools').insert({
      slug: SCHOOL_SLUG, name: 'Fork Test School',
      settings: { student_code: STUDENT_CODE, is_test: true }
    }).select('id, name, settings').single();
    if (ins.error) { console.error('could not create test school:', ins.error.message); process.exit(1); }
    school = ins.data;
    console.log('created test school:', school.id);
  } else {
    console.log('test school:', school.id);
  }

  // ---- a shared free-tier lesson to edit ------------------------------------
  const gen = (await sb.from('subjects').select('id, slug, school_id').eq('status', 'live'))
    .data.find(s => !s.school_id);
  const unit = (await sb.from('units').select('id, slug').eq('subject_id', gen.id).limit(1)).data[0];
  const lesson = (await sb.from('lessons')
    .select(['id', 'title', 'lesson_number'].concat(ALL_FIELDS).join(', '))
    .eq('unit_id', unit.id).order('lesson_number').limit(1)).data[0];
  console.log('target lesson: %s / %s / %s  (%s)\n', gen.slug, unit.slug, lesson.lesson_number, lesson.id);

  if (process.argv.includes('--clean')) {
    await sb.from('lesson_overrides').delete().eq('lesson_id', lesson.id).eq('school_id', school.id);
    console.log('override removed'); process.exit(0);
  }

  const before = JSON.parse(JSON.stringify(lesson));
  const teacher = { profile: { role: 'teacher', school_id: school.id, full_name: 'Fork Test Teacher' } };
  const admin = { profile: { role: 'platform_admin', school_id: null } };

  // ---- routing -------------------------------------------------------------
  const rTeacher = await resolveLessonWrite(teacher, fakeRes(), lesson.id);
  check('school editing free-tier content routes to an override',
    rTeacher && rTeacher.mode === 'override', JSON.stringify(rTeacher));
  const rAdmin = await resolveLessonWrite(admin, fakeRes(), lesson.id);
  check('admin still writes the base row directly',
    rAdmin && rAdmin.mode === 'direct', JSON.stringify(rAdmin));

  // ---- the edit ------------------------------------------------------------
  const EDITED = [{ question: 'FORK TEST — school-specific knowledge check',
                    correct: 0, options: ['a', 'b', 'c', 'd'] }];
  const w = await writeOverride(lesson.id, school.id, { knowledge_checks: EDITED }, teacher);
  check('override written', w.ok, w.error || ('created=' + w.created));
  if (!w.ok) { console.log('\nIs the table there? Run scripts/_create_lesson_overrides.sql first.'); process.exit(1); }

  // ---- the base row must be untouched, field by field ----------------------
  const after = (await sb.from('lessons')
    .select(['id'].concat(ALL_FIELDS).join(', ')).eq('id', lesson.id).single()).data;
  const drifted = ALL_FIELDS.filter(f => JSON.stringify(before[f]) !== JSON.stringify(after[f]));
  check('base lesson byte-identical after a school edit', drifted.length === 0,
    drifted.length ? 'DRIFTED: ' + drifted.join(', ') : ALL_FIELDS.length + ' fields compared');

  // ---- only the edited field is stored --------------------------------------
  const ovr = (await sb.from('lesson_overrides').select('*')
    .eq('lesson_id', lesson.id).eq('school_id', school.id).single()).data;
  const stored = ALL_FIELDS.filter(f => ovr[f] !== null && ovr[f] !== undefined);
  check('only the changed field is stored (rest inherit)',
    stored.length === 1 && stored[0] === 'knowledge_checks', 'stored: ' + stored.join(', '));
  check('fork stamped with the base version it came from',
    !!ovr.forked_from_version && ovr.forked_from_version === baseVersion(before));

  // ---- what each viewer sees ------------------------------------------------
  const merged = applyOverride(after, ovr);
  check('school sees its own knowledge checks',
    merged.knowledge_checks[0].question.startsWith('FORK TEST'));
  check('school still inherits the untouched article body',
    JSON.stringify(merged.content_html) === JSON.stringify(before.content_html));
  check('free user (no override applied) sees the original',
    JSON.stringify(applyOverride(after, null).knowledge_checks) ===
    JSON.stringify(before.knowledge_checks));

  // ---- another school must not see it ---------------------------------------
  const other = (await sb.from('lesson_overrides').select('id')
    .eq('lesson_id', lesson.id).neq('school_id', school.id)).data;
  check('no other school picked up this override', (other || []).length === 0);

  // ---- drift detection ------------------------------------------------------
  const pretendBaseMoved = Object.assign({}, after, { content_html: (after.content_html || '') + ' <!--x-->' });
  check('detects when StudyVault changes the original after a fork',
    applyOverride(pretendBaseMoved, ovr)._override.base_changed_since_fork === true);
  check('no false alarm while the original is unchanged',
    applyOverride(after, ovr)._override.base_changed_since_fork === false);

  console.log('\n' + (failures ? failures + ' FAILURES' : 'all checks passed'));
  console.log('test school id: ' + school.id + '   student code: ' +
    ((school.settings && school.settings.student_code) || STUDENT_CODE));
  console.log('clean up with: node scripts/_test_fork_on_edit.js --clean');
  process.exit(failures ? 1 : 0);
})();
