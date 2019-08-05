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
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Gaussian.csv")
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Exponential.csv")
FastBranching_test.add_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Triangular.csv")

# Configure the hardware for this test
configure_hardware(FastBranching_test)

# Load the HVI
configure_hvi(FastBranching_test, "C:\\Users\\Administrator\\PycharmProjects\\HVI1toHV2\\FastBranching_v0_6.HVI")

# Start the HVI
FastBranching_test.hvi.start()

# Send the triggers
for i in range(0, 50):

    waveform_slave = random.randint(1,4)
    waveform_master = random.randint(1,4)
    FastBranching_test.master_module.writeRegisterByNumber(0,waveform_master)
    FastBranching_test.slave_module.writeRegisterByNumber(0,waveform_slave)
    # print("Master wave:{}/Slave wave:{}".format(FastBranching_test.master_module.readRegisterByNumber(0)[1], FastBranching_test.slave_module.readRegisterByNumber(0)[1]))
    print("bleh")
    # FastBranching_test.slave_module.writeRegisterByNumber(7, int(waveform_slave))
    # FastBranching_test.master_module.writeRegisterByNumber(7, int(waveform_master))
    FastBranching_test.send_PXI_trigger_pulse(7, 1)
    # time.sleep(.1)


# Make sure the HVI stops running
FastBranching_test.hvi.stop()