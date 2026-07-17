import json

# 1. Sync the _diagrams shard to the patched live content so both shards match live.
pd = json.load(open("lesson_maths-eduqas_algebra-L13.json", encoding="utf-8"))
json.dump(pd, open("lesson_maths-eduqas_algebra-L13_diagrams.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

# 2. Write a revision changes file documenting this pass.
rev = {
    "key": "maths-eduqas_algebra-L13",
    "pass": "revision-after-check",
    "defects_fixed": [
        {
            "path": "guided.teach.bronze.display (SVG)",
            "severity": "fatal (figure)",
            "what": "viewBox was '0 0 285 78' but pattern-3's 7th dot sits at cx=288 r=5 (spans x=283-293), so its centre lay outside the 285-wide viewBox and it was clipped by overflow:hidden. Figure rendered 6 dots + a sliver while the label and aria-label both say 'Pattern 3: 7'.",
            "fix": "Widened viewBox to '0 0 300 78'. All 7 dots of pattern 3 now render fully; figure matches its label and the walk's 3,5,7 count. No dot coordinates changed; walk maths (d=2, rule 2n+1) untouched.",
            "old": "viewBox=\"0 0 285 78\"",
            "new": "viewBox=\"0 0 300 78\""
        },
        {
            "path": "problem_bank.silver[2].options",
            "severity": "minor (non-fatal)",
            "what": "options[1] '20 - 3n' and options[2] '-3n + 20' were algebraically identical (both 20-3n). Only options[1] fired the used_first_term diagnosis (expect:1); a click on the equal options[2] showed no diagnosis.",
            "fix": "Replaced options[2] with a genuinely distinct distractor '17 - 3n' (constant found by first term PLUS d = 20+(-3)=17 instead of first term MINUS d = 20-(-3)=23; wrong, at n=1 gives 14 not 20). Added an honest misconception (pattern added_d_to_first_term, expect:2) so the new distractor is diagnosed. All four options now distinct; correct answer still index 0 (23-3n).",
            "old": ["\\(23 - 3n\\)", "\\(20 - 3n\\)", "\\(-3n + 20\\)", "\\(3n + 20\\)"],
            "new": ["\\(23 - 3n\\)", "\\(20 - 3n\\)", "\\(17 - 3n\\)", "\\(3n + 20\\)"]
        }
    ],
    "preserved": "worked_examples[2] (Gold-labelled bronze-level nth-term task) left byte-for-byte as-is per checker note: it matched the pre-dump and was not introduced this conversion. All 20 bank solutions, guided walks, openers, teach boxes and other misconception expects untouched.",
    "validator": "PASS (structure, style, budgets all clean)",
    "patched_live": True,
    "notes": "Revision worked from a fresh live fetch (_eduqas_L13_live.json); only the two flagged fields were edited, then re-validated and PATCHed. Round-trip verified: viewBox 300 live, silver[2] four distinct options, expects [1,3,2], solutions [0]."
}
json.dump(rev, open("changes_maths-eduqas_algebra-L13_revision.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("synced diagrams shard + wrote changes_maths-eduqas_algebra-L13_revision.json")
