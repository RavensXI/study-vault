/** Fold the FLAGGED (not-edited) findings into _report.json. */
const fs = require('fs'), path = require('path');
const P = path.join(__dirname, '_report.json');
const report = JSON.parse(fs.readFileSync(P, 'utf8'));

report.flagged = [
  {
    id: 'F1', severity: 'HIGH', lesson: 8, id_supabase: 'aca80d53-af4d-4fad-9763-392a3ea26c6c',
    where: 'content_html n4 + glossary_terms + knowledge_checks[1] + exam_tip_html n23 + practice_questions[0].marks + flashcard_questions[2]',
    title: '"apophasis" is misdefined and taught as the name of the wrong device',
    exact_text: 'This technique of describing something by saying it <em>cannot</em> be described is called <dfn class="term" data-def="Describing something as indescribable or beyond words, often to heighten its impact on the reader.">apophasis</dfn>.',
    analysis: 'Apophasis (= paralipsis / praeteritio) is mentioning a thing by declaring you will not mention it ("I will not dwell on his convictions"). It is NOT the assertion that something is beyond description. The device actually at work with Hyde is the inexpressibility / ineffability topos — rhetorically closest to adynaton, or aporia (professed inability to describe). The false label is load-bearing: it is the CORRECT answer to knowledge_checks[1] ("Which language technique does Stevenson use when characters say Hyde is \'not easy to describe\'?" options Metaphor / Hyperbole / Apophasis / Simile), it is listed as required terminology in the exam tip, it appears in a top-band descriptor in practice_questions[0].marks, and it has its own glossary entry and flashcard. A student writing "apophasis" in an AQA answer would be using a term incorrectly under AO2.',
    not_fixed_because: 'The error is certain; the replacement is a judgement call with a six-place blast radius, including rewriting a knowledge-check stem, its correct answer and three distractors.',
    recommended_fix: 'Drop the false technical label rather than substitute an equally obscure one. Content n4: "...This technique — describing something by insisting it cannot be described — leaves the horror to the reader\'s imagination." Delete the "apophasis" glossary entry and its <dfn>. Exam tip: replace "apophasis" with "pathetic fallacy, epistolary elements, doppelganger, unreliable narrator" only. practice_questions[0].marks top band: "animalistic imagery, pathetic fallacy, the refusal to describe Hyde directly". knowledge_checks[1]: recast as "Why does Stevenson keep Hyde\'s appearance vague?" with options ["It makes Hyde seem harmless", "It forces the reader to imagine the horror", "It saves space in a short novella", "It hides a plot twist"], correct 1. flashcard_questions[2]: "Why does Stevenson refuse to describe Hyde clearly?"',
  },
  {
    id: 'F2', severity: 'MEDIUM', lesson: 8, id_supabase: 'aca80d53-af4d-4fad-9763-392a3ea26c6c',
    where: 'content_html n16 + glossary_terms "reliable narrator" + flashcard_questions[8]',
    title: 'Utterson called a "reliable narrator" in the same lesson that calls Chapters 1-8 third-person',
    exact_text: 'Utterson is a <dfn class="term" data-def="A narrator whose account the reader can trust because they have no reason to lie or distort.">reliable narrator</dfn> in the sense that he reports honestly what he sees.',
    analysis: 'Two paragraphs earlier the same lesson states "Chapters 1-8: Third-person narrative focused on Utterson", and L6 correctly calls him the "focaliser". Utterson never narrates; he is the focaliser of a third-person narration. Calling him a narrator undercuts the lesson\'s own structure teaching and the reliable/unreliable contrast it builds with Jekyll (who genuinely is a first-person narrator).',
    not_fixed_because: 'Common classroom shorthand; fixing it means retiring the "reliable narrator" glossary entry and rewording the Jekyll contrast, which is a pedagogic choice.',
    recommended_fix: 'Recast as: "The third-person narration is reliable while it follows Utterson — he reports honestly what he sees — but his perspective is limited..." and keep "unreliable narrator" for Jekyll only.',
  },
  {
    id: 'F3', severity: 'MEDIUM', lesson: 3, id_supabase: 'ebf5e3eb-4848-440b-9b22-ab2251c0308b',
    where: 'flashcard_questions[2]',
    title: '"Ape-like fury" called a simile',
    exact_text: 'q: "Which simile describes Hyde\'s violence in the Carew attack?"  a: "\'Ape-like fury\' — suggesting evolutionary degeneration."',
    analysis: 'A simile is conventionally a comparison made with "like" or "as" as a connecting word. "Ape-like" is a compound adjective, not a connective comparison; most examiners would accept "simile" but many mark it as a metaphor or simply "animalistic imagery". Teaching resources are genuinely split. The equivalent Macbeth error (simile vs metaphor on "I am in blood") was treated as HIGH in the pilot, but that case was unambiguous and this one is not.',
    not_fixed_because: 'Contested AO2 terminology, not a factual error.',
    recommended_fix: 'Safest neutral wording: q: "Which animalistic phrase describes Hyde\'s violence in the Carew attack?"',
  },
  {
    id: 'F4', severity: 'LOW', lesson: '2, 6', id_supabase: 'feb06618-51b1-4aa8-9732-5f20b8649ad2 / 7337351f-23a7-4038-babe-1a32e67c917b',
    where: 'L2 content_html n2, L2 flashcard_questions[0], L6 content_html n14, L6 flashcard_questions[9]',
    title: 'Enfield described as Utterson\'s "cousin"',
    exact_text: 'L2 n2: "The novella opens with Mr Utterson and his cousin Richard Enfield on their regular Sunday walk." / L6 n14: "Enfield is Utterson\'s cousin and walking companion."',
    analysis: 'Stevenson writes "Mr. Richard Enfield, his distant kinsman" (Story of the Door). The text never specifies the relationship. "Distant cousin" is the common study-guide gloss and is not demonstrably wrong, but "cousin" states more than the text supports.',
    not_fixed_because: 'Unsupported rather than certainly false; also costs a re-narration of L2 n2 and L6 n14 for a gloss most editions use.',
    recommended_fix: 'If changed, use "his distant kinsman Richard Enfield" to match the text exactly.',
  },
  {
    id: 'F5', severity: 'LOW', lesson: 1, id_supabase: '50025cc8-7796-4c70-8b32-cf2c010daa2e',
    where: 'content_html n6 (key fact)',
    title: 'West End / East End framing sits oddly next to Soho',
    exact_text: 'Victorian London had a stark divide between the wealthy West End and the poverty-stricken East End. Stevenson uses settings like Soho to represent the hidden, darker side of respectable society.',
    analysis: 'Both sentences are individually true, but the juxtaposition invites students to place Soho in the East End. Soho is in the West End — which is in fact the sharper point Stevenson is making: the squalor is not safely quarantined across town, it is a few streets from the respectable squares.',
    not_fixed_because: 'Not a false statement; the improvement is editorial.',
    recommended_fix: 'Second sentence: "Stevenson sets Hyde\'s rooms in Soho — a poor, disreputable quarter sitting inside the fashionable West End itself, so the hidden side of society is never far from the respectable one."',
  },
  {
    id: 'F6', severity: 'LOW', lesson: 3, id_supabase: 'ebf5e3eb-4848-440b-9b22-ab2251c0308b',
    where: 'glossary_terms "transformation" + content_html n14 data-def',
    title: '"transformation" defined only as trauma-induced character change',
    exact_text: 'definition: "A fundamental change in attitude or character resulting from a traumatic experience."',
    analysis: 'The definition is written to fit Lanyon, but in this novella "transformation" overwhelmingly denotes Jekyll\'s physical change into Hyde — the word students will meet in every other lesson of the unit. A glossary that narrows it to trauma risks confusing exactly the term the unit uses most.',
    not_fixed_because: 'Contextually defensible; rewriting it is a pedagogic choice.',
    recommended_fix: 'Either broaden ("A complete change in form, character or condition") or use a different dfn word for Lanyon, e.g. "decline".',
  },
  {
    id: 'F7', severity: 'LOW', lesson: 1, id_supabase: '50025cc8-7796-4c70-8b32-cf2c010daa2e',
    where: 'content_html n19 + flashcard_questions[10]',
    title: 'The burnt-first-draft anecdote is stated as fact',
    exact_text: 'Stevenson reportedly wrote the first draft of the novella in just three days after a vivid nightmare. His wife Fanny criticised the draft for being too much of a straightforward horror story, so he burned it and rewrote it as an allegory...',
    analysis: 'The "reportedly" hedges only the three days. Fanny\'s criticism and the burning come from Lloyd Osbourne\'s and Fanny\'s later accounts and are disputed by some Stevenson scholars (there is no manuscript evidence, and Stevenson\'s own letters do not mention burning it). Standard GCSE teaching, so low risk.',
    not_fixed_because: 'Universally taught; the hedge already present is arguably sufficient.',
    recommended_fix: 'Extend the hedge: "According to his family\'s later accounts, his wife Fanny criticised the draft..."',
  },
  {
    id: 'F8', severity: 'LOW', lesson: 3, id_supabase: 'ebf5e3eb-4848-440b-9b22-ab2251c0308b',
    where: 'content_html n3',
    title: '"ape-like fury" attached to the clubbing rather than the trampling',
    exact_text: 'The maid describes how Hyde "broke out in a great flame of anger" and "clubbed him to the earth" with "ape-like fury."',
    analysis: 'The text sequences these: "Mr. Hyde broke out of all bounds and clubbed him to the earth. And next moment, with ape-like fury, he was trampling his victim under foot." The "ape-like fury" belongs to the trampling that follows the clubbing. All three quoted fragments are verbatim; only the stitching is loose.',
    not_fixed_because: 'Every quotation is accurate; the conflation is minor and does not change the reading.',
    recommended_fix: '"...\'clubbed him to the earth\', then trampled him with \'ape-like fury\'."',
  },
  {
    id: 'F9', severity: 'LOW', lesson: 5, id_supabase: 'edca02be-82ac-42b2-a19b-7886fe5ffbf6',
    where: 'flashcard_questions[4]',
    title: '"Three adjectives" is inaccurate and the words are Utterson\'s, not the narrator\'s',
    exact_text: 'q: "Which three adjectives does Stevenson use for Hyde\'s appearance?"  a: "\'Troglodytic,\' \'ape-like,\' and \'hardly human.\'"',
    analysis: '"hardly human" is an adjectival phrase, not an adjective. "Troglodytic" and "hardly human" are Utterson\'s words in free indirect thought ("...seems hardly human! Something troglodytic, shall we say?"); only "ape-like" is narratorial. All three are verbatim.',
    not_fixed_because: 'Wording nicety, not a factual error.',
    recommended_fix: 'q: "Which three phrases describe Hyde as less than human?"',
  },
  {
    id: 'F10', severity: 'LOW', lesson: 3, id_supabase: 'ebf5e3eb-4848-440b-9b22-ab2251c0308b',
    where: 'lessons.slug',
    title: 'L3 slug still says incident-at-the-window after the title fix',
    exact_text: 'slug: "chapters-4-6-the-carew-murder-and-incident-at-the-window"',
    analysis: 'The title was corrected (Incident at the Window is Chapter 7, taught in L4) but the slug still carries the wrong chapter. Slugs are not shown to students in the lesson body, but they are in the URL.',
    not_fixed_because: 'Changing a live slug breaks any existing link or bookmark. Needs an owner decision, and a redirect if changed.',
    recommended_fix: 'Leave as-is unless a redirect is added; the URL scheme is /lesson/{subject}/{unit}/{number}, so the slug may not be routed at all — worth confirming before touching it.',
  },
  {
    id: 'F11', severity: 'MEDIUM', lesson: 'all (platform-wide)', id_supabase: 'scripts/lib/narration.py',
    where: 'get_mp3_duration()',
    title: 'ROOT CAUSE FOUND for the known "narration_manifest durations are unreliable" bug',
    exact_text: 'if version == 3 and bitrate_idx not in (0, 15) and sr_idx != 3:   # version 3 = MPEG1 only',
    analysis: 'Azure Speech returns MPEG-2 Layer III at 24 kHz (confirmed on a freshly uploaded clip: first frame header ff f3 a4 c4 -> version bits = 2 = MPEG2, layer bits = 1 = Layer III). get_mp3_duration only accepts version == 3 (MPEG1), so it never matches the real first frame; it then byte-scans until it hits a false-positive MPEG1-looking header inside the audio data and computes a duration from that. It also uses SAMPLES_PER_FRAME = 1152, whereas MPEG2 Layer III uses 576, and the MPEG1 bitrate table, which differs from MPEG2\'s. Worked example from this unit: L2 n17 is 181,440 bytes of 96 kbps CBR = 15.12 s true; the manifest stored 5.55 s (and 7.21 s before this run). This exactly explains memory note [[reference_narration_manifest_durations_unreliable]], which had the symptom but not the cause.',
    not_fixed_because: 'scripts/lib/narration.py is shared by every subject. Changing it inside a single fact-check batch would alter behaviour fleet-wide without Tom\'s go-ahead, and the memory note already records that the platform-wide re-measure needs his approval. The 5 clips re-narrated here were left with pipeline-consistent durations so this unit stays internally uniform.',
    recommended_fix: 'Accept version == 2 and version == 0 (MPEG2 / MPEG2.5), use SAMPLES_PER_FRAME = 576 and the MPEG2 bitrate table [0,8,16,24,32,40,48,56,64,80,96,112,128,144,160,0] for those versions, then run the platform-wide re-measure the memory note describes.',
  },
];

report.flagged_counts = report.flagged.reduce((a, f) => { a[f.severity] = (a[f.severity] || 0) + 1; return a; }, {});
report.totals = {
  lessons: 8,
  fixed: report.fixed_counts,
  flagged: report.flagged_counts,
  clips_renarrated: report.renarration ? report.renarration.total : 0,
  clips_verified: report.renarration ? report.renarration.verified_ok : 0,
};
fs.writeFileSync(P, JSON.stringify(report, null, 1), 'utf8');
console.log('flagged written:', report.flagged.length, JSON.stringify(report.totals));
