import sys
from PIL import Image
MAPS = {
 'pendle-hill-z16-final': {'E':{76:43,77:754,78:1466},'N':{43:433,42:1140}},
 'yorkshire-dales-z15-final': {'E':{88:279,89:636,90:994,91:1351},'N':{74:286,73:643,72:999}},
 'lake-district-z16-final': {'E':{34:56,35:784,36:1512},'N':{9:345,8:1053}},
 'northumberland-z15-final': {'E':{96:22,97:389,98:755,99:1122,100:1488},'N':{94:311,93:678,92:1045}},
}
def ref(m,x,y):
    d=MAPS[m]; E=d['E']; N=d['N']
    e0=min(E); x0=E[e0]; e1=max(E); x1=E[e1]
    px=(x1-x0)/(e1-e0)
    east=e0+(x-x0)/px
    n0=max(N); y0=N[n0]; n1=min(N); y1=N[n1]
    py=(y1-y0)/(n0-n1)
    north=n0-(y-y0)/py
    return east,north
if __name__=='__main__':
    m=sys.argv[1]
    for pair in sys.argv[2:]:
        x,y=[int(v) for v in pair.split(',')]
        e,n=ref(m,x,y)
        print(pair,'-> E %.3f N %.3f  4fig %02d%02d  6fig %03d%03d'%(e,n,int(e)%100,int(n)%100,int(e*10)%1000,int(n*10)%1000))
