"""Fix 3 (Enid's marriage) plus the Frankenstein L2 follow-on.

FIX 3 RULING — Enid ENDED the marriage; she was not abandoned.
  Oak National Academy, AQA Scene 7 lesson: "Brod tells Del that her mother
  left her father to protect her and Viv." Its exit quiz marks correct:
  "Enid left him to protect her children; Her husband was abusive."
  The Eduqas twin lesson states it against the alternative outright:
  "Enid left her husband to protect her children, not the other way around."
  Shalom Education: "She ended it because she didn't want her children to be
  exposed to her husband's physically abusive behaviour."
  The "abandoned" wording traces to Nick Hern Books' marketing blurb, and to
  the fact that the play deliberately sustains that misreading until Scene 7 —
  Del spends the play blaming her mother for driving her father away.

  => leave-taking L3 ("Enid eventually left him") is CORRECT — left untouched.
  => leave-taking L5 ("She was abandoned by her husband") is WRONG — rewritten,
     keeping the dramatic reversal Scene 7 delivers.

FIX 1b — Frankenstein L2 n13 repeats the L6 error: it says Shelley leaves
  Walton's choice ambiguous. Walton agrees to turn back. Corrected so the two
  lessons agree.
"""

LT_L5 = "dfc930cd-8246-46cc-9d9b-4fc16885d08e"
FRANK_L2 = "07d83404-fde9-43ab-8461-2064e8bb282b"

EDITS3 = [
    # Leave Taking uses STRAIGHT apostrophes; Frankenstein uses CURLY. Preserved.
    (3, LT_L5, "content_html",
     "She was abandoned by her husband after he subjected her to domestic "
     "violence — cruelty rooted in the racism and humiliation he suffered at "
     "work. Brod discloses this to Del in Scene 7.",
     "Her husband subjected her to domestic violence — cruelty rooted in the "
     "racism and humiliation he suffered at work — and Enid ended the marriage "
     "to protect her daughters. Brod discloses this to Del in Scene 7, "
     "overturning the assumption Del has carried for years that her mother "
     "drove her father away.",
     "n3 — Enid ended the marriage; she was not abandoned (ruling in docstring)"),

    (1, FRANK_L2, "content_html",
     "At the novel’s end, Walton’s crew demand they return south. Whether "
     "Walton heeds Victor’s cautionary tale determines whether the cycle of "
     "destruction continues. Shelley leaves this ambiguous — will humanity "
     "learn from its mistakes?",
     "At the novel’s end, Walton’s crew demand they return south — and Walton "
     "agrees, abandoning the expedition. He is the one man in the novel who "
     "heeds the warning in time, which is why Shelley gives him the last word. "
     "Whether humanity at large will learn from its mistakes is the question "
     "he leaves with the reader.",
     "n13 — same Walton error as L6: he agrees to turn back, not left ambiguous"),
]
