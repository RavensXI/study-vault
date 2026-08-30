import json, html
ART = r'C:\Users\tshau\.claude\jobs\6db560ab\tmp\exit_ticket_specimens.html'
doc = open(ART, encoding='utf-8').read()
MARK = '<!-- canary sections -->'
doc = doc[:doc.index(MARK)].rstrip() + '\n'
notes = {
 ('sci',4): 'Review trim: the draft appended a second clause that outlined the answer\u2019s shape.',
 ('sci',9): 'Review trim: the draft stacked two asks (big zone AND tiny zone); collapsed to the single telling case.',
 ('geo',3): 'Review fix (Tom\u2019s catch): the draft said \u201cHaiti\u2019s quake was bigger, YET its toll was higher\u201d \u2014 a false paradox implying smaller quakes should kill more. Reframed around the real anomaly: quakes close in size, tolls a thousand times apart.',
 ('geo',4): 'Review replacement (Tom\u2019s catch + duplication): the draft repeated L3\u2019s inverted \u201cyet\u201d AND re-asked L3\u2019s question. Replaced with a protection-vs-planning judgement the L3 ticket could not have extracted.',
 ('geo',6): 'Review fix: the draft invented \u201cfive days\u2019 notice\u201d \u2014 not in the lesson (and wrong). Rebuilt on the grounded facts: warnings + 800,000 evacuated.',
 ('geo',12): 'Review trim: the draft asked the student to \u201cimagine\u201d adaptations they had just been taught; reframed as explanation.',
}
def section(title, key, subj_slug, unit_slug, fn):
    rows = ['<h2>Sonnet canary &mdash; %s</h2>' % title]
    for t in json.load(open(fn, encoding='utf-8')):
        n = t['lesson_number']; note = notes.get((key, n))
        rows.append('<div class="ticket">')
        rows.append('<div class="t-head"><span class="t-lesson"><a href="https://www.studyvault.co.uk/lesson/%s/%s/%d">L%d</a></span><span class="t-from">%s</span></div>' % (subj_slug, unit_slug, n, n, html.escape(t['from'])))
        rows.append('<p class="t-q">%s</p>' % html.escape(t['q']))
        rows.append('<p class="t-a"><strong>Model answer:</strong> %s</p>' % html.escape(t['a']))
        if note: rows.append('<p class="t-note"><strong>%s</strong></p>' % note)
        rows.append('</div>')
    return '\n'.join(rows)
add = MARK + '\n'
add += '<div class="rules"><h3>The Sonnet canary (31 Aug)</h3><ul><li>Both units below were drafted end-to-end by <strong>Sonnet 5 subagents</strong> from the codified prompt, then reviewed. Tickets that were touched in review carry a note saying exactly what changed; everything else is untouched Sonnet output.</li><li>Scorecard &mdash; Biology (10): 0 factual errors, 2 register trims. Geography (20): 1 invented fact, 1 false-paradox pair (Tom\u2019s catch \u2014 now a pipeline rule), 1 register trim. 24 of 30 untouched.</li></ul></div>\n'
add += section('Biology Paper 1 (Unity Combined Science)', 'sci', 'science', 'biology-paper-1', '_out_science.json') + '\n'
add += section('Paper 1 Physical Geography (Unity)', 'geo', 'geography', 'paper-1', '_out_geography.json') + '\n</div>'
open(ART, 'w', encoding='utf-8').write(doc + add)
print('rebuilt', len(doc + add))
