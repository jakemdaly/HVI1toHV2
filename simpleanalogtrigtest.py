import sys
import keysightSD1
import matplotlib.pyplot as plt

chassis = 1
slotdig = 9
slotawg = 16
product = ""

dig = keysightSD1.SD_AIN()
awg = keysightSD1.SD_AOU()
digopen = dig.openWithSlot(product, chassis, slotdig)
print(digopen)
awgopen = awg.openWithSlot(product, chassis, slotawg)
print(awgopen)

dig.channelInputConfig(1, 3, keysightSD1.AIN_Impedance.AIN_IMPEDANCE_50, keysightSD1.AIN_Coupling.AIN_COUPLING_AC)
dig.channelTriggerConfig(1, keysightSD1.SD_AIN_TriggerMode.RISING_EDGE, 1)
dig.DAQconfig(1, 1000000, 3, 0, keysightSD1.SD_TriggerModes.ANALOGTRIG)
dig.DAQstart(1)

awg.channelWaveShape(1, keysightSD1.SD_Waveshapes.AOU_SINUSOIDAL)
awg.channelAmplitude(1, 1.5)
awg.channelFrequency(1, 1e6)

arr = []

arr.append(dig.DAQread(1, 30000, 2))
s = [1:30000]

plt.plot(arr)

print(arr)
input()