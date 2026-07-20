import os, urllib.request
from PIL import Image
D=r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\zz13"
os.makedirs(D, exist_ok=True)
base="https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
for f in ["pendle-hill-z16-final.jpg","yorkshire-dales-z15-final.jpg","snowdonia-z15-final.jpg","lake-district-z16-final.jpg"]:
    p=os.path.join(D,f)
    if not os.path.exists(p):
        urllib.request.urlretrieve(base+f, p)
    im=Image.open(p)
    print(f, im.size)
