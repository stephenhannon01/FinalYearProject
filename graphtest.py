import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
    (0.3, 0.6), # left, bottom
    (0.3, 0.8), # left, top
    (0.5, 0.8), # right, top
    (0.5, 0.6), # right, bottom
    (0., 0.), # ignored
    ]

vertstwo = [
    (0.1, 0.1), # left, bottom
    (0.3, 0.4), # left, top
    (0.2, 0.2), # right, top
    (0.3, 0.2), # right, bottom
    (0., 0.), # ignored
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]

path = Path(verts, codes)
pathtwo = Path(vertstwo, codes)

fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor=(1,0,0,0.5), lw=2)
patchtwo = patches.PathPatch(pathtwo, facecolor=(0,1,0,0.5), lw=2)
ax.add_patch(patch)
ax.add_patch(patchtwo)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
plt.show()
