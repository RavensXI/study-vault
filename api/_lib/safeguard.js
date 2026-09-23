const { callClaudeDetailed } = require('./claude');
const { supabase } = require('../pipeline/_lib/supabase');
const { sendEmail, escHtml } = require('./notify');

/**
 * The safeguarding route (23 Sep 2026, agreed with Tom).
 *
 * Anything a pupil writes in their own words (an exam answer, a tutor message,
 * a flashcard answer, a search) is read once more by a small model beside the
 * marking. It is not marking: it asks one question, whether the writer is
 * telling us that they, or another child, may be at risk of harm.
 *
 *   concern / unsure  ->  the pupil sees a support panel (Childline, Shout,
 *                         999). If they are signed in and belong to a school
 *                         with a safeguarding lead set up, the concern is kept
 *                         in safeguarding_alerts and the lead is emailed.
 *   no                ->  nothing happens and nothing is kept.
 *
 * WHAT THE EMAIL SAYS. The school's name and the time, and a link to sign in.
 * No pupil name, no pupil words: a disclosure must not sit in an inbox.
 *
 * WHERE IT RUNS. The same London path as the marking (api/_lib/claude.js), so a
 * pupil's words never leave the UK for this check either. It fails quietly: a
 * failed check never stops a pupil getting their marking back, it is logged.
 *
 * Schools set their contacts in schools.settings.safeguarding:
 *   { "lead_name": "...", "lead_email": "...", "deputy_emails": ["..."] }
 */

const MODEL = 'claude-haiku-4-5-20251001';
const MAX_TEXT = 4000;
const EMAIL_GAP_MS = 15 * 60 * 1000;   // at most one email per school per 15 minutes while alerts are unreviewed

const SYSTEM = `You check text that a UK secondary-school pupil (aged 11-16) typed into a GCSE revision website, to decide whether a Designated Safeguarding Lead should see it.

Decide whether the WRITER is telling us that they, or another child they know, may be at risk of harm. That includes:
- thoughts of suicide, not wanting to be alive, self-harm, an overdose
- physical, emotional or sexual abuse, or neglect, at home or anywhere else
- sexual exploitation or grooming (including online: someone asking for pictures, threats)
- being unsafe at home or at school, being afraid of someone, running away, being thrown out
- an eating disorder (restricting food, purging, counting calories to starve)
- serious bullying, violence or threats against the writer
- drug or alcohol harm to the writer, criminal exploitation (being made to carry or sell)

It is NOT a concern when the text is:
- academic content about harm: a set text (An Inspector Calls, Macbeth, Romeo and Juliet, war poetry), a History answer about violence, a Religious Studies answer about abortion or euthanasia, a Psychology answer about disorders, a creative-writing task about a character
- ordinary exam stress, frustration or exaggeration ("this exam is going to kill me", "I hate this question", "I'm going to fail")
- a complaint about the website, the marking or a teacher

When the text mixes an answer with something personal, judge the personal part.
If you are genuinely unsure whether a real person is at risk, answer "unsure": a person will look at it. Do not answer "unsure" for text that is plainly academic or plainly ordinary stress.

Reply with ONE JSON object and nothing else:
{"decision": "concern" | "unsure" | "no",
 "category": "suicide_or_self_harm" | "abuse_or_neglect" | "sexual_exploitation" | "unsafe_at_home_or_school" | "eating_disorder" | "bullying_or_violence" | "substances_or_criminal_exploitation" | "other" | "none",
 "about": "self" | "another_child" | "none",
 "confidence": 0.0-1.0,
 "reason": "one plain sentence a safeguarding lead can read"}`;

/* Short texts (flashcard answers, searches) only reach the model when they
   contain words like these. Wide on purpose: the model is the judge, this only
   saves a call on "photosynthesis". Exam answers and tutor messages always go. */
const PREFILTER = new RegExp([
  'kill(ing)? (my ?self|me)', 'suicid', 'end (it|my life)', "(don'?t|dont|do not) want to (be here|live|be alive|wake up)", 'want(ed)? to die',
  "(won'?t|wont) be (here|around)", 'better off without me', 'no point (in )?(living|anything|me)', 'self[- ]?harm', 'cut(ting)? (my ?self|my (arm|wrist|leg))',
  'hurt(ing)? my ?self', 'overdose', '(took|take|taking|swallowed) (some |all )?(of )?(my |mums? |dads? |the )?(pills|tablets)',
  'abus(e|ed|ing)', '(hits?|hitting|beats?|beat|beaten|punch(es|ed)?|kicks?|kicked|slaps?|slapped|chokes?|choked) (me|us|my (mum|brother|sister))',
  'belt', 'bruis', 'touch(es|ed|ing)? me', 'in(to)? my (room|bed) at night', 'rap(e|ed)\\b', 'nudes?', 'send (him |her |them )?(pics|pictures|photos)', 'groom',
  'scared (of|to go) (home|my (dad|mum|stepdad|stepmum|uncle|brother))', "(not|n'?t) safe", 'unsafe', 'kicked (me )?out', 'run(ning)? away', 'homeless',
  'starv', "(not|n'?t|stopped) eat(ing)?", '\\bcalories\\b', '(throw|throwing|made myself|make myself) (up|sick)', 'purg',
  'drunk', 'drinks too much', 'hate my ?self', 'want (it|this|everything) to stop', 'carry(ing)? (drugs|a knife|stuff) for', 'bullied|bullying|beat me up'
].join('|'), 'i');

