import os
from PIL import Image
d=os.path.dirname(os.path.abspath(__file__))
def crop(name,box,out,scale=2):
    im=Image.open(os.path.join(d,"_m_"+name)).convert("RGB").crop(box)
    im=im.resize((im.width*scale,im.height*scale),Image.LANCZOS)
    im.save(os.path.join(d,out))
    print(out, box, im.size)
crop("ribble-valley-z16-final.jpg",(0,0,400,400),"_c_rv16_tl.png")
crop("ribble-valley-z16-final.jpg",(1100,1050,1500,1302),"_c_rv16_br.png")
