# -*- coding: utf-8 -*-
"""Set window._currentProblem before the completion card can return past it.

    python scratchpad/_geo_guided/_fix_currentproblem_global.py

Tom, on L13: the completion card ("First one: finish it") showed no map, and a
hard refresh did not help. The data is clean on all six variants and showGuided
does render the panel, so it was being hidden again afterwards.

renderCurrentProblem() assigned window._currentProblem near its end, but the
completion branch returns well before that. switchView('practice') restores the
stimulus panel from that global and hides the panel when it is unset, so any
entry path that ends in switchView -- Start Practice, Back to examples -- wiped
the map that showGuided had just drawn. Only the first question of a tier, only
on the completion card, which is why it looked so arbitrary.

The global means "the problem currently on screen", so it belongs with the line
that decides which problem that is, not two hundred lines downstream past three
early returns. Moved up; the late assignment goes away rather than lingering as
a second source of truth.
"""
import io, sys

P = "practice.html"
s = io.open(P, encoding="utf-8").read()

OLD_EARLY = """      var p = items[idx];
      practiceState.answered = false;
"""
NEW_EARLY = """      var p = items[idx];
      practiceState.answered = false;
      // Set before any early return below. switchView() restores the stimulus
      // panel from this global and hides the panel when it is unset, so if the
      // completion branch returns without it, entering practice via Start
      // Practice or Back to examples hides the map that walk just rendered.
      window._currentProblem = p;
"""

OLD_LATE = """      // Handle passage panel (English Language types)
      window._currentProblem = p;
      handlePassagePanel(p);"""
NEW_LATE = """      // Handle passage panel (English Language types)
      handlePassagePanel(p);"""

for old, new, what in ((OLD_EARLY, NEW_EARLY, "early set"), (OLD_LATE, NEW_LATE, "late duplicate")):
    if old not in s:
        sys.exit("could not find the %s anchor" % what)
    if s.count(old) != 1:
        sys.exit("%s anchor is not unique (%d)" % (what, s.count(old)))
    s = s.replace(old, new, 1)

if s.count("window._currentProblem = p;") != 1:
    sys.exit("expected exactly one assignment after the move")

io.open(P, "w", encoding="utf-8").write(s)
print("window._currentProblem now set before the completion-card return")
