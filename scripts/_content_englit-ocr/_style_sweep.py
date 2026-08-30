# -*- coding: utf-8 -*-
"""
Style sweep: bring english-literature-ocr / unseen-poetry L1-L6 into house register.

Rewrites off-register sentences ONLY. No fact, mark, timing, quotation or taught
point changes. Every data-narration-id and every HTML structure is preserved.
Entity conventions kept: *_html fields use entities, plain-text fields use unicode.

Backs up the pre-sweep value of every field it touches to
_unseen_style_backup.json BEFORE the first write.

Run:  python scripts/_content_englit-ocr/_style_sweep.py          (dry run)
      python scripts/_content_englit-ocr/_style_sweep.py --write   (patch Supabase)
"""
import sys, os, json

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

UNIT_ID = "d15cce20-ab7f-4b4b-849f-53fd6595785d"
BACKUP = os.path.join(HERE, "_unseen_style_backup.json")

# --------------------------------------------------------------------------
# EDITS: lesson_number -> field -> list of (old, new)
# Each `old` must appear EXACTLY ONCE in the field, or the run aborts.
# --------------------------------------------------------------------------
EDITS = {

1: {"content_html": [
    # performative heading -> functional
    (r'<h2 data-narration-id="n1">The Unseen Poem Never Arrives Alone</h2>',
     r'<h2 data-narration-id="n1">The Unseen Poem Is Always Paired</h2>'),
    # clipped second-person payoff
    (r'In some courses the unseen poem is a task on its own. In yours it is not.',
     r'In some courses the unseen poem is a task on its own. In this course it is not.'),
    # "not decoration" flourish + "opens the field" metaphor
    (r'Those bullets are not decoration. They are the shape of a good answer, and they tell you that <strong>method</strong> matters as much as meaning. Part (b) then opens the field: &ldquo;Explore',
     r'The bullets are there to shape your answer, and they tell you that <strong>method</strong> matters as much as meaning. Part (b) is worded more broadly: &ldquo;Explore'),
    # strained "argue with best" construction
    (r'part (b) is chosen by you, so the poem you can argue with best is the poem you should pick.',
     r'part (b) is chosen by you, so pick the poem you can write about most confidently.'),
    # throat-clearing drumroll + "where the marks live"
    (r'One warning matters more than any other. Students often assume the two poets must agree. They frequently do not &mdash; and the differences between them are where the highest marks live.',
     r'The most common error is assuming that the two poets must agree. They frequently do not, and the differences between them are where the highest marks are earned.'),
    # intensifier "really" + dash
    (r'into the skill this paper is really built around &mdash; linking an unfamiliar poem',
     r'into the central skill of this paper: linking an unfamiliar poem'),
]},

2: {"content_html": [
    # "marks follow the sentence" compression + "describe ... exactly"
    (r'That means marks follow the sentence in which you explain what a word <em>does</em>, not the sentence in which you name a device. Examiners describe the weaker habit exactly: feature-spotting.',
     r'That means the marks come from explaining what a word <em>does</em>, not from naming a device. Examiners call the weaker habit feature-spotting.'),
    # inverted aphorism
    (r'Two images analysed this way beat ten techniques merely labelled.',
     r'Two images analysed this way earn more than ten techniques that are only named.'),
    # "hands the army" + triadic punch-list + "not merely X but Y"
    (r'The simile hands the army a predator&rsquo;s hunger and speed &mdash; but the more telling word is &ldquo;fold&rdquo;, which turns the victims into penned sheep: owned, counted, unable to run. The slaughter is made to feel not merely violent but routine.',
     r'The simile gives the army a predator&rsquo;s hunger and speed, but the more telling word is &ldquo;fold&rdquo;, which turns the victims into penned sheep: animals that are owned, counted and unable to escape. The slaughter is made to feel routine as well as violent.'),
    # clipped chiasmus + epigram
    (r'The mountain has not moved; the boy&rsquo;s guilt has. Personification here turns landscape into conscience.',
     r'The mountain has not moved; the boy&rsquo;s guilt makes it seem to. The personification turns the landscape into an image of the boy&rsquo;s conscience.'),
    # parallel-rhythm aphorism + "not X but Y"
    (r'It is easy to spot and easy to waste. The mark comes from precision: not &ldquo;the rain shows sadness&rdquo; but what <em>kind</em> of sadness the particular weather implies.',
     r'Students spot it easily but often stop there. The mark comes from precision. Do not write &ldquo;the rain shows sadness&rdquo;; say what <em>kind</em> of sadness the particular weather implies.'),
    # litotes
    (r'A repeated object in a short poem is rarely accidental.',
     r'A repeated object in a short poem is usually deliberate.'),
    # poetic heading
    (r'<h2 data-narration-id="n10">Connotation: The Word Behind the Word</h2>',
     r'<h2 data-narration-id="n10">Connotation: Testing a Poet&rsquo;s Word Choice</h2>'),
    # triad with escalation + coinage "off-true"
    (r'&ldquo;Slant&rdquo; suggests something off-true, oblique, faintly wrong &mdash; and that crookedness prepares',
     r'&ldquo;Slant&rdquo; suggests something oblique and slightly wrong, and that crookedness prepares'),
    # present-tense aphorism
    (r'Ask yourself: what would be lost if the poet had used the ordinary word instead? Your answer to that question is the analysis.',
     r'Ask yourself what would be lost if the poet had used the ordinary word instead. Your answer to that question is the point to write down.'),
    # performative collapsible title
    (r'<span>Sound: how a line feels in the mouth</span>',
     r'<span>Sound: consonants, vowels and pace</span>'),
    # clipped "Context decides which."
    (r'can hush a line or make it hiss. Context decides which.',
     r'can hush a line or make it hiss, depending on the context.'),
 ],
 "flashcard_questions": [
    # card lost its antecedent once the bank is shuffled; also carries "off-true"
    (u"What does that word choice suggest about the light?",
     u"What does Dickinson's word 'Slant' suggest about the light?"),
    (u"Something off-true and oblique, preparing the reader for pain.",
     u"Something oblique and slightly wrong, preparing the reader for pain."),
 ]},

3: {"content_html": [
    # hook heading
    (r'<h2 data-narration-id="n1">The Half of the Objective Most Students Skip</h2>',
     r'<h2 data-narration-id="n1">Why Form and Structure Matter</h2>'),
    # triadic fragment + dash
    (r'<strong>How do the final lines land?</strong> Resolution, refusal, or a deliberate failure to resolve &mdash; endings are the most quotable structural evidence you have.',
     r'<strong>How do the final lines land?</strong> Look for resolution, refusal, or a deliberate failure to resolve. Endings are the most quotable structural evidence you have.'),
    # two chained aphorisms + "what the poem is for"
    (r'The turn is the argument. Find it and you have found what the poem is for.',
     r'The turn carries the argument, so finding it usually tells you what the poem is trying to say.'),
    # intensifier
    (r'These are useful precisely because they need no knowledge of the poet.',
     r'These are useful because they need no knowledge of the poet.'),
    # triad with escalation
    (r'can make a poem sound inevitable, settled, even smug &mdash; useful when a poet wants an argument to feel proved.',
     r'can make a poem sound settled and inevitable &mdash; useful when a poet wants an argument to feel proved.'),
]},

4: {"content_html": [
    # intensifier "exactly why"
    (r'share no theme at all &mdash; which is exactly why the comparison part is worth writing carefully.',
     r'share no theme at all, which is why the comparison part rewards careful writing.'),
    # throat-clearing connective sentence
    (r'There is a matching warning. Examiners criticise responses',
     r'Examiners also criticise responses'),
    # "claiming company" compression + rhythm-driven verb variation
    (r'is claiming company; one who slides from <em>you</em> to <em>they</em> is stepping back',
     r'is claiming to speak for a group; one who moves from <em>you</em> to <em>they</em> is stepping back'),
    # poetic parallel heading
    (r'<h2 data-narration-id="n15">Other Readers, Other Readings</h2>',
     r'<h2 data-narration-id="n15">Recognising Other Valid Readings</h2>'),
    # clipped defensive beat
    (r'different valid responses to a text are possible. This is not hedging. Offering a second reading',
     r'different valid responses to a text are possible, and doing so is not hedging. Offering a second reading'),
    # inverted aphorism
    (r'three or four words you can place perfectly beat a whole line you half-remember.',
     r'three or four words you can place perfectly are worth more than a whole line you half-remember.'),
    # present-tense aphorism
    (r'Recognition is not recall, and the exam asks for recall.',
     r'Recognising a quotation is not the same as being able to recall it, and the exam asks for recall.'),
]},

5: {"content_html": [
    # triadic anaphoric heading
    (r'<h2 data-narration-id="n1">One Unseen Poem, One Cluster Poem, One Theme</h2>',
     r'<h2 data-narration-id="n1">How the Comparison Task Works</h2>'),
    # "turn on" / "hold together"
    (r'Twenty marks turn on how well you hold the two poems together.',
     r'All twenty marks depend on how well you keep the two poems together.'),
    # metaphor: you cannot hold a theme in your hand
    (r'then the unseen poem with that theme in your hand.',
     r'then the unseen poem with that theme in mind.'),
    # compressed aphorism
    (r'Annotate only against that idea. Anything else is time you will want later.',
     r'Annotate only against that idea. Time spent on anything else is time you will need later.'),
    # balanced chiastic aphorism
    (r'The shared idea gives you the paragraph; the difference in feeling gives you the point.',
     r'Use the shared idea to set up the paragraph, then make the difference in feeling your main point.'),
    # "a stanza that will not close" -> the actual mechanism; + inverted aphorism
    (r'the other through a widening stanza that will not close. Identical effects reached by opposite means make excellent comparative writing.',
     r'the other through a stanza that lengthens without reaching a full stop. When two poets reach the same effect by opposite means, that contrast makes excellent comparative writing.'),
    # "the spine of the response"
    (r'Say so, plainly, and use the clash as the spine of the response.',
     r'Say so plainly, and build the whole response around that disagreement.'),
    # clipped aphorism opening a key fact
    (r'<p>The grid is the plan. Four rows',
     r'<p>Use the grid as your plan. Four rows'),
    # read-twice nesting
    (r'A connective promising similarity in front of a point that is not similar reads worse than no connective at all.',
     r'A connective that promises similarity in front of a point that is really a contrast is worse than no connective at all.'),
    # strained metaphor "fetch"
    (r'and it never leaves one poem to fetch the other.',
     r'and it never abandons one poem to deal with the other separately.'),
 ],
 "knowledge_checks": [
    # keep the match option consistent with the rewritten body text
    (u"Both build unease — one through caesura, the other through a stanza that will not close",
     u"Both build unease — one through caesura, the other through a stanza that never reaches a full stop"),
 ]},

6: {"content_html": [
    # staccato sentence fragments as drumbeat
    (r'<p>Two hours. Eighty marks. Forty marks for the poetry section and forty for the Shakespeare section, so an even hour each. Inside the poetry hour,',
     r'<p>The paper is two hours long and worth eighty marks. Forty marks go to the poetry section and forty to the Shakespeare section, so each deserves an even hour. Inside the poetry hour,'),
    # two-beat "not X. It is Y." reversal
    (r'</dfn> is not a failure of skill. It is a failure of reading the instructions, and',
     r'</dfn> is a failure to read the instructions rather than a failure of skill, and'),
    # direct-address dramatics
    (r'The task says <em>one other poem</em>, and it means it.',
     r'The task asks for <em>one other poem</em>, so the part (a) poem cannot be used again.'),
    # the flagged aphorism + "a parade of quotations"
    (r'Length is not the mark. Examiners report very long scripts &mdash; some running to fifteen sides or more &mdash; whose quality was damaged by their quantity, with the same point restated through a parade of different quotations.',
     r'Length does not earn marks. Examiners report very long scripts &mdash; some running to fifteen sides or more &mdash; whose quality suffered from their length, with the same point restated through one quotation after another.'),
 ],
 "conclusion_html": [
    (r'beat eight thin ones; length is not the mark.',
     r'beat eight thin ones; length alone earns no marks.'),
 ]},
}


