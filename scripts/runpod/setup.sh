#!/bin/bash
# RunPod setup for StudyVault TTS narration
# Run this once after pod starts and files are uploaded.
#
# Prerequisites: Use a RunPod "PyTorch 2.x" template (CUDA pre-installed).
# GPU recommendation: RTX 4090 ($0.44/hr) or RTX A4000 ($0.26/hr) — model is only 1.7B.

set -e

echo "=== StudyVault TTS — RunPod Setup ==="

# Install system dependencies
apt-get update && apt-get install -y ffmpeg sox

# Install optimized Qwen3-TTS fork (~6x faster than stock qwen-tts)
pip install soundfile
pip install git+https://github.com/dffdeeq/Qwen3-TTS-streaming.git
pip install flash-attn --no-build-isolation

# Verify GPU access
python -c "
import torch
if torch.cuda.is_available():
    name = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_mem / 1e9
    print(f'GPU ready: {name} ({vram:.1f} GB VRAM)')
else:
    print('WARNING: No GPU detected! Generation will be slow.')
"

# Verify voice sample exists
if [ -f voicebox-test/new\ test\ clone.m4a ]; then
    echo "Voice sample found."
else
    echo "ERROR: Voice sample not found at voicebox-test/new test clone.m4a"
    echo "Make sure you uploaded the full zip correctly."
    exit 1
fi

echo ""
echo "=== Setup complete! ==="
echo "Run: bash runpod/run_all.sh"
