# Narration Pipeline — TTS Voice Cloning

Process for generating text-to-speech narration for lesson pages using voice cloning.

---

## Current Status (Feb 2026)

Qwen3-TTS (`Qwen3-TTS-12Hz-1.7B-Base`) running locally on AMD RX 6800 (CPU mode, ~6x real-time). Uses ICL voice cloning with a 30-second reference clip for accent preservation. CHUNK_TIMEOUT set to 600s (bumped from 300s to handle long paragraphs).

**WAV files are gitignored** — 19MB per lesson is too large to commit. Cloudflare R2 recommended for hosting (free 10GB tier, zero egress). Before narrating more lessons, set up R2 and update the manifest `src` paths to use R2 URLs.

---

## Narration Progress

| Unit | Lessons done | Notes |
|------|-------------|-------|
| Conflict & Tension 01–14 | 14/15 | Manifests populated, WAVs local only |
| Conflict & Tension 15 | partial | 1 audio clip generated |
| Health & People | 0/15 | Not started |
| Elizabethan | 0/15 | Not started |
| America | 0/15 | Not started |
| Business Theme 1 L01 | 1/30 | 33 clips, 7 min audio, WAVs local only |
| Sport Science | 0/10 | Not started |

---

## Generation Process

1. Extract `data-narration-id` elements from lesson HTML
2. Normalise text (strip HTML entities, handle special characters)
3. Build voice prompt from 30s reference clip (ICL mode)
4. Generate per-chunk WAV files
5. Update `window.narrationManifest` in the lesson HTML

Audio file naming: `narration_lesson-NN_nX.wav` (e.g. `narration_lesson-01_n1.wav`). Files live in the unit folder alongside lesson HTML (e.g. `conflict-tension/narration_lesson-01_n1.wav`).

---

## Voice Cloning Config

- **Reference audio**: `scripts/voice-reference/voice_sample_30s.wav` (30s crop of teacher reading, 24kHz mono)
- **ICL mode**: `x_vector_only_mode=False` with reference transcript in `REF_TEXT` constant — preserves Lancashire accent
- **Model**: `Qwen/Qwen3-TTS-12Hz-1.7B-Base` via `qwen-tts` package
- 10s clip was too thin (accent lost), 59s was too slow to process on CPU. 30s is the sweet spot.

---

## Models Tried

| Model | Result | Notes |
|-------|--------|-------|
| **Qwen3-TTS** (local AMD RX 6800) | **Working — current approach** | Acceptable voice quality. Slow generation but functional. Generated Conflict lessons 01–10 locally. |
| **Qwen3-TTS** (RunPod RTX 4090) | Too slow | ~14x real-time. Stock `qwen-tts` barely uses GPU (3%). Community fork (`dffdeeq/Qwen3-TTS-streaming`) tried with `torch.compile` — spent 30+ min compiling, never finished. |
| **Chatterbox TTS** | Bad voice quality | Fast generation but terrible voice cloning — "someone doing a bad English accent". Zero-shot cloning doesn't work for every voice. |
| **GPT-SoVITS v2Pro** (fine-tuned) | Mediocre + truncation | Trained on 6 min of teacher's voice. Voice somewhat recognisable but not convincing. Consistently truncates output. Chinese-first model. |

**Not yet tried:**
- **KaniTTS-2** — 400M param model, RTF ~0.2 on RTX 5080, zero-shot voice cloning via 128-dim speaker embeddings (WavLM). `pip install kani-tts-2`. Standard PyTorch so AMD/ROCm should work in principle. Flagged by research-tts agent 20 Feb 2026.
- **F5-TTS** — English-focused, good voice cloning reported, 15x real-time on GPU.
- **Professional narration** — hire a narrator or use a non-cloned AI voice.

---

## Infrastructure

- `scripts/generate_narration.py` — batch script wired for Qwen3-TTS. Extracts `data-narration-id` text from HTML, generates per-chunk WAV via ICL voice cloning, updates `window.narrationManifest`. Skips existing audio files. Has UTF-8 encoding fix for Windows.
- `scripts/voice-reference/voice_sample_30s.wav` — 30s reference clip (the one that works)
- `scripts/voice-reference/voice_sample.wav` — full 58.9s reference (too slow for CPU prompt building)
- `scripts/voice-reference/new test clone.m4a` — original 30s voice sample (m4a format)
- `scripts/voice-reference/new test appeasement.m4a` — 6 min voice sample (teacher reading lesson content)
- `runpod/` — setup scripts for RunPod cloud GPU (setup.sh, run_all.sh, pack_for_upload.sh, pack_results.sh)
- `test_gptsovits.py` — standalone GPT-SoVITS inference script

---

## Research Logs

The `research-tts` OpenClaw agent runs daily at 8am and writes findings to `tts-research-log.md` in the project root. Read this file before making TTS decisions — it tracks new model releases, benchmarks, and AMD compatibility.

---

## Audio Hosting (TODO)

WAV files need hosting before narration can go live for students. Recommended: **Cloudflare R2** (free 10GB tier, zero egress fees). Steps:

1. Create R2 bucket
2. Upload WAV files with public read access
3. Update `window.narrationManifest` `src` paths in each lesson to use R2 URLs
4. Test playback via the narration player UI
