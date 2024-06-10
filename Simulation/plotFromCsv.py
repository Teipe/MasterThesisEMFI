import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

height  = 6e-3
startZ  = height + 1.2e-3
endZ    = height + 1.2e-3
numZ = 1


startr = 0e-3
endr = 1e-2
numr = 1000
numTheta = 100
dtTheta = 2*np.pi/numTheta

rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

df1 = pd.read_csv(f"magneticFieldTiltedR0.001_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])
df4 = pd.read_csv(f"magneticFieldTiltedR0.0025_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])

B = np.array(df4.B)
B = B.reshape(numZ, numTheta, numr)
B1 = np.array(df1.B)
B1 = B1.reshape(numZ, numTheta, numr)


fig = plt.figure()
# fig.tight_layout()
fig.suptitle(r'$B_Z$ for coil with radius 4mm (left) and 1mm (right)')
ax = fig.add_subplot(111, projection='3d')

# Create the mesh in polar coordinates and compute corresponding Z.
R, P = np.meshgrid(rArr, theta1Arr)
B = np.array(B)

# Express the mesh in the cartesian system.
X, Y = R*np.cos(P), R*np.sin(P)

# Bcut = B
# Bcut1 = B1
# for i, z in enumerate(Bcut):
#   Bfloor = np.amax(z)*0.8
#   Bfloor1 = np.amax(B1[i])*0.8
#   for j, x in enumerate(z):
#     for k, y in enumerate(x):
#       if Bcut[i][j][k] <= Bfloor:
#         Bcut[i][j][k] = Bfloor
#       if Bcut1[i][j][k] <= Bfloor1:
#         Bcut1[i][j][k] = Bfloor1




# Plot the surface.
ax.set_title(r'$B_Z$ at z=0.5mm')
ax.plot_surface(X*1000, Y*1000, B[0], cmap=plt.cm.YlGnBu_r)
# ax3.set_title(r'$B_Z$ at z=5mm')
# ax3.plot_surface(X*1000, Y*1000, B1[0], cmap=plt.cm.YlGnBu_r)

ax.view_init(elev=25, azim=115, roll=0)
# ax3.view_init(elev=25, azim=115, roll=0)
ax.set_xlabel(r'x [mm]')
ax.set_ylabel(r'y [mm]')
ax.set_zlabel('\n\n' r'$B_z$ [T/A]')
# ax2.set_xlabel(r'x [mm]')
# ax2.set_ylabel(r'y [mm]')
# ax2.set_zlabel('\n\n' r'$B_z$ [T/A]')
# ax3.set_xlabel(r'x [mm]')
# ax3.set_ylabel(r'y [mm]')
# ax3.set_zlabel('\n\n' r'$B_z$ [T/A]')
# ax4.set_xlabel(r'x [mm]')
# ax4.set_ylabel(r'y [mm]')
# ax4.set_zlabel('\n\n' r'$B_z$ [T/A]')
fig = plt.figure()
ax = fig.add_subplot(111)
print(len(Y))
print(len(Y[0]))
print(len(B[0][int(len(B[0])/2)]))
# ax.plot(X[0], B[0][0])
# ax.plot(Y[int(len(B[0])/2)], B[0][int(len(B[0])/2)])
ax.plot(X[int(len(B[0])/2)], B[0][int(len(B[0])/2)])

# ax5 = fig.add_axes([0.1, 0.85, 0.8, 0.1])

# s = Slider(ax = ax5, label = 'value', valmin = 0, valmax = numZ-1, valinit = 3, valstep=1)

# def update(val):
#     value = s.val
#     ax.cla()
#     ax2.cla()
#     ax.plot_surface(X, Y, B[value], cmap = plt.cm.YlGnBu_r)
#     ax2.plot_surface(X, Y, B1[value], cmap = plt.cm.YlGnBu_r)
#     ax.set_zlim(np.amin(B[value]), np.amax(B[value]))
    # ax.set_zlim(-2, 7)

print(B[0][numTheta-1][numr-1])

# s.on_changed(update)
# update(0)
plt.savefig('magneticFieldHighRes.svg')
plt.show()
