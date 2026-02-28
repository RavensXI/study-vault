#!/bin/bash
# Run narration generation for all 60 History lessons.
# The script auto-skips already-generated WAV files, so it's safe to re-run.
#
# Usage:
#   bash runpod/run_all.sh          # all 60 lessons
#   bash runpod/run_all.sh health   # just one unit

set -e

UNIT="${1:-all}"

case "$UNIT" in
    conflict)
        FILES="conflict-tension/lesson-*.html"
        ;;
    health)
        FILES="health-people/lesson-*.html"
        ;;
    elizabethan)
        FILES="elizabethan/lesson-*.html"
        ;;
    america)
        FILES="america/lesson-*.html"
        ;;
    all)
        FILES="conflict-tension/lesson-*.html health-people/lesson-*.html elizabethan/lesson-*.html america/lesson-*.html"
        ;;
    *)
        echo "Usage: bash runpod/run_all.sh [conflict|health|elizabethan|america|all]"
        exit 1
        ;;
esac

echo "=== StudyVault TTS — Generating narration ==="
echo "Units: $UNIT"
echo ""

python generate_narration.py $FILES

echo ""
echo "=== Done! Pack results with: bash runpod/pack_results.sh ==="
