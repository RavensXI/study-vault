/**
 * Judgement calls FLAGGED for the orchestrator — deliberately NOT edited.
 * Also records the exam verification trail and the cross-unit blast radius.
 */
const fs = require('fs'), path = require('path');
const D = __dirname;
const R = path.join(D, '_report.json');
const rep = JSON.parse(fs.readFileSync(R, 'utf8'));

rep.flags = [
  {
    severity: 'MEDIUM', lesson: 6, id: 'f6c6bab1-5973-4cf8-b723-ca63ac91dd37',
    where: 'content_html n3 + flashcard_questions + glossary_terms',
    text: 'His <dfn class="term" data-def="A single character’s inner thoughts or feelings spoken aloud on stage, allowing the audience direct access to their emotions.">soliloquy</dfn> about wanting to be like “that guy” — confident, smooth, able to talk to Linda — reveals his growing insecurity.',
    analysis: '"That Guy" is a SUNG Act 2 number, and sources describe it as a duet between Mickey and Edward, not a solo spoken speech. Calling it a soliloquy is therefore inaccurate on two counts. The lesson also contradicts itself: KC1 calls it "Mickey’s song about ‘that guy’" while n3 and a flashcard call it a soliloquy. NOT FIXED because the correction is editorial rather than factual: many teachers legitimately treat a solo musical number as soliloquy-equivalent, and changing the word orphans the "soliloquy" glossary entry, which would have to be replaced in lockstep across content_html, flashcard_questions and glossary_terms. Note the SUBSTANCE is right — "that guy" is an idealised rival/masculinity, not Eddie, which is what the lesson already says.',
    recommend: 'Either keep "soliloquy" but call it sung, or move to "solo number" and swap the glossary term in lockstep.'
  },
  {
    severity: 'LOW', lesson: 4, id: '837c6539-0498-4f28-8e95-9a592dbf6afe',
    where: 'content_html n14/n15, conclusion_html, flashcard_questions; echoed in L5 and L6',
    text: '“I could have been him.” ... "This is Russell’s thesis in five words."',
    analysis: 'VERIFIED genuine, so not an error. But it is a fragment: the fuller line is "Why didn’t you give me away? I could have been him!" (11 words, still inside the 15-word ceiling), which carries the emotional cause the fragment drops. NOT FIXED because it is an enrichment rather than a correction, and it would ripple: L4 n15 says "Russell’s thesis in five words", an L4 flashcard asks for "which five-word line", and L5/L6 quote the same fragment.',
    recommend: 'Optional. If adopted, change all five call sites plus the "five words" framing together.'
  },
  {
    severity: 'LOW', lesson: 5, id: 'd2fef292-6473-4182-bf3d-82d851eda09c',
    where: 'glossary_terms "agency"',
    text: 'agency: "In literary analysis, the forces or factors that ultimately bring about the tragic outcome."',
    analysis: 'This is not what "agency" means. Agency is the capacity to act and to be the author of one’s own actions; the definition has been bent to fit the sentence it sits in. A student who carries this definition into an essay will misuse the term. NOT FIXED because rewording it correctly slightly changes how the surrounding sentence reads, which is an authoring call.',
    recommend: 'Redefine to the standard meaning; the surrounding argument about who is responsible still works.'
  },
  {
    severity: 'LOW', lesson: 5, id: 'd2fef292-6473-4182-bf3d-82d851eda09c',
    where: 'glossary_terms "convenient narrative"',
    text: 'convenient narrative: "A simplified, often misleading explanation that distracts from the real, more complex cause."',
    analysis: 'Not an established literary or critical term, but presented in the glossary alongside real terminology (cyclical structure, rhetorical question). A student may use it in an exam believing it is subject terminology, which AO2 rewards only when the terminology is real. NOT FIXED because removing a glossary entry is a content-design decision.',
    recommend: 'Consider retiring the entry, or relabel it as the lesson’s own phrase rather than a term.'
  },
  {
    severity: 'LOW', lesson: 2, id: '8e4b0146-b283-4d2e-ba94-48a79b3823c8',
    where: 'flashcard_questions',
    text: 'Q: "How does Russell’s sympathy between the two mothers land?"  A: "Clearly with Mrs Johnstone — warmth over bought security."',
    analysis: 'Ungrammatical question stem. Content is correct; only the phrasing is wrong. NOT FIXED because it is style, not fact.',
    recommend: 'Reword to "Where do Russell’s sympathies lie between the two mothers?"'
  },
  {
    severity: 'LOW', lesson: 5, id: 'd2fef292-6473-4182-bf3d-82d851eda09c',
    where: 'flashcard_questions',
    text: 'A: "The myth of meritocracy — that poverty is caused by laziness, not system."',
    analysis: 'Ungrammatical ("not system" needs an article). Style only.',
    recommend: 'Change to "...not by the system."'
  },
  {
    severity: 'INFO', lesson: 1, id: '8a84518f-43d9-4878-b334-63b1ef9cd9bb',
    where: 'content_html n2',
    text: '"Blood Brothers was first performed in 1983"',
    analysis: 'VERIFIED CORRECT — no fix needed. For the record: premiere Liverpool Playhouse, 8 January 1983 (Barbara Dickson); an earlier school version ran at Fazakerley Comprehensive in November 1981; West End transfer to the Lyric on 11 April 1983, closing that October; the long-running revival opened at the Albery on 28 July 1988, moved to the Phoenix in 1991 and closed on 10 November 2012.',
    recommend: 'No action. Enrichment only.'
  }
];

