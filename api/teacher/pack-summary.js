const { requireTeacher } = require('../pipeline/_lib/auth');
const { callClaudeDetailed, useBedrock } = require('../_lib/claude');
const { buildPack } = require('./_lib/pack');

/**
 * Drafts the teacher's summary paragraph for a parents' evening pack.
 *
 * TWO THINGS THIS DELIBERATELY DOES NOT DO.
 *
 * It does not accept the evidence from the client. The caller sends a class id
 * and a student id; the aggregates are rebuilt server-side by buildPack and the
 * prompt is assembled here. A page that posted its own numbers could put any
 * text it liked in front of the model, about any child.
 *
 * It does not send raw pupil data. The model receives counts, percentages and
 * question texts — no dates of individual sessions, no identifiers, and the
 * first name only. There is no reason a summarising model needs to know a
 * child's surname to write "he finds the League of Nations hard".
 *
 * It runs through api/_lib/claude.js, so it goes to Bedrock in eu-west-2 like
 * the marking routes. servedBy is returned so a silent US fallback is visible
 * rather than assumed — see reference_bedrock_london_setup.
 */

const MODEL = 'claude-haiku-4-5-20251001';   // a paragraph from a table: the cheap tier is right

const SYSTEM = [
  'You draft one short paragraph for a UK secondary teacher to read at parents evening.',
  'You are given evidence about one pupil in one GCSE subject.',
  '',
  'Rules:',
  '- British English. Plain, warm, professional. No bullet points, no headings.',
  '- 70 to 110 words. One paragraph.',
  '- Use ONLY the evidence given. Never invent a grade, a target, a predicted grade,',
  '  an effort score, or anything about behaviour, attendance or attitude.',
  '- Name specific topics from the evidence. "Struggles with Macbeth" is useful;',
  '  "should revise more" is not.',
  '- If the evidence is thin, say so plainly rather than padding.',
  '- Do not address the parent or the pupil directly. Write about the pupil in the',
  '  third person, for the teacher to say aloud.',
  '- End with one concrete thing that would help most, drawn from the weakest topics.'
].join('\n');

function evidence(p) {
  const first = String(p.student.name || 'The pupil').split(' ')[0];
  const L = [];
  L.push('Pupil: ' + first);
  L.push('Subject: ' + (p.class.subject || 'this subject'));
  L.push('Lessons finished: ' + p.headline.lessonsFinished);
  L.push('Quiz questions answered while revising: ' + p.headline.questionsAnswered);
  L.push('Overall recall accuracy: ' +
         (p.headline.recallAccuracy == null ? 'not enough evidence' : p.headline.recallAccuracy + '%'));
  L.push('Days revised in the last four weeks: ' + p.headline.daysRevised);

  if (p.units.length) {
    L.push('');
    L.push('By topic (pupil accuracy, then class average):');
    p.units.forEach(function (u) {
      L.push('- ' + u.unit + ': ' +
        (u.accuracy == null ? 'not enough evidence' : u.accuracy + '% of ' + u.answered + ' questions') +
        (u.classAccuracy == null ? '' : ' (class ' + u.classAccuracy + '%)') +
        ', ' + u.lessonsDone + ' lessons done');
    });
  }
  if (p.keepsMissing.length) {
    L.push('');
    L.push('Questions repeatedly answered wrong:');
    p.keepsMissing.forEach(function (m) {
      L.push('- ' + m.unit + ': "' + m.question + '" (wrong ' + m.times + ' times)');
    });
  }
  return L.join('\n');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const auth = await requireTeacher(req, res);
  if (!auth) return;

  /* FAIL CLOSED. api/_lib/claude.js falls back to the Anthropic API in the US
     when Bedrock is not configured, which is a sensible default for marking a
     practice answer and the wrong one here: this route sends a named child's
     attainment. Running it in the first test proved the point — it returned
     servedBy "anthropic-direct" because the shell had no AWS variables, and
     nothing would have flagged that in production either.

     A refusal is recoverable. Pupil data crossing the Atlantic because an
     environment variable was missing is not, and it would sit directly under a
     DPA claim about UK processing. */
  if (!useBedrock()) {
    return res.status(503).json({
      error: 'Summaries are unavailable: the UK AI region is not configured on this ' +
             'deployment, and this feature will not send pupil data anywhere else. ' +
             'Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_REGION (eu-west-2).'
    });
  }

  const b = req.body || {};
  const out = await buildPack(auth, b.class_id, b.student_id);
  if (!out.ok) return res.status(out.status || 400).json({ error: out.error });

  const p = out.pack;
  if (!p.headline.questionsAnswered && !p.headline.lessonsFinished) {
    return res.status(200).json({
      draft: String(p.student.name).split(' ')[0] +
        ' has not done enough on StudyVault yet for a summary to mean anything. ' +
        'There is no evidence here to report either way.',
      servedBy: 'none', generated: false
    });
  }

  try {
    const r = await callClaudeDetailed({
      model: MODEL,
      max_tokens: 400,
      system: SYSTEM,
      messages: [{ role: 'user', content: evidence(p) }]
    });
    /* Second guard, after the fact. useBedrock() only says Bedrock is
       CONFIGURED; callClaude can still fall back mid-call. This cannot unsend
       what went, but it stops the result being presented as UK-processed and
       makes the failure loud instead of invisible. */
    if (!/bedrock/i.test(r.servedBy || '')) {
      return res.status(502).json({
        error: 'The summary was not served from the UK region (' + (r.servedBy || 'unknown') +
               '), so it has not been returned. Check the Bedrock credentials.'
      });
    }

    return res.status(200).json({
      draft: (r.text || '').trim(),
      servedBy: r.servedBy,      // proves London rather than assuming it
      generated: true
    });
  } catch (e) {
    return res.status(502).json({ error: 'Could not draft the summary. ' + e.message });
  }
};
