// Exercise requireOwnership against real rows. No writes: the guard is called
// directly and its response is captured, so nothing reaches .update().
process.env.SUPABASE_URL = process.env.SUPABASE_URL || '';
const { createClient } = require('@supabase/supabase-js');
const { requireOwnership } = require('C:/Users/tshau/.claude/jobs/4059242c/tmp/plat/api/pipeline/_lib/scope.js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

function fakeRes() {
  const r = { code: null, body: null };
  r.status = c => { r.code = c; return r; };
  r.json = b => { r.body = b; return r; };
  return r;
}

(async () => {
  // a generic (free-tier) lesson and a school-owned lesson
  const subs = (await sb.from('subjects').select('id,slug,school_id').eq('status','live')).data;
  const gen = subs.find(s => !s.school_id);
  const sch = subs.find(s => s.school_id);
  async function aLesson(subjectId) {
    const u = (await sb.from('units').select('id').eq('subject_id', subjectId).limit(1)).data[0];
    return (await sb.from('lessons').select('id').eq('unit_id', u.id).limit(1)).data[0].id;
  }
  const genLesson = await aLesson(gen.id);
  const schLesson = await aLesson(sch.id);
  const otherSchool = subs.find(s => s.school_id && s.school_id !== sch.school_id);

  const cases = [
    ['platform_admin -> generic lesson',  {profile:{role:'platform_admin', school_id:null}},      'lesson', genLesson, true],
    ['platform_admin -> school lesson',   {profile:{role:'platform_admin', school_id:null}},      'lesson', schLesson, true],
    ['teacher -> GENERIC lesson',         {profile:{role:'teacher', school_id: sch.school_id}},   'lesson', genLesson, false],
    ['teacher -> OWN school lesson',      {profile:{role:'teacher', school_id: sch.school_id}},   'lesson', schLesson, true],
    ['teacher -> OTHER school lesson',    {profile:{role:'teacher', school_id: otherSchool ? otherSchool.school_id : '00000000-0000-0000-0000-000000000000'}, }, 'lesson', schLesson, false],
    ['teacher (no school) -> school',     {profile:{role:'teacher', school_id: null}},            'lesson', schLesson, false],
    ['teacher -> missing lesson',         {profile:{role:'teacher', school_id: sch.school_id}},   'lesson', '00000000-0000-0000-0000-000000000000', false],
  ];

  let fails = 0;
  for (const [name, auth, kind, id, expectAllowed] of cases) {
    const res = fakeRes();
    const ok = await requireOwnership(auth, res, kind, id);
    const good = ok === expectAllowed;
    if (!good) fails++;
    console.log((good ? '  PASS  ' : '  FAIL  ') + name.padEnd(34) +
      ' allowed=' + ok + (res.code ? '  http=' + res.code : '') +
      (res.body ? '  "' + String(res.body.error).slice(0, 52) + '..."' : ''));
  }
  // guide arm
  const g = (await sb.from('guide_pages').select('id,subject_id').limit(1)).data[0];
  const gSub = (await sb.from('subjects').select('school_id').eq('id', g.subject_id).single()).data;
  const res = fakeRes();
  const ok = await requireOwnership({profile:{role:'teacher', school_id:'x'}}, res, 'guide', g.id);
  console.log('  ' + (ok === false ? 'PASS  ' : 'FAIL  ') + 'teacher -> guide (owner school_id=' +
    gSub.school_id + ')  allowed=' + ok + '  http=' + res.code);
  if (ok !== false) fails++;
  console.log(fails ? '\n' + fails + ' FAILURES' : '\nall cases behave as intended');
  process.exit(fails ? 1 : 0);
})();
