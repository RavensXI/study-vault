"""Short narration over the mitosis short: eleven lines, one per shot, placed clear of the
big hits; Azure voice with a cheerful style; leading and trailing silence trimmed; the score
ducked under speech; muxed onto the master video. Also writes one-line voice samples.

  python narration/build_narration.py                       # Sonia cheerful (default)
  python narration/build_narration.py --voice en-GB-RyanNeural --style cheerful
  python narration/build_narration.py --samples
"""
import io, os, subprocess, sys, time, argparse
import requests
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault")
from scripts.lib.narration import AZURE_TTS_URL, AZURE_KEY, xml_escape  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument('--voice', default='en-GB-SoniaNeural'); ap.add_argument('--style', default='cheerful')
ap.add_argument('--rate', default='+10%'); ap.add_argument('--tag', default='')
ap.add_argument('--samples', action='store_true'); ap.add_argument('--fresh', action='store_true')
A = ap.parse_args()

# (start T, latest end T, text). Ends may run 0.3 s over into a quiet cut; never over the hits at 12.0 and 21.5.
LINES = [
    (0.55, 2.10, "One cell, about to divide."),
    (2.70, 4.60, "Chromosomes, in pairs."),
    (4.90, 6.90, "First, it grows."),
    (7.40, 9.60, "It copies its DNA, exactly."),
    (9.70, 11.80, "Two identical copies, joined."),
    (12.30, 13.60, "Mitosis begins."),
    (14.00, 16.10, "Fibres line them up in the middle,"),
    (16.70, 19.00, "and pull the copies to each end."),
    (19.60, 21.40, "Two new nuclei."),
    (22.00, 25.30, "The cell splits: two cells, genetically identical."),
    (26.40, 29.40, "And each one can divide again."),
]

def tts(text, voice, style, rate):
    inner = xml_escape(text)
    if rate: inner = f"<prosody rate='{rate}'>{inner}</prosody>"
    if style: inner = f"<mstts:express-as style='{style}'>{inner}</mstts:express-as>"
    ssml = ("<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
            "xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-GB'>"
            f"<voice name='{voice}'>{inner}</voice></speak>")
    h = {"Ocp-Apim-Subscription-Key": AZURE_KEY, "Content-Type": "application/ssml+xml",
         "X-Microsoft-OutputFormat": "riff-48khz-16bit-mono-pcm"}
    for _ in range(4):
        try:
            r = requests.post(AZURE_TTS_URL, headers=h, data=ssml.encode('utf-8'), timeout=60)
            if r.status_code == 200: return r.content
            print('  HTTP', r.status_code, r.text[:160])
        except requests.exceptions.RequestException as e:
            print('  retry:', str(e)[:80])
        time.sleep(4)
    raise SystemExit('TTS failed')

def trim(src, dst):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af',
                    'silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,'
                    'silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse', dst], check=True)

def secs(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip())

tag = A.tag or (A.voice.replace('en-GB-', '').replace('Neural', '') + ('-' + A.style if A.style else '')).lower()
outdir = os.path.join(HERE, tag); os.makedirs(outdir, exist_ok=True)
clips = []
for i, (t0, t1, text) in enumerate(LINES, 1):
    raw = os.path.join(outdir, 'raw-%02d.wav' % i); p = os.path.join(outdir, 'line-%02d.wav' % i)
    if A.fresh or not os.path.exists(raw):
        io.open(raw, 'wb').write(tts(text, A.voice, A.style, A.rate))
    trim(raw, p)
    d = secs(p); over = t0 + d - t1
    print('%02d  T %5.2f  %4.2fs  %-14s %s' % (i, t0, d, ('ok' if over <= 0 else 'over by %.2fs' % over), text)); clips.append((t0, p, d))

inputs = []; fl = []
for i, (t0, p, d) in enumerate(clips):
    inputs += ['-i', p]; fl.append('[%d:a]adelay=%d|%d[n%d]' % (i, int(t0 * 1000), int(t0 * 1000), i))
mix = ''.join('[n%d]' % i for i in range(len(clips))) + 'amix=inputs=%d:normalize=0,apad=whole_dur=30[nar]' % len(clips)
nar = os.path.join(outdir, 'narration.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fl + [mix]), '-map', '[nar]', '-ar', '48000', '-ac', '2', nar], check=True)

score = os.path.join(HERE, 'score.wav'); master = os.path.join(ROOT, 'exports', 'mitosis-short.mp4')
mixed = os.path.join(outdir, 'mix.wav')
fc = ("[1:a]asplit=2[sc][nv];"
      "[0:a][sc]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=600:makeup=1[ducked];"
      "[ducked][nv]amix=inputs=2:normalize=0:weights=1 1.2,alimiter=limit=0.95[out]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', score, '-i', nar, '-filter_complex', fc, '-map', '[out]', '-ar', '48000', mixed], check=True)
out = os.path.join(ROOT, 'exports', 'mitosis-short-narrated-%s.mp4' % tag)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', master, '-i', mixed, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
phone = out.replace('.mp4', '-phone.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', 'scale=720:1280', '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', phone], check=True)
print('wrote', out); print('wrote', phone)

if A.samples:
    for v, st in [('en-GB-SoniaNeural', 'cheerful'), ('en-GB-RyanNeural', 'cheerful'), ('en-GB-LibbyNeural', ''), ('en-GB-AdaMultilingualNeural', '')]:
        p = os.path.join(HERE, 'sample-%s.wav' % v.replace('en-GB-', '').replace('Neural', '').lower())
        io.open(p, 'wb').write(tts("Each chromosome: two identical copies. The cell splits: two cells, genetically identical.", v, st, A.rate))
        print('sample', p)
