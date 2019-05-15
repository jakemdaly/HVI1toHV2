import sys
import time
sys.path.append('C:/Program Files (x86)/Keysight/SD1/Libraries/Python')
from hardware_configurator import *
from test_initialization import *
from hvi_configurator import *

# In this example we will run a trigger example that will use HVI to synchronize two modules in a single chassis

# This is the top level module which configures and runs sub-parts:
# triggerExample.py
#   1. test_initialization.py (Test initialization)
#   2. hardware_configurator.py (Hardware configuration)
#   3. hvi_configurator (HVI configuration)

# Create array of module locations [chassis, slot]. Doesn't matter what type of SD1 instrument (dig/awg)
module_array = [[1, 4], [1, 5]]

# Use the inventory function to get more info about modules (instrument type, name, etc.)
module_dict = create_module_inventory(module_array)

# Initialize a test object using the module inventory we just created
HVItriggersync_test = Test_HVItriggersync(module_dict, #dictionary of modules used in the test
                                          4, #master slot
                                          5, #slave slot
                                          1, #master channel
                                          1) #slave channel

# Select one of the waveforms that comes with the SD1 as the waveform that we'll be using in our test
HVItriggersync_test.set_waveform("C:\\Users\\Public\\Documents\\Keysight\\SD1\\Examples\\Waveforms\\Sin_10MHz_50samples_192cycles.csv")

# Configure the hardware for this test
configure_hardware(HVItriggersync_test)

# Load the HVI
configure_hvi(HVItriggersync_test, "simpleHVIsync_5.HVI")

# Start the HVI
HVItriggersync_test.hvi.start()

# Send the triggers
for i in range(0, 50):
    HVItriggersync_test.send_PXI_trigger_pulse(0)
    time.sleep((.1))

# Make sure the HVI stops running
HVItriggersync_test.hvi.stop()