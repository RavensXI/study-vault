#!/bin/bash
# Pack generated narration files for download.
# Creates narration_results.tar.gz with all WAV files + updated HTML manifests.

set -e

echo "=== Packing narration results ==="

# Count what we're packing
WAV_COUNT=$(find conflict-tension health-people elizabethan america -name "narration_*.wav" 2>/dev/null | wc -l)
echo "Found $WAV_COUNT narration WAV files"

# Create archive with WAVs and updated HTML files (manifests are embedded in HTML)
tar czf narration_results.tar.gz \
    conflict-tension/narration_*.wav \
    health-people/narration_*.wav \
    elizabethan/narration_*.wav \
    america/narration_*.wav \
    conflict-tension/lesson-*.html \
    health-people/lesson-*.html \
    elizabethan/lesson-*.html \
    america/lesson-*.html \
    2>/dev/null

SIZE=$(du -h narration_results.tar.gz | cut -f1)
echo ""
echo "Created: narration_results.tar.gz ($SIZE)"
echo "Download this file, then extract in your Study Vault directory:"
echo "  tar xzf narration_results.tar.gz"
