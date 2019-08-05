import sys
import time
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
from hardware_configurator import *
from test_initialization import *
from hvi_configurator import *
import random


# In this example we will run an example where we dynamically queue waveforms in the middle of an HVI sequence

# This is the top level module which configures and runs sub-parts:
# FastBranching.py
#   1. test_initialization.py (Test initialization)
#   2. hardware_configurator.py (Hardware configuration)
#   3. hvi_configurator (HVI configuration)

# Create array of module locations [chassis, slot]. Doesn't matter what type of SD1 instrument (dig/awg)
module_array = [[1, 4], [1, 5]]

# Use the inventory function to get more info about modules (instrument type, name, etc.)
module_dict = create_module_inventory(module_array)

# Initialize a test object using the module inventory we just created
FastBranching_test = Test_FastBranching(module_dict, #dictionary of modules used in the test
                                          4, #master slot
                                          5, #slave slot
                                          1, #master channel
                                          1) #slave channel

# Add waveforms to the waveform array variable of our test
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Sin_10MHz_50samples_192cycles.csv")
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Triangular.csv")
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Gaussian.csv")
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Square.csv")


# Configure the hardware for this test
configure_hardware(FastBranching_test)

# Load the HVI
configure_hvi(FastBranching_test, "C:\\Users\\Administrator\\Documents\\Python\\fastbranching_ex.HVI")


# Initial PXI 7, R7 Settings
FastBranching_test.master_module.PXItriggerWrite(7, 1)
FastBranching_test.master_module.writeRegisterByNumber(7, 0)
FastBranching_test.master_module.writeRegisterByNumber(0, 0)
R7_m = FastBranching_test.master_module.readRegisterByNumber(7)
print("Initial settings:")
print("Reg7_master = ", R7_m[1])
control = input('Press enter to queue and start an AWG WFM using PXI_7 or q to exit: \n')

# Start the HVI
FastBranching_test.hvi.start()

#While loop for PXI triggering
count = 0
while control != 'q':
    wfNum_master = count
    if count >= 3:
        count = 0
    else: count += 1
    FastBranching_test.master_module.writeRegisterByNumber(0, int(wfNum_master))
    FastBranching_test.slave_module.writeRegisterByNumber(0, int(wfNum_master))
    FastBranching_test.master_module.PXItriggerWrite(7, 1)
    FastBranching_test.master_module.PXItriggerWrite(7, 0)

    print("Master wave:{}/Slave wave:{}".format(FastBranching_test.master_module.readRegisterByNumber(0)[1],
                                                FastBranching_test.slave_module.readRegisterByNumber(0)[1]))
    R7_m = FastBranching_test.master_module.readRegisterByNumber(7)
    R7_s = FastBranching_test.slave_module.readRegisterByNumber(7)
    print("Reg7_master = ", R7_m[1])
    time.sleep(.01)
    control = input()

# Make sure the HVI stops running
FastBranching_test.hvi.stop()