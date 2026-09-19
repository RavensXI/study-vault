"""Build the typed flashcard deck for one subject, end to end. Runs after Phase 3 content and
the fact-check, on lessons at any status (new subjects sit at pending_review until Tom flips).

  python scripts/flashcards/build_deck.py --subject latin-eduqas [--status pending_review] [--school-id X]

Steps (each is its own script, each re-runnable):
  1. generate  term / definition / cloze cards from the glossary and sentences   (build_recall_cards.py)
  2. author    list / explain cards on the Batch API, Sonnet, thinking off       (author_recall_cards_batch.py submit -> collect)
  3. gate      every authored card checked by Jev against its lesson            (gate_authored_cards.py)
  4. load      passing cards into lessons.recall_cards                          (load_authored.py)
  5. curate    the whole deck judged and trimmed to 14 by the teacher rating    (curate_recall_cards.py --apply)
The batch step waits for the Batch API (usually 5-30 minutes for one subject).
"""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
a = sys.argv[1:]
if "--subject" not in a: print(__doc__); sys.exit(1)
subject = a[a.index("--subject") + 1]
school = a[a.index("--school-id") + 1] if "--school-id" in a else None
status = a[a.index("--status") + 1] if "--status" in a else "live"
scope = ["--subject", subject, "--status", status] + (["--school-id", school] if school else [])
tag = ("unity__" if school else "") + subject
env = dict(os.environ, PYTHONIOENCODING="utf-8")

def run(*cmd, check=True):
    print("\n>>", " ".join(cmd), flush=True)
    r = subprocess.run([sys.executable] + list(cmd), cwd=ROOT, env=env)
    if check and r.returncode: sys.exit("step failed: " + " ".join(cmd))
    return r.returncode

gated = os.path.join(HERE, "_authored", tag + ".json")
if os.path.exists(gated): os.remove(gated)          # a stale result file would end the wait early
run("scripts/flashcards/build_recall_cards.py", *scope)
run("scripts/flashcards/author_recall_cards_batch.py", "submit", *scope)
while True:
    run("scripts/flashcards/author_recall_cards_batch.py", "collect", *scope)
    if os.path.exists(gated): break
    time.sleep(60)
run("scripts/flashcards/gate_authored_cards.py", gated)
run("scripts/flashcards/load_authored.py", gated.replace(".json", ".gated.json"))
run("scripts/flashcards/curate_recall_cards.py", *scope, "--apply")
print("\ndeck built for", subject, "| records: scripts/flashcards/_authored/curation_%s.json" % tag)
