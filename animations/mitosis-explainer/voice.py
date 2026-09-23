"""Gemini TTS, one clip per sentence (so the animation knows every sentence's length)."""
import base64, json, os, subprocess, sys, urllib.request, wave
KEY = os.environ['GEMINI_API_KEY']; MODEL = sys.argv[1] if len(sys.argv) > 1 else 'gemini-3.8-flash-tts'
VOICE = sys.argv[2] if len(sys.argv) > 2 else 'Sulafat'
STYLE = ('Read this as a warm, curious British science teacher talking to a 15-year-old: natural and friendly, '
         'with a little wonder, clear and unhurried, a British English accent. ')
lines = json.load(open('script.json', encoding='utf-8'))
out = {}
for l in [x for x in lines if len(sys.argv) < 4 or x['id'] in sys.argv[3].split(',')]:
    body = {'contents': [{'parts': [{'text': 'Say warmly and curiously, like a friendly British science teacher: ' + l['text']}]}],
            'generationConfig': {'responseModalities': ['AUDIO'],
                                 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': VOICE}}}}}
    req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}',
                                 data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    pcm = base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
    p = f"voice/{l['id']}.wav"
    with wave.open(p, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    out[l['id']] = round(len(pcm) / 2 / 24000, 3)
    print(l['id'], out[l['id']], 's', flush=True)
json.dump(out, open('voice/durations.json', 'w'), indent=1)
