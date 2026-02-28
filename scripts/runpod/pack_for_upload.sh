#!/bin/bash
# Run this LOCALLY (from your Study Vault directory) to create the upload zip.
# Usage: bash runpod/pack_for_upload.sh

set -e

echo "=== Packing files for RunPod upload ==="

tar czf runpod-upload.tar.gz \
    generate_narration.py \
    "voicebox-test/new test clone.m4a" \
    conflict-tension/lesson-*.html \
    health-people/lesson-*.html \
    elizabethan/lesson-*.html \
    america/lesson-*.html \
    runpod/setup.sh \
    runpod/run_all.sh \
    runpod/pack_results.sh

SIZE=$(du -h runpod-upload.tar.gz | cut -f1)
echo "Created: runpod-upload.tar.gz ($SIZE)"
echo ""
echo "Next steps:"
echo "  1. Upload this file to your RunPod pod"
echo "  2. On RunPod: cd /workspace && tar xzf runpod-upload.tar.gz"
echo "  3. On RunPod: bash runpod/setup.sh"
echo "  4. On RunPod: bash runpod/run_all.sh"
