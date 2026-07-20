# -*- coding: utf-8 -*-
"""Question-card polish + answer units.

Run from the worktree root:  python scratchpad/_geo_guided/_apply_card_polish.py

Written as a file, not a heredoc: the formatDisplay patches contain regex
backslashes, which do not survive a shell heredoc.
"""
import io, sys

P = 'practice.html'
s = io.open(P, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    if old not in s:
        sys.exit('NOT FOUND: ' + label)
    s = s.replace(old, new, 1)
    done.append(label)


# ---------------------------------------------------------------- alignment
sub("""    .problem-tier-desc {
      font-family: 'Inter', sans-serif;
      font-size: 0.78rem;
      color: var(--text-muted, #8a8580);
      text-align: right;
      margin: -0.35rem 0 0.75rem;
    }""",
    """    /* Everything in the question card shares one centred axis and a measure.
       This line used to be right-aligned, which read as detached from the card
       and made a third alignment in a stack of three. */
    .problem-tier-desc {
      font-family: 'Inter', sans-serif;
      font-size: 0.78rem;
      color: var(--text-muted, #8a8580);
      text-align: center;
      max-width: 36rem;
      margin: -0.35rem auto 1.1rem;
      text-wrap: pretty;
    }""", 'tier-desc centred')

sub("""    .problem-equation {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 1.75rem;
      font-weight: 700;
      text-align: center;
      margin-bottom: 0.5rem;
      min-height: 2.5rem;
      line-height: 1.4;
    }""",
    """    .problem-equation {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 1.75rem;
      font-weight: 700;
      text-align: center;
      /* centred display type needs a short measure, or the rags go wild and a
         two-sentence question looks accidental */
      max-width: 28rem;
      margin: 0 auto 0.75rem;
      min-height: 2.5rem;
      line-height: 1.32;
      text-wrap: balance;
    }
    /* the instruction sentence, split out by formatDisplay */
    .problem-equation .q-instr { display: block; margin-top: 0.5em; }""",
    'question measure + balance')

sub("""    .problem-hint {
      font-size: 0.82rem;
      color: var(--text-muted, #8a8580);
      font-style: italic;
      text-align: center;
      margin-bottom: 1rem;
    }""",
    """    .problem-hint {
      font-size: 0.82rem;
      color: var(--text-muted, #8a8580);
      font-style: italic;
      text-align: center;
      max-width: 32rem;
      margin: 0 auto 1.25rem;
      text-wrap: pretty;
    }
    /* the unit the answer is given in, beside the box */
    .problem-answer-unit {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--text-muted, #8a8580);
      margin-left: 0.55rem;
      white-space: nowrap;
    }
    body.dark-mode .problem-answer-unit { color: #a89e93; }""",
    'hint measure + unit style')

# ---------------------------------------------------- formatDisplay: no blank line
old_rule = ("      // 2. Line break before instruction sentences (Explain, Calculate, Find, etc.)\n"
            r"      text = text.replace(/\.\s+(Explain|Calculate|Find|State|Describe|Compare|Suggest|Evaluate|Identify|Give|Work out|Determine|Using|What|Which|How|Why)\b/g, '.<br><br>$1');")
new_rule = ("      // 2. The instruction sentence starts its own block. This used to emit\n"
            "      //    <br><br>, a full blank line: fine in small body text, but in\n"
            "      //    centred 1.75rem display type it reads as a mistake. Mark it here\n"
            "      //    and turn the marks into balanced spans once LaTeX is restored.\n"
            r"      text = text.replace(/\.\s+(Explain|Calculate|Find|State|Describe|Compare|Suggest|Evaluate|Identify|Give|Work out|Determine|Using|What|Which|How|Why)\b/g, '.\x01$1');")
sub(old_rule, new_rule, 'formatDisplay instruction break')

old_restore = ("      // Restore LaTeX\n"
               r"      text = text.replace(/\x00LATEX(\d+)\x00/g, function(_, i) { return latexSlots[i]; });"
               "\n      return text;")
new_restore = ("      // Restore LaTeX\n"
               r"      text = text.replace(/\x00LATEX(\d+)\x00/g, function(_, i) { return latexSlots[i]; });"
               "\n      if (text.indexOf('\\x01') !== -1) {\n"
               "        var parts = text.split('\\x01');\n"
               "        text = parts.shift() + parts.map(function (seg) {\n"
               "          return '<span class=\"q-instr\">' + seg + '</span>';\n"
               "        }).join('');\n"
               "      }\n"
               "      return text;")
sub(old_restore, new_restore, 'formatDisplay span wrap')

io.open(P, 'w', encoding='utf-8').write(s)
print('applied:')
for d in done:
    print('  -', d)