def apply_edits(rows, write):
    from collections import OrderedDict
    by_num = {r["lesson_number"]: r for r in rows}
    backup = OrderedDict()
    payloads = {}
    problems = []

    for num in sorted(EDITS):
        row = by_num.get(num)
        if row is None:
            problems.append("L%d: row not found" % num)
            continue
        changed = {}
        for field, pairs in EDITS[num].items():
            original = row.get(field)
            if isinstance(original, (list, dict)):
                blob = json.dumps(original, ensure_ascii=False)
                is_json = True
            else:
                blob = original or ""
                is_json = False
            new_blob = blob
            for old, new in pairs:
                n = new_blob.count(old)
                if n != 1:
                    problems.append("L%d %s: %d matches (expected 1) for %r"
                                    % (num, field, n, old[:70]))
                    continue
                new_blob = new_blob.replace(old, new)
            if new_blob != blob:
                changed[field] = json.loads(new_blob) if is_json else new_blob
        if changed:
            backup["L%d" % num] = {
                "lesson_id": row["id"],
                "lesson_number": num,
                "title": row["title"],
                "fields": {f: row.get(f) for f in changed},
            }
            payloads[num] = (row["id"], changed)
        print("L%d: %d field(s) changed  [%s]" % (num, len(changed), ", ".join(sorted(changed)) or "-"))

    if problems:
        print("\nABORT - anchor problems:")
        for p in problems:
            print("  " + p)
        return None, None

    return backup, payloads


def main():
    write = "--write" in sys.argv
    from lib.supabase_client import get_client
    sb = get_client()
    rows = sb.table("lessons").select("*").eq("unit_id", UNIT_ID).execute().data
    rows.sort(key=lambda r: r["lesson_number"])

    backup, payloads = apply_edits(rows, write)
    if payloads is None:
        sys.exit(1)

    if not write:
        print("\nDRY RUN ok. %d lessons would be patched. Re-run with --write." % len(payloads))
        return

    # Back up BEFORE the first write.
    with open(BACKUP, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=1)
    print("\nBacked up pre-sweep values -> %s" % BACKUP)

    for num in sorted(payloads):
        lid, changed = payloads[num]
        sb.table("lessons").update(changed).eq("id", lid).execute()
        print("L%d patched (%s) -> %s" % (num, ", ".join(sorted(changed)), lid))
    print("done")


if __name__ == "__main__":
    main()
