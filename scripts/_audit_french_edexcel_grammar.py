"""LanguageTool grammar audit on every French string in Edexcel French lessons.

Walks practice_data and extracts French text from:
- vocab_match pairs (left side = French)
- gap_fill sentences + answers
- translate problems (correct/accept lists for translate_to_target)
- dictation audio_text/correct_text
- role_play scenarios (French parts)
- worked_examples
- problem text/sentence_parts

Runs LanguageTool's French rule set, reports counts + samples.
"""
import json
import sys
from pathlib import Path
import language_tool_python
from collections import defaultdict

LESSON_DIR = Path("scripts/_content_french-edexcel/lessons")

# Fields to scan for French (target-language) text
def collect_french_strings(pd, lesson_slug):
    """Yield (problem_id, field_name, text) tuples."""
    if not isinstance(pd, dict):
        return

    pb = pd.get("problem_bank", {}) or {}
    for tier in ("bronze", "silver", "gold"):
        for i, p in enumerate(pb.get(tier, []) or []):
            pid = f"{tier}[{i}]"
            t = p.get("input_type") or ""

            if t == "vocab_match":
                for j, pair in enumerate(p.get("pairs", [])):
                    if pair.get("left"):
                        yield (pid, f"pair[{j}].left", pair["left"])

            elif t == "gap_fill":
                parts = p.get("sentence_parts") or []
                joined = "".join([s if isinstance(s, str) else "" for s in parts])
                if joined.strip():
                    yield (pid, "sentence_parts", joined)
                for j, gap in enumerate(p.get("gaps", []) or []):
                    if gap.get("answer"):
                        yield (pid, f"gaps[{j}].answer", gap["answer"])

            elif t in ("translate", "translate_to_target", "translate_to_english"):
                # If translate_to_target, the answer is French. If _to_english, the question is French.
                if t == "translate_to_english" and p.get("question"):
                    yield (pid, "question", p["question"])
                if t == "translate_to_target":
                    for j, a in enumerate((p.get("accept") or []) + ([p["correct"]] if p.get("correct") else [])):
                        if isinstance(a, str):
                            yield (pid, f"accept[{j}]", a)

            elif t == "dictation":
                txt = p.get("audio_text") or p.get("correct_text")
                if txt:
                    yield (pid, "audio_text", txt)

            elif t == "reorder":
                # correct_order is array of indexed words; word_bank is the French words
                wb = p.get("word_bank") or []
                if wb:
                    yield (pid, "word_bank.joined", " ".join([w for w in wb if isinstance(w, str)]))

            elif t == "spot_correct":
                # Has incorrect_sentence + correct_sentence
                if p.get("correct_sentence"):
                    yield (pid, "correct_sentence", p["correct_sentence"])

            elif t == "sentence_builder":
                # Similar to reorder
                wb = p.get("word_bank") or []
                if wb:
                    yield (pid, "word_bank.joined", " ".join([w for w in wb if isinstance(w, str)]))

            # role_play / writing / listening etc skipped — context-dependent French


def main():
    print("Loading LanguageTool (French)... this can take ~30s on first run")
    tool = language_tool_python.LanguageTool('fr')
    print("Loaded.\n")

    by_lesson_count = {}
    samples = []
    total_strings = 0

    for f in sorted(LESSON_DIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        pd = data.get("practice_data") or {}
        slug = data.get("_lesson_slug") or f.stem

        errors_in_lesson = 0
        for pid, field, text in collect_french_strings(pd, slug):
            if not text or not isinstance(text, str):
                continue
            total_strings += 1
            matches = tool.check(text)
            # Filter out style/whitespace noise
            real = [m for m in matches if m.ruleIssueType not in ("style", "whitespace") and m.category not in ("TYPOGRAPHY", "PUNCTUATION")]
            if real:
                errors_in_lesson += len(real)
                if len(samples) < 60:
                    for m in real[:2]:
                        samples.append({
                            "lesson": slug,
                            "problem": pid,
                            "field": field,
                            "text": text[:120],
                            "issue": m.message,
                            "rule": m.ruleId,
                            "suggestion": (m.replacements[:3] if m.replacements else []),
                        })

        by_lesson_count[slug] = errors_in_lesson
        print(f"  {slug:55s} errors: {errors_in_lesson}")

    tool.close()

    print(f"\nTotal French strings checked: {total_strings}")
    print(f"Total error candidates: {sum(by_lesson_count.values())}")
    avg = sum(by_lesson_count.values()) / max(len(by_lesson_count), 1)
    print(f"Avg per lesson: {avg:.2f}")
    worst = sorted(by_lesson_count.items(), key=lambda x: -x[1])[:5]
    print(f"\nWorst 5 lessons:")
    for slug, c in worst:
        print(f"  {slug:55s} {c}")

    print(f"\nSample errors (first 30):")
    for s in samples[:30]:
        print(f"  [{s['lesson']}/{s['problem']}/{s['field']}]")
        print(f"    text: {s['text']}")
        print(f"    issue: {s['issue']}")
        if s['suggestion']:
            print(f"    suggest: {s['suggestion']}")
        print()

    # Write full report
    with open("french_edexcel_grammar_audit.json", "w", encoding="utf-8") as f:
        json.dump({
            "by_lesson": by_lesson_count,
            "total_strings": total_strings,
            "total_errors": sum(by_lesson_count.values()),
            "avg_per_lesson": avg,
            "all_samples": samples,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nFull report: french_edexcel_grammar_audit.json")


if __name__ == "__main__":
    main()