function prefilterHit(text) { return PREFILTER.test(String(text || '')); }

function parse(text) {
  const m = String(text || '').match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch (e) { return null; }
}

/** One check. Returns { decision, category, about, confidence, reason, model, servedBy } or null on failure. */
async function check({ text, context, source }) {
  const body = String(text || '').slice(0, MAX_TEXT);
  if (!body.trim()) return null;
  const user = 'WHERE THE PUPIL WROTE IT: ' + ({ exam_answer: 'an answer to an exam-style practice question', tutor: 'a message to the lesson tutor chat', flashcard: 'a typed answer on a flashcard', search: 'the site search box' }[source] || source) +
    (context ? '\nTHE QUESTION OR TASK: ' + String(context).slice(0, 1500) : '') +
    '\n\nWHAT THE PUPIL TYPED:\n' + body;
  const r = await callClaudeDetailed({ model: MODEL, max_tokens: 200, system: SYSTEM, messages: [{ role: 'user', content: user }] });
  const j = parse(r.text);
  if (!j || !['concern', 'unsure', 'no'].includes(j.decision)) {
    console.error('[safeguard] unparseable check reply:', String(r.text).slice(0, 200));
    return { decision: 'unparseable', model: MODEL, servedBy: r.servedBy };
  }
  return Object.assign(j, { model: MODEL, servedBy: r.servedBy });
}

/** The signed-in pupil and the school whose safeguarding lead should hear, or null. */
async function identify(req) {
  const h = (req.headers && req.headers.authorization) || '';
  if (!h.startsWith('Bearer ')) return null;
  const { data, error } = await supabase.auth.getUser(h.slice(7));
  if (error || !data || !data.user) return null;
  const userId = data.user.id;
  // Class membership first (a class at a school is the explicit link), then the profile's school.
  const [{ data: mem }, { data: prof }] = await Promise.all([
    supabase.from('class_members').select('classes(school_id)').eq('student_id', userId),
    supabase.from('profiles').select('school_id, role').eq('id', userId).maybeSingle()
  ]);
  // Staff accounts (a teacher trying the tutor, a lead testing the route) are not pupils:
  // they see the support panel like anyone, but nothing is sent to their school.
  if (prof && ['teacher', 'school_admin', 'platform_admin'].includes(prof.role)) return { userId, school: null };
  const ids = Array.from(new Set((mem || []).map(m => m.classes && m.classes.school_id).concat(prof && prof.school_id ? [prof.school_id] : []).filter(Boolean)));
  if (!ids.length) return { userId, school: null };
  const { data: schools } = await supabase.from('schools').select('id, name, settings').in('id', ids);
  const withLead = (schools || []).find(s => s.settings && s.settings.safeguarding && s.settings.safeguarding.lead_email);
  return { userId, school: withLead || null };
}

function contacts(school) {
  const sg = (school && school.settings && school.settings.safeguarding) || {};
  return [sg.lead_email].concat(Array.isArray(sg.deputy_emails) ? sg.deputy_emails : [])
    .map(e => String(e || '').trim()).filter(e => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e));
}

