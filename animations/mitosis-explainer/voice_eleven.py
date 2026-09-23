"""ElevenLabs narration for script.json with one voice, trimmed, plus a matching timeline file.
   python voice_eleven.py VOICE_ID NAME   ->  voice_NAME/*.wav, timeline_NAME.js"""
import json, os, subprocess, sys, urllib.request
VID, NAME = sys.argv[1], sys.argv[2]
K = os.environ.get('ELEVENLABS_API_KEY') or subprocess.run(['powershell', '-NoProfile', '-Command', "[Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')"], capture_output=True, text=True).stdout.strip()
D = f'voice_{NAME}'; os.makedirs(D, exist_ok=True)
lines = json.load(open('script.json', encoding='utf-8')); dur = {}
for l in lines:
    body = {'text': l['text'], 'model_id': 'eleven_multilingual_v2', 'voice_settings': {'stability': 0.5, 'similarity_boost': 0.8, 'style': 0.2, 'use_speaker_boost': True}}
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VID}?output_format=mp3_44100_128', data=json.dumps(body).encode(), headers={'xi-api-key': K, 'Content-Type': 'application/json'})
    open(f"{D}/{l['id']}.mp3", 'wb').write(urllib.request.urlopen(req, timeout=120).read())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f"{D}/{l['id']}.mp3", '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1,areverse', '-ar', '24000', '-ac', '1', f"{D}/{l['id']}_t.wav"], check=True)
    dur[l['id']] = round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f"{D}/{l['id']}_t.wav"], capture_output=True, text=True).stdout), 3)
t = 3.2; tl = {'title': [0, 3.2], 'lines': {}}
gap = {'s1': 0.7, 's2': 0.9, 's3': 0.8, 's4': 1.1, 's5': 1.2, 's6': 1.3, 's7': 1.3, 'q': 3.0, 'a': 0.8}
for l in lines:
    tl['lines'][l['id']] = {'start': round(t, 3), 'dur': dur[l['id']], 'text': l['text']}; t += dur[l['id']] + gap[l['id']]
tl['end'] = [round(t, 3), round(t + 3, 3)]; tl['total'] = round(t + 3, 3)
open(f'timeline_{NAME}.js', 'w', encoding='utf-8').write('window.TL=' + json.dumps(tl, indent=1) + ';')
print(NAME, 'narration', round(sum(dur.values()), 1), 's; film', tl['total'], 's')
