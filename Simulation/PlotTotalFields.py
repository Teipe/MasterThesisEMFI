import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd

import sys

def moving_average(data, window_size):
    """
    Smooths the input data using a moving average.

    Parameters:
    data (array-like): The input data to be smoothed.
    window_size (int): The size of the moving window.

    Returns:
    smoothed_data (numpy array): The smoothed data with the same length as the input data.
    """
    if window_size % 2 == 0:
        raise ValueError("Window size must be odd.")

    padding = window_size // 2
    data_padded = np.pad(data, (padding, padding), mode='edge')
    smoothed_data = np.convolve(data_padded, np.ones(window_size) / window_size, mode='valid')
    return smoothed_data

### Removes the smallest value from entire signal, will hopefully make it "connected"
def reduce_to_zero(signal):
    smallestAmplitude = np.amin(np.abs(signal))
    print(smallestAmplitude)
    for i, x in enumerate(signal):
      if x > 0:
        signal[i] -= smallestAmplitude
      else:
        signal[i] += smallestAmplitude
    return signal

def find_pulse_width(signal, axis, multiplier=0.8, sign=-1):
  signal = np.multiply(signal, sign)
  maxAmp = np.amax(signal)
  changes = []
  insidePulse = False
  finished = False
  for i in range(1, len(signal)):
    if not(insidePulse) and signal[i]>=multiplier*maxAmp:
      changes.append(axis[i])
      insidePulse = True
    elif insidePulse and signal[i]<multiplier*maxAmp:  # Check for change in sign
      changes.append(axis[i])
      finished = True
      break
  print(changes)
  if finished:
    return changes[-1] - changes[0]
  else:
    return changes

def find_sign_changes(signal, axis):
    changes = []
    for i in range(1, len(signal)):
        if signal[i] * signal[i-1] < 0:  # Check for change in sign
            changes.append(axis[i])
    return changes


height  = 6e-3
startZ  = height + 1.2e-3
endZ    = height + 1.2e-3
numZ    = 1
startZ_1  = height + 1.2e-3
endZ_1    = height + 1.2e-3
numZ_1    = 1

rotateStart = 3*np.pi/16
# rotateStart = 0
rotateNum = 4
rotateEnd = np.pi*(rotateNum-1)/(rotateNum/2) + rotateStart
if rotateNum == 1:
  rotateArr = [0]
else:
  rotateArr = np.linspace(rotateStart, rotateEnd, rotateNum)

offsetStart = -1.5e-2
offsetEnd = 1.5e-2
offsetNum = 301
# offsetStart = -1.5e-2
# offsetEnd = 1.5e-2
# offsetNum = 101
offsetArr = np.linspace(offsetStart, offsetEnd, offsetNum)

numr = 1001
# df = pd.read_csv(f"{numr}_capturedMagenticField_{offsetStart}-{offsetEnd}-{offsetNum}_{rotateStart}-{rotateEnd}-{rotateNum}_{startZ_1}-{endZ_1}-{numZ_1}.csv")
df = pd.read_csv(f"capturedMagenticField_{offsetStart}-{offsetEnd}-{offsetNum}_{rotateStart}-{rotateEnd}-{rotateNum}_{startZ_1}-{endZ_1}-{numZ_1}.csv")

offset_rotated_totalField4 = np.array(df.offset_rotated_totalField4)
offset_rotated_totalField1 = np.array(df.offset_rotated_totalField1)
offset_rotated_totalField4_2 = np.array(df.offset_rotated_totalField4_2)
offset_rotated_totalField1_2 = np.array(df.offset_rotated_totalField1_2)
offset_rotated_totalField4_5 = np.array(df.offset_rotated_totalField4_5)
offset_rotated_totalField1_5 = np.array(df.offset_rotated_totalField1_5)
offset_rotated_totalField4 = offset_rotated_totalField4.reshape(rotateNum, offsetNum)
offset_rotated_totalField1 = offset_rotated_totalField1.reshape(rotateNum, offsetNum)
offset_rotated_totalField4_2 = offset_rotated_totalField4_2.reshape(rotateNum, offsetNum)
offset_rotated_totalField1_2 = offset_rotated_totalField1_2.reshape(rotateNum, offsetNum)
offset_rotated_totalField4_5 = offset_rotated_totalField4_5.reshape(rotateNum, offsetNum)
offset_rotated_totalField1_5 = offset_rotated_totalField1_5.reshape(rotateNum, offsetNum)

