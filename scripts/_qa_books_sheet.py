import os
from PIL import Image, ImageDraw
OUT=r"design-lab/assets/lw/shelf"
KEYS=["triple","french","german","business","econ","psych","socio","stats","pe","citizenship","astro","geology","classics","dt","eng","electronics","it","media","film","drama","music","mtech","food","hosp","hsc"]
COLS=9; CW,CH=170,540
rows=(len(KEYS)+COLS-1)//COLS
sheet=Image.new("RGB",(COLS*CW,rows*CH),(246,241,231))
d=ImageDraw.Draw(sheet)
for i,k in enumerate(KEYS):
    x,y=(i%COLS)*CW,(i//COLS)*CH
    p=os.path.join(OUT,f"book_{k}.png")
    if os.path.exists(p):
        im=Image.open(p).convert("RGBA")
        h=470; w=round(im.width*h/im.height); im=im.resize((w,h))
        sheet.paste(im,(x+(CW-w)//2,y+8),im)
    d.text((x+8,y+CH-42),k,fill=(60,50,40))
sheet.save(r"design-lab/assets/lw/shelf/_qa_sheet.png")
print("sheet ->",sheet.size)
