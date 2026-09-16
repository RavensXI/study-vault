"""Build the narration clips for the mitosis animation.

One MP3 per scene, Azure Speech, house format (24 kHz, 96 kbps, mono).
Voice: Ada (the site's even-lesson female voice) - the cell cycle sits in
lesson 2 of science-aqa / biology-paper-1, which is an even lesson.

    python animations/mitosis/build_audio.py

Writes animations/mitosis/audio/scene-NN.mp3 and audio/manifest.json.
The page reads durations from the Audio elements at load; the manifest is
a record for the README and for the verification pass.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.lib.narration import (  # noqa: E402
    generate_audio_rest,
    get_mp3_duration,
    get_voice_for_lesson,
)

# Lesson 2 -> Ada. Same rule the lesson narration uses.
VOICE, VOICE_LABEL = get_voice_for_lesson(2)

SCENES = [
    ("appear",    "Your body makes new cells all the time, to grow, to repair damage and to replace cells that wear out."),
    ("cycle",     "It does this in a series of stages called the cell cycle."),
    ("nucleus",   "Inside this cell the nucleus holds the chromosomes, and in body cells they come in pairs."),
    ("growth",    "First the cell grows and makes more of the structures inside it, such as ribosomes and mitochondria."),
    ("replicate", "Then the DNA is copied, so each chromosome becomes two identical copies, joined together."),
    ("envelope",  "Now mitosis begins, and the membrane around the nucleus breaks down."),
    ("spindle",   "Fine fibres stretch out from each end of the cell and take hold of the chromosomes."),
    ("align",     "The chromosomes line up in a row across the middle of the cell."),
    ("separate",  "The fibres pull the copies apart, so one set of chromosomes is pulled to each end of the cell."),
    ("reform",    "A new membrane forms around each set, so the nucleus has divided."),
    ("furrow",    "Finally the cytoplasm and the cell membrane divide, making two cells."),
    ("settle",    "Each new cell has the same chromosomes as the cell it came from, which is how the body grows and repairs itself."),
]

OUT = Path(__file__).resolve().parent / "audio"


def main():
    if not os.environ.get("AZURE_SPEECH_KEY"):
        print("AZURE_SPEECH_KEY is not set.")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    total = 0.0

    for i, (key, text) in enumerate(SCENES, start=1):
        name = f"scene-{i:02d}.mp3"
        path = OUT / name
        if path.exists() and "--force" not in sys.argv:
            dur = get_mp3_duration(path.read_bytes())
            print(f"  {name}  (kept)  {dur:.2f}s")
        else:
            print(f"  {name}  synthesising...")
            audio = generate_audio_rest(text, VOICE)
            if not audio:
                print(f"  FAILED on scene {i}")
                return 1
            path.write_bytes(audio)
            dur = get_mp3_duration(audio)
            print(f"  {name}  {dur:.2f}s  {len(audio)} bytes")
        total += dur
        manifest.append({
            "scene": i,
            "key": key,
            "file": f"audio/{name}",
            "text": text,
            "duration": dur,
            "words": len(text.split()),
        })

    (OUT / "manifest.json").write_text(json.dumps({
        "voice": VOICE,
        "voice_label": VOICE_LABEL,
        "format": "audio-24khz-96kbitrate-mono-mp3",
        "beat_seconds": 0.55,
        "speech_seconds": round(total, 2),
        "total_seconds": round(total + 0.55 * (len(SCENES) - 1), 2),
        "scenes": manifest,
    }, indent=2), encoding="utf-8")

    print(f"\nSpeech {total:.1f}s + beats = {total + 0.55 * (len(SCENES) - 1):.1f}s total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
