import numpy as np
import pandas as pd

# Note the magnetic field starts from the top of the probe. Meaning if you want the field 1 mm under the probe, z = height + 1

# radius  = 5e-3/2   #4mm diameter (+1mm wire)
radius  = 2e-3/2   #1mm diameter (+1mm wire)
height  = 6e-3  #6mm TODO: Fix height
loops   = 5

#Constants
mu_0  = 1.257e-6  #m kg s**-2 A**-2
current = 1
pi = np.pi
k = mu_0*current/4/pi

startZ  = height + 1.2e-3
endZ    = height + 1.2e-3
numZ = 1
zArr = np.linspace(startZ, endZ, num=numZ)
print(zArr)

# Used in master:
# startr = 0e-3
# endr = 2e-2
# numr = 2001
# numTheta = 100

startr = 0e-3
endr = 50e-3
numr = 1001
rArr = np.linspace(startr,  endr, num=numr)
numTheta = 50
numTheta0 = 20
theta1Arr = np.linspace(0, 2*pi*((numTheta-1)/numTheta), num=numTheta)
thetaArr = []
for theta in theta1Arr:
  thetaArr.append(int(np.round(theta*180/np.pi, 0)))
print(thetaArr)
theta0Arr = np.linspace(0, 2*pi*((numTheta0-1)/numTheta0), num=numTheta0)
dtTheta = 2*np.pi/numTheta
dr = (endr-startr)/numr

dl = (2*radius*np.pi)/numTheta0

# Size of B = sizeOfZ * sizeOfTheta * sizeOfr
# File format <name>_<startZ>-<endZ>-<spaceZ>_<startr>-<endr>-<spacer>_<numTheta>.csv
B = []
for z in zArr:
  Bz = []  
  for theta1 in theta1Arr:
    Br = []
    for r in rArr:
      BrTotal = 0
      for theta0 in theta0Arr:
        for n in range(0,loops,1):
          d   = np.sqrt((r*np.cos(theta1)-radius*np.cos(theta0))**2+(r*np.sin(theta1)-radius*np.sin(theta0))**2)
          z1  = z-n*(height/loops*(theta0/(2*pi)))# if r==0:
          ### TODO: Radius here should be dl, which would be d(length of wire)
          if d==0:
            zComp = 0
            cross=0
          else:
            zComp=np.cos(np.arctan(z1/d))
            if z1<0:
              zComp = zComp*-1
            cross=(np.pi/2-np.arccos(np.clip((radius**2+d**2-r**2)/(2*radius*d), -1, 1)))
            BrTotal += zComp*((np.sin(cross))/(d**2+z1**2))*dl
      Br.append(k*BrTotal)
    Bz.append(Br)
  B.append(Bz)


B = np.array(B)
Bdict = {'B' : B.flatten()}
df = pd.DataFrame(Bdict)
df.to_csv(f"magneticFieldTiltedR{radius}_{startZ}-{endZ}-{numZ}_{startr}-{endr}-{numr}_{numTheta}.csv")