"""Send the reference launch videos Tom liked (27 Sep 2026) to Gemini for a shot-by-shot breakdown
of animation technique, transitions, pacing and music sync. Output: <video>.breakdown.md"""
import os, sys, time
from google import genai

PROMPT = """You are a senior motion designer. Analyse this video as a reference for a product launch video.
Tom (the client) likes its ANIMATIONS and TRANSITIONS, not necessarily its visual style.

Give a precise shot-by-shot breakdown with timestamps (mm:ss.s): for every shot, what is on screen,
how elements enter/exit (easing, springiness, overshoot, stagger, masks, morphs, camera moves,
parallax, depth, blur, scale, rotation), how each transition works technically (match cut, shape
morph, zoom-through, wipe, mask reveal, whip, object handover between shots…), how long each shot
holds, how motion lines up with the music (which beats/hits, where it breathes), text/typography
animation (per-letter/word, kinetic type), and any recurring motif.

Then summarise: (1) the 10 techniques that make it feel slick, each with a concrete recipe a coder
could implement in HTML canvas/CSS (timings in ms, easing curves as cubic-bezier or spring params);
(2) average shot length and the pacing curve; (3) what to avoid copying. Be specific, not generic."""


def main():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    for path in sys.argv[1:]:
        f = client.files.upload(file=path)
        while f.state.name == "PROCESSING":
            time.sleep(5); f = client.files.get(name=f.name)
        r = client.models.generate_content(model="gemini-3.1-pro-preview", contents=[f, PROMPT])
        out = os.path.splitext(path)[0] + ".breakdown.md"
        open(out, "w", encoding="utf-8").write(r.text)
        print(out, len(r.text))


if __name__ == "__main__":
    main()
