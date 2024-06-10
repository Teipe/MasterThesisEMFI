import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd


### TODO: Changes that needs to be made
# Add calibration coefficient from Project
# 1. Change from circular circuit to rectangular. Done
# 2. Add a number for resistivity, so that we can calculate I from V(Emf)
# 3. Could correct for error introduced by circular dA
# 4. Add offset/center (see next TODO)
# 5. Calculated opposing field created by copper plane

# Rectangle geometry
length  = 10e-2  # 10cm
# width1   = 0.762e-3   # 30mil (this is the same as spacing plus width of trace)
# width2   = 0.5e-3  # 18mil (this is the same as spacing plus width of trace)
# Trace 3
width1   = 0.5e-3   # 18mil (this is the same as spacing plus width of trace)
# Trace 4
width2   = 0.3048e-3  # 12mil (this is the same as spacing plus width of trace)
# Trace 1 and 2
width5   = 5e-3   # 5mm (this is the same as spacing plus width of trace)
# Might want to add a width of trace, to verify the assumption that the 
#   outer part of the trace counts as width instead of the inner part.

def withinCircuit(radius, theta, width, offset=0):
    return abs(radius*np.cos(theta)+offset)<width/2 and abs(radius*np.sin(theta))<length/2

# TODO: Add some offset from where the coil start. For now we assume center
# offsetArr = np.linspace(0, 1e-2, num=20)
# offsetThetaArr = np.linspace(0, 2*np.pi, num=20)

height  = 6e-3
startZ  = height + 1.2e-3
endZ    = height + 1.2e-3
numZ    = 1
startZ_1  = height + 1.2e-3
endZ_1    = height + 1.2e-3
numZ_1    = 1

#Used in master
# startr = 0e-3
# endr = 2e-2
# numr = 2001
# numTheta = 100

startr = 0e-3
endr = 50e-3
numr = 1001
dr = (endr-startr)/numr


numTheta = 50
dtTheta = 2*np.pi/numTheta

zArr = np.linspace(startZ_1,  endZ_1, num=numZ_1)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)

