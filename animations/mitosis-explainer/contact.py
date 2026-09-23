import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image
TL = json.loads(open('timeline.js', encoding='utf-8').read().split('=', 1)[1].rstrip(';\n'))
L = TL['lines']
def at(i, f): return L[i]['start'] + L[i]['dur'] * f
TIMES = [1.8, at('s1', .8), at('s2', .95), at('s3', .9), at('s4', .95), at('s5', .95), at('s6', .95), at('s7', .95), L['q']['start'] + L['q']['dur'] + 1.8, at('a', .95), TL['end'][0] + 2]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(pathlib.Path('film.html').resolve().as_uri()); await pg.wait_for_function('window.READY === true', timeout=30000)
        ims = []
        for t in TIMES:
            url = await pg.evaluate('(t)=>{render(t);return document.getElementById("c").toDataURL("image/jpeg",.8)}', t)
            import base64, io; ims.append(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).resize((270, 480)))
        await b.close()
    cols = 6; rows = (len(ims) + cols - 1) // cols; M = Image.new('RGB', (cols * 276, rows * 486), '#555')
    for i, im in enumerate(ims): M.paste(im, ((i % cols) * 276, (i // cols) * 486))
    M.save('_contact.png'); print('ok')
asyncio.run(main())
