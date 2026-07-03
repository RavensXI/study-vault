"""Compute CSS matrix3d homographies mapping flat content layers onto the
painted pages of desk4-book-d-cut.png (2184x1443; corners measured on the
fine grid). Content layers live in plate-pixel space (the whole book wrapper
scales/rotates as one), transform-origin 0 0.
Also emits tab anchors along the cover fore-edge.
"""
import math
import numpy as np

# writable inner quads, plate px: TL, TR, BR, BL (already inset off curls)
L_IN = [(370, 190), (1010, 175), (1030, 1100), (330, 1115)]
R_IN = [(1190, 170), (1830, 175), (1925, 1090), (1165, 1105)]
LW, LH = 640, 915
RW, RH = 685, 920

def homography(W, H, quad):
    src = [(0,0),(W,0),(W,H),(0,H)]
    A, b = [], []
    for (x,y),(X,Y) in zip(src, quad):
        A.append([x,y,1,0,0,0,-X*x,-X*y]); b.append(X)
        A.append([0,0,0,x,y,1,-Y*x,-Y*y]); b.append(Y)
    h = np.linalg.solve(np.array(A,float), np.array(b,float))
    h00,h01,h02,h10,h11,h12,h20,h21 = h
    m = [h00,h10,0,h20, h01,h11,0,h21, 0,0,1,0, h02,h12,0,1]
    return "matrix3d(" + ",".join(f"{v:.6f}" for v in m) + ")"

print(f".pl{{width:{LW}px;height:{LH}px;transform:{homography(LW, LH, L_IN)}}}")
print(f".pr{{width:{RW}px;height:{RH}px;transform:{homography(RW, RH, R_IN)}}}")
print()
# tabs: along the cover fore-edge (1940,130)->(2075,1200); outward normal
E0, E1 = np.array([1940,130]), np.array([2075,1200])
edge = E1 - E0
print(f"tab rotate: {math.degrees(math.atan2(edge[0], edge[1]))-90:.1f} deg-ish; "
      f"normal angle {math.degrees(math.atan2(-edge[0], edge[1])):.1f}")
for i in range(9):
    t = 0.06 + i * (0.88 / 8)
    p = E0 + t * edge
    print(f"tab{i}: [{p[0]:.0f},{p[1]:.0f}],")