async function notify(school, alertId) {
  const to = contacts(school);
  if (!to.length) return false;
  // One email covers a burst: skip when this school was emailed in the last 15 minutes about an alert still unreviewed.
  const since = new Date(Date.now() - EMAIL_GAP_MS).toISOString();
  const { data: recent } = await supabase.from('safeguarding_alerts').select('id')
    .eq('school_id', school.id).eq('status', 'new').not('notified_at', 'is', null).gte('notified_at', since).limit(1);
  if (recent && recent.length) return false;
  const when = new Date().toLocaleString('en-GB', { timeZone: 'Europe/London', weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' });
  const link = 'https://www.studyvault.co.uk/teacher/safeguarding';
  const subject = 'StudyVault: a safeguarding concern needs review';
  const text = 'A possible safeguarding concern was flagged at ' + school.name + ' on ' + when + '.\n\n' +
    'Sign in to review it: ' + link + '\n\n' +
    'This email does not include the pupil\'s name or what they wrote. You are receiving it because you are listed as a safeguarding contact for ' + school.name + ' on StudyVault.';
  const html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#26231e;max-width:560px">' +
    '<p>A possible safeguarding concern was flagged at <b>' + escHtml(school.name) + '</b> on ' + escHtml(when) + '.</p>' +
    '<p><a href="' + link + '" style="color:#b0561c;font-weight:bold">Sign in to review it</a></p>' +
    '<p style="color:#7d7868;font-size:13px">This email does not include the pupil’s name or what they wrote. You are receiving it because you are listed as a safeguarding contact for ' + escHtml(school.name) + ' on StudyVault.</p></div>';
  let sent = false;
  for (const addr of to) { const r = await sendEmail({ to: addr, subject, html, text }); if (r && r.ok) sent = true; }
  if (sent) await supabase.from('safeguarding_alerts').update({ notified_at: new Date().toISOString() }).eq('id', alertId);
  return sent;
}

/**
 * Check what a pupil wrote and act on it. Never throws.
 *   screen(req, { text, context, source, page, prefilter })
 *   -> { support: bool, school_name?: string }  (support = show the support panel)
 */
async function screen(req, { text, context, source, page, prefilter }) {
  try {
    if (!text || !String(text).trim()) return { support: false };
    if (prefilter && !prefilterHit(text)) return { support: false };
    const r = await check({ text, context, source });
    if (!r || (r.decision !== 'concern' && r.decision !== 'unsure')) return { support: false };
    const who = await identify(req).catch(e => { console.error('[safeguard] identify failed:', e.message); return null; });
    if (!who || !who.school) return { support: true };            // free tier / anonymous / no lead set up: signpost only, keep nothing
    const { data: row, error } = await supabase.from('safeguarding_alerts').insert({
      school_id: who.school.id, student_id: who.userId, source, page: page ? String(page).slice(0, 300) : null,
      context: context ? String(context).slice(0, 2000) : null, body: String(text).slice(0, MAX_TEXT),
      decision: r.decision, category: r.category || null, reason: r.reason ? String(r.reason).slice(0, 500) : null,
      confidence: typeof r.confidence === 'number' ? Math.max(0, Math.min(1, r.confidence)) : null,
      model: r.model, served_by: r.servedBy
    }).select('id').single();
    if (error) { console.error('[safeguard] could not store alert:', error.message); return { support: true, school_name: who.school.name }; }
    await notify(who.school, row.id).catch(e => console.error('[safeguard] notify failed:', e.message));
    return { support: true, school_name: who.school.name };
  } catch (e) {
    console.error('[safeguard] check failed:', e.message);
    return { support: false };
  }
}

/* Await the check, but never hold a pupil's marking for long: the check started
   when the request did, so it has usually finished; if not, give it `ms` more. */
function settle(promise, ms) {
  let timer;
  const late = new Promise(resolve => { timer = setTimeout(() => { console.error('[safeguard] check still running after', ms, 'ms; answering without it'); resolve({ support: false }); }, ms); });
  return Promise.race([promise, late]).finally(() => clearTimeout(timer));
}

/* The pupil's own words inside a marking prompt, for callers that do not send them separately. */
function answerFromPrompt(prompt) {
  const m = String(prompt || '').match(/student answer:\s*([\s\S]*)$/i);
  return m ? m[1].trim() : '';
}

/* What the pupil reads in place of the marker's or the tutor's reply when the check flags.
   Seen on 23 Sep: given a disclosure, the marker wrote its own crisis message and got the
   Childline number wrong and promised confidentiality. The support panel carries the checked
   numbers; this line only points to it and never promises that nobody will be told. */
const HOLDING = 'This answer has not been marked, because what you wrote sounds as if something might be wrong. ' +
  'You do not have to deal with it on your own. The box below lists people you can talk to right now, and a teacher or another adult you trust can help too.';
const TUTOR_HOLDING = 'I’m sorry you’re dealing with that. You don’t have to handle it on your own. ' +
  'The box below lists people you can talk to right now, and a teacher or another adult you trust can help too.';

/* The marker's reply, replaced: plain text for the lesson questions, the JSON verdict for
   the practice pages (they read {quality, feedback}). */
function holdingResult(system) {
  return /"quality"/.test(String(system || ''))
    ? JSON.stringify({ quality: 'needs_work', feedback: HOLDING })
    : HOLDING;
}

module.exports = { screen, settle, check, prefilterHit, identify, answerFromPrompt, contacts, holdingResult, HOLDING, TUTOR_HOLDING };
