# Narration Pipeline — TTS

> **API Integration:** This document is read by the orchestration code to configure Azure Speech API calls. It is not sent to an LLM — narration is deterministic TTS generation.

Process for generating text-to-speech narration for lesson pages.

---

## Current Approach (Mar 2026)

**Azure Speech** (cloud API) with two alternating British English voices:
- **Odd lessons** (1, 3, 5, 7, 9...): `en-GB-OllieMultilingualNeural` (male)
- **Even lessons** (2, 4, 6, 8, 10...): `en-GB-BellaNeural` (female)

Speed: ~49 clips per minute (near-instant). A full 10-lesson subject generates in under 10 minutes. All 130 History/Business/Geography lessons generated in ~20 minutes using 8 parallel agents.

**Auth**: `AZURE_SPEECH_KEY` env var + region `uksouth`. Standard tier (S0) with $200 free Azure credit. $16 per 1M characters.

**Output format**: MP3 directly from Azure (96kbps, 24kHz, mono). No WAV conversion needed.

---

## Narration Progress

**All 140 lessons fully narrated.** ~4,600 MP3 clips total, hosted on Cloudflare R2.

| Unit | Lessons | Clips | Voice | Status |
|------|---------|-------|-------|--------|
| Conflict & Tension | 15/15 | ~450 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Health & People | 15/15 | ~450 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Elizabethan | 15/15 | ~450 | Ollie (odd) + Bella (even) | Complete, on R2 |
| America | 15/15 | ~450 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Business Theme 1 | 15/15 | ~500 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Business Theme 2 | 15/15 | ~450 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Geography Paper 1 | 20/20 | ~600 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Geography Paper 2 | 20/20 | ~600 | Ollie (odd) + Bella (even) | Complete, on R2 |
| Sport Science R180 | 10/10 | 350 | Ollie (odd) + Bella (even) | Complete, on R2 |

---

## Generation Process

1. Extract `data-narration-id` elements from lesson HTML
2. Parse text content, stripping HTML tags but preserving readable text
3. Insert sentence breaks (periods) after headings/labels inside container elements — ensures natural pauses between "Key Fact." and the body text, "Conclusion." and the paragraph, etc.
4. Generate per-chunk MP3 files via Azure Speech API (96kbps, 24kHz, mono)
5. Calculate MP3 duration from MPEG frame headers (no external library needed)
6. Update `window.narrationManifest` in the lesson HTML with filenames and durations
7. Skip existing audio files (re-run safe)

Audio file naming: `narration_lesson-NN_nX.mp3` (e.g. `narration_lesson-01_n1.mp3`). Files live in the unit folder alongside lesson HTML (gitignored — hosted on R2).

---

## Scripts

### `scripts/generate_azure_narration.py`

Batch TTS generator using Azure Speech. Outputs MP3 directly.

Usage:
```bash
# Generate all lessons in a unit directory (auto-detects lesson-NN.html files)
python scripts/generate_azure_narration.py --dir history/conflict-tension

# Generate specific lessons only
python scripts/generate_azure_narration.py --dir geography/paper-1 1 5 10

# Generate all Sport Science lessons
python scripts/generate_azure_narration.py --dir sport-science/r180
```

Key features:
- `--dir` argument accepts any subject/unit path relative to project root
- Auto-detects all `lesson-NN.html` files if no lesson numbers specified
- HTML parser extracts text from `data-narration-id` elements, handling nested containers (conclusions, key facts, exam tips, collapsibles)
- Inserts natural pauses after headings/labels inside container chunks
- Strips HTML entities (mdash, rsquo, rarr, pound, euro, etc.) to clean text
- Skips already-generated MP3 files (idempotent)
- Updates `window.narrationManifest` in lesson HTML automatically
- Per-lesson timing and character count summary with cost estimate
- Windows UTF-8 console encoding fix built in

### `scripts/convert_wav_to_mp3.py`

