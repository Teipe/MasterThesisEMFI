import numpy as np
import pandas as pd


# CPW geometry
length  = 10e-2  # 10cm
# Trace 5:
top5    = 6.9e-3
bottom5 = 8.5e-3
# Trace 6:
top6    = 7.2e-3
bottom6 = 8.7e-3

widthCPW = 0.635e-3   # 25mil trace width
# Might want to add a width of trace, to verify the assumption that the 
#   outer part of the trace counts as width instead of the inner part.

# Returns 1, -1 depending on polarity or 0 if outside
def withinCircuit(radius, theta, bottom, top, offset=0):
  polarity = 0
  if radius*np.cos(theta)+offset<top and radius*np.cos(theta)+offset>0:
    polarity = 1
  if radius*np.cos(theta)+offset>-bottom and radius*np.cos(theta)+offset<0:
    polarity = -1
  return polarity

height  = 6e-3
startZ  = height + 1.2e-3
endZ    = height + 1.2e-3
numZ    = 1
startZ_1  = height + 1.2e-3
endZ_1    = height + 1.2e-3
numZ_1    = 1

startr = 0e-3
endr = 2e-2
numr = 2000
dr = (endr-startr)/numr

numTheta = 100
dtTheta = 2*np.pi/numTheta

zArr = np.linspace(startZ_1,  endZ_1, num=numZ_1)
rArr = np.linspace(startr,  endr, num=numr)
theta1Arr = np.linspace(0, 2*np.pi, num=numTheta)
print(np.divide(theta1Arr, np.pi))

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

rotateStart = np.pi/8
rotateNum = 4
rotateEnd = np.pi*(rotateNum-1)/(rotateNum/2) + rotateStart
rotateArr = np.linspace(rotateStart, rotateEnd, rotateNum)

offsetStart = -1e-2
offsetEnd = 1e-2
offsetNum = 201
offsetArr = np.linspace(offsetStart, offsetEnd, offsetNum)

offset_rotated_totalField4_5 = []
offset_rotated_totalField1_5 = []
offset_rotated_totalField4_6 = []
offset_rotated_totalField1_6 = []
for rotation in rotateArr:
  offset_totalField4_5 = []
  offset_totalField1_5 = []
  offset_totalField4_6 = []
  offset_totalField1_6 = []
  rotated_theta1Arr = theta1Arr + rotation
  for offset in offsetArr:
    totalField4_5 = []
    totalField1_5 = []
    totalField4_6 = []
    totalField1_6 = []
    for i, z in enumerate(zArr):
      sumOfField4z_5 = 0
      sumOfField1z_5 = 0
      sumOfField4z_6 = 0
      sumOfField1z_6 = 0
      for j, r in enumerate(rArr):
        if r == 0:
          dA = dr**2*np.pi*(dtTheta/2/np.pi)
        else:
          dA = ((4*r*dr)*np.pi)*(dtTheta/2/np.pi)
        for k, theta in enumerate(rotated_theta1Arr):
          polarity = withinCircuit(r, theta, bottom5, top5, offset) # Change to cartesian
          sumOfField1z_5 += B1[i][k][j]*dA*polarity
          sumOfField4z_5 += B4[i][k][j]*dA*polarity
          polarity = withinCircuit(r, theta, bottom6, top6, offset) # Change to cartesian
          sumOfField1z_6 += B1[i][k][j]*dA*polarity
          sumOfField4z_6 += B4[i][k][j]*dA*polarity
      totalField4_5.append(sumOfField4z_5)  
      totalField1_5.append(sumOfField1z_5)  
      totalField4_6.append(sumOfField4z_6)  
      totalField1_6.append(sumOfField1z_6)  
    offset_totalField4_5.append(totalField4_5)  
    offset_totalField1_5.append(totalField1_5)  
    offset_totalField4_6.append(totalField4_6)  
    offset_totalField1_6.append(totalField1_6)  
  offset_rotated_totalField1_5.append(offset_totalField1_5)  
  offset_rotated_totalField4_5.append(offset_totalField4_5)  
  offset_rotated_totalField1_6.append(offset_totalField1_6)  
  offset_rotated_totalField4_6.append(offset_totalField4_6)  
  
offset_rotated_totalField1_5 = np.array(offset_rotated_totalField1_5)
offset_rotated_totalField4_5 = np.array(offset_rotated_totalField4_5) 
offset_rotated_totalField1_6 = np.array(offset_rotated_totalField1_6)
offset_rotated_totalField4_6 = np.array(offset_rotated_totalField4_6) 

FieldsDict = {'offset_rotated_totalField1_5':offset_rotated_totalField1_5.flatten(),
'offset_rotated_totalField4_5':offset_rotated_totalField4_5.flatten(),
'offset_rotated_totalField1_6':offset_rotated_totalField1_6.flatten(),
'offset_rotated_totalField4_6':offset_rotated_totalField4_6.flatten()}
df = pd.DataFrame(FieldsDict)
df.to_csv(f"capturedMagenticFieldCPW_{offsetStart}-{offsetEnd}-{offsetNum}_{rotateStart}-{rotateEnd}-{rotateNum}_{startZ_1}-{endZ_1}-{numZ_1}.csv")

# # Best settings after experimentation
# img_size = (32, 18)
# font_size = 55

# fig = plt.figure(figsize=img_size)
# font = {'size'   : font_size}
# plt.rc('font', **font)
# plt.rc('xtick', labelsize=font_size) 
# plt.rc('ytick', labelsize=font_size) 
# plt.title('Theoretical X Sweep from rotating Tx Ø 1mm')
# plt.xlabel('Posistion X(mm)')
# plt.ylabel("Rx Peak Voltage (mV)")
# for i, rotation in enumerate(rotateArr):
#   print(f'{int(np.round(rotation*180/np.pi, 0))}: Peak amplitude {offsetArr[np.argmax(offset_rotated_totalField1_5[i])]*1000}mm')
#   plt.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField1_5[i], ZL1)*200, label=f'Rotated {int(np.round(rotation*180/np.pi, 0))}°')
#   # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField4_5[rotation], ZL4)*200, label='4mm')
#   # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField1_2[rotation], ZL1)*200, label='1mm')
#   # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField4_2[rotation], ZL4)*200, label='4mm')
#   # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField1[rotation], ZL1)*200, label='1mm')
#   # ax.plot(np.multiply(offsetArr, 1000), np.divide(offset_rotated_totalField4[rotation], ZL4)*200, label='4mm')
# plt.grid(True, which='major', axis='both', linestyle='-', linewidth=1)
# plt.grid(True, which='minor', axis='both', linestyle='--', linewidth=0.8)
# plt.legend()
# plt.savefig(f'C:\\EMFI_Master\\Figures\\Theoretical_1mmRotationCPW.png', 
#             transparent = False,  
#             facecolor = 'white'
#             )
# plt.show()