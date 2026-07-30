#!/usr/bin/env bash
# Drive the open-weights pilot from this machine over SSH.
#   bash scripts/_ow_pilot_drive.sh <ssh-port> <ssh-host> [user]
# e.g. bash scripts/_ow_pilot_drive.sh 12345 69.30.85.10 root
set -euo pipefail

PORT="$1"; HOST="$2"; USER="${3:-root}"
KEY="$HOME/.ssh/runpod_pilot"
SSH="ssh -i $KEY -p $PORT -o StrictHostKeyChecking=accept-new $USER@$HOST"
SCP="scp -i $KEY -P $PORT -o StrictHostKeyChecking=accept-new"
SCRATCH="/c/Users/tshau/AppData/Local/Temp/claude/C--Users-tshau-Documents-Study-Vault/b7ce0950-5850-4b5c-8f69-ce16ff3c08b6/scratchpad/_lw_pilot"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "== 1/4 push sources + runner =="
$SSH "mkdir -p /workspace/orig /workspace/out"
$SCP "$SCRATCH"/*-orig.png "$USER@$HOST:/workspace/orig/"
$SCP "$HERE/_ow_pilot_pod.py" "$USER@$HOST:/workspace/"

echo "== 2/4 install deps (idempotent) =="
$SSH "pip install -q --upgrade diffusers transformers accelerate safetensors pillow 2>&1 | tail -1 || true"

echo "== 3/4 run (model download ~40GB on first pass) =="
# HF cache MUST live on the 100GB volume — the 20GB container disk can't hold the model
$SSH "cd /workspace && HF_HOME=/workspace/hf python3 _ow_pilot_pod.py"

echo "== 4/4 pull outputs =="
$SCP "$USER@$HOST:/workspace/out/*-qwen.png" "$SCRATCH/" || true
ls "$SCRATCH"/*-qwen.png 2>/dev/null | wc -l
echo "done — remember to STOP the pod in the RunPod console"
