import os
from PIL import Image
d=os.path.dirname(os.path.abspath(__file__))
def crop(name,box,out,scale=2):
    im=Image.open(os.path.join(d,"_m_"+name)).convert("RGB").crop(box)
    im=im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
    im.save(os.path.join(d,out)); print(out,box,im.size)
crop("dorset-coast-z16-final.jpg",(0,60,320,260),"_c_d16_worch.png",3)
crop("dorset-coast-z16-final.jpg",(1020,830,1360,1050),"_c_d16_kings.png",3)
