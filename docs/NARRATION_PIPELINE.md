# Narration Pipeline — TTS

Process for generating text-to-speech narration for lesson pages.

---

## Current Approach (Mar 2026)

**Azure Speech** (cloud API) with two alternating British English voices:
- **Odd lessons** (1, 3, 5, 7, 9...): `en-GB-OllieMultilingualNeural` (male)
- **Even lessons** (2, 4, 6, 8, 10...): `en-GB-BellaNeural` (female)

Speed: ~49 clips per minute (near-instant). A full 10-lesson subject generates in under 10 minutes.

**Auth**: `AZURE_SPEECH_KEY` env var + region `uksouth`. Free tier (F0) allows 0.5M chars/month. Standard tier (S0) needed for Dragon HD voices. Current setup uses S0 with $200 free Azure credit.

**WAV files are gitignored** — too large to commit. Cloudflare R2 recommended for hosting (free 10GB tier, zero egress). Before going live, set up R2 and update the manifest `src` paths to use R2 URLs.

---

## Narration Progress

| Unit | Lessons done | Voice | Notes |
|------|-------------|-------|-------|
| Sport Science R180 | 10/10 | Ollie (odd) + Bella (even) | Azure TTS, 350 clips, manifests with durations |
| Conflict & Tension 01–14 | 14/15 | Teacher clone (Qwen3) | Old approach, WAVs local only |
| Conflict & Tension 15 | partial | Teacher clone (Qwen3) | 1 audio clip generated |
| Health & People | 0/15 | — | Not started |
| Elizabethan | 0/15 | — | Not started |
| America | 0/15 | — | Not started |
| Business Theme 1 L01 | 1/30 | Teacher clone (Qwen3) | 33 clips, WAVs local only |

---

## Generation Process

1. Extract `data-narration-id` elements from lesson HTML
2. Parse text content, stripping HTML tags but preserving readable text
3. Insert sentence breaks (periods) after headings/labels inside container elements — ensures natural pauses between "Key Fact." and the body text, "Conclusion." and the paragraph, etc.
4. Generate per-chunk WAV files via Azure Speech API (24kHz, 16-bit mono PCM)
5. Update `window.narrationManifest` in the lesson HTML
6. Skip existing audio files (re-run safe)

Audio file naming: `narration_lesson-NN_nX.wav` (e.g. `narration_lesson-01_n1.wav`). Files live in the unit folder alongside lesson HTML.

---

## Script

`scripts/generate_azure_narration.py` — batch script for Azure Speech TTS.

Usage:
```bash
# Generate all 10 Sport Science lessons
python scripts/generate_azure_narration.py

# Generate specific lessons
python scripts/generate_azure_narration.py 1 3 5

# Generate a range
python scripts/generate_azure_narration.py 2 4 6 8 10
```

To adapt for other subjects, update `LESSON_DIR` at the top of the script.

Key features:
- HTML parser extracts text from `data-narration-id` elements, handling nested containers (conclusions, key facts, exam tips, collapsibles)
- Inserts natural pauses after headings/labels inside container chunks
- Strips HTML entities (mdash, rsquo, etc.) to clean text
- Skips already-generated WAV files
- Updates `window.narrationManifest` in lesson HTML automatically

---

## Models Tried

| Model | Result | Notes |
|-------|--------|-------|
| **Azure Speech** (Ollie + Bella) | **Current approach** | Near-instant generation, consistent voices, deterministic output. British English. Cheap ($16–30/1M chars). |
| **Kokoro TTS v1.0** (local ONNX) | Too robotic | 82M params, very fast on CPU, British voices available (`bf_emma`, `bf_isabella`). Voice quality not warm enough for lesson narration. |
| **Qwen3-TTS** (local AMD RX 6800) | Working but too slow | ~6x real-time on CPU. Acceptable voice quality with ICL voice cloning. Generated Conflict lessons 01–14. |
| **Qwen3-TTS** (RunPod RTX 4090) | Too slow | ~14x real-time. Stock `qwen-tts` barely uses GPU (3%). |
| **Chatterbox TTS** | Install failed | Pins numpy<1.26, incompatible with Python 3.12. Also bad voice cloning quality when tested previously. |
| **GPT-SoVITS v2Pro** (fine-tuned) | Mediocre + truncation | Trained on 6 min of teacher's voice. Consistently truncates output. |
| **Gemini TTS** (API) | Inconsistent voices | Good quality when it works, but voice changes between API calls — pitch, cadence, accent shift. Not suitable for multi-chunk narration. Preview status, may improve. |

---

## Legacy Infrastructure (Qwen3-TTS)

Kept for reference — Conflict & Tension lessons 01–14 were generated with this approach.

- `scripts/generate_narration.py` — batch script for Qwen3-TTS voice cloning
- `scripts/voice-reference/voice_sample_30s.wav` — 30s teacher reference clip
- `scripts/voice-reference/voice_sample.wav` — full 58.9s reference
- `scripts/runpod/` — RunPod cloud GPU deployment scripts

---

## Audio Hosting (TODO)

WAV files need hosting before narration can go live for students. Recommended: **Cloudflare R2** (free 10GB tier, zero egress fees). Steps:

1. Create R2 bucket
2. Upload WAV files with public read access
3. Update `window.narrationManifest` `src` paths in each lesson to use R2 URLs
4. Test playback via the narration player UI
