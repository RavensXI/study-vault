"""Render every frame at 24 fps, then mux with the narration."""
import asyncio, base64, json, os, pathlib, subprocess
from playwright.async_api import async_playwright
FPS = 24
TL = json.loads(open('timeline.js', encoding='utf-8').read().split('=', 1)[1].rstrip(';\n'))
os.makedirs('frames', exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(pathlib.Path('film.html').resolve().as_uri()); await pg.wait_for_function('window.READY === true', timeout=30000)
        n = int(TL['total'] * FPS)
        for i in range(n):
            url = await pg.evaluate('(t)=>{render(t);return document.getElementById("c").toDataURL("image/jpeg",.92)}', i / FPS)
            open(f'frames/{i:05d}.jpg', 'wb').write(base64.b64decode(url.split(',')[1]))
            if i % 300 == 0: print('frame', i, '/', n, flush=True)
        await b.close()
    # narration: each line at its start time
    ids = list(TL['lines'].keys())
    VD = os.environ.get('VOICE_DIR', 'voice'); OUTF = os.environ.get('OUT', 'mitosis-explainer.mp4')
    inputs = sum([['-i', f'{VD}/{k}_t.wav'] for k in ids], [])
    delays = ''.join(f"[{i}:a]adelay={int(TL['lines'][k]['start'] * 1000)}|{int(TL['lines'][k]['start'] * 1000)}[a{i}];" for i, k in enumerate(ids))
    mix = delays + ''.join(f'[a{i}]' for i in range(len(ids))) + f'amix=inputs={len(ids)}:normalize=0,apad,atrim=0:{TL["total"]}[out]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', mix, '-map', '[out]', '-ar', '48000', f'{VD}/narration.wav'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', 'frames/%05d.jpg', '-i', f'{VD}/narration.wav',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-shortest',
                    '-movflags', '+faststart', OUTF], check=True)
    print('done', os.path.getsize(OUTF) // 1024, 'KB')
asyncio.run(main())
