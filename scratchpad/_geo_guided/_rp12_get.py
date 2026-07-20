import urllib.request, os
from PIL import Image
d=os.path.dirname(os.path.abspath(__file__))
base="https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/"
for n in ["ribble-valley-z16-final.jpg","lake-district-z15-final.jpg","dorset-coast-z16-final.jpg","peak-district-z16-final.jpg","yorkshire-dales-z16-final.jpg","ribble-valley-z15-final.jpg","dorset-coast-z15-final.jpg","peak-district-z15-final.jpg"]:
    p=os.path.join(d,"_m_"+n)
    if not os.path.exists(p):
        req=urllib.request.Request(base+n, headers={"User-Agent":"Mozilla/5.0"})
        open(p,"wb").write(urllib.request.urlopen(req).read())
    print(n, Image.open(p).size)