fields = [offset_rotated_totalField4,
offset_rotated_totalField1,
offset_rotated_totalField4_2,
offset_rotated_totalField1_2,
offset_rotated_totalField4_5,
offset_rotated_totalField1_5]
field_names = ['Tx Ø 4mm, Trace 3',
'Tx Ø 1mm, Trace 3',
'Tx Ø 4mm, Trace 4',
'Tx Ø 1mm, Trace 4',
'Tx Ø 4mm, Trace 1',
'Tx Ø 1mm, Trace 1']
rx = ['Trace 3', 'Trace 3', 'Trace 4', 'Trace 4', 'Trace 1', 'Trace 1']

for i, offset_rotated in enumerate(fields):
  # Best settings after experimentation
  img_size = (32, 18)
  font_size = 55

  fig = plt.figure(figsize=img_size)
  font = {'size'   : font_size}
  plt.rc('font', **font)
  plt.rc('xtick', labelsize=font_size) 
  plt.rc('ytick', labelsize=font_size) 
  plt.title(f'Smoothed theoretical X Sweep from {field_names[i]}')
  plt.xlabel('Posistion X(mm)')
  plt.ylabel("Rx Peak Voltage (mV)")


  mu_0  = 1.257e-6  #m kg s**-2 A**-2
  loops = 5
  r1    = 1e-3
  r4    = 2.5e-3
  ZL1   = loops**2*r1**2*np.pi*mu_0/height
  ZL4   = loops**2*r4**2*np.pi*mu_0/height
  if i % 2 == 0:
    Z = ZL4
    TxAmp = 175e3 
  else:
    Z = ZL1
    TxAmp = 150e3 
  # Center around middle
  # Fix polarity
  # Fix size
  for j, rotation in enumerate(rotateArr):
    num_avg = 21
    print(field_names[i])
    print(np.amax(np.divide(moving_average(offset_rotated[j], num_avg), Z)*TxAmp))
    print("pulse width:")
    print(find_pulse_width(np.divide(moving_average(offset_rotated[j], num_avg), Z)*TxAmp, np.multiply(offsetArr, 1000), 0.9))
    print("Pulse changes:")
    print(find_sign_changes(np.divide(moving_average(offset_rotated[j], num_avg), Z)*TxAmp, np.multiply(offsetArr, 1000)))
    plt.plot(np.multiply(offsetArr, 1000), np.divide(moving_average(offset_rotated[j], num_avg), Z)*TxAmp, label=f'Rotated {np.round(rotateArr[j]/np.pi*180, 2)}°')
    # plt.plot(np.multiply(offsetArr, 1000), np.divide(moving_average(offset_rotated[j], num_avg), Z)*TxAmp, label=f'Rotated {int(np.round(rotateArr[j]/np.pi*180))}°')
  plt.grid(True, which='major', axis='both', linestyle='-', linewidth=1)
  plt.grid(True, which='minor', axis='both', linestyle='--', linewidth=0.8)
  plt.legend()
  plt.savefig(f'C:\\EMFI_Master\\Figures\\Theoretical\\33.75_{field_names[i]}_smoothed.png', 
              transparent = False,  
              facecolor = 'white'
              )
  # plt.savefig(f'C:\\EMFI_Master\\Figures\\Theoretical\\Theo_{field_names[i]}.png', 
  #             transparent = False,  
  #             facecolor = 'white'
  #             )
  plt.close()