"""Single-text questions in English Language 2.0 were marked with the two-text "compare" rubric (22 Sep 2026).

The generated Paper 2 reading lessons were given one marking prompt, 'compare', and 21 single-text
analysis and evaluation questions pointed at it, so the marker judged them against a scheme about two
writers (the student walk's adjudicator caught it: praise for being "even-handed" on a one-text answer).
Three rubrics in the house format, written for contemporary fiction and literary non-fiction alike:
language_structure, structure_analysis, evaluation.

  python scripts/_fix_englang2_rubrics.py [--apply]
"""
import io, json, os, re, sys, time, urllib.request
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
CONTRACT = ('Respond in JSON: {"quality":"excellent|good|needs_work|not_valid","feedback":"2-3 sentences, giving the mark out of the marks available",'
            '"improvement":"one sentence on what would raise it"}\n\n'
            'Also include a "misconception" field in your JSON response. If the student\'s answer shows one of these error patterns AND you can point '
            'to the exact place it happens, set it to that tag; otherwise set it to "none". Choose ONLY from: no-evidence-quoted, feature-spotting-no-effect, '
            'misread-question-focus, retell-not-analyse, informal-register, unfocused-answer, wrong-text-referenced, assertion-without-support. '
            'Never invent a tag that is not on this list.')
RUBRICS = {
 "language_structure": """You are a GCSE English Language tutor. The student is analysing how ONE writer uses language and/or structure in a single extract (contemporary fiction or literary non-fiction). Mark their response using these levels:

- Mastering (excellent): Perceptive, detailed analysis of the writer's choices of language and/or structure; precise, well-chosen references; effects on the reader explained with insight; stays tightly on the focus of the question.
- Secure (good): Clear explanation of the writer's methods with relevant references and some explanation of effect.
- Developing (needs_work): Identifies some methods or details but explains effect thinly, or drifts from the question's focus.
- Emerging (not_valid): Retells or describes the extract without analysing how it is written.

This is a single-text question: do not expect or reward comparison with another text. Naming a word or phrase without quotation marks is valid evidence. Do not require a set structure or named terminology. Be encouraging. """ + CONTRACT,
 "structure_analysis": """You are a GCSE English Language tutor. The student is analysing how ONE writer structures a single extract (contemporary fiction or literary non-fiction). Mark their response using these levels:

- Mastering (excellent): Perceptive analysis of how the extract is organised across the whole — openings, shifts in focus or time, contrasts, endings — and precisely why those choices shape the reader's response.
- Secure (good): Identifies structural choices with evidence and some explanation of their effect.
- Developing (needs_work): Notices what comes first or last but says little about why the writer ordered it that way.
- Emerging (not_valid): Retells the extract in order without commenting on structure.

This is a single-text question: do not expect or reward comparison with another text. Reward understanding of WHY the structure matters, not just what happens where. Be encouraging. """ + CONTRACT,
 "evaluation": """You are a GCSE English Language tutor. The student is evaluating ONE extract against a statement about it ("To what extent do you agree?"). Mark their response using these levels:

- Mastering (excellent): A clear, sustained evaluative judgement on the statement; analyses how the writer's methods create the effect; well-chosen evidence; may weigh up alternative readings.
- Secure (good): Takes a position on the statement and supports it with relevant evidence and some comment on method.
- Developing (needs_work): Agrees or disagrees with limited justification, or describes rather than evaluates.
- Emerging (not_valid): No real evaluation; retells the extract.

Agreeing, disagreeing or partly agreeing are all valid if supported. This is a single-text question: do not expect comparison with another text. Be encouraging. """ + CONTRACT,
}
CMP = re.compile(r"\bcompar|\bboth (texts|sources|writers|extracts)|\bSource[s]? [A-E]\b.*\bSource [A-E]\b|two (texts|writers|sources)", re.I)
def get(p): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + p, headers=H), timeout=240).read())
apply = "--apply" in sys.argv
rows = get("lessons?select=id,lesson_number,practice_data,units!inner(slug,subject_id)&units.subject_id=eq.b6ecfffe-69da-4f15-9bb4-b69e4f54edc8&limit=200")
backup, n = {}, 0
for r in rows:
    pd = r["practice_data"]; before = json.dumps(pd, ensure_ascii=False)
    for t, qs in pd["problem_bank"].items():
        for i, q in enumerate(qs):
            s = q.get("question") or ""
            if q.get("ai_prompt_key") != "compare" or CMP.search(s): continue
            key = ("evaluation" if re.search(r"evaluat|how far do you agree|to what extent", s, re.I) else
                   "structure_analysis" if re.search(r"structur", s, re.I) and not re.search(r"language", s, re.I) else "language_structure")
            q["ai_prompt_key"] = key
            pd.setdefault("ai_marking_prompts", {})[key] = RUBRICS[key]
            n += 1
            print("%-22s %-6s %d -> %s" % ("%s/%s" % (r["units"]["slug"], r["lesson_number"]), t, i, key))
    if json.dumps(pd, ensure_ascii=False) != before:
        backup[r["id"]] = json.loads(before)
        if apply:
            urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/lessons?id=eq." + r["id"], data=json.dumps({"practice_data": pd}).encode(),
                headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()
print("%d questions re-pointed in %d lessons%s" % (n, len(backup), "" if apply else " (dry run)"))
if apply:
    p = "scripts/_backup_englang2_rubrics_%s.json" % time.strftime("%Y-%m-%d")
    io.open(p, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False)); print("backup:", p)