rep.cross_unit_signal = {
  note: 'The three defect families fixed here are NOT unit-local. Measured across all live english-literature-aqa units AFTER this batch.',
  shakespeare_label_on_non_shakespeare_units: {
    total: 190,
    units: { dna: 42, 'pigeon-english': 42, 'lord-of-the-flies': 42, 'anita-and-me': 42, 'animal-farm': 11, 'an-inspector-calls': 11 }
  },
  duplicate_band_labels: {
    total: 178, of: 1332,
    units: ['pigeon-english 42', 'anita-and-me 42', 'lord-of-the-flies 41', 'much-ado-about-nothing 14', 'the-merchant-of-venice 12', 'power-and-conflict 10', 'the-tempest 7', 'the-sign-of-four 7', 'a-christmas-carol 3']
  },
  ao2_denial_lessons: {
    total: 2, units: ['dna', 'pigeon-english'], severity: 'HIGH',
    note: 'Same mark-affecting error corrected in blood-brothers L7: AO2 is worth 12 of the 30 marks on AQA Paper 2 Section A.'
  },
  blood_brothers_status: 'clean on all three after this batch'
};

rep.exam_verification = {
  sources: [
    'AQA 8702 specification v1.3 (GCSE exams June 2017 onwards)',
    'https://media.aqa.org.uk/resources/english/AQA-87022-SMS.PDF',
    'https://filestore.aqa.org.uk/sample-papers-and-mark-schemes/2023/june/AQA-87022-MS-JUN23.PDF',
    'https://filestore.aqa.org.uk/resources/english/AQA-87022-SQP.PDF',
    'https://media.aqa.org.uk/resources/english/AQA-87021-SMS.PDF'
  ],
  modern_text: 'Paper 2 Section A, 30 marks (AO1=12, AO2=12, AO3=6) + 4 marks AO4 = 34',
  ao4_also_on_paper1: 'yes - Paper 1 Section A Shakespeare only (30+4); the 19th-century novel essay is 30 with no SPaG',
  paper2_totals: '34 (Sec A) + 30 (Sec B poetry) + 32 (Sec C unseen: 24+8) = 96',
  closed_book_no_extract: 'confirmed - no printed extract on Section A, but that does NOT remove AO2',
  set_text_status: 'AQA 8702 section 3.2.1 lists "Blood Brothers (musical version)" by Willy Russell as a Modern text (Drama)'
};

fs.writeFileSync(R, JSON.stringify(rep, null, 1), 'utf8');
console.log('flags written:', rep.flags.length);
console.log('fixed counts:', JSON.stringify(rep.fixed_counts));
console.log('renarration:', rep.renarration.verified_ok + '/' + rep.renarration.total);
console.log('report bytes:', fs.statSync(R).size);