df1 = pd.read_csv(f"magneticFieldTiltedR0.001_{startZ_1}-{endZ_1}-{numZ_1}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])
df4 = pd.read_csv(f"magneticFieldTiltedR0.0025_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv", usecols=['B'])


mu_0  = 1.257e-6  #m kg s**-2 A**-2
loops = 5
r1    = 1e-3
r4    = 2.5e-3
ZL1   = loops**2*r1**2*np.pi*mu_0/height
ZL4   = loops**2*r4**2*np.pi*mu_0/height

B1 = np.array(df1.B)
B4 = np.array(df4.B)
B1 = B1.reshape(numZ_1, numTheta, numr)
B4 = B4.reshape(numZ, numTheta, numr)

rotateStart = 3*np.pi/16
rotateNum = 4
rotateEnd = np.pi*(rotateNum-1)/(rotateNum/2)+rotateStart
rotateArr = np.linspace(rotateStart, rotateEnd, rotateNum)


offsetStart = -1.5e-2
offsetEnd = 1.5e-2
offsetNum = 601
offsetArr = np.linspace(offsetStart, offsetEnd, offsetNum)
offset_rotated_totalField4 = []
offset_rotated_totalField1 = []
offset_rotated_totalField4_2 = []
offset_rotated_totalField1_2 = []
offset_rotated_totalField4_5 = []
offset_rotated_totalField1_5 = []
for rotation in rotateArr:
  offset_totalField4 = []
  offset_totalField1 = []
  offset_totalField4_2 = []
  offset_totalField1_2 = []
  offset_totalField4_5 = []
  offset_totalField1_5 = []
  rotated_theta1Arr = theta1Arr + rotation
  for offset in offsetArr:
    totalField4 = []
    totalField1 = []
    totalField4_2 = []
    totalField1_2 = []
    totalField4_5 = []
    totalField1_5 = []
    for i, z in enumerate(zArr):
      sumOfField4z = 0
      sumOfField1z = 0
      sumOfField4z_2 = 0
      sumOfField1z_2 = 0
      sumOfField4z_5 = 0
      sumOfField1z_5 = 0
      for j, r in enumerate(rArr):
        if r == 0:
          dA = dr**2*np.pi*(dtTheta/2/np.pi)
        else:
          dA = ((4*r*dr)*np.pi)*(dtTheta/2/np.pi)
        for k, theta in enumerate(rotated_theta1Arr):
          if withinCircuit(r, theta, width1, offset): # Change to cartesian
            sumOfField1z += B1[i][k][j]*dA
            sumOfField4z += B4[i][k][j]*dA
          if withinCircuit(r, theta, width2, offset): # Change to cartesian
            sumOfField1z_2 += B1[i][k][j]*dA
            sumOfField4z_2 += B4[i][k][j]*dA
          if withinCircuit(r, theta, width5, offset): # Change to cartesian
            sumOfField1z_5 += B1[i][k][j]*dA
            sumOfField4z_5 += B4[i][k][j]*dA
      totalField4.append(sumOfField4z)  
      totalField1.append(sumOfField1z)  
      totalField1_2.append(sumOfField1z_2)  
      totalField4_2.append(sumOfField4z_2)  
      totalField1_5.append(sumOfField1z_5)  
      totalField4_5.append(sumOfField4z_5)  
    offset_totalField4.append(totalField4)  
    offset_totalField1.append(totalField1)  
    offset_totalField1_2.append(totalField1_2)  
    offset_totalField4_2.append(totalField4_2)  
    offset_totalField1_5.append(totalField1_5)  
    offset_totalField4_5.append(totalField4_5)  
  offset_rotated_totalField4.append(offset_totalField4)  
  offset_rotated_totalField1.append(offset_totalField1)  
  offset_rotated_totalField1_2.append(offset_totalField1_2)  
  offset_rotated_totalField4_2.append(offset_totalField4_2)  
  offset_rotated_totalField1_5.append(offset_totalField1_5)  
  offset_rotated_totalField4_5.append(offset_totalField4_5)  
  
offset_rotated_totalField4 = np.array(offset_rotated_totalField4)
offset_rotated_totalField1 = np.array(offset_rotated_totalField1)
offset_rotated_totalField1_2 = np.array(offset_rotated_totalField1_2)
offset_rotated_totalField4_2 = np.array(offset_rotated_totalField4_2)
offset_rotated_totalField1_5 = np.array(offset_rotated_totalField1_5)
offset_rotated_totalField4_5 = np.array(offset_rotated_totalField4_5) 

FieldsDict = {'offset_rotated_totalField4':offset_rotated_totalField4.flatten(),
'offset_rotated_totalField1':offset_rotated_totalField1.flatten(),
'offset_rotated_totalField1_2':offset_rotated_totalField1_2.flatten(),
'offset_rotated_totalField4_2':offset_rotated_totalField4_2.flatten(),
'offset_rotated_totalField1_5':offset_rotated_totalField1_5.flatten(),
'offset_rotated_totalField4_5':offset_rotated_totalField4_5.flatten()}
df = pd.DataFrame(FieldsDict)
df.to_csv(f"doubleRes_capturedMagenticField_{offsetStart}-{offsetEnd}-{offsetNum}_{rotateStart}-{rotateEnd}-{rotateNum}_{startZ_1}-{endZ_1}-{numZ_1}.csv")

# Best settings after experimentation
img_size = (32, 18)
font_size = 55

fig = plt.figure(figsize=img_size)
font = {'size'   : font_size}
plt.rc('font', **font)
plt.rc('xtick', labelsize=font_size) 
plt.rc('ytick', labelsize=font_size) 
plt.title('Theoretical X Sweep from rotating Tx Ø 1mm')
plt.xlabel('Posistion X(mm)')
plt.ylabel("Rx Peak Voltage (mV)")
for i, rotation in enumerate(rotateArr):
  print(f'{int(np.round(rotation*180/np.pi, 0))}: Peak amplitude {offsetArr[np.argmax(offset_rotated_totalField1_5[i])]*1000}mm')
  plt.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField1_2[i], ZL1)*200, label=f'Rotated {int(np.round(rotation*180/np.pi, 0))}°')
  # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField4_5[rotation], ZL4)*200, label='4mm')
  # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField1_2[rotation], ZL1)*200, label='1mm')
  # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField4_2[rotation], ZL4)*200, label='4mm')
  # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField1[rotation], ZL1)*200, label='1mm')
  # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField4[rotation], ZL4)*200, label='4mm')
plt.grid(True, which='major', axis='both', linestyle='-', linewidth=1)
plt.grid(True, which='minor', axis='both', linestyle='--', linewidth=0.8)
plt.legend()
plt.savefig(f'C:\\EMFI_Master\\Figures\\Theoretical_1mmRotation.png', 
            transparent = False,  
            facecolor = 'white'
            )
plt.show()