"""Record a lo-fi study-beats bed from Lyria RealTime (Gemini API, same key as
image gen). Streams 48kHz 16-bit stereo PCM; we capture N seconds and write a
WAV, then ffmpeg it to a loopable MP3 for the desk radio's lo-fi dial.

Usage: python scripts/_gen_lofi.py [seconds] [outname]
"""
import os, sys, asyncio, wave
from google import genai
from google.genai import types

SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 150
NAME = sys.argv[2] if len(sys.argv) > 2 else "lofi-a"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_WAV = os.path.join(ROOT, "design-lab", "assets", NAME + ".wav")

PROMPTS = [
    ("lo-fi hip hop study beats", 1.0),
    ("warm mellow Rhodes piano, soft vinyl crackle", 0.7),
    ("gentle boom-bap drums, relaxed, unobtrusive", 0.5),
]

async def main():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"],
                          http_options={"api_version": "v1alpha"})
    chunks = []
    target_bytes = SECONDS * 48000 * 2 * 2   # 48kHz, 16-bit, stereo
    got = 0
    async with client.aio.live.music.connect(model="models/lyria-realtime-exp") as session:
        await session.set_weighted_prompts(
            prompts=[types.WeightedPrompt(text=t, weight=w) for t, w in PROMPTS])
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(bpm=74, temperature=1.0))
        await session.play()
        async for msg in session.receive():
            sc = getattr(msg, "server_content", None)
            if sc and getattr(sc, "audio_chunks", None):
                for ch in sc.audio_chunks:
                    if ch.data:
                        chunks.append(ch.data)
                        got += len(ch.data)
                if got >= target_bytes:
                    break
        await session.stop()
    pcm = b"".join(chunks)[:target_bytes]
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes(pcm)
    print(f"ok {OUT_WAV} ({len(pcm)//1024} KB, ~{len(pcm)/(48000*4):.0f}s)")

asyncio.run(main())