Batch converter for legacy WAV files to MP3 using ffmpeg.

```bash
python scripts/convert_wav_to_mp3.py              # Convert all, delete WAVs
python scripts/convert_wav_to_mp3.py --keep-wav    # Convert all, keep WAVs
```

Converts at 96kbps/24kHz/mono via libmp3lame. Typically achieves ~75% size reduction.

### `scripts/upload_to_r2.py`

Upload all narration MP3s to Cloudflare R2.

```bash
python scripts/upload_to_r2.py              # Upload all MP3s
python scripts/upload_to_r2.py --dry-run    # Show what would be uploaded
```

Requires env vars: `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID`. Lists existing R2 objects to skip re-uploads (idempotent). Uploads with `ContentType: audio/mpeg`.

---

## Audio Hosting — Cloudflare R2

All narration MP3s are hosted on **Cloudflare R2** (S3-compatible object storage, zero egress fees).

- **Bucket**: `studyvault-audio`
- **Public URL**: `https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev`
- **Example**: `https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history/conflict-tension/narration_lesson-01_n1.mp3`
- **Total size**: ~834 MB across ~4,600 files
- **Free tier**: 10 GB storage, 10M reads/month, zero egress — well within limits

File organisation on R2 mirrors local paths:
```
history/conflict-tension/narration_lesson-01_n1.mp3
business/theme-1/narration_lesson-01_n1.mp3
geography/paper-1/narration_lesson-01_n1.mp3
sport-science/r180/narration_lesson-01_n1.mp3
```

Each lesson's `window.narrationManifest` contains entries like:
```js
{ id: "n1", src: "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history/conflict-tension/narration_lesson-01_n1.mp3", duration: 12.34 },
```

### Adding narration for new lessons

1. Generate MP3s: `python scripts/generate_azure_narration.py --dir subject/unit`
2. Upload to R2: `python scripts/upload_to_r2.py`
3. Update manifest URLs: run the sed/regex to replace local filenames with R2 URLs (or update `upload_to_r2.py` to do this automatically)

---

## Models Tried

| Model | Result | Notes |
|-------|--------|-------|
| **Azure Speech** (Ollie + Bella) | **Current approach** | Near-instant generation, consistent voices, deterministic output. British English. Cheap ($16–30/1M chars). |
| **Kokoro TTS v1.0** (local ONNX) | Too robotic | 82M params, very fast on CPU, British voices available (`bf_emma`, `bf_isabella`). Voice quality not warm enough for lesson narration. |
| **Qwen3-TTS** (local AMD RX 6800) | Working but too slow | ~6x real-time on CPU. Acceptable voice quality with ICL voice cloning. Generated Conflict lessons 01–14 (legacy, since regenerated with Azure). |
| **Qwen3-TTS** (RunPod RTX 4090) | Too slow | ~14x real-time. Stock `qwen-tts` barely uses GPU (3%). |
| **Chatterbox TTS** | Install failed | Pins numpy<1.26, incompatible with Python 3.12. Also bad voice cloning quality when tested previously. |
| **GPT-SoVITS v2Pro** (fine-tuned) | Mediocre + truncation | Trained on 6 min of teacher's voice. Consistently truncates output. |
| **Gemini TTS** (API) | Inconsistent voices | Good quality when it works, but voice changes between API calls — pitch, cadence, accent shift. Not suitable for multi-chunk narration. Preview status, may improve. |

---

## Legacy Infrastructure (Qwen3-TTS)

Kept for reference — Conflict & Tension lessons 01–14 were originally generated with this approach but have since been regenerated with Azure Speech.

- `scripts/generate_narration.py` — batch script for Qwen3-TTS voice cloning
- `scripts/voice-reference/voice_sample_30s.wav` — 30s teacher reference clip
- `scripts/voice-reference/voice_sample.wav` — full 58.9s reference
- `scripts/runpod/` — RunPod cloud GPU deployment scripts
